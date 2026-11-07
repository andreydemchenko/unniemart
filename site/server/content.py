"""Everything the site shows that isn't orders: the weekly video briefs, numbers, news, dates, video covers and the
documents.

All of it is read from the project files (on the server: the copy the laptop pushes). Nothing here is written.
The weekly brief is read from its .md file, not the .json, because hand fixes go into the .md.
"""
import csv
import datetime as dt
import json
import re
from pathlib import Path

import settings

IDEA_FIELDS = {
    'why': 'why', 'blocked because': 'blocked', 'facts to tick against the source': 'facts',
    'on screen, first 2 s': 'hook', 'shot list': 'shots', 'caption (placeholder)': 'caption',
    'pinned comment (placeholder)': 'pinned', 'post': 'post', 'needs': 'needs',
}
SECTIONS = [('this week', 'main'), ('also passed', 'also'), ('waiting on stock', 'waiting')]
DOC_GROUPS = [
    ('Strategy', ['strategy/STRATEGY.md', 'strategy/PLAYBOOK.md', 'content/ideas/call-clips-plan.md',
              'content/ideas/2026-10-W42-W44.md']),
    ('Her answers', ['strategy/OWNER-ANSWERS.md', 'data/owner/notes.md', 'data/owner/studio/summary.md',
                     'strategy/OWNER-QUESTIONS.md']),
    ('Research', ['research/*.md']),
    ('How it works', ['strategy/AUTOMATION.md', 'automations/README.md']),
    ('Drafts', ['content/drafts/*.md']),                 # Andrey only
]
ADMIN_GROUPS = {'Drafts'}
TITLES = {'data/owner/studio/summary.md': 'TikTok Studio numbers she shared'}
BRIEF = re.compile(r'^(\d{4}-W\d{2})(?:-v(\d+))?\.md$')


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60]


def _link_ids(text):
    """'K3, W1, [C52](https://…)' → [{'id': 'K3', 'url': ''}, {'id': 'C52', 'url': 'https://…'}]."""
    out = []
    for part in re.split(r',\s*', text.strip()):
        m = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part.strip())
        out.append({'id': m.group(1), 'url': m.group(2)} if m else {'id': part.strip(), 'url': ''})
    return [x for x in out if x['id']]


def _fact(text):
    """'[ ] Claim. Source says: "quote" ([C52](url))' → {'claim', 'quote', 'src', 'url'}."""
    text = re.sub(r'^\[[ xX]\]\s*', '', text.strip())
    m = re.match(r'(?P<claim>.*?)\s*Source says:\s*"(?P<quote>.*)"\s*\((?P<src>.*)\)\s*$', text)
    if not m:
        return {'claim': text, 'quote': '', 'src': '', 'url': ''}
    src = _link_ids(m.group('src'))
    return {'claim': m.group('claim').strip(), 'quote': m.group('quote'),
            'src': src[0]['id'] if src else '', 'url': src[0]['url'] if src else ''}


def parse_brief(text, week=''):
    """A weekly brief (.md from automations/weekly_brief.py) → its ideas, each with every field."""
    title = re.search(r'^# (.+)$', text, re.M)
    rng = re.search(r'\(([A-Z][a-z]{2} \d{1,2}) to ([A-Z][a-z]{2} \d{1,2})\)', title.group(1) if title else '')
    out = {'week': week, 'title': title.group(1) if title else week, 'range': rng.group(0)[1:-1] if rng else '',
           'ideas': [], 'sources': {}}
    section, idea, field = None, None, None
    for line in text.splitlines():
        if line.startswith('## '):
            h = line[3:].lower()
            section = next((v for k, v in SECTIONS if h.startswith(k)), 'sources' if h.startswith('sources') else None)
            idea = None
            continue
        if section == 'sources':
            m = re.match(r'- \*\*(\w+)\*\* \(([^)]*)\): (.*)$', line)
            if m:
                link = re.search(r'\[link\]\(([^)]+)\)\s*$', m.group(3))
                kind, _, date = m.group(2).partition(', ')
                out['sources'][m.group(1)] = {'kind': kind, 'date': date,
                                              'text': re.sub(r'\s*\[link\]\([^)]+\)\s*$', '', m.group(3)),
                                              'url': link.group(1) if link else ''}
            continue
        if section is None:
            continue
        m = re.match(r'### (?:(\d+) · |· · )(.+)$', line)
        if m:
            idea = {'n': int(m.group(1)) if m.group(1) else None, 'title': m.group(2).strip(), 'section': section,
                    'format': '', 'season': '', 'questions': '', 'sources': [], 'why': '', 'blocked': '',
                    'facts': [], 'hook': '', 'shots': [], 'caption': '', 'pinned': '', 'post': '', 'needs': []}
            idea['key'] = f'{week}:{slug(idea["title"])}'
            out['ideas'].append(idea)
            field = None
            continue
        if idea is None or not line.strip():
            continue
        if not line.startswith((' ', '-')) and not idea['format']:            # the meta line under the title
            parts = [p.strip() for p in line.split(' · ')]
            idea['format'] = parts[0]
            idea['season'] = parts[1] if len(parts) > 1 else ''
            for p in parts[2:]:
                if p.startswith('fan questions:'):
                    idea['questions'] = p.split(':', 1)[1].strip()
                elif p.startswith('sources:'):
                    idea['sources'] = _link_ids(p.split(':', 1)[1])
            continue
        m = re.match(r'- \*\*(.+?):\*\*\s*(.*)$', line)
        if m:
            field = IDEA_FIELDS.get(m.group(1).lower())
            rest = m.group(2).strip()
            if field == 'needs':
                idea['needs'] = [n.strip() for n in rest.split(';') if n.strip()]
            elif field in ('why', 'blocked', 'hook', 'caption', 'pinned', 'post'):
                idea[field] = rest
            continue
        m = re.match(r'\s+(?:- |\d+\. )(.*)$', line)
        if m and field == 'facts':
            idea['facts'].append(_fact(m.group(1)))
        elif m and field == 'shots':
            idea['shots'].append(m.group(1).strip())
    for i in out['ideas']:                       # source ids → full source, for the "why" list
        for s in i['sources']:
            s.update({k: v for k, v in out['sources'].get(s['id'], {}).items() if k != 'url' or not s['url']})
    return out


def briefs(root=None):
    """Every week's latest brief, newest first."""
    root = Path(root or settings.CONTENT)
    best = {}
    for p in (root / 'content' / 'ideas').glob('*.md'):
        m = BRIEF.match(p.name)
        if m:
            v = int(m.group(2) or 1)
            if m.group(1) not in best or v > best[m.group(1)][0]:
                best[m.group(1)] = (v, p)
    out = []
    for week, (v, p) in sorted(best.items(), reverse=True):
        b = parse_brief(p.read_text(), week)
        b['file'] = str(p.relative_to(root))
        b['version'] = v
        y, w = int(week[:4]), int(week[-2:])
        monday = dt.date.fromisocalendar(y, w, 1)
        b['monday'], b['sunday'] = monday.isoformat(), (monday + dt.timedelta(days=6)).isoformat()
        out.append(b)
    return out


def _latest_json(folder, pattern='*.json'):
    files = sorted(Path(folder).glob(pattern))
    if not files:
        return None
    try:
        return json.loads(files[-1].read_text())
    except ValueError:
        return None


def stats(root=None):
    root = Path(root or settings.CONTENT)
    s = _latest_json(root / 'data' / 'stats')
    if not s:
        return None
    keep = ('id', 'date', 'url', 'views', 'likes', 'comments', 'shares', 'saves', 'x_normal', 'normal', 'format',
            'caption', 'flag', 'pinned')
    vids = [{k: v.get(k) for k in keep} for v in s.get('videos', [])]
    for v in vids:
        v['caption'] = (v['caption'] or '').split('\n')[0][:160]
    x = s.get('x') or {}
    return {'week': s.get('week'), 'made_at': s.get('made_at'), 'videos': vids,
            'scoreboard': s.get('scoreboard') or {}, 'fan_comments': s.get('fan_comments') or [],
            'question_types': s.get('question_types') or {},
            'x': {'median_views': x.get('median_views'),
                  'posts': [{k: p.get(k) for k in ('date', 'url', 'views', 'likes', 'replies', 'text')}
                            for p in x.get('posts', [])]}}


def peers(root=None):
    root = Path(root or settings.CONTENT)
    p = _latest_json(root / 'data' / 'peers')
    if not p:
        return None
    keep = ('account', 'group', 'country', 'url', 'views', 'saves', 'x_normal', 'format', 'caption', 'date')
    out = [{k: o.get(k) for k in keep} for o in p.get('outliers', [])]
    for o in out:
        o['caption'] = (o['caption'] or '').split('\n')[0][:160]
    return {'week': p.get('week'), 'made_at': p.get('made_at'), 'outliers': out,
            'accounts': len(p.get('accounts', []))}


def news(root=None, days=21):
    root = Path(root or settings.CONTENT)
    n = _latest_json(root / 'data' / 'news', '2*.json')
    if not n:
        return []
    cut = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()
    items = []
    for i in n.get('items', []):
        when = i.get('published') or i.get('first_seen') or ''
        if when and when < cut:
            continue
        items.append({'title': i.get('title', '')[:240], 'link': i.get('link'), 'source': i.get('source', ''),
                      'kind': i.get('kind'), 'when': when, 'groups': i.get('groups') or [],
                      'urgent': i.get('priority') == 'urgent', 'reason': i.get('reason', '')})
    items.sort(key=lambda i: i['when'], reverse=True)
    return items[:120]


def _date(s, end=False):
    s = (s or '').strip()
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
            return dt.date.fromisoformat(s)
        if re.fullmatch(r'\d{4}-\d{2}', s):
            y, m = map(int, s.split('-'))
            if end:
                return dt.date(y + m // 12, m % 12 + 1, 1) - dt.timedelta(days=1)
            return dt.date(y, m, 1)
    except ValueError:
        return None
    return None


def calendar(root=None, today=None):
    """Upcoming and ongoing events from data/calendar.csv, plus the call-clip posting dates."""
    root = Path(root or settings.CONTENT)
    today = today or dt.date.today()
    out = []
    path = root / 'data' / 'calendar.csv'
    if path.exists():
        with path.open() as f:
            for r in csv.DictReader(f):
                a = _date(r.get('date_start'))
                b = _date(r.get('date_end'), end=True) or _date(r.get('date_start'), end=True)
                if not a or (b or a) < today - dt.timedelta(days=1):
                    continue
                out.append({'start': a.isoformat(), 'end': b.isoformat() if b and b != a else None,
                            'month_only': len((r.get('date_start') or '').strip()) == 7,
                            'group': r.get('group', ''), 'type': r.get('event_type', ''), 'title': r.get('title', ''),
                            'where': '' if (r.get('location') or '').strip() in ('-', '–', 'n/a', 'TBA') else r.get('location', ''), 'url': r.get('source_url', ''),
                            'sure': r.get('confidence', ''), 'angle': r.get('content_angle', ''), 'kind': 'event'})
    clips = root / 'content' / 'ideas' / 'call-clips-plan.md'
    if clips.exists():
        for m in re.finditer(r'^\| ([A-Z][a-z]{2}) (\d{1,2})[^|]*\| ([^|]+)\| ([^|]+)\|', clips.read_text(), re.M):
            try:
                d = dt.datetime.strptime(f'{m.group(1)} {m.group(2)} {today.year}', '%b %d %Y').date()
            except ValueError:
                continue
            if d < today - dt.timedelta(days=1):
                d = d.replace(year=today.year + 1)
            who = m.group(3).strip()
            out.append({'start': d.isoformat(), 'end': None, 'month_only': False, 'group': 'ENHYPEN',
                        'type': 'post', 'title': f'Post a call clip: {who}', 'where': '', 'url': '',
                        'sure': 'high', 'angle': m.group(4).strip(), 'kind': 'post'})
    out.sort(key=lambda e: (e['start'], e['title']))
    return out


def studio(root=None):
    """Her TikTok Studio screenshots as summed up in data/owner/studio/summary.md (account-wide, last 365 days):
    where views come from and where viewers are. Updated by hand when she sends new screenshots."""
    path = Path(root or settings.CONTENT) / 'data' / 'owner' / 'studio' / 'summary.md'
    if not path.exists():
        return None
    text = path.read_text()

    def shares(label):
        m = re.search(rf'^{label}:\s*(.+)$', text, re.M | re.I)
        out = []
        for part in (m.group(1).rstrip('.').split(',') if m else []):
            mm = re.match(r'\s*(.+?)\s+([\d.]+)%\s*$', part)
            if mm:
                out.append({'name': mm.group(1), 'pct': float(mm.group(2))})
        return out
    period = re.search(r'\(([^)]*\d{4}[^)]*)\)', text)
    views = re.search(r'Post views ([\d.,]+K?)', text)
    shared = re.search(r'shared by the owner on (\d{4}-\d{2}-\d{2})', text)
    return {'period': period.group(1) if period else '', 'views': views.group(1) if views else None,
            'shared': shared.group(1) if shared else None,
            'sources': shares('Traffic source'), 'places': shares('Viewer locations')}


def owner_stock(root=None):
    path = Path(root or settings.CONTENT) / 'data' / 'owner' / 'stock.csv'
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def _title(p):
    try:
        for line in p.read_text().splitlines():
            if line.startswith('# '):
                return line[2:].strip()
    except OSError:
        pass
    return p.stem.replace('-', ' ')


def plan(root=None):
    """The plan on one screen (strategy/plan.json): the strategy in a line, the weekly mix, what's coming, the rules."""
    p = Path(root or settings.CONTENT) / 'strategy' / 'plan.json'
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return None


def media(root=None):
    """The videos the site can show with a picture (automations/media.py): {id: caption, views, files...}. Files are
    served from /media/ (signed in only)."""
    idx = Path(root or settings.CONTENT) / 'data' / 'media' / 'index.json'
    try:
        raw = json.loads(idx.read_text())
    except (OSError, ValueError):
        return {}
    keep = ('acc', 'url', 'cap', 'views', 'likes', 'comments', 'date', 'dur', 'mine', 'thumb', 'video', 'color', 'w',
            'h')
    return {vid: {k: v[k] for k in keep if v.get(k) not in (None, '')} for vid, v in raw.items()
            if isinstance(v, dict) and v.get('thumb')}


def docs(root=None, admin=False):
    root = Path(root or settings.CONTENT)
    out, seen = [], set()
    for group, pats in DOC_GROUPS:
        if group in ADMIN_GROUPS and not admin:
            continue
        for pat in pats:
            for p in sorted(root.glob(pat)):
                rel = str(p.relative_to(root))
                if rel in seen or not p.is_file():
                    continue
                seen.add(rel)
                text = p.read_text()
                out.append({'id': rel, 'title': TITLES.get(rel) or _title(p), 'group': group, 'words': len(text.split()),
                            'updated': dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat()})
    return out


def doc(rel, root=None, admin=False):
    """One document's text, only if it's in the list (no other files can be read this way)."""
    allowed = {d['id'] for d in docs(root, admin)}
    if rel not in allowed:
        return None
    return (Path(root or settings.CONTENT) / rel).read_text()


def watched(root=None):
    """A fingerprint of every file this module reads (name, time, size), to know when to send the page an update.
    Any change counts, also a file that arrives with an older time than the rest (rsync keeps the laptop's times)."""
    root = Path(root or settings.CONTENT)
    pats = ['content/ideas/*.md', 'data/stats/*.json', 'data/peers/*.json', 'data/news/*.json', 'data/calendar.csv',
            'data/owner/*.csv', 'data/owner/*.md', 'data/owner/studio/*.md', 'strategy/*.md', 'strategy/plan.json',
            'research/*.md',
            'content/drafts/*.md', 'automations/README.md', 'data/media/index.json']
    seen = []
    for pat in pats:
        for p in root.glob(pat):
            try:
                st = p.stat()
                seen.append((str(p), st.st_mtime_ns, st.st_size))
            except OSError:
                pass
    return hash(tuple(sorted(seen)))


def everything(root=None, admin=False, today=None):
    return {'briefs': briefs(root), 'stats': stats(root), 'peers': peers(root), 'news': news(root),
            'calendar': calendar(root, today), 'docs': docs(root, admin), 'demo': owner_stock(root),
            'studio': studio(root), 'plan': plan(root), 'media': media(root)}
