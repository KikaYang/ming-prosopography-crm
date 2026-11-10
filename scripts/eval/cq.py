"""
Competency questions: run all queries in data/evaluation/cq_queries/, write the raw results to cq_raw/,
and generate cq_results.csv from VERDICTS + OVERRIDES.
Run from the repository root:
    python scripts/eval/cq.py              # rewrite cq_raw/ and cq_results.csv
    python scripts/eval/cq.py --out DIR    # write elsewhere (used by the tests)
SPARQL runs on the ttl files at MODEL_REV (evaluated_versions/cq-v1/; the event and state versions each
merge SL12, SL11, SL14 and vocab.ttl); SQL runs read-only on a local CBDB.
Every change of judgement goes into OVERRIDES (with date, author and round); the table is not edited directly.
"""
import argparse
import csv
import io
import sqlite3
import sys
from pathlib import Path

from rdflib import BNode, Graph, Literal, URIRef

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DB_PATH, EVAL, git_show  # noqa: E402

MODEL_REV = "cq-v1"
CASES = ("SL12", "SL11", "SL14")
QUERIES = EVAL / "cq_queries"
VERSIONS = ("cbdb", "event", "state")


def graph(version):
    g = Graph()
    for case in CASES:
        g.parse(data=git_show(MODEL_REV, f"docs/modelling/{case}_{version}.ttl"), format="turtle")
    g.parse(data=git_show(MODEL_REV, "docs/modelling/vocab.ttl"), format="turtle")
    return g


def cell(v, g):
    if v is None:
        return ""
    if isinstance(v, URIRef):
        return v.n3(g.namespace_manager)
    assert not isinstance(v, BNode), "blank node in result"
    return str(v)


def render(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    w.writerows(rows)
    return ("﻿" + buf.getvalue()).encode("utf-8")


def run_all(out_dir):
    raw = Path(out_dir) / "cq_raw"
    raw.mkdir(parents=True, exist_ok=True)
    graphs = {v: graph(v) for v in ("event", "state")}
    ns = {p: n for p, n in graphs["event"].namespaces()}
    db = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) if DB_PATH.exists() else None
    for q in sorted(QUERIES.iterdir()):
        text = q.read_text(encoding="utf-8")
        if q.suffix == ".sql":
            if db is None:
                continue
            cur = db.execute(text)
            header = [d[0] for d in cur.description]
            rows = [["" if c is None else c for c in r] for r in cur.fetchall()]
        else:
            g = graphs[q.name.split(".")[1]]
            res = g.query(text, initNs=ns)
            header = [str(v) for v in res.vars]
            rows = [[cell(v, g) for v in r] for r in res]
        (raw / f"{q.name}.csv").write_bytes(render(header, rows))


# first-pass judgements (AI agent (Claude Code), tag eval-cq-v1): (cq_id, version) -> (verdict, result summary, note)
# verdicts: 答对 correct / 部分答对 partially correct / 答不了 cannot answer / 答错 wrong (rules in data/evaluation/README_en.md, "Competency questions")
VERDICTS = {
    ("CQ1", "cbdb"): ("部分答对", "带衔：列出杨一清、张璁等 8 人（含桂萼、吴一鹏、李承勋等本案史料未及者），都只是“吏部尚書”一条任官，任命方式未詳。掌部事：无结果。",
                      "两人都在，时段重叠，可读出同时带衔；但衔与职不分，也不写同掌。掌部事查不到，是没有记录，不等于表达了“未知”。其余 6 人不在本案史料内，无从判其对错"),
    ("CQ1", "event"): ("答错", "带衔：张璁（1528-06-27）。掌部事：掌事节点只有夏言掌吏科，无吏部。类型定义写“阁臣兼衔，非掌部事”。",
                       "张璁一半答对，杨一清未建模（scope）。答错在掌部事：类型 type:shangshu-personnel-xian 的 comment 和英文 label 把张璁的吏部尚书定为“非掌部事”“nominal”，等于把标准答案的“未知”答成确定的否定。Q1 写的是“标‘是否掌部事：未知’”，模型里没有这个标记。这一判依据 comment 和 label；若只看结构三元组，可改判部分答对，提请 Yang 决定"),
    ("CQ1", "state"): ("答错", "带衔：张璁，无时间。掌部事：无结果。类型定义同 event 版。", "同 event 版：共用同一类型，把“未知”答成“非掌部事”。另外时间无法限定，杨一清未建模"),
    ("CQ2", "cbdb"): ("答错", "1532 年在任 18 条：四衔都在，同时还有太子太傅、謹身殿大學士、少保，以及兵部右侍郎和各种一次性差遣。",
                      "只到年，新旧衔同时出现：太子太傅、谨身殿大学士与取代它们的太子太师、华盖殿大学士并列（同 J136-U16 distorted）；少保无止年，也被算作仍带"),
    ("CQ2", "event"): ("答对", "少傅、太子太师、吏部尚书、华盖殿大学士；CQ2b 列出太子太傅→太子太师、谨身殿→华盖殿等取代关系；时间含甲寅（1532-04-20）。",
                       "取代靠 D12 推算，属建模者判断（Q7）。太子太师、华盖殿的时间来自 E13（实录、年表、CBDB），列传嘉靖十三年被日期条件排除，本题不呈现分歧（见 CQ4）。卷136“太傅”的 E13 只在 state 版，event 版没有这个异文，结果不受影响"),
    ("CQ2", "state"): ("答不了", "13 个头衔，含合并后的差遣；太傅、少傅有 E13 来源；全部不带时间。", "四衔都在其中，但无法区分哪些在嘉靖十一年四月仍带。holds_title 只表示曾经持有，所以这不是错答"),
    ("CQ3", "cbdb"): ("答错", "文淵閣 1527–1528、謹身殿 1528–1532、華蓋殿 1532– 与 1533–1535 首尾相接；STATUS_DATA、EVENTS_DATA 中无致仕、召还。",
                      "读出来是 1527–1535 一直在阁，与两次致仕矛盾；1533 又是在任提及被记成起始年（同 J149-U01 distorted）"),
    ("CQ3", "event"): ("部分答对", "入阁 1527-11—12、致仕 1531-08-28、召还入阁 1532-01-14 至 04-20（范围）、致仕 1532-10-04；召与赴召：1532-01-14、1532-04-20、1533-02-16、1533-05-06。",
                       "主要时段、范围日期和第二次不在阁都对，1533 之后没有加入事件，不会推出已复任。缺嘉靖八年八月罢、九月召还（卷146 comment 提及，未建），所以第一段读出来是连续的。这是遗漏，不是错误断言，判部分答对；若 Yang 认为这已构成“推出一直在阁”，可改判答错"),
    ("CQ3", "state"): ("答不了", "内阁成员，身份大学士，无任何时间。", "P107 只表示现在或以前的成员，答不出时段（D15 规则 2）"),
    ("CQ4", "cbdb"): ("答错", "421880：1532，备注引明史列传卷196；421883：1533–1535，备注引世宗实录卷149。",
                      "只有自身两条，且两条的出处都有问题：列传实作嘉靖十三年，卷149 只是在任提及。读者会得出“列传作 1532”“实录作 1533”，都与史料矛盾"),
    ("CQ4", "event"): ("答对", "四条 E13：实录卷136 甲寅（1532-04-20）、年表三月、CBDB 1532、列传嘉靖十三年，各带来源；CBDB 来源注明与列传不符。CQ4b：卷141、卷149 的头衔串已作华盖殿，日期早于 1534。",
                       "分歧作为分歧呈现。模型不写裁决（判断层未建，D7 留给 CRMinf），但排除列传所需的依据都在结果里，判断由读者作出。若 Yang 认为标准答案的“判断”须由模型给出，可改判部分答对"),
    ("CQ4", "state"): ("答不了", "持有华盖殿大学士；卷149 头衔串。", "无时间，无 E13，四种说法都没有。卷149 的串也没有日期"),
    ("CQ5", "cbdb"): ("答不了", "少傅 1528–1534，任命方式未詳；同年起始 7 条。", "授予者、起因都没有（同 J089-U05、U06）。只能给出年份"),
    ("CQ5", "event"): ("部分答对", "授予者明世宗，起因明伦大典书成进呈，日期 1528-06-27，同一恩命：加少傅、加太子太傅、升吏部尚书、升谨身殿大学士。CQ5b：此前授予礼部尚书、文渊阁大学士。",
                       "问题本身答对。缺标准答案中的两点：荫一子为中书舍人（未建模）；原衔少保（J089-U12 未建，卷89 原文串也未建）"),
    ("CQ5", "state"): ("答不了", "持有少傅；卷132 E13；卷89 原文串。", "授予者、起因、时间都没有。“谁授予、为什么”无从回答"),
    ("CQ6", "cbdb"): ("部分答对", "BIOG_TEXT_DATA：張璁、劉鈗（未詳）、張衮（編纂者）；任官表：李時 祀儀成典監修官、李時 總裁官（1531）、張璁 總裁官、劉鈗 校正官。",
                      "只得张璁、李时、张衮（且在疑似重复记录 690197 下）三人；郭勋、汪鋐、桂萼、翟銮、廖道南、徐阶、程文德都没有。刘鈗和李时总裁官出自《國朝獻徵錄》，不在卷118，李时 1531 年的总裁官与卷118 的时点不同，不算矛盾"),
    ("CQ6", "event"): ("答对", "十人及差遣，与标准答案一致；夏言不在其中。", "人物识别（卿某）是建模者判断（Yang 确认）"),
    ("CQ6", "state"): ("部分答对", "从书出发走不到人；按四个职名取到十人，名单与差遣都对。", "结果对，但靠查询者预先知道哪四个职名属于修书；头衔与《祀仪成典》没有结构连接，有另一次修书就分不开（D22 的代价）"),
    ("CQ7", "cbdb"): ("答不了", "无结果。", "工程差遣全部未录（REPORT 第 5 节第 12 条），差遣之间也没有关联"),
    ("CQ7", "event"): ("答对", "郭勋、李时、汪鋐、张璁四人及工程差遣→修书差遣；桂萼、翟銮、夏言不在其中。", "P15 语义偏宽（T2），“以……身份”靠约定读出"),
    ("CQ7", "state"): ("部分答对", "同时持有工程、修书头衔的四人，名单正确。", "只说明两者并存，不说明“以……身份”；名单对是因为本案恰好如此。复合差遣按两截分行（D18 的配对丢失）"),
    ("CQ8", "cbdb"): ("答错", "1534 年提学类官职：崔桐（湖广）、徐階 提學使 1534–1539（无地点）；自连接后得徐階 同年 僉事 1534–1536、浙江。",
                      "徐阶和佥事能靠自连接找到，但结果把提學使列为独立职位，与“不是独立职位”矛盾（CBDB U08 已判 distorted）；止年 1539 与佥事的 1536 也不合“以本官带差遣”"),
    ("CQ8", "event"): ("答对", "徐阶，1534-05-05 起，提调学校（差遣职责），地点浙江，所属浙江按察司；本官按察司佥事；离开湖广黄州府，原文串“湖廣黃州府同知徐階”。",
                       "本官与差遣靠父事件间接相连（D26，kept_judgement）；“同知”只在原文串（T4）。差遣的上位类“差遣职责”表达了非独立职位，《职官志》的依据只在决策文档"),
    ("CQ8", "state"): ("部分答对", "徐阶持有提调学校；成员身份两条：浙江按察司 佥事、湖广黄州府 同知。", "人答对；但没有地点和 1534 的限定，两条身份也分不出哪条是当时的本官，又无前后"),
    ("CQ9", "cbdb"): ("部分答对", "同知（止 1534，黃州府）；提刑按察使司僉事 1534–1536（浙江布政司）；提學使 1534–1539（无地点）。",
                      "两处机构与官职都能读出，先后只靠同知止于 1534、佥事始于 1534，同年相接；离任是否隐含看不出；机构由官名加地点拼出（J161-U07）"),
    ("CQ9", "event"): ("答对", "加入浙江按察司（按察司僉事），离开湖广黄州府，同一日；E86 的 comment 注明隐含。", "原身份“同知”不在此结果，见原文串（CQ8）；标准答案的“同知”由此取得。隐含写在 comment 里"),
    ("CQ9", "state"): ("部分答对", "两个机构及身份，无前后。", "机构、身份都对，但问题问的是前后，无时间可排（J161-U07 lost）"),
    ("CQ10", "cbdb"): ("部分答对", "三人任官中备注与编码官名不合的 14 条，含 431870（太子太保，编为太子少保）及同类 420827、424211 等。",
                       "只命中第 4 项（太子太保同类 5 条），另外 9 条是规范化差异或备注错字。其余 4 项没有；CBDB 没有分歧结构，这只是备注与编码的比对"),
    ("CQ10", "event"): ("部分答对", "E13 四条，全部是第 1 项华盖殿时间。", "只有第 1 项。第 2 项太傅的 E13 只在 state 版；第 3、4、5 项（CBDB 起始年、431870、提學使）未建 E13"),
    ("CQ10", "state"): ("部分答对", "E13 两条：卷136 太傅、卷132 少傅。", "只有第 2 项，且无《职官志》依据（卷141 未入卡片）；第 1、3、4、5 项没有"),
}

# 此后的改判写在这里，按顺序应用：(cq_id, version, field, value, 审定/改动日期, 由谁, 轮次)；field 为 verdict / summary / note / approve（只记审定）
OVERRIDES = [
    # ---- eval-cq-v1.1：Yang 审核 2026-11-04（改判、改 note）
    ('CQ1', 'event', 'note',
     '张璁带衔一半答对，杨一清未建模（scope）。模型 label/comment 作“非掌部事”，与 D1（应标“是否掌部事：未知”）不符，属建模错误',
     '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ1', 'state', 'note',
     '模型 label/comment 作“非掌部事”，与 D1（应标“是否掌部事：未知”）不符，属建模错误（与 event 版共用同一类型）。另外时间无法限定，杨一清未建模',
     '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ3', 'event', 'verdict',
     '答错',
     '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ3', 'event', 'note',
     '缺嘉靖八年罢、召，查询推出 1527–1531 连续在阁，与年表矛盾；与 J136-U02（SL12 v1 判 distorted）同类。其余时段、范围日期和第二次不在阁都对，1533 之后没有加入事件，不会推出已复任',
     '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ4', 'event', 'verdict',
     '部分答对',
     '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ4', 'event', 'note',
     '四种说法及依据俱在，但裁决不在模型中（E13 只记主张，裁决留待 CRMinf）',
     '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    # ---- eval-cq-v1.1：Yang 审定 2026-11-04（全部 30 条；approve 只记审定，不改内容）
    ('CQ1', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ1', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ1', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ2', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ2', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ2', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ3', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ3', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ3', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ4', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ4', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ4', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ5', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ5', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ5', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ6', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ6', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ6', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ7', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ7', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ7', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ8', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ8', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ8', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ9', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ9', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ9', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ10', 'cbdb', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ10', 'event', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    ('CQ10', 'state', 'approve', '', '2026-11-04', 'Yang 审定', 'eval-cq-v1.1'),
    # ---- eval-cq-v1.2：Yang 审定 2026-11-04（按“答错”第二句复查）
    ('CQ9', 'cbdb', 'verdict', '答错', '2026-11-04', 'Yang 审定', 'eval-cq-v1.2'),
    ('CQ9', 'cbdb', 'note',
     '结果中“提學使 1534–1539”一行是与卷161 矛盾的肯定性结论（同 CQ8）。两处机构和官职能读出，先后只靠同知止于 1534、佥事始于 1534，同年相接；离任是否隐含看不出；机构由官名加地点拼出（J161-U07）',
     '2026-11-04', 'Yang 审定', 'eval-cq-v1.2'),
]
STATUS = "agent 初判，待 Yang 审核"


def rationale(cq, version):
    ext = "sql" if version == "cbdb" else "rq"
    files = sorted(p for p in QUERIES.iterdir()
                   if p.name.split(".")[0].rstrip("ab") == cq and p.name.split(".")[1:] == [version, ext])
    assert files, (cq, version)
    out = []
    for p in files:
        first = p.read_text(encoding="utf-8").splitlines()[0]
        mark = "-- 理由：" if ext == "sql" else "# 理由："
        assert first.startswith(mark), p.name
        out.append((p.name, first[len(mark):]))
    return out


def results():
    table = {k: dict(zip(("verdict", "summary", "note"), v)) for k, v in VERDICTS.items()}
    status = {k: STATUS for k in table}
    for cq, version, field, value, date, by, rnd in OVERRIDES:
        if field != "approve":
            table[(cq, version)][field] = value
        status[(cq, version)] = f"{by} {date}（{rnd}）"
    ids = [r["cq_id"] for r in csv.DictReader(open(EVAL / "competency_questions.csv", encoding="utf-8", newline=""))]
    assert set(table) == {(c, v) for c in ids for v in VERSIONS}
    rows = []
    for cq in ids:
        for v in VERSIONS:
            r = table[(cq, v)]
            assert r["verdict"] in ("答对", "部分答对", "答不了", "答错"), (cq, v)
            q = rationale(cq, v)
            rows.append([cq, v, r["verdict"], "；".join(n for n, _ in q), " ".join(f"[{n}] {w}" for n, w in q),
                         r["summary"], r["note"], status[(cq, v)]])
    return render(["cq_id", "version", "verdict", "queries", "rationale", "result_summary", "note", "status"], rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--out", default=str(EVAL))
    a = ap.parse_args()
    run_all(a.out)
    (Path(a.out) / "cq_results.csv").write_bytes(results())
