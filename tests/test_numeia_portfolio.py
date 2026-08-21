import unittest
from decimal import Decimal

from src.omega_integration.fake_executor import FakeExecutor
from src.omega_integration.contracts import SymbolSpec
from src.omega_integration.numeia_portfolio import NumeiaPortfolioAllocator


class NumeiaPortfolioIntegrationTests(unittest.TestCase):
    def test_initial_allocation_emits_intents_and_fake_lifecycle(self):
        weights = {
            "XAUUSD": Decimal("0.15"),
            "EURUSD": Decimal("0.07"),
            "US500": Decimal("0.20"),
        }
        allocator = NumeiaPortfolioAllocator(weights, cash_weight=Decimal("0.58"))
        specs = {
            symbol: SymbolSpec(symbol, Decimal("100"), Decimal("1"), Decimal("0.01"), Decimal("0.01"), Decimal("100"))
            for symbol in weights
        }
        intents = allocator.create_initial_intents(Decimal("10000"), specs)
        self.assertEqual(len(intents), 3)
        executor = FakeExecutor()
        results = [executor.execute(intent) for intent in intents]
        self.assertEqual(len(results), 3)
        self.assertTrue(all(item.status == "FILLED_FAKE" for item in results))

    def test_weight_mismatch_is_rejected(self):
        with self.assertRaises(ValueError):
            NumeiaPortfolioAllocator({"XAUUSD": Decimal("0.15")}, Decimal("0.15"))


if __name__ == "__main__":
    unittest.main()
