import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from src.omega_integration.line_signal import LineMomentumStrategy
from src.omega_integration.risk_gate import RiskCostGate


class RiskGateTests(unittest.TestCase):
    def setUp(self):
        now = datetime.now(timezone.utc)
        self.now = now
        self.signal = LineMomentumStrategy(2, 3, Decimal("0.001")).generate(
            "XAUUSD", "e1", [Decimal("100"), Decimal("100"), Decimal("101")],
            now, timedelta(minutes=5)
        )

    def test_allows_valid_signal_and_quote(self):
        decision = RiskCostGate().evaluate(
            self.signal, Decimal("10000"), Decimal("2500.00"), Decimal("2500.20"), self.now
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "ALLOW")

    def test_denies_expired_signal_and_excessive_spread(self):
        expired = self.signal.__class__(
            **{**self.signal.__dict__, "valid_until": self.now - timedelta(seconds=1)}
        )
        decision = RiskCostGate().evaluate(
            expired, Decimal("10000"), Decimal("2500"), Decimal("2510"), self.now
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "SIGNAL_EXPIRED")

    def test_denies_flat_signal(self):
        flat = LineMomentumStrategy(2, 3, Decimal("0.10")).generate(
            "XAUUSD", "e2", [Decimal("100"), Decimal("100"), Decimal("100")],
            self.now, timedelta(minutes=5)
        )
        decision = RiskCostGate().evaluate(
            flat, Decimal("10000"), Decimal("2500"), Decimal("2500.20"), self.now
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "SIGNAL_FLAT")


if __name__ == "__main__":
    unittest.main()
