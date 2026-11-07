#!/usr/bin/env python3
"""Her masterlist through Google's own API, as the robot account (a Google "service account") she shared it with.

She shares the sheet with the robot's email as Editor, like adding a helper. Then:
  - the website (site/server) notices her edits within seconds and writes payments, reminders and slots back;
  - the laptop downloads the sheet while it's private (masterlist.py).
Every change the website makes is also written to a "Desk log" tab first, with the value before and after.

The robot's key is a private file: ~/.config/unniemart/google-key.json on the laptop and on the server (or the path in
UM_GOOGLE_KEY). Never commit or paste it.

Without the key (or before she shares the sheet) the site falls back to her share link: read-only (PublicLink).

Usage:
  python3 automations/google_sheet.py check     # can the robot read her sheet? prints its email if not
"""
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

import requests

try:
    from google.auth.exceptions import GoogleAuthError     # the robot's sign-in failing (key revoked, no network)
except ImportError:                                         # pragma: no cover
    GoogleAuthError = ()

KEY = Path(os.environ.get('UM_GOOGLE_KEY') or Path.home() / '.config' / 'unniemart' / 'google-key.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']
XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
GSHEET = 'application/vnd.google-apps.spreadsheet'
EXCEL_NOTE = ('her masterlist is an Excel file (.xlsx) in Google Drive. The robot reads it, but Google only lets it '
              'write to a Google Sheet: she opens it, File, Save as Google Sheets, and shares the new copy with the robot')
SHEETS = 'https://sheets.googleapis.com/v4/spreadsheets'
DRIVE = 'https://www.googleapis.com/drive/v3/files'
LOG_TAB = 'Desk log'
LOG_HEADER = ['When', 'Who', 'What', 'Tab', 'Row', 'Username', 'Amount or detail', 'Before', 'After']


class GoogleError(Exception):
    pass


def sheet_id(link):
    m = re.search(r'/d/([\w-]{20,})', link or '')
    return m.group(1) if m else None


def robot_email(key=KEY):
    try:
        return json.loads(Path(key).read_text()).get('client_email')
    except (OSError, ValueError):
        return None


def col_letter(i):
    """0 → A, 25 → Z, 26 → AA."""
    s, i = '', i + 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def a1(tab, col=None, row=None, col2=None, row2=None):
    """A range in A1 notation: a1(t, 2, 5) is C5, a1(t, 0, 5, None, 5) the whole row 5, a1(t, 2, None, 2) column C.
    Her tab names have spaces and trailing spaces; the quotes keep them exact."""
    def ref(c, r):
        return (col_letter(c) if c is not None else '') + (str(r) if r is not None else '')
    rng = ref(col, row)
    if col2 is not None or row2 is not None:
        rng += ':' + ref(col2, row2)
    return "'" + tab.replace("'", "''") + "'!" + rng


class Sheet:
    """One spreadsheet, read and written as the robot account.

    An Excel file (.xlsx) uploaded to Drive is read only: Google's Sheets API can't touch it. Then mode is 'read'
    (the robot still sees every edit within seconds, and still works after she makes the sheet Restricted)."""
    mode = 'live'
    can_write = True
    office = None              # True for an Excel file; known after the first version()

    def __init__(self, sid, key=KEY, session=None):
        if session is None:
            from google.auth.transport.requests import AuthorizedSession
            from google.oauth2 import service_account
            creds = service_account.Credentials.from_service_account_file(str(key), scopes=SCOPES)
            session = AuthorizedSession(creds)
        self.s = session
        self.id = sid
        self._tabs = None

    @property
    def url(self):
        return f'https://docs.google.com/spreadsheets/d/{self.id}/edit'

    def _req(self, method, url, **kw):
        try:
            r = self.s.request(method, url, timeout=kw.pop('timeout', 60), **kw)
        except requests.RequestException as e:
            raise GoogleError(f'could not reach Google ({type(e).__name__})') from e
        except GoogleAuthError as e:
            raise GoogleError(f'the robot account could not sign in ({type(e).__name__})') from e
        if r.status_code in (403, 404):
            raise GoogleError("the robot account can't open her sheet (is it shared with it as Editor?)")
        if r.status_code == 429:
            raise GoogleError('Google says too many requests; trying again shortly')
        if r.status_code >= 400:
            try:
                msg = r.json().get('error', {}).get('message', '')
            except ValueError:
                msg = r.text[:200]
            raise GoogleError(f'Google said {r.status_code}: {msg[:200]}')
        return r

    # ---- reading ----

    def version(self):
        """Changes whenever anyone edits the sheet. Cheap to ask."""
        j = self._req('GET', f'{DRIVE}/{self.id}', params={'fields': 'version,modifiedTime,mimeType',
                                                             'supportsAllDrives': 'true'}).json()
        self.office = j.get('mimeType', GSHEET) != GSHEET
        if self.office:
            self.mode, self.can_write = 'read', False
        return j.get('version'), j.get('modifiedTime')

    def export(self):
        """The whole sheet as .xlsx bytes. An Excel file is downloaded as it is; a Google Sheet is converted."""
        if self.office is None:
            self.version()
        if self.office:
            r = self._req('GET', f'{DRIVE}/{self.id}', params={'alt': 'media', 'supportsAllDrives': 'true'},
                          timeout=120)
        else:
            r = self._req('GET', f'{DRIVE}/{self.id}/export', params={'mimeType': XLSX}, timeout=120)
        if not r.content.startswith(b'PK'):
            raise GoogleError('Google sent something that is not a spreadsheet')
        return r.content

    def get(self, rng, render='FORMULA'):
        """Cell values in a range: FORMULA gives '=500+2650' for formulas, numbers as numbers, text as text."""
        j = self._req('GET', f'{SHEETS}/{self.id}/values/{requests.utils.quote(rng, safe="")}',
                      params={'valueRenderOption': render, 'dateTimeRenderOption': 'FORMATTED_STRING'}).json()
        return j.get('values', [])

    def cell(self, tab, col, row, render='FORMULA'):
        v = self.get(a1(tab, col, row), render)
        return v[0][0] if v and v[0] else ''

    def row_values(self, tab, row, render='UNFORMATTED_VALUE'):
        v = self.get(a1(tab, None, row, None, row), render)          # 'tab'!5:5, the whole row from column A
        return v[0] if v else []

    def col_values(self, tab, col, render='UNFORMATTED_VALUE'):
        return [r[0] if r else '' for r in self.get(a1(tab, col, None, col), render)]

    def forget_tabs(self):
        self._tabs = None

    def tabs(self):
        """{tab title: numeric id}. The id goes in links (#gid=) and in note updates. Read again after forget_tabs()
        (each time the whole sheet is read), so new, renamed or deleted tabs are noticed."""
        if self._tabs is None:
            j = self._req('GET', f'{SHEETS}/{self.id}', params={'fields': 'sheets.properties(sheetId,title)'}).json()
            self._tabs = {s['properties']['title']: s['properties']['sheetId'] for s in j.get('sheets', [])}
        return self._tabs

    def note_of(self, tab, col, row):
        j = self._req('GET', f'{SHEETS}/{self.id}', params={
            'ranges': a1(tab, col, row), 'fields': 'sheets.data.rowData.values.note'}).json()
        try:
            return j['sheets'][0]['data'][0]['rowData'][0]['values'][0].get('note', '')
        except (KeyError, IndexError):
            return ''

    # ---- writing ----

    def put(self, tab, col, row, value, raw=False):
        """One cell. raw=False types it like a person would (formulas and dates work); raw=True stores text as is."""
        self._req('PUT', f'{SHEETS}/{self.id}/values/{requests.utils.quote(a1(tab, col, row), safe="")}',
                  params={'valueInputOption': 'RAW' if raw else 'USER_ENTERED'},
                  json={'values': [[value]]})

    def set_note(self, tab, col, row, text):
        tid = self.tabs().get(tab)
        if tid is None:
            raise GoogleError(f'no tab called {tab}')
        self._req('POST', f'{SHEETS}/{self.id}:batchUpdate', json={'requests': [{'updateCells': {
            'range': {'sheetId': tid, 'startRowIndex': row - 1, 'endRowIndex': row,
                      'startColumnIndex': col, 'endColumnIndex': col + 1},
            'rows': [{'values': [{'note': text}]}], 'fields': 'note'}}]})

    def log(self, values):
        """One line in the "Desk log" tab (made the first time). Stored as plain text: '=500' stays readable."""
        if LOG_TAB not in self.tabs():
            self._req('POST', f'{SHEETS}/{self.id}:batchUpdate',
                      json={'requests': [{'addSheet': {'properties': {'title': LOG_TAB,
                                                                       'gridProperties': {'frozenRowCount': 1}}}}]})
            self._tabs = None
            self._append([LOG_HEADER])
        self._append([[str(v) if v is not None else '' for v in values]])

    def _append(self, rows):
        self._req('POST', f'{SHEETS}/{self.id}/values/{requests.utils.quote(a1(LOG_TAB, 0, 1), safe="")}:append',
                  params={'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS'}, json={'values': rows})


class PublicLink:
    """Read-only fallback: her share link ("anyone with the link"). No change signal, so it's polled."""
    mode = 'link'
    can_write = False

    def __init__(self, sid, get=requests.get):
        self.id = sid
        self._get = get

    @property
    def url(self):
        return f'https://docs.google.com/spreadsheets/d/{self.id}/edit'

    def version(self):
        return None, None

    def export(self):
        try:
            r = self._get(f'https://docs.google.com/spreadsheets/d/{self.id}/export?format=xlsx', timeout=120)
            r.raise_for_status()
        except requests.RequestException as e:
            raise GoogleError(f'download failed ({type(e).__name__})') from e
        if not r.content.startswith(b'PK'):
            raise GoogleError('Google sent a sign-in page, not the sheet (the share link is off and the robot '
                              'account is not set up)')
        return r.content

    def tabs(self):
        return {}

    def forget_tabs(self):
        pass


def connect(link, key=KEY):
    """The best way in: the robot account when its key is here, else the share link."""
    sid = sheet_id(link)
    if not sid:
        raise GoogleError('no sheet link')
    if Path(key).exists():
        return Sheet(sid, key)
    return PublicLink(sid)


def stamp(now=None):
    from common import PHT
    return (now or dt.datetime.now(dt.timezone.utc)).astimezone(PHT).strftime('%Y-%m-%d %H:%M:%S')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import masterlist
    if (argv or ['check'])[0] != 'check':
        print(__doc__)
        return 2
    if not KEY.exists():
        print(f'No robot key yet. Put the JSON key file at {KEY}.')
        return 1
    link = masterlist.SOURCE.read_text().strip() if masterlist.SOURCE.exists() else ''
    try:
        s = Sheet(sheet_id(link))
        v, at = s.version()
        if s.office:
            print(f'The robot account can read her sheet (version {v}, last edit {at}), but not write: {EXCEL_NOTE}.')
            return 1
        print(f'The robot account can read and write her sheet (version {v}, last edit {at}). {len(s.tabs())} tabs.')
        return 0
    except GoogleError as e:
        print(f'Not yet: {e}. Robot email to share the sheet with: {robot_email()}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
