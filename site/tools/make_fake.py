#!/usr/bin/env python3
"""A stand-in copy of her masterlist for trying the site: same tabs, columns, items, amounts and formulas, but every
username, name, address and phone number replaced with made-up ones. The output stays outside git.

  python3 site/tools/make_fake.py OUT.xlsx [--from data/owner/orders/orders-2026.xlsx]
"""
import argparse
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'automations'))
import masterlist as ml  # noqa: E402

SYL = ['min', 'ji', 'ha', 'na', 'yu', 'ri', 'so', 'eun', 'ka', 'ye', 'jin', 'mo', 'a', 'bi', 'chae', 'won', 'lu',
       'pia', 'kat', 'bea', 'joy', 'ella', 'nic', 'dani', 'rhea', 'ivy', 'mae', 'tin', 'ara', 'kyla']
TAIL = ['_ph', '.carat', 'engene', '_army', 'bong', '_moa', 'stay', '_x', '07', '_ot7', 'zen', 'luv', '']
FIRST = ['Maria', 'Angela', 'Kristine', 'Joanna', 'Patricia', 'Bea', 'Camille', 'Andrea', 'Nicole', 'Rhea', 'Janelle',
         'Mae', 'Erika', 'Princess', 'Hannah', 'Jasmine', 'Kyla', 'Danica', 'Mikaela', 'Francine']
LAST = ['Santos', 'Reyes', 'Cruz', 'Bautista', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Ramos', 'Villanueva',
        'Castillo', 'Aquino', 'Navarro', 'Domingo', 'Salazar', 'Mercado', 'Gonzales', 'Lopez', 'Dela Cruz', 'Pascual']


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--from', dest='src', default=str(ml.SHEET))
    a = ap.parse_args(argv)
    import openpyxl
    rnd = random.Random(7)
    handles, people = {}, {}

    def handle(real):
        key = ml.clean(real).lower()
        if key not in handles:
            while True:
                h = ''.join(rnd.choice(SYL) for _ in range(rnd.choice([2, 2, 3]))) + rnd.choice(TAIL)
                if h not in handles.values():
                    break
            handles[key] = ('@' if str(real).strip().startswith('@') else '') + h
        return handles[key]

    def person(real):
        key = ml.clean(real).lower()
        if key not in people:
            people[key] = f'{rnd.choice(FIRST)} {rnd.choice(LAST)}'
        return people[key]

    wb = openpyxl.load_workbook(a.src)                        # formulas kept
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(max_row=6, values_only=True))
        hi = ml._header_row(rows)
        if ws.title == ml.STOCK_TAB:
            for row in ws.iter_rows():
                for c in row:
                    if c.column == 9 and isinstance(c.value, str) and c.row > 2 and 'username' not in c.value.lower():
                        c.value = ', '.join(handle(x) for x in re.split(r'[,\n]+', c.value) if x.strip())
            continue
        if hi is None:
            for row in ws.iter_rows():                      # odd tabs: blank anything that isn't a number
                for c in row:
                    if isinstance(c.value, str) and not c.value.startswith('=') and c.row > 1:
                        c.value = None
            continue
        h = [ml.clean(x).lower() for x in rows[hi]]
        user = ml._find(rows[hi], r'twitter user|username')
        names = [i for i, x in enumerate(h) if re.search(r'full name|gcash name|^name$', x)]
        wipe = [i for i, x in enumerate(h) if re.search(r'address|contact|phone|tracking|email', x)]
        for row in ws.iter_rows(min_row=hi + 2):
            for c in row:
                i = c.column - 1
                if c.value is None:
                    continue
                if i == user and isinstance(c.value, str):
                    c.value = handle(c.value)
                elif i in names and isinstance(c.value, str):
                    c.value = person(c.value)
                elif i in wipe:
                    c.value = None
    for name in ('Shipping list', 'Anniversary Giveaway'):
        if name in wb.sheetnames:
            ws = wb[name]
            for row in ws.iter_rows(min_row=2):
                for c in row:
                    if isinstance(c.value, str) and not c.value.startswith('='):
                        c.value = handle(c.value) if c.column == 2 else None
    wb.save(a.out)
    print(f'{a.out}: {len(handles)} made-up usernames')


if __name__ == '__main__':
    sys.exit(main())
