#!/usr/bin/env python3
"""Her order masterlist (a Google Sheet): download it, read the "ONHAND items" stock tab and the open balances.

PRIVATE DATA. The sheet has buyers' full names, addresses and phone numbers. It lives in data/owner/orders/
(git-ignored). Only username, GO tab, item, amounts, courier, due date and status leave this module; the name
columns are kept under `_names`, used only to match payment screenshots, and never printed or saved.

Usage:
  python3 automations/masterlist.py           # download the latest copy: as the robot account she shared the sheet
                                              # with (automations/google_sheet.py), else the link in source.txt
"""
import datetime as dt
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import google_sheet  # noqa: E402
from common import DATA, PHT, now_utc  # noqa: E402

ORDERS = DATA / 'owner' / 'orders'
SHEET = ORDERS / 'orders-2026.xlsx'
SOURCE = ORDERS / 'source.txt'          # her share link, one line (private, like the sheet)
STOCK_TAB = 'ONHAND items'
NOT_ORDERS = {STOCK_TAB, 'Terms and Conditions', 'Shipping list', 'Anniversary Giveaway', 'Desk log'}
CANCELLED = re.compile(r'cancel|refund|forfeit', re.I)
MONTHS = {m: i for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',
                                      'dec'], 1)}


# ---------- download ----------

def sheet_id(link):
    return google_sheet.sheet_id(link)


def _save(dest, content):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix('.tmp')
    tmp.write_bytes(content)
    tmp.replace(dest)


def fetch(dest=SHEET, source=SOURCE, get=requests.get, key=google_sheet.KEY):
    """Download the latest copy over the saved one: as the robot account when its key is on this laptop, else the
    share link. On any problem keep the old copy. Returns (ok, message)."""
    link = source.read_text().strip() if source.exists() else ''
    sid = sheet_id(link)
    if not sid:
        return False, f'no sheet link in {source.name}; using the saved copy'
    note = ''
    if Path(key).exists():
        try:
            content = google_sheet.Sheet(sid, key).export()
            _save(dest, content)
            return True, f'sheet downloaded as the robot account ({len(content) // 1024} KB)'
        except google_sheet.GoogleError as e:
            note = f'robot account: {e}; '
    try:
        content = google_sheet.PublicLink(sid, get).export()
    except google_sheet.GoogleError as e:
        return False, f'{note}{e}; using the saved copy'
    _save(dest, content)
    return True, f'{note}sheet downloaded ({len(content) // 1024} KB)'


def open_sheet(path=SHEET):
    import openpyxl
    return openpyxl.load_workbook(path, read_only=True, data_only=True)


def read_at(path=SHEET):
    """When the saved copy was downloaded, Philippine time."""
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).astimezone(PHT)


# ---------- small parsers (tested) ----------

def clean(v):
    return ' '.join(str(v).split()) if v is not None else ''


def num(v):
    """2650, '2,650', '₱2650.00', '-100' → float. Text, '#REF!' and blanks → None."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.replace(',', '').strip()
        m = re.fullmatch(r'(?:₱|php|p)?\s*(-?\d+(?:\.\d+)?)', s, re.I)
        return float(m.group(1)) if m else None
    return None


def parse_due(v, anchor_year=None, today=None):
    """A due date cell → (date, year_guessed). Real dates pass through. Text like 'PAYO/AUG 15' or 'June 30' takes
    the year of the nearest real date in the same tab (anchor_year), else the year closest to today."""
    if isinstance(v, dt.datetime):
        return v.date(), False
    if isinstance(v, dt.date):
        return v, False
    if isinstance(v, (int, float)) and 36500 < v < 73000:    # a date stored as a plain number (days since 1899-12-30)
        return dt.date(1899, 12, 30) + dt.timedelta(days=int(v)), False
    m = re.fullmatch(r'\s*(\d{4})-(\d{1,2})-(\d{1,2})\s*', str(v or ''))      # 2026-10-30 (what the website writes)
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))), False
        except ValueError:
            pass
    m = re.fullmatch(r'\s*(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})\s*', str(v or ''))  # 10/30/2026 typed as text
    if m:
        y = int(m.group(3)) + (2000 if len(m.group(3)) == 2 else 0)
        try:
            return dt.date(y, int(m.group(1)), int(m.group(2))), False
        except ValueError:
            pass
    found = None
    for m in re.finditer(r'([A-Za-z]{3,9})\.?\s*(\d{1,2})(?!\d)', str(v or '')):
        mon = MONTHS.get(m.group(1)[:3].lower())
        if mon and 1 <= int(m.group(2)) <= 31:
            found = (mon, int(m.group(2)))
    if not found:
        return None, False

    def make(y):
        try:
            return dt.date(y, *found)
        except ValueError:          # "Sept 31", "Feb 30": the last day of that month
            nxt = dt.date(y + found[0] // 12, found[0] % 12 + 1, 1)
            return nxt - dt.timedelta(days=1)
    if anchor_year:
        return make(anchor_year), False
    today = today or now_utc().astimezone(PHT).date()
    return min((make(y) for y in (today.year - 1, today.year, today.year + 1)), key=lambda d: abs(d - today)), True


def _find(header, *patterns):
    for p in patterns:
        for i, h in enumerate(header):
            if re.search(p, clean(h).lower()):
                return i
    return None


# ---------- the stock tab ----------

def _price_label(h):
    if isinstance(h, (dt.date, dt.datetime)):
        return f'if paid by {h:%b} {h.day}'
    h = clean(h).lower()
    if h == 'payo':
        return 'paid in full at order'
    m = re.match(r'(\d+) days', h)
    return f'within {m.group(1)} days' if m else h


def stock_items(ws, sold_out=False):
    """Items in the "ONHAND items" tab that still have slots (or no slot count; with sold_out=True, every item). Each
    has its sheet row and the slot columns, so the website can record a taken slot. Never returns who took them.

    Her layout: a section title row ("ENCHIN ... UNNIEMART" plus the slot column names), a header row
    (PAYO · 30 days · 60 days · DP, or dated price steps), then one row per item. A blank price means "same as the
    row above"; a row with neither prices nor slots is a sub-heading (e.g. "Weverse Shop with POB")."""
    out, section, sub, prices_at, dp_at, left_at, total_at, last = [], '', '', [], None, None, None, None
    taken_at = takers_at = title_r = None
    for at, r in enumerate(ws.iter_rows(values_only=True), 1):
        r = list(r) + [None] * 14
        name = clean(r[1])
        if not name:
            continue
        cells = [clean(x).lower() for x in r[2:14]]
        if 'unniemart' in name.lower() or any('slot' in c for c in cells):            # section title
            section = clean(re.sub(r'unniemart', '', name, flags=re.I)).strip(' -·')
            sub, last, prices_at, dp_at = '', None, [], None
            left_at = next((i + 2 for i, c in enumerate(cells) if c == 'total available slots'), None)
            total_at = next((i + 2 for i, c in enumerate(cells) if c == 'available slots'), None)
            taken_at = next((i + 2 for i, c in enumerate(cells) if c == 'slots taken'), None)
            takers_at = next((i + 2 for i, c in enumerate(cells) if 'username' in c), None)
            title_r = at
            continue
        if clean(r[2]).lower() == 'payo':                                               # header row
            dp_at = next((i for i in range(2, 14) if clean(r[i]).lower() == 'dp'), None)
            prices_at = [(i, _price_label(r[i])) for i in range(2, dp_at or 6)]
            continue
        if not prices_at:
            continue
        prices = [(label, num(r[i])) for i, label in prices_at if num(r[i]) is not None]
        dp = num(r[dp_at]) if dp_at is not None else None
        left = num(r[left_at]) if left_at is not None else None
        total = num(r[total_at]) if total_at is not None else None
        carried = False
        if not prices and left is None and total is None:
            sub = name                                                                  # sub-heading
            continue
        if not prices and last:
            prices, dp, carried = last['prices'], last['dp'], True
        if prices:
            last = {'prices': prices, 'dp': dp}
        if left is not None and left <= 0 and not sold_out:
            continue                                                                    # sold out
        taken = num(r[taken_at]) if taken_at is not None else None
        out.append({'section': section, 'sub': sub, 'item': name, 'prices': prices, 'dp': dp,
                    'slots_left': int(left) if left is not None else None,
                    'slots_total': int(total) if total is not None else None, 'price_carried': carried,
                    'slots_taken': int(taken) if taken is not None else None, 'r': at,
                    'cols': {'name': 1, 'total': total_at, 'taken': taken_at, 'takers': takers_at, 'left': left_at,
                             'title_r': title_r}})
    return out


def price_text(it):
    p = '; '.join(f'₱{a:,.0f} {label}' for label, a in it['prices'])
    if it['dp']:
        p += f'; down payment ₱{it["dp"]:,.0f}'
    return p


# ---------- the order tabs ----------

def _header_row(rows):
    for i, r in enumerate(rows[:6]):
        if r and _find(r, r'twitter user|username') is not None and _find(r, r'^total$', r'^total') is not None:
            return i
    return None


def tab_columns(h):
    """Where each field sits in a GO tab's header row (column numbers from 0; None when the tab has no such column)."""
    c = {'user': _find(h, r'twitter user|username'), 'item': _find(h, r'^items?$'),
         'qty': _find(h, r'^qty|^quantity|no\. of items'), 'total': _find(h, r'^total$', r'^total'),
         'pay': _find(h, r'^payment|downpayment'), 'bal': _find(h, r'^balance|rembal'),
         'mod': _find(h, r'^mod$', r'^courier$'), 'due': _find(h, r'due date|deadline'),
         'status': _find(h, r'^status$', r'status', r'remarks')}
    c['note'] = _find(h, r'^notes?$', r'^remarks?$')
    if c['note'] == c['status']:
        c['note'] = None
    return c


def tab_orders(title, rows, today=None):
    """Every order line in one GO tab, with its balance and due date. Rows the sheet marks as cancelled or
    refunded are left out. Each line keeps its sheet row (`r`) and the tab's columns (`cols`), so the website can
    write to the right cell; `shifted` lines (values two columns off) are read-only."""
    hi = _header_row(rows)
    if hi is None:
        return []
    h = rows[hi]
    c = tab_columns(h)
    names = [i for i, x in enumerate(h) if re.search(r'full name|gcash name', clean(x).lower())]
    get = lambda r, k: r[c[k]] if c[k] is not None else None  # noqa: E731
    lines = []
    for at, r in enumerate(rows[hi + 1:], hi + 2):        # at: the row number in her sheet
        r = list(r or ()) + [None] * 40
        user = clean(get(r, 'user'))
        if not re.search(r'[a-zA-Z]', user) or re.search(r'username', user, re.I):
            continue
        if any(isinstance(x, str) and CANCELLED.search(x) for x in r):
            continue
        shifted = c['item'] is not None and num(r[c['item']]) is not None and c['qty'] == c['item'] + 1
        if shifted:
            # Some old rows have no item and qty cells: every value sits two columns to the left.
            r = r[:c['item']] + [None, None] + r[c['item']:]
        total, pay, bal = num(get(r, 'total')), num(get(r, 'pay')), num(get(r, 'bal'))
        if bal is None and total is not None and pay is not None:
            bal = total - pay
        if bal is not None and (total is None or bal > total):     # unreadable row (often a date in the wrong cell)
            bal = None
        raw_due = get(r, 'due')
        lines.append({'tab': title, 'r': at, 'user': user, 'item': clean(get(r, 'item')), 'qty': num(get(r, 'qty')),
                      'total': total, 'paid': pay, 'balance': bal, 'courier': clean(get(r, 'mod')),
                      'status': clean(get(r, 'status')), 'note': clean(get(r, 'note')), 'raw_due': raw_due,
                      'cols': c, 'hr': hi + 1, 'shifted': shifted,
                      '_names': [clean(r[i]) for i in names if clean(r[i])]})
    # Text dates ("OCT 15") take the year of the nearest real date in the tab: above first, else below.
    years = [x['raw_due'].year if isinstance(x['raw_due'], (dt.date, dt.datetime)) else None for x in lines]
    for i, x in enumerate(lines):
        anchor = next((y for y in reversed(years[:i]) if y), None) or next((y for y in years[i:] if y), None)
        x['due'], x['year_guessed'] = parse_due(x['raw_due'], anchor, today)
        x['due_text'] = '' if isinstance(x['raw_due'], (dt.date, dt.datetime)) else clean(x['raw_due'])
        del x['raw_due']
    # Rows with no due date belong to the time of the dated rows around them (above first, else below).
    dues = [x['due'] for x in lines]
    for i, x in enumerate(lines):
        x['near'] = x['due'] or next((d for d in reversed(dues[:i]) if d), None) or next((d for d in dues[i:] if d), None)
    return lines


def all_orders(wb, today=None):
    out = []
    for ws in wb.worksheets:
        if ws.title in NOT_ORDERS:
            continue
        out += tab_orders(ws.title, list(ws.iter_rows(values_only=True)), today)
    return out


def main():
    ok, msg = fetch()
    print(f'masterlist: {msg}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
