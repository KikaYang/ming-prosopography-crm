# Ming prosopography and European standards

This repository accompanies a master's thesis in Digital Humanities and Digital Knowledge (University of Bologna). The thesis tests whether European prosopographical standards (the factoid model and CIDOC-CRM) can express the careers of Ming grand secretaries, using three case studies taken from the *Shizong shilu*: SL12 (juan 89, 136, 149), SL11 (juan 118) and SL14 (juan 161). Each case is modelled in an event version and a state version, and each model, together with the China Biographical Database (CBDB), is evaluated against information units drawn from the source text and against a set of competency questions.

This is a snapshot of November 2026 of work in progress.

## Start here

1. Two worked examples, provided separately from this repository. Read them first.
2. `docs/modelling/modelling_decisions_en.md`: the modelling decisions (D1–D26), the open questions (Q1–Q7, T1–T4) and a code reference.
   `docs/modelling/naming_en.md` explains how identifiers are formed and lists every identifier with its Chinese and English labels.
3. `data/evaluation/README_en.md`: the evaluation method, rules and versions.
4. The models (`docs/modelling/*.ttl`) and the evaluation tables (`data/evaluation/*_vs_units*.csv`, `cases_summary.csv`, `cq_results.csv`).

## Repository layout

| Path | Contents |
|---|---|
| `docs/modelling/` | CIDOC-CRM models in Turtle: `SL12_event.ttl`, `SL12_state.ttl`, `SL11_*.ttl`, `SL14_*.ttl`, the shared vocabulary `vocab.ttl` and `prefixes.ttl`; diagrams of the event versions (Chinese labels, and English labels in `*_en.png`); the modelling decision log; `naming_en.md`, the identifier rules with a table of all labels |
| `data/evaluation/` | Information units (`info_units.csv`), evaluation tables and summaries, competency questions with their queries (`cq_queries/`), raw results (`cq_raw/`) and judgements (`cq_results.csv`); evaluation notes (`README_en.md`) |
| `evaluated_versions/` | Verbatim copies of the model files as they stood at each evaluation (see below) |
| `data/deep_cases/` | Multi-source factoid tables for the three core persons (Zhang Cong, Xia Yan, Xu Jie) |
| `data/mingshi_zaifu/` | Grand secretaries of the *Mingshi* tables (juan 109–110) and their matching to CBDB |
| `coverage_ming_grand_secretaries.csv`, `coverage_check.py` | CBDB coverage of the Jiajing and Longqing grand secretaries, and the script that produces it |
| `data/apis/` | A record from the Austrian APIS prosopography, for comparison |
| `scripts/` | `check_crm.py` (checks Turtle against CIDOC-CRM), `ttl_to_diagram.py` (with `--lang en` for English diagrams), `naming_table.py` (regenerates the label table in `naming_en.md`), `match_mingshi_cbdb.py`; `scripts/eval/` generates the evaluation tables and runs the competency questions |
| `tests/` | Unit and regression tests |
| `ontologies/` | CIDOC-CRM 7.1.3 RDFS files |

Some tables were produced by scripts that are not part of this snapshot, because they depend on material that is not included:
- `data/deep_cases/`: built from CBDB, from an LLM extraction of *Mingshi* biographies and from manual checks of the *Shilu*; the extraction cache and the scripts are not included.
- `data/mingshi_zaifu/mingshi_zaifu_*.csv`: parsed from the Wikisource text of *Mingshi* juan 109–110; the parser and its input are not included. The CBDB matching (`mingshi_cbdb_*.csv`) is produced by `scripts/match_mingshi_cbdb.py`.

## Installation

Python 3.14 (other recent versions are untested). Graphviz `dot` is needed only for diagrams.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The CBDB database is not included. The CBDB evidence checks and SQL queries need the SQLite format of the CBDB standalone release (see below), placed at `private/cbdb_20260602/cbdb_20260613.sqlite3`, or at any path given in the `CBDB_PATH` environment variable. Without it, those checks are skipped and everything else runs.

## Running the tests and reproducing the evaluation tables

All commands run from the repository root.

```bash
.venv/bin/python -m unittest discover -s tests
```

```bash
.venv/bin/python scripts/eval/sl12.py
```

```bash
.venv/bin/python scripts/eval/sl11.py
```

```bash
.venv/bin/python scripts/eval/sl14.py
```

```bash
.venv/bin/python scripts/eval/cq.py
```

```bash
.venv/bin/python data/evaluation/summarize.py
```

```bash
.venv/bin/python scripts/check_crm.py docs/modelling/SL14_event.ttl --vocab docs/modelling/vocab.ttl
```

The evaluation scripts rewrite the tables in `data/evaluation/`; on an unchanged checkout the files stay byte-for-byte identical, which the tests check.

Each evaluation table was produced against the model files as they stood at a given point of development, identified by a tag (`eval-SL11-v1.2`, `eval-SL14-v1.1`, `cq-v1`). Those files are included unchanged in `evaluated_versions/<tag>/`, solely so that the evaluation tables can be reproduced; the current models in `docs/modelling/` have since received further changes (e.g. definitions moved into `vocab.ttl`, revised comments). Commit hashes and tag names in the documents and tables refer to the development history of the author's private repository, which is not part of this snapshot. In the tables and scripts, "Yang" refers to the author.

## Data sources and licences

- **CBDB reference release**: `CBDB_20260602_sqlite.7z`, from the official offline-release page of the China Biographical Database (accessible after login), downloaded 2026-11-09. It contains `cbdb_20260613.sqlite3`, sha256 `89a303995bffdcce6d602d4fc59e6133844aa9b015df74cf7230214d7ef7e41a`.
- **Check against the reference release** (2026-11-09): the work was originally carried out on a later SQLite build (`cbdb_20261003`). All CBDB records cited for the three cases were compared, record by record, with the reference release: the postings, posting addresses and code-table entries cited all match, the CBDB evidence of the three evaluation tables passes on the reference release, and the SQL competency queries return identical results. The bulk tables `coverage_ming_grand_secretaries.csv` and `data/mingshi_zaifu/mingshi_cbdb_*.csv` differed only in counts of records added after the reference release and were regenerated from it. Two points await confirmation by CBDB: the archive name (20260602) differs from the file name (20260613), and the file contains 659,236 people in `BIOG_MAIN`, while the download page gives 649,533 for BJ 20260602.
- **Historical sources**: *Shizong shilu* passages were checked on the Shidian Guji platform (red-line manuscript); *Mingshi* passages are from Wikisource. Short quotations only.
- **Licences**:
  - Unless otherwise noted, CC BY-NC-SA 4.0 (see `LICENSE`), which also covers the CBDB-derived content. Attribution of CBDB: China Biographical Database (CBDB), https://cbdb.hsites.harvard.edu/, release CBDB_20260602 (`cbdb_20260613.sqlite3`).
  - `ontologies/`: CC BY 4.0 (FORTH-ICS); see `ontologies/LICENSE.md`.
  - `data/apis/`: CC BY-NC-SA 3.0; see `data/apis/LICENSE.md`.

## Use of AI tools

The scripts, the first-pass evaluation judgements and some of the documents, including the English versions of the modelling decision log and of the evaluation notes, were written by an AI agent (Claude Code). The core parts of the models, all modelling decisions and all evaluation judgements were written or approved by the author. The documents and tables record this as "first-pass judgement: AI agent (Claude Code)" and "approved by the author" (or "Yang"). Details are given in the Methodology chapter of the thesis.
