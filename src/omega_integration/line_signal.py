from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Sequence

from .contracts import Signal


class LineMomentumStrategy:
    """Close/line-only baseline; it never reads OHLC shadows or sends orders."""

    STRATEGY_ID = "LINE_MOMENTUM_BASELINE_V1"

    def __init__(self, fast_period: int = 5, slow_period: int = 20, min_score: Decimal = Decimal("0")):
        if fast_period < 2 or slow_period <= fast_period:
            raise ValueError("require 2 <= fast_period < slow_period")
        if min_score < 0:
            raise ValueError("min_score cannot be negative")
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.min_score = min_score

    def generate(
        self,
        symbol: str,
        event_id: str,
        closes: Sequence[Decimal],
        generated_at: datetime,
        valid_for: timedelta,
    ) -> Signal:
        if len(closes) < self.slow_period:
            raise ValueError("insufficient closed line observations")
        fast = sum(closes[-self.fast_period:], Decimal("0")) / self.fast_period
        slow = sum(closes[-self.slow_period:], Decimal("0")) / self.slow_period
        score = (fast - slow) / slow if slow else Decimal("0")
        if score > self.min_score:
            direction = "BUY"
        elif score < -self.min_score:
            direction = "SELL"
        else:
            direction = "FLAT"
        confidence = min(Decimal("1"), abs(score) / max(self.min_score, Decimal("0.0001")))
        return Signal(
            signal_id=f"{self.STRATEGY_ID}:{symbol}:{event_id}",
            event_id=event_id,
            symbol=symbol,
            strategy_id=self.STRATEGY_ID,
            direction=direction,
            score=score,
            confidence=confidence,
            generated_at=generated_at,
            valid_until=generated_at + valid_for,
            features_ref="close_line_only",
        )
