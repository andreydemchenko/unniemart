# Unnie Mart automation: the weekly machine

Version 2 · 2026-10-14. Goal: the owner films and talks to customers; machines do the research, the remembering and
the paperwork. Tool facts, prices and risks come from `research/07-automation-stack.md`, feeds from
`research/06-calendar.md`, corrections from `research/08-fact-check.md` and `research/09-plan-review.md`.
**All hours and savings are estimates** built on volumes the owner hasn't confirmed: about 50 active orders and
40 to 80 DMs a week.

Nothing is posted or sent to a customer without a human tap, except FAQ auto-replies to messages that customers
send first, and the self-service order lookup page.

Words used here:
- **Apify:** a paid service that collects public TikTok and X data for us.
- **RSS feed:** a news site's machine-readable list of new articles.
- **Apps Script:** Google's free scripting built into Google Sheets.
- **Buffer:** an app that schedules posts to several platforms.
- **PayMongo / QR Ph:** a Philippine payment service / the national QR payment standard.
- **DTI / BIR:** business name registration / tax registration in the Philippines.

---

## 1. The weekly loop

```
 COLLECT (daily + Monday) ─► SHORTLIST (filters + rank) ─► BRIEF (Mon 8:00) ─► OWNER OK (10 min)
   news, calendar, own stats,   human-readable, sourced       3–5 videos with           │
   comments, peers, owner's     ideas only                    shot lists + captions     ▼
   stock list and DM tally                                                       FILM (one session)
            ▲                                                                            │
            └── LEARN (monthly, by hand, with Studio data) ◄── PUBLISH ◄── EDIT (CapCut templates) ◄┘
```

### Who does what, and how long it takes (estimates)

| Task | Who | When | Minutes a week |
|---|---|---|---|
| News, calendar, own stats, peers, comments | Machine | Daily / Monday | 0 |
| Stock list (what's on hand + which demo units exist) and a tally of DM/X questions | Owner | Monday | 5 |
| Approve or edit the brief | Owner | Monday | 10 |
| Film 3 videos | Owner | One session | 60 to 90 |
| Edit with CapCut templates (Clinic, Stock wall, News) | Owner or helper | Same week | 45 to 60 |
| Publish: TikTok scheduler, clean copy to Facebook and X | Owner | Scheduled | 15 to 20 |
| Pinned comments, TikTok Shop tags | Owner | When posting | 10 |
| Reply to keyword comments (News videos) | Owner | Same day | 10 to 20 |
| Test the order path (form, DMs, TikTok Shop) | Owner | Weekly | 5 |
| News videos that can't wait (sale details drop) | Owner | Ad hoc | 30 when it happens |
| **Total** | | | **about 3 to 4 hours a week** |

### The monthly human review

Once a month, Andrey and the owner look at TikTok Studio retention and search data, then decide which formats to
keep. Nothing changes automatically from week to week: with 3 posts a week, one breakout would swing any automatic
score.

---

## 2. How ideas get shortlisted

No weighted formula. Three hard filters, then a short ranked list a human picks from.

**Filters.** An idea is dropped if it fails any one of these:
1. **Has a source:** a news link, an official notice, a real fan question, or one of the shop's own videos.
2. **Can be filmed and sold:** the item or a demo unit is in hand (from the owner's weekly stock list), and the
   shop sells it now (on hand, or an open GO).
3. **Not a repeat offer:** the same offer wasn't posted in the last 14 days. Formats can repeat; Clinic #5 is fine.

**Ranking.** Sort what's left by:
1. A Philippine show or lightstick launch in the next 6 weeks, or an active season. BTS counts from now to Mar 16,
   2027, so it doesn't vanish until late February.
2. How many real fan questions match: comments plus the owner's DM and X tally.
3. Evidence level: stronger formats first (Clinic in season; stock wall in season, n=2), then tests (News, Money,
   Answer a fan).

---

## 3. The slop gate (runs before anything reaches the owner)

Blocks a draft if:
1. It has no source.
2. It contains a number that isn't in the order sheet or the linked source. Converted times (KST to Philippine
   time) and computed totals pass if they name what they came from.
3. It claims scarcity ("last X pieces") without a stock count.
4. It uses a banned phrase (Taglish and English list in `PLAYBOOK.md`). This needs a **new** checker; Andrey's
   existing one is for Russian text. Budget about 2 hours.
5. It asks for AI faces, AI voices, stock renders as the main shot, or someone else's footage.
6. It repeats an offer posted in the last 14 days.

**Facts need a human tick.** Every factual sentence ("only version 4 syncs", app names, dates) must quote the source
line it rests on, and the owner or Andrey ticks it. A machine can't catch a wrong fact that has no number in it.

**Source health.** Every brief starts with a line showing how many items each source returned. If a feed or scraper
returns zero, the brief says so. A quiet week must not look like "no news".

---

## 4. Build phases

### Phase A · Content brain (build first; needs only the owner's weekly stock list)

| Piece | What | Andrey's hours | Cost/month |
|---|---|---|---|
| `automations/news_watch` | Daily RSS + Google News check of the tested feeds (research 06, section 5), filtered by fandom and lightstick keywords, deduped. Urgent items (a new lightstick sale, a Manila concert, a ticket date) go to Telegram right away | 4 to 6 | $0 |
| `automations/weekly_stats` | Apify: the shop's last 30 TikToks + comments on the last 10; latest X posts. Each video compared with the account's normal | 4 to 6 | ~$1 |
| `automations/peer_watch` | Apify: about 20 peer shops × 10 newest videos. Flags videos 5× above that shop's normal, skipping videos under 3 days old (reuses `score_competitors.py`) | 3 | ~$3 |
| `automations/weekly_brief` | Calendar + news + stats + questions + peers → filters and ranking → Claude drafts the brief → slop gate → `content/ideas/YYYY-Www.md` + Telegram | 6 to 10 | $2 to 5 |
| Banned-phrase checker | Taglish and English list | 2 | $0 |
| **Total** | | **19 to 27** | **$6 to 9** |

**Time saved:** about 1.8 to 2 hours a week, mostly news scrolling (research 07 estimate). Caption drafts speed up
further once the Phase B order sheet supplies prices.

**Apify account:** one dedicated account for this project. Usage is about $4 a month; its free credit may cover it.
Don't spread the work across personal free accounts.

**Scraping note:** collecting public TikTok and X data goes against those platforms' terms in general. We use public
data only, never the shop's login, and keep volumes small (07).

### Phase B · Order desk (start when owner questions 7 to 9 are answered)

| Piece | What | Andrey's hours | Cost |
|---|---|---|---|
| Order sheet | One Google Sheet as the single source of truth: GOs (item, price ladder, DP, due dates, ETA, slots), orders, payments, batches (status timeline). A 20-second "manual add" form for orders that come in by DM | 6 (+ 2 owner) | $0 |
| "Check my order" page | Order code + last 4 digits of the phone → status, paid, balance, next due date, tracking. Codes are random, not counting up. Rate limit with lockout. First-name initial only. Nothing appears in any public list | 6 | $0 |
| 9 AM owner summary | Telegram: new orders, payments to check, due in 3 days, overdue, slots left, batch status changes | 5 | $0 |
| Saved Taglish replies | Price → GO post; "update po?" → lookup page; "how to order" → form; "saan mo kami nakita?" ("where did you see us?") for tracking. TikTok auto-replies only if the account qualifies | 3 (+ owner) | $0 |
| Free scheduler | TikTok Studio scheduler (15 minutes to 10 days ahead, no edits after scheduling) or Buffer free for X + TikTok | 1 | $0 |
| **Total** | | **~21 (+ 4 to 5 owner)** | **$0** |

**Time saved:** about 1.5 to 2.7 hours a week ("update po?" DMs, FAQ DMs, finding who owes what, finding orders,
batching posts; research 07).

**Privacy** (Philippine Data Privacy Act):
- Add a short privacy notice and consent line to the order form.
- Agree who can open the sheet.
- Keep payment screenshots only as long as needed.
- Crop screenshots to the amount and reference number before any AI reads them (Phase C).

**If the pilot ends,** the shop keeps the sheet, the form and a Google Apps Script copy of the lookup page. None of
it depends on Andrey's server.

### Phase C · Optional, one piece at a time, only if the volume is there

| Piece | Andrey's hours | Cost/month | Saves/week |
|---|---|---|---|
| Payment-screenshot pre-check (reads amount, reference and date; flags duplicates and mismatches; the owner still taps "paid") | 10 | $1 to 3 | 40 to 60 min |
| Payment-due reminder drafts for the owner to send | 4 | $0 to 3 (SMS, no links) | 20 to 30 min |
| Viral-spike mode: when a video takes off, sort its comments and suggest replies | 4 | $0 to 1 | 0 to 30 min |
| Payment links that mark "paid" automatically (PayMongo; QR Ph 1.34%, GCash 2.23% per payment). GCash for Business needs DTI + BIR (2303) registration and a GCash account verified for 12+ months | 10 to 12 | fees only | 45 to 60 min |
| DM bot test (Messenger or TikTok): answers FAQ and order status only, then hands over to a person. TikTok DM automation in the Philippines is unconfirmed | 8 to 12 | $29 to 39 | 30 to 60 min |
| Restock watcher on specific product pages (read-only, every few hours) | 4 to 6 | $0 | 20 to 30 min |
| **If all built** | **40 to 50** | **$30 to 46 + fees** | **about 2.5 to 4.5 h** |

---

## 5. Never automate

- Posting through our own TikTok app. TikTok's review rejects in-house posting tools, and unreviewed apps can only post privately (07, 08).
- Bots logged into the shop's accounts; auto-likes, auto-follows, auto-comments; cold DMs.
- Automatic **public** replies to comments.
- Fake reviews or testimonials; bought followers, likes or views.
- AI voices, AI avatars, AI idols, AI product photos.
- Marking a payment as paid; refunds, cancellations, complaints.
- Payment reminders sent without the owner's tap.
- Opening a GO or setting its price; buying stock at drop time.
- Publishing any lightstick, app, sync or date claim without a human check against the official source.
- Using customers' photos, names or comments in content without their consent.
- Anything a customer reads that the owner hasn't approved, except FAQ and status auto-replies to messages customers send first, and the lookup page.
