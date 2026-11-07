"""A stand-in for her Google Sheet, for tests and for trying the site on the laptop without touching her sheet.

Loads a .xlsx (formulas and values), answers like google_sheet.Sheet, and keeps every write in memory. Simple
formulas (+ - and cell references, like her "=500+2650" and "=I5-J5") are worked out so balances move like they do
in Google Sheets.
"""
import io
import re

import settings  # noqa: F401
import google_sheet as gs

REF = re.compile(r'\$?([A-Z]{1,3})\$?(\d+)')


def col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


class FakeSheet:
    mode = 'live'
    can_write = True
    url = 'https://docs.google.com/spreadsheets/d/FAKE/edit'

    def __init__(self, path_or_bytes):
        import openpyxl
        data = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, 'rb').read()
        wf = openpyxl.load_workbook(io.BytesIO(data), data_only=False)
        wv = openpyxl.load_workbook(io.BytesIO(data), data_only=True)
        self.order = wf.sheetnames
        self.f, self.v, self.notes, self.v_no = {}, {}, {}, 1
        for ws in wf.worksheets:
            cells = {}
            for row in ws.iter_rows():
                for c in row:
                    if c.value is not None:
                        cells[(c.row, c.column - 1)] = c.value
            self.f[ws.title] = cells
            vals = {}
            for row in wv[ws.title].iter_rows():
                for c in row:
                    if c.value is not None:
                        vals[(c.row, c.column - 1)] = c.value
            self.v[ws.title] = vals
        self.fail = None                      # set to a GoogleError to make every call fail (tests)

    def _check(self):
        if self.fail:
            raise self.fail

    # ---- formulas ----

    def _eval(self, tab, formula, depth=0):
        expr = formula.lstrip('=').replace(' ', '')
        if depth > 20 or not re.fullmatch(r'[A-Z0-9.$+\-()]+', expr):
            return None
        def sub(m):
            v = self.value(tab, col_index(m.group(1)), int(m.group(2)), depth + 1)
            return str(v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0)
        try:
            return eval(REF.sub(sub, expr), {'__builtins__': {}})          # digits, + - ( ) only
        except Exception:                                                   # noqa: BLE001
            return None

    def value(self, tab, col, row, depth=0):
        f = self.f[tab].get((row, col))
        if isinstance(f, str) and f.startswith('='):
            got = self._eval(tab, f, depth)
            return got if got is not None else self.v[tab].get((row, col))
        return f

    # ---- the google_sheet.Sheet interface ----

    def version(self):
        self._check()
        return str(self.v_no), None

    def export(self):
        self._check()
        import openpyxl
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        for tab in self.order:
            ws = wb.create_sheet(tab)
            for (r, c) in self.f[tab]:
                v = self.value(tab, c, r)
                ws.cell(r, c + 1, v)
        buf = io.BytesIO()
        wb.save(buf)
        return buf.getvalue()

    def tabs(self):
        return {t: 1000 + i for i, t in enumerate(self.order)}

    def forget_tabs(self):
        pass

    def cell(self, tab, col, row, render='FORMULA'):
        self._check()
        if render == 'FORMULA':
            v = self.f[tab].get((row, col), '')
        else:
            v = self.value(tab, col, row)
        if hasattr(v, 'isoformat'):
            v = f'{v:%m/%d/%Y}'
        return '' if v is None else v

    def row_values(self, tab, row, render='UNFORMATTED_VALUE'):
        self._check()
        cols = [c for (r, c) in self.f[tab] if r == row]
        return [self.cell(tab, c, row, render) for c in range(max(cols) + 1)] if cols else []

    def col_values(self, tab, col, render='UNFORMATTED_VALUE'):
        self._check()
        rows = [r for (r, c) in self.f[tab] if c == col]
        return [self.cell(tab, col, r, render) for r in range(1, max(rows) + 1)] if rows else []

    def put(self, tab, col, row, value, raw=False):
        self._check()
        if value == '' or value is None:
            self.f[tab].pop((row, col), None)
        elif raw and isinstance(value, str) and value.startswith('='):
            self.f[tab][(row, col)] = "'" + value
        else:
            self.f[tab][(row, col)] = value
        self.v_no += 1

    def note_of(self, tab, col, row):
        return self.notes.get((tab, row, col), '')

    def set_note(self, tab, col, row, text):
        self._check()
        self.notes[(tab, row, col)] = text
        self.v_no += 1

    def log(self, values):
        self._check()
        if gs.LOG_TAB not in self.f:
            self.order.append(gs.LOG_TAB)
            self.f[gs.LOG_TAB], self.v[gs.LOG_TAB] = {}, {}
            for i, h in enumerate(gs.LOG_HEADER):
                self.f[gs.LOG_TAB][(1, i)] = h
        n = max(r for (r, c) in self.f[gs.LOG_TAB]) + 1
        for i, v in enumerate(values):
            self.f[gs.LOG_TAB][(n, i)] = str(v)
        self.v_no += 1

    def log_rows(self):
        t = self.f.get(gs.LOG_TAB, {})
        n = max((r for (r, c) in t), default=0)
        return [[t.get((r, c), '') for c in range(len(gs.LOG_HEADER))] for r in range(2, n + 1)]
