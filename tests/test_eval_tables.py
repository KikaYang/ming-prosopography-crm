"""
The evaluation tables in data/evaluation/ must be exactly what scripts/eval/ generates
(base + OVERRIDES), and the evidence checks must actually catch wrong evidence.

Run from the repo root:
    python3 -m unittest tests/test_eval_tables.py -v
"""
import copy
import importlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "eval"))
import common  # noqa: E402
import cq  # noqa: E402

CASES = [importlib.import_module(m) for m in ("sl11", "sl14", "sl12")]
HAVE_DB = common.DB_PATH.exists()


class TestTablesReproduced(unittest.TestCase):
    def test_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            for case in CASES:
                for p in common.write(case, d, verify=True):
                    self.assertEqual(p.read_bytes(), (common.EVAL / p.name).read_bytes(),
                                     f"{p.name} differs from the generated table: change scripts/eval/, not the table")

    def test_overrides_well_formed(self):
        for case in CASES:
            for o in case.OVERRIDES:
                self.assertEqual(len(o), 7, o)
                self.assertIn(o[2], common.OPS, o)
                self.assertRegex(o[4], r"^\d{4}-\d{2}-\d{2}$", o)


class TestVerifiersCatchErrors(unittest.TestCase):
    def tables(self, case):
        return copy.deepcopy(common.build(case))

    def test_missing_triple(self):
        case = CASES[1]
        t = self.tables(case)
        t["event"][0]["ttl_evidence"] = "event:jj13-03-jimao-sheng crm:P4_has_time-span ts:no-such-day"
        with self.assertRaises(AssertionError):
            common.verify_models(case, t)

    @unittest.skipUnless(HAVE_DB, "CBDB SQLite not present")
    def test_wrong_cbdb_value(self):
        for bad in ("POSTED_TO_OFFICE_DATA posting_id 424200 c_firstyear=1535",
                    "POSTED_TO_OFFICE_DATA posting_id 424201（CBDB_line_ID 133447）c_office_id=70951 提調學校 1534–1539",
                    "POSTED_TO_ADDR_DATA posting_id 424200 c_addr_id=5576 黃州府",
                    "BIOG_MAIN c_personid 68547 c_name_chn=徐阶",
                    "SOME_TABLE row 1"):
            with self.subTest(bad=bad), self.assertRaises(AssertionError):
                common.verify_cbdb([{"unit_id": "x", "cbdb_evidence": bad}])

    @unittest.skipUnless(HAVE_DB, "CBDB SQLite not present")
    def test_wrong_sl12_cbdb_value(self):
        for bad in ("POSTED_TO_OFFICE_DATA posting_id 421871（少傅，1528–1533）",
                    "POSTED_TO_OFFICE_DATA posting_id 421871（少保，1528–1534）",
                    "POSTED_TO_OFFICE_DATA posting_id 421871 少傅(1528–)",
                    "POSTED_TO_OFFICE_DATA posting_id 421736（吏部尚書，1526–1529）",   # 杨一清's, not 张璁's
                    "POSTED_TO_OFFICE_DATA posting_id 421882/421883 c_firstyear=1534, c_fy_nh_year=嘉靖12",
                    "POSTED_TO_OFFICE_DATA posting_id 421882 c_notes = “(明實錄:世宗實錄;150卷)”",
                    "POSTED_TO_OFFICE_DATA posting_id 999999999 的 c_lastyear",
                    "ALTNAME_DATA c_alt_name_chn = 張璁（别名、曾用名）",
                    "BIOG_MAIN.c_name_chn = 張孚敬",
                    "POSTED_TO_OFFICE_DATA somewhere"):
            with self.subTest(bad=bad), self.assertRaises(AssertionError):
                common.verify_cbdb_sl12([{"unit_id": "x", "cbdb_evidence": bad}])

    @unittest.skipUnless(HAVE_DB, "CBDB SQLite not present")
    def test_correct_cbdb_value(self):
        common.verify_cbdb([{"unit_id": "x", "cbdb_evidence":
                             "POSTED_TO_OFFICE_DATA posting_id 424200 c_firstyear=1534 c_fy_nh_code=650 c_fy_nh_year=13"}])


class TestCompetencyQuestions(unittest.TestCase):
    def test_questions_frozen_at_tag(self):
        frozen = common.git_show("cq-v1", "data/evaluation/competency_questions.csv").encode("utf-8")
        self.assertEqual(frozen, (common.EVAL / "competency_questions.csv").read_bytes())

    def test_raw_results_reproduced(self):
        with tempfile.TemporaryDirectory() as d:
            cq.run_all(d)
            produced = sorted((Path(d) / "cq_raw").iterdir())
            self.assertEqual(len(produced), len(list(cq.QUERIES.iterdir())) if HAVE_DB else len(list(cq.QUERIES.glob("*.rq"))))
            for p in produced:
                self.assertEqual(p.read_bytes(), (common.EVAL / "cq_raw" / p.name).read_bytes(), p.name)

    def test_results_table_reproduced(self):
        self.assertEqual(cq.results(), (common.EVAL / "cq_results.csv").read_bytes(),
                         "cq_results.csv differs from the generated table: change scripts/eval/cq.py, not the table")


class TestEvaluatedVersions(unittest.TestCase):
    """evaluated_versions/<tag>/ must be verbatim copies of the files at <tag>; checked only where
    the git history with that tag is available."""
    def test_identical_to_tags(self):
        files = sorted(p for p in common.EVALUATED_VERSIONS.rglob("*") if p.is_file())
        self.assertTrue(files)
        tags = {p.relative_to(common.EVALUATED_VERSIONS).parts[0] for p in files}
        have = {t for t in tags if common.subprocess.run([common.GIT, "rev-parse", "-q", "--verify", f"refs/tags/{t}"],
                                                            cwd=ROOT, capture_output=True).returncode == 0}
        if not have:
            self.skipTest("no git history with the evaluation tags")
        for p in files:
            tag, *rest = p.relative_to(common.EVALUATED_VERSIONS).parts
            if tag in have:
                git = common.subprocess.run([common.GIT, "show", f"{tag}:{'/'.join(rest)}"], cwd=ROOT,
                                            capture_output=True, check=True).stdout
                self.assertEqual(git, p.read_bytes(), str(p))


if __name__ == "__main__":
    unittest.main()
