#!/usr/bin/env python3
"""Order desk logic shared by the website (site/server) and this laptop: who owes what by when, and kind
reminder drafts. Buyers send payment screenshots in DMs; she (or Andrey) records the amount on the website."""
import datetime as dt
import re

LATE_DAYS = 90          # balances due within the last 90 days are "late"; older ones are "old" (probably stale)
SOON_DAYS = 45
CURRENT_DAYS = 120      # an undated balance counts as current if the dated rows around it are this recent


# ---------- sorting balances (tested) ----------

def buckets(orders, today):
    """Open balances by urgency: late · week · soon · later · undated (current GO, no date) · old."""
    out = {k: [] for k in ('late', 'week', 'soon', 'later', 'undated', 'old')}
    for x in orders:
        if not x.get('balance') or x['balance'] <= 0:
            continue
        d, near = x.get('due'), x.get('near')
        if d is None:
            key = 'undated' if near and near >= today - dt.timedelta(days=CURRENT_DAYS) else 'old'
        elif d < today - dt.timedelta(days=LATE_DAYS):
            key = 'old'
        elif d < today:
            key = 'late'
        elif d <= today + dt.timedelta(days=7):
            key = 'week'
        elif d <= today + dt.timedelta(days=SOON_DAYS):
            key = 'soon'
        else:
            key = 'later'
        out[key].append(x)
    for k in out:
        out[k].sort(key=lambda x: (x.get('due') or dt.date.max, x['tab'], x['user'].lower()))
    return out


def live(b):
    """The balances a new payment could be for (not the old, probably stale ones)."""
    return b['late'] + b['week'] + b['soon'] + b['later'] + b['undated']


# ---------- words ----------

ACRONYMS = {'BTS', 'POB', 'LS', 'DP', 'PC', 'SG', 'ID', 'TXT', 'SVT', 'EXO', 'NCT', 'IU', 'DVD', 'EN', 'WTL', 'SS'}


def peso(v):
    return f'₱{v:,.0f}' if v is not None else '₱?'


def reminder(x, today):
    """A draft DM for the helper to rewrite in the shop's voice. Kind, no threats. A buyer who already paid part
    is thanked for it, and the message asks only for what's left."""
    item = x['item'] or x['tab']
    paid = x.get('paid') or 0
    part = f"Thank you po for the {peso(paid)} so far! " if paid > 0 and x.get('balance') else ''
    rest = 'remaining balance' if part else 'balance'
    if x['due'] and x['due'] < today:
        return (f"Hi po! {part}Just checking in on your {rest} of {peso(x['balance'])} for {item}, which was due on "
                f"{x['due']:%b} {x['due'].day}. Let us know po if you need help with it. Salamat po! 💜")
    due = f" is due on {x['due']:%b} {x['due'].day}" if x['due'] else ' is still open'
    return (f"Hi po! {part}Friendly reminder lang po: your {rest} of {peso(x['balance'])} for {item}{due}. "
            f"You can pay via GCash or Maya and send the screenshot here. Thank you po! 💜")


def nice(s):
    """'PLUSH KEYRING - WONCHU' → 'Plush Keyring - Wonchu' (BTS, POB and the like stay as they are)."""
    if not s.isupper():
        return s
    return re.sub(r"[A-Z][A-Z']*", lambda m: m.group(0) if m.group(0) in ACRONYMS else m.group(0).capitalize(), s)


def short(label):
    if label == 'paid in full at order':
        return 'in full'
    return re.sub(r'^within (\d+) days$', r'\1 days', re.sub(r'^if paid by ', 'by ', label))
