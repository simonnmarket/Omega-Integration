import tempfile
import unittest
from pathlib import Path

from tools.numeia_source_audit import audit


class NumeiaSourceAuditTests(unittest.TestCase):
    def test_classifies_execution_and_stub_paths_without_running_them(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "candidate.mq5").write_text(
                "CTrade trade;\ntrade.Buy(0.01, _Symbol);\nreturn true;\n",
                encoding="utf-8",
            )
            result = audit(root)
            self.assertTrue(result["read_only"])
            self.assertEqual(result["file_count"], 1)
            self.assertGreaterEqual(result["broker_match_count"], 2)
            self.assertGreaterEqual(result["stub_match_count"], 1)
            self.assertEqual(result["broker_side_effect"], "NONE_AUDIT_ONLY")
            self.assertEqual(result["promotion_status"], "PENDING_ADAPTER_AND_REPLAY")


if __name__ == "__main__":
    unittest.main()
