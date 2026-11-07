# 07 — Automation stack for Unnie Mart

Date: 2026-10-14. Author: research pass for Andrey (consultant).
Scope: remove repetitive manual work, keep the human parts human. Video editing is **out of scope**
(treat it as "phone editing in CapCut now, a plug-in editor later").

**How to read the labels**

| Label | Meaning |
|---|---|
| **[F]** | Fact. Comes from a source (URL + date in the Sources list) or from our own data pulled on 2026-10-14. |
| **[I]** | Inference from evidence. Likely true, not confirmed with the owner. |
| **[E]** | Estimate (hours, costs, volumes). The reasoning is shown. |
| **[U]** | Unverified or sources conflict. Test before you rely on it. |

---

## 0. TL;DR

1. **X (Twitter) is the main shop window, not TikTok.** [F] @unniemart_ on X has 18,662 followers and 20,142 posts
   (since Oct 2020) and posts WTS/LFB threads every day. TikTok has 5,909 followers. Since May 2026 the median TikTok
   video gets 598 plays and 1 comment. So "comment to reserve" automation on TikTok has low payoff right now.
   Orders go through a **Google Form** plus "DM to avail".
2. **The biggest time sinks we can automate** [E] are: answering "status / price / DOP?" DMs, checking payment proofs,
   chasing DOP (installment) due dates, writing the same WTS caption format, and scrolling for K-pop news.
   Filming, final approval, real conversations and packing stay human.
3. **Phase 1 costs $0–3/month and takes about one week to set up** [E]. It is one order sheet as the single source
   of truth, a "Check my order" page (order code + last 4 digits of the phone), native auto-replies, a free
   scheduler, a daily Telegram digest for the owner, and a K-pop news digest. It saves an estimated **3.5–5 h/week**.
4. **Don't build our own TikTok posting app.** [F] TikTok's audit rejects "a utility tool to help upload contents to
   the account(s) you or your team manages", and posts from unaudited apps stay private. Use TikTok Studio's scheduler
   or an audited tool (Buffer, Metricool, Later). Posting through the API also can't add TikTok library sounds.
5. **TikTok DM automation in the Philippines is unclear.** [U] Most partners say APAC (including PH) is supported, but
   one partner lists PH as unsupported. ManyChat's comment-to-DM has only partly rolled out, in VN/TH/ID. Test it,
   don't plan around it.
6. **GCash has no API for a personal wallet.** [F] The app shows 90 days of history, and older history comes by email
   as a password-protected PDF. A CSV export needs GCash for Business, which requires a registered business. Real
   payment automation means payment links with webhooks (for example PayMongo, QR Ph at 1.34%). That's Phase 3.

---

## 1. Evidence about this shop (pulled 2026-10-14)

| What | Finding | Label |
|---|---|---|
| TikTok @unniemart_ | 5,909 followers, 135.1K likes, 396 videos. Bio: "Your KPOP One-Stop Shop / ENCHIN ORDER FORM". The bio link is a bit.ly that leads to a Google Form | [F] Apify scrape `data/raw/tiktok-latest-2026-10-14.json` |
| TikTok reach | 27 videos since May 2026: median 598 plays, median 1 comment, max 12 comments. Old 2022–2023 videos reached 15K–226K plays with 100–1,000 comments | [F] same scrape |
| X @unniemart_ | 18,662 followers, 20,142 posts, location "73 11th avenue cubao". Bio links to TikTok Shop, Shopee and Lazada. Daily WTS/LFB posts get 691–1,873 views and 0–8 likes | [F] Apify `apidojo/tweet-scraper`, 10 latest posts |
| Sales channels | Google Form (order form), DMs on X/TikTok, a TikTok Shop (the link resolves to a live seller ID). Shopee and Lazada links are in the X bio (the Shopee short link resolved only to the homepage) | [F] / [U] marketplace status |
| Order form | Google Forms, behind bit.ly links. An anonymous fetch returns HTTP 401, so the form needs Google sign-in. Google requires sign-in for file-upload questions, so it probably collects a payment-proof screenshot | [F] 401 / [I] reason |
| Pricing model | "DP ₱300", then "PAYO ₱2,650 / July 31 DOP ₱2,750 / Aug 15 DOP ₱2,850". Paying later costs more. "Price is inclusive of PF and ISF". "LONG DOP until October 15". "BOXSHARE" | [F] captions |
| Sourcing | "Official from Weverse Shop", "with POB (1 Random Photocard)", "ETA 4–5 weeks upon arrival to KR Add", "3–4 weeks upon arrival to JP Add", "NETA" | [F] captions |
| Status updates | X posts like "LATEST STATUS OF OUR ARMYBOMB'S… just a little bit more and magiging ONHAND", "about to arrive at our PH ADD". TikTok: "Our box from Korea has arrived" | [F] X + TikTok captions |
| Facebook / Messenger | No FB page linked from the TikTok or X bios | [U] ask the owner |

**Glossary (PH GO slang, inferred from usage)** [I]: **GO** group order, **GOM** group order manager,
**WTS/LFB** want to sell / looking for buyer, **DP** downpayment (reserves the slot), **PAYO** the lowest "pay now in
full" price tier (the expansion is not confirmed), **DOP** date of payment (the installment deadline; a later DOP
means a higher price), **ISF/LSF** international/local shipping fee, **PF** processing fee, **KR/JP/PH Add** the
forwarder address in Korea/Japan, or the shop's PH address, **NETA** no exact time of arrival, **POB** pre-order
benefit, **Onhand** in stock in PH, **Boxshare** sharing a box or set split between buyers, **kaddy** a rented Korean
address (forwarder).

**What PH buyers compare against** [F]: in Feb 2026 a PH buyer on Reddit compared the Weverse BTS lightstick price
(~₱1,780) with PH GO prices of ₱2,700–2,900 before local shipping. They also saw "kaddy" Korean address rentals at
₱200–250. Their question was "why is it so much more expensive?". So trust and clear "what's included" messaging
matter. Automation must never make prices or status vaguer.

---

## 2. Workflow map (how a PH GO shop runs)

Sources: the shop's own captions [F], Huckleberry PH GO terms [F], generic GOM guides (Paysable 2026-03, Kfriday 2026-01) [F],
Reddit r/kpophelp threads [F]. Where Unnie Mart's own practice isn't visible, the row says [I] or [U].

| # | Step | How it works today | Pain / repetition | Evidence |
|---|---|---|---|---|
| 1 | **Sourcing** | Watch Weverse Shop (KR/JP) drops, release dates and POBs. Decide the GO, set the price tiers (DP, PAYO, DOP dates) that include PF+ISF | Daily scrolling of Weverse, X fan accounts and news; manual price math | [F] captions; [I] process |
| 2 | **Announce** | X post "🌹 WTS \| LFB \| GROUP \| ITEM 🌹 [PH GO] #Unniemart_Go" with prices, ETA and an order-form link. A TikTok video (unboxing, "connecting lightstick to app", Taglish humor). Reposted for days ("still available") | The same caption format is retyped and reposted daily; hashtags are copy-pasted | [F] |
| 3 | **Reservations** | Google Form (needs sign-in) plus "DM to avail" / "comment or DM to order" | Forms and DMs live in two places; DMs repeat the same questions (price, DOP, slots) | [F] |
| 4 | **Payments** | DP ₱300 reserves; balance by the chosen DOP. GCash/Maya/bank (typical for PH GOs: Huckleberry lists BPI, GCash and Palawan; Unnie Mart's methods not seen) | Each proof screenshot is checked by hand in the wallet app and ticked in a sheet; installments mean 2–3 payments per order; chasing late payers | [F] Huckleberry; [U] UM methods |
| 5 | **Order placement** | Buy on Weverse Shop at release, ship to the KR/JP forwarder ("KR Add") | Manual, high-stakes (stock sells out). Keep it human | [F] captions |
| 6 | **Batch tracking** | Statuses: ordered → at KR/JP add → shipped to PH → arrived at PH add → sorting → onhand. ETA "3–5 weeks upon arrival", "NETA" | Every buyer asks "update po?"; the owner answers one by one, plus public status posts | [F] X status posts; [I] volume |
| 7 | **Arrival in PH** | "Our box from Korea has arrived" post; extras become "#Unniemart_Onhand" stock | Re-announcing extras daily | [F] |
| 8 | **Packing and shipping** | Typical PH: J&T/LBC/Lalamove/Grab, meetups; LSF collected on arrival. Huckleberry ships on fixed weekdays after payment. Unnie Mart has a Cubao address (pickup possible) | Booking each parcel and sending tracking numbers one by one | [F] Huckleberry; [U] UM couriers |
| 9 | **Customer updates** | Public X status posts plus individual DMs. Some GOMs keep a public "tracker" spreadsheet (seen in GOM terms pages) | Same answer typed dozens of times | [F] kimxtaegos / Paysable |
| 10 | **Content** | Phone filming → CapCut → caption → post on TikTok (plus X photos) | Caption writing, hashtags, remembering to post | [F] |
| 11 | **Engagement** | DMs on X and TikTok; low TikTok comment volume now (median 1) | The DM backlog is the bottleneck | [F] |
| 12 | **Analytics** | Nothing visible | Nobody knows which posts or channels sell | [I] |

---

## 3. Step-by-step automation table

Costs are monthly, in USD. Setup hours are Andrey's build time plus owner time. Exchange-rate assumption [E]: about ₱58 = $1.

| Step | What to automate | Tool options (pick in **bold**) | $/mo | Setup h | Risk (ToS / ban / error) | Human must stay |
|---|---|---|---|---|---|---|
| 1 Sourcing / news | Daily digest of drops, restocks, PH concerts and fansigns for the shop's fandoms (ENHYPEN, BTS, BABYMONSTER, SEVENTEEN) | **Google News RSS** (PH edition, keyword filter) + **Soompi/Koreaboo/Rappler/Philstar RSS** → server cron → Telegram. Optional: Weverse Shop page-change watcher (Phase 3). X accounts: owner's own X list (free) or the Apify tweet scraper (~$0.15–0.40 per 1K tweets) instead of the X API ($0.005/post read) | 0–1 | 4–6 | Low. RSS is meant for this. Weverse robots.txt allows public pages (it blocks only /order and /api), but its ToS was not reviewed: poll politely and read-only | Deciding which GO to open and the price |
| 2 Announce | Draft the WTS caption from the GO row (prices, DOP tiers, ETA, form link) in the shop's own format; schedule it | **Template + LLM hook line** (numbers come from the sheet, never from the model) → Telegram approval → **Buffer Free** (3 channels: X + TikTok + 1) or **TikTok Studio scheduler** (desktop, ≤10 days ahead). Alternatives: Metricool Free (20 posts/mo), Later (from $18.75/mo, no free plan) | 0–5 | 4–8 | Error: wrong price or date. Fix: numbers rendered by code plus a numbers diff check. TikTok via API can't add library sounds; post trend-sound videos natively or use Buffer's notification mode | Filming; final OK; choosing the sound |
| 3 Reservations | One order sheet: Form → Sheet (already native) + DM orders added via a 20-second "manual add" form; auto order code (UM-ARMY-0143); slot counter per GO | **Google Forms + Sheets + Apps Script** (free; 90 min/day trigger runtime) | 0 | 4–6 | Error: duplicate orders. Fix: dedupe on phone/handle | Accepting edge-case orders; refusing bogus buyers |
| 4 Payments | (P1) Payment log with ref no. + amount; due/overdue list. (P2) LLM vision pre-reads screenshots (amount, ref no., date, name), flags duplicate ref numbers and amount mismatches; weekly reconciliation against the GCash PDF history. (P3) Payment links that mark "paid" through a webhook | P1 **Sheets**; P2 **Claude vision** (Sonnet 5.5 or Haiku 4.5); P3 **PayMongo** (QR Ph 1.34%, Maya 1.79%, GCash 2.23%) or GCash for Business CSV | P1 0; P2 1–3; P3 % of sales | P1 2; P2 8–10; P3 8–12 | Fake or edited receipts. The bot **never** confirms a payment, it only pre-fills and flags. PayMongo/G4B need a registered business ([F] G4B requires DTI-registered sole prop + a verified GCash account with 12 months of activity) | Final "paid" tick; refunds; disputes |
| 5 Order placement | Nothing beyond a checklist and a reminder ("Weverse drop 11:00 KST = 10:00 PH") | Calendar reminder from the GO sheet | 0 | 1 | — | Buying (high stakes, sells out) |
| 6 Batch tracking | One batch table (status + date + note). Every order inherits its batch status. A status change triggers a draft public update + an "affected buyers" list | **Sheets** batch table + Telegram "status changed → draft post?" | 0 | 3–4 | Error: wrong batch mapping. Fix: owner confirms each status change | Choosing honest wording on delays |
| 7 Arrival | Auto-generate the "arrived" checklist: who paid in full → ready to ship; who owes a balance → reminder drafts | Sheet views + Telegram | 0 | 2 | Low | Unboxing, sorting photocards |
| 8 Shipping | Shipping list by courier; tracking number pasted into the sheet appears on the lookup page. (Later) Lalamove API quotes and bookings | **Sheets**; Lalamove API ([F] PH supported, prod keys after wallet top-up). J&T/LBC: manual booking [U: no small-shipper API checked] | 0 | 2 | Low | Packing, booking pickups |
| 9 Customer updates | **"Check my order" page**: order code + last 4 digits of the phone → item, batch status, paid, balance, next DOP date, tracking no. Linked in the X bio, the TikTok bio link hub, auto-replies and the pinned post. (P2) SMS for arrival / balance due, **without links** | P1 **Apps Script web app** or a static page on Andrey's server fed from the sheet. P2 **Semaphore SMS** (₱0.56/SMS ex VAT). P3 ManyChat Messenger "status" flow (Pro $29–39/mo) | 0–2 | 6–8 | Privacy (Data Privacy Act RA 10173): never publish a public tracker with names + amounts. Globe blocks SMS with clickable links ([F] 2025) | Delay apologies, complaints |
| 10 Content | Weekly idea list from **real inputs only** (news with links, top own posts, real buyer questions), caption drafts, banned-phrase check | Server job + Claude API; approval in Telegram; output goes to `content/ideas/`, `content/drafts/` | 2–6 | 6–10 | Slop and invented facts. Fix: source IDs mandatory, banned list, numbers from the sheet, human approval | Filming, talking, final caption voice |
| 11 Engagement | Native auto-replies (FAQ: price, DOP, how to order, "check status here"); a saved-reply library in Taglish; daily DM/comment triage with suggested replies | TikTok auto-messages (**needs Advanced Access + Verified Business Account**); Meta Business Suite automations (if an FB page exists); X: pinned "How to order / Check status" post (X DMs now run on the encrypted X Chat API, which is heavy to build on) | 0 | 3–4 | Unofficial DM bots or browser bots logged into the account = ban risk ([F] TikTok Community Guidelines). Auto public replies feel cold | Real conversations, negotiation, complaints |
| 12 Analytics | Weekly report: TikTok plays/shares per video, X views per post, form orders per GO and per channel ("Where did you see this GO?" form question) | **Apify** weekly: own TikTok 30 videos ≈ $0.11, comments ≈ $0.06, X 25 posts ≈ $0.01 → Telegram/Markdown report | 0.5–2.5 | 4–6 | Scraping public data is against TikTok's ToS in general, but no shop credentials are used, so the account is not exposed. Keep volumes small | Deciding what to change |

---

## 4. Tool facts (with sources)

### 4.1 TikTok posting and scheduling

- [F] **Content Posting API, Direct Post:** "All content posted by unaudited clients will be restricted to private viewing
  mode". Unaudited clients "can only post to a private account". 6 requests/min per user token; a daily post cap
  exists (`spam_risk_too_many_posts`). Source: TikTok Direct Post reference (S1).
- [F] **Audit rejects in-house tools.** The guidelines list as rejected: "A utility tool to help upload contents to the account(s) you
  or your team manages". UX rules also require a privacy dropdown with no default, editable captions, a preview and a consent line
  (S2). Practical meaning: **Andrey can't get a private "post for Unnie Mart" app audited.** Use an audited third party.
- [F] **Upload to inbox/drafts** (`video.upload`): "users must click on inbox notifications to continue the editing flow in
  TikTok and complete the post". "At most 5 pending shares within any 24-hour period" (S3). This is the natural
  hand-off for the future plug-in editor: the draft lands in the TikTok app, and the owner adds the trending sound and posts. [U] Whether
  an unaudited app may use it for a non-sandbox account isn't stated. Test in the sandbox.
- [F] Bundle.social (2026-08-04): unaudited posts publish "as private… nothing in the API tells you", and the audit takes weeks (S4).
- [F] **TikTok Studio native scheduler:** desktop web only, 15 min to 10 days ahead, Business/Creator accounts; you
  "cannot edit the video, caption, or time" after scheduling (postfa.st, updated 2026-10-01; adaptlypost, July 2026) (S5, S6).
- [F] **Buffer:** Free plan = 3 channels, 10 scheduled posts per channel, 30-day analytics, comment inbox. Essentials
  $5/channel/mo yearly ($6 monthly) (S7, S8). TikTok: automatic or notification publishing. "Due to API limitations, we do not
  have access to TikTok's audio/music library". Limits of 5 hashtags and 25 posts per 24 h (S9). Supports X too.
- [F] **Metricool:** Free = 1 brand, 20 posts/month, 30-day analytics, 5 competitors. Starter from $20/mo (annual,
  5 brands), unlimited posting, and an inbox that includes TikTok comments (S10).
- [F] **Later:** Starter $18.75/mo billed yearly (30 posts per profile per month), 14-day trial, no free plan; TikTok
  auto-publish included (S11).
- [F] Adaptlypost: "TikTok permits 15 posts per account per 24 hours across all connected third-party apps combined" (S6). [U] Single source.

### 4.2 TikTok DMs and comments

- [F] **Native auto-messages** (welcome, keyword reply, suggested questions, chat prompts) "only available to TikTok
  accounts with Advanced Access and Verified Business Account (VBA) status". Updated May 2026 (S12). Keyword reply:
  keywords ≤40 chars, replies ≤500 chars. New messages are reviewed in about 1–5 days (from search snippets of the same article) [U on the limits].
- [F] **Business Messaging API window:** after a user's message, a business can send up to 10 messages in 48 h. If the user
  replies, the window resets. Businesses "cannot initiate conversations" (respond.io, modified 2026-09-06; Wati, 2026-09-02) (S13, S14).
- [U] **PH availability conflicts.** Wati excludes only the US/EEA/CH/UK/India, so PH is included (S14). Statusbrew: "APAC, LATAM,
  METAP, United States, or Canada" (S15). respond.io lists PH only under **media sending unavailable** (S13). Qiscus lists PH as an
  "Unsupported Region" (S16). Qiscus may have misread the media list, but nobody has tested it for this account. Also
  [F] Qiscus: a daily cap of "100–200 conversations" per business account (S16).
- [F] **ManyChat on TikTok:** US launch in Nov 2025. Comment-to-DM is "partially rolled out for users located in Vietnam, Thailand
  and Indonesia". Not available in the EU/UK (InstantDM summary of ManyChat community posts, 2026-08-25) (S17). The ManyChat
  community pages returned 403 to us, so the regions were not confirmed first-hand. [U]
- [F] **Ban risk:** TikTok's ToS bars "bots or scraping… unless TikTok has approved it in writing". The Integrity rules ban
  "automation tools, scripts, or tricks designed to bypass TikTok's systems" and fake engagement. Enforcement runs from
  removal to restricted reach to a ban (InstantDM summary, 2026-08-25, citing tiktok.com/legal and the Integrity policy) (S18).
  **Safe:** native auto-messages, official API partners, scheduling via audited tools. **Unsafe:** browser bots logged in
  to the shop account, auto-like/follow/comment, cold DMs.

### 4.3 Meta (Facebook / Messenger / Instagram)

- [F] **Meta Business Suite automations:** instant reply, away message, FAQ, custom keywords, comment-to-message (hashtag-triggered),
  "identify unanswered messages". Private reply: "Only one message can be sent to the person who commented", within 7 days.
  The 24-hour window applies after that (InstantDM, 2026-08) (S19).
- [F] **Messaging rules:** a 24-hour standard window. The Human Agent tag allows manual replies up to 7 days but needs app review
  and business verification (S20, S21).
- [F] **Message tags deprecated:** CONFIRMED_EVENT_UPDATE, ACCOUNT_UPDATE and POST_PURCHASE_UPDATE return error 100 from
  **2026-04-27**. Migrate to Utility Templates or the Marketing Messages API (Messenger changelog) (S22). Utility templates support named
  parameters such as `{{order_id}}` (2026-03-06) and images (2025-09-29) (S22).
- [F] **Marketing Messages on Messenger** (opt-in, paid) is available in the Philippines (Meta docs, updated 2026-04-17) (S23).
  [U] PH per-message price not found.
- [F] **ManyChat pricing changed on 2026-03-02.** Free = 25 active contacts/month (was 1,000). Pro $29/mo annual ($39 monthly)
  for 2,500 active contacts. An "active contact" is anyone messaged in the cycle (Featurebase, 2026-10-07) (S24). [U] An
  "Essential ~$15 / 250 contacts" tier appears only in a search snippet.
- [F] InstantDM: free (500 automations/mo), $9.99/mo and $24.99/mo plans; covers FB + IG comment-to-DM (S19).

### 4.4 Messaging habits in the Philippines (owner and customer channels)

- [F] Messenger: 98.0M users in PH in Sept 2026 (80.7% of the population). The 25–34 age group is the largest (NapoleonCat) (S25).
- [F] DataReportal Digital 2026 PH (data from Oct 2025): Messenger 67.1% of internet users, TikTok 65.3%, YouTube 60.8%,
  Instagram 27.4%, X 8.1%. TikTok ad reach: 64.0M adults (S26). Viber, Telegram and WhatsApp were not reported.
- [F]/[U] Viber is "the most popular messaging app for customer interactions" in PH (Infobip 2025 report, via a NoypiGeeks
  search snippet; the primary source was not fetched) (S27).
- [F] **Viber bots: "since 5.02.24, Viber bots can only be created on commercial terms"** (Viber developer docs) (S28).
  [U] The exact monthly fee was not confirmed.
- [F] Telegram Bot API: free. Andrey's server already runs Telegram bots. [U] There is no reliable PH Telegram usage share, so treat it
  as niche for customers but fine as an **owner-ops tool**.
- [I] For this shop, buyers' DMs arrive on **X** and **TikTok** (that's where "DM to avail" is posted), so a channel-agnostic lookup
  link beats building one bot per app.

### 4.5 Payments (GCash / Maya)

- [F] **Personal GCash:** the app shows the past 90 days (15 at a time). Older history is requested in-app for up to 4 years and arrives by
  email as a **PDF protected by a password** (last name + last 4 digits of the mobile number). There is no CSV and no API (GCash help, updated 2026-10-14) (S29).
- [F] **GCash for Business:** a web portal with "Export / Download CSV" (ref no., date, status, gross, fees, net, product,
  source) (S30). Requirements: the registrant is the authorized signatory of a government-registered business (sole prop, partnership or
  corporation), and a fully verified GCash account **with at least 12 months of activity**, in a low-risk industry (S31).
- [F] **PayMongo** fees: GCash 2.23%, Maya 1.79%, QR Ph 1.34%, cards 3.125% + ₱13.39. No monthly fee for payment
  acceptance. Settlement in 2–7 days (S32). Example [E]: a ₱2,650 lightstick via QR Ph costs ₱35.51 in fees.
  [U] Requirements for unregistered sellers were not checked.

### 4.6 SMS (fallback for "arrived / balance due")

- [F] Semaphore: ₱0.56 per SMS ex VAT (S33).
- [F] NTC ordered telcos to block malicious links in texts (Malaya report dated 2025-10-01). Globe blocks SMS containing clickable URLs, and Smart blocks
  URL shorteners (S34). **So: no links in SMS.** Say "Check your status at unniemart [page name]" instead.

### 4.7 Analytics and scraping

- [F] **Apify live prices (store API, 2026-10-14):** `clockworks/tiktok-scraper` $0.0037/result on the FREE tier ($0.003 BRONZE).
  `clockworks/tiktok-comments-scraper` $0.00125/comment (FREE). `apidojo/tweet-scraper` $0.0004/tweet. `harshmaur/reddit-scraper`
  $0.002/result.
- [F] **Our real runs on 2026-10-14:** 30 TikTok videos = $0.112; 396 videos = $1.19; 25 TikTok results = $0.075. Andrey's
  Apify accounts are on the FREE plan, each with a $10/month usage cap shown by the API.
- [F] **TikTok Display API** gives your own profile + recent videos. Video query fields include `view_count, like_count,
  comment_count, share_count` with the `video.list` scope (S35, S36). It needs a TikTok developer app approved for these scopes plus
  the shop's OAuth consent [U: review effort not checked]. Apify covers the same public numbers without an app.
- [F] **TikTok Research API** is academic/non-profit only (US, EEA, UK, CH, Canada). "Commercial entities are explicitly
  ineligible" (S37). **Not an option.**
- [U] TikTok Studio's own analytics export (download CSV/XLSX). The help pages render client-side and could not be confirmed. The owner can check
  "Download data" in TikTok Studio on the web.
- [F] **TikTok Creative Center trends for PH were not scrapeable reliably today.** We ran two Apify actors on 2026-10-14:
  `datapeak/tiktok-creative-center` returned 0 hashtags and 0 songs for PH (and 0 for the US). `automation-lab/…` returned 1 row (US) when
  asked for the Philippines. Its docs say "TikTok currently exposes a small public sample". Cost was under $0.01. Use: owner or
  Andrey checks Creative Center by hand (logged in, free), or scrape PH K-pop hashtags and competitor GO accounts directly.

### 4.8 News and trend monitoring

- [F] Feeds tested 2026-10-14 (HTTP 200 + items): **Soompi** `/feed` (60 items), **Koreaboo** `/feed/` (10),
  **Rappler music** feed (10), **Philstar entertainment** RSS (40), and **Google News RSS**, PH edition. A query for
  `(ENHYPEN OR BABYMONSTER OR BTS) (Philippines OR Manila OR Bulacan) when:30d` returned 51 items, for example "ENHYPEN gets up
  close with Filipino fans at first Manila fansign" (Manila Bulletin, 2026-10-07).
  Blocked or none: allkpop RSS (403), kpopping (404), PULP Live World feed (404). Ticketing sites (SM Tickets, TicketNet) and Weverse
  have no RSS (HTML only). Ticketmaster PH returned 401.
- [F] Weverse Shop `robots.txt` disallows only `/*/order/*` and `/*/api/*`. The public HTML (about 55K chars of text) renders
  server-side, so a low-frequency page-change watcher is technically simple. [U] Weverse ToS not reviewed.
- [F] **X API (docs.x.com, 2026-10-14):** pay-per-use only, "no subscriptions". Post read $0.005, user read $0.010, post create
  $0.015, post with URL **$0.200**, owned reads $0.001. Cap: 3M post reads per month. $20 free credit on the first card (S38).
  Basic/Pro are closed to new signups (a 2026 secondary source says Basic closed in Feb 2026) (S39).
- [E] Monitoring 15 X accounts × 5 posts/day ≈ 2,250 posts/mo costs about $11/mo on the X API, versus about $0.90 with the
  Apify tweet scraper (scraping is against X ToS in general but uses no shop credentials) or $0 with the owner's own X list.
- [F] **X DMs** now run on the **X Chat API** (end-to-end encrypted; client-side keys via the "Chat XDK") (S40). An X DM bot is
  a heavy build. Prefer a pinned post + lookup link.

### 4.9 Google stack and LLM

- [F] Apps Script consumer quotas: URL Fetch 20,000/day, trigger runtime 90 min/day, 6 min per execution, 30
  simultaneous executions per user (S41).
- [F] Claude API prices per 1M tokens (in/out): Sonnet 5.5 $2/$10, Haiku 4.5 $1/$5, Opus 5.5 $4/$20 (Anthropic model table,
  cached 2026-09-25).
- [E] Drafting load per month: ~1.5M input + 140K output tokens (idea runs, ~40 captions, ~200 reply suggestions,
  ~160 screenshot reads). That's ≈ $4.4/mo on Sonnet 5.5, ≈ $8.8 on Opus 5.5, less with Haiku for screenshot extraction.
- [F] Lalamove API supports the PH market (quotations, orders, webhooks). Production keys come after a wallet top-up (S42).

---

## 5. Risks

| Risk | Where | Likelihood | Mitigation |
|---|---|---|---|
| **Account ban or reach drop** from unofficial automation | TikTok, X | High if anyone logs a bot into the shop account | Only native features and audited tools via OAuth. No browser bots with the shop's password, no auto-like/follow/comment, no cold DMs |
| **Private posts by surprise** | Own TikTok API app | Certain if we build one | Don't build one. Use Buffer/Metricool/Later or TikTok Studio |
| **Trend sound missing** on scheduled TikToks | API schedulers | Certain | Trend-sound videos are posted natively from the phone. Schedule only original-audio posts |
| **Wrong price, DOP date or ETA** in a caption or reply | LLM drafts, templates | Medium | Numbers rendered by code from the sheet; a numbers diff check blocks the draft if any figure isn't in the sheet; human OK before posting |
| **Invented facts, slop, fake scarcity** | LLM ideas | Medium | Every idea carries a source ID (news URL, comment ID, own post ID) or is dropped; banned-phrase list; "limited / last slots" allowed only if the sheet shows ≤N slots; Andrey's `clients/slop-check.py` reused as a lint |
| **Fake or edited GCash screenshots** | Payments | Real in PH | The bot never marks "paid". It flags duplicate ref numbers and amount mismatches; weekly reconciliation against the GCash PDF/CSV; Phase 3 payment links remove screenshots entirely |
| **Privacy leak** | Public trackers, lookup page | Medium | No public sheet with names and amounts (RA 10173, Data Privacy Act). Lookup by order code + last 4 phone digits; rate-limit; show first name initial only |
| **Proactive Messenger updates blocked** | Messenger | Certain outside 24 h | POST_PURCHASE_UPDATE is gone (2026-04-27). Use public status posts + lookup page; Utility templates (paid outside the window) only if a Messenger bot exists |
| **SMS not delivered** | SMS | High if a link is included | No URLs; registered sender name; only buyers who agreed to SMS |
| **Vendor price changes** | ManyChat, X API | Proven in 2026 | Keep the core free (Sheets + Telegram + own server); paid tools are optional layers you can drop |
| **TikTok DM API not available in PH** | DM automation | Unclear | Treat it as an experiment in Phase 3; the lookup link works without it |
| **Cold-bot feel** | All DM automation | Medium | Bots answer only FAQ and status in the shop's Taglish voice and hand off to a human with "Wait lang po, si Unnie na sasagot 💖" |
| **Single point of failure** (Andrey's server) | Digest, lookup page | Low–medium | Apps Script version of the lookup page as a backup; the sheet stays usable by hand |

**Do-not-do list:** AI voices or avatars, AI-generated product photos, fake reviews or testimonials, bought followers,
auto-generated engagement, auto-sent messages to customers without an owner OK (except FAQ/status replies to
inbound DMs), posting through our own unaudited TikTok app.

---

## 6. Recommended stack, in phases

### Flow (all phases)

```
 DATA IN                          PROCESSING (Andrey's server: cron/systemd)        OWNER (Telegram bot)            OUT
 ───────                          ──────────────────────────────────────────        ────────────────────            ───
 Google Form ──► ORDER SHEET ◄── "manual add" form (DM orders)
 (order + proof)    │  (single source of truth: orders, payments, batches, GOs)
                    ├──► due / overdue / slots calc ───────────────────────────► 09:00 digest ──────────────► owner sends reminders
                    ├──► lookup JSON (code + last4) ─────────────────────────────────────────────────────────► "Check my order" page
                    ├──► batch status change ──► draft status post ────────────► [Approve/Edit] ─────────────► Buffer → X / TikTok
 Payment screenshot ┴──► (P2) vision pre-read + dup-ref check ────────────────► [Confirm paid] ──► sheet
 RSS + Google News ─────► filter by fandom keywords + dedupe ──────────────────► news digest (links)
 Apify weekly (own TikTok/X) ──► stats + top posts ────────────────────────────► weekly report
 Real comments/DM questions ─┐
 News items ─────────────────┼─► (P2) LLM idea + caption drafts (source IDs, ──► [Approve/Edit/Reject] ──────► owner films / posts
 Own top posts ──────────────┘     numbers from sheet, banned-phrase lint)                                           (CapCut now,
                                                                                                                    plug-in editor later)
```

Rules baked into the flow: nothing reaches a customer or a public feed without an owner tap, except native FAQ
auto-replies to inbound DMs and the self-service lookup page.

### Phase 1: free or cheap, under one week, biggest time saved

| # | Build | Tools | $/mo | Setup |
|---|---|---|---|---|
| 1 | **Order sheet as the single source of truth**: tabs GOs (item, tiers, DP, DOP dates, ETA, source link, slots), Orders (auto order code), Payments, Batches (status timeline). Plus a "manual add" form for DM orders | Google Forms/Sheets + Apps Script | 0 | 6 h Andrey + 2 h owner |
| 2 | **"Check my order" page** (order code + last 4 digits of the phone) showing status, paid, balance, next DOP, tracking. Put it in the X bio, the TikTok bio link hub and a pinned X post | Apps Script web app or static page on the server | 0 | 6 h |
| 3 | **Owner Telegram bot, daily 09:00 PH**: new orders, payments to verify, due in 3 days, overdue, slots left per GO, batch ETA changes. Buttons: mark checked, snooze | Andrey's server + Telegram Bot API | 0 | 5 h |
| 4 | **Native auto-replies + saved Taglish replies**: TikTok (if VBA-eligible) and Meta (if an FB page exists): price → GO post; "status/update" → lookup page; "how to order" → form. Saved replies for X DMs | TikTok Business, Meta Business Suite | 0 | 3 h owner + Andrey |
| 5 | **K-pop news digest** for the shop's fandoms, with links, deduped, daily | Google News RSS + Soompi/Koreaboo/Rappler/Philstar RSS | 0 | 4 h |
| 6 | **Free scheduling**: batch the week's X posts + original-audio TikToks | Buffer Free (X + TikTok + 1) or TikTok Studio scheduler | 0 | 1 h |
| 7 | **Weekly stats report** (own TikTok + X) | Apify (≈ $0.2/week) | 0.5–1 | 4 h |
|   | **Total** |  | **$0–3/mo** | **~25–30 h Andrey, ~4–5 h owner** |

**Hours saved per week: about 3.5–5 h** [E]. Reasoning, using assumed volumes (2–4 open GOs, ~50 active orders,
40–80 DMs/week, ~10 posts/week; validate them with a one-week time log):
- Status/"update po?" DMs: 10–25/week × 3 min = 30–75 min. The lookup page and auto-reply deflect ~60%, saving **20–45 min**.
- FAQ DMs (price, DOP, how to order): 15–30 × 2 min = 30–60 min. Native or saved replies halve it, saving **15–30 min**.
- News scrolling: ~20 min/day = 140 min. A 30-min digest saves **~110 min**.
- Finding who owes what before each DOP: 30–60 min. The auto due list saves **15–30 min**.
- Re-finding orders across Form/DMs/notes: ~30–45 min. One sheet + order codes saves **20–35 min**.
- Batching posts in a scheduler instead of posting live daily saves **~20 min**.

### Phase 2: weeks 2–6, after Phase 1 is used daily

| # | Build | Tools | $/mo | Setup |
|---|---|---|---|---|
| 1 | **Payment pre-check**: screenshot → amount, ref no., date, name pre-filled; duplicate-ref and amount-mismatch flags; owner taps Confirm. Weekly reconciliation against the GCash PDF history (owner uploads it) | Claude vision (Haiku 4.5 / Sonnet 5.5) + server | 1–3 | 10 h |
| 2 | **Caption and idea drafts with guardrails**: WTS caption from the GO row (code fills numbers, LLM writes only the Taglish hook line); weekly idea list from real comments, news links and own top posts. Approval in Telegram, then to Buffer or copy-paste | Claude API + Telegram + Buffer | 2–5 | 10 h |
| 3 | **DOP reminder drafts** per buyer (Taglish, personal, with amount and date from the sheet) for the owner to send. Optional SMS (no links) to buyers who agreed to it | Sheet + Telegram; Semaphore SMS | 0–3 | 4 h |
| 4 | **Spike mode for viral posts**: when a TikTok passes N plays, scrape its comments, classify them (price ask / reserve / complaint) and send suggested replies to the owner | Apify comments ($0.00125/comment) + LLM | 0–1 | 4 h |
| 5 | Optional **Metricool Starter** if the owner wants one inbox (TikTok comments + FB/IG) and competitor tracking | Metricool | 0 or 20–25 | 2 h |
|   | **Total** |  | **$3–12/mo** (≈ $25–37 with Metricool) | **~30 h** |

**Additional hours saved: about 2–2.5 h/week** [E] (cumulative ~5.5–7.5 h):
- Payment checks: 25–40/week × 3 min = 75–120 min. Pre-fill + flags save ~50%, so **40–60 min**.
- Captions: ~10/week × 10 min = 100 min. Drafts from sheet data save ~50%, so **~50 min**.
- Reminders: drafted messages cut 2 min → 30 s each, so **20–30 min**.
- Spike triage: only during spikes; occasional saving of **0–30 min**.

### Phase 3: month 2–3+, only if volume justifies it

| # | Build | Tools | $/mo | Setup |
|---|---|---|---|---|
| 1 | **Payment links with webhooks**: DP and DOP links per order, auto-marked paid. Kills screenshot checks for buyers who use them | PayMongo (QR Ph 1.34%) or GCash for Business (needs DTI + 12-month GCash) | % of sales (≈ ₱36 per ₱2,650) | 10–12 h |
| 2 | **In-channel DM bot for FAQ + status** where the volume is: Messenger/IG via ManyChat (External Request to the lookup JSON); TikTok DMs only after a live PH test with a partner | ManyChat Pro $29–39; TikTok partner TBD | 29–60 | 8–12 h |
| 3 | **Restock and drop watchers** on specific Weverse Shop / Ktown4u product pages (every few hours, read-only) | Server cron | 0 | 4–6 h |
| 4 | **Upload-to-drafts hand-off** for the future plug-in editor: edited video → TikTok inbox draft → owner adds the sound and posts | TikTok `video.upload` (≤5 pending per 24 h) | 0 | (later) |
|   | **Total** |  | **≈ $30–60/mo + payment fees** | **~25–30 h** |

**Additional hours saved: about 2–2.5 h/week** [E] (cumulative ~7.5–10 h): payment verification mostly gone (45–60 min),
in-channel FAQ/status deflection (30–60 min), less manual drop-watching (20–30 min).

---

## 7. What stays human (on purpose)

- Filming and talking on camera. Choosing the trending sound. The final caption voice.
- Deciding which GOs to open, pricing, buying on Weverse at drop time.
- Final "paid" confirmation, refunds, cancellations, complaints, delay apologies.
- Real conversations with buyers (the "unnie" relationship is the brand).
- Packing, photocard sorting, courier handover.

## 8. Open questions for the owner (needed before building)

1. Real weekly volumes: DMs per channel, active orders, payments per week, posts per week (one-week time log).
2. Is there an active Facebook page or Messenger inbox? Instagram?
3. GCash personal or GCash for Business? Is the shop DTI-registered? Maya/bank too?
4. What does the Google Form collect (proof upload, phone, X/TikTok handle)? Where do responses live today?
5. Couriers used (J&T, LBC, Lalamove, meetups at Cubao)? Who books and how?
6. Are the TikTok Shop, Shopee and Lazada stores active? (Marketplace orders get platform tracking for free.)
7. Is the TikTok account a Business account, and is it eligible for Advanced Access / VBA (auto-messages)?
8. Will the owner use Telegram for the daily digest? If not: an email digest, or Messenger via a Page (limited by the 24 h window).

---

## Sources (accessed 2026-10-14 unless noted)

- S1 TikTok Direct Post API reference: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- S2 TikTok Content Sharing Guidelines: https://developers.tiktok.com/doc/content-sharing-guidelines
- S3 TikTok Upload (inbox) API reference: https://developers.tiktok.com/doc/content-posting-api-reference-upload-video
- S4 bundle.social, TikTok API approval (2026-08-04): https://bundle.social/blog/tiktok-api-approval
- S5 PostFast, TikTok scheduling on desktop (updated 2026-10-01): https://postfa.st/blog/how-to-schedule-tiktok-posts-on-desktop-in-2025-plus-bonus
- S6 AdaptlyPost, how to schedule TikTok posts (July 2026): https://adaptlypost.com/en/blog/how-to-schedule-tiktok-posts
- S7 Buffer pricing: https://buffer.com/pricing
- S8 NapoleonCat, Buffer pricing (2026-08-26): https://napoleoncat.com/blog/buffer-pricing/
- S9 Buffer help, using TikTok with Buffer: https://support.buffer.com/article/559-using-tiktok-with-buffer
- S10 Metricool pricing: https://metricool.com/pricing/
- S11 Later pricing: https://later.com/pricing/
- S12 TikTok Business Help, automatic messages (updated May 2026): https://ads.tiktok.com/help/article/navigate-auto-message-business-accounts?lang=en
- S13 respond.io TikTok overview (modified 2026-09-06): https://respond.io/help/tiktok/tiktok-overview
- S14 Wati, TikTok DMs (2026-09-02): https://support.wati.io/en/articles/15701340-how-to-connect-and-manage-tiktok-messages-dms-in-wati
- S15 Statusbrew, TikTok DMs requirements: https://statusbrew.com/help/articles/tiktok-direct-messages-not-working
- S16 Qiscus, TikTok Direct Message: https://documentation.qiscus.com/latest/omnichannel-chat/tiktok-direct-message
- S17 InstantDM, TikTok comment to DM (2026-08-25): https://instantdm.com/blog/tiktok-comment-to-dm
- S18 InstantDM, is TikTok automation allowed (2026-08-25): https://instantdm.com/blog/is-tiktok-automation-allowed
- S19 InstantDM, Facebook comment automation (2026-08): https://instantdm.com/blog/facebook-comment-automation
- S20 InstantDM, Facebook DM automation (2026-08-28): https://instantdm.com/blog/facebook-dm-automation
- S21 Meta Send API reference: https://developers.facebook.com/docs/messenger-platform/reference/send-api
- S22 Meta Messenger Platform changelog: https://developers.facebook.com/documentation/business-messaging/messenger-platform/changelog
- S23 Meta Marketing Messages on Messenger: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger
- S24 Featurebase, ManyChat pricing (2026-10-07): https://www.featurebase.app/blog/manychat-pricing
- S25 NapoleonCat, Messenger users in PH (Sept 2026): https://napoleoncat.com/stats/messenger-users-in-philippines/
- S26 DataReportal, Digital 2026 Philippines (published 2025-11-05): https://datareportal.com/reports/digital-2026-philippines
- S27 NoypiGeeks on Infobip 2025 report (search snippet only; page blocked): https://www.noypigeeks.com/?p=272178
- S28 Viber REST Bot API docs: https://developers.viber.com/docs/api/rest-bot-api/
- S29 GCash help, how to request transaction history: https://help.gcash.com/hc/en-us/articles/360034155433-How-to-request-transaction-history
- S30 GCash help, GCash for Business transaction history: https://help.gcash.com/hc/en-us/articles/48457463083545
- S31 GCash help, GCash for Business requirements: https://help.gcash.com/hc/en-us/articles/48456974006041-What-are-the-requirements-to-create-a-GCash-for-Business-merchant-account
- S32 PayMongo pricing: https://www.paymongo.com/pricing
- S33 Semaphore SMS: https://www.semaphore.co
- S34 Malaya, NTC orders blocking of texts with links (2025-10-01): https://malaya.com.ph/news/ntc-orders-blocking-of-texts-with-links (plus carrier summary in sent.dm PH SMS guidance)
- S35 TikTok Display API overview: https://developers.tiktok.com/doc/display-api-overview
- S36 TikTok Query Videos: https://developers.tiktok.com/doc/tiktok-api-v2-video-query
- S37 TikTok Research API: https://developers.tiktok.com/products/research-api/
- S38 X API pricing: https://docs.x.com/x-api/getting-started/pricing
- S39 PostProxy, X API pricing 2026: https://www.postproxy.dev/blog/x-api-pricing-2026/
- S40 X Chat API intro: https://docs.x.com/xchat/introduction.md
- S41 Google Apps Script quotas: https://developers.google.com/apps-script/guides/services/quotas
- S42 Lalamove developers: https://developers.lalamove.com/
- GO workflow: Huckleberry PH terms https://huckleberryph.carrd.co/ · KIMXTAEGOS terms https://kimxtaegos.carrd.co/ ·
  Paysable GOM guide (2026-03-03) https://blog.paysable.com/?p=1512 · Kfriday (2026-01-05) https://www.kfriday.net/posts/kfriday/996
- Reddit (via Apify, 2026-10-14): r/kpophelp "Renting korean rental address or join GO's" (2026-02-08)
  https://www.reddit.com/r/kpophelp/comments/1qyx8cr/ · "need help on selling kpop merch (from philippines!)" (2026-07-07)
  https://www.reddit.com/r/kpophelp/comments/1upm6qr/
- Own data: `data/raw/tiktok-latest-2026-10-14.json`, `data/raw/tiktok-popular-2026-10-14.json`; X scrape of @unniemart_ (10 posts);
  Apify store API prices and run costs; feed tests (curl) for Soompi, Koreaboo, Rappler, Philstar, Google News, allkpop, Weverse.

Research spend on Apify for this report: under $0.40 (Reddit search + threads, the X profile, Creative Center tests).
Note: the web search quota ran out midway, so later checks used direct fetches of primary pages. Anything not fetched
first-hand is marked [U].
