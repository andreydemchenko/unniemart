# The Unnie Mart website

https://unniemart.159-195-15-10.sslip.io (the old https://unniemart-desk.vercel.app forwards here)

One private place to run the shop, for Andrey and her: orders and balances live from her Google Sheet (and written
back to it), stock and slots, the weekly video plan and how the videos do, to-dos, and the plan on one screen.
Four pages: Home, Orders (to collect, by GO, stock), Videos, Plan. Phone first, plain words, real pictures: her
TikToks show as their covers and play right on the site, stock items can have a photo.
Look and feel: `PRODUCT.md` and `DESIGN.md` at the project root.

## How it fits together

```
her Google Sheet  ⇄  server (always on)  ⇄  the page on her phone / Andrey's laptop
                        ↑
      laptop, every hour: briefs, numbers, docs, the one-page plan (strategy/plan.json),
                          video covers and small video files (automations/media.py)
```

- **Her sheet stays the truth.** The server asks Google every ~12 seconds whether it changed and re-reads it, so her
  edits show up on the site within seconds. The site writes back only these, each one checked against the row first
  and logged in her "Desk log" tab (before and after): a payment (`=500` becomes `=500+2650`, 15 minutes to Undo), a
  due date, status, courier or note, a stock slot taken or freed, a reminder note on the username cell.
- **Part payments:** buyers send their GCash or Maya screenshot in a DM; she types the amount on the site. A part
  payment is added to the same Payment cell (`=300+1000`), so the order panel can list each payment. Saving a part
  payment can also set a new due date for the rest, and money over the balance can go to the same buyer's other open
  orders (oldest due first). After saving, a thank-you DM with what's left is ready to copy. Reminders to a buyer who
  paid part thank them for it and ask only for the rest.
- **Access to her sheet:** a Google "robot account" (service account, `unniemart-desk@unniemart.iam.gserviceaccount.com`,
  made on Andrey's Google account) she shares the sheet with as Editor. Since Oct 15 the site reads and writes her
  Google Sheet copy ("Masterlist 2026_v2", private: only her and the robot). The robot can also read an Excel file
  (mode "read", view only) but Google won't let any program write into one. Without the robot the server reads her
  share link every 2 minutes.
- **Reminding late buyers:** "Remind all" (Home and Orders) goes through everyone late, most late first: the kind
  message is ready, Copy notes the reminder, "Open their X" opens the buyer's profile, Next.
- **Videos:** `automations/media.py` (laptop) keeps a cover picture of every TikTok the site shows and small copies
  of her own videos (540p, about 2 MB, so they start at once; the next one loads while she watches). Some of her
  2022 to 2023 posts only give their sound: those, and other shops' videos, play in TikTok's own player inside the
  site. The files go to `~/unniemart/mirror/data/media` with the rest; the server sends them only to signed-in
  devices (`/media/...`, skipping through a video works). Each video idea shows a video like it (her own best one
  of that kind, from `strategy/plan.json`, or the one the brief points to) and the real fan comments behind it.
- **Stock photos:** tap an item, "Add a photo" (the phone makes it small first). Kept on the server
  (`~/unniemart/state/photos`), by item name, so they stay when rows move. "Copy list to post" copies the stock
  as a post (placeholder words for her to change).
- **The site's own data** (SQLite on the server): logins, tasks, video progress (status, shots and facts ticked),
  stock photos, history. Not her orders.
- **Pages update live**: each page keeps a request open and reloads only when something changed (a payment on
  another phone, her edit in the sheet, a new brief).

## Folders

| | |
|---|---|
| `server/` | Python (FastAPI). `app.py` routes and logins, video files and stock photos, `desk.py` her sheet (read, write, history), `content.py` briefs, numbers, the plan, video list, docs, `store.py` database, `auth.py` passwords, `settings.py` paths, `fake.py` a stand-in sheet for testing, `seed.py` first tasks |
| `web/` | The page (Svelte 5 + Vite). `src/views` one file per page, `src/components` panels and rows (`Player` the video player, `Thumb` a video cover, `RemindSheet` reminding late buyers), `src/app.css` colours, type, motion |
| `deploy/` | The systemd service and the Caddy block |
| `tools/make_fake.py` | A stand-in copy of her sheet with made-up buyers, for trying the site |
| `tests/` | `python3 -m pytest -q site/tests` |

Shared with the laptop scripts: `automations/masterlist.py` (reading her layout), `automations/order_desk.py`
(buckets, reminders), `automations/google_sheet.py` (the robot account).

## On the server

`dev@159.195.15.10`, user service `unniemart` (127.0.0.1:8821) behind Caddy (`~/.config/caddy/Caddyfile`, block
`unniemart.159-195-15-10.sslip.io`, automatic HTTPS). Nothing in `~/aireels` is used or touched.

| Where | What |
|---|---|
| `~/unniemart/app` | the code (sent by `site/deploy.sh`) |
| `~/unniemart/mirror` | the project files the site shows, video covers and small video files in `data/media` (sent by `automations/site_sync.py`) |
| `~/unniemart/state` | `desk.db`, `photos/` (stock photos) |
| `~/.config/unniemart` | private: `users.json` (password hashes), `source.txt` (her sheet link), `google-key.json` (robot key) |

```bash
bash site/deploy.sh                                       # build the page, send the code, restart (safe to repeat)
ssh dev@159.195.15.10 'journalctl --user -u unniemart -n 50'   # the server's log
ssh dev@159.195.15.10 'cd ~/unniemart/app/site/server && ~/unniemart/.venv/bin/python auth.py reset owner'   # new password
```

Logins: one password per person (no usernames), stays signed in 180 days. Passwords: `data/owner/orders/site-logins.json`
(private). Andrey's login also sees Drafts and the robot account's status.

## Connecting her sheet (done Oct 15)

1. The robot account (Google Cloud project `unniemart`, Sheets API + Drive API, service account `unniemart-desk`); its
   key is in `~/.config/unniemart/google-key.json` on the laptop and the server.
2. She saved the masterlist as a Google Sheet and shared the copy with the robot as Editor.
3. Its link is in `data/owner/orders/source.txt` (laptop) and `~/.config/unniemart/source.txt` (server; the old one
   is kept as `source.old.txt`). After changing either: `ssh dev@159.195.15.10 'systemctl --user restart unniemart'`.
   `python3 automations/google_sheet.py check` tests it from the laptop.
4. Open: buyers check their orders through the old Excel file's public link, which no longer updates. Not decided
   yet: give buyers a view link to the new sheet, or have the robot keep the old file updated.

## Trying it on the laptop

```bash
python3 site/tools/make_fake.py /tmp/fake.xlsx                       # made-up buyers, her real layout
UM_CONF=/tmp/umconf python3 site/server/auth.py add andrey Andrey admin
UM_FAKE=/tmp/fake.xlsx UM_STATE=/tmp/umstate UM_CONF=/tmp/umconf python3 -m uvicorn app:app --app-dir site/server --port 8821
cd site/web && npm run dev                                            # http://localhost:5180 (or npm run build)
```
Writes to the stand-in sheet stay in memory.
