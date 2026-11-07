# Automations

Phase A ("content brain") and the first step of Phase B (order desk) from `strategy/AUTOMATION.md` section 4.
The website that shows all of it (and writes payments to her sheet) is in `site/` (see `site/README.md`).
Python 3.10+, needs `requests` and `openpyxl`.
Run everything from the project folder.

| Script | What it does | When | Cost | Output |
|---|---|---|---|---|
| `news_watch.py` | 35 sources: Google News, K-pop and PH press feeds, PH ticket sites (SM Tickets, PULP, Live Nation, Ticketnet), Weverse Shop notices for 11 groups, Reddit. Keeps the shop's groups, dedupes, flags urgent items | Daily | $0 | `data/news/YYYY-MM-DD.json`, `data/news/latest.md`, Telegram (urgent only) |
| `weekly_stats.py` | Shop's 30 latest TikToks, comments on the 10 latest, latest X posts. Each video vs normal; scoreboard vs STRATEGY section 11; fan questions by type | Monday | ~$0.10 | `data/stats/YYYY-Www.md` + `.json` |
| `peer_watch.py` | 10 newest videos from 17 peer shops. Flags 5x-normal outliers, 3 to 45 days old | Monday | ~$0.45 | `data/peers/YYYY-Www.md` + `.json` |
| `banned_check.py` | Slop list from `PLAYBOOK.md` plus scarcity without a count, "don't miss out" without a date, AI or stock visuals | On every draft | $0 | Exit code 1 if blocked |
| `weekly_brief.py` | Calendar + news + stats + fan questions + peers + her stock list (her sheet's "ONHAND items" tab plus `stock.csv`) and notes (the season-ending show, like BTS Bulacan, is always included) → Claude (Opus 5.5, through the `claude` command on Andrey's subscription) drafts ideas that cite numbered sources → Python checks every idea: quotes must be in the source, numbers must be in a source, banned phrases, same offer within 14 days, stock list → ranked by season, fan questions, format evidence | Monday | $0 (subscription) | `content/ideas/YYYY-Www.md`, `data/briefs/YYYY-Www.json` (never overwrites: a second run that week writes `-v2`) |
| `masterlist.py` | Downloads her order masterlist (Google Sheet: as the robot account she shared it with, `google_sheet.py`, else the link in `data/owner/orders/source.txt`) and reads it: the "ONHAND items" stock tab, and every GO tab's balances, due dates, sheet rows and columns. Keeps the old copy if Google sends a sign-in page. Names, addresses and phone numbers never leave it. The website uses the same reading rules | Monday | $0 | `data/owner/orders/orders-2026.xlsx` (private) |
| `order_desk.py` | Order logic shared with the website: due this week / late / coming up / older, kind reminder drafts (a buyer who paid part is thanked for it and asked only for the rest) | Used by the website | $0 | nothing |
| `google_sheet.py` | Her sheet through Google's API as the robot account (a service account she shares the sheet with as Editor): download, read cells, write one cell, notes, the "Desk log" tab. Falls back to the share link (read-only). `python3 automations/google_sheet.py check` | Used by the website and `masterlist.py` | $0 | |
| `site_sync.py` | Keeps the website current: sends the briefs, numbers, news, calendar, docs, the one-page plan (`strategy/plan.json`) and `data/media` to the server. Her orders are not sent: the server reads her sheet itself | Hourly + after daily/weekly | $0 | the server's copy (`~/unniemart/mirror`) |
| `media.py` | Pictures and videos for the website (yt-dlp + ffmpeg, no account; videos kept small, 540p ~0.8 Mbit/s, incl. other shops' videos the site points to): a cover picture (360 px WebP, ~15 KB) for her newest 40 videos, her 24 most watched, every video a brief or the plan points to, and this week's peer standouts; small copies of her own videos (540p, ~2 MB) so they play at once. Other shops' videos: cover only (they play in TikTok's player). A failed one is tried again the next day, 3 times at most | Daily + Monday | $0 | `data/media/` (not in git): `t/`, `v/`, `index.json` |
| `score_competitors.py` | The research-03 scoring script. Also imported by the others for the peer list and format labels | Once | | `data/competitor-videos.csv` |

## Run

```bash
python3 automations/news_watch.py              # add --dry-run to print only, --only "SM Tickets" to test one source
python3 automations/weekly_stats.py            # --from-raw: no spend, re-uses the Oct 14 research scrape
python3 automations/peer_watch.py              # --from-raw: same
python3 automations/weekly_brief.py            # --dry-run: show the prompt; --from-json data/briefs/2026-W43.json: re-check, no Claude
python3 automations/media.py                      # fetch missing video covers and her new videos (--dry-run: list)
python3 automations/site_sync.py                  # update the website now
python3 automations/google_sheet.py check         # can the robot account open her sheet?
bash site/deploy.sh                               # put a new version of the website on the server
python3 automations/banned_check.py caption.txt    # or: echo "text" | python3 automations/banned_check.py
python3 -m pytest -q automations/tests
```

## Schedule (on Andrey's laptop)

Three launchd jobs, installed in `~/Library/LaunchAgents/` (copies of `automations/launchd/`):

| Job | When (laptop time, UTC+7) | Runs |
|---|---|---|
| `com.andrei.unniemart-news` | Every day 07:30 (08:30 PHT) | `run.sh daily`: news_watch → media → site_sync |
| `com.andrei.unniemart-desk` | Every hour while awake | `run.sh desk`: site_sync (files to the website). Quiet unless the website hasn't been updated for 6+ hours |
| `com.andrei.unniemart-weekly` | Mondays 06:30 (07:30 PHT) | `run.sh weekly`: weekly_stats → peer_watch → masterlist → weekly_brief → media → site_sync, about 15 minutes |

If the laptop is asleep, the job runs when it wakes; if it's off, that run is skipped (the website keeps running on
the server and keeps reading her sheet; only new briefs and news wait for the laptop). A Mac
notification pops up for urgent news, a finished brief, or a failed step. Logs: `data/logs/`.

```bash
launchctl kickstart gui/$(id -u)/com.andrei.unniemart-news      # run now
launchctl bootout gui/$(id -u)/com.andrei.unniemart-weekly      # stop a job (remove the plist to keep it off)
```

## Her weekly input (`data/owner/`)

- `stock.csv`: one row per item: demo unit / on hand / open GO (yes, no, unknown, planned), ETA. The brief only
  plans filming for items with a demo unit or stock, and asks about the unknowns.
- `notes.md`: free text for the week (when she can film, anything new). Replace it each week.
- `questions.csv`: optional tally of DM and X questions by type (`type,count`; types as in `weekly_stats.py`).
- `studio/summary.md`: the latest TikTok Studio numbers she shared.
- `orders/` (**private, git-ignored**): her masterlist, its share link (`source.txt`), the website's passwords
  (`site-logins.json`). An old `payments/` folder (screenshots from before Oct 15) is no longer used. Never commit or
  paste anything from here.
- `finance/` (**private, git-ignored**): her expenses and profits, when she sends them.

## Settings

- **What to watch:** groups, keywords and feeds live in `config.py`.
- **Apify:** tokens are read from `~/.config/apify/tokens.txt`. `apify.py` picks the token with the most room,
  never prints it, caps each run's spend, and logs every run with its cost to `data/state/apify_runs.jsonl`.
- **Claude:** `weekly_brief.py` calls `claude -p` with no tools and no files, from an empty temp folder. Model
  `claude-opus-5-5` (needs Claude Code 2.1.280 or newer; `claude update`). Change it with `--model`.
- **Telegram:** put `TELEGRAM_BOT_TOKEN=...` and `TELEGRAM_CHAT_ID=...` in the project `.env` (not committed).
  Without them, scripts just write files.
- **Memory:** `data/state/` (not committed) holds what was already seen: headlines, comments, flagged peer videos,
  the shop's video history. Delete a file there to start that memory fresh.
  The first `news_watch` run with empty memory records everything and sends no alerts.

## Rules the scripts follow

- News items are **headlines only**. Open the link and check the official source before using a date or price.
- Every report starts with source health. A source that returned 0 items is named, so a quiet week doesn't look
  like "no news".
- Fan comments are kept as text only, without usernames.
- Her buyers' data stays on this laptop. The order desk shows usernames and amounts only; full names are never shown.
  Payment screenshots stay in her DMs: the website no longer takes them (Andrey, Oct 15).
- Nothing is posted or sent to customers. Telegram goes to Andrey only.

## Her sheet and the website
The website (`site/`, on the server) reads her sheet directly and writes payments, dates, slots and reminder notes
back to it, each one logged in her "Desk log" tab. Access is a Google robot account (service account) she shares the
sheet with as Editor; its key is private (`~/.config/unniemart/google-key.json` on the laptop and the server). Setup
and details: `site/README.md`. Her steps: `content/drafts/connect-sheet.md`.

Buyers' data: the server reads her sheet in memory and shows usernames, items, amounts and dates only. Full names,
addresses and phone numbers are never shown.
