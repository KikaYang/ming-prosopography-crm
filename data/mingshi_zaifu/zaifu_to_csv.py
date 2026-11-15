"""Convert zaifu.json (output of parse_zaifu.py) into the two CSV files.

Reconstructed in November 2026 to reproduce mingshi_zaifu_long.csv and
mingshi_zaifu_persons.csv byte for byte. Simplified forms use OpenCC (t2s).
"""
import csv
import json
import sys

import opencc

T2S = opencc.OpenCC('t2s').convert

EXIT_KEYWORDS = ['致仕', '卒', '歸', '乞', '黜', '罷', '免', '下獄', '死', '棄市',
                 '遣戍', '削籍', '閒住', '回籍', '改南京', '出督師']
NOTE_GAP = '在阁年份不连续：可能是丁忧/罢免后复入，也可能是解析误差，需核'
NOTE_MISSING_CHAR = '名字含缺字，以□代'


def spans(years):
    out = []
    for y in years:
        if out and y == out[-1][1] + 1:
            out[-1][1] = y
        else:
            out.append([y, y])
    return out


def main(src='zaifu.json', long_out='mingshi_zaifu_long.csv',
         persons_out='mingshi_zaifu_persons.csv'):
    data = json.load(open(src, encoding='utf-8'))
    rows = data['rows']

    with open(long_out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['person_trad', 'person_simp', 'year_ce', 'reign_year',
                    'mingshi_juan', 'event_text'])
        for r in rows:
            w.writerow([r['person'], T2S(r['person']), r['year'], r['label'],
                        r['vol'], r['text']])

    with open(persons_out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['seq', 'name_trad', 'name_simp', 'first_year_ce',
                    'last_year_ce', 'n_years_listed', 'tenure_spans', 'n_spans',
                    'first_entry_record', 'last_record', 'exit_keywords', 'note'])
        for i, name in enumerate(data['order'], 1):
            rs = [r for r in rows if r['person'] == name]
            years = sorted({r['year'] for r in rs})
            sp = spans(years)
            sp_txt = '; '.join(f'{a}-{b}' if a != b else f'{a}' for a, b in sp)
            entry = next((r for r in rs if '入' in r['text']), None)
            first_entry = f"{entry['label']}:{entry['text']}" if entry else ''
            last = rs[-1]
            last_rec = f"{last['label']}:{last['text']}"
            kws = '/'.join(k for k in EXIT_KEYWORDS if k in last['text'])
            notes = []
            if len(sp) > 1:
                notes.append(NOTE_GAP)
            if '□' in name:
                notes.append(NOTE_MISSING_CHAR)
            w.writerow([i, name, T2S(name), years[0], years[-1], len(years),
                        sp_txt, len(sp), first_entry, last_rec, kws,
                        '；'.join(notes)])


if __name__ == '__main__':
    main(*sys.argv[1:])
