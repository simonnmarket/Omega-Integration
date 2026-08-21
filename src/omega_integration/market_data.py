from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable, Mapping


@dataclass(frozen=True)
class MarketEvent:
    event_id: str
    symbol: str
    asset_class: str
    timestamp: datetime
    bid: Decimal
    ask: Decimal
    last: Decimal | None
    volume: Decimal | None
    source: str
    timeframe: str
    closed: bool


class MarketDataValidationError(ValueError):
    pass


class NormalizedMarketData:
    """Strict in-memory boundary between a data source and OMEGA components."""

    def __init__(self, allowed_symbols: Mapping[str, str]):
        self._allowed_symbols = dict(allowed_symbols)

    def normalize(self, row: Mapping[str, object]) -> MarketEvent:
        required = (
            "event_id", "symbol", "asset_class", "timestamp", "bid", "ask",
            "source", "timeframe", "closed",
        )
        missing = [key for key in required if key not in row]
        if missing:
            raise MarketDataValidationError(f"missing fields: {','.join(missing)}")

        symbol = str(row["symbol"])
        asset_class = str(row["asset_class"])
        if symbol not in self._allowed_symbols:
            raise MarketDataValidationError(f"symbol not allowlisted: {symbol}")
        if self._allowed_symbols[symbol] != asset_class:
            raise MarketDataValidationError(f"asset class mismatch: {symbol}")

        try:
            timestamp = datetime.fromisoformat(str(row["timestamp"]).replace("Z", "+00:00"))
            bid = Decimal(str(row["bid"]))
            ask = Decimal(str(row["ask"]))
        except (TypeError, ValueError, ArithmeticError) as exc:
            raise MarketDataValidationError(f"invalid market values: {exc}") from exc
        if bid <= 0 or ask <= 0 or ask < bid:
            raise MarketDataValidationError("invalid quote: require 0 < bid <= ask")

        last = self._optional_decimal(row.get("last"), "last")
        volume = self._optional_decimal(row.get("volume"), "volume")
        if volume is not None and volume < 0:
            raise MarketDataValidationError("volume cannot be negative")
        if not isinstance(row["closed"], bool):
            raise MarketDataValidationError("closed must be boolean")

        return MarketEvent(
            event_id=str(row["event_id"]),
            symbol=symbol,
            asset_class=asset_class,
            timestamp=timestamp,
            bid=bid,
            ask=ask,
            last=last,
            volume=volume,
            source=str(row["source"]),
            timeframe=str(row["timeframe"]),
            closed=row["closed"],
        )

    def normalize_many(self, rows: Iterable[Mapping[str, object]]) -> list[MarketEvent]:
        return [self.normalize(row) for row in rows]

    @staticmethod
    def _optional_decimal(value: object, name: str) -> Decimal | None:
        if value is None:
            return None
        try:
            return Decimal(str(value))
        except (TypeError, ValueError, ArithmeticError) as exc:
            raise MarketDataValidationError(f"invalid {name}") from exc
