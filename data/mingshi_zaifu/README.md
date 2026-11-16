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

`zaifu_to_csv.py` requires the `opencc` package (verified with 1.4.2), and `extract_text.py` requires `pdftotext` from poppler. Neither is listed in `requirements.txt`.

## Missing characters

Two rare characters cannot be encoded in the PDF text layer. Line 14 of `parse_zaifu.py` writes them as □:

- 沈□: the text layer reads 沈? (as does `ms110n.txt`);
- 李國□: one character is missing after 李國, which `pdftotext` outputs as a space (李國 七月 in `ms110n.txt`).

The note column of `mingshi_zaifu_persons.csv` marks both names: 名字含缺字，以□代 (the name contains a missing character, written □).

## History

The original parsing was carried out on 2026-10-06 in a cloud session; its intermediate files were not preserved. The pipeline was reconstructed in November 2026 and reproduces both CSV files byte for byte.

- Running `zaifu_to_csv.py` on `sources/zaifu.json` gives both CSV files identical to those in this directory, and running `parse_zaifu.py` on the two text files in `sources/` gives a `zaifu.json` identical to `sources/zaifu.json` (verified 2026-11-15).
- The extraction of the two text files from the PDFs with poppler 24.02 was carried out in a separate Linux environment.

## Known issues

- For juan 109, `parse_zaifu.py` reports an abnormal score for the alignment of years (cost ≈ 1000; 1000.06 when reproduced), so a few records may be assigned to the wrong year; this has not been checked. Juan 110 is normal (cost 1.94).
- The reign label of 1402 was once given as 洪武四年; since 2026-10-09 it reads 建文四年(洪武三十五年). The year_ce column was always correct.
- In `mingshi_zaifu_persons.csv`, 23 persons have discontinuous years in office; their note column marks them for checking.
