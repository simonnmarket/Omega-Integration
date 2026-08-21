import unittest
from datetime import timezone
from decimal import Decimal

from src.omega_integration.market_data import MarketDataValidationError, NormalizedMarketData


class MarketDataContractTests(unittest.TestCase):
    def setUp(self):
        self.adapter = NormalizedMarketData({"XAUUSD": "metal", "EURUSD": "fx"})

    def test_normalizes_allowlisted_closed_quote(self):
        event = self.adapter.normalize({
            "event_id": "e1",
            "symbol": "XAUUSD",
            "asset_class": "metal",
            "timestamp": "2026-08-21T10:00:00Z",
            "bid": "2500.10",
            "ask": "2500.20",
            "last": "2500.15",
            "volume": "12",
            "source": "fixture",
            "timeframe": "M5",
            "closed": True,
        })
        self.assertEqual(event.bid, Decimal("2500.10"))
        self.assertTrue(event.closed)
        self.assertEqual(event.timestamp.tzinfo, timezone.utc)

    def test_rejects_symbol_and_quote_violations(self):
        base = {
            "event_id": "e1", "symbol": "XAUUSD", "asset_class": "metal",
            "timestamp": "2026-08-21T10:00:00Z", "bid": "2500.20", "ask": "2500.10",
            "source": "fixture", "timeframe": "M5", "closed": True,
        }
        with self.assertRaises(MarketDataValidationError):
            self.adapter.normalize({**base, "symbol": "BTCUSD"})
        with self.assertRaises(MarketDataValidationError):
            self.adapter.normalize(base)


if __name__ == "__main__":
    unittest.main()
