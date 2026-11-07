#!/usr/bin/env python3
"""Daily news watch for Unnie Mart (strategy/AUTOMATION.md, section 4, Phase A).

Polls Google News, K-pop and PH press feeds, PH ticket sites, Weverse Shop notices and two subreddits; keeps items
about the shop's groups (automations/config.py); dedupes against what it has seen before; then:
  - data/news/YYYY-MM-DD.json   new items of the day + source health for every run (weekly_brief reads these)
  - data/news/latest.md          human digest of the last run
  - Telegram                     urgent items only (new lightstick sale, PH show or ticket date, new K-pop event on
                                 a PH ticket site), if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are in .env

Headlines only. Nothing here is a verified fact: open the link before using a date or price.

The first run (no memory yet) records everything as seen and sends no alerts, so day one isn't a flood.

Usage: python3 automations/news_watch.py [--dry-run] [--no-telegram] [--only NAME]
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import email.utils
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C  # noqa: E402
from common import DATA, PHT, STATE, esc, http_get, load_json, now_utc, save_json, telegram_send  # noqa: E402

NEWS_DIR = DATA / 'news'
SEEN_FILE = STATE / 'news_seen.json'

_GROUPS = [(name, tier,
            re.compile(ci, re.I) if ci else None,
            re.compile(cs) if cs else None, wid) for name, tier, ci, cs, wid in C.GROUPS]
_R = {k: re.compile(getattr(C, k), re.I) for k in ('LIGHTSTICK', 'SALE', 'PH', 'CONCERT', 'TICKET', 'MERCH', 'KPOP')}
_PH_CS = re.compile(C.PH_CS)
_FAN_Q = re.compile(r'fake|legit|authentic|where (to|can i) buy|connect|pair|sync|which version|old version', re.I)


# ---------- classification ----------

def match_groups(text):
    out = []
    for name, tier, ci, cs, _ in _GROUPS:
        if (ci and ci.search(text)) or (cs and cs.search(text)):
            out.append(name)
    return out


def classify(title, kind, broad=True):
    """Return (priority, groups, reason). priority is 'urgent', 'normal', 'low' or None (drop).
    kind: 'news' (feeds), 'ticket' (new title on a PH ticket site), 'weverse' (Weverse Shop notice of a watched
    artist), 'reddit' (fan posts)."""
    t = title or ''
    groups = match_groups(t)
    has = {k: bool(r.search(t)) for k, r in _R.items()}
    ph = has['PH'] or bool(_PH_CS.search(t))

    if kind == 'ticket':
        if groups or has['KPOP']:
            return 'urgent', groups, 'new K-pop event on a PH ticket site'
        return 'low', groups, 'new event on a PH ticket site'
    if kind == 'weverse':
        if has['LIGHTSTICK']:
            return 'urgent', groups, 'Weverse Shop lightstick notice'
        if re.search(r"season'?s greetings|membership|pre-?order|ticket", t, re.I) or ph:
            return 'normal', groups, 'Weverse Shop notice (SG / membership / pre-order)'
        return 'low', groups, 'Weverse Shop notice'
    if kind == 'reddit':
        if (has['LIGHTSTICK'] or ph or _FAN_Q.search(t)) and (groups or has['LIGHTSTICK'] or ph):
            return 'normal', groups, 'fan question'
        return None, groups, ''

    # news
    if groups and has['LIGHTSTICK'] and has['SALE']:
        return 'urgent', groups, 'lightstick release or sale'
    if (groups or has['KPOP']) and ph and (has['CONCERT'] or has['TICKET']):
        return 'urgent', groups, 'PH show or tickets'
    if groups and (has['CONCERT'] or has['TICKET'] or has['MERCH'] or has['LIGHTSTICK']):
        return 'normal', groups, 'group news: tour / merch / release'
    if has['KPOP'] and ph:
        return 'normal', groups, 'K-pop in the Philippines'
    if broad:
        return None, groups, ''
    return 'low', groups, 'matched a targeted search'


def norm_key(title):
    return re.sub(r'[^a-z0-9]+', ' ', (title or '').lower()).strip()


# ---------- parsers (pure functions, tested) ----------

def _date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d


def parse_feed(content):
    """RSS or Atom -> [{title, link, published, publisher}]. Google News titles lose their ' - Publisher' tail."""
    root = ET.fromstring(content)
    out = []
    for it in root.iter('item'):
        title = (it.findtext('title') or '').strip()
        src = it.find('source')
        publisher = (src.text or '').strip() if src is not None else ''
        if publisher and title.endswith(' - ' + publisher):
            title = title[: -len(publisher) - 3]
        out.append({'title': unescape(title), 'link': (it.findtext('link') or '').strip(),
                    'published': _date(it.findtext('pubDate')), 'publisher': publisher})
    a = '{http://www.w3.org/2005/Atom}'
    for e in root.iter(a + 'entry'):
        link = e.find(a + 'link')
        out.append({'title': unescape((e.findtext(a + 'title') or '').strip()),
                    'link': link.get('href', '') if link is not None else '',
                    'published': _date(e.findtext(a + 'published') or e.findtext(a + 'updated')), 'publisher': ''})
    return out


def parse_sitemap(content):
    sm, nn = '{http://www.sitemaps.org/schemas/sitemap/0.9}', '{http://www.google.com/schemas/sitemap-news/0.9}'
    out = []
    for u in ET.fromstring(content).iter(sm + 'url'):
        news = u.find(nn + 'news')
        title = news.findtext(nn + 'title') if news is not None else ''
        pub = news.findtext(nn + 'publication_date') if news is not None else None
        out.append({'title': unescape((title or '').strip()), 'link': (u.findtext(sm + 'loc') or '').strip(),
                    'published': _date(pub), 'publisher': ''})
    return out


def _strip(h):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def parse_smtickets(page):
    marker = "original_array = JSON.parse('"
    i = page.find(marker)
    if i >= 0:
        arr, _ = json.JSONDecoder().raw_decode(page[i + len(marker):].replace("\\'", "'"))
        return [{'title': a['event_long_title'].strip(),
                 'link': f"https://www.smtickets.com/events/view/{a['event_id']}",
                 'when': a.get('event_date_time', '')} for a in arr]
    return [{'title': _strip(m), 'link': '', 'when': ''}
            for m in re.findall(r'class="event_li"[^>]*>\s*<div>(.*?)</div>', page, re.S)]


def parse_pulp(page):
    start, end = page.find('UPCOMING SHOWS'), page.find('>MEDIA<')
    block = page[start:end if end > start else None] if start >= 0 else ''
    return [{'title': _strip(m), 'link': 'https://www.pulpliveworld.com/', 'when': ''}
            for m in re.findall(r'<h\d[^>]*>(.*?)</h\d>', block, re.S) if 'UPCOMING SHOWS' not in m]


def parse_livenation(page):
    return [{'title': _strip(t), 'link': 'https://www.livenation.ph/', 'when': _strip(w)}
            for t, w in re.findall(r'header5[^>]*>([^<]+)</p><small[^>]*>([^<]+)</small>', page)]


_TICKETNET_SKIP = re.compile(r'featured shows|upcoming events|new frontier theater|gateway cineplex|faq|fake tickets', re.I)


def parse_ticketnet(page):
    out = []
    for m in re.findall(r'<h\d[^>]*>(.*?)</h\d>', page, re.S):
        t = _strip(m)
        if len(t) > 3 and not _TICKETNET_SKIP.search(t):
            out.append({'title': t, 'link': 'https://www.ticketnet.com.ph/', 'when': ''})
    return out


TICKET_PARSERS = {'smtickets': parse_smtickets, 'pulp': parse_pulp, 'livenation': parse_livenation,
                  'ticketnet': parse_ticketnet}


def parse_weverse_notices(page, artist_id):
    """Weverse Shop notice list -> notices for this artist, plus site-wide ones that name a watched group."""
    i = page.find('"notices":[')
    if i < 0:
        return []
    arr, _ = json.JSONDecoder().raw_decode(page[i + len('"notices":'):])
    out = []
    for n in arr:
        if n.get('artistId') == artist_id or (n.get('artistId') == 0 and match_groups(n.get('title', ''))):
            out.append({'title': n['title'].strip(), 'artist': n.get('artistName', ''),
                        'link': C.WEVERSE_NOTICE.format(id=artist_id, nid=n['id']),
                        'published': _date(n.get('displayStartAt'))})
    return out


# ---------- collection ----------

def _sources():
    """(name, kind, fetch) for every source. fetch() returns a list of raw items."""
    src = []
    for name, url, broad in C.GNEWS + C.FEEDS:
        src.append((name, 'news', broad, lambda u=url: parse_feed(http_get(u).content)))
    for name, url in C.SITEMAPS:
        src.append((name, 'news', True, lambda u=url: parse_sitemap(http_get(u).content)))
    for name, url, parser in C.TICKET_SITES:
        src.append((name, 'ticket', False, lambda u=url, p=parser: TICKET_PARSERS[p](http_get(u).text)))
    for name, _, _, _, wid in C.GROUPS:
        if wid:
            src.append((f'Weverse Shop notices: {name}', 'weverse', False,
                        lambda w=wid: parse_weverse_notices(http_get(C.WEVERSE_NOTICES.format(id=w)).text, w)))
    return src


def _reddit():
    return [(name, 'reddit', False, lambda u=url: parse_feed(http_get(u, ua=C.REDDIT_UA, tries=1).content))
            for name, url in C.REDDIT]


def collect(only=None):
    """Fetch every source. Returns (items, health)."""
    sources = _sources()
    if only:
        sources = [s for s in sources if only.lower() in s[0].lower()]
    results = {}
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch): (name, kind, broad) for name, kind, broad, fetch in sources}
        for f in cf.as_completed(futs):
            results[futs[f]] = f
    # Reddit last and one at a time (it rate-limits)
    for name, kind, broad, fetch in _reddit():
        if only and only.lower() not in name.lower():
            continue
        time.sleep(2)
        f = cf.Future()
        try:
            f.set_result(fetch())
        except Exception as e:  # noqa: BLE001
            f.set_exception(e)
        results[(name, kind, broad)] = f

    cutoff = now_utc() - dt.timedelta(days=C.MAX_AGE_DAYS)
    items, health = [], []
    for (name, kind, broad), f in sorted(results.items()):
        try:
            raw = f.result()
        except Exception as e:  # noqa: BLE001
            health.append({'source': name, 'ok': False, 'count': 0, 'kept': 0, 'error': str(e)[:160]})
            continue
        kept = 0
        for r in raw:
            pub = r.get('published')
            if pub and pub < cutoff:
                continue
            prio, groups, reason = classify(r['title'], kind, broad)
            if kind == 'weverse' and not groups:
                groups = match_groups(r.get('artist', '')) or [r.get('artist', '')]
            if prio is None:
                continue
            kept += 1
            items.append({'key': norm_key(r['title']), 'title': r['title'], 'link': r.get('link', ''),
                          'source': name + (f" ({r['publisher']})" if r.get('publisher') else ''),
                          'kind': kind, 'published': pub.isoformat() if pub else None,
                          'when': r.get('when', ''), 'groups': groups, 'priority': prio, 'reason': reason})
        health.append({'source': name, 'ok': True, 'count': len(raw), 'kept': kept,
                       'error': '' if raw else 'returned 0 items'})
    return items, health


def dedupe(items):
    """One item per headline; the highest priority copy wins."""
    rank = {'urgent': 0, 'normal': 1, 'low': 2}
    best = {}
    for it in items:
        if it['key'] and (it['key'] not in best or rank[it['priority']] < rank[best[it['key']]['priority']]):
            best[it['key']] = it
    out = sorted(best.values(), key=lambda x: x['published'] or '', reverse=True)   # newest first...
    return sorted(out, key=lambda x: rank[x['priority']])                            # ...within each priority


# ---------- output ----------

def _fmt_date(iso):
    if not iso:
        return ''
    return dt.datetime.fromisoformat(iso).astimezone(PHT).strftime('%b %d')


def digest_md(new, health, run_at, seeded):
    lines = [f"# News watch · {run_at.astimezone(PHT):%Y-%m-%d %H:%M} PHT", '',
             'Headlines only. Open the link and check the official source before using any date, price or version.', '']
    if seeded:
        lines += ['**First run:** everything below was recorded as already seen. No alerts were sent.', '']
    bad = [h for h in health if not h['ok'] or h['count'] == 0]
    lines.append(f"**Sources:** {len(health) - len(bad)} of {len(health)} returned items."
                 + (' Problems: ' + '; '.join(f"{h['source']}: {h['error']}" for h in bad) if bad else ''))
    lines.append('')
    for prio, head in (('urgent', 'Urgent'), ('normal', 'Worth a look'), ('low', 'Low priority')):
        group = [i for i in new if i['priority'] == prio]
        lines.append(f'## {head} ({len(group)})')
        lines.append('')
        for i in group:
            g = ', '.join(i['groups']) or '-'
            meta = ' · '.join(x for x in (i['source'], _fmt_date(i['published']) or i['when'], i['reason']) if x)
            lines.append(f"- **{g}** [{i['title']}]({i['link']})  \n  {meta}")
        lines.append('')
    lines += ['## Source health', '', '| Source | OK | Items | Kept | Note |', '|---|---|---|---|---|']
    lines += [f"| {h['source']} | {'yes' if h['ok'] else 'NO'} | {h['count']} | {h['kept']} | {h['error']} |"
              for h in health]
    return '\n'.join(lines) + '\n'


def telegram_text(urgent, health):
    lines = [f'🔔 <b>Unnie Mart news watch</b>: {len(urgent)} urgent', '']
    for i in urgent:
        g = ', '.join(i['groups']) or 'K-pop'
        lines.append(f"• <b>{esc(g)}</b>: {esc(i['title'])}")
        lines.append(f"  {esc(i['source'])} · {esc(i['reason'])}")
        if i['link']:
            lines.append(f"  {esc(i['link'])}")
        lines.append('')
    bad = [h['source'] for h in health if not h['ok']]
    if bad:
        lines.append(f"⚠️ Sources down: {esc(', '.join(bad))}")
    lines.append('Headlines only: check the official source before filming.')
    return '\n'.join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--dry-run', action='store_true', help='print only; no files, no memory, no Telegram')
    ap.add_argument('--no-telegram', action='store_true')
    ap.add_argument('--only', help='only sources whose name contains this text (for debugging)')
    a = ap.parse_args(argv)

    run_at = now_utc()
    items, health = collect(a.only)
    items = dedupe(items)

    seen = load_json(SEEN_FILE, {})
    seeded = not seen and not a.only
    new = [i for i in items if i['key'] not in seen]
    for i in new:
        i['first_seen'] = run_at.isoformat()

    md = digest_md(new, health, run_at, seeded)
    urgent = [i for i in new if i['priority'] == 'urgent']
    if a.dry_run:
        print(md)
        return 0

    for i in new:
        seen[i['key']] = run_at.isoformat()
    keep_after = (run_at - dt.timedelta(days=C.SEEN_KEEP_DAYS)).isoformat()
    save_json(SEEN_FILE, {k: v for k, v in seen.items() if v >= keep_after})

    day_file = NEWS_DIR / f'{run_at.astimezone(PHT):%Y-%m-%d}.json'
    day = load_json(day_file, {'items': [], 'runs': []})
    day['items'] += new
    day['runs'].append({'run_at': run_at.isoformat(), 'seeded': seeded, 'new': len(new), 'health': health})
    save_json(day_file, day)
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    (NEWS_DIR / 'latest.md').write_text(md)

    sent = False
    if urgent and not seeded and not a.no_telegram:
        sent = telegram_send(telegram_text(urgent, health))
    ok = sum(h['ok'] and h['count'] > 0 for h in health)
    print(f"{len(new)} new ({len(urgent)} urgent) · sources {ok}/{len(health)} · "
          f"{'seeded, no alerts' if seeded else ('Telegram sent' if sent else 'Telegram not sent')} · "
          f"{day_file.relative_to(DATA.parent)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
