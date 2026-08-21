import tempfile
import unittest
from pathlib import Path

from tools.forensic_log_parser import parse


class ForensicLogParserTests(unittest.TestCase):
    def test_separates_scan_attempt_and_trade_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.log"
            path.write_text(
                "2025-01-01 00:00:00,000 - INFO - Scan completo. Trades: 0\n"
                "2025-01-01 00:00:01,000 - DEBUG - order_send retcode=10016, comment=Invalid stops\n"
                "2025-01-01 00:00:02,000 - INFO - Scan completo. Trades: 0\n",
                encoding="utf-8",
            )
            result = parse(path)
            self.assertEqual(result["lines"], 3)
            self.assertEqual(result["events"]["scan_cycle"], 2)
            self.assertEqual(result["events"]["order_attempt_or_rejection"], 1)
            self.assertEqual(result["trade_count_max_reported"], 0)
            self.assertEqual(result["broker_access"], "NOT_PERFORMED_PARSER_ONLY")


if __name__ == "__main__":
    unittest.main()
