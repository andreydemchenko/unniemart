#!/usr/bin/env python3
"""Keeps the website (site/, running on the server) up to date from this laptop. Runs every hour (run.sh desk) and
after the daily and weekly jobs.

Sends the files the site shows to the server's copy: weekly briefs, numbers, news, calendar, strategy, research,
her notes, video covers and her videos (data/media, from media.py). (Her orders are not sent: the server reads her
sheet itself.)

Quiet when the laptop is offline; fails loudly only when the site hasn't been updated for 6 hours.

Usage:
  python3 automations/site_sync.py
"""
import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, ROOT, load_json, now_utc, save_json  # noqa: E402

SERVER = os.environ.get('UM_SERVER', 'dev@159.195.15.10')
REMOTE = os.environ.get('UM_REMOTE', '/home/dev/unniemart')
SYNCED = DATA / 'state' / 'site_synced.json'
STALE_HOURS = 6
SHOW = ['strategy/*.md', 'strategy/plan.json', 'research/*.md', 'content/ideas/*.md', 'content/drafts/*.md', 'automations/README.md',
        'data/stats/*.json', 'data/peers/*.json', 'data/news/2*.json', 'data/calendar.csv', 'data/owner/stock.csv',
        'data/owner/notes.md', 'data/owner/studio/summary.md',
        'data/media/index.json', 'data/media/t/*.webp', 'data/media/v/*.mp4']
SSH = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15']


class SyncError(Exception):
    pass


def files(root=ROOT):
    out = []
    for pat in SHOW:
        out += sorted(str(p.relative_to(root)) for p in root.glob(pat) if p.is_file())
    return out


def run(cmd, stdin=None):
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise SyncError((p.stderr or p.stdout).strip().splitlines()[-1][:200] if (p.stderr or p.stdout) else
                        f'{cmd[0]} failed')
    return p.stdout


def rsync(*args, stdin=None):
    return run(['rsync', '-a', '-e', ' '.join(SSH), *args], stdin)


def push_content():
    """Send the files; remove the server's copies of files that are gone here (a deleted draft disappears there too)."""
    import shlex
    names = files()
    rsync('--files-from=-', f'{ROOT}/', f'{SERVER}:{REMOTE}/mirror/', stdin='\n'.join(names) + '\n')
    there = run(SSH + [SERVER, f'cd {REMOTE}/mirror && find . -type f']).split('\n')
    gone = sorted({t[2:] for t in there if t.startswith('./')} - set(names))
    if gone:
        run(SSH + [SERVER, f'cd {REMOTE}/mirror && rm -f -- ' + ' '.join(shlex.quote(g) for g in gone)])
    return len(names)


def stale(path=SYNCED, now=None):
    last = load_json(path, {}).get('at')
    if not last:
        return None
    hours = ((now or now_utc()) - dt.datetime.fromisoformat(last)).total_seconds() / 3600
    return hours if hours >= STALE_HOURS else None


def main(argv=None):
    argparse.ArgumentParser(description='Update the Unnie Mart website from this laptop').parse_args(argv)
    try:
        n = push_content()
    except (SyncError, subprocess.TimeoutExpired, OSError) as e:
        h = stale()
        if h:
            print(f'Site not updated for {h:.0f} hours: {e}')
            return 1
        print(f'Site not updated this time (it will try again): {e}')
        return 0
    save_json(SYNCED, {'at': now_utc().isoformat()})
    print(f'Site updated: {n} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
