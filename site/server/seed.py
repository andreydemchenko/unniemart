#!/usr/bin/env python3
"""First tasks for a new site, from the plan's "Next" list (CLAUDE.md) and what she already agreed to.
Runs once: does nothing if there are tasks already.

  python3 site/server/seed.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import settings  # noqa: E402
import store as store_mod  # noqa: E402

TASKS = [
    # (title, who, due, note)
    ('Check the W43 video plan: tick every fact against its source', 'andrey', '2026-10-18',
     'Videos page, open each idea, "Facts to check".'),
    ('Send her the round 4 questions and the call-clips plan', 'andrey', '2026-10-19',
     'content/drafts/questions-for-her-round4.md and content/ideas/call-clips-plan.md'),
    ('Decide how buyers see the masterlist now', 'andrey', '2026-10-20',
     'Her new Google Sheet is private (only her and the robot). Buyers still open the old Excel link, which no longer '
     'updates. Either she gives buyers a view link to the new sheet, or the robot keeps the old file updated.'),
    ('Add "Where did you find us?" to the order form', 'owner', None,
     'She agreed on Oct 14. Tells us which videos bring orders.'),
    ('Ask her for expenses and profits per GO', 'andrey', None,
     'They go in data/owner/finance/ (private). Then: profit per GO and per item type.'),
]


def main():
    s = store_mod.Store(settings.DB)
    if s.q('select id from tasks limit 1'):
        print('tasks already there; nothing added')
        return 0
    for title, who, due, note in TASKS:
        s.run('insert into tasks (title, who, due, note, created_at, created_by) values (?,?,?,?,?,?)',
              (title, who, due, note, store_mod.now(), 'andrey'))
    print(f'{len(TASKS)} tasks added')
    return 0


if __name__ == '__main__':
    sys.exit(main())
