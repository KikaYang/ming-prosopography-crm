"""
Generate the SL14 evaluation tables: cbdb / event / state_vs_units_SL14.csv.
Base: first-pass judgements at tag eval-SL14-v1 (AI agent (Claude Code)); v1.1 re-evaluates the state
version (block 2, Huangzhou Prefecture, was added after the evaluation) and implements the review of 2026-11-03.
Run from the repository root:
    python scripts/eval/sl14.py              # rewrite the three tables in data/evaluation/ and check the evidence
    python scripts/eval/sl14.py --out DIR    # write elsewhere (used by the tests)
Evidence check: model evidence is looked up as triples in the ttl + vocab files of the version recorded in
EVALUATED (evaluated_versions/<tag>/); CBDB evidence by SQL (skipped if the database is absent).
Every change of judgement goes into OVERRIDES (with date, author and round); the tables are not edited directly.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EVAL, write  # noqa: E402

CASE = "SL14"
SUFFIX = "_SL14"
PREFIX = "J161-"
VOCAB_REV = 'eval-SL14-v1.1'
EVALUATED = {'event': ('eval-SL14-v1.1', 'docs/modelling/SL14_event.ttl'), 'state': ('eval-SL14-v1.1', 'docs/modelling/SL14_state.ttl')}

# first-pass judgements (AI agent (Claude Code); tag eval-SL14-v1, commit cf1d4ff), transcribed once from that tag's tables
# and not changed since; every later change goes into OVERRIDES
BASE = {
    'cbdb': [
        ('J161-U01', 'partial', 'omission', 'POSTED_TO_OFFICE_DATA posting_id 424200 c_firstyear=1534 c_fy_nh_code=650 c_fy_nh_year=13 ; 424201 c_firstyear=1534', '否',
         '只到年（嘉靖十三年）；c_fy_month、c_fy_day、c_fy_day_gz 均空；cause：月、日、干支字段存在但未填（同 J118-U05）'),
        ('J161-U02', 'lost', 'limit', '', '是',
         '无事件，因而无发令者；cause：没有发令者字段（同 J118-U07）'),
        ('J161-U03', 'lost', 'omission', '', '否',
         '424200 c_appt_code=0（未詳）；cause：任命方式有“陞”(52)，未使用（同 J118-U42）'),
        ('J161-U04', 'kept', '', 'POSTED_TO_OFFICE_DATA posting_id 432216 c_office_id=70974 同知 c_lastyear=1534 ; POSTED_TO_ADDR_DATA posting_id 432216 c_addr_id=5576 黃州府（ADDR_BELONGS_DATA 属 5520 湖廣布政司）', '否',
         '官职代码只是通用的“同知”，府名靠任职地点表（POSTED_TO_ADDR_DATA）结构化保留，湖廣经 ADDR_BELONGS_DATA 可推出；c_firstyear 空，只有止年 1534。另有重复记录 472581（400010 府同知，同一地点，无年份；见 REPORT.md 第 5 节第 3 条）'),
        ('J161-U05', 'kept', '', 'BIOG_MAIN c_personid 68547 c_name_chn=徐階', '否',
         ''),
        ('J161-U06', 'kept', '', 'POSTED_TO_OFFICE_DATA posting_id 424200（CBDB_line_ID 133446）c_office_id=70944 提刑按察使司僉事 1534–1536 ; POSTED_TO_ADDR_DATA posting_id 424200 c_addr_id=5331 浙江布政司', '否',
         '核心单元。官名被规范化为“提刑按察使司僉事”，省份从官名中去掉（REPORT.md 第 5 节第 4 条），但浙江作为任职地点保存在 POSTED_TO_ADDR_DATA（5331 浙江布政司），可查询，故判 kept。与提调学校拆成两条无关联的记录，见 J161-U09'),
        ('J161-U07', 'partial', 'limit', 'POSTED_TO_OFFICE_DATA posting_id 432216 c_office_id=70974 同知 c_lastyear=1534 ; POSTED_TO_ADDR_DATA posting_id 432216 c_addr_id=5576 黃州府（ADDR_BELONGS_DATA 属 5520 湖廣布政司） ; POSTED_TO_OFFICE_DATA posting_id 424200（CBDB_line_ID 133446）c_office_id=70944 提刑按察使司僉事 1534–1536 ; POSTED_TO_ADDR_DATA posting_id 424200 c_addr_id=5331 浙江布政司', '是',
         '核心单元。同知止于 1534、佥事始于 1534，由年份只能推出两任在同一年相接，推不出先后，也推不出因升而离任；两条之间没有任何关联。cause：CBDB 无记录之间的前后任关联字段；“陞”(52) 只能标出新官由升得来，不能指明由何官升（“陞”未用，计入 J161-U03）'),
        ('J161-U08', 'partial', 'omission', 'POSTED_TO_OFFICE_DATA posting_id 424201（CBDB_line_ID 133447）c_office_id=70951 提學使 1534–1539 ; c_notes=[提學使](提調學校)(明實錄:世宗實錄;161卷)', '否',
         '核心单元。职能“提学”在，但编为 70951 提學使（Commissioner of an Education Intendant Circuit，一个独立的职位），原文“提調學校”只在 c_notes；未标官职类别（c_office_category_id 空）。cause：OFFICE_CODES 有 70923 提調學校（Supervisor of Education，库中已用 6 次）和类别 15 兼職差遣，均未使用。提學使作为职位编码，是否构成 distorted（会被读成另一个官职），提请 Yang 决定'),
        ('J161-U09', 'partial', 'omission', 'POSTED_TO_OFFICE_DATA posting_id 424200（CBDB_line_ID 133446）c_office_id=70944 提刑按察使司僉事 1534–1536 ; POSTED_TO_ADDR_DATA posting_id 424200 c_addr_id=5331 浙江布政司 ; POSTED_TO_OFFICE_DATA posting_id 424201（CBDB_line_ID 133447）c_office_id=70951 提學使 1534–1539 ; c_notes=[提學使](提調學校)(明實錄:世宗實錄;161卷)', '否',
         '核心单元。本官（424200）与差遣（424201）拆成两条无关联的记录，同引卷161；年份 1534–1536 与 1534–1539 重叠，可推出并存，推不出“以佥事带提调学校”（属“可由年份推出并存”的 partial）。两条止年不同，也与“以本官带差遣”不合。cause：OFFICE_CODES 有合并代码 72462 提刑按察使司提學僉事（库中已用 7 次），类别 15 兼職差遣亦可标出差遣性质，均未使用，故为 omission'),
        ('J161-U10', 'notes_only', 'omission', 'POSTED_TO_OFFICE_DATA posting_id 424200 c_notes=…(明實錄:世宗實錄;161卷) ; 424201 c_notes=…(明實錄:世宗實錄;161卷)', '否',
         '卷号只在 c_notes；c_source 为 9602（人名權威資料）；cause：可用《世宗實錄》（TEXT_CODES 13593）作 c_source、卷号入 c_pages（同 J118-U66）'),
    ],
    'event': [
        ('J161-U01', 'kept', '', 'event:jj13-03-jimao-sheng crm:P4_has_time-span ts:jj13-03-jimao ; ts:jj13-03-jimao crm:P1_is_identified_by name:date-jj13-03-jimao ; name:date-jj13-03-jimao rdfs:label "嘉靖十三年三月己卯"@zh-Hant', '否',
         '格里历 1534-05-05（D14，已与中研院核对）'),
        ('J161-U02', 'kept_judgement', '', 'event:jj13-03-jimao-sheng crm:P14_carried_out_by person:ming-shizong', '是',
         '隐含主语由建模者写为明世宗（D23）'),
        ('J161-U03', 'kept', '', 'event:jj13-03-jimao-sheng crm:P2_has_type type:action-sheng ; event:jj13-03-jimao-sheng crm:P11_had_participant person:68547', '否',
         '父事件（D23）'),
        ('J161-U04', 'partial', 'limit', 'event:jj13-03-jimao-sheng-2 rdf:type crm:E86_Leaving ; event:jj13-03-jimao-sheng-2 crm:P145_separated person:68547 ; event:jj13-03-jimao-sheng-2 crm:P146_separated_from group:huangzhou-fu ; name:guanxian-jj13-03-jimao-xu-jie-yuan rdfs:label "湖廣黃州府同知徐階"@zh-Hant ; person:68547 crm:P1_is_identified_by name:guanxian-jj13-03-jimao-xu-jie-yuan', '否',
         '核心单元。离开黄州府经隐含的 E86 + P146 结构化（D24）；离开时的身份“同知”无法写出：CIDOC-CRM 7.1.3 中 P146 没有 .1 属性，也没有 PC146（D24、T4），“同知”只在原文串的 rdfs:label 里。cause：CRM 本身的限制，不标约定所致。另一种做法是另建一个时间未知的 E85 + PC144（加入黄州府，身份同知），D24 未采用；如 Yang 认为应采用，此行改判 omission'),
        ('J161-U05', 'partial', 'omission', 'person:68547 crm:P1_is_identified_by name:guanxian-jj13-03-jimao-xu-jie-yuan', '否',
         '姓名只在原文串的文字和人物的 rdfs:label 中，无本名 E41；cause：徐阶为核心人物，可按 D6 建，未建（判法 1，同 J118-U50）'),
        ('J161-U06', 'kept', '', 'event:jj13-03-jimao-sheng-1 crm:P143_joined person:68547 ; event:jj13-03-jimao-sheng-1 crm:P144_joined_with group:zhejiang-anchasi ; pc:jj13-03-jimao-sheng-1-anchasi crm:P01_has_domain event:jj13-03-jimao-sheng-1 ; pc:jj13-03-jimao-sheng-1-anchasi crm:P144.1_kind_of_member type:anchasi-qianshi ; event:jj13-03-jimao-sheng crm:P9_consists_of event:jj13-03-jimao-sheng-1', '否',
         '核心单元。E85 + PC144（D3）；省份在机构 group:zhejiang-anchasi 中（与 CBDB 的规范化官名不同，省份未丢失）'),
        ('J161-U07', 'kept_judgement', '', 'event:jj13-03-jimao-sheng crm:P2_has_type type:action-sheng ; event:jj13-03-jimao-sheng crm:P9_consists_of event:jj13-03-jimao-sheng-1 ; event:jj13-03-jimao-sheng crm:P9_consists_of event:jj13-03-jimao-sheng-2 ; event:jj13-03-jimao-sheng-2 rdf:type crm:E86_Leaving ; event:jj13-03-jimao-sheng-2 crm:P145_separated person:68547 ; event:jj13-03-jimao-sheng-2 crm:P146_separated_from group:huangzhou-fu', '是',
         '核心单元。“升”父事件把加入浙江按察司（E85）与离开黄州府（E86）作为组成部分结构化相连（D23）；离任为隐含，由建模者按 D24 补建，故判 kept_judgement。先后：两者是同一升调的组成部分，同时发生，无需另表先后。离开时的身份“同知”未表达，见 J161-U04'),
        ('J161-U08', 'kept', '', 'event:chaiqian-68547-tidiao-xuexiao crm:P2_has_type type:tidiao-xuexiao ; event:chaiqian-68547-tidiao-xuexiao crm:P14_carried_out_by person:68547 ; event:chaiqian-68547-tidiao-xuexiao crm:P7_took_place_at place:zhejiang', '否',
         '核心单元。差遣节点（D16、D25），地点浙江用 P7；未编造所属之“事”（D25）'),
        ('J161-U09', 'kept_judgement', '', 'event:chaiqian-68547-tidiao-xuexiao crm:P17_was_motivated_by event:jj13-03-jimao-sheng ; event:jj13-03-jimao-sheng crm:P9_consists_of event:jj13-03-jimao-sheng-1 ; event:jj13-03-jimao-sheng-1 crm:P144_joined_with group:zhejiang-anchasi ; event:chaiqian-68547-tidiao-xuexiao crm:P11_had_participant group:zhejiang-anchasi', '否',
         '核心单元。“以本官带差遣”没有直接连线：差遣节点经 P17 指向父事件，父事件经 P9 含加入按察司的 E85（佥事），差遣节点再以 P11 连到同一机构（D25、D26）。靠两条间接路径加建模者的约定才能读出，故判 kept_judgement（D26 预期）。本官与差遣形态不同（E85 与任职节点）见 T1'),
        ('J161-U10', 'kept', '', 'doc:shizong-shilu-161 rdf:type crm:E31_Document ; doc:shizong-shilu-161 crm:P70_documents event:jj13-03-jimao-sheng ; doc:shizong-shilu-161 crm:P70_documents event:chaiqian-68547-tidiao-xuexiao', '否',
         '所有事件都有卷161 的 P70（D7）；原文串另有 P67'),
    ],
    'state': [
        ('J161-U01', 'lost', 'limit', '', '否',
         'state 版不带时间（D15 规则 2）'),
        ('J161-U02', 'lost', 'limit', '', '是',
         'state 版不建事件（D15），因而无发令者；约定所致（D15）'),
        ('J161-U03', 'lost', 'limit', '', '否',
         'state 版不建事件（D15）；P107 无法带“升”；约定所致（D15）'),
        ('J161-U04', 'partial', 'omission', 'name:guanxian-jj13-03-jimao-xu-jie-yuan rdfs:label "湖廣黃州府同知徐階"@zh-Hant ; person:68547 crm:P1_is_identified_by name:guanxian-jj13-03-jimao-xu-jie-yuan', '否',
         '核心单元。按现状判：第②块只有浙江按察司的 P107 + PC107，没有黄州府（提交 96ade00 的说明写“浙江按察司、黄州府”，与文件不符）；“同知”与黄州府只在原文串的 rdfs:label 里。cause：可写 group:huangzhou-fu P107 person:68547 + PC107（P107.1 type:fu-tongzhi，词汇已在 vocab），未写。写入后重评（判法 4）；写入后预期 kept（PC107 可带身份，这是 state 版相对 event 版的优势，见 T4）'),
        ('J161-U05', 'partial', 'omission', 'person:68547 crm:P1_is_identified_by name:guanxian-jj13-03-jimao-xu-jie-yuan', '否',
         '姓名只在原文串的文字和人物的 rdfs:label 中，无本名 E41；cause：徐阶为核心人物，可按 D6 建，未建（判法 1，同 J118-U50）'),
        ('J161-U06', 'kept', '', 'group:zhejiang-anchasi crm:P107_has_current_or_former_member person:68547 ; pc:zhejiang-anchasi-member-68547 crm:P01_has_domain group:zhejiang-anchasi ; pc:zhejiang-anchasi-member-68547 crm:P02_has_range person:68547 ; pc:zhejiang-anchasi-member-68547 crm:P107.1_kind_of_member type:anchasi-qianshi', '否',
         '核心单元。P107 + PC107（D22），身份按察司佥事'),
        ('J161-U07', 'lost', 'limit', '', '是',
         '核心单元。state 版不建事件（D15），“升”与离任无从表达；P107 不带时间（D15 规则 2），即使补写黄州府的 P107，两段成员身份也推不出先后（属“连并存也推不出”）。约定所致（D15；先后顺序的时间部分属 CRM 本身）'),
        ('J161-U08', 'kept_ext', '', 'person:68547 mpv:holds_title type:tidiao-xuexiao', '否',
         '核心单元。靠扩展属性 mpv:holds_title（D22）；地点浙江未表达'),
        ('J161-U09', 'lost', 'limit', '', '否',
         '核心单元。佥事（P107 + PC107）与提调学校（holds_title）是两条互不相连的陈述，都不带时间，推不出并存，更推不出“以佥事带提调学校”（属“连并存也推不出”）。D22 把无机构的差遣写成 holds_title；提调学校按 D25 有所属机构，仍写作 holds_title（Yang 编写），因而无法连到按察司。约定所致（D15、D22；同时性的时间部分属 CRM 本身）'),
        ('J161-U10', 'kept', '', 'doc:shizong-shilu-161 rdf:type crm:E31_Document ; doc:shizong-shilu-161 crm:P67_refers_to name:guanxian-jj13-03-jimao-xu-jie-yuan', '否',
         '出处只连到原文串（无事件，故无 P70）'),
    ],
}

# (version, unit_id, op, value, 审定/改动日期, 由谁, 轮次)；按顺序应用
OVERRIDES = [
    # ---- eval-SL14-v1.1
    ('cbdb', 'J161-U01', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U02', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U03', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U04', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U05', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U06', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U07', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U08', 'judgement', 'distorted', '2026-11-03', 'Yang', 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U08', 'note', '核心单元。编为 70951 提學使，使徐阶多出一个独立职位：《明史·职官四》按察司下只有“提督学道”，由副使、佥事分管，无“提学使”之职；原文“提調學校”只在 c_notes，未标官职类别。cause：OFFICE_CODES 有 70923 提調學校（库中已用 6 次）、72462 提刑按察使司提學僉事（已用 7 次），类别 15 兼職差遣亦可用，均未使用（Yang 审定 2026-11-03，原判 partial / omission）', '2026-11-03', 'Yang', 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U09', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('cbdb', 'J161-U10', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U01', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U02', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U03', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U04', 'cause', 'omission', '2026-11-03', 'Yang', 'eval-SL14-v1.1'),
    ('event', 'J161-U04', 'note', '核心单元。离开黄州府经隐含的 E86 + P146 结构化（D24）；“同知”只在原文串的 rdfs:label 里。cause：可另建一个时间未知的 E85 + PC144（加入黄州府，P144.1 身份同知）表达原官，未建。CRM 能表达曾任某职，但不能表达以何身份离开（P146 无 .1 属性，见 T4）（Yang 审定 2026-11-03，原判 partial / limit）', '2026-11-03', 'Yang', 'eval-SL14-v1.1'),
    ('event', 'J161-U05', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U06', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U07', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U08', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U09', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('event', 'J161-U10', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U01', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U02', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U03', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U04', 'judgement', 'kept', '2026-11-03', 'agent（重评）', 'eval-SL14-v1.1'),
    ('state', 'J161-U04', 'cause', '', '2026-11-03', 'agent（重评）', 'eval-SL14-v1.1'),
    ('state', 'J161-U04', 'evidence', 'group:huangzhou-fu crm:P107_has_current_or_former_member person:68547 ; pc:huangzhou-fu-member-68547 crm:P01_has_domain group:huangzhou-fu ; pc:huangzhou-fu-member-68547 crm:P02_has_range person:68547 ; pc:huangzhou-fu-member-68547 crm:P107.1_kind_of_member type:fu-tongzhi', '2026-11-03', 'agent（重评）', 'eval-SL14-v1.1'),
    ('state', 'J161-U04', 'note', '核心单元。P107 + PC107，身份府同知（P107.1 type:fu-tongzhi）：PC107 能带身份，这是 state 版相对 event 版的不同（见 T4）；不带时间，“原官”之“原”（在佥事之前）推不出，见 J161-U07。v1.1 重评：第②块黄州府为评价后补入（5cf2a2a），v1 按现状判 partial / omission；待 Yang 审核', '2026-11-03', 'agent（重评）', 'eval-SL14-v1.1'),
    ('state', 'J161-U05', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U06', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U07', 'note', '核心单元。state 版不建事件（D15），“升”与离任无从表达；黄州府（同知）与浙江按察司（佥事）两段成员身份都已写出，但 P107 不带时间（D15 规则 2），推不出先后（属“连并存也推不出”）。约定所致（D15；先后顺序的时间部分属 CRM 本身）；v1.1 只按补入的黄州府改写 note 措辞，判定不变；Yang 审定 2026-11-03：同意', '2026-11-03', 'agent（重评）', 'eval-SL14-v1.1'),
    ('state', 'J161-U08', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U09', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    ('state', 'J161-U10', "note+", "Yang 审定 2026-11-03：同意", '2026-11-03', "Yang", 'eval-SL14-v1.1'),
    # ---- eval-SL14-v1.1 审定补记（state U04 的重评判定经 Yang 审定）
    ('state', 'J161-U04', 'note', '核心单元。P107 + PC107，身份府同知（P107.1 type:fu-tongzhi）：PC107 能带身份，这是 state 版相对 event 版的不同（见 T4）；不带时间，“原官”之“原”（在佥事之前）推不出，见 J161-U07。v1.1 重评：第②块黄州府为评价后补入（5cf2a2a），v1 按现状判 partial / omission；Yang 审定 2026-11-03：同意', '2026-11-03', 'Yang', 'eval-SL14-v1.1 审定补记'),
]


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--out", default=str(EVAL), help="output directory (default data/evaluation/)")
    ap.add_argument("--no-verify", action="store_true", help="skip the evidence checks (ttl at EVALUATED, CBDB)")
    a = ap.parse_args()
    for p in write(sys.modules[__name__], a.out, verify=not a.no_verify):
        print(p)
