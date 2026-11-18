# *Mingshi* Tables of Grand Secretaries: parsing pipeline

This directory holds the grand secretaries of the Yongle to Chongzhen reigns and their year-by-year records, parsed from the Tables of Grand Secretaries (宰輔年表) in *Mingshi*, juan 109–110, together with their matching to CBDB.

## Source

- Wikisource, *Mingshi*, juan 109 (oldid=2594725) and juan 110 (oldid=2594726):
  - https://zh.wikisource.org/w/index.php?title=明史/卷109&oldid=2594725
  - https://zh.wikisource.org/w/index.php?title=明史/卷110&oldid=2594726
- Printed to PDF from a browser (Safari) on 2026-10-06. The PDFs are not included in this repository.
- The pages do not name a base edition.
- The text of the Mingshi is in the public domain; the licence of this repository applies only to the extraction, parsing and derived tables.

## Pipeline

```
PDF → extract_text.py → sources/ms109n.txt, sources/ms110n.txt
    → parse_zaifu.py → sources/zaifu.json
    → zaifu_to_csv.py → mingshi_zaifu_long.csv, mingshi_zaifu_persons.csv
    → scripts/match_mingshi_cbdb.py → mingshi_cbdb_match.csv, mingshi_cbdb_candidates.csv
```

| Step | Script | Description |
|---|---|---|
| 1 | `extract_text.py` | `pdftotext -layout` (poppler 24.02) keeps the two-column layout of the tables; the text is then normalised to Unicode NFKC. The PDF text layer uses Kangxi-radical code points (e.g. U+2F00 ⼀, ⿈); without normalisation `parse_zaifu.py` cannot find its starting name (黃淮). The `n` in the file names stands for the normalised text |
| 2 | `parse_zaifu.py` | Reads `ms109n.txt` and `ms110n.txt` from the working directory (juan 109 from 黃淮 onwards), skips page headers (containing 维基文库) and footers (URLs), separates the year column (紀年) from the column of appointments and dismissals (宰輔拜免) by layout, and writes `zaifu.json` |
| 3 | `zaifu_to_csv.py` | Generates the two CSV files from `zaifu.json`; simplified-character names are produced with OpenCC `t2s` |

To reproduce, from the `sources/` directory:

```bash
python ../extract_text.py /path/to/juan109.pdf /path/to/juan110.pdf
python ../parse_zaifu.py
python ../zaifu_to_csv.py zaifu.json ../mingshi_zaifu_long.csv ../mingshi_zaifu_persons.csv
```

`zaifu_to_csv.py` requires the `opencc` package (1.4.2, listed in `requirements.txt`); `extract_text.py` requires `pdftotext` from poppler, a system tool not listed in `requirements.txt`.

## Missing characters

Two rare characters cannot be encoded in the PDF text layer. Line 14 of `parse_zaifu.py` writes them as □:

- 沈□: the text layer reads 沈? (as does `ms110n.txt`);
- 李國□: one character is missing after 李國, which `pdftotext` outputs as a space (李國 七月 in `ms110n.txt`).

The note column of `mingshi_zaifu_persons.csv` marks both names: 名字含缺字，以□代 (the name contains a missing character, written □).

## History

The original parsing was carried out on 2026-10-06; its intermediate files were not preserved. The pipeline was reconstructed in November 2026. The present version contains the correction of 2026-11-18 (see "Known issues") and differs from the original version of October 2026 in three rows: `mingshi_zaifu_long.csv` has 1,039 rows instead of 1,040, and three rows of `mingshi_zaifu_persons.csv` differ. The files are reproducible byte for byte from the corrected pipeline; they are no longer identical to the original version.

- Running `zaifu_to_csv.py` on `sources/zaifu.json` gives both CSV files identical to those in this directory, and running `parse_zaifu.py` on the two text files in `sources/` gives a `zaifu.json` identical to `sources/zaifu.json`. `parse_zaifu.py` reports `109 cost 0.06`, `110 cost 1.94`, `1039 rows` and `163 persons`.
- `tests/test_zaifu_parse.py` checks that the alignment cost of each juan is below 100 and that no (person, year) pair occurs twice within a juan.
- The extraction of the two text files from the PDFs with poppler 24.02 was carried out in a separate Linux environment.

## Known issues

- Resolved (2026-11-18): abnormal alignment cost for juan 109 (about 1000; 1000.06 when reproduced).
  - Cause: the entry for Xu Youzhen 徐有貞 in Jingtai 8 is broken over two lines in the layout, and the second line begins with 文淵閣事. `resolve()` read the initial 文 as the one-character short name of Wang Wen 王文 and started a new record for him. Wang Wen then appeared twice in the same year segment, which the year alignment penalises with 1000.
  - Effect on three persons: the record of Xu Youzhen was cut off after 掌; Wang Wen had a false record for 1457 (淵閣事。六月下獄……); the entry of Shang Lu 商輅, 五月兼太常寺卿 (fifth month, concurrently Chief Minister of the Court of Imperial Sacrifices), was assigned to 1457 instead of 1456 (Jingtai 7).
  - Correction: in `resolve()`, when the previous entry does not end with 。, a one-character short name is read as a continuation line and does not start a new record. The cost for juan 109 is now 0.06; juan 110 is unchanged (1.94). `mingshi_zaifu_long.csv` has 1,039 rows instead of 1,040.
- The reign label of 1402 was once given as 洪武四年; since 2026-10-09 it reads 建文四年(洪武三十五年). The year_ce column was always correct.
- In `mingshi_zaifu_persons.csv`, 23 persons have discontinuous years in office; their note column marks them for checking.
