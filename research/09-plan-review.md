# 09 · Plan review: what's wrong, weak or missing

Date: 2026-10-14. Reviewer: review agent. Status: **findings only, no plan files edited.**

Reviewed: `strategy/STRATEGY.md`, `strategy/PLAYBOOK.md`, `strategy/AUTOMATION.md`, `strategy/OWNER-QUESTIONS.md`,
`content/ideas/2026-10-W42-W44.md`, against research 01 to 07.

How I checked:
- I read all 7 research reports and all 5 plan files in full.
- I re-computed the key numbers from `data/own-videos.csv`, `data/comments.csv` and `data/competitor-videos.csv` with pandas.
- I ran three web checks: the ENHYPEN Bulacan 2025 concert date, Heeseung's exit, and how far ahead TikTok Studio lets you schedule. Links are at the end.

Severity:
- **Must fix**: wrong or overstated facts that hold up the main bet, numbers that don't add up, or anything that would embarrass Andrey in front of the client.
- **Should fix**: weak logic, gaps, contradictions or risk that would hurt the result.
- **Nice to have**: polish.

Counts: 6 must fix · 20 should fix · 14 nice to have.

---

## MUST FIX

### M1 · The main bet's evidence is overstated, and its biggest risk (concert timing) isn't in the plan

**Where**
- STRATEGY §1: "The proof of what works is strong and comes from three directions at once"
- STRATEGY §1: "Across 923 videos from 20 similar shops, lightstick tutorials are the strongest format: 27 times the shop's normal views"
- STRATEGY §1 table: "1 lightstick tutorial | The format that historically does 6 times better than anything around it"
- STRATEGY §2: "Home fandom: ENHYPEN … Second: SEVENTEEN … Third: BTS"
- PLAYBOOK Card A: "Clinic (2 a week)"

**What's wrong**
1. **The niche evidence comes from 2 accounts, not 20 shops.**
   - The 7 tutorials in `competitor-videos.csv` come from `milky_kshop`, an Indonesian shop (5 videos), and `iamurgrace_`, a US creator who is not a shop (2 videos).
   - For sellers only, the median is **16.8× (n=5, one shop)**. The 27× figure includes the US creator.
   - The 923 videos come from **21 accounts**: 16 sellers (13 PH, one of them a Thai-merch GOM, plus 3 SEA) and 5 non-PH creators.
2. **The own-account record is mostly 2022 to 2023.**
   - 01 §2.2: tutorials from 2024 to 2026 have a median relative performance of **1.01** (5 videos).
   - Since 2025 there have been 4 lightstick tutorials: **2 hits and 2 flops**.
   - The only tutorial in the last 12 months (2026-05-01) got **571 views, 0.95× and 0 saves**. The plan's table implies the opposite.
3. **Every recent tutorial hit landed just before a PH concert by that fandom.** Neither the plan nor the research says so.
   - Caratbong V3, 2025-01-14 (30.5K): SEVENTEEN played Bulacan on Jan 18 to 19, 2025 (04 §1.4).
   - Engenebong V2, 2025-01-25 (225K): ENHYPEN's *Walk the Line* show in Bulacan was on **Mar 1, 2025** (ABS-CBN, GMA). The shop's own Feb 2025 posts carry `#wtlinbulacan`. The 225K video's comments peak in **March 2025** (10 of 53).
   - Hammerbong V2, 2023-03-02 (30K): BLACKPINK played Manila on Mar 25 to 26, 2023 (date from fan comments, 01 §9.1, unverified).
   - The flops had no concert close by. BLACKPINK V2, Jun 2025 (913 views): the PH show was 5 months away. ENHYPEN guide, May 2026 (571 views): the tour has no PH stop.
4. **The calendar doesn't fit the fandom order.**
   - 06 §1: **no ENHYPEN and no SEVENTEEN concert in PH in this window.** Five SEVENTEEN members enlist in the second half of 2026.
   - The only big matching concert is BTS. But BTS is the account's **weakest** fandom: 1 of 21 BTS posts ever doubled its neighbours, 5% (01 §3).
5. **Nobody knows whether tutorial views turn into sales.**
   - 01 §9.2 asks two open questions: did the hits sell (Q4), and can foreign viewers buy at all (Q8)? OWNER-QUESTIONS doesn't ask for orders after the 2025-01-25 tutorial.
   - The plan's answer to foreign reach is "Taglish voice … keep it local". That has no evidence behind it, and it conflicts with 02 Card A ("English, so international owners searching also land on it").
6. **No stock check, no cost of demo units, no saturation check.**
   - Clinic needs an opened unit of every model. You can't unbox a buyer's sealed item, so the shop must own demo units at ₱2,150 to ₱3,100 each.
   - VER.4 has been on sale since Feb 2026, and BTS is the biggest fandom worldwide. The VER.4 search results may already be crowded. Nobody checked TikTok search.

**Fix**
- Restate the evidence honestly: "8 own tutorials, strongest in 2022 to 2023 and Jan 2025; 2 of the last 4 hit. Elsewhere, one Indonesian shop (median 17×, n=5) and one US creator."
- Make **concert or launch timing** an explicit rule. Clinic topics go first to models with a PH concert or a new release within about 6 weeks:
  - BTS VER.4, now through Mar 16
  - ENHYPEN Renewal, at launch
  - LE SSERAFIM, Dec 5 to 6, and NCT 127, Dec 12, only if the shop stocks those lightsticks
- Drop SEVENTEEN from "second fandom" during the hiatus.
- Add owner questions:
  - Orders and DMs in the 7 days after the 2025-01-25 tutorial
  - Which demo units the shop already owns
- Before filming, search TikTok for "army bomb ver 4 connect" and "army bomb ver 4 bulacan" and log what's there.
- Add a 4-week kill rule. If the first 4 Clinic videos all sit near the account's normal views, cut Clinic to 1 a week.

### M2 · "Most of it is the shop's own content mix" has no support, and it sets the wrong expectation

**Where:** STRATEGY §1: "Part of this hits every small account … But most of it is the shop's own content mix."

**What's wrong**
- No research report splits platform from content. 01 §9.1 says the opposite: "The 2022-23 boom was partly the platform and timing … Format alone can't bring it back."
- 03 §2: "Unnie Mart's median reach (10% of followers) is in the same band as active PH sellers … The reach is not unusually bad." Its peers sit at 13%, 13%, 8% and 3%.
- If the client reads this as "fix your content and 2023 comes back", the targets in §8 will look like failures even when the plan works.

**Fix:** Replace it with something like: "Part platform (small accounts lost about 40% in 2025), part content and posting volume (7 posts in 90 days vs 26 to 50 at active peers). This data can't say which is bigger."

### M3 · The automation costs, hours and time saved don't add up

**Where:** STRATEGY §9 table, AUTOMATION §4.

| Item | Plan says | What the sources say |
|---|---|---|
| Phase A cost | STRATEGY: "~$2 to 5" | AUTOMATION: "~$5 to 9/month". Apify about $0.95/week ≈ $4/month, plus the model at $2 to 5. The $2 to 5 only holds if Apify stays on free credit (see S12). |
| Phase A setup | "about 12 to 16 hours" | 07's own parts: news digest 4 to 6 h, weekly stats 4 to 6 h, idea and caption drafts 6 to 10 h (10 h in 07 Phase 2). That's **14 to 22 h before the peer watcher**. |
| Phase B time saved | "3.5 to 5 hours a week (07)" | 07's 3.5 to 5 h includes the **news digest (~110 min/week)** and post batching. The plan moved the digest to Phase A. The order-desk items alone save **~1.5 to 2.7 h/week** (07 §6: 20–45 + 15–30 + 15–30 + 20–35 + 20 min). 07's own line items add up to **3.3 to 4.5 h**, not 3.5 to 5. |
| Phase B setup | "~25 to 30 hours (07)" | 07's 25 to 30 h includes the news digest (4 h) and weekly stats (4 h), which are now in Phase A. They're counted twice. Phase B alone is about **21 h of Andrey's time plus 4 to 5 h of the owner's**. |
| Phase B cost | STRATEGY "$0 to 3" | Every row in AUTOMATION Phase B is $0. |
| Phase C cost | "$3 to 60" | 07 Phase 2 ($3 to 12, or $25 to 37 with Metricool) plus Phase 3 ($30 to 60) comes to **$33 to 72/month plus payment fees** (QR Ph 1.34%, GCash 2.23% of every sale). |
| Phase C time | "+2 to 5 hours a week (07)" | 07: +2 to 2.5 h for Phase 2 and +2 to 2.5 h for Phase 3, so **+4 to 5 h only if both are built**. |

**Fix:** Rebuild the §9 table from 07's line items. Show Andrey's hours, the owner's hours, the monthly cost and the fees separately. Label the time saved as an estimate built on volumes the owner hasn't confirmed: 40 to 80 DMs a week and about 50 active orders.

### M4 · Internal notes that must not reach the client

**Where**
- AUTOMATION §5: "Andrey's `WeverseShopAutomation` project snipes Weverse drops, but automated buying may break Weverse's terms. Not part of this plan."
- AUTOMATION §3: "Andrey's `clients/slop-check.py` can be reused as the checker"
- STRATEGY §7 refers to the same checker.

**What's wrong**
- The first line tells the client the consultant has a drop-sniping tool that may break the shop's main supplier's terms. That's a reputational risk, and it invites a request to use it.
- `slop-check.py` is a **Russian-language** checker tuned to Andrey's own posts. Its `BANNED` list is Russian phrases. It can't check Taglish captions as it stands.

**Fix**
- Delete the WeverseShopAutomation sentence.
- Replace the slop-check reference with "a new banned-phrase checker (Taglish and English list in PLAYBOOK)", and budget about 2 h for it.

### M5 · Card C's headline evidence comes from a post the research flagged as possibly paid

**Where**
- STRATEGY §3 row 3: "Same presenter, same wall: news-first got 10,300 views and 33 comments. Price-first got 629 views and 2 comments (02)"
- PLAYBOOK Card C: "'Comment Enchin' was the shop's best sales post at 17×"
- Ideas #5

**What's wrong**
- 01 §1.3 says the Enchin post's like rate (0.9%) is "well below the ~2% norm. That fits paid promotion … Ask the owner."
- 02 §12 Q3 asks whether M1 was promoted.
- The plan calls it the cleanest test and gives no caveat. If the owner paid to promote it, they'll spot the mistake at once.

**Fix**
- Add "(if it wasn't promoted, see owner question 4)".
- Until then, lean on the comment gap (33 vs 2), which says more than the views. Call Card C a **test**, not a proven format.

### M6 · Claims the owner or fans can check and find wrong

| Where (quote) | What's wrong | Evidence | Fix |
|---|---|---|---|
| STRATEGY §2: "The shop's comments already ask 'may Army Bomb po kayo?' more than anything else (01)" | False. It's the most-requested **other artist**: 15 of 73 requests. Stock questions number 220. | 01 §8.2 "Request: another artist or item" | "Among requests for artists the shop doesn't post, BTS comes first (15 comments)." |
| STRATEGY §1 table: "10 memes … Below average, every time (01, 02)" | 2 of the 10 beat their neighbours (1.49×, 1.25×). None doubled them. | `own-videos.csv`, last 12 months, type trend/meme/skit | "None of the 10 doubled normal; median 0.8×" |
| STRATEGY §3 and Ideas: "0 of 12 beat average since 2024" | 0 of 12 **doubled** normal. 2 of 12 beat it. Median 0.81. | 01 §2.2 (% ≥2× = 0%); CSV | Same wording fix |
| STRATEGY §1: "Nobody in the Philippine shop scene is explaining it yet" (VER.4 sync) | Unsupported. 03 sampled the last 50 videos of 13 PH accounts and never searched for VER.4 explainers. PH shops do sell VER.4: forever9ph had "FETA onhand" Army Bombs in Feb 2026 (04 sources). | 03 §1, §6 | "We didn't find one in a 13-shop sample". Then search TikTok to confirm. |

---

## SHOULD FIX

### S1 · Other number mismatches

| Where | Plan says | Correct |
|---|---|---|
| PLAYBOOK rule 1 | "VB: 5 of 6 hits show the real item" | **4 of 6** (H2, H3, H4, H6). H1 and H5 show the idol. 02 §8.1 contradicts itself here. |
| STRATEGY §3, PLAYBOOK, AUTOMATION | BABYMONSTER "views fell each time: 1,186 → 446" | 1,186 → 629 → 598 → 430 → **446** (the last one rose). The account baseline fell over the same months too (May median 544, Aug 438), so "reposting burns the offer" is mixed up with the general decline. |
| STRATEGY §10 | "all 12 are in OWNER-QUESTIONS.md" | **14** |
| STRATEGY §8, OWNER-Q #11 | "23% of the comments on the 225K tutorial weren't from the Philippines" | 12 of 53 comments (23%) are in Spanish, Indonesian or Korean. That's language, not location. A 53-comment sample. |
| STRATEGY §2 | "lightsticks at ₱2,500 to ₱3,500" | The shop's own captions show **₱2,150** (BABYMONSTER pay-in-full price, May 2026) to **₱3,100** (Caratbong, last due date). |
| STRATEGY §5 | "On-hand items not linked to TikTok Shop (2% of posts …)" | 2% of the **latest 50**. All-time it's 25% (101 of 396), and 01 §7 found no significant effect within the same period (p = 0.16). |
| STRATEGY §1 | "most-liked comment on the whole account" | Most-liked in the **sample** (1,057 comments on 29 videos). |
| STRATEGY §3 | Posting more "doesn't raise the average (05, Buffer)" | Buffer: **+17% views per post on average** going from 1 to 2–5 posts a week. The *median* stayed flat. Say "the typical video". |
| STRATEGY §1 | "From 1,015 real fan comments" (presented as current) | 889 of the 1,015 come from 2022–23 videos (01 §8). Add that. |

### S2 · Small samples stated as rules

| Where (quote) | Evidence behind it | Fix |
|---|---|---|
| STRATEGY §4.1 / PLAYBOOK 2: "something visibly changes within 1.5 seconds" | One video (H2, 1.3 s). H6 paid off at 2.5 s (30.5K) and H1 at 4.0 s (226K). | "within the first 2 to 4 seconds; faster is better" |
| STRATEGY §4.5: "Two seconds of nothing at the end loses viewers" | No retention data. Two flops (L1, L3) had end cards. | Keep the rule and call it a guess until Studio data arrives. |
| STRATEGY §4.3: "Model-name hashtags were the only hashtags with any effect" | 01 §7 calls this an inference. The tags fall in the SEVENTEEN 2023 ticket window (#svtlightstick, 8 videos). | "looked strongest, small sample" |
| STRATEGY §1: "Lightstick sales follow ticket day" | 63 comments on 4 SEVENTEEN videos from 2023, 45 of them on one video. No sales data. | "Fans say they buy after getting a ticket" |
| STRATEGY §1: "Trust questions never stop" | 27 comments (2.7%) | "come up on 10 of 29 videos" |
| STRATEGY §2: "Price posts die in a day" | No time-series data. (The search half of that line has some support: the 225K video's comments run across 18 months.) | Delete the price-post half. |
| STRATEGY §4.2 / PLAYBOOK 3: "Never the DP alone"; "Fans have read a ₱100 down payment alone as proof the item is fake" | 1 to 2 comments. 02 Card E recommends the **opposite** as a test: "lead with the smallest number (₱300 DP)". | See S4 |
| STRATEGY §4.8: "TikTok first shows a new video to people in the region it was posted from" | See S14. | |

### S3 · Selective evidence: old or one-off hits quoted without context

- **"The shop's own reply video on installments got 42,500 views"** (STRATEGY §3, PLAYBOOK Card D). That was 2023, during the SEVENTEEN ticket window. The 2025 installment reply got **1,342 (1.01×)**. Quote both.
- **"Stock wall: 71,600 views on 6 seconds"** (STRATEGY §3, ideas #6). That was 2023-10-05, with 45 "ticket first" comments, inside the SEVENTEEN tour window. The other recent stock hit (M3, 11.9K, Nov 2025) also sat in a SEVENTEEN tour window. The 2026 arrival clip got 416. Stock walls look concert-timed too.
- **"A Philippine shop's arrival-day vlog did 151×"** (STRATEGY §3, ideas #9). One video, from **2021**, pinned, by an account inactive since Feb 2024. It's a "day in the life", not an arrival vlog. Add the date and "n=1".
- **"The 226,000-view hit was this kind of video"** (STRATEGY §3 bonus, PLAYBOOK bonus). It was a Weverse video call, not a concert or cinema moment, and nobody knows whose call it was. Non-sales concert content is the account's **weakest** type (median 0.60×; 0.63× for 2024–26, 01 §2). The 56K repost came 7 weeks after Heeseung left ENHYPEN, which is another timing effect. Drop "this kind of video". Don't give "Real fan moment" a format strength of 3 (see S10).

### S4 · Money worry and installments, the top pain, get only 2 videos a month

**Where:** STRATEGY §3 (Answer a fan, "2 a month"); PLAYBOOK rule 3.

**Evidence**
- 04 ranks **affordability as pain #1**. Lightstick setup is #5.
- The shop's biggest sales hits were installment hooks: "Pwede hulugan" got 89K views and 1,006 comments.
- Installment posts get 8× the comments per view (0.8% vs 0.1%, 01 §2.5).
- 02 Card E ("₱300 DP lang …", a test) and 04's "Ipon plan: kaya mo 'to by [concert date]" and "Ticket muna, lightstick later" were all dropped without a reason.

**Fix**
- Add a monthly "ipon plan" video tied to the next concert: a real DOP calendar on paper.
- Run Card E as an A/B test against the "no price in 3 s" rule instead of banning it.
- Keep the "DP + total on one line" format, but drop "never".

### S5 · The workload isn't realistic for a 1 to 2 person shop

**Where:** STRATEGY §3 ("4 videos a week"); AUTOMATION §1 ("about 2.5 to 3 hours for 4 videos").

**What's wrong**
- The 2.5 to 3 h counts only approval, filming, editing and publishing (10 + 60–90 + 60 + 15 min). It leaves out several jobs the plan itself creates:
  - "Reply to every one" of the keyword comments (Card C)
  - The weekly order-path test (§5)
  - Counting stock for the weekly wall
  - Writing pinned comments and tagging TikTok Shop items
  - Cross-posting with captions rewritten for each platform (05)
  - Going to cinema or concert events
- Card C must go up "the same day the sale details are published", so it can't be batched.
- Clinic needs a different model, or a different problem, every time: 16+ videos in 12 weeks.
- The person posting may be outside PH (the Netherlands flag). The stock is in Cubao (07).

**Fix**
- Make **3 a week** the target and 4 the stretch goal.
- List every recurring task with an owner and the minutes it takes.
- Make demo units and "who films where" a precondition (owner question 1 plus the new demo-unit question).

### S6 · Targets aren't calibrated

| Target | Problem | Evidence | Fix |
|---|---|---|---|
| Clinic saves median ≥ 0.5% | It sits **above the shop's own best-format median** | Lightstick tutorials: median 0.35% saves (01 §2.3) | Set ≥ 0.35%, stretch 0.5% |
| ≥ 1 video above 10K per month | The last 12 months had 4 posts ≥ 10K. Two look paid (tote, Enchin), one is reused footage of unknown ownership. **One clean one** (11.9K, inside a SEVENTEEN tour window). | CSV | "3 breakouts in 12 weeks" can stay as a stretch goal. Add a realistic floor, such as "Clinic median ≥ 2× account median". |
| Zero-comment posts < 25% | Down from 53% without reasoning. Recent posts get a median of 1 comment (07). | | Under 40% at 12 weeks |
| No sales target | The consultant's goal is sales. "Where did you see us?" only catches **form** orders. DM orders on X and TikTok skip it. | 07 §2 | Ask about the source in DMs too (a saved reply). Set an order baseline in week 1. |
| "Average views stay flat by design" | Unclear wording | | "We expect the typical video to stay around 600 views; growth comes from breakouts and search." |

### S7 · X is where the shop actually sells, and the plan barely covers it

**Where:** STRATEGY §1 ("The order desk is X, the form and DMs"); AUTOMATION §1 ("GO details to X").

**What's missing**
- An X content routine
- An X metric
- Who writes the daily WTS/LFB posts
- How Clinic videos get reused on X
- The research gap: 04 couldn't read X, and 07 scraped only 10 posts (691 to 1,873 views each, 0 to 8 likes)

**Fix**
- Add a short X section: post types, how often, the pinned "how to order / check my order" post, and which Clinic clips get reposted.
- Put X views per post and orders from X into §8.
- Add a weekly X scrape. 07 prices it at about $0.01.

### S8 · Facebook is under-planned, and the plan contradicts the research on whether the shop even uses it

**Where:** STRATEGY §11: "Cross-post clean files … **if the shop has or makes a page**"; OWNER-Q #10.

**Evidence**
- 02 §7 L6: slide 1 is "a screenshot of **the shop's own Facebook post**", with a "13m" timestamp. 02 §10.5 says the WTS caption is a Facebook post. So the shop already posts on Facebook.
- 07 §1 says only that no FB page is linked from the TikTok or X bios.
- Facebook has the widest reach in PH (95.8M) and is where parents and gift-buyers are (04 Persona C). 05 recommends Messenger as the place to confirm GO orders.

**Fix**
- Change OWNER-Q #10 to "We saw a Facebook post of yours in a July TikTok. Which FB page or group is it, and does it get orders?"
- Add Facebook Reels plus the "gift guide for parents" video as a Facebook-first item.

### S9 · LIVE is dropped in one line, with no reason

**Where:** STRATEGY §11: "LIVE selling | Not now. Test later for 4 to 6 weeks, through TikTok Shop only"

**What's wrong**
- 05 Do #8 recommends a test, and 03 shows 6 of 13 PH and SEA sellers sell on LIVE.
- The plan gives no reason. Possible reasons:
  - Capacity
  - A TikTok Shop checkout can't handle DP and due-date tiers, and 05 couldn't verify pre-order rules
  - The 18+ host rule
- A **non-selling "Lightstick Clinic LIVE"** (Q&A, troubleshooting) in the 2 weeks before BTS Bulacan fits the help-desk strategy. It wouldn't break the off-platform rule if it doesn't push sales.

**Fix:** State the reason. Plan one or two Q&A LIVEs in late Feb to early Mar 2027 as the test.

### S10 · The scoring formula: false precision, weights that clash with the evidence, a window that hides BTS

**Where:** AUTOMATION §2.

| Issue | Evidence | Fix |
|---|---|---|
| The demand window is 21 days. BTS Bulacan (Mar 13) gets no event points until about Feb 20, but the calendar wants BTS content now and weekly from January. | AUTOMATION §2 vs STRATEGY §6 | Count events within 21 days **or** a tracked "season" (BTS Oct to Mar) |
| "big fandom event (BTS, ENHYPEN) 3" | BTS is the weakest fandom on the account (5% doubled). ENHYPEN has no PH event this window. | Weight by the *event* (concert or launch in PH), not by fandom |
| "+1 per 5 matching questions" | Comments are scraped on the last 10 videos only. Recent posts get a median of 1 comment, so this term will almost always be 0. | Feed in DM and X questions (the owner's tally) or drop the term |
| format_strength: "Real fan moment 3", the same as Clinic | n = 1 recording, ownership unknown. Concert content median 0.60×. | Give it 1 |
| "News + keyword 2" | Rests on the possibly paid post (M5) | Give it 1.5 until owner Q4 is answered |
| freshness 0.3 if a similar video was posted in the last 30 days | Every weekly stock wall and every "Clinic #n" in a series gets marked down. The slop gate uses **14** days. | Apply it to the same *offer* only, not the format. Use one window. |
| No "can we sell it" factor | A Clinic on a model the shop can't sell scores the same as one it can | Add "sellable now (on hand or open GO)" as a filter |
| "Learn: format scores updated" | No rule. With about 4 posts a week, one breakout will swing the scores. | No automatic weight changes. Review monthly by hand with Studio data. |
| Over-engineered for picking 4 to 6 ideas | Multiplying made-up weights looks exact and isn't | Use 3 hard filters (has a source, can film, not a repeat offer), then a short ranked list a human picks from |
| "Decide … doesn't need the owner" | `can_film` needs the owner's live stock list. The ideas file is already "blocked until the owner answers". | Say Phase A needs a weekly stock list from the owner (2 min) |

### S11 · Slop-gate gaps

- **The number check will block correct posts.** Converted times (KST to PHT), computed totals and countdowns won't appear in the source or the sheet. Allow "derived from [field]".
- **It can't catch the riskiest errors.** Those are factual claims without numbers: "only VER.4 syncs", app names, "the cinema controls the lightstick". Require every factual sentence in a brief to quote the source line it rests on. A human ticks it.
- **"Check the source the day you post" clashes with scheduling.** PLAYBOOK rule 9 and the ideas file say to check on posting day, but AUTOMATION schedules up to 10 days ahead, and 07 §4.1 says a scheduled TikTok **can't be edited**. Rule: anything with a date or version claim gets scheduled no more than 48 h ahead, or re-checked the morning it posts.
- STRATEGY §7 lists 5 gate rules and AUTOMATION §3 lists 6 (the "repeat offer" rule is missing from STRATEGY).

### S12 · Missing safeguards in the automation design

| Gap | Why it matters | Fix |
|---|---|---|
| The lookup page has no rate limit, and order codes can be guessed | 07's example code "UM-ARMY-0143" counts up in order. Last 4 phone digits = 10,000 combinations. 07 asked for a rate limit and "first name initial only". The plan dropped both. | Random codes, a rate limit with lockout, initials only |
| AUTOMATION: "No names or amounts shown publicly", yet the page shows "paid, balance" | Contradiction | "Shown only after code + last 4 digits; never in a public list" |
| No privacy notice on the order form; payment screenshots go to an AI API (Phase C); names and amounts go to Telegram | The Data Privacy Act (RA 10173) applies to the shop | Add a short privacy notice and consent line to the form. Crop screenshots to amount and reference only. Set a retention period. Say who can open the sheet. |
| No alert when a scraper or feed fails | An empty Monday brief looks like "nothing happened" | A "source health" line in every brief, with an alert if an input returns 0 items |
| "Apify fits inside the free monthly credit" | The research ran on 4 different free tokens (#4 to #7) belonging to Andrey. A client job running on several personal free accounts is fragile, and it may break Apify's free-plan terms (check). | Budget a paid or client-owned Apify account (about $4/month) |
| Scraping TikTok is against TikTok's ToS (07 §3 row 12) | The client should know | One line in AUTOMATION: public data only, no shop login, small volumes |
| Single server, no handover | Everything runs "on Andrey's server as timers". 07 lists it as a single point of failure. | Say what the shop keeps if the pilot ends (the sheet, the lookup page as an Apps Script backup) |

### S13 · The "never automate" list is incomplete

AUTOMATION §5 leaves out items that 07 §5 and §7 list:
- Fake reviews or testimonials; bought followers or likes
- AI voices, avatars and AI product photos (these sit in the slop gate but not here)
- Automatic **public** replies to comments
- Payment reminders sent without the owner's tap
- Opening a GO or setting its price
- Refunds, cancellations and complaints
- Publishing any lightstick, app or sync claim without a human check against the official notice
- Using customers' photos, names or comments in content without consent

Also: "Anything a customer reads that the owner hasn't approved" conflicts with Phase C's "DM bot test". Say the bot answers FAQ and status only, then hands over to a human.

### S14 · The Netherlands flag: the wording is stronger than the evidence

**Where:** STRATEGY §4.8: "TikTok first shows a new video to people in the region it was posted from"; OWNER-Q #1; §10.

**Evidence**
- 05 §1.1: "region posted from" is one input. TikTok calls same-country a "**weak**" signal (Newsroom 2020).
- 02 §3: the 4 NL posts got 416 to 1,156 views, in line with the PH posts just before (430 to 446). "NL isn't proven to be the cause."
- There are innocent explanations: the owner travelling or living abroad, a helper abroad, a VPN.

**Fix**
- Write: "TikTok uses the posting region as one of many inputs. The 4 NL posts didn't do worse. Still, post from a PH phone when you can, and we'll test it."
- Ask neutrally: "Who handles posting now, and from which country or phone?"
- Tell the owner this comes from public video metadata, so it doesn't read as surveillance.

### S15 · Privacy in the "Answer a fan" ideas

**Where:** Ideas #7 replies to "natatakot ako baka hindi ko mafullypaid sa dop 😭" (a **2022** comment on video 7147618684377304346).

**What's wrong:** TikTok's reply-with-video puts the commenter's **handle and avatar** on screen. This would publicly spotlight a 4-year-old comment about money fear from someone who may be a minor.

**Fix**
- Use a recent comment and ask the commenter first.
- Or re-type the question as on-screen text with no handle: "Tanong ng isang buyer: …"
- Same rule for idea #8.

### S16 · Heeseung footage: the plan stops reuse but not the post that's already up

- 01 §0: the 226K Fate Tour clip is **pinned**. If the call isn't the owner's, the pinned post is the problem, not just future reuse. Add: "If it isn't yours, unpin it and decide whether to keep it up."
- PLAYBOOK Bonus cites the 226K video as evidence for "only your own footage", which implies it was the owner's. Reword it.

### S17 · Taglish drafts: some lines read translated, and none follow the plan's own "po" rule

The audience report (04 §7.2) lists as cringe: "corporate English or AI-sounding copy with no *po*, no specifics, no feeling". I'm not a native speaker, so the owner should rewrite all of these. These are the ones to flag:

| Where | Line | Problem | Suggestion (owner to confirm) |
|---|---|---|---|
| Ideas #7 title | "Takot ka bang hindi mabayaran ang DOP?" | DOP is the payment *deadline*; you don't "pay the DOP". Fans wrote "mafullypaid **sa** dop". "Takot ka bang…" also opens like an ad. | "Paano kung hindi ka umabot sa DOP? Ito po mangyayari." |
| Ideas #1 caption | "Official notice: only VER.4 syncs with the show. Panoorin muna bago bumili." | It reads like a slogan, and with "bumili" it nudges a purchase in what's meant to be an honest explainer. The shop sells VER.4, so this video needs to avoid a fear-selling tone. | Lead with the notice: "May VER.3 ka? Ito po sabi ng official notice para sa Bulacan." Mention that the old one still lights up. |
| Ideas #4 caption | "Kailangan mo bang mag-upgrade? Honest answer." | "Honest answer." is English marketing filler | "Spoiler: gumagana pa rin po yung VER.2 mo." |
| Ideas #8 | "Ano ang tamang app ng ENHYPEN lightstick?" | Stiff, textbook Tagalog | "Anong app ba talaga ng Engenebong?" |
| PLAYBOOK Card C, Ideas #5 | "[Fandom], stop ka muna dyan! [Item] is finally here!" | It's the shop's own M1 line. Used every week it becomes a template. "Is finally here" is misleading for a **pre-order** that arrives in weeks. | Vary the opener. For pre-orders: "…open na ang pre-order!" |
| All caption drafts | No "po" anywhere | STRATEGY §3 says "Fans write Taglish with 'po'. The captions should too." The drafts ignore it. | Either add "po" where natural or relax the rule |
| PLAYBOOK B2 vs Ideas #9 | "Ep. 2 next week." vs "Ep. 2 next box." | "Next week" promises a schedule that shipments can't keep | Use "next box" |

### S18 · Plain language: a normal reader hits jargon with no explanation

Andrey asked for plans "a normal person can understand". Terms used without a definition:

| Doc | Terms |
|---|---|
| STRATEGY | GO / GOs (§6, §7), DP (§4), SG (§6), WTS/LFB (§1, §3), median (§1, §8), "Phase A/B/C"; "pain #5 (04)" and "fears #1, #4, #8 (04)" point to research numbering a reader can't decode |
| PLAYBOOK | DP, "ISF and PF", ETA, Commercial Music Library, "content disclosure" |
| AUTOMATION | Apify, RSS, "timers", "source ID", **"plug-in editor"** (never explained anywhere), Creator Search Insights / "Content gap", verified business account, PayMongo / QR Ph, DTI |
| Ideas, OWNER-Q | GOM, DOP, "ISF and PF" |

**Fix**
- Add a 12-line glossary at the top of STRATEGY.
- Name pains in words, not research numbers.
- In **fan-facing** captions, swap "includes ISF and PF" for "kasama na shipping at packing". New fans who arrive through search won't know GO jargon (02 §10.5; 03 §6 "explaining the GO process for new fans").

### S19 · AI-slop phrasing in our own docs

| Where | Phrase | Problem |
|---|---|---|
| STRATEGY §1 | "The proof of what works is strong and comes from three directions at once" | An overclaim built on a rhetorical triad (see M1) |
| STRATEGY §1 | "The next five months are the best season the shop will get." | Hype with nothing behind it |
| STRATEGY §8 | "We can't win the lottery without tickets" | Cliché |
| STRATEGY §9 | "Research and idea time goes to near zero" | Vague and unmeasured |
| Ideas #4 | "An honest 'you don't have to upgrade' builds more trust than a hard sell (04)" | 04 doesn't say this. It's misattributed. |

### S20 · Owner questions that are missing

- **Account type** (Business, Creator or personal). 05 shows `commerceUser=false, ttSeller=true`. The answer decides the music library, the scheduler (Creator or Business only) and auto-replies (07 Q7). It also settles a contradiction: AUTOMATION says "videos with trending sounds go up by hand", while PLAYBOOK rule 8 says business accounts can't use the general library for commercial posts.
- **Orders after the hits**: the 2025-01-25 tutorial, the 2026-05-12 Enchin post (01 §9.2 Q4).
- **Demo units** the shop owns, and whether it will buy some (M1).
- Whether any recent post shows as "not eligible for recommendation" in Studio (05 §8 Q4).

---

## NICE TO HAVE

1. **Scheduling, 10 vs 30 days.** The plan (AUTOMATION, 10 days) agrees with 07 and current guides (HopperHQ: "up to 10 days in advance"). The "30 days" sits in **research 05 §6 Do #6**, with no source. Correct 05, not the plan. Also add "can't edit after scheduling" (see S11).
2. **Heeseung's exit is confirmed** by several outlets (GMA, Manila Bulletin, Bandwagon). 06 cites one. Add a second link, since the plan repeats the fact 4 times.
3. Ideas: "the shop doesn't usually run SM GOs". The shop has 10 EXO and 4 NCT videos and has sold the EXO lightstick VER.3 (06 §2). Reword it: "hasn't run SM GOs since 2023".
4. STRATEGY §1 states "then Season's Greetings 2027 pre-orders" as fact. 06 says HYBE SG is **expected**, not announced. §6 already says "expected". Match it.
5. "Facebook reaches more Filipinos than TikTok". The TikTok ad-reach count excludes under-18s, a large share of K-pop fans (05 §4b). Add the caveat.
6. Research ideas not used, all cheap and evidence-backed:
   - A "rating every lightstick we've sold" video (03: 1.5M, 7.6× format median)
   - A "what DP, PAYO, DOP mean" explainer for new fans (03 §6)
   - Cubao pickup and same-day delivery before concerts as a selling point (04 §6, 07 §1)
   - Freebies at the venue (04 §4.4)
   - "Real vs fake lightstick" (04 §9, 05 Do #1)
   - Spike mode for viral posts (07 Phase 2 #4)
7. The 60-day checkpoint says to "keep the formats that beat average". Define it (median vs the account's 21-neighbour baseline, at least 4 videos per format) so one breakout doesn't decide.
8. peer_watch pulls the "newest 10" videos each week, so many will be under 3 days old with views still climbing. `score_competitors.py` already excludes those. Keep that rule.
9. Creator Search Insights is "available in select regions; check in app for PH" (05 §2.2). The monthly owner screenshot step should say "if available".
10. A Clinic with a selling pinned comment is arguably a "post that sells". Say whether "Your brand" goes on Clinic videos too.
11. PLAYBOOK rule 4 (text not bottom-right) is sound UI advice, but H2, the 225K hit, had its step list bottom-right (02 §7). Don't cite the hits as evidence for it.
12. "They also have a TikTok Shop, Shopee and Lazada" is stated as fact. 07 marks the Shopee and Lazada status as unverified (the Shopee link went to the homepage).
13. The §8 baseline mixes time windows: 608 is the 2026 median, 0.09% and 53% are last-12-month figures, 7 is the last 90 days. Label each.
14. Ideas file header: "Taglish lines are placeholders". Good. Put the same warning on the PLAYBOOK caption template.

---

## Contradictions index (where each is handled)

| # | Contradiction | Finding |
|---|---|---|
| 1 | Phase A cost $2–5 (STRATEGY) vs $5–9 (AUTOMATION) | M3 |
| 2 | Phase B savings 3.5–5 h, which includes the news digest, now in Phase A | M3 |
| 3 | "all 12" vs 14 owner questions | S1 |
| 4 | Scheduling 10 days (plan, 07) vs 30 days (05) | N1 |
| 5 | "Check the source the day you post" vs scheduling 10 days ahead with no edits | S11 |
| 6 | Freshness window 30 days vs slop gate 14 days; 5 vs 6 gate rules | S10, S11 |
| 7 | "Phase A doesn't need the owner" vs `can_film` needing the owner's stock list | S10 |
| 8 | Lookup page "no amounts shown" vs it shows paid and balance | S12 |
| 9 | Facebook "if the shop has a page" vs 02 showing the shop's own FB post | S8 |
| 10 | Captions "with po" vs no "po" in any draft | S17 |
| 11 | "Only own footage … 226K was this kind of video" vs "don't reuse until confirmed" | S3, S16 |
| 12 | "Never DP alone / no price in 3 s" vs 02 Card E "lead with ₱300 DP" | S4 |
| 13 | Taglish voice "keeps it local" vs 02 Card A "English, so international owners land on it" | M1 |
| 14 | "Trending sounds by hand" vs "business accounts can't use the general library" | S20 |
| 15 | "Build first: Phase A" vs 07 "Phase 1 order desk first: biggest time saved" (no reason given for flipping 07's order) | M3 (state the reason) |
| 16 | "Never anything a customer reads without OK" vs Phase C DM bot | S13 |
| 17 | "Ep. 2 next week" vs "Ep. 2 next box" | S17 |

---

## Web checks used in this review

- ENHYPEN Walk the Line in Bulacan, Mar 1, 2025: [ABS-CBN](https://abs-cbn.com/entertainment/showbiz/events/2025/3/2/enhypen-heats-up-ph-stadium-with-walk-the-line-concert-1619), [GMA](https://gmanetwork.com/news/lifestyle/hobbiesandactivities/927430/enhypen-to-bring-walk-the-line-tour-in-bulacan-in-march-2025/story)
- Heeseung leaves ENHYPEN, Mar 10, 2026: [GMA](https://www.gmanetwork.com/news/showbiz/showbizabroad/979432/heeseung-to-leave-enhypen/story/), [Manila Bulletin](https://mb.com.ph/2026/03/10/k-pop-idol-heeseung-leaving-enhypen-group-to-continue-with-six-members), [Bandwagon](https://www.bandwagon.asia/articles/enhypen-s-heeseung-parts-ways-with-group-prepares-for-solo-album)
- TikTok Studio scheduling limit (up to 10 days): [Hopper HQ](https://www.hopperhq.com/blog/how-to-schedule-tiktok-posts-desktop-mobile/)
