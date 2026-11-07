"""Logins: one password per person, no usernames. The password says who it is.

users.json (private, in UM_CONF): {"andrey": {"name": "Andrey", "role": "admin", "hash": "scrypt$..."}, ...}
Roles: admin (Andrey: sees everything, also drafts and sync details), owner (her: everything else).
A login lasts 180 days on that device (a random token in a cookie; the database keeps only its hash).

  python3 site/server/auth.py add andrey "Andrey" admin     # makes a new password and prints it once
  python3 site/server/auth.py add owner "Unnie Mart" owner
  python3 site/server/auth.py reset owner                    # new password (old devices stay signed in)
"""
import base64
import hashlib
import hmac
import json
import secrets
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import settings  # noqa: E402

WORDS = 'abcdefghjkmnpqrstuvwxyz23456789'           # no 0/o, 1/l/i: easy to type on a phone


def new_password():
    return '-'.join(''.join(secrets.choice(WORDS) for _ in range(4)) for _ in range(3))


def hash_password(pw, salt=None):
    salt = salt or secrets.token_bytes(16)
    h = hashlib.scrypt(pw.strip().lower().encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    return 'scrypt$' + base64.b64encode(salt).decode() + '$' + base64.b64encode(h).decode()


def check_password(pw, stored):
    try:
        _, salt, h = stored.split('$')
        got = hash_password(pw, base64.b64decode(salt)).split('$')[2]
        return hmac.compare_digest(got, h)
    except (ValueError, AttributeError):
        return False


def load_users(path=None):
    path = Path(path or settings.USERS)
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, ValueError):
        return {}


def who_is(pw, users):
    """The user id for this password, or None."""
    found = None
    for uid, u in users.items():
        if check_password(pw, u.get('hash', '')):
            found = uid
    return found


def token_hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


class Throttle:
    """At most `limit` wrong passwords per address in `window` seconds."""

    def __init__(self, limit=8, window=900):
        self.limit, self.window, self.fails = limit, window, {}

    def blocked(self, ip):
        now = time.time()
        self.fails[ip] = [t for t in self.fails.get(ip, []) if now - t < self.window]
        return len(self.fails[ip]) >= self.limit

    def fail(self, ip):
        self.fails.setdefault(ip, []).append(time.time())


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    users = load_users()
    if len(argv) >= 1 and argv[0] in ('add', 'reset'):
        uid = argv[1]
        if argv[0] == 'add':
            users[uid] = {'name': argv[2], 'role': argv[3] if len(argv) > 3 else 'owner'}
        elif uid not in users:
            print(f'no user {uid}')
            return 1
        pw = new_password()
        users[uid]['hash'] = hash_password(pw)
        settings.USERS.parent.mkdir(parents=True, exist_ok=True)
        settings.USERS.write_text(json.dumps(users, indent=1))
        settings.USERS.chmod(0o600)
        print(f'{uid}: {pw}')
        return 0
    if argv and argv[0] == 'list':
        for uid, u in users.items():
            print(uid, u.get('name'), u.get('role'))
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
