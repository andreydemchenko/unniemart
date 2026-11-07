import datetime as dt
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import masterlist as ml  # noqa: E402
import weekly_brief as wb  # noqa: E402

TODAY = dt.date(2026, 10, 14)


def make_sheet(path):
    """A tiny copy of her layout, with made-up buyers."""
    book = openpyxl.Workbook()
    st = book.active
    st.title = 'ONHAND items'
    for r in [
        [None, 'ENCHIN\nENHYPEN OFFICIAL CHARACTER\nUNNIEMART', None, None, None, None, None, 'Available slots',
         'Username of takers', 'slots taken', 'total available slots'],
        [None, 'Merch List', 'PAYO', '30 days after purchase', '60 days after purchase', 'DP'],
        [None, 'PLUSH KEYRING - WONCHU', 1580, 1680, 1780, 300, None, 5, '@buyer_a', 1, 4],
        [None, 'PLUSH KEYRING - JAKEY', None, None, None, None, None, 7, '@buyer_b', 1, 6],
        [None, 'FACE CUSHION - WONCHU', 2550, 2650, 2750, 500, None, 1, '@buyer_c', 1, 0],
        [None, 'ENHYPEN THE SIN : BLISS\nUNNIEMART'],
        [None, 'ALBUM', 'PAYO', dt.datetime(2026, 10, 15), dt.datetime(2026, 11, 15), 'DP'],
        [None, 'Weverse Shop with POB'],
        [None, 'Vinyl', 2350, 2450, 2550, 300],
    ]:
        st.append(r)
    go = book.create_sheet('BTS Lightstick')
    for r in [
        [None, 'Twitter username', None, 'Full Name', 'Address', 'Contact #', 'Item', 'Qty', 'Total', 'Payment',
         'Balance', 'courier', 'Deadline of Payment', 'Remarks'],
        [1, '@old_row', None, None, None, None, 2500, 300, 2200, 'J&T', 45016],       # shifted 2023 row
        [2, 'fan_one', None, 'Juana Dela Cruz', 'secret', '0900', 'BTS LS V4', 1, 3150, 500, 2650, 'JNT',
         dt.datetime(2026, 8, 15), 'Sept release'],
        [3, 'fan_two', None, 'Maria Santos', 'secret', '0900', 'BTS LS V4', 1, 3150, 500, 2650, 'SDD', 'OCT 15'],
        [4, 'fan_three', None, None, None, None, 'BTS LS V4', 1, 3050, 500, 2550, 'SDD', 'SEPT 15'],
        [5, 'fan_four', None, None, None, None, 'BTS LS V4', 1, 3150, 500, 2650, 'SDD', 'OCT 15', 'cancelled'],
        [6, 'fan_five', None, None, None, None, 'BTS LS V4', 1, 3150, None, 3150, 'SDD', 'OCT 15'],
        [7, 'fan_six', None, None, None, None, 'BTS LS V4', 1, 2950, 2950, 0, 'SDD', 'PAYO/AUG 15'],
    ]:
        go.append(r)
    book.save(path)
    return path


def test_stock_tab(tmp_path):
    book = ml.open_sheet(make_sheet(tmp_path / 's.xlsx'))
    items = ml.stock_items(book['ONHAND items'])
    names = [i['item'] for i in items]
    assert names == ['PLUSH KEYRING - WONCHU', 'PLUSH KEYRING - JAKEY', 'Vinyl']   # sold-out cushion left out
    jakey = items[1]
    assert jakey['price_carried'] and jakey['prices'][0] == ('paid in full at order', 1580) and jakey['slots_left'] == 6
    vinyl = items[2]
    assert vinyl['sub'] == 'Weverse Shop with POB' and vinyl['section'] == 'ENHYPEN THE SIN : BLISS'
    assert ml.price_text(vinyl) == ('₱2,350 paid in full at order; ₱2,450 if paid by Oct 15; ₱2,550 if paid by '
                                    'Nov 15; down payment ₱300')
    assert '@buyer' not in repr(items)                      # who took the slots never leaves the module


def test_order_tab(tmp_path):
    book = ml.open_sheet(make_sheet(tmp_path / 's.xlsx'))
    rows = {x['user']: x for x in ml.all_orders(book, TODAY)}
    assert 'fan_four' not in rows                           # cancelled
    assert rows['@old_row']['balance'] == 2200 and rows['@old_row']['due'] == dt.date(2023, 3, 31)
    assert rows['fan_two']['due'] == dt.date(2026, 10, 15) and not rows['fan_two']['year_guessed']
    assert rows['fan_three']['due'] == dt.date(2026, 9, 15)
    assert rows['fan_five']['balance'] == 3150 and rows['fan_five']['paid'] is None
    assert rows['fan_six']['balance'] == 0
    assert rows['fan_one']['_names'] == ['Juana Dela Cruz']
    assert rows['@old_row']['r'] == 2 and rows['fan_two']['r'] == 4      # row numbers in her sheet
    assert not any('secret' in repr({k: v for k, v in x.items() if k != '_names'}) for x in rows.values())


def test_parse_due():
    assert ml.parse_due('PAYO / Aug 15', 2026) == (dt.date(2026, 8, 15), False)
    assert ml.parse_due('Sept 31', 2026) == (dt.date(2026, 9, 30), False)
    assert ml.parse_due('June 30', None, TODAY) == (dt.date(2026, 6, 30), True)
    assert ml.parse_due('Jan 15', None, TODAY) == (dt.date(2027, 1, 15), True)
    assert ml.parse_due('Payo', 2026) == (None, False)
    assert ml.parse_due(45016) == (dt.date(2023, 3, 31), False)


def test_fetch_keeps_old_copy_on_sign_in_page(tmp_path):
    src, dest = tmp_path / 'source.txt', tmp_path / 'sheet.xlsx'
    dest.write_bytes(b'PK old')
    src.write_text('https://docs.google.com/spreadsheets/d/1gb6rxjHASqtglyr7hKbdMaZCt_TEST/edit')
    nokey = tmp_path / 'no-key.json'

    class R:
        def __init__(self, content):
            self.content = content

        def raise_for_status(self):
            pass
    ok, msg = ml.fetch(dest, src, get=lambda url, timeout: R(b'<html>Sign in</html>'), key=nokey)
    assert not ok and 'sign-in' in msg and dest.read_bytes() == b'PK old'
    ok, _ = ml.fetch(dest, src, get=lambda url, timeout: R(b'PK new'), key=nokey)
    assert ok and dest.read_bytes() == b'PK new'
    assert ml.fetch(dest, tmp_path / 'missing.txt', key=nokey)[0] is False


def test_fetch_as_the_robot_account(tmp_path, monkeypatch):
    import google_sheet as gs
    src, dest, key = tmp_path / 'source.txt', tmp_path / 'sheet.xlsx', tmp_path / 'key.json'
    src.write_text('https://docs.google.com/spreadsheets/d/1gb6rxjHASqtglyr7hKbdMaZCt_TEST/edit')
    key.write_text('{}')
    seen = []

    class Robot:
        def __init__(self, sid, k):
            seen.append(sid)

        def export(self):
            return b'PK from the robot'
    monkeypatch.setattr(gs, 'Sheet', Robot)
    ok, msg = ml.fetch(dest, src, get=None, key=key)
    assert ok and 'robot account' in msg and dest.read_bytes() == b'PK from the robot'
    assert seen == ['1gb6rxjHASqtglyr7hKbdMaZCt_TEST']

    class Broken(Robot):
        def export(self):
            raise gs.GoogleError("the robot account can't open her sheet")

    class R:
        content = b'PK via link'

        def raise_for_status(self):
            pass
    monkeypatch.setattr(gs, 'Sheet', Broken)                      # not shared yet → the share link, and says why
    ok, msg = ml.fetch(dest, src, get=lambda url, timeout: R(), key=key)
    assert ok and msg.startswith("robot account: the robot account can't open") and dest.read_bytes() == b'PK via link'


def test_sheet_stock_becomes_brief_sources(tmp_path):
    rows = wb.sheet_stock(make_sheet(tmp_path / 's.xlsx'))
    assert rows[0]['item'] == 'ENCHIN ENHYPEN OFFICIAL CHARACTER · PLUSH KEYRING - WONCHU'
    assert rows[0]['on_hand'] == 'yes' and rows[2]['on_hand'] == 'unknown' and rows[2]['open_go'] == 'yes'
    assert '4 of 5 slots left' in rows[0]['price_note']
    # a price from her sheet may be written in a caption; one that isn't there is still blocked
    sources = {'K1': {'id': 'K1', 'kind': 'stock', 'url': '', 'date': '', 'text': rows[0]['price_note']}}
    base = {'title': 't', 'format': 'Money', 'season': 'none', 'why': '', 'source_ids': ['K1'], 'facts': [],
            'item': rows[0]['item'], 'needs_unit': False, 'sells': False, 'offer_keywords': [],
            'question_type': 'none', 'hook_on_screen': '', 'shot_list': [], 'pinned_comment': '', 'post_window': '',
            'needs': []}
    ok = wb.gate({**base, 'caption': 'Wonchu plush keyring ₱1,580 #enhypen #enchin #kpopph'}, sources, rows, [], [])
    bad = wb.gate({**base, 'caption': 'Wonchu plush keyring ₱1,499 #enhypen #enchin #kpopph'}, sources, rows, [], [])
    assert ok['status'] == 'ready' and bad['status'] == 'held'
    assert wb.sheet_stock(tmp_path / 'none.xlsx') == []
