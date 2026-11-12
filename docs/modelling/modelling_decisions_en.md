# Modelling decision log (from SL12 onwards)

> English version of the author's modelling decision log.
> Translation notes: office titles follow Hucker (1985), *A Dictionary of Official Titles in Imperial China*, and match the English labels in `docs/modelling/vocab.ttl`; titles not in Hucker are translated into English (basis given in the glossary); hall names are kept in pinyin. Quotations from historical sources are kept in Chinese, with an English gloss where helpful. Turtle code blocks are reproduced unchanged.

> Decisions and rationale: Yang. Drafting and alternative options: AI agent (Claude Code).
> Version: 2026-10-12. All classes and properties have been checked against CIDOC-CRM 7.1.3 (including the PC extension).
> Convention: the event version is the main model; the state version serves only as a point of comparison, used in the argument for RQ1.

---

## Code reference

(Added 2026-11-08. Each description summarises the original entry, which prevails; each status is taken from the entry itself. Q items have three statuses: resolved / provisionally handled, awaiting confirmation / open. T items have two statuses: open / reviewed (see "Review of 2026-11-09").)

### Modelling decisions D1–D26

| Code | Description | Status |
|---|---|---|
| D1 | A grand secretary's "Minister of X" is a concurrent rank title; an E85 is created only when the source states that he was in charge of the ministry | In force |
| D2 | A title conferral is an E7, linked to the title by mpv:conferred_title | In force |
| D3 | The Grand Secretariat is an E74; entry uses E85 + PC144; hall names are types | In force |
| D4 | No type for *jian* 兼; a title classification tree plus the original title string | In force |
| D5 | Retirement is an E86 from the Grand Secretariat; titles are not withdrawn; recall is an E85 | In force |
| D6 | Personal name and bestowed name are separate E41s, distinguished by P2 | In force |
| D7 | Every event carries a P70 source; disputed claims use E13 | In force |
| D8 | URIs based on GitHub Pages; vocabulary and instances kept apart | In force |
| D9 | Source text in traditional characters (@zh-Hant); project vocabulary in simplified characters plus @en | In force |
| D10 | Properties referenced by P177 are explicitly declared as E55 | In force |
| D11 | Information units first, then modelling, then evaluation (SL12 excepted) | In force |
| D12 | Within one broader class, a later title replaces an earlier one | In force |
| D13 | One decree is a parent event; each title conferred is a sub-event | In force |
| D14 | P82a/b in the Gregorian calendar, with Julian date and sexagenary day noted | In force |
| D15 | The state version has no events; it uses holds_title and no time | In force |
| D16 | A duty assignment is an E7 activity node, P9i part of the undertaking it serves | In force |
| D17 | A duty assignment held in the capacity of another: P15 to the earlier assignment node | In force |
| D18 | A compound assignment name is one node with two types (rank and function) | In force |
| D19 | Being in charge of an office's affairs is a node, with P11 to that office | In force |
| D20 | Editorial principles are an E29; the book being compiled is an E73 | In force |
| D21 | The three core persons are modelled in full; others only where relevant to the case | In force |
| D22 | In the state version, assignments without an institution use holds_title | In force |
| D23 | A promotion is a parent event, with E85 and E86 as its parts | In force |
| D24 | Where "promoted from A to B" does not state the departure, an implicit E86 is added | In force |
| D25 | A standing assignment invents no "undertaking"; P7 to a place, P11 to the institution | In force |
| D26 | The substantive office's E85 and the assignment node are linked through the same parent event | In force |

### Questions awaiting historical confirmation Q1–Q7

| Code | Description | Status |
|---|---|---|
| Q1 | Whether Zhang Cong was actually in charge of the Ministry of Personnel after 1528 | Resolved |
| Q2 | Whether all titles were retained after retirement | Provisionally handled, awaiting confirmation |
| Q3 | Whether promotion between hall titles implied a change of function | Provisionally handled, awaiting confirmation |
| Q4 | The exact dates of Zhang Cong's retirements and recalls | Resolved (within the scope of SL12) |
| Q5 | The exact date of conferral of Huagaidian Daxueshi | Treated as a divergence (E13 claims side by side) |
| Q6 | Whether the 1533 reinstatement dates from the decree (first month) or the arrival in the capital (fourth month) | Resolved (within the scope of SL12) |
| Q7 | Whether a promotion within the same series always replaces the earlier title | Provisionally handled, awaiting confirmation |

### CRM limitations and questions for testing T1–T4

| Code | Description | Status |
|---|---|---|
| T1 | Whether the substantive office should also be modelled as an office-holding node (option 4B) | Open |
| T2 | "In the capacity of": the type of capacity can be expressed with PC14 + P14.1; pointing to a specific assignment requires P17/P134 (partly expressible) | Reviewed (2026-11-09) |
| T3 | "In charge of affairs": P11 carries no sense of direction; an E7 carried out by the institution + P14/P14.1 would be preferable (a choice of pattern) | Reviewed (2026-11-09) |
| T4 | Capacity on departure: expressible if, as in the CRM examples, the office itself is an E74; the gap comes from the D3 convention | Reviewed (2026-11-09) |

### Cases and competency questions

| Code | Description |
|---|---|
| SL12 | Juan 89, 136, 149: Zhang Cong's title conferrals, entry into the Grand Secretariat, retirement, and the divergence over Huagaidian |
| SL11 | Juan 118: the edict of Jiajing 9, tenth month, *xinwei* day; duty assignments for compiling the *Siyi chengdian* |
| SL14 | Juan 161: Xu Jie promoted to Assistant Surveillance Commissioner of Zhejiang, Supervisor of Education |
| CQ1 | After 1528, who held the title Minister of Personnel, and who was actually in charge of the ministry |
| CQ2 | Which titles Zhang Fujing held in the fourth month of Jiajing 11 |
| CQ3 | In which periods of 1527–1533 Zhang Cong was in the Grand Secretariat, and in which he was not |
| CQ4 | When Zhang Cong received Huagaidian Daxueshi, and what each source says |
| CQ5 | Who conferred Junior Mentor on Zhang Cong, and why |
| CQ6 | Who made up the compilation team of the *Siyi chengdian*, and in what roles |
| CQ7 | Who was appointed to a compilation assignment in the capacity of a construction assignment |
| CQ8 | Who was Supervisor of Education in Zhejiang in 1534, and what was his substantive office |
| CQ9 | In which institutions Xu Jie served before and after the third month of Jiajing 13 |
| CQ10 | Which statements diverge across the three cases, and on what grounds |

---

## D1 How to express "Minister of Personnel" → option D: distinguish the ministerial title from being in charge of the ministry

**Decision**
- A grand secretary's "Minister of X" is treated as a **concurrent rank title**, through the same mechanism as honorary titles (see D2).
- Only when a source explicitly records "in charge of the ministry's affairs" (掌部事) or an equivalent expression is an E85 Joining (joining that ministry) created, with P144.1 kind of member "Minister".
- When a source does not say whether he was in charge of the ministry, only the concurrent title is created, with the note "in charge of the ministry: unknown".

**Rationale**
- In the Ming, the minister as a post was held by one person per ministry (who directed its business), but as a concurrent rank title of a grand secretary it could be conferred on several people at once.
- The sources themselves distinguish the two:
  - *Shizong shilu*, juan 89 (Jiajing 7, sixth month, *xinchou*, first day): Yang Yiqing and Zhang Cong both held "Minister of Personnel";
  - *Shizong shilu*, juan 383 (SL15): on Xu Jie's entry into the Grand Secretariat the text notes specifically that he "remained in charge of the ministry" (仍掌部事).
- If every "Minister" were modelled as joining a ministry, the model would wrongly conclude that a ministry had two ministers at the same time.

**Significance for RQ1**
"The same title is an office in one context and a rank in another": CRM has no ready-made structure to distinguish the two, so the distinction depends on a modelling convention plus an extension property. This is how the substantive office / duty assignment problem appears in the Ming.

**Dating**
Zhang Cong's promotion to Minister of Personnel (concurrent title) is in juan 89, Jiajing 7, sixth month. CBDB 130150 gives 1533 as the start year, which is inaccurate: juan 149 only mentions him in office.

**Source basis**
*Mingshi*, juan 72, Treatise on Officials 1: "其后大学士杨士奇等加至三孤，兼尚书衔" (thereafter grand secretaries such as Yang Shiqi were raised to the Three Solitaries and given concurrent ministerial titles) [page reference in the Zhonghua edition to be added]. (approved by the author, 2026-10-24)

**Known defect** (approved by the author, 2026-11-04)
Known defect: the label of type:shangshu-personnel-xian does not agree with D1; see CQ1. Not changed for now; to be revised together with other changes.

Check of 2026-11-08: *Mingshi*, juan 112, Table of the Seven Chief Ministers 2, column for Minister of Personnel:
from Jiajing 6, eleventh month, to Jiajing 8, second month, the minister was Gui E; in Jiajing 8, second month, Gui E entered the Grand Secretariat and was succeeded by Fang Xianfu; Zhang Cong does not appear in this column.
Wherever a grand secretary was in charge of a ministry, the table notes it: Jiajing 11, "献夫七月以内阁掌部事" (Xianfu, in the seventh month, in charge of the ministry while in the Grand Secretariat);
Jiajing 21, "嵩八月入阁，仍掌部事" (Song entered the Grand Secretariat in the eighth month and remained in charge of the ministry); Jiajing 22, "嵩四月解部事" (Song relinquished the ministry in the fourth month).
Conclusion: the Minister of Personnel conferred on Zhang Cong in Jiajing 7, sixth month, did not involve being in charge of the ministry.
Treatment: deferred to v3 — the label of type:shangshu-personnel-xian in the vocabulary is to be made neutral,
and "not in charge of the ministry" is to be restated as an E13 assertion with juan 112 as its source; the gold-standard answer to CQ1 will be updated with the new version,
and eval-cq-v1.x remains unchanged.

Supplement (2026-11-12): whether a grand secretary actually ran a ministry is decided on the basis of (1) an explicit statement in the sources, such as "in charge of the ministry's affairs" (掌部事); or (2) his name appearing in the ministry's column of a table of office holders, such as the Table of the Seven Chief Ministers in the *Mingshi*. Wording that merely confers a post, such as "promoted to Minister of …", is not sufficient, because grand secretaries often held a ministerial title as a rank (for example, in the same decree of Jiajing 7, sixth month, Yang Yiqing already held the title of Minister of Personnel and Zhang Cong was promoted to Minister of Personnel, while the Personnel column of the Table of the Seven Chief Ministers lists Gui E). Where neither applies, the title is treated as a concurrent rank title.
Check: *Mingshi*, juan 112, does not mention Zhang Cong or Zhang Fujing anywhere. From Jiajing 9, ninth month, to Jiajing 10, twelfth month, no one is listed in the Personnel column; according to the biography of Fang Xianfu in *Mingshi*, juan 196, Fang Xianfu asked for leave on grounds of illness, and "帝即报允，然犹虚位以俟" (the emperor at once granted it, but still kept the post vacant to await him): the post was kept vacant for Fang Xianfu, and the ministry was not run by anyone else.
Conclusion: the titles Minister of Personnel and Minister of Rites that Zhang Cong held while a grand secretary (Jiajing 6 to 14) were both concurrent rank titles; he was not in charge of either ministry.
The conclusion of the check of 2026-11-08 is accordingly extended to this whole period.

---

## D2 Honorary titles such as Junior Mentor and Grand Preceptor of the Heir Apparent have no corresponding institution → option D, adjusted: the extension property is attached to the conferral event

**Decision**
- Each conferral is an E7 Activity, typed as an honorary-title conferral (or "promote", following the source's wording), with P14 carried out by pointing to the emperor, P11 had participant pointing to the recipient, and P4 for the time.
- **One** extension property is added, `mpv:conferred_title` (domain E7 Activity, range E55 Type), linking the conferral event to the title conferred.
- When one decree confers several titles, only one event is created, carrying several `mpv:conferred_title` values.
- The occasion of the decree is expressed with P17 was motivated by, e.g. "the completion and presentation of the *Minglun dadian*".

**Rationale**
- The Three Solitaries and the Three Preceptors of the Heir Apparent had no actual institution in the Ming, so P144/P107 cannot be used (both require an E74 Group).
- E13 is not used for historical conferrals: E13 is already used for the factoid layer ("what a source says"), and one class serving both roles would conflate the two layers.
- The extension property is attached to the event, not to the person: on the person it would, as in the state version, have no time.
- Only one property is added; everything else follows CRM.
- Source basis: *Mingshi*, juan 72, Treatise on Officials 1: "自此以后，公、孤但虚衔，为勋戚文武大臣加官、赠官" (from then on, the Dukes and Solitaries were merely nominal titles, added or granted posthumously to nobles and to high civil and military officials); "由是东宫师傅止为兼官、加官及赠官……终明世皆为虚衔" (thereafter the preceptors and mentors of the Heir Apparent were only concurrent, added or posthumous titles … nominal throughout the Ming) [page reference in the Zhonghua edition to be added]. (approved by the author, 2026-10-24)

**Example (juan 89)**
```turtle
event:jj07-06-jiaen a crm:E7_Activity ;
    crm:P2_has_type type:jiaen ;                     # 加恩
    crm:P14_carried_out_by person:shizong ;
    crm:P11_had_participant person:68266 ;
    crm:P4_has_time-span ts:jj07-06-xinchou ;
    crm:P17_was_motivated_by event:minglun-dadian-jincheng ;
    mpv:conferred_title type:shaofu ,                 # 加
                       type:taizi-taifu ,            # 加
                       type:libu-shangshu-xian ,     # 升（兼衔，D1）
                       type:jinshendian-daxueshi .   # 升（殿阁衔，D3）

mpv:conferred_title a rdf:Property ;
    rdfs:label "conferred title"@en , "授衔"@zh ;
    rdfs:domain crm:E7_Activity ;
    rdfs:range  crm:E55_Type ;
    rdfs:comment "扩展属性：一次授予活动所授予的头衔。CIDOC-CRM 7.1.3 中无对应属性。"@zh .
```

**Details still open**
- Whether "add" (加) and "promote" (升) should be distinguished: they could be two sub-properties, or the event could be given a P2 type. This can wait until more cases are available.
- In juan 89, "promoted to Jinshendian Daxueshi" also implies a change in standing within the Grand Secretariat and needs to be aligned with the E85 Joining of D3 (see D3).

---

## D3 Is Huagaidian Daxueshi a substantive office or an honorary title? → option C

**Decision**
- The Grand Secretariat is an E74 Group; entry uses E85 Joining, with P144.1 kind of member "Grand Secretary" on the PC144.
- Hall names (Huagaidian, Jinshendian, Wenyuange, Wuyingdian 武英殿, Dongge 東閣 …) are separate E55 types, recorded in the title classification (see D4).
- Promotion between halls (e.g. Jinshendian → Huagaidian) is treated as a conferral event (see D2), not as a new entry into the Grand Secretariat.

**Rationale**
- The Grand Secretariat was not a statutory office in the Ming, but in practice it operated as a group, responsible for drafting rescripts and similar business (sources: *Mingshi*, Treatise on Officials; Wang Qiju, *Mingdai neige zhidu shi*).
- *Shizong shilu*, juan 89, uses "promote" (升) for hall titles, distinguishing them from "add" (加) for the Solitaries and the Heir Apparent's titles; this shows that hall titles differ in nature from honorific titles.
- This makes it possible to query directly "who was in the Grand Secretariat in a given year".

**Time constraint**
In Jiajing 41 Huagaidian was renamed Zhongjidian 中極殿 (Jinshendian was at the same time renamed Jianjidian 建極殿). Hall names must therefore be distinguished by date; this belongs to the RQ1 theme of "titles valid for a limited period".

---

## D4 The character *jian* 兼 ("concurrently") → changed to "title classification + original text"; no separate *jian* type

**Decision**
1. A title classification tree is built with P127 has broader term:
   ```
   少师 / 少傅 / 少保            → 三孤     → 加衔
   太子太师 / 太子太傅 / 太子太保 → 东宫三师 → 加衔
   某部尚书（兼衔）              → 品阶兼衔
   某部尚书（掌部事）            → 本官
   某殿/某阁大学士               → 殿阁衔
   ```
   (Shaoshi 少師 / Junior Mentor / Junior Guardian → Three Solitaries → honorary title; Grand Preceptor / Grand Mentor / Taizi taibao 太子太保 of the Heir Apparent → Three Preceptors of the Heir Apparent → honorary title; Minister of X (concurrent) → concurrent rank title; Minister of X (in charge of the ministry) → substantive office; Grand Secretary of a hall → grand secretary hall title.)
2. The original title string is an E41 (type "official title string") attached to the person with P1, and the source document points to it with P67 refers to. Cost: the string itself carries no time; its time is obtained indirectly through "document → P70 documented event → P4 time-span". (approved by the author, 2026-10-16)
3. No *jian* type is created. The hierarchy expressed by *jian* is preserved jointly by the title classification and the original string.

**Rationale**
- *Jian* has at least two uses in the sources: a Solitary title held concurrently with an Heir Apparent title (少保兼太子太保), and a substantive office held concurrently with a hall title (礼部尚书兼文渊阁大学士). A single *jian* type cannot distinguish them.
- Once the titles are classified, most of the hierarchy can be inferred; what cannot be inferred is still preserved in the original string.
- Keeping the original string also addresses directly the "splitting of compound titles" found in the *Shilu* checks: once CBDB splits a title string, the original string is lost.
- Source basis: *Mingshi*, juan 72, Treatise on Officials 1: "自此以后，公、孤但虚衔，为勋戚文武大臣加官、赠官"; "由是东宫师傅止为兼官、加官及赠官……终明世皆为虚衔" [page reference in the Zhonghua edition to be added]. (approved by the author, 2026-10-24)

**Example**
```turtle
type:shaofu a crm:E55_Type ; rdfs:label "少傅" ;
    crm:P127_has_broader_term type:sangu .
type:sangu a crm:E55_Type ; rdfs:label "三孤" ;
    crm:P127_has_broader_term type:jiaxian .
type:jiaxian a crm:E55_Type ; rdfs:label "加衔" .
```

---

## D5 Retirement and answering a summons → option A

**Decision**
- Retirement is an E86 Leaving of type "retirement from office", with P145 separated pointing to the person and P146 separated from pointing to the **Grand Secretariat** (E74).
- Retirement does not affect titles already conferred: titles have only conferral events (D2), no withdrawal events.
- Reinstatement on a summons is a new E85 Joining of the Grand Secretariat, of type "recall to office".
- "Retired status" is not modelled separately; it is the period between a Leaving and the next Joining.

**Rationale**
- Juan 149 refers to Zhang Fujing as "致仕少傅兼太子太师、吏部尚书、华盖殿大学士" (retired Junior Mentor and Grand Preceptor of the Heir Apparent, Minister of Personnel, Huagaidian Daxueshi), which shows that the titles were retained after retirement.
- Consistent with D1: the ministerial title is concurrent, so retirement does not require "leaving the Ministry of Personnel"; he leaves only the Grand Secretariat, which keeps the logic simple.

**To be checked**
The exact dates of Zhang Cong's several retirements and recalls are to be added after checking each juan.

Reinstatement after recall is for now not created as an E85; this will be decided once Q6 (whether reinstatement dates from the decree or from the arrival in the capital) is confirmed. (approved by the author, 2026-10-16)

Supplement: where the source says "令／著致仕" (ordered to retire), P14 records the emperor; recall and re-entry into the Grand Secretariat is an E85, with P82a/b expressing a range when the date is uncertain; Q6 is resolved within the scope of SL12. (approved by the author, 2026-10-24)

---

## D6 Change of name → option A

**Decision**
- The two E41s "張璁" (Zhang Cong) and "張孚敬" (Zhang Fujing) are both attached to the person with P1 is identified by, and typed with P2 has type as "personal name" and "name bestowed by the emperor".

**Rationale**
- Simple and queryable.
- The name was changed to avoid a taboo (璁 was a homophone of 熜 in the emperor's personal name 厚熜), and the emperor bestowed the name 孚敬. Expressing "when and why the name changed" would require an additional event and an extension; this is left as future work.

**Known limitation**
The model cannot answer "by what name was he called in documents of a given year".

---

## D7 Factoid layer → option C, plus source attribution for everything

**Decision**
1. **Every** event receives a source: `source document P70 documents event` (e.g. `juan 149 P70 documents mention-in-office`).
2. Only **disputed** claims are wrapped in an E13 Attribute Assignment: P140 / P177 / P141 express the claim, P16 used specific object points to the source, P14 carried out by points to the interpreter. First batch:
   - the start date of Huagaidian Daxueshi (biography / table of grand secretaries / *Shilu*: three sources)
   - the start year of Taizi taibao 太子太保 in SL15
   - the start year of Minister of Personnel in CBDB 130150 (CBDB 1533 vs *Shilu* juan 89, 1528)
   - Grand Mentor (太傅) as former title in juan 136 vs Junior Mentor in juan 89. Basis: juan 132 "少傅兼太子太傅", juan 141 "少傅兼太子太师", and the Treatise on Officials, "文臣无生加三公者" (no civil official received one of the Three Dukes in his lifetime). (Added 2026-10-24)
3. Adjudication of disputes is left to CRMinf (I1 Argumentation), to be done once the skeleton is complete.

**Rationale**
- RQ2 concerns divergence between sources; concentrating E13 on disputed points matches the focus of the research.
- P70 ensures that every piece of information has a source, avoiding "no dispute, no source", in keeping with the factoid model.
- Wrapping every triple in an E13 would multiply the data for the three persons several times over, mostly without analytical value.

---

## Questions awaiting historical confirmation

| # | Question | Current basis | Current treatment |
|---|---|---|---|
| Q1 | Was Zhang Cong actually in charge of the Ministry of Personnel after 1528? | Juan 89 says only "promoted to Minister of Personnel", not that he was in charge of the ministry | Treated as a concurrent title, noted "in charge of the ministry: unknown". Resolved (2026-11-08): not in charge of the ministry; see D1, "Check of 2026-11-08" |
| Q2 | Were all titles retained after retirement? | Juan 149 still lists the full titles at retirement | Titles are not withdrawn on retirement |
| Q3 | Did promotion between hall titles imply a change of function? | Juan 89 uses "promote" (升) | Treated as a conferral event, not as a new entry into the Grand Secretariat |
| Q4 | The exact dates of Zhang Cong's retirements and recalls | Not yet checked juan by juan | To be checked. Resolved (2026-11-08, within the scope of SL12): the 1531 retirement / summons / arrival in the capital are in *Shilu* juan 128, 132, 136 and are written into block ⑩ of SL12_event.ttl (the arrival in block ⑨); the 1529 dismissal and summons are in *Mingshi* juan 110, to the month only, and are not modelled. |
| Q5 | The exact date of conferral of Huagaidian Daxueshi | After 1528-06 and before 1533-04 | Expressed as an interval; E13 records the divergence among three sources |
| Q6 | Should Zhang Cong's reinstatement in Jiajing 12 be dated to the decree of the first month or to the arrival in the capital in the fourth month? | Table of grand secretaries, Jiajing 12: "正月召復任。四月赴召至京" (summoned back to office in the first month; arrived in the capital in the fourth); *Shizong shilu*, juan 149, Jiajing 12, fourth month, *yihai*: "赴台（疑为召）至京" ("went to the *tai* [probably an error for 召, summons] and arrived in the capital") | The E85 for "recall and reinstatement" is not created for now; only the E7 "answered the summons and arrived in the capital" of the fourth month (block ⑦ of SL12_event.ttl). 2026-10-24: resolved within the scope of SL12 (see the D5 supplement): the recall of Jiajing 11 is an E85 with a range expressed by P82a/b (block ⑩); the reinstatement of Jiajing 12 is outside the scope of SL12 |
| Q7 | Does promotion within the same series always replace the earlier title? | The sources say nothing explicit; juan 136, "余官如故" (other offices as before), does not say which earlier titles were replaced (approved by the author, 2026-10-24) | Inferred as replacement under D12, without adding triples (modeller's judgement) (approved by the author, 2026-10-24) |

These questions are to be put to specialists in Ming history. Wherever the thesis relies on one of these judgements, it is marked "modeller's judgement, awaiting historical confirmation".

---

## D8 URI scheme → based on GitHub Pages, vocabulary and instances kept apart, instances segmented by entity type

> Decision: Yang (2026-10-12); drafting: AI agent (Claude Code).
> Approved by the author (2026-11-08); both the decision and the rationale are confirmed.

**Decision**
- Base address: `https://kikayang.github.io/ming-prosopography-crm/`, matching the name of the GitHub repository.
- The extension vocabulary (project-defined properties and classes) is under `/vocab/`, prefix `mpv:`; e.g. `mpv:conferred_title` from D2.
- Instances are under `/id/`, segmented by entity type, with one prefix per segment:
  | Prefix | Path | Used for | CRM class |
  |---|---|---|---|
  | `person:` | `/id/person/` | persons | E21 |
  | `name:` | `/id/name/` | names | E41 |
  | `doc:` | `/id/doc/` | source documents (e.g. a juan of the *Shilu*) | E31 |
  | `event:` | `/id/event/` | events and activities | E5 / E7 and subclasses |
  | `ts:` | `/id/ts/` | time-spans | E52 |
  | `group:` | `/id/group/` | institutions and groups (Grand Secretariat, Ministry of Personnel) | E74 |
  | `type:` | `/id/type/` | types and title vocabulary | E55 |
  | `pc:` | `/id/pc/` | PC property-class nodes (PC14, PC144, etc.) | subclasses of PC0 |
  | `work:` | `/id/work/` | works and schemes (e.g. the book compiled, editorial principles) | E29 / E73 |
  | `place:` | `/id/place/` | places (e.g. the province of a standing assignment) | E53 |
- All Turtle files copy their prefixes from `docs/modelling/prefixes.ttl`; CIDOC-CRM uses the official namespace `crm:`.
- Check (c) of `scripts/check_crm.py` treats `mpv:` as the extension namespace by default.

**Rationale**
- **Resolvable, free, stable**: GitHub Pages addresses use HTTPS and require no domain purchase. Vocabulary documentation can later be published at this address so that the URIs resolve, in line with Linked Data principles.
- **Vocabulary and instances kept apart**: `/vocab/` holds the schema-level extensions (the part the thesis argues for under RQ1) and `/id/` holds the data. Keeping them apart makes it immediately clear which terms are new in this project. This is also common practice, e.g. in Linked Art and Cool URIs.
- **Instances segmented by type**: entities of different types cannot collide (e.g. `type:shaofu` and an event of the same name under `event:`). IDs can also be allocated by type when RDF is generated in bulk.
- **Valid Turtle**: with one prefix per segment, `ts:jj12-04-yihai` is a valid prefixed name. The earlier `ex:ts/jj12-04-yihai` is a syntax error in Turtle that neither rdflib nor Jena can parse.
- **Person IDs reuse the CBDB personid** (e.g. `person:68266`): stable, and linkable back to CBDB directly.

**Risks and open points**
- The URIs depend on the GitHub user name and repository name. A rename or move would break all URIs. If needed, a persistent redirection service such as w3id.org could be used instead (future work).
- GitHub Pages is not yet configured, so these URIs do **not resolve** for now.
- Rules for local names are not yet written down, e.g. the abbreviation of reign-period dates (`jj` = Jiajing), the spelling of pinyin, and how to name persons without a CBDB ID (`person:shizong`).
- Titles and event types are both under `type:`; whether this needs further segmentation (e.g. `/id/type/title/`) will be decided once the vocabulary has grown.

Supplement (approved by the author, 2026-10-30): a new prefix `work:` for works and schemes (E29, E73), e.g. the editorial principles and the *Siyi chengdian* 祀儀成典 in SL11. `doc:` remains reserved for source documents (E31).

Supplement (approved by the author, 2026-10-30): where pinyin could be misread as an English word, syllables are separated by a hyphen (e.g. group:li-ke).

Supplement (approved by the author, 2026-11-02): a new prefix `place:` (`/id/place/`) for places (E53), e.g. Zhejiang as the location of the standing assignment in D25.

---

## D9 Script and language tags (approved by the author, 2026-10-16)

Source text (personal names, book titles, office titles, titles, quotations) is in traditional characters, tagged @zh-Hant; vocabulary defined by the modeller (type names, etc.) is in simplified characters, tagged @zh-Hans, with an additional @en label. Labels must match the actual characters; typical errors of simplified–traditional conversion must be avoided (the cyclical character 丑 is not 醜).

In type names, the part taken from the source is tagged @zh-Hant; distinctions added by the modeller (such as "concurrent title of a grand secretary") are not written into the Chinese label, but into rdfs:comment (@zh-Hans) and the @en label. Every E55 type must have an @en label. (approved by the author, 2026-10-16)

This rule applies only to types defined in the project namespaces (type:, etc.); terms belonging to CIDOC-CRM (such as crm:P4_has_time-span, declared as E55 under D10) keep the official CRM labels and receive no additional ones. (approved by the author, 2026-10-16)

English names follow Hucker 1985, with the entry number noted; titles not in Hucker are given in pinyin, noted in the comment (at present Jinshendian and Huagaidian Daxueshi). (approved by the author, 2026-10-24)

Supplement (2026-11-10): every instance node (except name nodes) also carries an @en label. Name nodes hold original title strings and dates and are labelled only in @zh-Hant.

Supplement (2026-11-12): office titles not in Hucker are translated into English; the basis, or "contextual translation", is given in the glossary. Hall names stay in pinyin. Type nodes also carry an rdfs:comment @en explanation, written for readers unfamiliar with Ming institutions. name:date-cbdb-421880 is a CBDB field value and carries no language tag; it is the only exception.

---

## D10 The object type of P177 (approved by the author, 2026-10-16)

The text of CRM 7.1.3 allows properties to be instances of E55, but in the RDFS encoding a property is only an rdf:Property, which does not match the range E55 of P177. This project explicitly declares, in the data, that each referenced property is also an E55_Type. (approved by the author, 2026-10-16)

---

## D11 Order of the information-unit list and the modelling (approved by the author, 2026-10-24)

- The information-unit list for SL12 (juan 89/136/149) was drawn up only after SL12_event.ttl had been modelled; this is stated openly in the evaluation. SL12 serves as a trial run of the method.
- From SL11 and SL14 onwards the order is strict: first list the information units, then model, then evaluate.
- The evaluation rules are frozen before the extended sample begins; after freezing, the model is not revised in response to evaluation results. For SL12, both versions (v1 and v2) are reported in the thesis, with the changes classified as omission or limit.

---

## D12 Promotion within a series: the new title replaces the old (approved by the author, 2026-10-24)

- **Decision**: within the same broader class (Three Solitaries, Three Preceptors of the Heir Apparent, three junior preceptors of the Heir Apparent 東宮三少, ministerial titles, hall titles), a title conferred later replaces one conferred earlier. Queries of the form "which titles did he hold at a given time" infer this by rule, without adding triples. Retirement does not trigger replacement (D5).
- **Basis**: the division into series and the ranks are in *Mingshi*, juan 72, Treatise on Officials 1 (Three Dukes and Three Solitaries; three preceptors and three junior preceptors of the Heir Apparent). The replacement rule itself is not stated in the sources and is the modeller's judgement; see Q7.
- **Effect on the evaluation**: J089-U23 and J136-U16 can be judged kept_judgement in v2.

---

## D13 Conferral split into sub-events (approved by the author, 2026-10-24)

- One decree is one parent event (E7); each title conferred is a sub-event, linked with `crm:P9_consists_of`. A sub-event carries only `P2_has_type` (the action: add / promote / advance, type:action-*) and `mpv:conferred_title`; the emperor, the recipient, the time and the source are taken from the parent event. A sub-event receives its own P70 only when its source differs from that of the parent.
- **Rationale**: a single property cannot carry a qualifier such as the "action". CRM solves the analogous problem for P144 with an intermediate node of a PC class; this project instead uses CRM's existing P9, adds no class, and keeps conferred_title as its only extension property.
- Block ⑥ (entry into the Grand Secretariat) is not split for now: the table of grand secretaries uses no verb there.

---

## D14 Conversion to the Western calendar (approved by the author, 2026-10-24)

P82a/b use the Gregorian calendar; the comment notes the Julian date and the sexagenary day. (approved by the author, 2026-10-24)

Detailed rules (set by: Yang, 2026-10-24): precision to the day; where only year and month are given, the whole month is used; each conversion is checked against the Academia Sinica "Two Thousand Years of Chinese–Western Calendar Conversion".

Where only the year is given (e.g. "Jiajing 13" in the biography, or 1532 in CBDB, i.e. Jiajing 11), the whole lunar year is used, including any intercalary month. (approved by the author, 2026-10-24)

Supplement (drafted by AI agent (Claude Code); approved by the author, 2026-11-08): by the XSD specification, xsd:dateTime is the proleptic Gregorian calendar.

---

## D15 Rules for the state version (approved by the author, 2026-10-26)

- The state version describes only "what he was"; it creates no events for conferral, entry into or departure from the Grand Secretariat.
- Rule 1: only one extension property is allowed, `mpv:holds_title` (E21 Person → E55 Type), for the same reason as conferred_title in the event version: the Three Solitaries and the Three Preceptors of the Heir Apparent have no institution, so P107 cannot be used.
- Rule 2: no extension for expressing time. Neither PC107 nor a property is an E2 Temporal Entity, so CRM does not allow P4 on them; giving a state a time requires either an extension or a switch to events, which is itself a finding for RQ1.
- Rule 3: E13 is used only for disputed claims, as in D7.
- Names (D6) and original title strings (D4) are expressed as in the event version.

---

## D16 Duty assignments as activity nodes (Draft; approved by the author, 2026-10-30)

- The undertaking an assignment serves is an E7 (e.g. compiling the *Siyi chengdian*, building the suburban altar); a person holding an assignment is a separate E7 node, with `P2_has_type` (type of assignment), `P14_carried_out_by` (holder), `P9i_forms_part_of` (undertaking it belongs to) and `P17_was_motivated_by` (the edict making the appointment).
- **Rationale**: an assignment is tied to a concrete undertaking and differs in nature from a title (D2, a marker of standing).
- PC14 + P14.1 is not used: the box cannot carry time or source, nor be linked to other nodes. This agrees with the conclusion of the three-way comparison for SL12.
- Titles use conferred_title (D2, D13) and assignments use activity nodes (D16); this is how the RQ1 distinction between substantive office and duty assignment appears in the model.
- Supplement (approved by the author, 2026-10-30): actions such as appointment and promotion are parts of the edict and are linked to it with P9 / P9i (as in D13); an assignment node is an ongoing tenure caused by the edict and points to it with P17.

---

## D17 A duty assignment held in the capacity of another (Draft; approved by the author, 2026-10-30)

- The new assignment node points to the earlier assignment node with `crm:P15_was_influenced_by`; the original form of address is kept as a separate E41.
- **Rationale**: CRM has no property for "in the capacity of", and P15 is semantically broad; no extension is added for now, the choice is tested in the evaluation, and the result serves as evidence for RQ1.
- Alternative: an extension property `mpv:in_capacity_of`. Whether to adopt it: see T2.

---

## D18 Compound assignment names (Draft; approved by the author, 2026-10-30)

- E.g. "知建造事、总督工程官" (Zhi jianzao shi, Zongdu gongcheng guan): one assignment node with two P2 types (rank: Zhi / Tongzhi jianzao shi; function: Zongdu gongcheng, Dushi guizhi, etc.).
- Basis: Li Shi's "同知建造事，督视规制官" (Tongzhi jianzao shi, Dushi guizhi guan) shows that the first part indicates rank and the second function.
- The original text has no punctuation; the enumeration comma was added by the modern edition, and the division is the modeller's judgement.
- Supplement (approved by the author, 2026-10-30): under the assignment type (`type:chaiqian`) there are two broader classes, "rank within a duty assignment" (`type:chaiqian-weici`) and "function of a duty assignment" (`type:chaiqian-zhize`); a name is split only when both parts occur, e.g. "監視巡察工程官" (Jianshi xuncha gongcheng guan) is not split and receives only a function type.

---

## D19 Being in charge of affairs (*zhangshi* 掌事) (Final; approved by the author, 2026-10-30)

- Where the source says explicitly that someone directs the affairs of an office ("掌部事", "掌科事"), a *zhangshi* node is created as in D16 (P2 `type:zhangshi`, P14 the person, P17 the edict making the appointment), and the office directed is linked with `crm:P11_had_participant` (E74).
- P16 is not used: the range of P16 is E70 Thing, which does not admit an E74 Group (E74 falls under E39 Actor). P11 is semantically broad ("participation" rather than "direction"), and the evaluation takes this into account. See T3.
- Retention of an existing post ("仍兼", still concurrently) is not created as an event.
- A formal post in a new institution (e.g. promotion to Academician Reader-in-waiting of the Hanlin Academy) uses E85 + PC144 as in D3.
- This entry makes uniform the rule in D1 that an event is created only for being in charge of a ministry.

---

## D20 Editorial principles and the book (Draft; approved by the author, 2026-10-30)

- The editorial principles (凡例條目) are an E29 Design or Procedure, to which the compilation activity points with `P33_used_specific_technique`; the principles are produced by the event of the emperor's pronouncement ("上谓") (E65 Creation, `P94_has_created`, P14 the Shizong emperor).
- The book being compiled is an E73, with its title "祀儀成典" attached by P102.

---

## D21 Scope of persons (Draft; approved by the author, 2026-10-30)

- For the three core persons (Zhang Cong, Xia Yan, Xu Jie), all offices and assignments recorded in the source are modelled; for other persons, only what bears directly on the modelling problems of the case (in SL11, their assignment nodes in this edict); the rest is judged not_modelled / scope in the evaluation.
- CBDB personids of the three core persons (from `data/deep_cases/factoids_3persons.csv` and `cbdb_postings_3persons.csv`, which agree): 張璁 Zhang Cong 68266, 夏言 Xia Yan 68194, 徐階 Xu Jie 68547.

---

## D22 Duty assignments in the state version (Draft; approved by the author, 2026-10-30)

- Assignments without an institution are treated like honorary titles, with `mpv:holds_title` (D15, rule 1).
- Option S2 (a "team" E74 for each undertaking, with P107 + PC107) is rejected. Reason: the event version already rejects treating temporary teams as institutions (D16); the two versions must keep the same modelling stance, differing only in "event versus state".
- Posts in standing institutions (Hanlin Academy, Office of Scrutiny for Personnel) use P107 + PC107.

---

## D23 Structure of an appointment (Draft; approved by the author, 2026-11-02)

- One promotion is one parent event (E7), with `P2_has_type` `type:action-sheng` and `P14_carried_out_by` the Shizong emperor; where the source gives no subject, the comment notes "implicit".
- The E85 into the new institution and the E86 from the old one are parts of the parent event, linked with `crm:P9_consists_of`.
- Any assignment node arising from it points to the parent event with `P17_was_motivated_by`.
- Consistent with D13 (sub-events with P9) and with the D16 supplement (actions with P9 / P9i, assignments with P17).

---

## D24 Implicit departure (Draft; approved by the author, 2026-11-02)

- Where the source says "promoted from A to B" without stating the departure, an E86 is created, with `P146_separated_from` the institution of A, and the comment notes "implicit".
- **Rationale**: without the departure, the model would imply that he held posts in two places at once.
- Checked (in the CIDOC-CRM 7.1.3 core and PC files in `ontologies/`): CRM defines .1 properties only for P107 and P144 (P107.1 and P144.1 kind of member, corresponding to PC107 and PC144); P146 separated from has no .1 property and there is no PC146. Hence **joining can record a capacity, leaving cannot**: an E86 can say which institution was left, but not in what capacity. The earlier capacity (e.g. Vice Prefect) could be expressed with an additional E85 + PC144 of unknown date, which this project has not adopted (judged omission in the evaluation); the capacity in which someone left cannot be expressed in CRM (no P146.1); see T4.

---

## D25 Standing duty assignments and their institutions (Draft; approved by the author, 2026-11-02)

- Supplement to D16: one-off assignments (compiling a book, building) point to their undertaking with `P9i_forms_part_of`; standing assignments (e.g. Supervisor of Education) do not invent an "undertaking", but use `crm:P7_took_place_at` for the place (E53, new prefix `place:`, see the D8 supplement) and `crm:P11_had_participant` for the institution they belong to (as in D19).
- **Basis**: *Mingshi*, juan 75, Treatise on Officials 4: "按察司副使、僉事分司諸道。提督學道，清軍道，驛傳道，十三布政司俱各一員" (the vice commissioners and assistant commissioners of the surveillance commissions divided among the circuits; each of the thirteen provinces had one Education Intendant Circuit (提督學道) [Hucker 1958, p. 54], one military-registration circuit and one post circuit); and "兩京不設布、按二司，故督學以御史" (the two metropolitan areas had no provincial administration or surveillance commissions, so education was supervised by censors) [page reference in the Zhonghua edition to be added]. Supervising education was a function that could be attached to different substantive offices (assistant commissioner, vice commissioner, censor), and is therefore modelled as a separate assignment node rather than merged into the substantive office.

---

## D26 Substantive office carrying a duty assignment (Draft; approved by the author, 2026-11-02)

- The E85 of the substantive office and the assignment node are linked through the same parent event (D23), and the assignment node is linked with P11 to the institution of the substantive office (D25). No further link is added.
- The expected judgement in the evaluation is kept_judgement.
- On the problem that substantive office and assignment take different forms and cannot be linked directly, see T1.

---

## Open questions (awaiting external advice)

Parallel to the "questions awaiting historical confirmation" (Q1–Q7): Q items are questions of historical fact, T items are questions of modelling and standards. (Compiled 2026-11-02)

| # | Source | Question | Current practice |
|---|---|---|---|
| T1 | D26 | The substantive office is expressed by joining / leaving events (E85 / E86) and the duty assignment by an office-holding node (D16); because the two take different forms, "substantive office carrying an assignment" cannot be linked directly. Should the substantive office also be modelled as an office-holding node (option 4B)? | Linked indirectly through the same parent event (D23), with no further link |
| T2 | D17 | Holding an assignment "in the capacity of" another: should the use of P15 be reported as a semantic gap in CRM, or should an extension property (`mpv:in_capacity_of`) be added and evaluated as a fourth variant? | P15 is used; no extension added |
| T3 | D19 | "Directing the affairs of an office" uses P11, whose meaning is broad ("participation" rather than "direction"). Treatment as for T2: report a semantic gap, or add an extension property and evaluate it as a variant? | P11 is used |
| T4 | D24 | CRM can express that someone once held a post (an additional E85 + PC144 of unknown date, with P144.1 giving the capacity), but not the capacity in which he left (P146 has no .1 property, and there is no PC146). Is this worth putting forward as a suggestion for CRM? (Narrowed 2026-11-03; approved by the author) | The earlier capacity is kept only in the original string (E41); the E85 + PC144 of unknown date is not created (judged omission for J161-U04 in the SL14 evaluation) |

### Review of 2026-11-09: T2–T4 and the CRM scope notes

- Basis: the scope notes of P11, P14, P15, P134, P144 and P146 in ontologies/CIDOC_CRM_v7.1.3.rdf.
- T4: the examples for P144 and P146 in CRM both model the office itself as an E74: the P144 example is Gorbachev joining
  "the office of Leader of the USSR", and the P146 example is Washington leaving "the office of President of the United States".
  Under this pattern, leaving the group that is the office expresses the capacity on departure, and no P146.1 is needed. T4 is restated as follows: the gap results from this project's convention (D3: institutions are E74,
  posts are given with P144.1) and is not a limitation of CRM itself; the cost is that every post requires its own group, which must in addition be linked to its institution.
- T3: the scope note of P11 states that it "does not imply any causal relationship"; it expresses participation only, with no sense of direction;
  the scope note of P14, by contrast, states that it "implies causal or legal responsibility". Directing affairs requires precisely the latter.
  (Note: the qualification in P11 that groups can "physically" participate only through individuals concerns physical presence; it does not apply here and is not used as an argument.)
  Alternative pattern: the institution's business is modelled as an E7 carried out by the institution (P14 the institution), the activity of directing its affairs is P9i part of it, and P14.1 marks the role.
  T3 is restated as a choice of pattern.
- T2: the scope note of P14 states that P14.1 specifies the nature of the participation. The type of capacity in "in the capacity of a construction official" can be expressed with PC14 + P14.1;
  pointing to a specific assignment node requires a sub-property of P15 (P17 or P134), which is more specific than P15. T2 is restated as partly expressible.
- Treatment: the frozen evaluations are not re-judged. This review is reported in the discussion of the thesis and in the v3 report;
  the earlier conclusion that "the gap in CRM is semantic" is changed to "the distinctions can be expressed, but depend on the pattern chosen, each with its own costs".
