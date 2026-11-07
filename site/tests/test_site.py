"""The website's server: reading her sheet, writing back safely, the content pages, logins.
Everything runs on a small made-up sheet (FakeSheet); nothing touches Google."""
import datetime as dt
import io
import json
import sys
from pathlib import Path

import openpyxl
import pytest

SERVER = Path(__file__).resolve().parent.parent / 'server'
sys.path.insert(0, str(SERVER))

import auth  # noqa: E402
import settings  # noqa: E402
import content  # noqa: E402
import desk as desk_mod  # noqa: E402
import store as store_mod  # noqa: E402
from fake import FakeSheet  # noqa: E402

TODAY = dt.date(2026, 10, 14)


def sheet_bytes():
    """Her layout in miniature: a stock tab with formulas and a GO tab with every kind of Payment cell."""
    book = openpyxl.Workbook()
    st = book.active
    st.title = 'ONHAND items'
    for r in [
        [None, 'ENCHIN\nENHYPEN OFFICIAL CHARACTER\nUNNIEMART', None, None, None, None, None, 'Available slots',
         'Username of takers', 'slots taken', 'total available slots'],
        [None, 'Merch List', 'PAYO', '30 days after purchase', '60 days after purchase', 'DP'],
        [None, 'PLUSH KEYRING - WONCHU', 1580, '=C3+100', '=D3+100', 300, None, 5, '@buyer_a', 1, '=H3-J3'],
        [None, 'FACE CUSHION - WONCHU', 2550, '=C4+100', '=D4+100', 500, None, 1, '@buyer_c', 1, '=H4-J4'],
    ]:
        st.append(r)
    go = book.create_sheet('BTS Lightstick ')                   # her tab names can end in a space
    for r in [
        [None, 'Twitter username', 'Full Name', 'Item', 'Qty', 'Total', 'Payment', 'Balance', 'courier',
         'Deadline of Payment', 'Status'],
        [1, 'fan_formula', 'Juana Dela Cruz', 'BTS LS V4', 1, 3150, '=500', '=F2-G2', 'JNT', dt.datetime(2026, 10, 16), ''],
        [2, 'fan_number', 'Maria Santos', 'BTS LS V4', 1, 3150, 500, '=F3-G3', 'SDD', dt.datetime(2026, 10, 10), ''],
        [3, 'fan_empty', None, 'BTS LS V4', 1, 3150, None, '=F4-G4', 'SDD', 'OCT 30', ''],
        [4, 'fan_text', None, 'BTS LS V4', 1, 3150, 'see DM', 3150, 'SDD', 'OCT 30', ''],
        [5, 'fan_typed', None, 'BTS LS V4', 1, 3150, 500, 2650, 'SDD', 'OCT 30', ''],
        [6, 'fan_twice', None, 'BTS LS V4', 1, 3150, 500, '=F7-G7', 'SDD', 'OCT 30', ''],
        [7, 'fan_twice', None, 'BTS LS V4', 1, 3150, 500, '=F8-G8', 'SDD', 'OCT 30', ''],
        [8, 'fan_paid', None, 'BTS LS V4', 1, 3150, 3150, '=F9-G9', 'SDD', dt.datetime(2026, 9, 1), ''],
        [9, 'fan_multi', None, 'BTS LS V4', 1, 3150, 500, '=F10-G10', 'SDD', 'OCT 30', ''],
        [10, 'fan_multi', None, 'Photocard', 1, 820, 100, '=F11-G11', 'SDD', 'OCT 30', ''],
    ]:
        go.append(r)
    buf = io.BytesIO()
    book.save(buf)
    return buf.getvalue()


@pytest.fixture
def d(tmp_path, monkeypatch):
    monkeypatch.setattr(desk_mod, 'today_pht', lambda: TODAY)
    src = FakeSheet(sheet_bytes())
    dk = desk_mod.Desk(src, store_mod.Store(tmp_path / 'db.sqlite'), names={'owner': 'Her'})
    dk.tick(force=True)
    assert dk.error is None
    return dk


def line(dk, user):
    return next(x for x in dk.snapshot()['lines'] if x['user'] == user)


def pay_cell(dk, r):
    return dk.src.cell('BTS Lightstick ', 6, r)


def test_snapshot(d):
    s = d.snapshot()
    by = {x['user']: x for x in s['lines']}
    assert 'fan_paid' not in by                                          # fully paid: not owed
    assert by['fan_formula']['bucket'] == 'week' and by['fan_formula']['bal'] == 2650
    assert by['fan_number']['bucket'] == 'late'
    assert by['fan_formula']['go'] == 'BTS Lightstick' and by['fan_formula']['tab'] == 'BTS Lightstick '
    assert [x['bucket'] for x in s['lines']][:2] == ['late', 'week']   # most urgent first
    assert 'Juana' not in json.dumps(s)                                  # full names never leave the server
    assert by['fan_formula']['can'] == {'pay': True, 'due': True, 'status': True, 'courier': True, 'note': False}
    g = s['gos'][0]
    assert g['go'] == 'BTS Lightstick' and g['buyers'] == 8 and g['paid'] == 500 * 6 + 3150 + 100
    st = {i['item']: i for i in s['stock']}
    assert st['Plush Keyring - Wonchu']['left'] == 4 and st['Face Cushion - Wonchu']['left'] == 0


def test_pay_adds_to_her_formula_and_logs_first(d):
    x = line(d, 'fan_formula')
    out = d.pay('owner', x['tab'], x['r'], x['user'], 2650)
    assert pay_cell(d, 2) == '=500+2650' and out['bal'] == 0
    log = d.src.log_rows()
    assert log[0][1:9] == ['Her', 'payment', 'BTS Lightstick ', '2', 'fan_formula', '2650', '=500', '=500+2650']
    d.tick(force=True)
    assert 'fan_formula' not in [x['user'] for x in d.snapshot()['lines']]


def test_pay_number_empty_and_text_cells(d):
    for user, r, want in (('fan_number', 3, '=500+1000'), ('fan_empty', 4, 1000)):
        x = line(d, user)
        d.pay('owner', x['tab'], x['r'], user, 1000)
        assert pay_cell(d, r) == want
    x = line(d, 'fan_text')
    with pytest.raises(desk_mod.DeskError, match='text in it'):
        d.pay('owner', x['tab'], x['r'], 'fan_text', 1000)
    assert pay_cell(d, 5) == 'see DM'
    with pytest.raises(desk_mod.DeskError, match='amount'):
        d.pay('owner', x['tab'], x['r'], 'fan_number', 0)


def test_typed_balance_is_lowered_and_undo_puts_both_back(d):
    x = line(d, 'fan_typed')
    out = d.pay('owner', x['tab'], x['r'], 'fan_typed', 650.5)
    assert pay_cell(d, 6) == '=500+650.50' or pay_cell(d, 6) == '=500+650.5'
    assert d.src.cell('BTS Lightstick ', 7, 6) == 1999.5
    d.undo('owner', out['change'])
    assert pay_cell(d, 6) == 500 and d.src.cell('BTS Lightstick ', 7, 6) == 2650
    with pytest.raises(desk_mod.DeskError, match='Already'):
        d.undo('owner', out['change'])


def test_undo_refuses_when_someone_changed_the_cell(d):
    x = line(d, 'fan_formula')
    out = d.pay('owner', x['tab'], x['r'], 'fan_formula', 100)
    d.src.put('BTS Lightstick ', 6, 2, '=500+100+50')                   # she typed more in the sheet
    with pytest.raises(desk_mod.DeskError, match='changed since'):
        d.undo('owner', out['change'])
    assert pay_cell(d, 2) == '=500+100+50'


def test_rows_that_moved_are_found_again_or_refused(d):
    x = line(d, 'fan_number')
    tab = d.src.f['BTS Lightstick ']                                     # she inserts a row above everyone
    d.src.f['BTS Lightstick '] = {((r + 1) if r > 1 else r, c): v for (r, c), v in tab.items()}
    d.pay('owner', x['tab'], x['r'], 'fan_number', 100)
    assert d.src.cell('BTS Lightstick ', 6, 4) == '=500+100'           # now on row 4, not 3
    y = line(d, 'fan_twice')
    with pytest.raises(desk_mod.DeskError, match='sheet changed'):
        d.pay('owner', y['tab'], y['r'], 'fan_twice', 100)              # moved, and two rows look the same


def test_read_only_refuses_writes_but_remembers_reminders(d):
    d.src.can_write = False
    x = line(d, 'fan_number')
    with pytest.raises(desk_mod.DeskError, match="isn't shared"):
        d.pay('owner', x['tab'], x['r'], 'fan_number', 100)
    d.remind('owner', x['tab'], x['r'], 'fan_number')
    assert d.src.notes == {}
    assert line(d, 'fan_number')['reminded']


def test_remind_edit_and_slot(d):
    x = line(d, 'fan_number')
    d.remind('owner', x['tab'], x['r'], 'fan_number')
    assert d.src.notes[('BTS Lightstick ', 3, 1)].startswith('Reminded Oct')
    d.edit('owner', x['tab'], x['r'], 'fan_number', 'due', '2026-10-30')
    d.edit('owner', x['tab'], x['r'], 'fan_number', 'status', '=HACK()')
    assert d.src.cell('BTS Lightstick ', 9, 3) == '2026-10-30'
    assert d.src.cell('BTS Lightstick ', 10, 3) == "'=HACK()"            # text stays text
    y = line(d, 'fan_number')
    assert y['due'] == '2026-10-30' and y['bucket'] == 'soon'
    with pytest.raises(desk_mod.DeskError):
        d.edit('owner', x['tab'], x['r'], 'fan_number', 'total', '1')
    it = next(i for i in d.snapshot()['stock'] if i['item'] == 'Plush Keyring - Wonchu')
    out = d.slot('owner', it['r'], it['raw'], 1, '@new_fan')
    assert out == {'taken': 2, 'left': 3}
    assert d.src.cell('ONHAND items', 8, 3) == '@buyer_a, @new_fan'
    d.tick(force=True)
    assert next(i for i in d.snapshot()['stock'] if i['r'] == it['r'])['left'] == 3
    kinds = [a['kind'] for a in d.store.activity()]
    assert {'remind', 'edit', 'slot'} <= set(kinds)


def test_sheet_edits_show_up_in_history(d):
    d.src.put('BTS Lightstick ', 6, 3, '=500+1000')                    # she types a payment in the sheet
    d.checked = 0
    assert d.tick() is True
    assert d.store.activity()[0]['text'] == 'fan_number paid ₱1,000 · BTS LS V4'.replace('fan', '@fan')
    assert d.tick() is False                                             # nothing new: no download


def test_google_error_is_shown_not_raised(d):
    import google_sheet as gs
    d.src.fail = gs.GoogleError("the robot account can't open her sheet")
    d.tick(force=True)
    assert 'robot account' in d.snapshot()['sheet']['error']


class Drive:
    """Google's answers to the robot, for one file of the given type."""
    def __init__(self, mime):
        self.mime, self.calls = mime, []

    def request(self, method, url, timeout=None, params=None, **kw):
        self.calls.append((method, url.rsplit('/', 1)[-1], dict(params or {})))

        class R:
            status_code = 200
            content = b'PK the sheet'

            def json(r):
                return {'version': '7', 'modifiedTime': '2026-10-13T10:08:18Z', 'mimeType': self.mime}
        return R()


def test_an_excel_file_is_read_by_the_robot_but_not_written():
    import google_sheet as gs
    s = gs.Sheet('1gb6rxjHASqtglyr7hKbdMaZCt_TEST', session=Drive(gs.XLSX))
    assert s.export() == b'PK the sheet'                               # learns the type first, then downloads as is
    assert s.mode == 'read' and not s.can_write and s.office
    assert s.s.calls[-1][2] == {'alt': 'media', 'supportsAllDrives': 'true'}

    g = gs.Sheet('1gb6rxjHASqtglyr7hKbdMaZCt_TEST', session=Drive(gs.GSHEET))
    g.version()
    assert g.mode == 'live' and g.can_write
    g.export()
    assert g.s.calls[-1][1] == 'export'                                # a real Google Sheet is converted


def test_the_site_reads_an_excel_file_through_the_robot_and_says_why_it_cant_write(tmp_path):
    import google_sheet as gs
    key = tmp_path / 'key.json'
    key.write_text('{}')
    src = desk_mod.AutoSource('1gb6rxjHASqtglyr7hKbdMaZCt_TEST', key,
                              sheet=lambda sid, k: gs.Sheet(sid, session=Drive(gs.XLSX)))
    assert src.mode == 'read' and not src.can_write and 'Save as Google Sheets' in src.robot_error
    d = desk_mod.Desk(src, store_mod.Store(tmp_path / 'db'))
    with pytest.raises(desk_mod.DeskError, match='Excel file'):
        d._need_live()


# ---------- content ----------

BRIEF = """# Weekly brief · 2026-W43 (Oct 19 to Oct 25)

Draft for Andrey.

## This week (ranked)

### 1 · Army Bomb VER.4 ipon plan

Money · BTS Bulacan · fan questions: 1 (money) · sources: K3, [C52](https://example.com/c52)

- **Why:** Money is the top worry.
- **Facts to tick against the source:**
  - [ ] Prices. Source says: "₱3,150 paid in full" (K3)
  - [ ] Shows. Source says: "Mar 13, 14 and 16" ([C52](https://example.com/c52))
- **On screen, first 2 s:** Army Bomb VER.4 installment
- **Shot list:**
  1. First frame: planner
  2. End on the calendar
- **Caption (placeholder):** Army Bomb VER.4 #bts
- **Pinned comment (placeholder):** GO open po
- **Post:** Film and post Oct 20 to 22.
- **Needs:** Planner; Pen

## Waiting on stock

### · · Box from Korea Ep. 1

Proof · BTS Bulacan · fan questions: 0 · sources: K3

- **Why:** Shows the order is real.
- **Blocked because:** no stock yet
- **Needs:** The box itself

## Sources used

- **K3** (stock, 2026-10-14): BTS Army Bomb VER.4 · price ₱3,150
- **C52** (calendar, 2027-03-13): BTS in Bulacan [link](https://example.com/c52)
"""


def test_brief_parser():
    b = content.parse_brief(BRIEF, '2026-W43')
    assert b['range'] == 'Oct 19 to Oct 25' and len(b['ideas']) == 2
    i = b['ideas'][0]
    assert (i['n'], i['format'], i['season'], i['section']) == (1, 'Money', 'BTS Bulacan', 'main')
    assert i['hook'] == 'Army Bomb VER.4 installment' and i['shots'] == ['First frame: planner', 'End on the calendar']
    assert i['needs'] == ['Planner', 'Pen'] and i['post'].startswith('Film and post')
    assert i['facts'][1] == {'claim': 'Shows.', 'quote': 'Mar 13, 14 and 16', 'src': 'C52', 'url': 'https://example.com/c52'}
    assert i['sources'][0]['text'].startswith('BTS Army Bomb') and i['key'] == '2026-W43:army-bomb-ver-4-ipon-plan'
    w = b['ideas'][1]
    assert w['section'] == 'waiting' and w['n'] is None and w['blocked'] == 'no stock yet'


def test_docs_only_listed_files(tmp_path):
    (tmp_path / 'strategy').mkdir()
    (tmp_path / 'strategy' / 'STRATEGY.md').write_text('# The plan\n\nhi')
    (tmp_path / 'content' / 'drafts').mkdir(parents=True)
    (tmp_path / 'content' / 'drafts' / 'note.md').write_text('# Draft\n')
    assert [d['title'] for d in content.docs(tmp_path)] == ['The plan']
    assert len(content.docs(tmp_path, admin=True)) == 2
    assert content.doc('strategy/STRATEGY.md', tmp_path) == '# The plan\n\nhi'
    assert content.doc('../../etc/passwd', tmp_path) is None
    assert content.doc('content/drafts/note.md', tmp_path) is None             # drafts: Andrey only


# ---------- logins and the API ----------

def test_studio_numbers_come_from_her_summary(tmp_path):
    f = tmp_path / 'data' / 'owner' / 'studio' / 'summary.md'
    f.parent.mkdir(parents=True)
    f.write_text('TikTok Studio, account-wide, last 365 days (Oct 13, 2025 to Oct 12, 2026), screenshots shared by the '
                 'owner on 2026-10-14.\nTraffic source: Search 77.1%, For You 18.7%, Personal profile 2.8%, Following 1.4%.\n'
                 'Post views 309.7K, profile views 2.9K.\nViewer locations: Philippines 65.5%, United States 4.1%, other 30.4%.\n')
    s = content.studio(tmp_path)
    assert s['period'] == 'Oct 13, 2025 to Oct 12, 2026' and s['views'] == '309.7K' and s['shared'] == '2026-10-14'
    assert s['sources'][0] == {'name': 'Search', 'pct': 77.1} and len(s['sources']) == 4
    assert [p['name'] for p in s['places']] == ['Philippines', 'United States', 'other']
    assert content.studio(tmp_path / 'nothing') is None


def test_any_changed_file_updates_the_page(tmp_path):
    import os
    (tmp_path / 'strategy').mkdir()
    a, b = tmp_path / 'strategy' / 'plan.json', tmp_path / 'strategy' / 'STRATEGY.md'
    a.write_text('{}')
    b.write_text('# new')
    os.utime(a, (1_000_000, 1_000_000))
    before = content.watched(tmp_path)
    a.write_text('{"line": "x"}')
    os.utime(a, (1_000_000, 1_000_000))            # same old time (rsync keeps the laptop's), new size
    assert content.watched(tmp_path) != before


def test_passwords():
    h = auth.hash_password('abcd-efgh-jkmn')
    assert auth.check_password(' ABCD-efgh-jkmn ', h) and not auth.check_password('abcd-efgh-jkmx', h)
    users = {'andrey': {'hash': h}, 'owner': {'hash': auth.hash_password('pqrs-tuvw-xyz2')}}
    assert auth.who_is('pqrs-tuvw-xyz2', users) == 'owner' and auth.who_is('nope', users) is None
    t = auth.Throttle(limit=2, window=60)
    t.fail('1.2.3.4')
    t.fail('1.2.3.4')
    assert t.blocked('1.2.3.4') and not t.blocked('5.6.7.8')


def test_api(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    monkeypatch.setattr(settings, 'DB', tmp_path / 'db.sqlite')
    monkeypatch.setattr(settings, 'USERS', tmp_path / 'users.json')
    monkeypatch.setattr(desk_mod, 'today_pht', lambda: TODAY)
    (tmp_path / 'users.json').write_text(json.dumps({
        'andrey': {'name': 'Andrey', 'role': 'admin', 'hash': auth.hash_password('aaaa-bbbb-cccc')},
        'owner': {'name': 'Her', 'role': 'owner', 'hash': auth.hash_password('dddd-eeee-ffff')}}))
    import app as app_mod
    site = app_mod.Site(source=FakeSheet(sheet_bytes()))
    site.desk.tick(force=True)
    monkeypatch.setattr(app_mod, 'site', site)
    c = TestClient(app_mod.app)
    assert c.get('/api/state').status_code == 401
    assert c.post('/api/login', json={'password': 'wrong'}).status_code == 401
    r = c.post('/api/login', json={'password': 'dddd-eeee-ffff'})
    assert r.status_code == 200 and r.json()['me'] == {'id': 'owner', 'name': 'Her', 'admin': False}
    s = c.get('/api/state').json()
    assert 'robot' not in s['desk']['sheet']                                   # setup details: Andrey only
    x = next(l for l in s['desk']['lines'] if l['user'] == 'fan_number')
    body = {'tab': x['tab'], 'r': x['r'], 'user': x['user'], 'item': x['ri'], 'amount': 2650}
    assert c.post('/api/pay', json=[1], headers={'X-UM': '1'}).status_code == 400
    assert c.post('/api/pay', json={**body, 'r': 'x'}, headers={'X-UM': '1'}).status_code == 400
    assert c.post('/api/pay', json=body).status_code == 403                    # no X-UM header: refused
    assert c.post('/api/pay', json=body, headers={'X-UM': '1', 'Origin': 'https://evil.example'}).status_code == 403
    r = c.post('/api/pay', json=body, headers={'X-UM': '1'})
    assert r.status_code == 200 and r.json()['bal'] == 0
    r = c.post('/api/pay', json={**body, 'user': 'fan_text', 'r': 5}, headers={'X-UM': '1'})
    assert r.status_code == 409 and 'text in it' in r.json()['error']
    t = c.post('/api/tasks', json={'title': ' Film the clinic ', 'who': 'owner', 'due': '2026-10-21'},
               headers={'X-UM': '1'}).json()
    c.post(f'/api/tasks/{t["id"]}', json={'done': True}, headers={'X-UM': '1'})
    s = c.get('/api/state').json()
    assert s['tasks'][0]['title'] == 'Film the clinic' and s['tasks'][0]['done_by'] == 'owner'
    assert c.post('/api/idea', json={'key': 'w:x', 'status': 'posted', 'shots': [0, 2]},
                  headers={'X-UM': '1'}).json()['shots'] == [0, 2]
    p = c.get('/api/payments', params={'tab': x['tab'], 'r': x['r'], 'user': x['user'], 'item': x['ri']}).json()
    assert p['parts'] == [500, 2650]                                           # the cell was =500, then +2650
    assert c.post('/api/upload', content=b'x', headers={'X-UM': '1'}).status_code in (404, 405)   # no screenshots
    assert c.get('/api/doc', params={'id': 'automations/common.py'}).status_code == 404
    c.post('/api/logout', headers={'X-UM': '1'})
    assert c.get('/api/state').status_code == 401


def test_videos_and_stock_photos(tmp_path, monkeypatch):
    """Video covers and her videos are for signed-in devices only, can be skipped through, and nothing else in the
    folder can be read. Stock photos: pictures only, small, and gone from disk when removed."""
    from fastapi.testclient import TestClient
    media = tmp_path / 'content' / 'data' / 'media'
    (media / 't').mkdir(parents=True)
    (media / 'v').mkdir()
    (media / 't' / '111.webp').write_bytes(b'RIFF0000WEBPVP8 ')
    (media / 'v' / '111.mp4').write_bytes(b'0123456789' * 100)
    (media / 'index.json').write_text(json.dumps({
        '111': {'acc': 'unniemart_', 'mine': True, 'cap': 'Connecting engenebong', 'views': 225400,
                'thumb': 't/111.webp', 'video': 'v/111.mp4', 'color': '#334455'},
        '222': {'acc': 'unniemart_', 'fail': {'n': 1}}}))                      # no cover yet: not shown
    assert content.media(tmp_path / 'content') == {'111': {
        'acc': 'unniemart_', 'mine': True, 'cap': 'Connecting engenebong', 'views': 225400, 'thumb': 't/111.webp',
        'video': 'v/111.mp4', 'color': '#334455'}}
    for k, v in {'DB': tmp_path / 'db.sqlite', 'USERS': tmp_path / 'users.json', 'MEDIA': media,
                 'PHOTOS': tmp_path / 'photos'}.items():
        monkeypatch.setattr(settings, k, v)
    (tmp_path / 'users.json').write_text(json.dumps({
        'owner': {'name': 'Her', 'role': 'owner', 'hash': auth.hash_password('dddd-eeee-ffff')}}))
    import app as app_mod
    site = app_mod.Site(source=FakeSheet(sheet_bytes()))
    monkeypatch.setattr(app_mod, 'site', site)
    c = TestClient(app_mod.app)
    assert c.get('/media/t/111.webp').status_code == 401
    c.post('/api/login', json={'password': 'dddd-eeee-ffff'})
    r = c.get('/media/t/111.webp')
    assert r.status_code == 200 and 'immutable' in r.headers['cache-control']
    r = c.get('/media/v/111.mp4', headers={'Range': 'bytes=0-9'})
    assert r.status_code == 206 and r.content == b'0123456789'                 # the video can be skipped through
    assert c.get('/media/index.json').status_code == 404
    assert c.get('/media/..%2F..%2Fusers.json').status_code == 404

    key = 'enhypen|plush keyring - wonchu'
    jpeg = b'\xff\xd8\xff\xe0' + b'x' * 100
    assert c.post('/api/photo', params={'key': key}, content=jpeg).status_code == 403          # no X-UM header
    assert c.post('/api/photo', params={'key': key}, content=b'hello', headers={'X-UM': '1'}).status_code == 400
    big = b'\xff\xd8\xff' + b'x' * settings.PHOTO_MAX
    assert c.post('/api/photo', params={'key': key}, content=big, headers={'X-UM': '1'}).status_code == 413
    name = c.post('/api/photo', params={'key': key}, content=jpeg, headers={'X-UM': '1'}).json()['file']
    assert c.get('/api/state').json()['photos'] == {key: name}
    assert c.get(f'/photo/{name}').content == jpeg
    assert b'hash' not in c.get('/photo/..%2Fusers.json').content                 # the page, never the file
    second = c.post('/api/photo', params={'key': key}, content=jpeg + b'2', headers={'X-UM': '1'}).json()['file']
    assert not (tmp_path / 'photos' / name).exists() and (tmp_path / 'photos' / second).exists()   # old one gone
    c.post('/api/photo/remove', json={'key': key}, headers={'X-UM': '1'})
    assert c.get('/api/state').json()['photos'] == {} and not (tmp_path / 'photos' / second).exists()


# ---------- the review's cases (wrong line, moved columns, double taps, failures halfway) ----------

def test_the_same_buyer_with_two_orders_gets_the_right_one(d):
    lc = next(x for x in d.snapshot()['lines'] if x['user'] == 'fan_multi' and x['ri'] == 'Photocard')
    tab = d.src.f['BTS Lightstick ']                              # a row is inserted above both
    d.src.f['BTS Lightstick '] = {((r + 1) if r > 1 else r, c): v for (r, c), v in tab.items()}
    d.pay('owner', lc['tab'], lc['r'], 'fan_multi', 720, item='Photocard')
    assert d.src.cell('BTS Lightstick ', 6, 12) == '=100+720'          # Photocard, now row 12
    assert d.src.cell('BTS Lightstick ', 6, 11) == 500                 # the lightstick is untouched
    with pytest.raises(desk_mod.DeskError, match='changed'):
        d.pay('owner', lc['tab'], 99, 'fan_multi', 1)                  # no item, row gone: which one? refuse


def test_a_new_column_stops_writes_until_the_sheet_is_read_again(d):
    x = line(d, 'fan_number')
    t = d.src.f['BTS Lightstick ']                                # she inserts a column before Payment
    d.src.f['BTS Lightstick '] = {(r, c + 1 if c >= 6 else c): v for (r, c), v in t.items()}
    with pytest.raises(desk_mod.DeskError, match='columns changed'):
        d.pay('owner', x['tab'], x['r'], 'fan_number', 100, item=x['ri'])
    assert d.src.log_rows() == []                                      # nothing written, not even the log
    d.tick(force=True)
    x = line(d, 'fan_number')
    d.pay('owner', x['tab'], x['r'], 'fan_number', 100, item=x['ri'])
    assert d.src.cell('BTS Lightstick ', 7, 3) == '=500+100'


def test_a_second_tap_is_not_a_second_payment(d):
    x = line(d, 'fan_number')
    a = d.pay('owner', x['tab'], x['r'], 'fan_number', 100, item=x['ri'], req='tap-1')
    b = d.pay('owner', x['tab'], x['r'], 'fan_number', 100, item=x['ri'], req='tap-1')
    assert a == b and pay_cell(d, 3) == '=500+100'


def test_failures_after_the_write_still_count_as_paid(d, monkeypatch):
    import google_sheet as gs
    x = line(d, 'fan_typed')
    real_put, calls = d.src.put, []

    def put(tab, col, row, value, raw=False):
        calls.append(col)
        real_put(tab, col, row, value, raw)
        if len(calls) == 1:
            raise gs.GoogleError('timeout')                    # Google saved it but the answer got lost
        raise gs.GoogleError('quota')                          # then the typed Balance can't be lowered
    monkeypatch.setattr(d.src, 'put', put)
    out = d.pay('owner', x['tab'], x['r'], 'fan_typed', 100, item=x['ri'], req='r1')
    assert pay_cell(d, 6) == '=500+100' and 'Balance' in out['warn'] and out['change']

    def broken(tab, col, row, value, raw=False):
        raise gs.GoogleError('quota')                          # nothing saved: say so
    monkeypatch.setattr(d.src, 'put', broken)
    y = line(d, 'fan_empty')
    with pytest.raises(gs.GoogleError):
        d.pay('owner', y['tab'], y['r'], 'fan_empty', 100, item=y['ri'])
    assert pay_cell(d, 4) == ''


def test_no_writes_while_the_sheet_cannot_be_read(d):
    import google_sheet as gs
    x = line(d, 'fan_number')
    d.src.fail = gs.GoogleError('Google said 500')
    d.tick(force=True)
    d.src.fail = None
    with pytest.raises(desk_mod.DeskError, match="can't be read"):
        d.pay('owner', x['tab'], x['r'], 'fan_number', 100, item=x['ri'])


def test_slot_with_text_is_left_alone(d):
    it = next(i for i in d.snapshot()['stock'] if i['item'] == 'Plush Keyring - Wonchu')
    d.src.put('ONHAND items', 9, it['r'], '1 + 1 hold')
    with pytest.raises(desk_mod.DeskError, match='text in it'):
        d.slot('owner', it['r'], it['raw'], 1)
    assert d.src.cell('ONHAND items', 9, it['r']) == '1 + 1 hold'


def test_undo_only_touches_its_own_balance(d):
    first = None
    for i in range(12):                                         # change ids 1..: parent 1 must not match parent 12
        x = line(d, 'fan_typed')
        out = d.pay('owner', x['tab'], x['r'], 'fan_typed', 1, item=x['ri'])
        first = first or out['change']
    kids = d.store.q("select id from changes where kind = 'bal' and json_extract(extra, '$.parent') = ?", (first,))
    assert len(kids) == 1
