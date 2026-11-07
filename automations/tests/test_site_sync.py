import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import site_sync as ss  # noqa: E402


def test_only_the_files_the_site_shows(tmp_path):
    for f in ['strategy/STRATEGY.md', 'content/ideas/2026-W43-v2.md', 'data/news/2026-10-14.json', 'data/calendar.csv',
              'data/owner/orders/orders-2026.xlsx', 'data/owner/orders/source.txt', 'data/owner/finance/x.csv',
              'data/state/news_seen.json', 'data/raw/scrape.json']:
        p = tmp_path / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('x')
    got = ss.files(tmp_path)
    assert got == ['strategy/STRATEGY.md', 'content/ideas/2026-W43-v2.md', 'data/news/2026-10-14.json', 'data/calendar.csv']
    assert not any('owner/orders' in f or 'finance' in f for f in got)          # her sheet never goes this way


def test_stale_only_after_six_hours(tmp_path):
    now = dt.datetime(2026, 10, 14, 12, 0, tzinfo=dt.timezone.utc)
    f = tmp_path / 's.json'
    assert ss.stale(f, now) is None
    f.write_text(json.dumps({'at': (now - dt.timedelta(hours=2)).isoformat()}))
    assert ss.stale(f, now) is None
    f.write_text(json.dumps({'at': (now - dt.timedelta(hours=7)).isoformat()}))
    assert round(ss.stale(f, now)) == 7
