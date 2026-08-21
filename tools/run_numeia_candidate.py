#!/usr/bin/env python3
"""Run the Numeia portfolio candidate through the fake executor."""

from decimal import Decimal
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.omega_integration.contracts import SymbolSpec
from src.omega_integration.fake_executor import FakeExecutor
from src.omega_integration.numeia_portfolio import NumeiaPortfolioAllocator


def main() -> int:
    weights = {
        "US500": Decimal("0.20"), "GER40": Decimal("0.15"), "UK100": Decimal("0.15"),
        "XAUUSD": Decimal("0.15"), "XAGUSD": Decimal("0.05"), "UKOIL+": Decimal("0.05"),
        "EURUSD": Decimal("0.07"), "GBPUSD": Decimal("0.07"), "USDJPY": Decimal("0.06"),
    }
    specs = {symbol: SymbolSpec(symbol, Decimal("100"), Decimal("1"), Decimal("0.01"), Decimal("0.01"), Decimal("100")) for symbol in weights}
    allocator = NumeiaPortfolioAllocator(weights, Decimal("0.05"))
    intents = allocator.create_initial_intents(Decimal("10000"), specs)
    executor = FakeExecutor()
    results = [executor.execute(intent) for intent in intents]
    report = {
        "candidate": allocator.SOURCE,
        "mode": "FAKE_EXECUTOR",
        "equity": 10000,
        "intents": [intent.__dict__ | {"volume": str(intent.volume), "target_value": str(intent.target_value)} for intent in intents],
        "executions": [result.__dict__ for result in results],
        "broker_access": "NONE",
        "profit": "NOT_EVALUATED",
    }
    output = Path("reports/research/numeia_candidate_fake_run.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"intents": len(intents), "executions": len(results), "broker_access": "NONE"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
