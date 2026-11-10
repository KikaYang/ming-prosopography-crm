"""
Shared machinery for the evaluation-table generators (scripts/eval/sl12.py, sl11.py, sl14.py).

A case module defines
    CASE       "SL12" / "SL11" / "SL14"
    SUFFIX     table file-name suffix ("" / "_SL11" / "_SL14")
    PREFIX     unit-id prefix(es) in data/evaluation/info_units.csv ("J118-", or a tuple for several juan)
    BASE       first-pass judgements (AI agent (Claude Code)): {version: [(unit_id, judgement, cause, evidence, implicit, note), ...]}
    OVERRIDES  later changes, applied in order: (version, unit_id, op, value, date, by, round)
               op: "judgement" / "cause" / "evidence" / "note"   replace the field
                   "note+"                                        append to the note (joined with "；")
    EVALUATED  {version: (tag, case ttl path)} for the model versions, and VOCAB_REV:
               the files as they stood when the table was (re)evaluated; evidence is checked there.
               They are read from evaluated_versions/<tag>/ (verbatim copies made for this
               snapshot); without that directory, from the git history (git show <tag>:<path>).

Tables are written as UTF-8 with BOM, CRLF line ends, csv-module quoting, which reproduces the
tables in data/evaluation/ byte for byte. Every change of a judgement goes into OVERRIDES; the
tables are not edited by hand (data/evaluation/README_en.md).
"""
import csv
import io
import os
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "data" / "evaluation"
# CBDB standalone release CBDB_20260602 (file cbdb_20260613.sqlite3); override with the CBDB_PATH environment variable
DB_PATH = Path(os.environ["CBDB_PATH"]) if os.environ.get("CBDB_PATH") else ROOT / "private" / "cbdb_20260602" / "cbdb_20260613.sqlite3"
GIT = shutil.which("git") or "/opt/homebrew/bin/git"
VERSIONS = ["cbdb", "event", "state"]
EVCOL = {"cbdb": "cbdb_evidence", "event": "ttl_evidence", "state": "ttl_evidence"}
JUDGEMENTS = {"cbdb": {"kept", "notes_only", "partial", "distorted", "lost"},
              "event": {"kept", "kept_ext", "kept_judgement", "partial", "distorted", "lost", "not_modelled"}}
JUDGEMENTS["state"] = JUDGEMENTS["event"]
KEPT = {"kept", "kept_ext", "kept_judgement"}
OPS = {"judgement", "cause", "evidence", "note", "note+"}


# ---------------------------------------------------------------- building the tables
def units(prefix):
    rows = [r for r in csv.DictReader(open(EVAL / "info_units.csv", encoding="utf-8"))
            if r["unit_id"].startswith(prefix) and r["in_scope"] == "是"]
    return {r["unit_id"]: r for r in rows}


def build(case):
    """{version: [row dict in table column order]} after applying the overrides."""
    us = units(case.PREFIX)
    tables = {}
    for v in VERSIONS:
        base = case.BASE[v]
        assert [b[0] for b in base] == list(us), f"{v}: base rows differ from info_units.csv"
        tables[v] = {b[0]: {"judgement": b[1], "cause": b[2], "evidence": b[3], "implicit": b[4], "note": b[5]}
                     for b in base}
    for v, uid, op, value, date, by, rnd in case.OVERRIDES:
        assert op in OPS and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) and by and rnd, (v, uid, op)
        row = tables[v][uid]
        if op == "note+":
            row["note"] = f"{row['note']}；{value}" if row["note"] else value
        else:
            row[op] = value
    out = {}
    for v in VERSIONS:
        rows = []
        for uid, u in us.items():
            r = tables[v][uid]
            assert r["judgement"] in JUDGEMENTS[v], (v, uid, r["judgement"])
            assert (r["cause"] == "") == (r["judgement"] in KEPT), (v, uid)
            assert r["judgement"] not in KEPT or r["evidence"], (v, uid, "kept without evidence")
            rows.append({"unit_id": uid, "type": u["type"], "text": u["text"], "judgement": r["judgement"],
                         "cause": r["cause"], EVCOL[v]: r["evidence"], "implicit": r["implicit"], "note": r["note"]})
        out[v] = rows
    return out


def render(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)
    return ("﻿" + buf.getvalue()).encode("utf-8")


def write(case, out_dir=EVAL, verify=True):
    tables = build(case)
    if verify:
        verify_models(case, tables)
        if DB_PATH.exists():
            getattr(case, "CBDB_VERIFIER", verify_cbdb)(tables["cbdb"])
    paths = []
    for v, rows in tables.items():
        p = Path(out_dir) / f"{v}_vs_units{case.SUFFIX}.csv"
        p.write_bytes(render(rows))
        paths.append(p)
    return paths


# ---------------------------------------------------------------- model evidence
EVALUATED_VERSIONS = ROOT / "evaluated_versions"


def git_show(rev, path):
    """The file at <path> as it stood at tag <rev>: from evaluated_versions/<rev>/<path> if present,
    otherwise from the git history."""
    local = EVALUATED_VERSIONS / rev / path
    if local.exists():
        return local.read_bytes().decode("utf-8")
    r = subprocess.run([GIT, "show", f"{rev}:{path}"], cwd=ROOT, capture_output=True)
    if r.returncode != 0:
        raise FileNotFoundError(f"{path} at {rev}: not in {local.relative_to(ROOT)} and not in the git history")
    return r.stdout.decode("utf-8")


def verify_models(case, tables):
    prefixes = git_show(case.VOCAB_REV, "docs/modelling/prefixes.ttl")
    for v in ("event", "state"):
        rev, path = case.EVALUATED[v]
        g = Graph()
        g.parse(data=git_show(rev, path), format="turtle")
        g.parse(data=git_show(case.VOCAB_REV, "docs/modelling/vocab.ttl"), format="turtle")
        for r in tables[v]:
            for t in [x.strip() for x in r["ttl_evidence"].split(" ; ") if x.strip()]:
                tg = Graph()
                tg.parse(data=prefixes + "\n" + t + " .", format="turtle")
                for tr in tg:
                    assert tr in g, f"{case.CASE} {v} {r['unit_id']}: not in {path}@{rev}: {t}"


# ---------------------------------------------------------------- CBDB evidence
YEARS = re.compile(r"(\d{4})–(\d{4})")
FIELD = re.compile(r"(c_[a-z_]+)=([^ （(;]+(?:\([^)]*\))*[^ （;]*)")


def verify_cbdb(rows):
    db = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    q = lambda sql, *a: db.execute(sql, a).fetchall()
    for r in rows:
        table, posting = None, None
        for seg in [s.strip() for s in r["cbdb_evidence"].split(" ; ") if s.strip()]:
            where = f"{r['unit_id']}: {seg}"
            m = re.match(r"(POSTED_TO_OFFICE_DATA|POSTED_TO_ADDR_DATA|BIOG_MAIN|BIOG_TEXT_DATA|TEXT_CODES) ?", seg)
            if m:
                table, seg = m.group(1), seg[m.end():]
            m = re.match(r"posting_id (\d+)|(\d{5,})(?= |$)", seg)
            if m:
                posting = int(m.group(1) or m.group(2))
                seg = seg[m.end():]
            if table == "POSTED_TO_OFFICE_DATA":
                cols = [c[1] for c in q("PRAGMA table_info(POSTED_TO_OFFICE_DATA)")]
                row = q("SELECT * FROM POSTED_TO_OFFICE_DATA WHERE c_posting_id=?", posting)
                assert row, where
                rec = dict(zip(cols, row[0]))
                m = re.match(r"（CBDB_line_ID (\d+)）", seg)
                if m:
                    assert f"CBDB_line_ID={m.group(1)}" in (rec["c_notes"] or ""), where
                    seg = seg[m.end():]
                _fields(rec, seg, where)
                y = YEARS.search(seg)
                if y:
                    assert (rec["c_firstyear"], rec["c_lastyear"]) == (int(y.group(1)), int(y.group(2))), where
                names = re.findall(r"[一-鿿]+", FIELD.sub("", seg))
                if names:
                    office = q("SELECT c_office_chn FROM OFFICE_CODES WHERE c_office_id=?", rec["c_office_id"])[0][0]
                    assert names[0] == office, f"{where}: office is {office}"
            elif table == "POSTED_TO_ADDR_DATA":
                m = re.match(r" ?c_addr_id=(\d+) (\S+?)(（ADDR_BELONGS_DATA 属 (\d+) (\S+?)）)?$", seg)
                assert m, where
                assert q("SELECT 1 FROM POSTED_TO_ADDR_DATA WHERE c_posting_id=? AND c_addr_id=?", posting, int(m.group(1))), where
                assert q("SELECT c_name_chn FROM ADDR_CODES WHERE c_addr_id=?", int(m.group(1))) == [(m.group(2),)], where
                if m.group(3):
                    assert q("SELECT 1 FROM ADDR_BELONGS_DATA WHERE c_addr_id=? AND c_belongs_to=?", int(m.group(1)), int(m.group(4))), where
                    assert q("SELECT c_name_chn FROM ADDR_CODES WHERE c_addr_id=?", int(m.group(4))) == [(m.group(5),)], where
            elif table == "BIOG_MAIN":
                m = re.fullmatch(r"c_personid (\d+) c_name_chn=(\S+)", seg)
                assert m and q("SELECT c_name_chn FROM BIOG_MAIN WHERE c_personid=?", int(m.group(1))) == [(m.group(2),)], where
            elif table == "BIOG_TEXT_DATA":
                m = re.fullmatch(r"c_personid (\d+) c_textid (\d+) c_role_id=(\d+)", seg)
                assert m and q("SELECT 1 FROM BIOG_TEXT_DATA WHERE c_personid=? AND c_textid=? AND c_role_id=?",
                               *map(int, m.groups())), where
            elif table == "TEXT_CODES":
                m = re.fullmatch(r"c_textid (\d+) c_title_chn=(\S+)", seg)
                assert m and q("SELECT c_title_chn FROM TEXT_CODES WHERE c_textid=?", int(m.group(1))) == [(m.group(2),)], where
            else:
                raise AssertionError(f"unparsed evidence: {where}")


def _fields(rec, seg, where):
    for col, val in FIELD.findall(seg):
        actual = rec[col]
        if col == "c_notes":
            frag = val.lstrip("…")
            assert frag in (actual or ""), f"{where}: c_notes={actual}"
        else:
            assert str(actual) == val, f"{where}: {col}={actual}"


# ---------------------------------------------------------------- CBDB evidence, SL12 wording
# SL12 tables predate the "c_field=value ; ..." format and word evidence as prose; every shape
# found there is listed below and anything else fails. Evidence is about 張璁 unless it names 杨一清.
ZHANG_CONG, YANG_YIQING = 68266, 68260
IDS = r"(\d+(?:/\d+)*)"


def verify_cbdb_sl12(rows):
    db = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    q = lambda sql, *a: db.execute(sql, a).fetchall()
    cols = [c[1] for c in q("PRAGMA table_info(POSTED_TO_OFFICE_DATA)")]

    def post(pid, person, where):
        row = q("SELECT * FROM POSTED_TO_OFFICE_DATA WHERE c_posting_id=?", int(pid))
        assert row, f"{where}: no posting {pid}"
        rec = dict(zip(cols, row[0]))
        assert rec["c_personid"] == person, f"{where}: {pid} belongs to {rec['c_personid']}"
        return rec

    def office(rec, name, first, last, where):
        actual = q("SELECT c_office_chn FROM OFFICE_CODES WHERE c_office_id=?", rec["c_office_id"])[0][0]
        assert actual == name, f"{where}: office is {actual}"
        assert str(rec["c_firstyear"]) == first, f"{where}: c_firstyear={rec['c_firstyear']}"
        if last is not None:   # "" = 无止年
            assert (rec["c_lastyear"] or "") == (int(last) if last else ""), f"{where}: c_lastyear={rec['c_lastyear']}"

    for r in rows:
        ev, where = r["cbdb_evidence"], f"{r['unit_id']}: {r['cbdb_evidence']}"
        if not ev:
            continue
        m = re.fullmatch(r"BIOG_MAIN\.c_name_chn = (\S+)", ev)
        if m:
            assert q("SELECT c_name_chn FROM BIOG_MAIN WHERE c_personid=?", ZHANG_CONG) == [(m.group(1),)], where
            continue
        m = re.fullmatch(r"ALTNAME_DATA c_alt_name_chn = (\S+?)（别名、曾用名）", ev)
        if m:
            assert q("SELECT 1 FROM ALTNAME_DATA WHERE c_personid=? AND c_alt_name_chn=? AND c_alt_name_type_code=3",
                     ZHANG_CONG, m.group(1)), where
            continue
        m = re.fullmatch(r"(杨一清 )?POSTED_TO_OFFICE_DATA posting_id (.+)", ev)
        assert m, f"unparsed evidence: {where}"
        person, body = (YANG_YIQING if m.group(1) else ZHANG_CONG), m.group(2)
        if f := re.fullmatch(IDS + r" c_firstyear=(\d{4}), c_fy_nh_year=嘉靖(\d+)", body):
            for pid in f.group(1).split("/"):
                rec = post(pid, person, where)
                assert str(rec["c_firstyear"]) == f.group(2) and str(rec["c_fy_nh_year"]) == f.group(3), f"{where}: {pid} {rec['c_firstyear']} {rec['c_fy_nh_year']}"
                assert q("SELECT c_nianhao_chn FROM NIAN_HAO WHERE c_nianhao_id=?", rec["c_fy_nh_code"]) == [("嘉靖",)], where
        elif f := re.fullmatch(IDS + r" c_notes = “(.+)”", body):
            for pid in f.group(1).split("/"):
                assert f.group(2) in (post(pid, person, where)["c_notes"] or ""), f"{where}: {pid}"
        elif f := re.fullmatch(IDS + r"(?: 与 (\d+))? 的(?:年份区间| c_lastyear)", body):
            for pid in f.group(1).split("/") + ([f.group(2)] if f.group(2) else []):
                post(pid, person, where)
        elif f := re.fullmatch(r"(\d+)（(\S+?)，(?:(\d{4})–(\d{4})?|c_firstyear (\d{4})(，无止年)?)）", body):
            first, last = f.group(3) or f.group(5), f.group(4) or ""
            if f.group(5) and not f.group(6):   # 只写起始年，止年不论
                last = None
            office(post(f.group(1), person, where), f.group(2), first, last, where)
        else:
            items = body.split("、")
            for item in items:
                f = re.fullmatch(r"(\d+) (\S+?)\((\d{4})–(\d{4})?\)", item)
                assert f, f"unparsed evidence: {where}"
                office(post(f.group(1), person, where), f.group(2), f.group(3), f.group(4) or "", where)
