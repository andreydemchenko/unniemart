"""Run an Apify actor and return its items. Picks the token with the most room left this month, never prints a full
token, caps each run's spend, and logs every run (actor, items, cost) to data/state/apify_runs.jsonl."""
import json
import time
from pathlib import Path

import requests

from common import STATE, now_utc

TOKENS = Path.home() / '.config/apify/tokens.txt'
API = 'https://api.apify.com/v2'
LOG = STATE / 'apify_runs.jsonl'
MIN_ROOM_USD = 1.0      # don't use a token with less than this left


def _tokens():
    out = []
    for line in TOKENS.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            out.append(line.split()[-1].split('=')[-1])
    return out


def room(token):
    d = requests.get(f'{API}/users/me/limits', params={'token': token}, timeout=20).json()['data']
    return d['limits']['maxMonthlyUsageUsd'] - d['current']['monthlyUsageUsd']


def pick_token():
    best, best_room = None, -1.0
    for t in _tokens():
        try:
            r = room(t)
        except (requests.RequestException, KeyError, ValueError):
            continue
        if r > best_room:
            best, best_room = t, r
    if best is None or best_room < MIN_ROOM_USD:
        raise RuntimeError(f'no Apify token with at least ${MIN_ROOM_USD} left (best: ${best_room:.2f})')
    return best, best_room


def run(actor, actor_input, name, max_usd=1.0, timeout_s=600):
    """Start `actor` (e.g. 'clockworks/tiktok-profile-scraper'), wait, return its dataset items."""
    token, left = pick_token()
    r = requests.post(f"{API}/acts/{actor.replace('/', '~')}/runs",
                      params={'token': token, 'waitForFinish': 60, 'maxTotalChargeUsd': max_usd},
                      json=actor_input, timeout=90)
    r.raise_for_status()
    data = r.json()['data']
    deadline = time.time() + timeout_s
    while data['status'] in ('READY', 'RUNNING') and time.time() < deadline:
        data = requests.get(f"{API}/actor-runs/{data['id']}", params={'token': token, 'waitForFinish': 60},
                            timeout=90).json()['data']
    items = []
    if data['status'] == 'SUCCEEDED':
        items = requests.get(f"{API}/datasets/{data['defaultDatasetId']}/items",
                             params={'token': token, 'clean': 'true'}, timeout=120).json()
    STATE.mkdir(parents=True, exist_ok=True)
    with LOG.open('a') as f:
        f.write(json.dumps({'at': now_utc().isoformat(), 'name': name, 'actor': actor, 'run_id': data['id'],
                            'token': '...' + token[-4:], 'room_before_usd': round(left, 2), 'status': data['status'],
                            'items': len(items), 'usd': data.get('usageTotalUsd')}) + '\n')
    if data['status'] != 'SUCCEEDED':
        raise RuntimeError(f"Apify {actor} run {data['id']} ended {data['status']}")
    return items
