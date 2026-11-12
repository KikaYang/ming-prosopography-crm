"""
docs/modelling/identifiers_glossary_en.md: the table must match the models (docs/modelling/*.ttl),
name_glosses_en.csv and glossary_basis_en.csv.

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

    def test_untagged_label_goes_to_chinese_column(self):
        # name:date-cbdb-421880 carries a CBDB field value without a language tag (D9 exception)
        self.assertIn("| `name:date-cbdb-421880` | 1532 |", naming_table.table())

    def test_every_name_node_and_time_span_is_listed(self):
        text = naming_table.table()
        self.assertIn("| `name:zhang-fujing` | 張孚敬 | Zhang Fujing", text)
        self.assertIn("| `ts:jj13-03-jimao` | 嘉靖十三年三月己卯 | Jiajing 13, 3rd month, day jimao |", text)

    def test_every_type_has_an_explanation(self):
        rows = [l for l in naming_table.table().splitlines() if l.startswith("| `type:")]
        self.assertTrue(rows)
        for row in rows:
            self.assertNotEqual(row.split(" | ")[3], "—", row)


if __name__ == "__main__":
    unittest.main()
