# Identifiers and labels

This note describes how identifiers are formed in the models (`docs/modelling/*.ttl`) and lists every labelled identifier with its Chinese and English labels. The rules summarise decisions D8 and D9 of the modelling decision log; the table at the end is generated from the labels by `scripts/naming_table.py`.

## Base addresses and prefixes

Base address: `https://kikayang.github.io/ming-prosopography-crm/`. The extension vocabulary is under `/vocab/` (prefix `mpv:`); instances are under `/id/`, one segment and one prefix per entity type. All Turtle files copy their prefixes from `docs/modelling/prefixes.ttl`.

| Prefix | Path | Used for | CRM class |
|---|---|---|---|
| `mpv:` | `/vocab/` | extension properties (`mpv:conferred_title`, `mpv:holds_title`) | — |
| `person:` | `/id/person/` | persons | E21 |
| `name:` | `/id/name/` | names, original title strings, original date expressions | E41, E35 |
| `doc:` | `/id/doc/` | source documents | E31 |
| `event:` | `/id/event/` | events, activities, attribute assignments | E5, E7 and subclasses, E13 |
| `ts:` | `/id/ts/` | time-spans | E52 |
| `group:` | `/id/group/` | institutions and groups | E74 |
| `type:` | `/id/type/` | types: titles, actions, categories | E55 |
| `pc:` | `/id/pc/` | nodes for properties of properties (PC107, PC144) | PC classes |
| `work:` | `/id/work/` | works and schemes (a book being compiled, editorial principles) | E29, E73 |
| `place:` | `/id/place/` | places | E53 |

## Local names

**Spelling.** Local names are lower case, in pinyin without tone marks, with words separated by hyphens. Where a pinyin word could be misread as an English word, its syllables are separated by a hyphen as well (`group:li-ke`, not `like`). In a few event identifiers a personal name is written as one word (`event:jj09-10-xiayan-sheng`); elsewhere surname and given name are separated (`name:zhang-cong`).

**Persons.** Persons recorded in CBDB take their CBDB personid (`person:68266` for Zhang Cong). Persons without a CBDB identifier take a pinyin name (`person:ming-shizong`); `person:yang` is the modeller, recorded as the interpreter in E13 assignments.

**Dates.** Dates follow the Chinese reign calendar:
- `jj` is the reign period Jiajing 嘉靖, followed by the reign year in two digits: `jj13` is Jiajing 13;
- the lunar month follows in two digits: `jj13-03` is the third month;
- the day is given by its sexagenary name in pinyin (`jj13-03-jimao`), or `01` for the first day of the month (`jj07-06-01`);
- a range is written `<from>-to-<to>` (`jj10-11-to-jj11-03`);
- an undated "earlier" (初) in the source is `chuyu` (`jj09-chuyu`);
- a time-span taken from a CBDB record is named after the record (`ts:cbdb-421880`).

The same date part is used for the time-span (`ts:`) and for the name node holding the original date expression (`name:date-…`). Western dates are given only in P82a/P82b, in the proleptic Gregorian calendar (D14).

**Events.**
- Datable events: `<date>-<action>`, with a person added where needed to distinguish events of the same day (`event:jj09-10-xiayan-sheng`). Sub-events of one decree (D13) or of one promotion (D23) add `-1`, `-2`, … (`event:jj07-06-jiaen-1`).
- Undertakings, and events without a modelled date, are named by their content (`event:jiaotan-jianzao`, `event:siyi-chengdian-xiushu`, `event:huagaidian-conferral`).
- Duty assignments (D16): `chaiqian-<personid>-<assignment>` (`event:chaiqian-68266-zongcai`).
- Being in charge of an office's affairs (D19): `zhangshi-<personid>-<institution>` (`event:zhangshi-68194-li-ke`).
- Attribute assignments recording a disputed claim (D7): `<topic>-claim-<source>` (`event:huagaidian-claim-shilu-136`).

**Action words.** Event identifiers use pinyin for the action:

| Word | Chinese | Meaning |
|---|---|---|
| `ruge` | 入閣 | entry into the Grand Secretariat |
| `jiaen` | 加恩 | bestowal of honours |
| `sheng` | 升 | promotion |
| `zhishi` | 致仕 | retirement |
| `zhao` | 召 | summons |
| `zhaohuan` | 召還 | recall to office |
| `zhijing`, `fuzhao` | 至京, 赴召 | arrival in the capital, answering a summons |
| `chi` | 敕 | edict |
| `chuyu`, `shangwei` | 初諭, 上謂 | the emperor's earlier instruction, the emperor's pronouncement |
| `shouzha`, `tongshi` | 手扎, 同視 | handwritten note, joint inspection |
| `yiding-tili`, `shouchang` | 議定體例, 首倡 | settling the format, first proposal |
| `jianzao`, `xiushu` | 建造, 修書 | construction, compilation |

The actions of title conferral are also types (D13): `type:action-jia` (加, add), `type:action-sheng` (升, promote), `type:action-jin` (進, advance).

**Types.** Office titles take the pinyin of the title (`type:shaofu`, `type:jinshendian-daxueshi`, `type:anchasi-qianshi`). Ministerial titles held concurrently by grand secretaries end in `-xian` (concurrent rank title) and name the ministry in English (`type:shangshu-personnel-xian`, `type:shangshu-rites-xian`). Categories are named in pinyin (`type:sangu`, `type:dian-ge-xian`, `type:chaiqian-zhize`).

**Property-of-property nodes.** A PC144 node attached to a joining event is `<event>-<group>` (`pc:jj06-10-ruge-neige`); a PC107 node of the state version is `<group>-member-<personid>` (`pc:neige-member-68266`).

**Names.** Personal names are written `<surname>-<given name>` (`name:zhang-cong`). Original title strings are `guanxian-<date>-<person>`, with `-yuan` (former) or `-xin` (new) where one entry gives both (`name:guanxian-jj13-03-jimao-xu-jie-yuan`). Original date expressions are `date-<date>`; titles of works are `title-<work>`.

**Documents.** Juan of the *Shizong shilu* are `doc:shizong-shilu-<juan>`, with the juan number in three digits (`doc:shizong-shilu-089`); juan of the *Mingshi* are `doc:mingshi-<juan>`; a CBDB record cited as a source is `doc:cbdb-<posting_id>`.

## Labels

Source text (personal names, book titles, office titles, quotations) is labelled in traditional characters (`@zh-Hant`); vocabulary defined by the modeller is labelled in simplified characters (`@zh-Hans`). Every E55 type and every instance node except name nodes carries an English label (`@en`); name nodes hold original title strings and date expressions and are labelled only in `@zh-Hant` (D9). English office titles follow Hucker (1985); titles not in Hucker are given in pinyin with an English gloss.

The English label of `type:shangshu-personnel-xian` ("… concurrent nominal title held by a Grand Secretary") is a known defect recorded under competency question CQ1 and is to be revised in v3; `type:shangshu-rites-xian` and `type:pinjie-jianxian` use the same wording. Elsewhere this kind of title is called a concurrent rank title.

## Table

<!-- BEGIN TABLE (generated by scripts/naming_table.py) -->

| identifier | Chinese | English |
|---|---|---|
| `person:127536` | 汪鋐 | Wang Hong |
| `person:130180` | 郭勛 | Guo Xun |
| `person:130490` | 張袞 | Zhang Gun |
| `person:131629` | 程文德 | Cheng Wende |
| `person:132101` | 廖道南 | Liao Daonan |
| `person:68136` | 翟鑾 | Zhai Luan |
| `person:68140` | 李時 | Li Shi |
| `person:68194` | 夏言 | Xia Yan |
| `person:68266` | 張璁 | Zhang Cong (Zhang Fujing) |
| `person:68285` | 桂萼 | Gui E |
| `person:68547` | 徐階 | Xu Jie |
| `person:ming-shizong` | 明世宗 / 朱厚熜 | Jiajing Emperor (Ming Shizong, Zhu Houcong) |
| `person:yang` | — | Yang Tianchi (modeller) |
| `group:hanlinyuan` | 翰林院 | Hanlin Academy |
| `group:huangzhou-fu` | 湖廣黃州府 | Huangzhou Prefecture, Huguang |
| `group:li-ke` | 吏科 | Office of Scrutiny for Personnel |
| `group:neige` | 內閣 | Grand Secretariat |
| `group:zhejiang-anchasi` | 浙江按察司 | Zhejiang Provincial Surveillance Commission |
| `place:zhejiang` | 浙江 | Zhejiang |
| `doc:cbdb-421880` | — | CBDB POSTED_TO_OFFICE_DATA, posting_id 421880 |
| `doc:mingshi-110` | 明史 卷110 宰輔年表二 | Mingshi, juan 110 (Table of Grand Secretaries, part 2) |
| `doc:mingshi-196` | 明史 卷196 列傳第八十四 | Mingshi, juan 196 (biography of Zhang Cong) |
| `doc:shizong-shilu` | 世宗實錄 | Ming Shizong shilu |
| `doc:shizong-shilu-089` | 世宗實錄 卷089 | Ming Shizong shilu, juan 89 |
| `doc:shizong-shilu-118` | 世宗實錄 卷118 | Ming Shizong shilu, juan 118 |
| `doc:shizong-shilu-128` | 世宗實錄 卷128 | Ming Shizong shilu, juan 128 |
| `doc:shizong-shilu-132` | 世宗實錄 卷132 | Ming Shizong shilu, juan 132 |
| `doc:shizong-shilu-135` | 世宗實錄 卷135 | Ming Shizong shilu, juan 135 |
| `doc:shizong-shilu-136` | 世宗實錄 卷136 | Ming Shizong shilu, juan 136 |
| `doc:shizong-shilu-141` | 世宗實錄 卷141 | Ming Shizong shilu, juan 141 |
| `doc:shizong-shilu-146` | 世宗實錄 卷146 | Ming Shizong shilu, juan 146 |
| `doc:shizong-shilu-149` | 世宗實錄 卷149 | Ming Shizong shilu, juan 149 |
| `doc:shizong-shilu-161` | 世宗實錄 卷161 | Ming Shizong shilu, juan 161 |
| `work:siyi-chengdian` | 祀儀成典 | Siyi chengdian (compilation on the reformed state sacrifices, commissioned 1530) |
| `work:siyi-chengdian-fanli` | 祀儀成典凡例條目 | Editorial principles of the Siyi chengdian |
| `event:chaiqian-127536-gongcheng` | 監視巡察工程官（汪鋐） | Duty assignment of Wang Hong as Jianshi xuncha gongcheng guan (inspector of the works) |
| `event:chaiqian-127536-jianxiu` | 監修官（汪鋐） | Duty assignment of Wang Hong as Jianxiu guan (supervisor) for the Siyi chengdian (1530) |
| `event:chaiqian-130180-gongcheng` | 知建造事總督工程官（郭勛） | Duty assignment of Guo Xun as Zhi jianzao shi and Zongdu gongcheng guan (in charge of construction; general supervisor of the works) |
| `event:chaiqian-130180-jianxiu` | 監修官（郭勛） | Duty assignment of Guo Xun as Jianxiu guan (supervisor) for the Siyi chengdian (1530) |
| `event:chaiqian-130490-zuanxiu` | 纂修官（張袞） | Duty assignment of Zhang Gun as Compiler of the Siyi chengdian (1530) |
| `event:chaiqian-131629-zuanxiu` | 纂修官（程文德） | Duty assignment of Cheng Wende as Compiler of the Siyi chengdian (1530) |
| `event:chaiqian-132101-zuanxiu` | 纂修官（廖道南） | Duty assignment of Liao Daonan as Compiler of the Siyi chengdian (1530) |
| `event:chaiqian-68136-fuzongcai` | 副總裁官（翟鑾） | Duty assignment of Zhai Luan as Fu zongcai guan (deputy director-general) of the Siyi chengdian (1530) |
| `event:chaiqian-68140-gongcheng` | 同知建造事，督視規制官（李時） | Duty assignment of Li Shi as Tongzhi jianzao shi and Dushi guizhi guan (associate in charge of construction; supervisor of the building design) |
| `event:chaiqian-68140-jianxiu` | 監修官（李時） | Duty assignment of Li Shi as Jianxiu guan (supervisor) for the Siyi chengdian (1530) |
| `event:chaiqian-68194-gongcheng` | 監視巡察工程官（夏言） | Duty assignment of Xia Yan as Jianshi xuncha gongcheng guan (inspector of the works) |
| `event:chaiqian-68266-gongcheng` | 知建造事、總督工程官（張璁） | Duty assignment of Zhang Cong as Zhi jianzao shi and Zongdu gongcheng guan (in charge of construction; general supervisor of the works) |
| `event:chaiqian-68266-zongcai` | 總裁官（張璁） | Duty assignment of Zhang Cong as Zongcai guan (director-general) of the Siyi chengdian (1530) |
| `event:chaiqian-68285-fuzongcai` | 副總裁官（桂萼） | Duty assignment of Gui E as Fu zongcai guan (deputy director-general) of the Siyi chengdian (1530) |
| `event:chaiqian-68547-tidiao-xuexiao` | 提調學校（徐階） | Duty assignment of Xu Jie as Supervisor of Education in Zhejiang (1534) |
| `event:chaiqian-68547-zuanxiu` | 纂修官（徐階） | Duty assignment of Xu Jie as Compiler of the Siyi chengdian (1530) |
| `event:huagaidian-claim-cbdb-421880` | 华盖殿授衔时间：CBDB posting 421880 | Date of the Huagaidian conferral according to CBDB posting 421880 |
| `event:huagaidian-claim-mingshi-110` | 华盖殿授衔时间：明史卷110宰辅年表 | Date of the Huagaidian conferral according to Mingshi, juan 110 |
| `event:huagaidian-claim-mingshi-196` | 华盖殿授衔时间：明史卷196列传 | Date of the Huagaidian conferral according to Mingshi, juan 196 |
| `event:huagaidian-claim-shilu-136` | 华盖殿授衔时间：世宗实录卷136 | Date of the Huagaidian conferral according to Ming Shizong shilu, juan 136 |
| `event:huagaidian-conferral` | 張孚敬進兼太子太師、華蓋殿大學士 | Advancement of Zhang Fujing to Grand Preceptor of the Heir Apparent and Huagaidian Daxueshi (Grand Secretary of the Huagai Hall; date disputed) |
| `event:huagaidian-conferral-1` | 進兼太子太師 | Advancement of Zhang Fujing to Grand Preceptor of the Heir Apparent (date disputed) |
| `event:huagaidian-conferral-2` | 華蓋殿大學士 | Advancement of Zhang Fujing to Huagaidian Daxueshi (Grand Secretary of the Huagai Hall; date disputed) |
| `event:jiaotan-jianzao` | 郊坛建造 | Construction of the suburban altar |
| `event:jiaozhi-gengding` | 更定郊制 | Revision of the rules for the suburban sacrifices |
| `event:jj06-10-ruge` | 張璁入閣 | Entry of Zhang Cong into the Grand Secretariat (1527) |
| `event:jj07-06-jiaen` | 嘉靖七年六月加恩纂述諸臣（張璁） | Bestowal of honours on Zhang Cong for the compilation of the Minglun dadian (official compilation on the Great Rites Controversy, presented 1528) |
| `event:jj07-06-jiaen-1` | 加少傅 | Addition of Junior Mentor to Zhang Cong (1528) |
| `event:jj07-06-jiaen-2` | 加太子太傅 | Addition of Grand Mentor of the Heir Apparent to Zhang Cong (1528) |
| `event:jj07-06-jiaen-3` | 升吏部尚書 | Promotion of Zhang Cong to Minister of Personnel (1528) |
| `event:jj07-06-jiaen-4` | 升謹身殿大學士 | Promotion of Zhang Cong to Jinshendian Daxueshi (Grand Secretary of the Jinshen Hall; 1528) |
| `event:jj09-10-guiyou-shouzha` | 復出手扎示璁 | Handwritten note of the Jiajing Emperor shown to Zhang Cong (1530) |
| `event:jj09-10-guiyou-tongshi` | 仍召輔臣璁同視 | Summons of Zhang Cong to inspect together with the Jiajing Emperor (1530) |
| `event:jj09-10-xiayan-sheng` | 升翰林院侍讀學士（夏言） | Promotion of Xia Yan to Academician Reader-in-waiting of the Hanlin Academy (1530) |
| `event:jj09-10-xinwei-chi` | 降敕 | Edict of the Jiajing Emperor on the compilation of the Siyi chengdian (1530) |
| `event:jj09-chuyu` | 諭……命（張璁與李時議定體例） | Instruction of the Jiajing Emperor to Zhang Cong and Li Shi to settle the format of the book (1530) |
| `event:jj09-shangwei` | 上謂（凡例條目） | Pronouncement of the Jiajing Emperor on the editorial principles (1530) |
| `event:jj09-xiayan-shouchang` | 首倡正議 | First proposal of the correct ritual by Xia Yan |
| `event:jj09-yiding-tili` | 議定體例 | Settling of the format of the book by Zhang Cong and Li Shi |
| `event:jj10-07-zhishi` | 張孚敬致仕（嘉靖十年） | Retirement of Zhang Fujing from the Grand Secretariat (1531) |
| `event:jj10-11-zhao` | 遣行人周文燭齎敕召張孚敬復任辦事 | Summons of Zhang Fujing back to office, delivered by the Messenger Zhou Wenzhu (1532) |
| `event:jj10-11-zhaohuan` | 張孚敬召還入閣 | Recall of Zhang Fujing to the Grand Secretariat (1532) |
| `event:jj11-03-zhijing` | 張孚敬應召至京 | Arrival of Zhang Fujing in the capital in answer to the summons (1532) |
| `event:jj11-08-zhishi` | 張孚敬致仕 | Retirement of Zhang Fujing from the Grand Secretariat (1532) |
| `event:jj12-01-zhao` | 遣鴻臚寺左少卿陳璋召張孚敬復任 | Summons of Zhang Fujing back to office, delivered by Chen Zhang, Left Vice Minister of the Court of State Ceremonial (1533) |
| `event:jj12-04-fuzhao` | 張孚敬赴召至京 | Arrival of Zhang Fujing in the capital in answer to the summons (1533) |
| `event:jj13-03-jimao-sheng` | 升湖廣黃州府同知徐階為浙江按察司僉事，提調學校 | Promotion of Xu Jie from Vice Prefect of Huangzhou to Assistant Surveillance Commissioner of Zhejiang and Supervisor of Education (1534) |
| `event:jj13-03-jimao-sheng-1` | — | Joining of the Zhejiang Provincial Surveillance Commission by Xu Jie (1534) |
| `event:jj13-03-jimao-sheng-2` | — | Leaving of Huangzhou Prefecture by Xu Jie (implicit, 1534) |
| `event:minglun-dadian-jincheng` | 明倫大典書成進呈 | Completion and presentation of the Minglun dadian (official compilation on the Great Rites Controversy, presented 1528) |
| `event:siyi-chengdian-xiushu` | 纂辑祀仪成典 | Compilation of the Siyi chengdian |
| `event:taifu-claim-shilu-132` | 张孚敬原任头衔：世宗实录卷132 作少傅 | Former title of Zhang Fujing according to Ming Shizong shilu, juan 132 (Junior Mentor) |
| `event:taifu-claim-shilu-136` | 张孚敬原任头衔：世宗实录卷136 作太傅 | Former title of Zhang Fujing according to Ming Shizong shilu, juan 136 (Grand Mentor) |
| `event:zhangshi-68194-li-ke` | 掌吏科事（夏言） | Xia Yan in charge of the affairs of the Office of Scrutiny for Personnel (1530) |
| `pc:hanlinyuan-member-68194` | — | Membership of Xia Yan in the Hanlin Academy as Academician Reader-in-waiting |
| `pc:huangzhou-fu-member-68547` | — | Membership of Xu Jie in Huangzhou Prefecture, Huguang, as Vice Prefect |
| `pc:jj06-10-ruge-neige` | — | Membership of Zhang Cong in the Grand Secretariat as Grand Secretary |
| `pc:jj09-10-xiayan-hanlin` | — | Membership of Xia Yan in the Hanlin Academy as Academician Reader-in-waiting |
| `pc:jj10-zhaohuan-neige` | — | Membership of Zhang Fujing in the Grand Secretariat as Grand Secretary |
| `pc:jj13-03-jimao-sheng-1-anchasi` | — | Membership of Xu Jie in the Zhejiang Provincial Surveillance Commission as Assistant Surveillance Commissioner |
| `pc:li-ke-member-68194` | — | Membership of Xia Yan in the Office of Scrutiny for Personnel as Chief Supervising Secretary |
| `pc:neige-member-68266` | — | Membership of Zhang Cong in the Grand Secretariat as Grand Secretary |
| `pc:zhejiang-anchasi-member-68547` | — | Membership of Xu Jie in the Zhejiang Provincial Surveillance Commission as Assistant Surveillance Commissioner |
| `name:date-cbdb-421880` | — | — |
| `name:date-jj06-10` | 嘉靖六年十月 | — |
| `name:date-jj07-06-01` | 嘉靖七年六月辛丑朔 | — |
| `name:date-jj09-10-guiyou` | 嘉靖九年十月癸酉 | — |
| `name:date-jj09-10-xinwei` | 嘉靖九年十月辛未 | — |
| `name:date-jj09-chuyu` | 初 | — |
| `name:date-jj10-07-wuwu` | 嘉靖十年七月戊午 | — |
| `name:date-jj10-11-dingchou` | 嘉靖十年十一月丁丑 | — |
| `name:date-jj11-03` | 嘉靖十一年三月 | — |
| `name:date-jj11-03-jiayin` | 嘉靖十一年三月甲寅 | — |
| `name:date-jj11-08-xinchou` | 嘉靖十一年八月辛丑 | — |
| `name:date-jj12-01-bingchen` | 嘉靖十二年正月丙辰 | — |
| `name:date-jj12-04-yihai` | 嘉靖十二年四月乙亥 | — |
| `name:date-jj13` | 嘉靖十三年 | — |
| `name:date-jj13-03-jimao` | 嘉靖十三年三月己卯 | — |
| `name:guanxian-jj07-06-zhang-cong` | 少保、禮部尚書兼文淵閣大學士張璁 | — |
| `name:guanxian-jj09-10-guiyou-zhang-cong` | 輔臣璁 | — |
| `name:guanxian-jj09-10-renxu-zhang-cong` | 少傅兼太子太傅、吏部尚書張璁 | — |
| `name:guanxian-jj09-10-xinwei-gui-zhai` | 內閣輔臣大學士卿萼、卿鸞 | — |
| `name:guanxian-jj09-10-xinwei-guo-xun` | 知建造事總督工程官卿勛 | — |
| `name:guanxian-jj09-10-xinwei-li-shi` | 同知建造事，督視規制官卿時 | — |
| `name:guanxian-jj09-10-xinwei-wang-hong` | 監視巡察工程官卿𬭎 | — |
| `name:guanxian-jj09-10-xinwei-xia-yan` | 監視巡察工程官吏科都給事中夏言 | — |
| `name:guanxian-jj09-10-xinwei-zhang-cong` | 知建造事、總督工程官卿璁 | — |
| `name:guanxian-jj09-10-xu-jie` | 編修徐階 | — |
| `name:guanxian-jj09-chuyu-zhang-cong` | 大學士 | — |
| `name:guanxian-jj10-11-zhang-fujing` | 致仕少傅兼太子太傅、吏部尚書、謹身殿大學士張孚敬 | — |
| `name:guanxian-jj11-03-zhang-fujing` | 原任太傅兼太子太傅、吏部尚書、謹身殿大學士張孚敬 | — |
| `name:guanxian-jj11-08-zhang-fujing` | 少傅兼太子太師、吏部尚書、華蓋殿大學士張孚敬 | — |
| `name:guanxian-jj12-04-zhang-fujing` | 致仕少傅兼太子太師、吏部尚書、華蓋殿大學士張孚敬 | — |
| `name:guanxian-jj13-03-jimao-xu-jie-xin` | 浙江按察司僉事，提調學校 | — |
| `name:guanxian-jj13-03-jimao-xu-jie-yuan` | 湖廣黃州府同知徐階 | — |
| `name:title-shizong-shilu` | 世宗實錄 | — |
| `name:title-siyi-chengdian` | 祀儀成典 | — |
| `name:zhang-cong` | 張璁 | — |
| `name:zhang-fujing` | 張孚敬 | — |
| `type:action-jia` | 加 | add (title) |
| `type:action-jin` | 进 | advance |
| `type:action-sheng` | 升 | promote |
| `type:anchasi-qianshi` | 按察司僉事 | Assistant Surveillance Commissioner |
| `type:benming` | 本名 | personal name |
| `type:chaiqian` | 差遣 | duty assignment |
| `type:chaiqian-weici` | 差遣位次 | rank within a duty assignment |
| `type:chaiqian-zhize` | 差遣职责 | function of a duty assignment |
| `type:ciming` | 赐名 | name bestowed by the emperor |
| `type:daxueshi` | 大學士 | Grand Secretary |
| `type:dian-ge-xian` | 殿阁衔 | grand secretary hall title |
| `type:donggong-sanshi` | 東宮三師 | Three Preceptors of the Heir Apparent |
| `type:dushi-guizhi-guan` | 督視規制官 | Dushi guizhi guan |
| `type:fu-tongzhi` | 府同知 | Vice Prefect |
| `type:fu-zongcai-guan` | 副總裁官 | Fu zongcai guan |
| `type:guanxian-chuan` | 官衔串 | official title string |
| `type:hanlin-shidu-xueshi` | 翰林院侍讀學士 | Academician Reader-in-waiting |
| `type:huagaidian-daxueshi` | 華蓋殿大學士 | Huagaidian Daxueshi |
| `type:jiaen` | 加恩 | bestowal of honor |
| `type:jianshi-xuncha-gongcheng-guan` | 監視巡察工程官 | Jianshi xuncha gongcheng guan |
| `type:jianxiu-guan` | 監修官 | Jianxiu guan |
| `type:jiaxian` | 加衔 | honorary title |
| `type:jinshendian-daxueshi` | 謹身殿大學士 | Jinshendian Daxueshi |
| `type:li-ke-du-jishizhong` | 吏科都給事中 | Chief Supervising Secretary of the Office of Scrutiny for Personnel |
| `type:pinjie-jianxian` | 品阶兼衔 | concurrent nominal title |
| `type:sangong` | 三公 | Three Dukes |
| `type:sangu` | 三孤 | Three Solitaries |
| `type:shangshu-personnel-xian` | 吏部尚書 | Minister of Personnel (concurrent nominal title held by a Grand Secretary) |
| `type:shangshu-rites-xian` | 禮部尚書 | Minister of Rites (concurrent nominal title held by a Grand Secretary) |
| `type:shaobao` | 少保 | Junior Guardian |
| `type:shaofu` | 少傅 | Junior Mentor |
| `type:shouxian-action` | 授衔动作 | title-conferral action |
| `type:taifu` | 太傅 | Grand Mentor |
| `type:taizi-taifu` | 太子太傅 | Grand Mentor of the Heir Apparent |
| `type:taizi-taishi` | 太子太師 | Grand Preceptor of the Heir Apparent |
| `type:tidiao-xuexiao` | 提調學校 | Supervisor of Education |
| `type:tongzhi-jianzao-shi` | 同知建造事 | Tongzhi jianzao shi |
| `type:wenyuange-daxueshi` | 文淵閣大學士 | Grand Secretary of the Hall of Literary Profundity |
| `type:zhangshi` | 掌事 | in charge of the affairs of an office |
| `type:zhao` | 召 | summons |
| `type:zhaohuan` | 召还 | recall to office |
| `type:zhi-jianzao-shi` | 知建造事 | Zhi jianzao shi |
| `type:zhishi` | 致仕 | retirement from office |
| `type:zongcai-guan` | 總裁官 | Director-general |
| `type:zongdu-gongcheng-guan` | 總督工程官 | Zongdu gongcheng guan |
| `type:zuanxiu-guan` | 纂修官 | Compiler |
| `mpv:conferred_title` | 授衔 | conferred title |
| `mpv:holds_title` | 持有头衔 | holds title |

<!-- END TABLE -->
