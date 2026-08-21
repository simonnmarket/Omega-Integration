import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from src.omega_integration.line_signal import LineMomentumStrategy


class LineSignalTests(unittest.TestCase):
    def test_line_only_strategy_generates_buy_without_ohlc(self):
        now = datetime.now(timezone.utc)
        closes = [Decimal("100") for _ in range(19)] + [Decimal("110")]
        signal = LineMomentumStrategy(5, 20, Decimal("0.001")).generate(
            "XAUUSD", "e1", closes, now, timedelta(minutes=5)
        )
        self.assertEqual(signal.direction, "BUY")
        self.assertEqual(signal.features_ref, "close_line_only")
        self.assertEqual(signal.valid_until, now + timedelta(minutes=5))

    def test_insufficient_line_history_is_rejected(self):
        with self.assertRaises(ValueError):
            LineMomentumStrategy().generate(
                "EURUSD", "e1", [Decimal("1.1")] * 5,
                datetime.now(timezone.utc), timedelta(minutes=5)
            )


if __name__ == "__main__":
    unittest.main()
