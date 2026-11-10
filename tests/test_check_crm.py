"""
Tests for scripts/check_crm.py: deliberately broken snippets must be caught.

Run from the repo root:
    python3 -m unittest tests/test_check_crm.py -v
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from rdflib import Graph

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_crm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
# the project prefixes (D8), copied from the one shared file
PREFIXES = (ROOT / "docs" / "modelling" / "prefixes.ttl").read_text(encoding="utf-8") + "\n"

# A correct snippet in the style of docs/modelling (D1–D3): joining the cabinet with
# a PC144 role, a time-span, an mpv: property with domain/range, an mpv: subclass.
VALID = PREFIXES + """
person:zhang-cong a crm:E21_Person ;
    crm:P1_is_identified_by name:zhang-fujing .
name:zhang-fujing a crm:E41_Appellation ;
    crm:P190_has_symbolic_content "張孚敬" .
group:neige a crm:E74_Group .
type:daxueshi a crm:E55_Type .
event:join-neige a crm:E85_Joining ;
    crm:P143_joined person:zhang-cong ;
    crm:P144_joined_with group:neige ;
    crm:P4_has_time-span ts:jj07-06 .
pc:join-neige a crm:PC144_joined_with ;
    crm:P01_has_domain event:join-neige ;
    crm:P02_has_range group:neige ;
    crm:P144.1_kind_of_member type:daxueshi .
ts:jj07-06 a crm:E52_Time-Span ;
    crm:P82a_begin_of_the_begin "1528-07-17"^^xsd:date .

mpv:TitleConferral rdfs:subClassOf crm:E7_Activity .
mpv:conferred_title a rdf:Property ;
    rdfs:domain crm:E7_Activity ;
    rdfs:range crm:E55_Type .
type:shaofu a crm:E55_Type .
event:confer-shaofu a mpv:TitleConferral ;
    crm:P14_carried_out_by person:shizong ;
    mpv:conferred_title type:shaofu ;
    crm:P4_has_time-span ts:jj07-06 .
person:shizong a crm:E21_Person .
"""

ONTO = check_crm.Ontology()


def run(ttl):
    g = Graph()
    g.parse(data=ttl, format="turtle")
    return check_crm.check(g, ONTO)


def found(issues, level, chk, *words):
    return [i for i in issues if i.level == level and i.check == chk
            and all(w in i.message for w in words)]


class TestValid(unittest.TestCase):
    def test_valid_snippet_has_no_errors_or_warnings(self):
        issues = run(VALID)
        self.assertEqual(issues, [], "\n".join(i.message for i in issues))


class TestA_Existence(unittest.TestCase):
    def test_misspelled_property_from_apis(self):
        # APIS writes P145_seperated; CRM 7.1.3 has P145_separated
        issues = run(PREFIXES + """
            event:e1 a crm:E86_Leaving ; crm:P145_seperated person:p1 .
            person:p1 a crm:E21_Person .""")
        hit = found(issues, check_crm.ERROR, "a", "P145_seperated")
        self.assertTrue(hit)
        self.assertIn("P145_separated", hit[0].message)   # suggestion offered

    def test_unknown_class(self):
        issues = run(PREFIXES + "event:x1 a crm:E999_Office .")
        self.assertTrue(found(issues, check_crm.ERROR, "a", "E999_Office"))

    def test_class_used_as_predicate(self):
        issues = run(PREFIXES + "event:x1 a crm:E21_Person ; crm:E55_Type event:y1 .")
        self.assertTrue(found(issues, check_crm.ERROR, "a", "是类，却用作谓语"))

    def test_property_used_as_type(self):
        issues = run(PREFIXES + "event:x1 a crm:P14_carried_out_by .")
        self.assertTrue(found(issues, check_crm.ERROR, "a", "是属性，却用作 rdf:type"))


class TestB_DomainRange(unittest.TestCase):
    def test_domain_violation(self):
        # P14 carried out by: domain E7 Activity; a Time-Span is not an activity
        issues = run(PREFIXES + """
            ts:t1 a crm:E52_Time-Span ; crm:P14_carried_out_by person:p1 .
            person:p1 a crm:E21_Person .""")
        self.assertTrue(found(issues, check_crm.ERROR, "b", "主语", "E52_Time-Span"))

    def test_range_violation(self):
        # P14 range E39 Actor; a Group is an actor, a Type is not
        issues = run(PREFIXES + """
            event:a1 a crm:E7_Activity ; crm:P14_carried_out_by type:t1 .
            type:t1 a crm:E55_Type .""")
        self.assertTrue(found(issues, check_crm.ERROR, "b", "宾语", "E55_Type"))

    def test_subclass_accepted(self):
        # E85 Joining ⊑ E7 Activity, E74 Group ⊑ E39 Actor: no error
        issues = run(PREFIXES + """
            event:j1 a crm:E85_Joining ; crm:P14_carried_out_by group:g1 .
            group:g1 a crm:E74_Group .""")
        self.assertEqual(found(issues, check_crm.ERROR, "b"), [])

    def test_ex_subclass_followed(self):
        issues = run(PREFIXES + """
            mpv:Office rdfs:subClassOf crm:E55_Type .
            event:a1 a crm:E7_Activity ; crm:P2_has_type type:o1 .
            type:o1 a mpv:Office .""")
        self.assertEqual(found(issues, check_crm.ERROR, "b"), [])

    def test_literal_where_entity_expected(self):
        issues = run(PREFIXES + 'person:p1 a crm:E21_Person ; crm:P1_is_identified_by "張璁" .')
        self.assertTrue(found(issues, check_crm.ERROR, "b", "字面量"))

    def test_entity_where_literal_expected(self):
        issues = run(PREFIXES + "person:p1 a crm:E21_Person ; crm:P3_has_note doc:note1 .")
        self.assertTrue(found(issues, check_crm.ERROR, "b", "rdfs:Literal"))

    def test_untyped_node_is_warning_not_error(self):
        issues = run(PREFIXES + "event:a1 a crm:E7_Activity ; crm:P14_carried_out_by person:nobody .")
        self.assertTrue(found(issues, check_crm.WARNING, "b", "没有 rdf:type"))
        self.assertEqual(found(issues, check_crm.ERROR, "b"), [])

    def test_type_outside_crm_is_warning(self):
        issues = run(PREFIXES + """
            event:a1 a crm:E7_Activity ; crm:P14_carried_out_by event:x1 .
            event:x1 a mpv:Official .""")
        self.assertTrue(found(issues, check_crm.WARNING, "b", "不在 CRM 类层级中"))


class TestC_ExtensionProperties(unittest.TestCase):
    def test_missing_range(self):
        issues = run(PREFIXES + """
            mpv:conferred_title a rdf:Property ; rdfs:domain crm:E7_Activity .
            event:a1 a crm:E7_Activity ; mpv:conferred_title type:t1 .
            type:t1 a crm:E55_Type .""")
        hit = found(issues, check_crm.ERROR, "c", "conferred_title", "rdfs:range")
        self.assertTrue(hit)
        self.assertNotIn("rdfs:domain", hit[0].message)

    def test_missing_both(self):
        issues = run(PREFIXES + "event:a1 a crm:E7_Activity ; mpv:held_concurrently event:b1 .")
        self.assertTrue(found(issues, check_crm.ERROR, "c", "rdfs:domain", "rdfs:range"))

    def test_other_namespaces_not_subject_to_c(self):
        # (c) applies to mpv: only; e.g. rdfs:label or a foreign vocabulary is not required to declare
        issues = run(PREFIXES + """
            @prefix foaf: <http://xmlns.com/foaf/0.1/> .
            person:p1 a crm:E21_Person ; foaf:nick "羅峰" .""")
        self.assertEqual(found(issues, check_crm.ERROR, "c"), [])

    def test_ext_ns_option(self):
        g = Graph()
        g.parse(data=PREFIXES + """
            @prefix my: <http://example.org/other#> .
            event:a1 a crm:E7_Activity ; my:p type:t1 ; mpv:q type:t1 .
            type:t1 a crm:E55_Type .""", format="turtle")
        issues = check_crm.check(g, ONTO, "http://example.org/other#")
        self.assertTrue(found(issues, check_crm.ERROR, "c", "my:p"))
        self.assertFalse(found(issues, check_crm.ERROR, "c", "mpv:q"))


class TestD_P4(unittest.TestCase):
    def test_p4_on_pc_node(self):
        # PC0 / PC144 have no superclass, so they are not E2 (cf. SL12_sketch D1-B)
        issues = run(PREFIXES + """
            pc:x1 a crm:PC144_joined_with ; crm:P4_has_time-span ts:t1 .
            ts:t1 a crm:E52_Time-Span .""")
        self.assertTrue(found(issues, check_crm.ERROR, "d", "PC144_joined_with"))

    def test_p4_on_person(self):
        issues = run(PREFIXES + """
            person:p1 a crm:E21_Person ; crm:P4_has_time-span ts:t1 .
            ts:t1 a crm:E52_Time-Span .""")
        self.assertTrue(found(issues, check_crm.ERROR, "d", "E21_Person"))

    def test_p4i_object_must_be_e2(self):
        issues = run(PREFIXES + """
            ts:t1 a crm:E52_Time-Span ; crm:P4i_is_time-span_of group:g1 .
            group:g1 a crm:E74_Group .""")
        self.assertTrue(found(issues, check_crm.ERROR, "d", "E74_Group"))

    def test_p4_reported_once(self):
        # not duplicated as a (b) domain error
        issues = run(PREFIXES + """
            person:p1 a crm:E21_Person ; crm:P4_has_time-span ts:t1 .
            ts:t1 a crm:E52_Time-Span .""")
        self.assertEqual(found(issues, check_crm.ERROR, "b"), [])


class TestCLI(unittest.TestCase):
    def test_exit_code_and_output(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.ttl"
            bad.write_text(PREFIXES + "person:p1 a crm:E21_Person ; crm:P4_has_time-span ts:t1 .\n"
                                      "ts:t1 a crm:E52_Time-Span .", encoding="utf-8")
            good = Path(d) / "good.ttl"
            good.write_text(VALID, encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(check_crm.main([str(bad)]), 1)
                self.assertEqual(check_crm.main([str(good)]), 0)
            self.assertIn("== 错误：1", buf.getvalue())


class TestVocab(unittest.TestCase):
    """--vocab: shared definitions in a separate file are loaded with the case file."""
    VOCAB = PREFIXES + """
        type:t1 a crm:E55_Type .
        group:g1 a crm:E74_Group .
        mpv:conferred_title a rdf:Property ; rdfs:domain crm:E7_Activity ; rdfs:range crm:E55_Type ."""
    CASE = PREFIXES + """
        event:a1 a crm:E7_Activity ; crm:P2_has_type type:t1 ; crm:P14_carried_out_by group:g1 ;
            mpv:conferred_title type:t1 ."""

    def run_cli(self, *vocab_texts):
        with tempfile.TemporaryDirectory() as d:
            case = Path(d) / "case.ttl"; case.write_text(self.CASE, encoding="utf-8")
            args = [str(case)]
            for i, v in enumerate(vocab_texts):
                p = Path(d) / f"vocab{i}.ttl"; p.write_text(v, encoding="utf-8")
                args += ["--vocab", str(p)]
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = check_crm.main(args)
            return code, buf.getvalue()

    def test_without_vocab_types_unknown_and_ext_undeclared(self):
        code, out = self.run_cli()
        self.assertEqual(code, 1)                      # (c): mpv:conferred_title undeclared
        self.assertIn("没有 rdf:type", out)            # (b): type:t1, group:g1 untyped

    def test_with_vocab_clean(self):
        code, out = self.run_cli(self.VOCAB)
        self.assertEqual(code, 0)
        self.assertIn("== 错误：0", out)
        self.assertIn("== 警告：0", out)
        self.assertIn("（案例文件 4 条）", out)

    def test_vocab_repeatable(self):
        first, second = self.VOCAB.split("group:g1")[0], PREFIXES + "group:g1 a crm:E74_Group ."
        rest = PREFIXES + "mpv:conferred_title a rdf:Property ; rdfs:domain crm:E7_Activity ; rdfs:range crm:E55_Type ."
        code, out = self.run_cli(first, second, rest)
        self.assertEqual(code, 0)
        self.assertIn("== 警告：0", out)

    def test_vocab_errors_still_reported(self):
        bad_vocab = self.VOCAB + "\n type:t1 crm:P4_has_time-span ts:t9 . ts:t9 a crm:E52_Time-Span ."
        code, out = self.run_cli(bad_vocab)
        self.assertEqual(code, 1)
        self.assertIn("(d)", out)


class TestSL12WithVocab(unittest.TestCase):
    """Regression: both SL12 versions check clean together with docs/modelling/vocab.ttl."""
    def test_sl12_files(self):
        vocab = ROOT / "docs" / "modelling" / "vocab.ttl"
        for case in ("SL12_event.ttl", "SL12_state.ttl"):
            g = Graph()
            g.parse(ROOT / "docs" / "modelling" / case, format="turtle")
            g.parse(vocab, format="turtle")
            issues = check_crm.check(g, ONTO)
            self.assertEqual(issues, [], f"{case}: " + "; ".join(i.message for i in issues))


if __name__ == "__main__":
    unittest.main()
