"""
Draw a Turtle file as a relationship diagram (rdflib + Graphviz → PNG).

Usage (from the repo root, with .venv active):
    python scripts/ttl_to_diagram.py docs/modelling/SL12_event.ttl
    python scripts/ttl_to_diagram.py docs/modelling/SL12_event.ttl --since cf9cc87
    python scripts/ttl_to_diagram.py docs/modelling/SL12_event.ttl --vocab docs/modelling/vocab.ttl

    --since COMMIT   only the triples added after COMMIT (compared with the file as it was
                     at COMMIT, via git); nodes that already existed are drawn dashed
    --out DIR        output directory (default docs/modelling/diagrams/)
    --comments       also draw rdfs:comment literals (left out by default)
    --vocab FILE     shared vocabulary (e.g. docs/modelling/vocab.ttl), repeatable, as in
                     check_crm.py. Only nodes that occur in the case file's triples are drawn;
                     the vocabulary is used only to look up their classes and labels.

Nodes show the prefixed ID, class(es) and rdfs:label(s), coloured by CRM class family
(resolved through CIDOC-CRM 7.1.3 subclass relations). Literals are drawn as notes.
rdf:type and rdfs:label are shown inside the nodes, not as edges.
Writes <name>.png and the Graphviz source <name>.dot. Needs Graphviz `dot`.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_crm import CRM, MPV, ROOT, Ontology, superclasses  # noqa: E402

OUT_DIR = ROOT / "docs" / "modelling" / "diagrams"
FONT = "PingFang SC"
LITERAL_MAX = 40

# (legend label, colour, CRM class whose subclasses get this colour); first match wins
FAMILIES = [
    ("时间段 E52", "#fff2cc", CRM["E52_Time-Span"]),
    ("名称 E41", "#cfe2f3", CRM["E41_Appellation"]),
    ("类型 E55", "#eeeeee", CRM["E55_Type"]),
    ("文献 E31/E73", "#ead1dc", CRM["E73_Information_Object"]),
    ("人物 E21", "#f4cccc", CRM["E21_Person"]),
    ("群体 E74", "#fce5cd", CRM["E74_Group"]),
    ("事件 E2", "#d9ead3", CRM["E2_Temporal_Entity"]),
    ("PC 属性类", "#d9d2e9", CRM["PC0_Typed_CRM_Property"]),
]
EXTENSION = ("扩展词汇 mpv:", "#c9daf8")
OTHER = ("其他 / 无类型", "#ffffff")


def git_exe():
    return "/opt/homebrew/bin/git" if Path("/opt/homebrew/bin/git").exists() else "git"


def graph_at(ttl: Path, commit: str) -> Graph:
    """The file as it was at `commit`; empty graph if it did not exist then."""
    rel = ttl.resolve().relative_to(ROOT)
    r = subprocess.run([git_exe(), "-C", str(ROOT), "show", f"{commit}:{rel.as_posix()}"],
                       capture_output=True, text=True)
    g = Graph()
    if r.returncode == 0:
        g.parse(data=r.stdout, format="turtle")
    elif "does not exist" not in r.stderr and "exists on disk, but not in" not in r.stderr:
        sys.exit(f"git show {commit}:{rel} 失败：{r.stderr.strip()}")
    return g


def short(term, g):
    if isinstance(term, BNode):
        return f"_:{str(term)[:6]}"
    s = term.n3(g.namespace_manager)
    return s[len("crm:"):] if s.startswith("crm:") else s


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def family(node, g, onto):
    if isinstance(node, URIRef) and str(node).startswith(MPV):
        return EXTENSION
    types = set(g.objects(node, RDF.type))
    closure = set().union(*(superclasses(t, (onto.g, g)) for t in types)) if types else set()
    for label, colour, cls in FAMILIES:
        if cls in closure:
            return label, colour
    return OTHER


def literal_text(lit: Literal, g):
    text = str(lit)
    if len(text) > LITERAL_MAX:
        text = text[:LITERAL_MAX] + "…"
    if lit.language:
        text += f"\n@{lit.language}"
    elif lit.datatype:
        text += f"\n^^{short(lit.datatype, g)}"
    return text


def to_dot(full: Graph, triples, onto, title, existing=frozenset(), comments=False):
    """`triples` decides what is drawn; `full` (case file + any vocabulary) is only used to
    look up classes, labels and prefixes of the drawn nodes."""
    skip = {RDF.type, RDFS.label} | (set() if comments else {RDFS.comment})
    edges = [(s, p, o) for s, p, o in triples if p not in skip]
    nodes = {s for s, _, _ in triples} | {o for _, _, o in edges if not isinstance(o, Literal)}
    ids = {n: f"n{i}" for i, n in enumerate(sorted(nodes, key=lambda n: short(n, full)))}
    used = {}
    lines = ["digraph G {",
             f'  graph [rankdir=LR, fontname="{FONT}", fontsize=16, labelloc=t, '
             f'label="{esc(title)}", nodesep=0.25, ranksep=0.6];',
             f'  node [shape=box, style="rounded,filled", fontname="{FONT}", fontsize=10];',
             '  edge [fontname="Helvetica", fontsize=9, color="#555555"];']
    for n, nid in ids.items():
        fam, colour = family(n, full, onto)
        used[fam] = colour
        parts = [short(n, full)]
        types = sorted(short(t, full) for t in full.objects(n, RDF.type))
        if types:
            parts.append(" / ".join(types))
        parts += [str(l) for l in sorted(full.objects(n, RDFS.label), key=str)]
        style = "rounded,filled,dashed" if n in existing else "rounded,filled"
        lines.append(f'  {nid} [label="{esc(chr(10).join(parts))}", fillcolor="{colour}", style="{style}"];')
    for k, (s, p, o) in enumerate(sorted(edges, key=lambda t: (short(t[0], full), short(t[1], full), str(t[2])))):
        label = esc(short(p, full))
        if isinstance(o, Literal):
            lines.append(f'  lit{k} [shape=note, style=filled, fillcolor="#ffffff", fontsize=9, '
                         f'label="{esc(literal_text(o, full))}"];')
            lines.append(f'  {ids[s]} -> lit{k} [label="{label}", style=dotted];')
        else:
            lines.append(f'  {ids[s]} -> {ids[o]} [label="{label}"];')
    legend = [f'<TR><TD BGCOLOR="{c}">{fam}</TD></TR>' for fam, c in used.items()]
    if existing:
        legend.append('<TR><TD>虚线框：此前已有的节点</TD></TR>')
    lines.append('  legend [shape=plaintext, fontsize=9, label=<<TABLE BORDER="0" CELLBORDER="1" '
                 f'CELLSPACING="0" CELLPADDING="4"><TR><TD><B>图例</B></TD></TR>{"".join(legend)}</TABLE>>];')
    lines.append("}")
    return "\n".join(lines), len(edges), len(nodes)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ttl", type=Path)
    ap.add_argument("--since", metavar="COMMIT")
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--comments", action="store_true")
    ap.add_argument("--vocab", action="append", default=[], metavar="VOCAB.ttl",
                    help="shared vocabulary used to look up classes and labels (repeatable)")
    args = ap.parse_args(argv)
    dot = shutil.which("dot") or "/opt/homebrew/bin/dot"
    if not Path(dot).exists():
        sys.exit("找不到 Graphviz 的 dot 命令")

    case = Graph().parse(args.ttl, format="turtle")        # what is drawn
    full = Graph()                                         # lookup: case file + vocabulary
    full += case
    for prefix, ns in case.namespaces():
        full.bind(prefix, ns, override=True)
    for v in args.vocab:
        full.parse(v, format="turtle")
    onto = Ontology()
    vocab_note = f"（类名与标签另查 {'、'.join(Path(v).name for v in args.vocab)}）" if args.vocab else ""
    if args.since:
        old = graph_at(args.ttl, args.since)
        triples = [t for t in case if t not in old]
        existing = {n for t in triples for n in (t[0], t[2])
                    if not isinstance(n, Literal) and (n, None, None) in old}
        name = f"{args.ttl.stem}_since_{args.since[:7]}"
        title = f"{args.ttl.name}：{args.since[:7]} 之后新增的 {len(triples)} 条三元组{vocab_note}"
    else:
        triples, existing = list(case), set()
        name = args.ttl.stem
        title = f"{args.ttl.name}：全部 {len(case)} 条三元组{vocab_note}"

    src, n_edges, n_nodes = to_dot(full, triples, onto, title, existing, args.comments)
    args.out.mkdir(parents=True, exist_ok=True)
    dot_path, png_path = args.out / f"{name}.dot", args.out / f"{name}.png"
    dot_path.write_text(src, encoding="utf-8")
    subprocess.run([dot, "-Tpng", "-Gdpi=130", str(dot_path), "-o", str(png_path)], check=True)
    print(f"{len(triples)} 条三元组 → {n_nodes} 个节点、{n_edges} 条边（不含 rdf:type / rdfs:label"
          f"{'' if args.comments else ' / rdfs:comment'}）\n{png_path}\n{dot_path}")


if __name__ == "__main__":
    main()
