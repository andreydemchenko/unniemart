"""The Unnie Mart website: one page (site/web) and the small API behind it.

Run on the server by systemd (site/deploy/unniemart.service):
  uvicorn app:app --host 127.0.0.1 --port 8821 --proxy-headers
On the laptop, to try it with a stand-in sheet:
  UM_FAKE=path/to/fake.xlsx UM_STATE=/tmp/um uvicorn app:app --app-dir site/server --port 8821

Every request except login needs a signed-in device. Changes need the header X-UM: 1 (a page on another site can't
send it), so only this page can change anything.
"""
import asyncio
import datetime as dt
import hashlib
import json
import re
import secrets
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response

import auth
import settings
import content
import desk as desk_mod
import google_sheet as gs
import store as store_mod

COOKIE = 'um'


class Pulse:
    """A number that goes up whenever anything the page shows changes; pages wait on it (long poll)."""

    def __init__(self):
        self.v, self.cv = 1, 1
        self.loop, self.event = None, None

    def bind(self, loop):
        self.loop, self.event = loop, asyncio.Event()

    def bump(self, content=False):
        self.v += 1
        if content:
            self.cv += 1
        if self.loop:
            self.loop.call_soon_threadsafe(self._wake)

    def _wake(self):
        self.event.set()
        self.event = asyncio.Event()

    async def wait(self, v, cv, timeout=25):
        if v != self.v or cv != self.cv or self.event is None:
            return
        try:
            await asyncio.wait_for(self.event.wait(), timeout)
        except asyncio.TimeoutError:
            pass


def make_source():
    if settings.FAKE:
        from fake import FakeSheet
        return FakeSheet(settings.FAKE)
    sid = gs.sheet_id(settings.sheet_link())
    return desk_mod.AutoSource(sid, settings.GOOGLE_KEY) if sid else None


class Site:
    def __init__(self, source=None):
        self.users = auth.load_users()
        self.store = store_mod.Store(settings.DB)
        self.pulse = Pulse()
        names = {u: v.get('name', u) for u, v in self.users.items()}
        self.desk = desk_mod.Desk(source if source is not None else make_source(), self.store, self.pulse.bump, names)
        self.throttle = auth.Throttle()
        self.content_mtime = 0.0
        self.content_cache = {}
        self.stop = threading.Event()

    def loop(self):
        """Background: re-read her sheet when it changes, notice new content."""
        self.desk.tick(force=True)
        last_files = 0.0
        while not self.stop.is_set():
            try:
                self.desk.tick()
                if time.time() - last_files > settings.CHECK_CONTENT_S:
                    last_files = time.time()
                    m = content.watched()
                    if m != self.content_mtime:
                        self.content_mtime = m
                        self.content_cache = {}
                        self.pulse.bump(content=True)
            except Exception as e:                                     # noqa: BLE001  keep the loop alive
                print('loop:', type(e).__name__, e, flush=True)
            self.stop.wait(2)

    def content_for(self, admin):
        if admin not in self.content_cache:
            today = desk_mod.today_pht()
            self.content_cache[admin] = content.everything(admin=admin, today=today)
        return self.content_cache[admin]


site = None


@asynccontextmanager
async def lifespan(_app):
    global site
    if site is None:
        site = Site()
    site.pulse.bind(asyncio.get_running_loop())
    threading.Thread(target=site.loop, daemon=True).start()
    yield
    site.stop.set()


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)


# ---------- helpers ----------

def me(request):
    token = request.cookies.get(COOKIE)
    uid = site.store.session_user(auth.token_hash(token), settings.SESSION_DAYS) if token else None
    if not uid or uid not in site.users:
        raise HTTPException(401, 'Sign in first.')
    return uid


def admin(uid):
    return site.users.get(uid, {}).get('role') == 'admin'


def guard(request):
    """For anything that changes data: signed in, and sent by this page."""
    if request.headers.get('x-um') != '1':
        raise HTTPException(403, 'Not allowed.')
    origin = request.headers.get('origin')
    if origin and origin.split('://')[-1] != request.headers.get('host'):
        raise HTTPException(403, 'Not allowed.')
    return me(request)


async def body(request):
    try:
        b = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(400, 'Bad request.') from None
    if not isinstance(b, dict):
        raise HTTPException(400, 'Bad request.')
    return b


def whole(v, default=0):
    """A whole number from the page, or a clear 400 instead of a crash."""
    try:
        return int(v if v is not None else default)
    except (TypeError, ValueError):
        raise HTTPException(400, 'Bad request.') from None


def run(fn, *a, **k):
    """Run a sheet write in a thread (Google can take a few seconds); turn its errors into a message."""
    async def go():
        try:
            return await asyncio.to_thread(fn, *a, **k)
        except desk_mod.DeskError as e:
            raise HTTPException(409, str(e)) from None
        except gs.GoogleError as e:
            raise HTTPException(502, f'Google: {e}') from None
    return go()


@app.exception_handler(HTTPException)
async def http_error(request, exc):
    return JSONResponse({'error': exc.detail}, status_code=exc.status_code)


# ---------- signing in ----------

@app.post('/api/login')
async def login(request: Request):
    ip = request.headers.get('x-forwarded-for', request.client.host if request.client else '').split(',')[0]
    if site.throttle.blocked(ip):
        raise HTTPException(429, 'Too many tries. Wait 15 minutes.')
    b = await body(request)
    site.users = auth.load_users() or site.users
    uid = await asyncio.to_thread(auth.who_is, str(b.get('password', ''))[:100], site.users)
    if not uid:
        site.throttle.fail(ip)
        raise HTTPException(401, "That password didn't work.")
    token = secrets.token_urlsafe(32)
    site.store.session_add(auth.token_hash(token), uid, request.headers.get('user-agent'))
    r = JSONResponse({'me': profile(uid)})
    r.set_cookie(COOKIE, token, max_age=settings.SESSION_DAYS * 86400, httponly=True, samesite='lax',
                 secure=request.url.scheme == 'https', path='/')
    return r


@app.post('/api/logout')
async def logout(request: Request):
    token = request.cookies.get(COOKIE)
    if token:
        site.store.session_end(auth.token_hash(token))
    r = JSONResponse({'ok': True})
    r.delete_cookie(COOKIE, path='/')
    return r


def profile(uid):
    u = site.users.get(uid, {})
    return {'id': uid, 'name': u.get('name', uid), 'admin': u.get('role') == 'admin'}


@app.get('/api/me')
async def get_me(request: Request):
    return {'me': profile(me(request))}


# ---------- reading ----------

@app.get('/api/state')
async def state(request: Request):
    uid = me(request)
    d = site.desk.snapshot()
    if not admin(uid):
        d = {**d, 'sheet': {k: v for k, v in d['sheet'].items() if k not in ('robot', 'robot_error')}}
    return {'v': site.pulse.v, 'cv': site.pulse.cv, 'me': profile(uid), 'desk': d,
            'loading': site.desk.read_at is None and site.desk.error is None,
            'tasks': site.store.tasks(), 'ideas': site.store.ideas(), 'activity': site.store.activity(),
            'photos': site.store.photos(), 'people': {u: v.get('name', u) for u, v in site.users.items()}}


@app.get('/api/content')
async def get_content(request: Request):
    uid = me(request)
    return {'cv': site.pulse.cv, **site.content_for(admin(uid))}


@app.get('/api/wait')
async def wait(request: Request, v: int = 0, cv: int = 0):
    me(request)
    await site.pulse.wait(v, cv)
    return {'v': site.pulse.v, 'cv': site.pulse.cv}


@app.get('/api/go')
async def go(request: Request, tab: str):
    me(request)
    return {'lines': site.desk.go_lines(tab)}


@app.get('/api/history')
async def history(request: Request, tab: str, user: str):
    me(request)
    return {'changes': site.store.changes_for(tab, user)}


@app.get('/api/doc')
async def get_doc(request: Request, id: str):
    uid = me(request)
    text = content.doc(id, admin=admin(uid))
    if text is None:
        raise HTTPException(404, 'Not found.')
    return {'id': id, 'text': text}


@app.get('/api/payments')
async def payments(request: Request, tab: str, r: int, user: str, item: str = None):
    """Each payment on one order line, as she wrote them in the Payment cell (=500+2650 → 500, 2650)."""
    me(request)
    return await run(site.desk.payments, tab, r, user, item)


# ---------- changing her sheet ----------

@app.post('/api/pay')
async def pay(request: Request):
    uid = guard(request)
    b = await body(request)
    out = await run(site.desk.pay, uid, b.get('tab'), whole(b.get('r')), b.get('user', ''), b.get('amount'),
                    b.get('item'), str(b.get('req') or '')[:64] or None)
    return out


@app.post('/api/undo')
async def undo(request: Request):
    uid = guard(request)
    b = await body(request)
    return await run(site.desk.undo, uid, whole(b.get('change')))


@app.post('/api/remind')
async def remind(request: Request):
    uid = guard(request)
    b = await body(request)
    return await run(site.desk.remind, uid, b.get('tab'), whole(b.get('r')), b.get('user', ''), b.get('item'))


@app.post('/api/edit')
async def edit(request: Request):
    uid = guard(request)
    b = await body(request)
    return await run(site.desk.edit, uid, b.get('tab'), whole(b.get('r')), b.get('user', ''),
                     b.get('field'), b.get('value', ''), b.get('item'))


@app.post('/api/slot')
async def slot(request: Request):
    uid = guard(request)
    b = await body(request)
    return await run(site.desk.slot, uid, whole(b.get('r')), b.get('raw', ''), whole(b.get('delta'), 1),
                     b.get('taker', ''))


# ---------- tasks and videos ----------

def _date_or_none(s):
    try:
        return dt.date.fromisoformat(s).isoformat() if s else None
    except ValueError:
        raise HTTPException(400, 'Pick a date.') from None


@app.post('/api/tasks')
async def task_add(request: Request):
    uid = guard(request)
    b = await body(request)
    title = ' '.join(str(b.get('title', '')).split())[:300]
    if not title:
        raise HTTPException(400, 'Write the task first.')
    tid = site.store.run('insert into tasks (title, who, due, note, created_at, created_by) values (?,?,?,?,?,?)',
                         (title, b.get('who') if b.get('who') in site.users else None, _date_or_none(b.get('due')),
                          str(b.get('note', ''))[:2000], store_mod.now(), uid))
    site.pulse.bump()
    return {'id': tid}


@app.post('/api/tasks/{tid}')
async def task_change(request: Request, tid: int):
    uid = guard(request)
    b = await body(request)
    rows = site.store.q('select * from tasks where id = ?', (tid,))
    if not rows:
        raise HTTPException(404, 'That task is gone.')
    t = rows[0]
    if b.get('delete'):
        site.store.run('delete from tasks where id = ?', (tid,))
        site.pulse.bump()
        return {'ok': True}
    if 'done' in b:
        done = bool(b['done'])
        site.store.run('update tasks set done_at = ?, done_by = ? where id = ?',
                       (store_mod.now() if done else None, uid if done else None, tid))
        if done:
            site.store.act(uid, 'task', f'Done: {t["title"]}', {'task': tid})
    for f in ('title', 'note'):
        if f in b:
            site.store.run(f'update tasks set {f} = ? where id = ?', (str(b[f])[:2000], tid))
    if 'who' in b:
        site.store.run('update tasks set who = ? where id = ?', (b['who'] if b['who'] in site.users else None, tid))
    if 'due' in b:
        site.store.run('update tasks set due = ? where id = ?', (_date_or_none(b['due']), tid))
    site.pulse.bump()
    return {'ok': True}


@app.post('/api/idea')
async def idea(request: Request):
    uid = guard(request)
    b = await body(request)
    key = str(b.get('key', ''))[:200]
    if not key:
        raise HTTPException(400, 'Bad request.')
    status = b.get('status')
    if status is not None and status not in ('todo', 'filmed', 'posted', 'skipped'):
        raise HTTPException(400, 'Bad request.')
    lists = {k: [whole(i) for i in b[k]] for k in ('shots', 'facts', 'needs') if isinstance(b.get(k), list)}
    out = site.store.idea_set(key, str(b.get('week', ''))[:10], uid, status=status, link=b.get('link'), **lists)
    if status:
        words = {'filmed': 'Filmed', 'posted': 'Posted', 'skipped': 'Skipped', 'todo': 'Back to the plan'}
        site.store.act(uid, 'idea', f'{words[status]}: {b.get("title", "")[:120]}', {'idea': key})
    site.pulse.bump()
    return out


# ---------- pictures and videos ----------

KEEP = 'private, max-age=31536000, immutable'       # file names never change content
IMAGE_TYPES = {b'\xff\xd8\xff': '.jpg', b'\x89PNG': '.png', b'RIFF': '.webp'}


@app.get('/media/{path:path}')
async def media_file(request: Request, path: str):
    """Video covers and her videos (automations/media.py). Videos can be skipped through (range requests)."""
    me(request)
    f = (settings.MEDIA / path).resolve()
    if f.suffix not in ('.webp', '.mp4', '.jpg') or not f.is_file() or not f.is_relative_to(settings.MEDIA.resolve()):
        raise HTTPException(404, 'Not found.')
    return FileResponse(f, headers={'Cache-Control': KEEP})


@app.get('/photo/{name}')
async def photo_file(request: Request, name: str):
    me(request)
    f = settings.PHOTOS / name
    if not re.fullmatch(r'[0-9a-f]{16}\.(jpg|png|webp)', name) or not f.is_file():
        raise HTTPException(404, 'Not found.')
    return FileResponse(f, headers={'Cache-Control': KEEP})


def _photo_key(k):
    k = ' '.join(str(k or '').split())[:200]
    if not k:
        raise HTTPException(400, 'Bad request.')
    return k


def _drop_photo(file):
    if file and file not in site.store.photos().values():
        (settings.PHOTOS / file).unlink(missing_ok=True)


@app.post('/api/photo')
async def photo_add(request: Request, key: str):
    """A photo for a stock item (the page makes it small first). Only pictures, at most 3 MB."""
    uid = guard(request)
    key = _photo_key(key)
    if whole(request.headers.get('content-length'), 0) > settings.PHOTO_MAX:
        raise HTTPException(413, 'That photo is too big.')
    data = bytearray()
    async for chunk in request.stream():               # stop reading as soon as it's too big
        data += chunk
        if len(data) > settings.PHOTO_MAX:
            raise HTTPException(413, 'That photo is too big.')
    data = bytes(data)
    ext = next((e for magic, e in IMAGE_TYPES.items() if data.startswith(magic)), None)
    if not ext or (ext == '.webp' and data[8:12] != b'WEBP'):
        raise HTTPException(400, 'That is not a photo.')
    name = hashlib.sha256(data).hexdigest()[:16] + ext
    settings.PHOTOS.mkdir(parents=True, exist_ok=True)
    (settings.PHOTOS / name).write_bytes(data)
    old = site.store.photo_set(key, name, uid)
    if old != name:
        _drop_photo(old)
    site.pulse.bump()
    return {'file': name}


@app.post('/api/photo/remove')
async def photo_remove(request: Request):
    uid = guard(request)
    key = _photo_key((await body(request)).get('key'))
    _drop_photo(site.store.photo_set(key, None, uid))
    site.pulse.bump()
    return {'ok': True}


# ---------- the page ----------

@app.get('/{path:path}')
async def page(path: str):
    if path.startswith('api/'):
        raise HTTPException(404, 'Not found.')
    f = (settings.WEB / path).resolve()
    if path and f.is_file() and f.is_relative_to(settings.WEB.resolve()):
        cache = 'public, max-age=31536000, immutable' if path.startswith('assets/') else 'no-cache'
        return FileResponse(f, headers={'Cache-Control': cache})
    index = settings.WEB / 'index.html'
    if not index.exists():
        return Response('The page is not built yet (site/web: npm run build).', media_type='text/plain')
    return FileResponse(index, headers={'Cache-Control': 'no-cache'})
