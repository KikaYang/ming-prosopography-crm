"""Extract the text of Mingshi juan 109-110 from the printed Wikisource pages.

Input:  PDFs of zh.wikisource.org/wiki/明史/卷109 (oldid=2594725) and
        明史/卷110 (oldid=2594726), printed from the browser on 2026-10-06.
Output: ms109n.txt, ms110n.txt, the input of parse_zaifu.py.

Steps: `pdftotext -layout` (poppler; verified with 24.02.0) keeps the two-column
layout of the table; Unicode NFKC normalisation then maps the Kangxi-radical
code points used in the PDF text layer (e.g. U+2F00 ⼀) and full-width
punctuation to their ordinary forms. Without it parse_zaifu.py cannot find its
starting name (黃淮).

Usage: python extract_text.py juan109.pdf juan110.pdf
"""
import subprocess
import sys
import unicodedata


def extract(pdf, out):
    raw = subprocess.run(['pdftotext', '-layout', pdf, '-'], check=True,
                         capture_output=True).stdout.decode('utf-8')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(unicodedata.normalize('NFKC', raw))


if __name__ == '__main__':
    extract(sys.argv[1], 'ms109n.txt')
    extract(sys.argv[2], 'ms110n.txt')
