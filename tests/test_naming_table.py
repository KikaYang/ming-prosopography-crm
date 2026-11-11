"""
docs/modelling/naming_en.md: the identifier table must match the labels in docs/modelling/*.ttl.

Run from the repo root:
    python3 -m unittest tests/test_naming_table.py -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import naming_table  # noqa: E402


class TestNamingTable(unittest.TestCase):
    def test_table_up_to_date(self):
        self.assertEqual(naming_table.main(["--check"]), 0, "run scripts/naming_table.py")


if __name__ == "__main__":
    unittest.main()
