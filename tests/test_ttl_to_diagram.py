"""
Tests for scripts/ttl_to_diagram.py --vocab: only case-file nodes are drawn,
the vocabulary only supplies classes and labels.

Run from the repo root:
    python3 -m unittest tests/test_ttl_to_diagram.py -v
"""
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ttl_to_diagram  # noqa: E402

PREFIXES = (ROOT / "docs" / "modelling" / "prefixes.ttl").read_text(encoding="utf-8") + "\n"
CASE = PREFIXES + """
event:a1 a crm:E7_Activity ; rdfs:label "授衔"@zh-Hans ;
    mpv:conferred_title type:shaofu .
"""
VOCAB = PREFIXES + """
type:shaofu a crm:E55_Type ; rdfs:label "少傅"@zh-Hant , "Junior Mentor"@en .
type:unused a crm:E55_Type ; rdfs:label "不应出现"@zh-Hans .
"""
ONTO = ttl_to_diagram.Ontology()


def dot_for(case_text, *vocab_texts):
    case = Graph().parse(data=case_text, format="turtle")
    full = Graph()
    full += case
    for v in vocab_texts:
        full.parse(data=v, format="turtle")
    src, n_edges, n_nodes = ttl_to_diagram.to_dot(full, list(case), ONTO, "t")
    return src, n_edges, n_nodes


class TestVocabLookup(unittest.TestCase):
    def test_labels_and_class_from_vocab(self):
        src, _, _ = dot_for(CASE, VOCAB)
        self.assertIn("type:shaofu", src)
        self.assertIn("少傅", src)
        self.assertIn("Junior Mentor", src)
        self.assertIn("E55_Type", src)

    def test_vocab_only_nodes_not_drawn(self):
        src, _, n_nodes = dot_for(CASE, VOCAB)
        self.assertNotIn("type:unused", src)
        self.assertNotIn("不应出现", src)
        self.assertEqual(n_nodes, 2)          # event:a1, type:shaofu

    def test_without_vocab_node_drawn_but_unlabelled(self):
        src, _, n_nodes = dot_for(CASE)
        self.assertEqual(n_nodes, 2)
        self.assertNotIn("少傅", src)
        self.assertNotIn("E55_Type", src)

    def test_same_edges_with_and_without_vocab(self):
        self.assertEqual(dot_for(CASE)[1], dot_for(CASE, VOCAB)[1])


@unittest.skipUnless(shutil.which("dot") or Path("/opt/homebrew/bin/dot").exists(), "Graphviz dot not installed")
class TestCLI(unittest.TestCase):
    def test_vocab_option_repeatable(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "case.ttl").write_text(CASE, encoding="utf-8")
            (d / "v1.ttl").write_text(PREFIXES + 'type:shaofu a crm:E55_Type .', encoding="utf-8")
            (d / "v2.ttl").write_text(PREFIXES + 'type:shaofu rdfs:label "少傅"@zh-Hant .', encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                ttl_to_diagram.main([str(d / "case.ttl"), "--vocab", str(d / "v1.ttl"),
                                     "--vocab", str(d / "v2.ttl"), "--out", str(d / "out")])
            src = (d / "out" / "case.dot").read_text(encoding="utf-8")
            self.assertTrue((d / "out" / "case.png").exists())
            self.assertIn("少傅", src)
            self.assertIn("E55_Type", src)
            self.assertIn("类名与标签另查 v1.ttl、v2.ttl", src)


if __name__ == "__main__":
    unittest.main()
