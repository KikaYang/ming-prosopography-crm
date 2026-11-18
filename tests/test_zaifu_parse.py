"""
Regression test for data/mingshi_zaifu/parse_zaifu.py (2026-11-18).

A continuation line in juan 109 beginning with "文淵閣事" was once read as the
short name of Wang Wen 王文, which truncated the record of Xu Youzhen 徐有貞,
created a false row for Wang Wen and pushed the year alignment cost of juan 109
to about 1000.

Run from the repo root:
    python3 -m unittest tests/test_zaifu_parse.py -v
"""
import collections
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZAIFU = ROOT / "data" / "mingshi_zaifu"
MAX_COST = 100
# (person, year_ce, juan) pairs allowed to occur more than once; none at present.
DUPLICATE_WHITELIST = set()


class TestZaifuParse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = Path(cls.tmp.name)
        for name in ("ms109n.txt", "ms110n.txt"):
            shutil.copy(ZAIFU / "sources" / name, d / name)
        out = subprocess.run([sys.executable, str(ZAIFU / "parse_zaifu.py")],
                             cwd=d, capture_output=True, text=True, check=True).stdout
        cls.costs = {v: float(c) for v, c in re.findall(r"^(109|110) cost ([\d.]+)", out, re.M)}
        cls.rows = json.loads((d / "zaifu.json").read_text(encoding="utf-8"))["rows"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_dp_cost(self):
        self.assertEqual(set(self.costs), {"109", "110"})
        for vol, cost in self.costs.items():
            self.assertLess(cost, MAX_COST, f"juan {vol}: year alignment cost {cost}")

    def assertNoDuplicates(self, keys, where):
        dup = {k: n for k, n in collections.Counter(keys).items()
               if n > 1 and k not in DUPLICATE_WHITELIST}
        self.assertEqual(dup, {}, f"{where}: (person, year, juan) occurs more than once")

    def test_no_duplicate_person_year_parsed(self):
        self.assertNoDuplicates(((r["person"], str(r["year"]), r["vol"]) for r in self.rows),
                                "parse_zaifu.py output")

    def test_no_duplicate_person_year_csv(self):
        with open(ZAIFU / "mingshi_zaifu_long.csv", encoding="utf-8-sig") as f:
            keys = [(r["person_trad"], r["year_ce"], r["mingshi_juan"]) for r in csv.DictReader(f)]
        self.assertNoDuplicates(keys, "mingshi_zaifu_long.csv")


if __name__ == "__main__":
    unittest.main()
