from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
from typing import Sequence

from .contracts import OrderIntent, Signal, SymbolSpec
from .fake_executor import FakeExecutor
from .line_signal import LineMomentumStrategy
from .risk_gate import RiskCostGate, RiskDecision


class IntegratedCandidate:
    """Single offline path joining line signal, risk gate and fake execution."""

    SOURCE = "OMEGA_INTEGRATED_LINE_CANDIDATE_V1"

    def __init__(self, strategy: LineMomentumStrategy, gate: RiskCostGate, executor: FakeExecutor):
        self.strategy = strategy
        self.gate = gate
        self.executor = executor

    def process(
        self,
        symbol: str,
        event_id: str,
        closes: Sequence[Decimal],
        bid: Decimal,
        ask: Decimal,
        equity: Decimal,
        spec: SymbolSpec,
        generated_at: datetime,
        valid_for: timedelta,
    ) -> tuple[Signal, RiskDecision, OrderIntent | None, object | None]:
        signal = self.strategy.generate(symbol, event_id, closes, generated_at, valid_for)
        decision = self.gate.evaluate(signal, equity, bid, ask, generated_at)
        if not decision.allowed:
            return signal, decision, None, None
        target_value = decision.max_notional
        raw_volume = target_value / (spec.price * spec.contract_size)
        steps = (raw_volume / spec.volume_step).to_integral_value(rounding=ROUND_DOWN)
        volume = min(steps * spec.volume_step, spec.max_volume)
        if volume < spec.min_volume:
            return signal, RiskDecision(
                False, "VOLUME_BELOW_MINIMUM", symbol, signal.signal_id,
                decision.estimated_cost_bps, decision.max_notional,
            ), None, None
        intent = OrderIntent(
            intent_id=f"{self.SOURCE}:{signal.signal_id}",
            symbol=symbol,
            side=signal.direction,
            volume=volume,
            target_value=target_value,
            source=self.SOURCE,
            reason="line_signal_risk_gate_allow",
        )
        return signal, decision, intent, self.executor.execute(intent)
