"""
Regenerate the per-type summaries of the information-unit evaluations.

Usage (from the repo root):
    python data/evaluation/summarize.py

Reads  SL12: cbdb_vs_units.csv, event_vs_units.csv, state_vs_units.csv
       SL11: cbdb_vs_units_SL11.csv, event_vs_units_SL11.csv, state_vs_units_SL11.csv
       SL14: cbdb_vs_units_SL14.csv, event_vs_units_SL14.csv, state_vs_units_SL14.csv
Writes the *_summary.csv for each of these, plus
       three_way_summary.csv / three_way_summary_SL11.csv / three_way_summary_SL14.csv
       (CBDB / event / state side by side, plain counts, plus limit counts),
       sl11_vs_sl12_summary.csv (totals per judgement and cause, SL12 and SL11 side by side) and
       cases_summary.csv (the same totals for SL12, SL11 and SL14 side by side)

Columns: type, n, one column per judgement (x/n), then n_nonkept and one column per
cause (x/n_nonkept). "Kept" judgements (kept, kept_ext, kept_judgement) carry no cause;
non-kept rows with an empty cause (e.g. unclear) are counted under cause_blank.
cause_limit_convention counts the limit rows whose note says “约定所致（Dx）”, i.e. limits
caused by the project's own conventions rather than by CRM itself (a reporting split, not a
change of the judgement rules).
Rows "合计" and "其中 implicit=是" follow the per-type rows.
"""
import csv
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TYPE_ORDER = ["title", "event", "relation", "issuer", "title_string", "name_form",
              "date", "action", "source", "motive", "status"]
CAUSES = ["limit", "omission", "scope"]
MODEL_JUDGEMENTS = ["kept", "kept_ext", "kept_judgement", "partial", "distorted", "lost", "not_modelled"]
SPECS = {
    "cbdb_vs_units": ["kept", "notes_only", "partial", "distorted", "lost", "unclear"],
    "event_vs_units": MODEL_JUDGEMENTS,
    "state_vs_units": MODEL_JUDGEMENTS,
    # SL11: evaluation rules v1 (frozen 2026-10-28) have no "unclear"
    "cbdb_vs_units_SL11": ["kept", "notes_only", "partial", "distorted", "lost"],
    "event_vs_units_SL11": MODEL_JUDGEMENTS,
    "state_vs_units_SL11": MODEL_JUDGEMENTS,
    "cbdb_vs_units_SL14": ["kept", "notes_only", "partial", "distorted", "lost"],
    "event_vs_units_SL14": MODEL_JUDGEMENTS,
    "state_vs_units_SL14": MODEL_JUDGEMENTS,
}
CASES = {"SL12": "", "SL11": "_SL11", "SL14": "_SL14"}   # case -> file-name suffix
VERSIONS = ["cbdb", "event", "state"]
KEPT = {"kept", "kept_ext", "kept_judgement"}
CONVENTION = "约定所致（"


def is_convention(r):
    return r["cause"] == "limit" and CONVENTION in r["note"]


def line(label, rows, judgements):
    n = len(rows)
    j = Counter(r["judgement"] for r in rows)
    nonkept = [r for r in rows if r["judgement"] not in KEPT]
    c = Counter(r["cause"] or "blank" for r in nonkept)
    m = len(nonkept)
    cells = [label, str(n)] + [f"{j[x]}/{n}" for x in judgements] + [str(m)]
    conv = sum(is_convention(r) for r in nonkept)
    cells += [f"{c['limit']}/{m}", f"{conv}/{m}"] + [f"{c[x]}/{m}" for x in CAUSES[1:] + ["blank"]]
    return ",".join(cells)


def summarize(name, judgements):
    rows = list(csv.DictReader(open(HERE / f"{name}.csv", encoding="utf-8-sig")))
    bad = {r["judgement"] for r in rows} - set(judgements)
    assert not bad, f"{name}: unknown judgements {bad}"
    for r in rows:
        assert (r["cause"] == "") == (r["judgement"] in KEPT or r["judgement"] == "unclear"), r["unit_id"]
        assert r["cause"] in CAUSES + [""], r["unit_id"]
        assert CONVENTION not in r["note"] or r["cause"] == "limit", r["unit_id"]
    by = defaultdict(list)
    for r in rows:
        by[r["type"]].append(r)
    types = TYPE_ORDER + sorted(set(by) - set(TYPE_ORDER))
    out = ["type,n," + ",".join(judgements) + ",n_nonkept," +
           "cause_limit,cause_limit_convention," + ",".join(f"cause_{c}" for c in CAUSES[1:] + ["blank"])]
    out += [line(t, by[t], judgements) for t in types if t in by]
    out.append(line("合计", rows, judgements))
    out.append(line("其中 implicit=是", [r for r in rows if r["implicit"] == "是"], judgements))
    (HERE / f"{name}_summary.csv").write_text("\n".join(out) + "\n", encoding="utf-8-sig")
    return out


def three_way(suffix=""):
    """Side-by-side plain counts per type for CBDB / event / state, with each one's limit count."""
    THREE_WAY = [(k, f"{k}_vs_units{suffix}") for k in VERSIONS]
    data = {k: list(csv.DictReader(open(HERE / f"{name}.csv", encoding="utf-8-sig"))) for k, name in THREE_WAY}
    assert len({tuple(r["unit_id"] for r in rows) for rows in data.values()}) == 1, "unit lists differ"
    cols = [f"{k}_{j}" for k, name in THREE_WAY for j in SPECS[name] + ["limit", "limit_convention"]]
    def cells(rowsets):
        out = []
        for k, name in THREE_WAY:
            rows = rowsets[k]
            c = Counter(r["judgement"] for r in rows)
            out += [str(c[j]) for j in SPECS[name]] + [str(sum(r["cause"] == "limit" for r in rows)),
                                                       str(sum(is_convention(r) for r in rows))]
        return out
    types = [t for t in TYPE_ORDER if any(r["type"] == t for r in data["cbdb"])]
    lines = ["type,n," + ",".join(cols)]
    for t in types:
        sub = {k: [r for r in rows if r["type"] == t] for k, rows in data.items()}
        lines.append(",".join([t, str(len(sub["cbdb"]))] + cells(sub)))
    lines.append(",".join(["合计", str(len(data["cbdb"]))] + cells(data)))
    imp = {k: [r for r in rows if r["implicit"] == "是"] for k, rows in data.items()}
    lines.append(",".join(["其中 implicit=是", str(len(imp["cbdb"]))] + cells(imp)))
    (HERE / f"three_way_summary{suffix}.csv").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    return lines


def cases_side_by_side(cases, filename):
    """Totals per judgement and per cause, each version with the given cases next to each other."""
    judgements = []
    for js in SPECS.values():
        judgements += [j for j in js if j not in judgements]
    cols = [(v, case) for v in VERSIONS for case in cases]
    data = {(v, case): list(csv.DictReader(open(HERE / f"{v}_vs_units{CASES[case]}.csv", encoding="utf-8-sig")))
            for v, case in cols}
    lines = ["item," + ",".join(f"{v}_{case}" for v, case in cols)]
    lines.append(",".join(["n"] + [str(len(data[c])) for c in cols]))
    for j in judgements:
        lines.append(",".join([j] + [str(sum(r["judgement"] == j for r in data[c])) for c in cols]))
    for cause in CAUSES:
        lines.append(",".join([f"cause_{cause}"] + [str(sum(r["cause"] == cause for r in data[c])) for c in cols]))
        if cause == "limit":
            lines.append(",".join(["cause_limit_convention"] + [str(sum(is_convention(r) for r in data[c])) for c in cols]))
    lines.append(",".join(["implicit=是"] + [str(sum(r["implicit"] == "是" for r in data[c])) for c in cols]))
    (HERE / filename).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    return lines


if __name__ == "__main__":
    for name, judgements in SPECS.items():
        print(f"== {name}")
        print("\n".join(summarize(name, judgements)))
    for case, suffix in CASES.items():
        print(f"== three_way_summary{suffix} ({case})")
        print("\n".join(three_way(suffix)))
    print("== sl11_vs_sl12_summary")
    print("\n".join(cases_side_by_side(["SL12", "SL11"], "sl11_vs_sl12_summary.csv")))
    print("== cases_summary")
    print("\n".join(cases_side_by_side(list(CASES), "cases_summary.csv")))
