"""
Check a Turtle file against CIDOC-CRM 7.1.3 (core RDFS + PC extension). Read only.

Usage (from the repo root):
    python3 scripts/check_crm.py FILE.ttl [--vocab VOCAB.ttl ...] [--ext-ns IRI] [--ontology-dir DIR]

    --vocab   load shared vocabulary (e.g. docs/modelling/vocab.ttl) together with FILE;
              may be given more than once. The checks run on the merged graph.

Checks
    (a) every crm: IRI used exists in CRM 7.1.3; predicates must be properties,
        rdf:type objects must be classes
    (b) subjects / objects of crm: properties match rdfs:domain / rdfs:range,
        following rdfs:subClassOf (CRM's and any declared in the file)
    (c) every extension property (mpv:, see docs/modelling/prefixes.ttl) used as a predicate
        declares rdfs:domain and rdfs:range in the loaded files (FILE plus any --vocab)
    (d) crm:P4_has_time-span only on (subclasses of) E2 Temporal Entity
        (and crm:P4i_is_time-span_of only pointing at one)

Types are taken only from explicit rdf:type statements in the loaded files (plus their
superclasses); nothing is inferred from domains/ranges. A node with no rdf:type, or
with types outside the CRM hierarchy, cannot be checked and gives a warning.

Exit code: 1 if there are errors, 0 otherwise (warnings alone do not fail).
"""
import argparse
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
MPV = "https://kikayang.github.io/ming-prosopography-crm/vocab/"   # project extension namespace (D8)
ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_FILES = ["CIDOC_CRM_v7.1.3.rdf", "CIDOC_CRM_v7.1.3_PC.rdf"]
P4, P4I, E2 = CRM["P4_has_time-span"], CRM["P4i_is_time-span_of"], CRM["E2_Temporal_Entity"]

ERROR, WARNING = "错误", "警告"


@dataclass
class Issue:
    level: str   # ERROR / WARNING
    check: str   # a / b / c / d
    message: str


class Ontology:
    def __init__(self, ontology_dir=ROOT / "ontologies"):
        self.g = Graph()
        for f in ONTOLOGY_FILES:
            self.g.parse(Path(ontology_dir) / f)
        self.classes = set(self.g.subjects(RDF.type, RDFS.Class))
        self.properties = set(self.g.subjects(RDF.type, RDF.Property))
        self.names = {str(x)[len(str(CRM)):]: x for x in self.classes | self.properties}

    def suggest(self, iri):
        local = str(iri)[len(str(CRM)):]
        close = difflib.get_close_matches(local, self.names, n=2, cutoff=0.75)
        return f"（是否应为 {' / '.join('crm:' + c for c in close)}？）" if close else ""

    def domains(self, prop):
        return self._inherited(prop, RDFS.domain)

    def ranges(self, prop):
        return self._inherited(prop, RDFS.range)

    def _inherited(self, prop, pred):
        """Declared domain/range, else the nearest super-property's (none occur in 7.1.3)."""
        seen, todo = set(), [prop]
        while todo:
            p = todo.pop()
            vals = set(self.g.objects(p, pred))
            if vals:
                return vals
            seen.add(p)
            todo += [s for s in self.g.objects(p, RDFS.subPropertyOf) if s not in seen]
        return set()


def superclasses(cls, graphs):
    """cls and all its superclasses over rdfs:subClassOf in the given graphs."""
    out, todo = set(), [cls]
    while todo:
        c = todo.pop()
        if c in out:
            continue
        out.add(c)
        for g in graphs:
            todo += list(g.objects(c, RDFS.subClassOf))
    return out


def in_crm(term):
    return isinstance(term, URIRef) and str(term).startswith(str(CRM))


def check(data: Graph, onto: Ontology, ext_ns=MPV):
    issues = []
    n = data.namespace_manager
    fmt = lambda t: t.n3(n) if not isinstance(t, BNode) else f"_:{t}"
    graphs = (onto.g, data)

    def type_closure(node):
        types = set(data.objects(node, RDF.type))
        return types, set().union(*(superclasses(t, graphs) for t in types)) if types else set()

    # (a) crm: IRIs exist; right kind in predicate / rdf:type position --------------------
    reported = set()
    for s, p, o in data:
        for pos, term in (("主语", s), ("谓语", p), ("宾语", o)):
            if not in_crm(term) or term in reported:
                continue
            if term not in onto.classes and term not in onto.properties:
                reported.add(term)
                issues.append(Issue(ERROR, "a", f"{fmt(term)} 不在 CIDOC-CRM 7.1.3 中"
                                                f"{onto.suggest(term)}"))
        if in_crm(p) and p in onto.classes:
            issues.append(Issue(ERROR, "a", f"{fmt(p)} 是类，却用作谓语：{fmt(s)} {fmt(p)} {fmt(o)}"))
        if p == RDF.type and in_crm(o) and o in onto.properties:
            issues.append(Issue(ERROR, "a", f"{fmt(o)} 是属性，却用作 rdf:type 的对象：{fmt(s)}"))

    # (b) domain / range, (d) P4 ------------------------------------------------------
    for s, p, o in data:
        if not in_crm(p) or p not in onto.properties:
            continue
        triple = f"{fmt(s)} {fmt(p)} {fmt(o)}"
        if p in (P4, P4I):
            node = s if p == P4 else o
            types, closure = type_closure(node)
            if not types:
                issues.append(Issue(WARNING, "d", f"{fmt(node)} 没有 rdf:type，无法确认它是 E2 的子类：{triple}"))
            elif E2 not in closure:
                issues.append(Issue(ERROR, "d", f"P4 只能用于 E2 Temporal Entity 的子类，"
                                                f"而 {fmt(node)} 的类型是 "
                                                f"{', '.join(sorted(fmt(t) for t in types))}：{triple}"))
            other, expected = (o, onto.ranges(p)) if p == P4 else (s, onto.domains(p))
            issues += _check_node(other, expected, "宾语" if p == P4 else "主语", triple,
                                  type_closure, fmt, onto)
            continue
        issues += _check_node(s, onto.domains(p), "主语", triple, type_closure, fmt, onto)
        issues += _check_node(o, onto.ranges(p), "宾语", triple, type_closure, fmt, onto)

    # (c) extension properties declare domain and range in the file ----------------------
    for p in sorted({p for p in data.predicates() if str(p).startswith(ext_ns)}):
        missing = [name for name, pred in (("rdfs:domain", RDFS.domain), ("rdfs:range", RDFS.range))
                   if (p, pred, None) not in data]
        if missing:
            issues.append(Issue(ERROR, "c", f"扩展属性 {fmt(p)} 在文件中没有声明 "
                                            f"{' 和 '.join(missing)}"))
    return issues


def _check_node(node, expected, role, triple, type_closure, fmt, onto):
    """Check one end of a crm: triple against the property's domain or range."""
    if not expected:
        return []
    exp_crm = {e for e in expected if in_crm(e)}
    if RDFS.Literal in expected:
        if not isinstance(node, Literal):
            return [Issue(ERROR, "b", f"{role}应为字面量（rdfs:Literal），实际是 {fmt(node)}：{triple}")]
        return []
    if not exp_crm:          # e.g. range rdf:Property / domain rdfs:Class: not checked
        return []
    if isinstance(node, Literal):
        return [Issue(ERROR, "b", f"{role}应为 {', '.join(sorted(fmt(e) for e in exp_crm))} 的实例，"
                                  f"实际是字面量 {fmt(node)}：{triple}")]
    types, closure = type_closure(node)
    if not types:
        return [Issue(WARNING, "b", f"{role} {fmt(node)} 没有 rdf:type，无法检查是否符合 "
                                    f"{', '.join(sorted(fmt(e) for e in exp_crm))}：{triple}")]
    if exp_crm & closure:
        return []
    if not any(in_crm(c) for c in closure):
        return [Issue(WARNING, "b", f"{role} {fmt(node)} 的类型 "
                                    f"{', '.join(sorted(fmt(t) for t in types))} 不在 CRM 类层级中"
                                    f"（没有 rdfs:subClassOf 到 crm: 类），无法检查：{triple}")]
    return [Issue(ERROR, "b", f"{role} {fmt(node)} 的类型 {', '.join(sorted(fmt(t) for t in types))} "
                              f"不是 {', '.join(sorted(fmt(e) for e in exp_crm))} 或其子类：{triple}")]


def report(issues, out=None):
    out = out or sys.stdout
    for level in (ERROR, WARNING):
        items = [i for i in issues if i.level == level]
        print(f"== {level}：{len(items)}", file=out)
        for i in sorted(items, key=lambda i: (i.check, i.message)):
            print(f"  ({i.check}) {i.message}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ttl")
    ap.add_argument("--vocab", action="append", default=[], metavar="VOCAB.ttl",
                    help="shared vocabulary loaded together with the case file (repeatable)")
    ap.add_argument("--ext-ns", default=MPV, help=f"extension namespace IRI (default: mpv: {MPV})")
    ap.add_argument("--ontology-dir", default=ROOT / "ontologies")
    args = ap.parse_args(argv)
    data = Graph()
    data.parse(args.ttl, format="turtle")
    n_case = len(data)
    for v in args.vocab:
        data.parse(v, format="turtle")
    issues = check(data, Ontology(args.ontology_dir), args.ext_ns)
    loaded = "".join(f" + {v}" for v in args.vocab)
    print(f"{args.ttl}{loaded}: {len(data)} 条三元组" + (f"（案例文件 {n_case} 条）" if args.vocab else ""))
    report(issues)
    return 1 if any(i.level == ERROR for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
