# Unnie Mart workspace

Talk to Andrey in **English**, in plain words a normal person understands. No jargon, no em dashes.
The shop's audience speaks Taglish (English + Tagalog).

## What this is
Content strategy + automations for Unnie Mart (TikTok @unniemart_, X @unniemart_), a Philippine K-pop group-order (GO) merch shop.
The owner is someone Andrey knows personally (she/her). It's a pilot between people who know each other, not a formal client job.
She films and approves; machines do research, ideas, drafts, tracking.

## Where we are (update this when things change)
- **2026-10-14:** research done (`research/01` to `11`), plan v2.1 written and reviewed twice.
  Git is initialised, nothing committed.
- **2026-10-14 (later):** owner message drafted (`content/drafts/2026-10-14-owner-message.md`, not sent yet).
  Phase A partly built and tested (`automations/README.md`): `news_watch`, `weekly_stats`, `peer_watch`,
  `banned_check`, 24 tests passing. Each ran once for real; memory lives in `data/state/`.
- **2026-10-14 (evening):** she answered Q1 to Q7 and sent TikTok Studio screenshots: `strategy/OWNER-ANSWERS.md`.
  Search is 77% of views; no ads ever; the Heeseung call is hers; Army Bomb box arrives last week of October;
  she's in Vietnam until Oct 20. Phase A is done: `weekly_brief` built (Claude Opus 5.5 via `claude -p` on
  Andrey's subscription), 37 tests passing, first brief at `content/ideas/2026-W43.md` (not reviewed yet).
  Scheduled on Andrey's laptop (launchd): news daily, the weekly chain Mondays. A new run never overwrites a
  brief: Monday Oct 19 writes `2026-W43-v2.md` next to the reviewed one. No Telegram yet (Mac notifications).
- **Her weekly input** lives in `data/owner/` (stock list, notes). Update it from her messages until there's a sheet.
- **2026-10-14 (night):** Phase B step 1 built. `masterlist.py` downloads her sheet (link in
  `data/owner/orders/source.txt`) daily and on Mondays; the brief now reads her "ONHAND items" tab for stock, prices
  and slots. `order_desk.py` writes a private page, `data/owner/orders/desk.html`: due this week, late, coming up,
  payment screenshots matched to open balances, stock on hand, older balances. 49 tests passing.
  W43-v2 fixed by hand (both halves of the refund rule; "old Army Bomb" needs no demo unit), 6 ready.
- **2026-10-14 (late night):** a first order desk page went online on Vercel (password-locked). Andrey found it
  looked AI-made; replaced the same night (below). The old link now forwards to the website.
- **2026-10-14 (late night, 2):** **the website** (`site/`, `site/README.md`): https://unniemart.159-195-15-10.sslip.io,
  running all the time on Andrey's server (user service `unniemart`, Caddy). Home (money to collect, due this week,
  late, to-dos, next video, dates, news), Orders (to collect, by GO, screenshots), Stock, Videos (the weekly brief as
  a checklist: status, shots, facts), Tasks, Dates, News, Numbers, Plan (all docs). Two logins (Andrey, her; passwords
  in `data/owner/orders/site-logins.json`). Look: friendly banking-app style, Google Sans (`PRODUCT.md`; colours changed since, see `DESIGN.md`).
  Her sheet is read live (her edits show within seconds) and written back (payment, Undo, due date, status, courier,
  note, slot, reminder note), every write logged in a "Desk log" tab. Writing needs the **robot account** (a Google
  service account she shares the sheet with); until then the site is view only. The Apps Script plan was dropped.
  The laptop pushes briefs/news/numbers/docs hourly (`automations/site_sync.py`) and reads payment screenshots.
  73 tests passing (incl. a review of every write path). Tested with made-up buyers in a browser, and live
  (read-only) on her real sheet.
- **2026-10-14 (late night, 3):** the robot account exists (on Andrey's Google account:
  `unniemart-desk@unniemart.iam.gserviceaccount.com`, key on laptop and server). Found: her masterlist is an
  **Excel file** (`Masterlist.xlsx`) in Drive. The robot reads it (edits show within ~15 s) but Google can't write
  into Excel files, so the site stays view only until she saves it as a Google Sheet and shares that copy.
  Site redesigned for fewer words: charts (split bar, 7-day bars, views chart, rings), faces for buyers, icons for
  every kind of thing, a month calendar, stock as tiles with slot dots, news limited to her groups (`DESIGN.md`).
  75 tests passing.
- **2026-10-15:** she saved the masterlist as a Google Sheet ("Masterlist 2026_v2", private: only her and the robot)
  and shared it with the robot. The site now reads and writes it ("Live"); no payment written to it yet. Her answers:
  buyers DO check their orders through the old (Excel, public) link, which no longer updates; she edits in Google
  Sheets on phone and browser. **Open: how buyers see the masterlist now** (it holds buyers' names and addresses).
  Site redesigned again for less text: Home cut to money, late, this week, next video, to-dos; two-tone icons plus
  drawn merch icons (lightstick, photocard, picket...); calm headlines and group badges in News; Numbers rebuilt
  (posts a week vs goal, where viewers come from from her TikTok Studio, a dot per video for "What works", goal
  bars). 76 tests passing.
- **2026-10-15 (later):** Andrey: too much text, too many screens, no screenshot uploads (buyers send them in DMs),
  handle part payments well. The site now has **4 pages**: Home, Orders (to collect, by GO, stock), Videos (the
  week's list plus views, posts a week, what works), Plan (one screen from `strategy/plan.json`: the idea, the weekly
  mix, what's coming, 4 rules, goals; documents behind one button). News, Dates, Numbers, Tasks and More are gone;
  to-dos live on Home. Screenshot upload and reading removed everywhere (site and laptop). **Part payments:** each
  payment in the Payment cell shows as a chip; the payment screen shows what's left, can set a new due date for the
  rest, can put extra money on the buyer's other orders, and ends with a thank-you DM to copy (placeholder Taglish).
  Reminders thank a buyer for what they've paid. 74 tests passing (2 screenshot tests removed).
- **2026-10-15 (evening):** Andrey: "even a child would understand", real videos with a quick player, real images,
  beautiful, grow her business. Plain words everywhere ("Money to collect", "9 days late", "Film and post Oct 20 to
  22", "Big text at the start"). **Real videos:** `automations/media.py` keeps covers of 71 TikToks and small copies of
  45 of her videos (540p, ~2 MB; 81 MB in all; her 2022 to 2023 posts only give sound, so those and other shops'
  videos play in TikTok's player); a full-screen player (tap, swipe, next one preloaded). Videos page: this week's 3
  circles, each idea with a picture of a video like it, her videos as a grid (newest / most views), what gets views.
  Video ideas show the example video and the real fan comment behind it. Plan: each kind of video shows her own best
  one (her lightstick how-tos are her biggest hits: 225K views). **Remind all** late buyers in one go. **Stock:**
  photos (added on the site, kept on the server) and "Copy list to post". 79 tests passing.
- **2026-10-15 (night):** Andrey: videos load too long, yellow too bright, look more modern, less text. New look:
  cool off-white, a deep navy money card, one cobalt blue; video ideas as big picture posters on Home and Videos;
  buyers as round faces; a floating bottom bar; Orders shows the first 3 of "Coming up" and "Later". Videos: the
  other shops' videos are now kept too (52 play from the site; only photo slideshows use TikTok's player), heavy
  files made smaller, the next/previous video and this week's examples load ahead (swipe to next: ~0.5 s; first tap
  ~1.5 s from far away). Live Caddy security setting now allows `media-src 'self' blob:` (backup kept). 81 tests.
- **Next:**
  1. Andrey reviews `content/ideas/2026-W43-v2.md`, ticks the facts, sends her the picks plus
     `content/ideas/call-clips-plan.md` and `content/drafts/questions-for-her-round4.md` (box share, 2 late VER.4
     balances, old balances, the new website, what "SCO" means). The facts can be ticked on the website (Videos).
  2. Decide with her how buyers see the masterlist (the old Excel link stopped updating Oct 15): a view link to the
     new sheet, or the robot keeps the old file updated (she'd share it with the robot as Editor). Then send her
     `content/drafts/connect-sheet.md` (site intro, password). Check the first real payments in the Desk log tab.
  3. Her expenses and profits go in `data/owner/finance/` when she sends them (then: profit per GO, per item type).
     Private like `data/owner/orders/` (masterlist, buyers' personal data): never commit, paste or upload either.
     The one exception: the website's server reads her sheet itself (in memory; only usernames, items, amounts and
     dates are shown). Don't copy her masterlist
     anywhere else. The robot key (`~/.config/unniemart/google-key.json`) is private too.
  4. Later: Telegram bot (or the desk page on her phone), move the schedule to the server, GCash question (Q8).
- **Time-sensitive:**
  - The Army Bomb VER.4 box (KP60121) reaches her in the last week of October (her estimate). That unlocks the
    Army Bomb clinic and the "Box from Korea" video. She's back in the Philippines Oct 20; no filming before that.
  - HYBE CINE FEST runs Oct 24 to 31, so video #4 has to go up Oct 20 to 22.
  - ENHYPEN Renewal lightstick sale details are due in October. `news_watch` (daily) watches Weverse Shop
    notices and Google News for it.
- Apify spend so far: about $9.55 on 2026-10-14, all from free credit. Per-run log: `data/state/apify_runs.jsonl`.

## Rules
- **No AI slop.** No AI voices, AI faces, stock footage, fake scarcity, invented facts or generic hype.
  Every idea must point to a real source: their own data, a real fan comment, a real event with a link.
- Drafts only. Nothing gets posted or sent to customers (or to her) without Andrey's OK. Exception, Andrey's choice
  (2026-10-14): on the website she sees everything as soon as it's made (briefs, strategy, research), except Drafts.
- Facts (dates, prices, release info) need a source link. Mark anything unverified.
- Taglish lines are placeholders until she rewrites them in her own voice.
- Apify tokens live in `~/.config/apify/tokens.txt`. Never print them in full. Check usage first
  (`https://api.apify.com/v2/users/me/limits?token=...`) and use the token with the most room.
- Do not touch `/home/dev/aireels` on the server (still in development).
- Paid image/video generation (kie.ai etc.) only after a dry run and Andrey's OK.
- Commit or push only when Andrey asks.

## Where things are
See `README.md` for folders. Strategy lives in `strategy/`, research in `research/`, data in `data/`, the website in
`site/` (look and feel: `PRODUCT.md`, `DESIGN.md`). Server: `dev@159.195.15.10`, everything in `~/unniemart`.
