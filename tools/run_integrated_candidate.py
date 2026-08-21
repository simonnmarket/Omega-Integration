from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.omega_integration.candidate_pipeline import IntegratedCandidate
from src.omega_integration.contracts import SymbolSpec
from src.omega_integration.fake_executor import FakeExecutor
from src.omega_integration.line_signal import LineMomentumStrategy
from src.omega_integration.risk_gate import RiskCostGate


def main() -> None:
    now = datetime.now(timezone.utc)
    candidate = IntegratedCandidate(
        LineMomentumStrategy(2, 3, Decimal("0.001")), RiskCostGate(), FakeExecutor()
    )
    cases = [
        ("XAUUSD", "e-buy", [Decimal("100"), Decimal("100"), Decimal("101")], Decimal("2500"), Decimal("2500.20")),
        ("EURUSD", "e-flat", [Decimal("1"), Decimal("1"), Decimal("1")], Decimal("1.1"), Decimal("1.1001")),
    ]
    spec = {
        "XAUUSD": SymbolSpec("XAUUSD", Decimal("2500"), Decimal("1"), Decimal("0.01"), Decimal("0.01"), Decimal("10")),
        "EURUSD": SymbolSpec("EURUSD", Decimal("1.1"), Decimal("100000"), Decimal("0.01"), Decimal("0.01"), Decimal("10")),
    }
    results = []
    for symbol, event_id, closes, bid, ask in cases:
        signal, decision, intent, execution = candidate.process(
            symbol, event_id, closes, bid, ask, Decimal("10000"), spec[symbol], now, timedelta(minutes=5)
        )
        results.append({
            "symbol": symbol,
            "direction": signal.direction,
            "gate": decision.reason,
            "intent_id": intent.intent_id if intent else None,
            "execution_status": execution.status if execution else None,
        })
    report = {
        "candidate": "OMEGA_INTEGRATED_LINE_CANDIDATE_V1",
        "mode": "FAKE_EXECUTOR",
        "broker_access": "NONE",
        "results": results,
        "economic_result": "NOT_EVALUATED",
    }
    output = Path("reports/research/integrated_candidate_fake_run.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
