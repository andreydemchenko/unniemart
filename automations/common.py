"""Shared helpers for the Unnie Mart automations: paths, .env, HTTP, Telegram, small JSON state files."""
import datetime as dt
import html
import json
import os
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
STATE = DATA / 'state'          # dedupe memory, not committed
PHT = dt.timezone(dt.timedelta(hours=8))
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'


def load_env(path=ROOT / '.env'):
    """KEY=value lines from the project .env into os.environ (existing env wins)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def http_get(url, ua=UA, timeout=25, tries=2):
    """GET with a browser UA and one retry. Raises on the final failure."""
    err = None
    for i in range(tries):
        try:
            r = requests.get(url, headers={'User-Agent': ua, 'Accept-Language': 'en-US,en;q=0.8'}, timeout=timeout)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            err = e
            if i + 1 < tries:
                time.sleep(3)
    raise err


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1))
    tmp.replace(path)


def telegram_send(text):
    """Send an HTML-formatted message if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set. Returns True if sent.
    Long text is split on line breaks to stay under Telegram's 4096-character limit."""
    load_env()
    token, chat = os.environ.get('TELEGRAM_BOT_TOKEN'), os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat:
        return False
    chunks, cur = [], ''
    for line in text.split('\n'):
        if len(cur) + len(line) + 1 > 3900:
            chunks.append(cur)
            cur = ''
        cur += line + '\n'
    chunks.append(cur)
    for c in chunks:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage',
                          data={'chat_id': chat, 'text': c, 'parse_mode': 'HTML', 'disable_web_page_preview': 'true'},
                          timeout=20)
        r.raise_for_status()
    return True


def esc(s):
    """Escape text for Telegram HTML."""
    return html.escape(s or '', quote=False)
