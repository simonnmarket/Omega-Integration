from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from .contracts import OrderIntent


@dataclass(frozen=True)
class Mt5Preflight:
    login: int
    server: str
    trade_mode: int
    balance: Decimal
    equity: Decimal
    symbol: str
    bid: Decimal
    ask: Decimal
    terminal_path: str


@dataclass(frozen=True)
class Mt5Execution:
    ticket: int
    order_id: int
    deal_id: int
    symbol: str
    volume: Decimal
    side: str
    retcode: int
    comment: str
    sent_at: str


class Mt5DemoExecutor:
    """Strict MT5 DEMO adapter. No mock fallback and no REAL-account path."""

    def __init__(self, terminal_path: str, expected_server: str):
        self.terminal_path = Path(terminal_path)
        self.expected_server = expected_server
        self._mt5 = None

    def connect(self) -> Mt5Preflight:
        import MetaTrader5 as mt5

        self._mt5 = mt5
        if not mt5.initialize(path=str(self.terminal_path), timeout=5000):
            raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
        account = mt5.account_info()
        terminal = mt5.terminal_info()
        if account is None or terminal is None:
            self.disconnect()
            raise RuntimeError("MT5 account_info or terminal_info unavailable")
        if int(account.trade_mode) != 0:
            self.disconnect()
            raise RuntimeError("refusing non-DEMO account")
        if str(account.server) != self.expected_server:
            self.disconnect()
            raise RuntimeError(f"unexpected server: {account.server}")
        return self._quote("XAUUSD", account, terminal)

    def send_and_close(self, intent: OrderIntent) -> tuple[Mt5Execution, Mt5Execution]:
        if self._mt5 is None:
            raise RuntimeError("connect() must pass before send")
        mt5 = self._mt5
        if intent.volume != Decimal("0.01"):
            raise ValueError("DEMO canary requires exactly 0.01 volume")
        if intent.side not in {"BUY", "SELL"}:
            raise ValueError("only BUY/SELL can be sent")
        tick = mt5.symbol_info_tick(intent.symbol)
        info = mt5.symbol_info(intent.symbol)
        if tick is None or info is None:
            raise RuntimeError(f"symbol unavailable: {intent.symbol}")
        if not mt5.symbol_select(intent.symbol, True):
            raise RuntimeError(f"symbol_select failed: {intent.symbol}")

        order_type = mt5.ORDER_TYPE_BUY if intent.side == "BUY" else mt5.ORDER_TYPE_SELL
        price = tick.ask if intent.side == "BUY" else tick.bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": intent.symbol,
            "volume": float(intent.volume),
            "type": order_type,
            "price": price,
            "deviation": 50,
            "magic": 20260821,
            "comment": "OMEGA-LINE-CANARY",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": self._filling_mode(info.filling_mode, mt5),
        }
        checked = mt5.order_check(request)
        if checked is None or int(checked.retcode) not in {0, getattr(mt5, "TRADE_RETCODE_DONE", 10009)}:
            raise RuntimeError(f"order_check rejected: {checked} last_error={mt5.last_error()}")
        before_positions = {
            int(p.ticket) for p in (mt5.positions_get(symbol=intent.symbol) or ())
            if int(p.magic) == 20260821
        }
        result = mt5.order_send(request)
        if result is None or int(result.retcode) not in {
            getattr(mt5, "TRADE_RETCODE_DONE", 10009),
            getattr(mt5, "TRADE_RETCODE_PLACED", 10008),
            getattr(mt5, "TRADE_RETCODE_DONE_PARTIAL", 10010),
        }:
            raise RuntimeError(f"order_send rejected: {result} last_error={mt5.last_error()}")
        entry = self._execution(result, intent.symbol, intent.volume, intent.side)
        positions = [
            p for p in (mt5.positions_get(symbol=intent.symbol) or ())
            if int(p.magic) == 20260821 and int(p.ticket) not in before_positions
        ]
        if positions:
            position = positions[0]
            close_side = "SELL" if intent.side == "BUY" else "BUY"
            close_type = mt5.ORDER_TYPE_SELL if close_side == "SELL" else mt5.ORDER_TYPE_BUY
            close_tick = mt5.symbol_info_tick(intent.symbol)
            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": intent.symbol,
                "volume": float(position.volume),
                "type": close_type,
                "position": int(position.ticket),
                "price": close_tick.bid if close_side == "SELL" else close_tick.ask,
                "deviation": 50,
                "magic": 20260821,
                "comment": "OMEGA-LINE-CLOSE",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": self._filling_mode(info.filling_mode, mt5),
            }
            close_check = mt5.order_check(close_request)
            if close_check is None or int(close_check.retcode) not in {0, getattr(mt5, "TRADE_RETCODE_DONE", 10009)}:
                raise RuntimeError(f"close order_check rejected: {close_check}")
            close_result = mt5.order_send(close_request)
            if close_result is None or int(close_result.retcode) not in {
                getattr(mt5, "TRADE_RETCODE_DONE", 10009),
                getattr(mt5, "TRADE_RETCODE_PLACED", 10008),
                getattr(mt5, "TRADE_RETCODE_DONE_PARTIAL", 10010),
            }:
                raise RuntimeError(f"close order rejected: {close_result}")
            exit_execution = self._execution(close_result, intent.symbol, intent.volume, close_side)
        else:
            raise RuntimeError(f"entry accepted without reconciled position: {entry.ticket}")
        remaining = mt5.positions_get(symbol=intent.symbol) or ()
        if any(int(p.magic) == 20260821 for p in remaining):
            raise RuntimeError("zero-exposure check failed after close")
        return entry, exit_execution

    def disconnect(self) -> None:
        if self._mt5 is not None:
            self._mt5.shutdown()
            self._mt5 = None

    def _quote(self, symbol, account, terminal):
        tick = self._mt5.symbol_info_tick(symbol)
        if tick is None:
            raise RuntimeError(f"tick unavailable: {symbol}")
        return Mt5Preflight(
            login=int(account.login), server=str(account.server), trade_mode=int(account.trade_mode),
            balance=Decimal(str(account.balance)), equity=Decimal(str(account.equity)),
            symbol=symbol, bid=Decimal(str(tick.bid)), ask=Decimal(str(tick.ask)),
            terminal_path=str(getattr(terminal, "path", "")),
        )

    @staticmethod
    def _filling_mode(mask, mt5):
        """Convert MT5 symbol filling bitmask to one ORDER_FILLING enum."""
        if int(mask) & 1:
            return mt5.ORDER_FILLING_FOK
        if int(mask) & 2:
            return mt5.ORDER_FILLING_IOC
        return mt5.ORDER_FILLING_RETURN

    @staticmethod
    def _execution(result, symbol, volume, side):
        return Mt5Execution(
            ticket=int(getattr(result, "order", 0) or getattr(result, "deal", 0)),
            order_id=int(getattr(result, "order", 0)), deal_id=int(getattr(result, "deal", 0)),
            symbol=symbol, volume=volume, side=side, retcode=int(result.retcode),
            comment=str(result.comment), sent_at=datetime.now(timezone.utc).isoformat(),
        )
