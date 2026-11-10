"""
Match the 163 grand secretaries parsed from 《明史·宰辅年表》 to CBDB person IDs.

Usage:
    python3 scripts/match_mingshi_cbdb.py cbdb_20261003/cbdb_20261003.sqlite3

Input : data/mingshi_zaifu/mingshi_zaifu_persons.csv
Output: data/mingshi_zaifu/mingshi_cbdb_match.csv  (one row per 明史 person)
        data/mingshi_zaifu/mingshi_cbdb_candidates.csv (all candidates with scores)

Matching = name (BIOG_MAIN.c_name_chn or ALTNAME_DATA) + plausibility:
  +5  a CBDB posting whose office name contains 大學士 overlapping the 明史 tenure
  +2  death year >= last tenure year (or unknown)
  +2  birth year <= first tenure year - 15 (or unknown)
  +1  index year within [first-60, last+10]
  -10 lifetime clearly incompatible with the tenure
Status: unique / resolved (one clear best) / ambiguous / none / override
Person identification remains a human decision: review 'ambiguous' and 'none'.
"""
import csv, sqlite3, sys

PERSONS = "data/mingshi_zaifu/mingshi_zaifu_persons.csv"
OUT = "data/mingshi_zaifu/mingshi_cbdb_match.csv"
OUT_C = "data/mingshi_zaifu/mingshi_cbdb_candidates.csv"

# name forms differing between 明史 (Wikisource) and CBDB, plus known disambiguations
ALIASES = {"張璁": ["張孚敬"], "郭朴": ["郭樸"], "沈□": ["沈㴶", "沈潅"], "李國□": ["李國𣚴", "李國普"],
           "袁宗皐": ["袁宗皋"], "趙志皐": ["趙志皋"], "徐光啟": ["徐光啓"], "賀逢聖": ["賀逢聖"], "金幼孜": ["金善"], "魏炤乘": ["魏照乘"]}
PID_OVERRIDE = {"張璧": 130683}


def main(db):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    persons = list(csv.DictReader(open(PERSONS, encoding="utf-8-sig")))
    out, allc = [], []
    for p in persons:
        name = p["name_trad"]; fy = int(p["first_year_ce"]); ly = int(p["last_year_ce"])
        names = [name] + ALIASES.get(name, [])
        q = ",".join("?" * len(names))
        pids = {r[0] for r in con.execute(f"SELECT c_personid FROM BIOG_MAIN WHERE c_name_chn IN ({q})", names)}
        pids |= {r[0] for r in con.execute(f"SELECT c_personid FROM ALTNAME_DATA WHERE c_alt_name_chn IN ({q})", names)}
        cands = []
        for pid in pids:
            b = con.execute("SELECT c_personid,c_name_chn,c_index_year,c_birthyear,c_deathyear FROM BIOG_MAIN WHERE c_personid=?", (pid,)).fetchone()
            if b is None: continue
            by = b["c_birthyear"] or 0; dy = b["c_deathyear"] or 0; iy = b["c_index_year"] or 0
            daxue = con.execute("""SELECT COUNT(*) FROM POSTED_TO_OFFICE_DATA p JOIN OFFICE_CODES o ON p.c_office_id=o.c_office_id
                                   WHERE p.c_personid=? AND o.c_office_chn LIKE '%大學士%'
                                   AND (p.c_firstyear IS NULL OR p.c_firstyear=0 OR p.c_firstyear BETWEEN ? AND ?)""",
                                (pid, fy - 3, ly + 3)).fetchone()[0]
            npost = con.execute("SELECT COUNT(*) FROM POSTED_TO_OFFICE_DATA WHERE c_personid=?", (pid,)).fetchone()[0]
            s = 0
            if daxue: s += 5
            if dy == 0 or dy >= ly - 1: s += 2
            if by == 0 or by <= fy - 15: s += 2
            if iy and fy - 60 <= iy <= ly + 10: s += 1
            if (dy and dy < fy) or (by and by > fy - 10): s -= 10
            c = dict(name=name, personid=pid, cbdb_name=b["c_name_chn"], index_year=iy, birth=by, death=dy,
                     daxueshi_postings=daxue, postings=npost, score=s)
            cands.append(c); allc.append(c)
        cands.sort(key=lambda c: (-c["score"], -c["postings"]))
        if name in PID_OVERRIDE:
            best = next((c for c in cands if c["personid"] == PID_OVERRIDE[name]), None); status = "override"
        elif not cands or cands[0]["score"] < 0:
            best = None; status = "none"
        elif len(cands) == 1:
            best = cands[0]; status = "unique"
        elif cands[0]["score"] > cands[1]["score"]:
            best = cands[0]; status = "resolved"
        else:
            best = cands[0]; status = "ambiguous"
        out.append(dict(seq=p["seq"], name_trad=name, name_simp=p["name_simp"], mingshi_first=fy, mingshi_last=ly,
                        status=status, n_candidates=len(cands),
                        cbdb_personid=best["personid"] if best else "", cbdb_name=best["cbdb_name"] if best else "",
                        cbdb_birth=best["birth"] if best else "", cbdb_death=best["death"] if best else "",
                        cbdb_daxueshi_postings=best["daxueshi_postings"] if best else "",
                        cbdb_postings=best["postings"] if best else "", score=best["score"] if best else ""))
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    with open(OUT_C, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(allc[0])); w.writeheader(); w.writerows(allc)
    from collections import Counter
    print(Counter(r["status"] for r in out))
    for r in out:
        if r["status"] in ("none", "ambiguous") or (r["status"] != "none" and r["cbdb_daxueshi_postings"] == 0):
            print(r["status"], r["name_trad"], r["mingshi_first"], r["mingshi_last"], r["cbdb_personid"], r["cbdb_birth"], r["cbdb_death"], "大學士任官:", r["cbdb_daxueshi_postings"], "候选:", r["n_candidates"])


if __name__ == "__main__":
    main(sys.argv[1])
