"""The site's own small database (SQLite): logins, tasks, video progress, stock photos, history.

Her orders are NOT here: they live in her sheet and are read from it. This only keeps what the sheet has no place
for, plus a copy of every change the site made to the sheet (for Undo and the history on each order).
"""
import datetime as dt
import json
import sqlite3
import threading

SCHEMA = """
create table if not exists sessions (token text primary key, user text, created text, seen text, agent text);
create table if not exists tasks (id integer primary key, title text not null, who text, due text, note text,
  done_at text, done_by text, created_at text, created_by text);
create table if not exists ideas (key text primary key, week text, status text, shots text, facts text, needs text,
  link text, updated_at text, updated_by text);
create table if not exists changes (id integer primary key, at text, who text, kind text, tab text, r integer,
  usr text, item text, col integer, before text, after text, extra text, undone_at text);
create table if not exists activity (id integer primary key, at text, who text, kind text, text text, ref text);
create table if not exists photos (key text primary key, file text, at text, who text);
create index if not exists activity_at on activity(at);
create index if not exists changes_line on changes(tab, r);
"""


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


class Store:
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path), check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.lock = threading.RLock()
        with self.lock:
            self.db.executescript(SCHEMA)
            self.db.commit()

    def q(self, sql, args=()):
        with self.lock:
            return [dict(r) for r in self.db.execute(sql, args).fetchall()]

    def run(self, sql, args=()):
        with self.lock:
            cur = self.db.execute(sql, args)
            self.db.commit()
            return cur.lastrowid

    # ---- sessions ----

    def session_add(self, token_hash, user, agent):
        t = now()
        self.run('insert into sessions values (?,?,?,?,?)', (token_hash, user, t, t, (agent or '')[:200]))

    def session_user(self, token_hash, max_days):
        rows = self.q('select user, seen from sessions where token = ?', (token_hash,))
        if not rows:
            return None
        seen = dt.datetime.fromisoformat(rows[0]['seen'])
        if dt.datetime.now(dt.timezone.utc) - seen > dt.timedelta(days=max_days):
            self.run('delete from sessions where token = ?', (token_hash,))
            return None
        if dt.datetime.now(dt.timezone.utc) - seen > dt.timedelta(hours=6):
            self.run('update sessions set seen = ? where token = ?', (now(), token_hash))
        return rows[0]['user']

    def session_end(self, token_hash):
        self.run('delete from sessions where token = ?', (token_hash,))

    # ---- history ----

    def act(self, who, kind, text, ref=None):
        self.run('insert into activity (at, who, kind, text, ref) values (?,?,?,?,?)',
                 (now(), who, kind, text, json.dumps(ref or {}, ensure_ascii=False)))

    def activity(self, limit=60):
        out = self.q('select * from activity order by id desc limit ?', (limit,))
        for a in out:
            a['ref'] = json.loads(a['ref'] or '{}')
        return out

    def change(self, who, kind, tab, r, usr, item, col, before, after, extra=None):
        return self.run('insert into changes (at, who, kind, tab, r, usr, item, col, before, after, extra) '
                        'values (?,?,?,?,?,?,?,?,?,?,?)',
                        (now(), who, kind, tab, r, usr, item, col, json.dumps(before), json.dumps(after),
                         json.dumps(extra or {}, ensure_ascii=False)))

    def changes_for(self, tab, usr, limit=20):
        out = self.q('select * from changes where tab = ? and usr = ? order by id desc limit ?', (tab, usr, limit))
        for c in out:
            for k in ('before', 'after', 'extra'):
                c[k] = json.loads(c[k]) if c[k] else None
        return out

    def last_reminders(self):
        """{(tab, username): 'iso time'} of the latest reminder per order line."""
        out = {}
        for c in self.q("select tab, usr, max(at) at from changes where kind = 'remind' group by tab, usr"):
            out[(c['tab'], c['usr'])] = c['at']
        return out

    # ---- tasks ----

    def tasks(self):
        return self.q('select * from tasks order by done_at is not null, coalesce(due, "9999"), id')

    # ---- stock photos (files in state/photos) ----

    def photos(self):
        return {r['key']: r['file'] for r in self.q('select key, file from photos')}

    def photo_set(self, key, file, who):
        old = self.photos().get(key)
        if file:
            self.run('insert or replace into photos values (?,?,?,?)', (key, file, now(), who))
        else:
            self.run('delete from photos where key = ?', (key,))
        return old

    # ---- ideas (video progress) ----

    def ideas(self):
        out = {}
        for r in self.q('select * from ideas'):
            for k in ('shots', 'facts', 'needs'):
                r[k] = json.loads(r[k]) if r[k] else []
            out[r['key']] = r
        return out

    def idea_set(self, key, week, who, **fields):
        cur = self.ideas().get(key) or {'status': 'todo', 'shots': [], 'facts': [], 'needs': [], 'link': ''}
        cur.update({k: v for k, v in fields.items() if v is not None})
        self.run('insert or replace into ideas values (?,?,?,?,?,?,?,?,?)',
                 (key, week, cur['status'], json.dumps(cur['shots']), json.dumps(cur['facts']),
                  json.dumps(cur['needs']), cur.get('link') or '', now(), who))
        return self.ideas()[key]
