from __future__ import annotations

from decimal import Decimal, ROUND_DOWN

from .contracts import OrderIntent, SymbolSpec


class NumeiaPortfolioAllocator:
    """Contract-level reproduction of Numeia v5.1 allocation behavior.

    This class calculates intents only. It never imports or calls a broker API.
    """

    SOURCE = "NUMEIA_V5_1_PORTFOLIO_CANDIDATE"

    def __init__(self, weights: dict[str, Decimal], cash_weight: Decimal = Decimal("0.05")) -> None:
        if not weights:
            raise ValueError("weights cannot be empty")
        if any(value < 0 for value in weights.values()):
            raise ValueError("weights cannot be negative")
        total = sum(weights.values(), cash_weight)
        if abs(total - Decimal("1")) > Decimal("0.000001"):
            raise ValueError(f"weights plus cash must equal 1.0, got {total}")
        self.weights = dict(weights)
        self.cash_weight = cash_weight

    @staticmethod
    def _normalize_volume(value: Decimal, spec: SymbolSpec) -> Decimal:
        if value < spec.min_volume:
            return Decimal("0")
        steps = (value / spec.volume_step).to_integral_value(rounding=ROUND_DOWN)
        normalized = steps * spec.volume_step
        return min(normalized, spec.max_volume)

    def create_initial_intents(self, equity: Decimal, specs: dict[str, SymbolSpec]) -> list[OrderIntent]:
        if equity <= 0:
            raise ValueError("equity must be positive")
        intents: list[OrderIntent] = []
        for symbol, weight in self.weights.items():
            if symbol not in specs:
                raise KeyError(f"missing symbol specification: {symbol}")
            spec = specs[symbol]
            target_value = equity * weight
            raw_volume = target_value / (spec.price * spec.contract_size)
            volume = self._normalize_volume(raw_volume, spec)
            if volume <= 0:
                continue
            intents.append(
                OrderIntent(
                    intent_id=f"{self.SOURCE}:INIT:{symbol}",
                    symbol=symbol,
                    side="BUY",
                    volume=volume,
                    target_value=target_value,
                    source=self.SOURCE,
                    reason="initial_target_weight",
                )
            )
        return intents
