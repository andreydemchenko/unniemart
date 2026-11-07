"""Where the website keeps things. Same code on the laptop (for testing) and on the server.

  UM_CONTENT  the project files the site shows (brief, strategy, news, numbers). On the server: a copy the laptop
              pushes (~/unniemart/mirror). Default: the project folder.
  UM_STATE    the site's own data: database, stock photos. Default: site/.state (git-ignored).
  UM_CONF     private settings: users.json (logins), google-key.json (robot account), source.txt (her sheet link).
              Default: ~/.config/unniemart.
  UM_FAKE     a .xlsx file to use instead of her sheet (testing; writes stay in memory).
"""
import os
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PROJECT = SITE.parent
AUTOMATIONS = PROJECT / 'automations'
sys.path.insert(0, str(AUTOMATIONS))

CONTENT = Path(os.environ.get('UM_CONTENT') or PROJECT)
STATE = Path(os.environ.get('UM_STATE') or SITE / '.state')
CONF = Path(os.environ.get('UM_CONF') or Path.home() / '.config' / 'unniemart')
FAKE = os.environ.get('UM_FAKE')
WEB = Path(os.environ.get('UM_WEB') or SITE / 'web' / 'dist')

DB = STATE / 'desk.db'
PHOTOS = STATE / 'photos'                  # stock photos she or Andrey added
MEDIA = CONTENT / 'data' / 'media'         # video covers and her videos (automations/media.py, pushed by site_sync)
USERS = CONF / 'users.json'
GOOGLE_KEY = Path(os.environ.get('UM_GOOGLE_KEY') or CONF / 'google-key.json')


def sheet_link():
    for p in (CONF / 'source.txt', CONTENT / 'data' / 'owner' / 'orders' / 'source.txt'):
        if p.exists() and p.read_text().strip():
            return p.read_text().strip()
    return ''


CHECK_LIVE_S = 12          # how often to ask Google whether her sheet changed (robot account)
CHECK_LINK_S = 120         # share-link mode has no change signal: download this often
CHECK_CONTENT_S = 20
SESSION_DAYS = 180
UNDO_MINUTES = 15
PHOTO_MAX = 3 * 1024 * 1024
