"""
CBDB coverage check for Ming grand secretaries (嘉靖–萬曆, 1522–1620).

Usage:
    python3 coverage_check.py cbdb_XXXXXXXX.sqlite3

Outputs:
    coverage_ming_grand_secretaries.csv   one row per candidate
    (summary printed to stdout)
"""
import csv
import sqlite3
import sys

# 嘉靖—萬曆年間入閣者（繁體，與CBDB一致）。張璁 CBDB 可能以「張孚敬」收錄，兩者都查。
CANDIDATES = [
    # 嘉靖
    "楊廷和", "蔣冕", "毛紀", "費宏", "石珤", "賈詠", "楊一清", "謝遷",
    "張璁", "翟鑾", "桂萼", "方獻夫", "李時", "夏言", "顧鼎臣", "嚴嵩",
    "許讚", "張璧", "徐階", "呂本", "袁煒", "嚴訥", "李春芳", "郭朴", "高拱",
    # 隆慶
    "陳以勤", "張居正", "趙貞吉", "殷士儋", "高儀",
    # 萬曆
    "呂調陽", "張四維", "馬自強", "申時行", "余有丁", "許國", "王錫爵",
    "王家屏", "趙志皋", "張位", "陳于陛", "沈一貫", "沈鯉", "朱賡",
    "于慎行", "李廷機", "葉向高", "方從哲", "吳道南",
]
ALIASES = {"張璁": ["張孚敬"], "郭朴": ["郭樸"]}
# manual disambiguation where the "most postings" rule picks a homonym
PID_OVERRIDE = {"張璧": 130683}

# Ming grand secretaries of this period: index year roughly 1490–1620
YEAR_MIN, YEAR_MAX = 1480, 1630


def table_cols(con, table):
    return {r[1] for r in con.execute(f"PRAGMA table_info({table})")}


def count(con, table, pid, where=""):
    sql = f"SELECT COUNT(*) FROM {table} WHERE c_personid=? {where}"
    return con.execute(sql, (pid,)).fetchone()[0]


def main(db):
    con = sqlite3.connect(db)

    # find the dynasty code for 明
    ming = con.execute(
        "SELECT c_dy FROM DYNASTIES WHERE c_dynasty_chn='明'"
    ).fetchone()
    ming_dy = ming[0] if ming else None

    # text id(s) for 明史, to see how much of each record comes from it
    mingshi_ids = [r[0] for r in con.execute(
        "SELECT c_textid FROM TEXT_CODES WHERE c_title_chn='明史' OR c_title_chn LIKE '明史稿%'"
    )]

    has_src = "BIOG_SOURCE_DATA" in {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}

    rows = []
    for name in CANDIDATES:
        names = [name] + ALIASES.get(name, [])
        q = ",".join("?" * len(names))
        hits = con.execute(
            f"""SELECT c_personid, c_name_chn, c_index_year, c_birthyear,
                       c_deathyear, c_dy
                FROM BIOG_MAIN WHERE c_name_chn IN ({q})""",
            names,
        ).fetchall()

        # keep Ming-era matches
        def is_ming(h):
            _, _, iy, by, dy_, dyn = h
            yrs = [y for y in (iy, by, dy_) if y and y > 0]
            if yrs and any(YEAR_MIN <= y <= YEAR_MAX for y in yrs):
                return True
            return ming_dy is not None and dyn == ming_dy and not yrs

        cands = [h for h in hits if is_ming(h)]
        if name in PID_OVERRIDE:
            cands = [h for h in hits if h[0] == PID_OVERRIDE[name]]
        # prefer records that have any dates at all
        dated = [h for h in cands if h[2]]
        cands = dated or cands
        if not cands:
            rows.append({"name": name, "status": "NOT FOUND",
                         "n_homonyms": len(hits)})
            continue

        # if several, pick the one with most postings
        best, best_n = None, -1
        for h in cands:
            n = count(con, "POSTED_TO_OFFICE_DATA", h[0])
            if n > best_n:
                best, best_n = h, n
        pid = best[0]

        postings = best_n
        postings_dated = count(con, "POSTED_TO_OFFICE_DATA", pid,
                               "AND c_firstyear IS NOT NULL AND c_firstyear>0")
        distinct_offices = con.execute(
            "SELECT COUNT(DISTINCT c_office_id) FROM POSTED_TO_OFFICE_DATA "
            "WHERE c_personid=?", (pid,)).fetchone()[0]
        altnames = count(con, "ALTNAME_DATA", pid)
        addrs = count(con, "BIOG_ADDR_DATA", pid)
        kin = count(con, "KIN_DATA", pid)
        assoc = count(con, "ASSOC_DATA", pid)
        entry = count(con, "ENTRY_DATA", pid)

        from_mingshi = ""
        if has_src and mingshi_ids:
            qm = ",".join("?" * len(mingshi_ids))
            from_mingshi = con.execute(
                f"SELECT COUNT(*) FROM BIOG_SOURCE_DATA WHERE c_personid=? "
                f"AND c_textid IN ({qm})", [pid] + mingshi_ids).fetchone()[0]

        rows.append({
            "name": name, "status": "OK", "personid": pid,
            "cbdb_name": best[1], "index_year": best[2],
            "birth": best[3], "death": best[4],
            "n_homonyms": len(hits),
            "postings": postings, "postings_dated": postings_dated,
            "distinct_offices": distinct_offices,
            "altnames": altnames, "addresses": addrs,
            "kin": kin, "assoc": assoc, "entry": entry,
            "mingshi_as_source": from_mingshi,
        })

    fields = ["name", "status", "personid", "cbdb_name", "index_year",
              "birth", "death", "n_homonyms", "postings", "postings_dated",
              "distinct_offices", "altnames", "addresses", "kin", "assoc",
              "entry", "mingshi_as_source"]
    with open("coverage_ming_grand_secretaries.csv", "w",
              newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    ok = [r for r in rows if r["status"] == "OK"]
    print(f"Ming dynasty code: {ming_dy}; 明史 text ids: {mingshi_ids}")
    print(f"Found {len(ok)}/{len(rows)} candidates")
    for r in rows:
        if r["status"] != "OK":
            print(f"  NOT FOUND: {r['name']} (homonyms: {r['n_homonyms']})")
    if ok:
        def dist(key):
            v = sorted(int(r[key]) for r in ok)
            return f"min {v[0]}, median {v[len(v)//2]}, max {v[-1]}"
        for k in ["postings", "postings_dated", "distinct_offices",
                  "altnames", "addresses", "kin", "assoc"]:
            print(f"  {k:17s} {dist(k)}")
        rich = [r for r in ok if r["postings"] >= 5]
        print(f"  >=5 postings: {len(rich)}/{len(ok)}")
        if mingshi_ids and has_src:
            n_ms = sum(1 for r in ok if r["mingshi_as_source"])
            print(f"  cites 明史 as source: {n_ms}/{len(ok)}")


if __name__ == "__main__":
    main(sys.argv[1])
