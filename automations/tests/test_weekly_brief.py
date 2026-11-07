import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import weekly_brief as wb  # noqa: E402

SOURCES = {
    'C1': {'id': 'C1', 'kind': 'calendar', 'url': 'https://weverse.io/bts/notice/33579', 'date': '2026-06-12',
           'text': '2026-06-12 to 2027-03-16 · BTS · Armybomb VER.4-only concert sync in effect, Bulacan Mar 13, 14 and 16'},
    'Q1': {'id': 'Q1', 'kind': 'fan question (past)', 'url': '', 'date': '',
           'text': 'the app name “EN-official light stick ver. 2” it this right? (type: setup: connect / app / battery)'},
    'K1': {'id': 'K1', 'kind': 'stock', 'url': '', 'date': '', 'text': 'BTS Army Bomb VER.4 · demo unit: planned'},
}
STOCK = [
    {'item': 'ENHYPEN Official Light Stick VER.2 (Engenebong)', 'demo_unit': 'yes', 'on_hand': 'unknown',
     'open_go': 'unknown', 'eta': ''},
    {'item': 'BTS Army Bomb VER.4', 'demo_unit': 'planned', 'on_hand': 'no', 'open_go': 'unknown',
     'eta': 'last week of October 2026'},
]
ACTIVE = ['BTS Bulacan', 'ENHYPEN Renewal']


def idea(**kw):
    base = {'title': 't', 'format': 'Clinic', 'season': 'BTS Bulacan', 'why': '', 'source_ids': ['C1'],
            'facts': [], 'item': 'none', 'needs_unit': False, 'sells': False, 'offer_keywords': [],
            'question_type': 'none', 'hook_on_screen': 'May VER.3 ka?', 'shot_list': ['VER.4 lights up'],
            'caption': 'Army Bomb VER.4 para sa Bulacan #armybombv4 #bts #kpopph', 'pinned_comment': '',
            'post_window': '', 'needs': []}
    base.update(kw)
    return base


def test_target_week_and_dates():
    assert wb.target_week(dt.date(2026, 10, 14))[0] == '2026-W43'       # Wednesday → next week
    assert wb.target_week(dt.date(2026, 10, 19))[0] == '2026-W43'       # Monday → this week
    assert wb._day('2026-10') == dt.date(2026, 10, 1)
    assert wb._day('2026-12', end=True) == dt.date(2026, 12, 31)
    assert wb.active_seasons(dt.date(2026, 10, 19)) == ['BTS Bulacan', 'ENHYPEN Renewal']
    assert 'BTS Bulacan' not in wb.active_seasons(dt.date(2027, 3, 17))


def test_calendar_window():
    rows = [{'date_start': '2026-10', 'date_end': ''}, {'date_start': '2026-12-12', 'date_end': ''},
            {'date_start': '2026-10-01', 'date_end': '2026-10-05'}, {'date_start': '2026-06-12', 'date_end': '2027-03-16'}]
    got = wb.calendar_rows(rows, dt.date(2026, 10, 14))
    assert rows[0] in got and rows[3] in got          # month-only and long-running events count
    assert rows[1] not in got and rows[2] not in got  # too far ahead / already over


def test_season_anchor_show_is_always_a_source():
    bulacan = {'date_start': '2027-03-13', 'date_end': '2027-03-16', 'event_type': 'concert'}
    other = {'date_start': '2027-03-13', 'date_end': '', 'event_type': 'concert'}
    assert wb.season_anchors([bulacan, other], dt.date(2026, 10, 14)) == [bulacan]
    assert wb.season_anchors([bulacan], dt.date(2027, 3, 17)) == []


def test_numbers_ignore_hashtags_and_single_digits():
    assert wb.numbers('Step 1 to 4 #armybombv4 #2027 ₱___ DP') == []
    assert wb.numbers('Bulacan Mar 13, ₱2,750 total') == ['13', '2750']


def test_clean_idea_is_ready():
    g = wb.gate(idea(facts=[{'claim': 'Only VER.4 syncs', 'source_id': 'C1', 'quote': 'Armybomb VER.4-only concert sync'}],
                     caption='Para sa Bulacan, Mar 13 #armybombv4'), SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'ready', g


def test_invented_quote_and_number_are_held():
    g = wb.gate(idea(facts=[{'claim': 'Old ones still light up', 'source_id': 'C1', 'quote': 'VER.3 still lights up'}]),
                SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'held' and 'quote not found' in g['problems'][0]
    g = wb.gate(idea(caption='Only 450 pesos DP for Bulacan'), SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'held' and '"450"' in g['problems'][0]


def test_quote_matching_ignores_quote_style_and_case():
    f = [{'claim': 'app name', 'source_id': 'Q1', 'quote': 'the app name "EN-official light stick ver. 2"'}]
    assert wb.gate(idea(source_ids=['Q1'], facts=f), SOURCES, STOCK, [], ACTIVE)['status'] == 'ready'


def test_slop_and_scarcity_are_held():
    g = wb.gate(idea(caption='Last 2 pcs! Stay till the end'), SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'held' and len(g['problems']) == 2
    g = wb.gate(idea(shot_list=['AI avatar explains the steps']), SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'held'


def test_unknown_source_drops_or_flags():
    assert wb.gate(idea(source_ids=['X9']), SOURCES, STOCK, [], ACTIVE)['status'] == 'dropped'
    g = wb.gate(idea(source_ids=['C1', 'X9']), SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'held' and 'X9' in g['problems'][0]


def test_repeat_offer_within_14_days():
    recent = [{'caption': 'Engenebong V2 on hand na po', 'date': '2026-10-10T00:00:00+00:00', 'url': 'u'}]
    g = wb.gate(idea(sells=True, offer_keywords=['engenebong']), SOURCES, STOCK, recent, ACTIVE)
    assert g['status'] == 'held' and 'same offer' in g['problems'][0]
    assert wb.gate(idea(sells=False, offer_keywords=['engenebong']), SOURCES, STOCK, recent, ACTIVE)['status'] == 'ready'


def test_stock_filter():
    g = wb.gate(idea(item='BTS Army Bomb VER.4', needs_unit=True), SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'waiting' and 'last week of October' in g['problems'][0]
    g = wb.gate(idea(item='ENHYPEN Official Light Stick VER.2 (Engenebong)', needs_unit=True, sells=True,
                     offer_keywords=['engenebong']), SOURCES, STOCK, [], ACTIVE)
    assert g['status'] == 'ready' and any('ask her' in w for w in g['warnings'])


def test_rank_order():
    q = {'setup: connect / app / battery': 3}
    a = idea(format='Money', season='none')
    b = idea(format='Clinic', season='BTS Bulacan')
    c = idea(format='Proof', season='BTS Bulacan', question_type='setup: connect / app / battery')
    keys = {n: wb.rank_key(i, SOURCES, q, ACTIVE)[0] for n, i in (('a', a), ('b', b), ('c', c))}
    assert sorted(keys, key=keys.get) == ['c', 'b', 'a']   # season first, then questions, then evidence


def test_full_render():
    inp = {'own': [], 'stats': {'question_types': {}}, 'tally': {}, 'stock': STOCK}
    ideas = [idea(title='Ready one', facts=[{'claim': 'VER.4 only', 'source_id': 'C1', 'quote': 'VER.4-only'}]),
             idea(title='Held one', caption='Last 2 pcs'),
             idea(title='Waiting one', item='BTS Army Bomb VER.4', needs_unit=True),
             idea(title='Dropped one', source_ids=['nope'])]
    sources = wb.check_all(ideas, list(SOURCES.values()), inp, dt.date(2026, 10, 14))
    md = wb.brief_md('2026-W43', dt.date(2026, 10, 19), dt.date(2026, 10, 25), ideas, sources, 'health',
                     wb.now_utc(), 'opus')
    assert '### 1 · Ready one' in md and '## Waiting on stock' in md and '## Blocked by the slop gate' in md
    assert '- Dropped one' in md and '**C1**' in md and '[ ] VER.4 only' in md
    assert '—' not in md


def test_repeat_check_ignores_hashtags():
    recent = [{'caption': 'Sino wala pang bag? #bts #armybomb', 'date': '2026-10-10T00:00:00+00:00', 'url': 'u'}]
    assert wb.gate(idea(sells=True, offer_keywords=['armybomb']), SOURCES, STOCK, recent, ACTIVE)['status'] == 'ready'


def test_new_run_never_overwrites_a_brief(tmp_path):
    assert wb.brief_name('2026-W43', tmp_path) == '2026-W43'
    (tmp_path / '2026-W43.md').write_text('[x] ticked')
    assert wb.brief_name('2026-W43', tmp_path) == '2026-W43-v2'
    (tmp_path / '2026-W43-v2.md').write_text('')
    assert wb.brief_name('2026-W43', tmp_path) == '2026-W43-v3'
