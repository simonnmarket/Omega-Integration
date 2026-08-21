import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from src.omega_integration.candidate_pipeline import IntegratedCandidate
from src.omega_integration.contracts import SymbolSpec
from src.omega_integration.fake_executor import FakeExecutor
from src.omega_integration.line_signal import LineMomentumStrategy
from src.omega_integration.risk_gate import RiskCostGate


class IntegratedCandidateTests(unittest.TestCase):
    def test_buy_reaches_fake_executor(self):
        now = datetime.now(timezone.utc)
        candidate = IntegratedCandidate(
            LineMomentumStrategy(2, 3, Decimal("0.001")), RiskCostGate(), FakeExecutor()
        )
        signal, decision, intent, execution = candidate.process(
            "XAUUSD", "e-buy", [Decimal("100"), Decimal("100"), Decimal("101")],
            Decimal("2500"), Decimal("2500.20"), Decimal("10000"),
            SymbolSpec("XAUUSD", Decimal("2500"), Decimal("1"), Decimal("0.01"), Decimal("0.01"), Decimal("10")),
            now, timedelta(minutes=5),
        )
        self.assertEqual(signal.direction, "BUY")
        self.assertTrue(decision.allowed)
        self.assertIsNotNone(intent)
        self.assertEqual(execution.status, "FILLED_FAKE")

    def test_flat_stops_before_order_intent(self):
        now = datetime.now(timezone.utc)
        candidate = IntegratedCandidate(
            LineMomentumStrategy(2, 3, Decimal("0.001")), RiskCostGate(), FakeExecutor()
        )
        _, decision, intent, execution = candidate.process(
            "EURUSD", "e-flat", [Decimal("1"), Decimal("1"), Decimal("1")],
            Decimal("1.1"), Decimal("1.1001"), Decimal("10000"),
            SymbolSpec("EURUSD", Decimal("1.1"), Decimal("100000"), Decimal("0.01"), Decimal("0.01"), Decimal("10")),
            now, timedelta(minutes=5),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "SIGNAL_FLAT")
        self.assertIsNone(intent)
        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()
