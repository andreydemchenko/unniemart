import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import order_desk as od  # noqa: E402

TODAY = dt.date(2026, 10, 14)


def row(user, bal, due=None, near=None, total=3150, paid=500, names=(), r=5):
    return {'tab': 'BTS Lightstick ', 'r': r, 'user': user, 'item': 'BTS LS V4', 'qty': 1, 'total': total, 'paid': paid,
            'balance': bal, 'courier': 'JNT', 'status': '', 'due': due, 'near': near or due, 'year_guessed': False,
            'due_text': '', '_names': list(names)}


def test_buckets():
    d = lambda n: TODAY + dt.timedelta(days=n)  # noqa: E731
    b = od.buckets([row('a', 2650, d(1)), row('b', 2550, d(-29)), row('c', 100, d(-200)), row('d', 0, d(1)),
                    row('e', 500, d(20)), row('f', 500, d(90)), row('g', 900, None, near=d(-10)),
                    row('h', 900, None, near=d(-400))], TODAY)
    assert [x['user'] for x in b['week']] == ['a'] and [x['user'] for x in b['late']] == ['b']
    assert [x['user'] for x in b['soon']] == ['e'] and [x['user'] for x in b['later']] == ['f']
    assert [x['user'] for x in b['undated']] == ['g'] and {x['user'] for x in b['old']} == {'c', 'h'}
    assert 'd' not in {x['user'] for k in b for x in b[k]}       # nothing owed


def test_reminder_is_kind_and_has_no_buyer_data():
    late = od.reminder(row('fan', 2550, TODAY - dt.timedelta(days=29), names=['Secret Name']), TODAY)
    soon = od.reminder(row('fan', 2650, TODAY + dt.timedelta(days=1)), TODAY)
    assert '₱2,550' in late and 'Sep 15' in late and 'Secret' not in late
    assert 'due on Oct 15' in soon and 'GCash or Maya' in soon
    assert 'Thank you po for the ₱500 so far' in late and 'remaining balance of ₱2,550' in late   # paid part already
    fresh = od.reminder(row('fan', 3150, TODAY + dt.timedelta(days=3), paid=None), TODAY)
    assert 'so far' not in fresh and 'your balance of ₱3,150' in fresh
    for text in (late, soon):
        assert not any(w in text.lower() for w in ('forfeit', 'cancel', 'last chance', 'urgent'))


def test_nice_names():
    assert od.nice('PLUSH KEYRING - WONCHU') == 'Plush Keyring - Wonchu'
    assert od.nice('BTS LS V4') == 'BTS LS V4' and od.nice('Regular Set') == 'Regular Set'
    assert od.short('paid in full at order') == 'in full' and od.short('within 30 days') == '30 days'
    assert od.short('if paid by Oct 15') == 'by Oct 15'
