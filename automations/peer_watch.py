#!/usr/bin/env python3
"""Peer watch for Unnie Mart (strategy/AUTOMATION.md, section 4, Phase A).

Apify: the 10 newest videos of each peer shop in score_competitors.ACC. Flags videos at 5x or more of that shop's
normal (median views of its videos from the last 180 days), skipping videos under 3 days old (still growing) and
videos already flagged. History starts from the 1,038-video research scrape (data/competitor-videos.csv).

Writes data/peers/YYYY-Www.json (weekly_brief reads it) and data/peers/YYYY-Www.md.
An outlier is a format idea to look at, not something to copy: credit or re-film, never re-post.

Usage:
  python3 automations/peer_watch.py              # live, about $0.75 of Apify credit
  python3 automations/peer_watch.py --from-raw   # no spend: re-use the research scrape
"""
import argparse
import csv
import datetime as dt
import json
import re
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, PHT, STATE, load_json, now_utc, save_json  # noqa: E402
from score_competitors import ACC, classify  # noqa: E402

PEERS_DIR = DATA / 'peers'
RAW_DIR = DATA / 'raw' / 'weekly'
HISTORY = STATE / 'peer_videos.json'
FLAGGED = STATE / 'peer_flagged.json'
OUTLIER_X = 5.0
MIN_AGE_DAYS = 3
MAX_AGE_DAYS = 45       # only fresh outliers are news
NORMAL_DAYS = 180
# The shop itself; an off-niche food shop; dormant or closed accounts (notes in score_competitors.ACC).
SKIP = {'unniemart_', 'koppashop', 'iammist.k', 'chylcartz', 'pinkcardz', 'nabishoppe'}
NO_DOWNLOADS = {k: False for k in ('shouldDownloadVideos', 'shouldDownloadCovers', 'shouldDownloadSlideshowImages',
                                   'shouldDownloadAvatars', 'shouldDownloadMusicCovers')}


def _ts(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def peers():
    return [a for a in ACC if a not in SKIP]


def account_normal(videos, now, exclude_id=None):
    """Median views of the account's videos from the last NORMAL_DAYS (all of them if there are fewer than 5)."""
    recent = [v['views'] for v in videos if v['id'] != exclude_id and (now - _ts(v['date'])).days <= NORMAL_DAYS]
    if len(recent) < 5:
        recent = [v['views'] for v in videos if v['id'] != exclude_id]
    return st.median(recent) if recent else None


def load_history():
    hist = load_json(HISTORY, None)
    if hist is not None:
        return hist
    hist = {}
    with open(DATA / 'competitor-videos.csv') as f:
        for r in csv.DictReader(f):
            hist.setdefault(r['account'], {})[r['video_id']] = {
                'id': r['video_id'], 'date': r['created'] + 'T00:00:00+00:00', 'url': r['url'],
                'views': int(r['views']), 'likes': int(r['likes']), 'comments': int(r['comments']),
                'saves': int(r['saves'] or 0), 'caption': r['caption'], 'followers': r['followers']}
    return hist


def video_row(v):
    return {'id': str(v['id']), 'date': v['createTimeISO'], 'url': v['webVideoUrl'], 'views': v.get('playCount') or 0,
            'likes': v.get('diggCount') or 0, 'comments': v.get('commentCount') or 0,
            'saves': v.get('collectCount') or 0, 'caption': (v.get('text') or '').strip()[:300],
            'followers': (v.get('authorMeta') or {}).get('fans'), 'pinned': bool(v.get('isPinned')),
            'slideshow': bool(v.get('isSlideshow')), 'duration_s': (v.get('videoMeta') or {}).get('duration')}


def fetch_live():
    import apify
    items = apify.run('clockworks/tiktok-profile-scraper',
                      {'profiles': peers(), 'resultsPerPage': 10, 'profileScrapeSections': ['videos'],
                       'profileSorting': 'latest', 'excludePinnedPosts': True, **NO_DOWNLOADS},
                      'peer_watch', max_usd=1.5)
    save_json(RAW_DIR / f"peers-{now_utc().astimezone(PHT):%Y-%m-%d}.json", items)
    return items


def fetch_raw():
    items = []
    for fn in ('prof_a.json', 'prof_b.json', 'prof_c.json'):
        items += json.loads((DATA / 'raw' / 'competitors' / fn).read_text())
    return [v for v in items if v['authorMeta']['name'] not in SKIP]


def analyse(items, hist, flagged, now):
    counts = {}
    for v in items:
        name = (v.get('authorMeta') or {}).get('name')
        if not name:
            continue
        counts[name] = counts.get(name, 0) + 1
        hist.setdefault(name, {})[str(v['id'])] = video_row(v)

    outliers, accounts = [], []
    for name in peers():
        vids = list(hist.get(name, {}).values())
        normal = account_normal(vids, now)
        newest = max((v['date'] for v in vids), default=None)
        accounts.append({'account': name, 'group': ACC[name][0], 'country': ACC[name][1],
                         'scraped_now': counts.get(name, 0), 'normal': normal,
                         'newest_post': newest[:10] if newest else None})
        for v in vids:
            age = (now - _ts(v['date'])).days
            if v.get('pinned') or not (MIN_AGE_DAYS <= age <= MAX_AGE_DAYS) or v['id'] in flagged:
                continue
            n = account_normal(vids, now, exclude_id=v['id'])
            if n and v['views'] >= OUTLIER_X * n:
                flagged[v['id']] = now.isoformat()
                outliers.append({'account': name, 'group': ACC[name][0], 'country': ACC[name][1], **v,
                                 'age_days': age, 'normal': n, 'x_normal': round(v['views'] / n, 1),
                                 'saves_per_view': round(v['saves'] / v['views'], 4) if v['views'] else 0,
                                 'format': classify(v['caption'], {'isSlideshow': v.get('slideshow')})})
    outliers.sort(key=lambda o: -o['x_normal'])
    return {'outliers': outliers, 'accounts': accounts}


def report_md(week, res, n_items, now, source):
    acc = res['accounts']
    quiet = [a['account'] for a in acc if a['scraped_now'] == 0]
    L = [f'# Peer watch · {week}', '',
         f"Made {now.astimezone(PHT):%Y-%m-%d %H:%M} PHT from {source}: {n_items} videos from "
         f"{len(acc) - len(quiet)} of {len(acc)} shops."
         + (f" No videos returned for: {', '.join(quiet)}." if quiet else ''), '',
         f'Outlier = {OUTLIER_X:g}x or more of that shop\'s normal (median of its last {NORMAL_DAYS} days), '
         f'{MIN_AGE_DAYS} to {MAX_AGE_DAYS} days old, not flagged before. A format to learn from, never a video to re-post.',
         '', f"## Outliers ({len(res['outliers'])})", '']
    if not res['outliers']:
        L.append('None this week.')
    else:
        L += ['| Shop | Posted | Views | vs normal | Saves | Format | Caption |', '|---|---|---|---|---|---|---|']
        for o in res['outliers']:
            cap = re.sub(r'\s+', ' ', o['caption'])[:80].replace('|', '/')
            L.append(f"| {o['account']} ({o['country']}) | [{_ts(o['date']):%b %d}]({o['url']}) | {o['views']:,} | "
                     f"{o['x_normal']}x | {o['saves_per_view'] * 100:.2f}% | {o['format']} | {cap} |")
    L += ['', '## Shops', '', '| Shop | Group | Videos this run | Normal | Newest post |', '|---|---|---|---|---|']
    L += [f"| {a['account']} | {a['group']} | {a['scraped_now']} | {a['normal'] or '-'} | {a['newest_post'] or '-'} |"
          for a in acc]
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Peer watch for Unnie Mart')
    ap.add_argument('--from-raw', action='store_true', help='use the research scrape (no Apify spend)')
    ap.add_argument('--dry-run', action='store_true', help='print the report; save nothing')
    a = ap.parse_args(argv)

    now = now_utc()
    items = fetch_raw() if a.from_raw else fetch_live()
    hist, flagged = load_history(), load_json(FLAGGED, {})
    res = analyse(items, hist, flagged, now)
    y, w, _ = now.astimezone(PHT).isocalendar()
    week = f'{y}-W{w:02d}'
    source = 'the research scrape (--from-raw)' if a.from_raw else 'a live Apify scrape'
    md = report_md(week, res, len(items), now, source)
    if a.dry_run:
        print(md)
        return 0
    save_json(HISTORY, hist)
    save_json(FLAGGED, flagged)
    save_json(PEERS_DIR / f'{week}.json', {'week': week, 'made_at': now.isoformat(), 'source': source,
                                           'videos': len(items), **res})
    (PEERS_DIR / f'{week}.md').write_text(md)
    print(f"{week}: {len(items)} videos, {len(res['outliers'])} outliers · data/peers/{week}.md")
    return 0


if __name__ == '__main__':
    sys.exit(main())
