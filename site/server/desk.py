"""Her orders and stock, live from her sheet, and the changes the website writes back.

Reading: every few seconds the site asks Google whether her sheet changed (robot account) or, on the share link,
downloads it every two minutes. On a change it reads the whole sheet with the same rules as the laptop
(automations/masterlist.py) and notes what changed (shown as "In the sheet: ..." in the history).

Writing (robot account only): Payment received, an edited due date / status / courier / note, a stock slot taken.
Each one first checks the row still belongs to that buyer (rows can move), writes a line to her "Desk log" tab with
the value before and after, then changes the one cell. A payment can be undone for 15 minutes if nobody changed the
cell since. Reminders are noted on the username cell.

A part payment is added to the same Payment cell ("=500" → "=500+2650"), so every payment on a line can be listed.

Buyers' full names are read with the rest of the sheet but never leave this module.
"""
import collections
import datetime as dt
import io
import json
import re
import threading
import time

import settings  # noqa: F401  (puts automations/ on the path)
import google_sheet as gs
import masterlist as ml
import order_desk as od
from common import PHT, now_utc

LIVE_BUCKETS = ('late', 'week', 'soon', 'later', 'undated')
EDITABLE = {'due': 'due', 'status': 'status', 'courier': 'mod', 'note': 'note'}


class DeskError(Exception):
    pass


def today_pht():
    return now_utc().astimezone(PHT).date()


def parse(xlsx, today=None):
    import warnings
    import openpyxl
    warnings.filterwarnings('ignore', message='Unknown extension', module='openpyxl')   # Google's export, harmless
    wb = openpyxl.load_workbook(io.BytesIO(xlsx), read_only=True, data_only=True)
    try:
        lines = ml.all_orders(wb, today)
        items = ml.stock_items(wb[ml.STOCK_TAB], sold_out=True) if ml.STOCK_TAB in wb.sheetnames else []
    finally:
        wb.close()
    return lines, items


def peso(v):
    v = float(v or 0)
    return f'₱{v:,.0f}' if v == int(v) else f'₱{v:,.2f}'


def amount_text(a):
    return str(int(a)) if float(a) == int(a) else f'{a:.2f}'


def _key(x):
    return (x['tab'], x['user'].lower(), x['item'].lower())


def diff(old, new):
    """What changed in the sheet between two reads, in words. Lines are matched by tab, buyer and item."""
    if not old:
        return []
    def index(lines):
        out, seen = {}, {}
        for x in lines:
            k = _key(x)
            seen[k] = seen.get(k, 0) + 1
            out[k + (seen[k],)] = x
        return out
    a, b = index(old), index(new)
    out = []
    for k, y in b.items():
        x = a.get(k)
        who = '@' + y['user'].lstrip('@')
        where = y['item'] or y['tab'].strip()
        if x is None:
            out.append(('new', f'New order: {who} · {where}', y))
            continue
        p0, p1 = x.get('paid') or 0, y.get('paid') or 0
        if p1 > p0 + 0.005:
            out.append(('pay', f'{who} paid {peso(p1 - p0)} · {where}', y))
        elif abs((x.get('balance') or 0) - (y.get('balance') or 0)) > 0.005:
            out.append(('balance', f'{who} balance now {peso(y.get("balance"))} · {where}', y))
        if x.get('due') != y.get('due') and y.get('due'):
            out.append(('due', f'{who} due {y["due"]:%b} {y["due"].day} · {where}', y))
    return out


def split_payments(v):
    """The amounts in a Payment cell, in the order they were added. Her way of adding a payment is "+amount" on the
    formula, so "=300+1000+1450" is three payments."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return [round(float(v), 2)] if v else []
    s = str(v if v is not None else '').strip().replace(',', '')
    if not s:
        return []
    if re.fullmatch(r'=?\s*\d+(\.\d+)?(\s*\+\s*\d+(\.\d+)?)*', s):
        return [round(float(n), 2) for n in re.findall(r'\d+(?:\.\d+)?', s)]
    return None


def norm_cell(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return round(float(v), 2)
    s = str(v if v is not None else '').strip()
    n = ml.num(s)
    return round(n, 2) if n is not None and not s.startswith('=') else s.replace(' ', '').upper()


class AutoSource:
    """The robot account when it can open her sheet, else her share link (read-only). While on the share link it
    tries the robot again every minute, so the site starts writing by itself once she shares the sheet."""
    RETRY_S = 60

    def __init__(self, sid, key, sheet=None, link=None):
        from pathlib import Path
        self.sid, self.key = sid, Path(key)
        self._sheet, self._link = sheet or gs.Sheet, link or gs.PublicLink
        self.cur, self.tried, self.robot_error = None, 0.0, None
        self.pick()

    def pick(self):
        self.tried = time.time()
        if self.key.exists():
            try:
                s = self._sheet(self.sid, self.key)
                s.version()
                # an Excel file: the robot reads it (faster than the link, and works once it's Restricted) but
                # can't write; that only changes when she saves it as a Google Sheet, which is a new file and link
                self.cur, self.robot_error = s, (gs.EXCEL_NOTE if getattr(s, 'office', False) else None)
                return
            except Exception as e:                      # noqa: BLE001  any failure: read-only via the link
                self.robot_error = str(e) if isinstance(e, gs.GoogleError) else f'robot account: {type(e).__name__}'
        else:
            self.robot_error = 'no robot key on the server yet'
        if self.cur is None or self.cur.can_write:
            self.cur = self._link(self.sid)

    def version(self):
        if self.cur.mode == 'link' and time.time() - self.tried > self.RETRY_S:
            self.pick()
        return self.cur.version()

    def __getattr__(self, name):              # mode, can_write, url, export, cell, put, ...
        return getattr(self.cur, name)


class Desk:
    def __init__(self, source, store, bump=lambda: None, names=None):
        self.src = source
        self.store = store
        self.bump = bump
        self.names = names or {}             # user id → display name, for the Desk log
        self.lines, self.items = [], []
        self.version = None
        self.read_at = None
        self.error = None
        self.checked = 0.0
        self.writes = 0
        self.gids = {}
        self.lock = threading.RLock()
        self.wlock = threading.Lock()
        self.rev = 0                         # bumps on every change to what the page shows
        self._snap = None
        self._reqs = collections.OrderedDict()   # recent payment requests: a repeated tap is not paid twice

    # ---------- reading ----------

    @property
    def live(self):
        return getattr(self.src, 'can_write', False)

    def tick(self, force=False):
        """Read her sheet again when it changed. Called by the background loop (and after writes)."""
        if self.src is None:
            return False
        now = time.time()
        every = settings.CHECK_LINK_S if self.src.mode == 'link' else settings.CHECK_LIVE_S
        if not force and now - self.checked < every:
            return False
        self.checked = now
        writes = self.writes
        try:
            v, _ = self.src.version()
            if not force and v is not None and v == self.version and self.lines:
                return False
            lines, items = parse(self.src.export(), today_pht())
            getattr(self.src, 'forget_tabs', lambda: None)()        # tabs may have been added, renamed or deleted
            gids = self.src.tabs() if self.src.mode == 'live' else {}
        except Exception as e:                                      # noqa: BLE001  shown on the page, retried
            msg = str(e) if isinstance(e, gs.GoogleError) else f'could not read the sheet ({type(e).__name__})'
            changed = self.error != msg
            self.error = msg
            if changed:
                self._changed()
            return False
        if writes != self.writes:            # a write landed while reading: read again on the next tick
            self.checked = 0
            return False
        with self.lock:
            changes = diff(self.lines, lines)
            self.lines, self.items, self.version, self.gids = lines, items, v, gids
            self.read_at, self.error = now_utc(), None
        if len(changes) > 25:
            self.store.act('sheet', 'sheet', f'{len(changes)} changes in the sheet')
        else:
            for kind, text, y in changes:
                self.store.act('sheet', 'sheet-' + kind, text, {'k': f'{y["tab"]}|{y["r"]}'})
        self._changed()
        return True

    def _changed(self):
        self.rev += 1
        self._snap = None
        self.bump()

    # ---------- what the page gets ----------

    def _client_line(self, x, bucket, today, reminded):
        c = x['cols']
        can = self.live and not x.get('shifted')
        due = x.get('due')
        return {
            'k': f'{x["tab"]}|{x["r"]}', 'tab': x['tab'], 'go': x['tab'].strip(), 'r': x['r'], 'user': x['user'],
            'item': od.nice(x['item']) if x['item'] else '', 'ri': x['item'], 'qty': x.get('qty'), 'total': x.get('total'),
            'paid': x.get('paid'), 'bal': x.get('balance'), 'due': due.isoformat() if due else None,
            'due_text': x.get('due_text', ''), 'guessed': bool(x.get('year_guessed')),
            'near': x['near'].isoformat() if x.get('near') else None, 'bucket': bucket,
            'status': x.get('status', ''), 'courier': x.get('courier', ''), 'note': x.get('note', ''),
            'reminded': reminded.get((x['tab'], x['user'])),
            'msg': od.reminder(x, today) if (x.get('balance') or 0) > 0 else '',
            'can': {'pay': can and c.get('pay') is not None,
                    **{f: can and c.get(col) is not None for f, col in EDITABLE.items()}},
            'gid': self.gids.get(x['tab']),
        }

    def snapshot(self):
        """Open balances, GO totals and stock, for the page. Cached until something changes."""
        today = today_pht()
        if self._snap and self._snap[0] == today:
            return self._snap[1]
        rev = self.rev
        with self.lock:
            lines, items = list(self.lines), list(self.items)
        reminded = self.store.last_reminders()
        b = od.buckets(lines, today)
        bucket_of = {id(x): k for k, xs in b.items() for x in xs}
        open_lines = [self._client_line(x, k, today, reminded) for k in ('late', 'week', 'soon', 'later', 'undated', 'old')
                      for x in b[k]]                                    # each group by due date, soonest first
        gos = {}
        for x in lines:
            g = gos.setdefault(x['tab'], {'tab': x['tab'], 'go': x['tab'].strip(), 'lines': 0, 'buyers': set(),
                                          'total': 0.0, 'paid': 0.0, 'owed': 0.0, 'owed_old': 0.0, 'open': 0,
                                          'last': None})
            g['lines'] += 1
            g['buyers'].add(x['user'].lower())
            g['total'] += x.get('total') or 0
            g['paid'] += x.get('paid') or 0
            k = bucket_of.get(id(x))
            if k in LIVE_BUCKETS:
                g['owed'] += x['balance']
                g['open'] += 1
            elif k == 'old':
                g['owed_old'] += x['balance']
            d = x.get('due') or x.get('near')
            if d and (g['last'] is None or d > g['last']):
                g['last'] = d
        go_list = []
        for g in gos.values():
            g['buyers'] = len(g['buyers'])
            g['last'] = g['last'].isoformat() if g['last'] else None
            go_list.append(g)
        go_list.sort(key=lambda g: (g['owed'] <= 0, -dt.date.fromisoformat(g['last']).toordinal()
                                    if g['last'] else 0))
        stock = [{'k': f'stock|{it["r"]}', 'r': it['r'], 'section': od.nice(it['section']), 'sub': od.nice(it['sub']),
                  'item': od.nice(it['item']), 'raw': it['item'],
                  'prices': [[od.short(lbl), a] for lbl, a in it['prices']], 'dp': it['dp'],
                  'left': it['slots_left'], 'total': it['slots_total'], 'taken': it['slots_taken'],
                  'carried': it['price_carried'],
                  'can': self.live and it['cols'].get('taken') is not None} for it in items]
        snap = {'lines': open_lines, 'gos': go_list, 'stock': stock, 'today': today.isoformat(),
                'sheet': self.status()}
        if rev == self.rev:                     # nothing changed while building it
            self._snap = (today, snap)
        return snap

    def status(self):
        src = self.src
        return {'mode': src.mode if src else 'off', 'can_write': self.live, 'error': self.error,
                'read_at': self.read_at.isoformat() if self.read_at else None,
                'url': src.url if src else None, 'robot': gs.robot_email(settings.GOOGLE_KEY),
                'robot_error': getattr(src, 'robot_error', None) if src else None}

    def go_lines(self, tab):
        today = today_pht()
        reminded = self.store.last_reminders()
        with self.lock:
            lines = [x for x in self.lines if x['tab'] == tab]
        b = od.buckets(lines, today)
        bucket_of = {id(x): k for k, xs in b.items() for x in xs}
        return [self._client_line(x, bucket_of.get(id(x), 'paid'), today, reminded) for x in lines]

    def payments(self, tab, r, user, item=None):
        """The separate payments on one line, from its Payment cell: "=500+2650" → [500, 2650]. None when the cell
        can't be split (another formula, text) or the site can only read the share link."""
        x = self._find(tab, r, user, item)
        if not self.live or self.error or x.get('shifted') or x['cols'].get('pay') is None:
            return {'parts': None}
        return {'parts': split_payments(self.src.cell(tab, x['cols']['pay'], x['r']))}

    # ---------- writing ----------

    def _find(self, tab, r, user, item=None):
        """The order line the page means: same tab, buyer and item (the row number can be out of date). A buyer
        with several lines in one tab must match exactly; otherwise the page is asked to refresh."""
        with self.lock:
            cands = [x for x in self.lines if x['tab'] == tab and x['user'] == user and
                     (item is None or x['item'] == item)]
        exact = [x for x in cands if x['r'] == r]
        if exact:
            return exact[0]
        if len(cands) == 1:
            return cands[0]
        raise DeskError('That order changed in the sheet. Pull down to refresh, then try again.')

    def _need_live(self):
        if not self.live:
            if getattr(self.src, 'office', False):
                raise DeskError("Can't write to her sheet yet: it's an Excel file. Once she saves it as a Google "
                                "Sheet, payments go straight in.")
            raise DeskError("Can't write to her sheet yet: it isn't shared with the robot account.")
        if self.error:
            raise DeskError("Her sheet can't be read right now, so nothing is changed. Try again in a minute.")

    def _check_cols(self, x):
        """Her header row must still say what it said at the last read (a new column moves everything)."""
        if ml.tab_columns(self.src.row_values(x['tab'], x['hr'])) != x['cols']:
            self.checked = 0                                                     # read the sheet again soon
            raise DeskError("The sheet's columns changed. Pull down to refresh, then try again.")

    def _locate(self, x):
        """The row this order line is on now. Rows move when she inserts or sorts; then the same buyer (and item)
        must be found exactly once."""
        c, tab = x['cols'], x['tab']
        same = lambda row: (len(row) > c['user'] and ml.clean(row[c['user']]) == x['user'] and  # noqa: E731
                            (c['item'] is None or not x['item'] or
                             ml.clean(row[c['item']] if len(row) > c['item'] else '') == x['item']))
        if same(self.src.row_values(tab, x['r'])):
            return x['r']
        users = self.src.col_values(tab, c['user'])
        items = self.src.col_values(tab, c['item']) if c['item'] is not None and x['item'] else None
        hits = [i + 1 for i, u in enumerate(users) if ml.clean(u) == x['user'] and
                (items is None or ml.clean(items[i] if i < len(items) else '') == x['item'])]
        if len(hits) != 1:
            raise DeskError('The sheet changed. Pull down to refresh, then try again.')
        return hits[0]

    def _log(self, who, what, tab, r, user, detail, before, after):
        self.src.log([gs.stamp(), self.names.get(who, who), what, tab, r, user, detail,
                      '' if before is None else before, '' if after is None else after])

    def _reread(self, x, r):
        row = self.src.row_values(x['tab'], r)
        c = x['cols']
        get = lambda k: row[c[k]] if c.get(k) is not None and c[k] < len(row) else None  # noqa: E731
        paid, total, bal = ml.num(get('pay')), ml.num(get('total')), ml.num(get('bal'))
        if bal is None and total is not None and paid is not None:
            bal = total - paid
        with self.lock:
            x.update({'r': r, 'paid': paid, 'balance': bal if bal is not None else x.get('balance')})
            if total is not None:
                x['total'] = total
        self.writes += 1
        self._changed()

    def pay(self, who, tab, r, user, amount, item=None, req=None):
        """Payment received: added to the line's Payment cell the way she writes them ("=500" → "=500+2650").
        `req` is a one-off id from the page: the same request twice (a second tap, a retry) is paid once."""
        try:
            amount = round(float(amount), 2)
        except (TypeError, ValueError):
            raise DeskError('Enter the amount received.') from None
        if not 0 < amount < 1_000_000:
            raise DeskError('Enter the amount received.')
        self._need_live()
        with self.wlock:
            if req and req in self._reqs:
                return self._reqs[req]
            x = self._find(tab, r, user, item)
            if x.get('shifted'):
                raise DeskError('This row is laid out differently. Change it in the sheet.')
            c = x['cols']
            if c.get('pay') is None:
                raise DeskError('This tab has no Payment column.')
            r = self._locate(x)
            self._check_cols(x)
            cur = self.src.cell(tab, c['pay'], r)
            amt = amount_text(amount)
            if isinstance(cur, str) and cur.startswith('='):
                nxt = f'{cur}+{amt}'
            elif isinstance(cur, (int, float)) and not isinstance(cur, bool) and cur:
                nxt = f'={amount_text(cur)}+{amt}'
            elif cur in ('', None, 0):
                nxt = float(amt) if '.' in amt else int(amt)
            elif ml.num(cur) is not None:
                nxt = f'={amount_text(ml.num(cur))}+{amt}'
            else:
                raise DeskError(f'The Payment cell has text in it ("{str(cur)[:24]}"). Change it in the sheet.')
            self._log(who, 'payment', tab, r, user, amt, cur, nxt)
            try:
                self.src.put(tab, c['pay'], r, nxt)
            except gs.GoogleError:
                try:                                    # it may have landed anyway (a timeout after Google saved it)
                    landed = norm_cell(self.src.cell(tab, c['pay'], r)) == norm_cell(nxt)
                except gs.GoogleError:
                    landed = False
                if not landed:
                    raise
            cid = self.store.change(who, 'pay', tab, r, user, x['item'], c['pay'], cur, nxt, {'amount': amount})
            warn = ''
            if c.get('bal') is not None:                 # a typed-in balance (no formula) is lowered here too
                try:
                    b = self.src.cell(tab, c['bal'], r)
                    if isinstance(b, (int, float)) and not isinstance(b, bool):
                        nb = round(b - amount, 2)
                        self._log(who, 'balance', tab, r, user, amt, b, nb)
                        self.src.put(tab, c['bal'], r, nb)
                        self.store.change(who, 'bal', tab, r, user, x['item'], c['bal'], b, nb, {'parent': cid})
                except gs.GoogleError:
                    warn = 'The payment is saved, but its Balance cell is typed in and could not be lowered. ' \
                           'Check it in the sheet.'
            try:
                self._reread(x, r)
            except gs.GoogleError:
                self.writes += 1
                self.checked = 0                         # the next read brings the new balance
            out = {'change': cid, 'paid': x.get('paid'), 'bal': x.get('balance'), 'r': r, 'warn': warn}
            if req:
                self._reqs[req] = out
                while len(self._reqs) > 300:
                    self._reqs.popitem(last=False)
        self.store.act(who, 'pay', f'{peso(amount)} from @{user.lstrip("@")} · {x["item"] or tab.strip()}',
                       {'k': f'{tab}|{r}', 'change': cid})
        self._changed()
        return out

    def undo(self, who, cid):
        rows = self.store.q('select * from changes where id = ?', (cid,))
        if not rows or rows[0]['kind'] != 'pay':
            raise DeskError('Nothing to undo.')
        ch = rows[0]
        if ch['undone_at']:
            raise DeskError('Already undone.')
        age = now_utc() - dt.datetime.fromisoformat(ch['at'])
        if age > dt.timedelta(minutes=settings.UNDO_MINUTES):
            raise DeskError('Too late to undo here. Change it in the sheet.')
        self._need_live()
        kids = self.store.q("select * from changes where kind = 'bal' and undone_at is null and "
                            "json_extract(extra, '$.parent') = ?", (cid,))
        with self.wlock:
            x = self._find(ch['tab'], ch['r'], ch['usr'], ch['item'])
            r = self._locate(x)
            self._check_cols(x)
            for c in [ch] + kids:
                before, after = json.loads(c['before']), json.loads(c['after'])
                now = self.src.cell(c['tab'], c['col'], r)
                if norm_cell(now) != norm_cell(after):
                    raise DeskError('That cell was changed since. Fix it in the sheet.')
            for c in [ch] + kids:
                before, after = json.loads(c['before']), json.loads(c['after'])
                self._log(who, 'undo', c['tab'], r, c['usr'], '', after, before)
                self.src.put(c['tab'], c['col'], r, '' if before is None else before)
                self.store.run('update changes set undone_at = ? where id = ?', (now_utc().isoformat(), c['id']))
            self._reread(x, r)
        amount = json.loads(ch['extra'] or '{}').get('amount')
        self.store.act(who, 'undo', f'Undid {peso(amount)} from @{ch["usr"].lstrip("@")}',
                       {'k': f'{ch["tab"]}|{r}'})
        self._changed()
        return {'paid': x.get('paid'), 'bal': x.get('balance')}

    def remind(self, who, tab, r, user, item=None):
        """A reminder went out: remembered here, and (robot account) noted on the username cell."""
        x = self._find(tab, r, user, item)
        when = now_utc().astimezone(PHT)
        if self.live and not self.error and not x.get('shifted'):
            with self.wlock:
                r = self._locate(x)
                self._check_cols(x)
                col = x['cols']['user']
                note = self.src.note_of(tab, col, r)
                nxt = (note + '\n' if note else '') + f'Reminded {when:%b} {when.day} (website)'
                self._log(who, 'reminder', tab, r, user, '', note, nxt)
                self.src.set_note(tab, col, r, nxt)
        self.store.change(who, 'remind', tab, r, user, x['item'], None, None, None)
        self.store.act(who, 'remind', f'Reminded @{user.lstrip("@")} · {x["item"] or tab.strip()}',
                       {'k': f'{tab}|{r}'})
        self._changed()
        return {'reminded': now_utc().isoformat(timespec='seconds')}

    def edit(self, who, tab, r, user, field, value, item=None):
        if field not in EDITABLE:
            raise DeskError('That field can only be changed in the sheet.')
        self._need_live()
        value = ml.clean(value)
        if field == 'due' and value and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise DeskError('Pick a date.')
        with self.wlock:
            x = self._find(tab, r, user, item)
            col = x['cols'].get(EDITABLE[field])
            if col is None or x.get('shifted'):
                raise DeskError('That field can only be changed in the sheet.')
            r = self._locate(x)
            self._check_cols(x)
            cur = self.src.cell(tab, col, r)
            if isinstance(cur, str) and cur.startswith('='):
                raise DeskError('That cell has a formula. Change it in the sheet.')
            self._log(who, 'edit ' + field, tab, r, user, '', cur, value)
            self.src.put(tab, col, r, value, raw=field != 'due')
            self.store.change(who, 'edit', tab, r, user, x['item'], col, cur, value, {'field': field})
            with self.lock:
                if field == 'due':
                    x['due'], x['year_guessed'] = ml.parse_due(value)
                    x['due_text'] = ''
                    x['near'] = x['due'] or x.get('near')
                else:
                    x[{'courier': 'courier'}.get(field, field)] = value
            self.writes += 1
        label = {'due': 'due date', 'status': 'status', 'courier': 'courier', 'note': 'note'}[field]
        self.store.act(who, 'edit', f'@{user.lstrip("@")} {label}: {value or "cleared"}', {'k': f'{tab}|{r}'})
        self._changed()
        return {'ok': True}

    def slot(self, who, r, raw, delta, taker=''):
        """A stock slot taken (+1) or freed (-1) in the "ONHAND items" tab. Her formula works out what's left."""
        self._need_live()
        delta = 1 if int(delta) > 0 else -1
        with self.wlock:
            with self.lock:
                it = next((i for i in self.items if i['r'] == r and i['item'] == raw), None)
            if it is None or it['cols'].get('taken') is None:
                raise DeskError('That item moved. Pull down to refresh.')
            tab, cols = ml.STOCK_TAB, it['cols']
            if ml.clean(self.src.cell(tab, cols['name'], r, 'UNFORMATTED_VALUE')) != raw or (
                    cols.get('title_r') and ml.clean(self.src.cell(tab, cols['taken'], cols['title_r'],
                                                                   'UNFORMATTED_VALUE')).lower() != 'slots taken'):
                self.checked = 0
                raise DeskError('The stock tab changed. Pull down to refresh.')
            cur = self.src.cell(tab, cols['taken'], r)
            if isinstance(cur, str) and cur.startswith('='):
                raise DeskError('That cell has a formula. Change it in the sheet.')
            if cur not in ('', None) and ml.num(cur) is None:
                raise DeskError(f'The "slots taken" cell has text in it ("{str(cur)[:24]}"). Change it in the sheet.')
            nxt = max(0, int(ml.num(cur) or 0) + delta)
            self._log(who, 'slot ' + ('taken' if delta > 0 else 'freed'), tab, r, '', raw, cur, nxt)
            self.src.put(tab, cols['taken'], r, nxt)
            taker = ml.clean(taker)
            if taker and delta > 0 and cols.get('takers') is not None:
                t = self.src.cell(tab, cols['takers'], r)
                nt = (f'{t}, ' if ml.clean(t) else '') + taker
                self._log(who, 'slot taker', tab, r, taker, raw, t, nt)
                self.src.put(tab, cols['takers'], r, nt, raw=True)
            with self.lock:
                it['slots_taken'] = nxt
                if it['slots_total'] is not None:
                    it['slots_left'] = it['slots_total'] - nxt
            self.writes += 1
        name = od.nice(raw)
        self.store.act(who, 'slot', (f'Slot taken · {name}' + (f' · {taker}' if taker else '')) if delta > 0
                       else f'Slot freed · {name}', {'k': f'stock|{r}'})
        self._changed()
        return {'taken': it['slots_taken'], 'left': it['slots_left']}
