#!/usr/bin/env python3
"""Weekly brief for Unnie Mart (strategy/AUTOMATION.md, sections 2 to 4, Phase A).

Gathers the week's inputs into numbered sources (calendar, news, own stats and fan questions, peer outliers, the
owner's stock list and notes, TikTok Studio summary), asks Claude for video ideas that cite those sources, then
checks every idea in Python:
  filters  1 has a real source · 2 can be filmed and sold (stock list) · 3 not the same offer within 14 days
  gate     fact quotes must appear in the cited source · numbers must appear in a source · banned phrases
  ranking  active season · matching fan questions · evidence level of the format
Claude runs through the `claude` command on Andrey's subscription (no API key, no tools, no files).

Writes content/ideas/YYYY-Www.md (the draft for Andrey) and data/briefs/YYYY-Www.json (everything, for checking).
The week is the one starting next Monday, or this week when run on a Monday.

Usage:
  python3 automations/weekly_brief.py               # full run, about 5 to 6 minutes with Opus
  python3 automations/weekly_brief.py --dry-run     # build the source pack and prompt, don't call Claude
  python3 automations/weekly_brief.py --from-json data/briefs/2026-W43.json   # re-check and re-render, no Claude
"""
import argparse
import csv
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import masterlist  # noqa: E402
from banned_check import check as banned_check  # noqa: E402
from common import DATA, PHT, ROOT, esc, load_env, load_json, now_utc, save_json, telegram_send  # noqa: E402
from weekly_stats import QUESTION_TYPES, question_type  # noqa: E402

IDEAS_DIR = ROOT / 'content' / 'ideas'
BRIEFS_DIR = DATA / 'briefs'
OWNER = DATA / 'owner'
MODEL = 'claude-opus-5-5'
CLAUDE_TIMEOUT_S = 900
SEASON_DAYS = 42        # "a Philippine show or lightstick launch in the next 6 weeks"
REPEAT_DAYS = 14
NEWS_DAYS = 8
STALE_DAYS = 8          # stats or peers older than this are called out
MAX_READY = 5
PAST_QUESTIONS = 20    # most-liked real questions from the research comment scrape (data/comments.csv)
# STRATEGY.md section 2. BTS counts until the last Bulacan night.
SEASONS = [
    ('BTS Bulacan', '2026-06-12', '2027-03-16'),
    ('ENHYPEN Renewal', '2026-10-01', '2026-11-30'),
    ('Manila December shows', '2026-10-20', '2026-12-12'),
    ('Early 2027 shows', '2026-12-01', '2027-02-20'),
]
FORMATS = ['Clinic', 'Proof', 'Money', 'News', 'Answer a fan', 'Fan moment']
QTYPES = [q for q, _ in QUESTION_TYPES]
NUM = re.compile(r'\d[\d,.]*\d|\d')


# ---------- pure helpers (tested) ----------

def norm(s):
    """Lowercase, straight quotes, every run of non-letters/digits becomes one space."""
    s = (s or '').lower().replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return ' '.join(re.sub(r"[^\w']+|_", ' ', s).split())


def _day(s, end=False):
    """'2026-10-19' or '2026-10' (a whole month) → date."""
    s = (s or '').strip()
    if re.fullmatch(r'\d{4}-\d\d-\d\d', s):
        return dt.date.fromisoformat(s)
    if re.fullmatch(r'\d{4}-\d\d', s):
        y, m = map(int, s.split('-'))
        first = dt.date(y, m, 1)
        return (dt.date(y + m // 12, m % 12 + 1, 1) - dt.timedelta(days=1)) if end else first
    return None


def target_week(today):
    """(label, monday, sunday) for the week starting next Monday, or this week on a Monday."""
    monday = today + dt.timedelta(days=(7 - today.weekday()) % 7)
    y, w, _ = monday.isocalendar()
    return f'{y}-W{w:02d}', monday, monday + dt.timedelta(days=6)


def active_seasons(day):
    return [n for n, a, b in SEASONS if dt.date.fromisoformat(a) <= day <= dt.date.fromisoformat(b)]


def calendar_rows(rows, today, days=SEASON_DAYS):
    """Events running now or starting in the next `days` days."""
    out = []
    for r in rows:
        start, end = _day(r['date_start']), _day(r['date_end'] or r['date_start'], end=True)
        if start and end and start <= today + dt.timedelta(days=days) and end >= today:
            out.append(r)
    return out


def season_anchors(rows, today):
    """The show that ends each active season (e.g. BTS Bulacan in March), even when it's months away."""
    ends = {dt.date.fromisoformat(b) for n, a, b in SEASONS if n in active_seasons(today)}
    return [r for r in rows if r['event_type'] == 'concert'
            and _day(r['date_end'] or r['date_start'], end=True) in ends]


def numbers(text):
    """Numbers of 2+ digits a reader would take as a fact (hashtags and ₱___ placeholders ignored)."""
    text = re.sub(r'#\w+', ' ', text or '')
    return sorted({n.replace(',', '').rstrip('.') for n in NUM.findall(text) if len(re.sub(r'\D', '', n)) >= 2})


def _flat(s, n):
    return re.sub(r'\s+', ' ', s or '').strip()[:n]


def stock_row(stock, item):
    return next((r for r in stock if r['item'] == item), None)


def gate(idea, sources, stock, own_recent, active):
    """Check one idea. Returns dict(status, problems, warnings). Status: ready | held | waiting | dropped."""
    problems, warnings = [], []
    ids = [i for i in idea.get('source_ids', []) if i in sources]
    unknown = [i for i in idea.get('source_ids', []) if i not in sources]
    if unknown:
        problems.append(f"cites sources that don't exist: {', '.join(unknown)}")
    if not ids:
        return {'status': 'dropped', 'problems': problems + ['no real source'], 'warnings': warnings}

    # Facts: the quote has to be in the cited source, word for word (ignoring case and punctuation).
    for f in idea.get('facts', []):
        src = sources.get(f.get('source_id'))
        if not src:
            problems.append(f"fact \"{f.get('claim', '')[:60]}\" cites unknown source {f.get('source_id')}")
        elif not f.get('quote') or norm(f['quote']) not in norm(src['text']):
            problems.append(f"fact \"{f.get('claim', '')[:60]}\": quote not found in {src['id']}")

    # Numbers: anything a viewer reads (caption, screen text, pinned comment, fact claims) must come from a source.
    pool = ' '.join(sources[i]['text'] for i in ids) + ' ' + ' '.join(
        sources[f['source_id']]['text'] for f in idea.get('facts', []) if f.get('source_id') in sources)
    pool += ' ' + ' '.join(s['text'] for s in sources.values() if s['kind'] in ('stock', 'owner notes'))
    pool_digits = pool.replace(',', '')
    viewer_text = ' '.join([idea.get('caption', ''), idea.get('hook_on_screen', ''), idea.get('pinned_comment', '')]
                           + [f.get('claim', '') for f in idea.get('facts', [])])
    for n in numbers(viewer_text):
        if not re.search(rf'(?<!\d){re.escape(n)}(?!\d)', pool_digits):
            problems.append(f'number "{n}" is not in any cited source')

    # Banned phrases and slop (captions are checked as captions; the shot list for visuals and wording).
    for label, text in (('caption', idea.get('caption', '')), ('screen text', idea.get('hook_on_screen', '')),
                        ('pinned comment', idea.get('pinned_comment', '')),
                        ('shot list', '\n'.join(idea.get('shot_list', [])))):
        for f in banned_check(text, markdown=(label == 'shot list')):
            msg = f'{label}: {f.rule} "{f.match}" ({f.message})'
            (problems if f.level == 'BLOCK' else warnings).append(msg)

    # Filter 3: same offer within REPEAT_DAYS (formats can repeat, offers can't).
    if idea.get('sells'):
        for kw in idea.get('offer_keywords', []):
            k = norm(kw)
            hit = next((v for v in own_recent if k and k in norm(re.sub(r'#\w+', ' ', v['caption']))), None)
            if hit:
                problems.append(f"same offer (\"{kw}\") posted {hit['date'][:10]} ({hit['url']})")
                break

    status = 'held' if problems else 'ready'

    # Filter 2: can it be filmed and sold? Unknowns stay in, with a warning.
    item = idea.get('item') or 'none'
    if item != 'none':
        r = stock_row(stock, item)
        if r is None:
            warnings.append(f'"{item}" is not on the stock list')
        else:
            filmable = 'yes' in (r['demo_unit'], r['on_hand'])
            if idea.get('needs_unit') and not filmable:
                eta = f" (expected: {r['eta']})" if r.get('eta') else ''
                if status == 'ready':
                    status = 'waiting'
                problems.append(f'no demo unit or stock of {item} yet{eta}')
            if idea.get('sells'):
                if r['on_hand'] == 'no' and r['open_go'] == 'no':
                    if status == 'ready':
                        status = 'waiting'
                    problems.append(f'{item} is not on sale (not on hand, no open GO)')
                elif 'unknown' in (r['on_hand'], r['open_go']) and 'yes' not in (r['on_hand'], r['open_go']):
                    warnings.append(f'ask her: is {item} on hand or in an open GO?')
    if idea.get('season') not in ('none', None) and idea['season'] not in active:
        warnings.append(f"season \"{idea['season']}\" isn't active this week")
    return {'status': status, 'problems': problems, 'warnings': warnings}


def rank_key(idea, sources, q_counts, active):
    """Sort key per AUTOMATION.md section 2: season, then fan questions, then evidence."""
    in_season = idea.get('season') in active
    cited_q = sum(1 for i in idea.get('source_ids', []) if sources.get(i, {}).get('kind', '').startswith('fan question'))
    questions = q_counts.get(idea.get('question_type'), 0) + cited_q
    fmt = idea.get('format')
    evidence = 3 if fmt == 'Clinic' and in_season else 2 if fmt == 'Proof' and in_season else 1
    return (-int(in_season), -questions, -evidence), {'in_season': in_season, 'questions': questions,
                                                      'evidence': evidence}


# ---------- inputs ----------

def _latest(folder, pattern):
    files = sorted(folder.glob(pattern))
    return (files[-1], json.loads(files[-1].read_text())) if files else (None, None)


def load_news(today):
    """Urgent and normal items from the last NEWS_DAYS of news_watch files, plus the latest run's health."""
    items, seen, last_run = [], set(), None
    for f in sorted((DATA / 'news').glob('20??-??-??.json')):
        if (today - dt.date.fromisoformat(f.stem)).days > NEWS_DAYS:
            continue
        d = json.loads(f.read_text())
        for it in d.get('items', []):
            if it.get('priority') in ('urgent', 'normal') and it['key'] not in seen:
                seen.add(it['key'])
                items.append(it)
        if d.get('runs'):
            last_run = d['runs'][-1]
    items.sort(key=lambda it: (it['priority'] != 'urgent', -(dt.datetime.fromisoformat(
        it['published']).timestamp() if it.get('published') else 0)))
    return items, last_run


def stock_from_sheet(it, updated):
    """One item of her "ONHAND items" tab as a stock row. Never carries who took the slots."""
    left, total = it['slots_left'], it['slots_total']
    slots = f'{left} of {total} slots left' if left is not None and total else 'no slot limit listed'
    name = ' · '.join(x for x in (it['section'], it['sub'], it['item']) if x)
    return {'item': name, 'fandom': '', 'demo_unit': 'unknown', 'on_hand': 'yes' if left else 'unknown',
            'open_go': 'yes', 'eta': '', 'price_note': f'{masterlist.price_text(it)} · {slots} (her stock sheet)',
            'updated': updated, 'from_sheet': 'yes'}


def sheet_stock(path=None):
    """Her live stock tab from the saved masterlist, as stock rows. [] when there's no saved copy."""
    path = path or masterlist.SHEET
    if not path.exists():
        return []
    wb = masterlist.open_sheet(path)
    try:
        items = masterlist.stock_items(wb[masterlist.STOCK_TAB]) if masterlist.STOCK_TAB in wb.sheetnames else []
    finally:
        wb.close()
    updated = masterlist.read_at(path).date().isoformat()
    return [stock_from_sheet(it, updated) for it in items]


def load_inputs(today):
    with open(DATA / 'calendar.csv') as f:
        rows = list(csv.DictReader(f))
    cal = calendar_rows(rows, today)
    cal += [r for r in season_anchors(rows, today) if r not in cal]
    news, news_run = load_news(today)
    stats_path, stats = _latest(DATA / 'stats', '20??-W??.json')
    peers_path, peers = _latest(DATA / 'peers', '20??-W??.json')
    with open(OWNER / 'stock.csv') as f:
        stock = [{k: (v or '').strip() for k, v in r.items()} for r in csv.DictReader(f)]
    stock += sheet_stock()
    tally = {}
    qfile = OWNER / 'questions.csv'
    if qfile.exists():
        with open(qfile) as f:
            for r in csv.DictReader(f):
                if r.get('type') in QTYPES and (r.get('count') or '').strip().isdigit():
                    tally[r['type']] = tally.get(r['type'], 0) + int(r['count'])
    notes = (OWNER / 'notes.md').read_text() if (OWNER / 'notes.md').exists() else ''
    studio = (OWNER / 'studio' / 'summary.md').read_text() if (OWNER / 'studio' / 'summary.md').exists() else ''
    own = list(load_json(DATA / 'state' / 'own_videos.json', {}).values())
    past = []
    if (DATA / 'comments.csv').exists():
        with open(DATA / 'comments.csv') as f:
            for r in csv.DictReader(f):
                t = question_type(r['comment_text'])
                if t in QTYPES and r['is_shop_comment'].lower() not in ('true', '1'):
                    past.append({**r, 'type': t, 'likes': int(r['likes'] or 0)})
        past = sorted(past, key=lambda r: -r['likes'])[:PAST_QUESTIONS]
    return {'past_questions': past, 'calendar': cal, 'news': news, 'news_run': news_run, 'stats': stats, 'stats_path': stats_path,
            'peers': peers, 'peers_path': peers_path, 'stock': stock, 'tally': tally, 'notes': notes,
            'studio': studio, 'own': own}


def build_sources(inp, now):
    """Number every input so Claude can cite it and Python can check the citation."""
    src = []

    def add(prefix, kind, text, url='', date='', note=''):
        n = sum(1 for s in src if s['id'][0] == prefix) + 1
        src.append({'id': f'{prefix}{n}', 'kind': kind, 'date': date, 'text': text.strip(), 'url': url,
                    **({'note': note} if note else {})})

    for r in inp['calendar']:
        add('C', 'calendar', f"{r['date_start']}{' to ' + r['date_end'] if r['date_end'] else ''} · {r['group']} · "
            f"{r['event_type']} · {r['title']} · {r['location']} · confidence {r['confidence']}",
            r['source_url'], r['date_start'], note=r['content_angle'])
    for it in inp['news']:
        if it.get('published'):
            add('N', f"news ({it['priority']})", f"{it['title']} [{it['source']}]", it['link'], it['published'][:10])
        else:       # ticket pages and some notices have no date: say when we found it, not when it was announced
            add('N', f"news ({it['priority']}, undated)", f"{it['title']} [{it['source']}] (no publish date; first "
                f"seen by our watcher {(it.get('first_seen') or '')[:10]}, which is not the announcement date)",
                it['link'])
    stats = inp['stats'] or {}
    for c in [c for c in stats.get('fan_comments', []) if c.get('type')][:30]:
        add('Q', 'fan question', f"{c['text']} (type: {c['type']}; replies: {'yes' if c['has_replies'] else 'no'})",
            c['video'], c['date'][:10])
    for r in inp.get('past_questions', []):
        add('Q', 'fan question (past)', f"{_flat(r['comment_text'], 200)} (type: {r['type']}; {r['likes']} likes; "
            f"on a {r['video_group']} video)", r['video_url'], r['date'][:10])
    own = sorted(inp['own'], key=lambda v: v['date'], reverse=True)
    picked = {v['id']: v for v in own[:12]}
    picked.update({v['id']: v for v in sorted(inp['own'], key=lambda v: -v['views'])[:12]})
    xn = {v['id']: v.get('x_normal') for v in stats.get('videos', [])}
    for v in sorted(picked.values(), key=lambda v: v['date'], reverse=True):
        extra = f", {xn[v['id']]}x the account's normal" if xn.get(v['id']) else ''
        add('O', 'own video', f"{v['views']:,} views, {v['saves']} saves, {v['comments']} comments{extra}. "
            f"Caption: {_flat(v['caption'], 200)}", v['url'], v['date'][:10])
    for o in (inp['peers'] or {}).get('outliers', []):
        add('P', 'peer outlier', f"{o['account']} ({o['country']}, {o['group']}): {o['views']:,} views, "
            f"{o['x_normal']}x its normal, format {o['format']}. Caption: {_flat(o['caption'], 200)}",
            o['url'], o['date'][:10])
    for r in inp['stock']:
        add('K', 'stock', f"{r['item']} · demo unit: {r['demo_unit']} · on hand: {r['on_hand']} · open GO: "
            f"{r['open_go']} · ETA: {r['eta'] or '-'} · price: {r['price_note'] or '-'}", date=r['updated'])
    if inp['studio']:
        add('S', 'tiktok studio', inp['studio'])
    if inp['notes']:
        add('W', 'owner notes', inp['notes'])
    return src


def health_line(inp, today):
    parts = []
    run = inp['news_run']
    if run:
        h = run.get('health', [])
        bad = [f"{x['source']}" for x in h if not x['ok'] or x['count'] == 0]
        age = (today - dt.datetime.fromisoformat(run['run_at']).astimezone(PHT).date()).days
        parts.append(f"news: {len(h) - len(bad)} of {len(h)} sources answered"
                     + (f" (nothing from {', '.join(bad)})" if bad else '')
                     + (f", **last run {age} days ago**" if age > 1 else '')
                     + f", {len(inp['news'])} items kept from the last {NEWS_DAYS} days")
    else:
        parts.append('news: **no news_watch run in the last 8 days**')
    for name, path, d in (('stats', inp['stats_path'], inp['stats']), ('peers', inp['peers_path'], inp['peers'])):
        if not d:
            parts.append(f'{name}: **missing**')
            continue
        age = (now_utc() - dt.datetime.fromisoformat(d['made_at'])).days
        stale = f', **{age} days old**' if age > STALE_DAYS else ''
        if name == 'stats':
            hh = d.get('health', {})
            parts.append(f"stats {d['week']}: {hh.get('tiktok', 0)} TikToks, {hh.get('comments', 0)} with comments, "
                         f"{hh.get('x', 0)} X posts{stale}")
        else:
            got = sum(1 for a in d['accounts'] if a['scraped_now'])
            parts.append(f"peers {d['week']}: {got} of {len(d['accounts'])} shops, {len(d['outliers'])} outliers{stale}")
    sheet = [r for r in inp['stock'] if r.get('from_sheet')]
    hand = [r for r in inp['stock'] if not r.get('from_sheet')]
    upd = max((r['updated'] for r in hand), default='never')
    parts.append(f"stock list: {len(hand)} items, updated {upd}"
                 + (f"; her stock sheet: {len(sheet)} items with slots, read {sheet[0]['updated']}" if sheet
                    else '; **her stock sheet: not found**'))
    parts.append(f"calendar: {len(inp['calendar'])} events now or in the next {SEASON_DAYS} days")
    return ' · '.join(parts)


# ---------- Claude ----------

SYSTEM = """You draft the weekly video brief for Unnie Mart, a small Philippine K-pop group-order (GO) shop on TikTok \
(@unniemart_). The owner films on her phone and posts herself. Andrey reviews every idea before she sees it.

Hard rules:
- Use only the numbered sources you are given. Every idea cites the source ids it rests on.
- Every fact (a date, a version, what a notice says, an app name, a count) goes in `facts`, with `quote` copied \
character for character from that source's text. If you can't quote it from a source, don't claim it anywhere.
- Never invent a number. A price may be written only when copied exactly from a stock source; anything else is \
₱___. Slots left change daily: if a line mentions them, add "re-check slots the day she posts" to `needs`. No view \
predictions.
- `item` is an exact item name from the stock list, or "none". `needs_unit` is true when the video needs that \
physical item or a demo unit on camera. `sells` is true when the video or its pinned comment offers something for sale.
- `offer_keywords`: 1 to 3 short words that would appear in a caption selling the same thing (for the 14-day repeat \
check). Empty when `sells` is false.
- `question_type` is the fan-question type the video answers (from the list), or "none".
- `season` is one of the active seasons, or "none".
- Formats follow the playbook cards. First frame is the real thing; visible payoff in 2 to 4 seconds; say the search \
phrase out loud and on screen. Clinic needs a demo unit and the official manual.
- No AI voices, AI faces, AI images, stock footage or other people's footage. No fake scarcity, no "don't miss out" \
without a real date, no "100% legit", no generic hype, no em dashes, no markdown in captions. 3 to 5 exact hashtags \
with the model name, never #fyp or #viral.
- Captions and on-screen lines are Taglish placeholders the owner rewrites: short, plain, "po" where natural, the \
search phrase in English.
- A source's `note` is our own research note: use it for ideas, never as a fact quote. Undated news items were \
found by our watcher on that day; don't call them new or "just announced".
- Don't re-make a tutorial the shop already has that still earns views (see the TikTok Studio source) unless it's a \
new version or a clearly different problem. A checklist or how-to with a lightstick is a Clinic.
- `season` is the season the video actually serves, not the closest one.
- Respect the owner notes (when she can film, what she has). Don't plan filming on days she can't.
- `why`, `needs` and `post_window` are for Andrey: short, plain English, no jargon.

Propose 6 to 9 different ideas, strongest first, mixing formats. Prefer active seasons, real fan questions and the \
shop's own proven formats. Skip anything you can't source."""


def idea_schema(stock):
    items = ['none'] + [r['item'] for r in stock]
    seasons = ['none'] + [n for n, _, _ in SEASONS]
    s = lambda **kw: {'type': 'string', **kw}  # noqa: E731
    return {
        'type': 'object', 'required': ['ideas'], 'additionalProperties': False,
        'properties': {'ideas': {'type': 'array', 'minItems': 3, 'maxItems': 10, 'items': {
            'type': 'object', 'additionalProperties': False,
            'required': ['title', 'format', 'season', 'why', 'source_ids', 'facts', 'item', 'needs_unit', 'sells',
                         'offer_keywords', 'question_type', 'hook_on_screen', 'shot_list', 'caption',
                         'pinned_comment', 'post_window', 'needs'],
            'properties': {
                'title': s(), 'format': s(enum=FORMATS), 'season': s(enum=seasons), 'why': s(),
                'source_ids': {'type': 'array', 'items': s(), 'minItems': 1},
                'facts': {'type': 'array', 'items': {
                    'type': 'object', 'additionalProperties': False, 'required': ['claim', 'source_id', 'quote'],
                    'properties': {'claim': s(), 'source_id': s(), 'quote': s()}}},
                'item': s(enum=items), 'needs_unit': {'type': 'boolean'}, 'sells': {'type': 'boolean'},
                'offer_keywords': {'type': 'array', 'items': s()},
                'question_type': s(enum=['none'] + QTYPES),
                'hook_on_screen': s(), 'shot_list': {'type': 'array', 'items': s()}, 'caption': s(),
                'pinned_comment': s(), 'post_window': s(), 'needs': {'type': 'array', 'items': s()}}}}}}


def _section(path, start, stop):
    text = path.read_text()
    a = text.find(start)
    b = text.find(stop, a + 1) if a >= 0 else -1
    return text[a:b if b > 0 else None].strip() if a >= 0 else ''


def build_prompt(sources, inp, today, week, monday, sunday, active):
    playbook = _section(ROOT / 'strategy' / 'PLAYBOOK.md', '## Rules for every video', '## Caption template')
    season_pb = _section(ROOT / 'strategy' / 'STRATEGY.md', '## 3. The season playbook', '## 4.')
    stats = inp['stats'] or {}
    sb = stats.get('scoreboard', {})
    q_counts = dict(stats.get('question_types', {}))
    for k, v in inp['tally'].items():
        q_counts[k] = q_counts.get(k, 0) + v
    return (f"Today is {today:%A %b %d, %Y} in the Philippines. The brief is for {week} "
            f"({monday:%b %d} to {sunday:%b %d}).\n"
            f"Active seasons this week: {', '.join(active) or 'none'}.\n"
            f"Fan-question types (from the list): {', '.join(QTYPES)}.\n"
            f"Fan questions counted this week: {json.dumps(q_counts)}.\n"
            f"Account scoreboard: {json.dumps(sb)}.\n\n"
            f"# Playbook (format cards)\n\n{playbook}\n\n# Season playbook\n\n{season_pb}\n\n"
            f"# Sources\n\n{json.dumps(sources, ensure_ascii=False, indent=0)}\n")


def model_label(requested, used):
    """The model that wrote the ideas. `claude` also uses a small model for background chores; leave that out."""
    return requested if requested in used or not used else ', '.join(used)


def call_claude(prompt, schema, model=MODEL, timeout=CLAUDE_TIMEOUT_S):
    """One `claude -p` call: no tools, no MCP servers, no saved session, structured output."""
    cmd = ['claude', '-p', '--model', model, '--tools', '', '--strict-mcp-config', '--no-session-persistence',
           '--system-prompt', SYSTEM, '--output-format', 'json', '--json-schema', json.dumps(schema)]
    with tempfile.TemporaryDirectory() as tmp:      # neutral folder: no project files or CLAUDE.md in reach
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd=tmp)
    if p.returncode != 0:
        raise RuntimeError(f'claude exited {p.returncode}: {(p.stderr or p.stdout)[-500:]}')
    out = json.loads(p.stdout)
    if out.get('is_error') or not out.get('structured_output'):
        raise RuntimeError(f"claude returned no ideas: {str(out.get('result'))[:500]}")
    meta = {k: out.get(k) for k in ('duration_ms', 'num_turns', 'session_id')}
    meta['models'] = sorted((out.get('modelUsage') or {}).keys())
    return out['structured_output'], meta


# ---------- output ----------

def _src_links(idea, sources):
    out = []
    for i in idea.get('source_ids', []):
        s = sources.get(i)
        if s:
            out.append(f"[{i}]({s['url']})" if s['url'] else i)
    return ', '.join(out)


def _idea_md(n, idea, sources, full=True):
    r = idea['_rank']
    L = [f"### {n} · {idea['title']}", '',
         f"{idea['format']} · {idea['season'] if idea['season'] != 'none' else 'no season'} · "
         f"fan questions: {r['questions']}{' (' + idea['question_type'] + ')' if idea['question_type'] != 'none' else ''}"
         f" · sources: {_src_links(idea, sources)}", '',
         f"- **Why:** {idea['why']}"]
    if idea['_gate']['problems']:
        L.append('- **Blocked because:** ' + '; '.join(idea['_gate']['problems']))
    if idea.get('facts'):
        L.append('- **Facts to tick against the source:**')
        for f in idea['facts']:
            s = sources.get(f['source_id'])
            link = f" ([{f['source_id']}]({s['url']}))" if s and s['url'] else f" ({f['source_id']})"
            L.append(f"  - [ ] {f['claim']} Source says: \"{f['quote']}\"{link}")
    if full:
        L.append(f"- **On screen, first 2 s:** {idea['hook_on_screen']}")
        L.append('- **Shot list:**')
        L += [f'  {i}. {step}' for i, step in enumerate(idea['shot_list'], 1)]
        L.append(f"- **Caption (placeholder):** {idea['caption']}")
        if idea.get('pinned_comment'):
            L.append(f"- **Pinned comment (placeholder):** {idea['pinned_comment']}")
        L.append(f"- **Post:** {idea['post_window']}")
    if idea.get('needs'):
        L.append('- **Needs:** ' + '; '.join(idea['needs']))
    if idea['_gate']['warnings']:
        L.append('- **Check:** ' + '; '.join(idea['_gate']['warnings']))
    return L + ['']


def brief_md(week, monday, sunday, ideas, sources, health, now, model):
    by = {k: [i for i in ideas if i['_gate']['status'] == k] for k in ('ready', 'held', 'waiting', 'dropped')}
    ready = by['ready'][:MAX_READY]
    spare = by['ready'][MAX_READY:]
    L = [f"# Weekly brief · {week} ({monday:%b %d} to {sunday:%b %d})", '',
         f"Draft for Andrey, made {now.astimezone(PHT):%Y-%m-%d %H:%M} PHT by `automations/weekly_brief.py` "
         f"(Claude {model}). Nothing here goes to the owner until you've checked it.", '',
         f"**Sources:** {health}.", '',
         f"**Ideas:** {len(ideas)} drafted · {len(by['ready'])} passed every check · {len(by['held'])} blocked by "
         f"the slop gate · {len(by['waiting'])} waiting on stock · {len(by['dropped'])} dropped (no source).", '',
         '**Before you send:** tick every fact against its source (open the link; news items are headlines only). '
         'Taglish lines are placeholders for her to rewrite. Prices come only from her stock list; re-check them the '
         'day she posts.', '',
         f"## This week (ranked: season, then fan questions, then format evidence; core 3 = the first 3)", '']
    if not ready:
        L += ['Nothing passed every check this week. See the blocked list below.', '']
    for n, idea in enumerate(ready, 1):
        L += _idea_md(n, idea, sources)
    if spare:
        L += ['## Also passed (if there is time)', '']
        for n, idea in enumerate(spare, len(ready) + 1):
            L += _idea_md(n, idea, sources)
    if by['waiting']:
        L += ['## Waiting on stock', '']
        for idea in by['waiting']:
            L += _idea_md('·', idea, sources, full=False)
    if by['held']:
        L += ['## Blocked by the slop gate (fix, or drop)', '']
        for idea in by['held']:
            L += _idea_md('·', idea, sources)
    if by['dropped']:
        L += ['## Dropped (no real source)', ''] + [f"- {i['title']}" for i in by['dropped']] + ['']
    L += ['## Sources used', '']
    used = {i for idea in ideas for i in idea.get('source_ids', [])} | {
        f['source_id'] for idea in ideas for f in idea.get('facts', [])}
    for s in sources.values():
        if s['id'] in used:
            text = re.sub(r'\s+', ' ', s['text'])[:180]
            L.append(f"- **{s['id']}** ({s['kind']}{', ' + s['date'] if s['date'] else ''}): {text}"
                     + (f" [link]({s['url']})" if s['url'] else ''))
    return '\n'.join(L) + '\n'


def telegram_text(week, ideas, path):
    ready = [i for i in ideas if i['_gate']['status'] == 'ready'][:3]
    held = sum(1 for i in ideas if i['_gate']['status'] == 'held')
    lines = [f'<b>Weekly brief {week}</b>: {len(ready)} ready to review, {held} blocked by the slop gate.']
    lines += [f"{n}. {esc(i['title'])} ({esc(i['format'])})" for n, i in enumerate(ready, 1)]
    lines.append(f'File: {esc(str(path.relative_to(ROOT)))}')
    return '\n'.join(lines)


# ---------- main ----------

def check_all(ideas, sources_list, inp, today):
    sources = {s['id']: s for s in sources_list}
    active = active_seasons(today)
    cutoff = (dt.datetime.combine(today, dt.time(), PHT) - dt.timedelta(days=REPEAT_DAYS)).isoformat()
    own_recent = [v for v in inp['own'] if v['date'] >= cutoff]
    q_counts = dict((inp['stats'] or {}).get('question_types', {}))
    for k, v in inp['tally'].items():
        q_counts[k] = q_counts.get(k, 0) + v
    for idea in ideas:
        idea['_gate'] = gate(idea, sources, inp['stock'], own_recent, active)
        idea['_key'], idea['_rank'] = rank_key(idea, sources, q_counts, active)
    ideas.sort(key=lambda i: i['_key'])         # stable: Claude's order breaks ties
    return sources


def brief_name(week, ideas_dir=IDEAS_DIR):
    """'2026-W43', or '2026-W43-v2' if that brief exists already (Andrey may have ticked boxes in it)."""
    name, n = week, 2
    while (ideas_dir / f'{name}.md').exists():
        name, n = f'{week}-v{n}', n + 1
    return name


def main(argv=None):
    ap = argparse.ArgumentParser(description='Weekly brief for Unnie Mart')
    ap.add_argument('--dry-run', action='store_true', help="build the prompt and stop; don't call Claude")
    ap.add_argument('--from-json', help='re-check and re-render a saved data/briefs/*.json (no Claude call)')
    ap.add_argument('--model', default=MODEL)
    ap.add_argument('--no-telegram', action='store_true')
    a = ap.parse_args(argv)
    load_env()

    now = now_utc()
    today = now.astimezone(PHT).date()
    week, monday, sunday = target_week(today)
    inp = load_inputs(today)
    active = active_seasons(monday)
    if a.from_json:
        saved = json.loads(Path(a.from_json).read_text())
        sources_list, raw, meta = saved['sources'], saved['raw_ideas'], saved.get('claude', {})
        week, name = saved['week'], Path(a.from_json).stem   # a re-render replaces its own file on purpose
        model = model_label(a.model, meta['models']) if meta.get('models') else saved.get('model', a.model)
        monday, sunday = dt.date.fromisoformat(saved['monday']), dt.date.fromisoformat(saved['sunday'])
    else:
        sources_list = build_sources(inp, now)
        prompt = build_prompt(sources_list, inp, today, week, monday, sunday, active)
        if a.dry_run:
            print(prompt)
            print(f'--- {len(sources_list)} sources, {len(prompt):,} characters. Not sent.', file=sys.stderr)
            return 0
        name = brief_name(week)
        print(f'{week}: asking Claude ({a.model}) with {len(sources_list)} sources...', file=sys.stderr)
        raw, meta = call_claude(prompt, idea_schema(inp['stock']), a.model)
        model = model_label(a.model, meta['models'])
        save_json(BRIEFS_DIR / f'{name}.json', {        # saved first, so a later error can't lose Claude's answer
            'week': week, 'monday': monday.isoformat(), 'sunday': sunday.isoformat(), 'made_at': now.isoformat(),
            'model': model, 'claude': meta, 'sources': sources_list, 'raw_ideas': raw})
    ideas = json.loads(json.dumps(raw['ideas']))
    sources = check_all(ideas, sources_list, inp, today)
    health = health_line(inp, today)
    md = brief_md(week, monday, sunday, ideas, sources, health, now, model)
    out = IDEAS_DIR / f'{name}.md'
    out.write_text(md)
    save_json(BRIEFS_DIR / f'{name}.json', {
        'week': week, 'monday': monday.isoformat(), 'sunday': sunday.isoformat(), 'made_at': now.isoformat(),
        'model': model, 'claude': meta, 'health': health, 'sources': sources_list, 'raw_ideas': raw,
        'checked': [{'title': i['title'], **i['_gate'], **i['_rank']} for i in ideas],
        **({'hand_edits': saved['hand_edits']} if a.from_json and saved.get('hand_edits') else {})})
    counts = {k: sum(1 for i in ideas if i['_gate']['status'] == k) for k in ('ready', 'held', 'waiting', 'dropped')}
    print(f"{week}: {len(ideas)} ideas · {counts} · {out.relative_to(ROOT)}")
    if not a.no_telegram and not a.from_json:
        telegram_send(telegram_text(week, ideas, out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
