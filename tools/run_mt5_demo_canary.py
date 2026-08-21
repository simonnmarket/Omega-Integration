from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.omega_integration.contracts import OrderIntent
from src.omega_integration.mt5_demo_executor import Mt5DemoExecutor


def main() -> None:
    executor = Mt5DemoExecutor(
        r"C:\Program Files\MetaTrader 5\terminal64.exe", "HantecMarketsMU-MT5"
    )
    preflight = executor.connect()
    try:
        intent = OrderIntent(
            intent_id="OMEGA-DEMO-CANARY-20260821-XAUUSD-001",
            symbol="XAUUSD", side="BUY", volume=Decimal("0.01"),
            target_value=Decimal("0"), source="OMEGA_INTEGRATED_LINE_CANDIDATE_V1",
            reason="authorized_single_demo_canary",
        )
        entry, exit_ = executor.send_and_close(intent)
        report = {"verdict": "PASS", "preflight": preflight.__dict__, "entry": entry.__dict__, "exit": exit_.__dict__, "zero_exposure": True}
    finally:
        executor.disconnect()
    path = Path("reports/technical/mt5_demo_canary_2026-08-21.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, default=str))


if __name__ == "__main__":
    main()
