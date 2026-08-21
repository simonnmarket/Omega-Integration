from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .contracts import Signal


@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    reason: str
    symbol: str
    signal_id: str
    estimated_cost_bps: Decimal
    max_notional: Decimal


class RiskCostGate:
    """Pure pre-trade gate. It does not alter signals or contact a broker."""

    def __init__(
        self,
        max_spread_bps: Decimal = Decimal("25"),
        max_notional_pct: Decimal = Decimal("0.20"),
    ) -> None:
        if max_spread_bps <= 0:
            raise ValueError("max_spread_bps must be positive")
        if not Decimal("0") < max_notional_pct <= Decimal("1"):
            raise ValueError("max_notional_pct must be in (0, 1]")
        self.max_spread_bps = max_spread_bps
        self.max_notional_pct = max_notional_pct

    def evaluate(
        self,
        signal: Signal,
        equity: Decimal,
        bid: Decimal,
        ask: Decimal,
        now: datetime,
    ) -> RiskDecision:
        if equity <= 0:
            raise ValueError("equity must be positive")
        if bid <= 0 or ask < bid:
            raise ValueError("invalid quote")
        mid = (bid + ask) / Decimal("2")
        spread_bps = ((ask - bid) / mid) * Decimal("10000")
        max_notional = equity * self.max_notional_pct
        reason = "ALLOW"
        allowed = True
        if signal.direction == "FLAT":
            allowed, reason = False, "SIGNAL_FLAT"
        elif now >= signal.valid_until:
            allowed, reason = False, "SIGNAL_EXPIRED"
        elif spread_bps > self.max_spread_bps:
            allowed, reason = False, "SPREAD_ABOVE_LIMIT"
        return RiskDecision(
            allowed=allowed,
            reason=reason,
            symbol=signal.symbol,
            signal_id=signal.signal_id,
            estimated_cost_bps=spread_bps,
            max_notional=max_notional,
        )
