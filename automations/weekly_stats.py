#!/usr/bin/env python3
"""Weekly stats for Unnie Mart (strategy/AUTOMATION.md, section 4, Phase A).

Apify: the shop's 30 latest TikToks, comments on the 10 latest, the latest X posts. Each video is compared with the
account's normal (median views of the 21 posts around it in time, as in STRATEGY.md), and the scoreboard is checked
against the starting point and targets in STRATEGY.md section 11.

Writes data/stats/YYYY-Www.json (weekly_brief reads it) and data/stats/YYYY-Www.md (for people).
Fan comments are kept as text only: no usernames in the output.

Usage:
  python3 automations/weekly_stats.py              # live, about $0.15 to 0.30 of Apify credit
  python3 automations/weekly_stats.py --from-raw   # no spend: re-use the 2026-10-14 research scrape
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
from score_competitors import classify  # noqa: E402

HANDLE = 'unniemart_'
STATS_DIR = DATA / 'stats'
RAW_DIR = DATA / 'raw' / 'weekly'
HISTORY = STATE / 'own_videos.json'
COMMENTS_SEEN = STATE / 'comments_seen.json'
NO_DOWNLOADS = {k: False for k in ('shouldDownloadVideos', 'shouldDownloadCovers', 'shouldDownloadSlideshowImages',
                                   'shouldDownloadAvatars', 'shouldDownloadMusicCovers')}

# Starting point and targets: STRATEGY.md section 11 (research 01).
START = {'median_views_2026': 608, 'zero_comment_share': 0.53, 'saves_per_view': 0.0009, 'posts_90d': 7}
TARGET = {'posts_week': 3, 'clinic_x_normal': 2.0, 'clinic_saves': 0.0035, 'zero_comment_share': 0.40,
          'breakout_views': 10_000}
PLAN_START = dt.datetime(2026, 10, 14, tzinfo=PHT)

# Fan question types (research 01 and 04). First match wins.
QUESTION_TYPES = [
    ('stock: available pa?', r'avail|meron pa|may stock|in stock|on ?hand pa|sold out|may natira|pwede pa|\bmay \w+ pa\b'),
    ('setup: connect / app / battery', r'connect|\bapp\b|pair|bluetooth|batter|sync|ayaw|not working|gumagana|turn on'),
    ('trust: legit / fake', r'legit|scam|authentic|original|\bfake\b|official ba|totoo'),
    ('timing: will it arrive?', r'aabot|before the concert|kailan|\beta\b|arrive|darating|dating'),
    ('money: installment / DP', r'hulugan|install|\bdp\b|down ?payment|payo|\bdop\b|ipon'),
    ('price', r'how much|mag ?kano|\bhm\b|price|presyo'),
    ('how to order', r'how to order|pa(a)?no (mag)?order|order form|\bdm\b|link|saan (po )?(mag)?order'),
]


# ---------- pure helpers (tested) ----------

def iso_week(d):
    y, w, _ = d.isocalendar()
    return f'{y}-W{w:02d}'


def neighbour_normal(videos, i, window=21):
    """Median views of the `window` posts nearest in time to videos[i] (videos sorted oldest first)."""
    n = len(videos)
    half = window // 2
    lo = max(0, min(i - half, n - window))
    return st.median(v['views'] for v in videos[lo:lo + window])


def question_type(text):
    t = (text or '').lower()
    for name, pat in QUESTION_TYPES:
        if re.search(pat, t):
            return name
    return 'other question' if '?' in t else None


def is_clinic(caption):
    return classify(caption) == 'Lightstick tutorial'


# ---------- data ----------

def _ts(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def video_row(v):
    return {'id': str(v['id']), 'date': v['createTimeISO'], 'url': v['webVideoUrl'], 'views': v.get('playCount') or 0,
            'likes': v.get('diggCount') or 0, 'comments': v.get('commentCount') or 0,
            'shares': v.get('shareCount') or 0, 'saves': v.get('collectCount') or 0,
            'caption': (v.get('text') or '').strip(), 'pinned': bool(v.get('isPinned')),
            'slideshow': bool(v.get('isSlideshow')), 'shop_tag': bool(v.get('hasTikTokShopProduct')),
            'duration_s': (v.get('videoMeta') or {}).get('duration')}


def load_history():
    """Every known video, seeded once from data/own-videos.csv (the 396-video research table)."""
    hist = load_json(HISTORY, None)
    if hist is not None:
        return hist
    hist = {}
    with open(DATA / 'own-videos.csv') as f:
        for r in csv.DictReader(f):
            d = dt.datetime.strptime(r['date_pht'], '%Y-%m-%d %H:%M').replace(tzinfo=PHT)
            hist[r['video_id']] = {'id': r['video_id'], 'date': d.astimezone(dt.timezone.utc).isoformat(),
                                   'url': r['url'], 'views': int(r['views']), 'likes': int(r['likes']),
                                   'comments': int(r['comments']), 'shares': int(r['shares']),
                                   'saves': int(r['saves']), 'caption': r['caption'],
                                   'pinned': r['pinned'] == 'True', 'slideshow': r['slideshow'] == 'True',
                                   'shop_tag': r['tiktok_shop_product_tagged'] == 'True',
                                   'duration_s': float(r['duration_s'] or 0)}
    return hist


def fetch_live():
    import apify
    tt = apify.run('clockworks/tiktok-profile-scraper',
                   {'profiles': [HANDLE], 'resultsPerPage': 30, 'profileScrapeSections': ['videos'],
                    'profileSorting': 'latest', 'excludePinnedPosts': False, **NO_DOWNLOADS},
                   'weekly_stats: tiktok', max_usd=0.5)
    latest = sorted((v for v in tt if not v.get('isPinned')), key=lambda v: v['createTimeISO'], reverse=True)[:10]
    comments = apify.run('clockworks/tiktok-comments-scraper',
                         {'postURLs': [v['webVideoUrl'] for v in latest], 'commentsPerPost': 50,
                          'maxRepliesPerComment': 0}, 'weekly_stats: comments', max_usd=0.5) if latest else []
    try:
        x = apify.run('apidojo/tweet-scraper', {'twitterHandles': [HANDLE], 'maxItems': 20, 'sort': 'Latest'},
                      'weekly_stats: x', max_usd=0.2)
    except Exception as e:  # noqa: BLE001  (X is a nice-to-have; TikTok numbers still matter)
        print(f'X scrape failed: {e}', file=sys.stderr)
        x = []
    stamp = now_utc().astimezone(PHT).strftime('%Y-%m-%d')
    for name, obj in (('tiktok', tt), ('comments', comments), ('x', x)):
        save_json(RAW_DIR / f'{name}-{stamp}.json', obj)
    return tt, comments, x


def fetch_raw():
    raw = DATA / 'raw'
    tt = json.loads((raw / 'tiktok-latest-2026-10-14.json').read_text())
    urls = {v['webVideoUrl'] for v in tt}
    comments = [c for c in json.loads((raw / 'comments-2026-10-14.json').read_text())
                if (c.get('videoWebUrl') or c.get('submittedVideoUrl')) in urls]
    x = json.loads((raw / 'x-posts-2026-10-14.json').read_text())
    return tt, comments, x


# ---------- analysis ----------

def analyse(tt, comments, x, hist, seen_cids, now):
    fresh = [video_row(v) for v in tt]
    for r in fresh:
        hist[r['id']] = {**hist.get(r['id'], {}), **r, 'updated': now.isoformat()}

    allv = sorted((v for v in hist.values() if not v.get('pinned')), key=lambda v: v['date'])
    pos = {v['id']: i for i, v in enumerate(allv)}
    fresh_ids = {r['id'] for r in fresh}
    videos = []
    for v in sorted((hist[i] for i in fresh_ids), key=lambda v: v['date'], reverse=True):
        age = (now - _ts(v['date'])).days
        normal = neighbour_normal(allv, pos[v['id']]) if v['id'] in pos else None
        x_norm = round(v['views'] / normal, 2) if normal else None
        flag = ('too early' if age < 3 else 'beat normal (2x+)' if x_norm and x_norm >= 2
                else 'below half of normal' if x_norm is not None and x_norm <= 0.5 else '')
        videos.append({**{k: v[k] for k in ('id', 'date', 'url', 'views', 'likes', 'comments', 'shares', 'saves',
                                            'pinned', 'shop_tag', 'duration_s')},
                       'caption': v['caption'][:300], 'age_days': age, 'normal': normal, 'x_normal': x_norm,
                       'saves_per_view': round(v['saves'] / v['views'], 4) if v['views'] else 0,
                       'format': classify(v['caption']), 'flag': flag})

    def since(days):
        return [v for v in allv if (now - _ts(v['date'])).days < days]

    y12 = since(365)
    y2026 = [v for v in allv if v['date'] >= '2026']
    clinic = [v for v in videos if v['format'] == 'Lightstick tutorial' and not v['pinned'] and v['age_days'] >= 3]
    board = {
        'posts_last_7d': len(since(7)),
        'posts_last_90d': len(since(90)),
        'median_views_2026': st.median(v['views'] for v in y2026) if y2026 else None,
        'zero_comment_share_12m': round(sum(v['comments'] == 0 for v in y12) / len(y12), 2) if y12 else None,
        'saves_per_view_12m': round(st.median(v['saves'] / v['views'] for v in y12 if v['views']), 4) if y12 else None,
        'clinic_count_latest30': len(clinic),
        'clinic_median_x_normal': st.median(v['x_normal'] for v in clinic if v['x_normal']) if clinic else None,
        'clinic_median_saves': st.median(v['saves_per_view'] for v in clinic) if clinic else None,
        'breakouts_since_plan': [v['url'] for v in allv
                                 if _ts(v['date']) >= PLAN_START and v['views'] > TARGET['breakout_views']],
    }

    fan = []
    for c in comments:
        cid = str(c.get('cid') or '')
        if not cid or cid in seen_cids or c.get('uniqueId') == HANDLE:
            continue
        seen_cids[cid] = now.isoformat()
        qt = question_type(c.get('text'))
        fan.append({'text': (c.get('text') or '').strip()[:300], 'likes': c.get('diggCount') or 0,
                    'date': c.get('createTimeISO', ''), 'video': c.get('videoWebUrl') or c.get('submittedVideoUrl'),
                    'type': qt, 'has_replies': bool(c.get('replyCommentTotal'))})
    fan.sort(key=lambda c: -c['likes'])
    types = {}
    for c in fan:
        if c['type']:
            types[c['type']] = types.get(c['type'], 0) + 1

    posts = []
    for p in x:
        if p.get('isRetweet') or p.get('type') == 'mock_tweet':
            continue
        try:
            when = dt.datetime.strptime(p.get('createdAt', ''), '%a %b %d %H:%M:%S %z %Y').isoformat()
        except ValueError:
            when = ''
        posts.append({'date': when, 'url': p.get('url'), 'views': p.get('viewCount'),
                      'likes': p.get('likeCount'), 'replies': p.get('replyCount'),
                      'text': (p.get('text') or '').strip()[:200]})
    posts.sort(key=lambda p: p['date'], reverse=True)
    xv = [p['views'] for p in posts if p['views'] is not None]
    return {'videos': videos, 'scoreboard': board, 'fan_comments': fan, 'question_types': types,
            'x': {'posts': posts, 'median_views': st.median(xv) if xv else None}}


# ---------- report ----------

def _pct(x, digits=1):
    return '-' if x is None else f'{x * 100:.{digits}f}%'


def report_md(week, res, health, now, source):
    b = res['scoreboard']
    L = [f'# Weekly stats · {week}', '',
         f"Made {now.astimezone(PHT):%Y-%m-%d %H:%M} PHT from {source}. "
         f"Sources: TikTok {health['tiktok']} videos, comments {health['comments']}, X {health['x']} posts"
         + (' (**a source returned 0: numbers below are incomplete**)' if 0 in health.values() else '') + '.', '',
         '"Normal" = median views of the 21 posts around a video in time. Videos under 3 days old are still growing.',
         '', '## Scoreboard (STRATEGY.md section 11)', '',
         '| Measure | Now | Start (Oct 14) | Target by mid-Jan |', '|---|---|---|---|',
         f"| Posts in the last 7 days | {b['posts_last_7d']} | - | {TARGET['posts_week']} a week |",
         f"| Posts in the last 90 days | {b['posts_last_90d']} | {START['posts_90d']} | about 36 in 12 weeks |",
         f"| Median views, 2026 posts | {b['median_views_2026']} | {START['median_views_2026']} | - |",
         f"| Posts with zero comments, last 12 months | {_pct(b['zero_comment_share_12m'], 0)} | "
         f"{_pct(START['zero_comment_share'], 0)} | under {_pct(TARGET['zero_comment_share'], 0)} |",
         f"| Saves per view (median), last 12 months | {_pct(b['saves_per_view_12m'], 2)} | "
         f"{_pct(START['saves_per_view'], 2)} | - |",
         f"| Clinic videos in the latest 30 (3+ days old) | {b['clinic_count_latest30']} | - | at least 12 in 12 weeks |",
         f"| Clinic median vs normal | {b['clinic_median_x_normal'] or '-'}x | - | {TARGET['clinic_x_normal']}x or more |",
         f"| Clinic median saves | {_pct(b['clinic_median_saves'], 2)} | - | {_pct(TARGET['clinic_saves'], 2)} or more |",
         f"| Videos over 10,000 views since Oct 14 | {len(b['breakouts_since_plan'])} | - | 3 in 12 weeks |",
         '', '## Latest videos', '',
         '| Posted | Views | vs normal | Saves | Comments | Format | Caption | Note |', '|---|---|---|---|---|---|---|---|']
    for v in res['videos']:
        cap = re.sub(r'\s+', ' ', v['caption'])[:60].replace('|', '/')
        L.append(f"| [{_ts(v['date']).astimezone(PHT):%b %d %Y}]({v['url']}) | {v['views']:,} | "
                 f"{v['x_normal'] or '-'}x | {_pct(v['saves_per_view'], 2)} | {v['comments']} | {v['format']} | "
                 f"{cap} | {'pinned ' if v['pinned'] else ''}{v['flag']} |")
    fan = res['fan_comments']
    L += ['', f'## Fan comments: {len(fan)} new on the latest 10 videos', '']
    if res['question_types']:
        L += ['| Question type | Count |', '|---|---|']
        L += [f'| {k} | {n} |' for k, n in sorted(res['question_types'].items(), key=lambda kv: -kv[1])]
        L.append('')
    L.append('Questions (most liked first, text only; re-type without names before showing on screen):')
    L.append('')
    qs = [c for c in fan if c['type']]
    for c in qs[:20]:
        text = re.sub(r'\s+', ' ', c['text'])[:160]
        reply = 'has replies' if c['has_replies'] else '**no replies**'
        L.append(f"- \"{text}\" · {c['type']} · {c['likes']} likes · {reply} · [video]({c['video']})")
    if not qs:
        L.append('- none this week')
    xs = res['x']
    L += ['', f"## X: {len(xs['posts'])} posts, median {xs['median_views'] or '-'} views", '',
          '| Posted | Views | Likes | Replies | Text |', '|---|---|---|---|---|']
    for p in xs['posts'][:15]:
        t = re.sub(r'\s+', ' ', p['text'])[:70].replace('|', '/')
        when = f"{_ts(p['date']).astimezone(PHT):%b %d}" if p['date'] else '?'
        L.append(f"| [{when}]({p['url']}) | {p['views']} | {p['likes']} | {p['replies']} | {t} |")
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Weekly stats for Unnie Mart')
    ap.add_argument('--from-raw', action='store_true', help='use the 2026-10-14 research scrape (no Apify spend)')
    ap.add_argument('--dry-run', action='store_true', help='print the report; save nothing')
    a = ap.parse_args(argv)

    now = now_utc()
    tt, comments, x = fetch_raw() if a.from_raw else fetch_live()
    hist = load_history()
    seen = load_json(COMMENTS_SEEN, {})
    res = analyse(tt, comments, x, hist, seen, now)
    week = iso_week(now.astimezone(PHT))
    health = {'tiktok': len(tt), 'comments': len(comments), 'x': len(x)}
    source = 'the 2026-10-14 research scrape (--from-raw)' if a.from_raw else 'a live Apify scrape'
    md = report_md(week, res, health, now, source)
    if a.dry_run:
        print(md)
        return 0
    save_json(HISTORY, hist)
    save_json(COMMENTS_SEEN, seen)
    save_json(STATS_DIR / f'{week}.json', {'week': week, 'made_at': now.isoformat(), 'source': source,
                                           'health': health, **res})
    (STATS_DIR / f'{week}.md').write_text(md)
    b = res['scoreboard']
    print(f"{week}: {len(res['videos'])} videos, {len(res['fan_comments'])} new comments, {len(x)} X posts · "
          f"posts last 7d {b['posts_last_7d']} · median 2026 {b['median_views_2026']} · data/stats/{week}.md")
    return 0


if __name__ == '__main__':
    sys.exit(main())
