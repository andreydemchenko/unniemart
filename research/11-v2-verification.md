# 11 · Verification of plan v2

Date: 2026-10-14. Scope: `strategy/STRATEGY.md`, `PLAYBOOK.md`, `AUTOMATION.md`, `OWNER-QUESTIONS.md`,
`content/ideas/2026-10-W42-W44.md` (all v2), checked against 08, 09, 10, research 01–07 and the three CSVs
(re-computed with pandas). No other file edited.

**Result:** 25 of 26 review items are FIXED (S7 with a minor gap), and 1 is PARTLY fixed (S18). Of the 10 changes the
fact-check (08) asked for, 8 are FIXED and 2 are PARTLY fixed. v2 also introduces **2 new must-fix errors**, both
in the main bet (N1 and N2).

---

## 1. Status of review items (09)

| ID | Status | Evidence from v2 |
|---|---|---|
| M1 | FIXED | STRATEGY §2: "8 lightstick tutorials, median 21,000 views… Of the last 4, 2 hit and 2 flopped". There is a kill rule, OWNER-Q 1 covers demo units and Q3 covers orders after the hits, and SEVENTEEN is now "keep it light". *The timing claim this review introduced has since been overstated: see N1.* |
| M2 | FIXED | §1: "Two things happened at once, and the data can't say which is bigger" |
| M3 | FIXED | The §10 table now splits Andrey's hours, owner's hours, cost and time saved, and says "estimates… assume 2 to 4 open GOs, about 50 active orders and 40 to 80 DMs". The Phase A, B and C sums match AUTOMATION. Small leftovers are in N3 and N14. |
| M4 | FIXED | WeverseShopAutomation is gone. AUTOMATION §3: "This needs a **new** checker… Budget about 2 hours." |
| M5 | FIXED | §4: "That post may have been paid (owner question 4) \| Test". PLAYBOOK D: "the comment gap is the stronger signal" |
| M6 | FIXED | "None of the 10… doubled normal; median 0.8×". "We found no Philippine seller making them (03)". The Army Bomb comment claim and the "0 of 12" claim are removed. |
| S1 | FIXED | "4 of the 6 hits open on the real item". "1,186 → 629 → 598 → 430 → 446". "top 6 of the 17". "in our sample of 1,057". One leftover: N11. |
| S2 | FIXED | "first 2 to 4 seconds". End card: "A guess until we see retention data". "come up on 10 of 29 videos we sampled" |
| S3 | FIXED | "A 2023 installment reply got 42,500 (in a SEVENTEEN window); a 2025 one got 1,342". PLAYBOOK B2: "2021… (CO, n=1). Treat it as a test." |
| S4 | FIXED | Season playbook "6 to 4 weeks: **Ipon plan**", "Ticket muna", Card C A/B test. The word "never" is gone. |
| S5 | FIXED | "Target: 3 videos a week, 4 as a stretch". The AUTOMATION §1 task table lists who does what, and the total is "about 3 to 4 hours a week". |
| S6 | FIXED | Saves "0.35%… (stretch: 0.5%)". Zero-comment posts "Under 40%". Clinic "at least 2× the account's normal". "Orders per week… set it in week 1" |
| S7 | FIXED (minor gap) | §6 X row: pinned post, Clinic reposts, "Track views per post and orders from X weekly", plus the weekly X scrape. X views per post are not in the §11 targets table, and it doesn't say who writes the daily WTS post. |
| S8 | FIXED | "The shop already posts on Facebook (a July TikTok showed a screenshot…)". The gift guide is Facebook-first. OWNER-Q 11 is reworded. |
| S9 | FIXED | A reason is given (owner's time, TikTok Shop checkout vs installments), plus a "non-selling 'Lightstick Clinic LIVE'… late Feb to early Mar 2027" test |
| S10 | FIXED | "No weighted formula. Three hard filters". "BTS counts from now to Mar 16". There is a sellable filter. "Nothing changes automatically" |
| S11 | FIXED | Derived numbers "pass if they name what they came from". Facts get a source quote and a human tick. "at most 48 hours ahead". "same 6 rules" |
| S12 | FIXED | Random codes, lockout, initials only. Privacy notice. Source-health line. One dedicated Apify account. Scraping note. Handover. (No retention period set: "only as long as needed".) |
| S13 | FIXED | The AUTOMATION §5 list is complete. The DM bot "answers FAQ and order status only, then hands over to a person". |
| S14 | FIXED | "TikTok treats the posting region as one input among many, and those 4 didn't do worse". Asked neutrally in Q5. |
| S15 | FIXED | "re-type the question on screen… Don't use reply-with-video on the old comment" |
| S16 | FIXED | "The clip is pinned. If the call isn't the owner's own, unpin it". The PLAYBOOK Bonus no longer cites the 226K video. |
| S17 | FIXED | "Paano kung hindi ka umabot sa DOP? Ito po mangyayari". "Spoiler: gumagana pa rin po yung VER.2 mo." "Ep. 2 next box." "For a pre-order, don't say 'it's here'" |
| S18 | **PARTLY** | A glossary is added (GO, GOM, DP, DOP, PAYO, WTS/LFB, SG, median, normal), and ISF/PF became "kasama na shipping at packing". Terms still unexplained are listed in §4. |
| S19 | FIXED | "three directions", "best season", "lottery" and "near zero" are gone. A new one-liner overclaims: see N1. |
| S20 | FIXED | Q10 account type. Q3 orders after the hits. Q1 demo units. Q2 "not eligible for recommendation" |

## 2. Status of the fact-check's "plan must change" items (08)

| # | Status | Evidence from v2 |
|---|---|---|
| 1 Scheduler 10 days | FIXED | AUTOMATION: "15 minutes to 10 days ahead, no edits after scheduling". research/05 is corrected too. |
| 2 ENHYPEN November | FIXED | "Comeback targeted for November (date and format not set, so no album GO until announced)" |
| 3 Search wording | FIXED | "matches… captions, on-screen text, subtitles and hashtags… Engagement counts too". No "voiceover" claim. |
| 4 Army Bomb explainer | FIXED | Ideas #1: "the notice does **not** say old Army Bombs still light up… we **show** it on camera… as our demo" |
| 5 EVAN | FIXED | "EVAN's (formerly Heeseung's) birthday". "now performs solo as EVAN" |
| 6 Commercial music | FIXED | "businesses use the Commercial Music Library for all their posts, not just ads". One conflict remains: N8. |
| 7 GCash for Business | **PARTLY** | Q8 asks about "DTI **and** BIR (Form 2303)", but the "GCash account verified 12+ months" requirement is missing from Q8 and from AUTOMATION Phase C ("Needs DTI + BIR registration"). |
| 8 FB vs TikTok | FIXED | "Facebook reaches 95.6M adult Filipinos and TikTok 64.0M (ad reach, 08)" |
| 9 13th month | FIXED | "13th-month pay for working fans and parents (due by Dec 24)", with the "gift for your fan" guide for parents |
| 10 Daily ENHYPEN recheck | **PARTLY** | Ideas #5: "the news watcher will flag them". The watcher isn't built yet (19 to 27 h of work). Nobody is assigned a manual daily Weverse check for the rest of October, but idea #6 must post "the same day the sale details are published". |

---

## 3. New issues in v2, ranked

### MUST FIX

**N1 · The headline "timing" finding gets both counterexamples wrong.**
- **Where:** STRATEGY §1: "The same tutorial format got 225,000 views… and 571 views with no concert coming". The section calls this "the most important finding" and adds "Format matters, but timing decides whether it pays". PLAYBOOK Card A says the same. STRATEGY §4 marks Clinic and Proof "Proven, when timed".
- **What the data shows:**
  - The 571 video (2026-05-01, 41 s) isn't the same format. It says the "user guide is finally OUT on YouTube!! watch it".
  - The 913 video (2025-06-28) runs 82 s and opens with a long spoken intro.
  - 01 §9.1 (fact 3) blames both flops on breaking the 38–44 s step format.
  - The 913 flop also sat in what 01 §2.5 calls the "BLACKPINK tour window, Jun–Jul 2025". BLACKPINK sales posts that day and the next got 3,626 (2.7×) and 8,129 (6.6×).
- **Fix:** "Both recent hits came just before a PH concert. Both flops had no concert close by **and** broke the format. We can't separate the two, so we do both." Drop "timing decides". Downgrade "Proven" to "Strong when timed and done in the short step format".

**N2 · "No BTS concert-window content was ever tried" is false** (STRATEGY §2, seasons table).
- **What the data shows:** In Jan to Jul 2026 the shop posted 8 BTS ARIRANG posts with a concert angle: tour news, 2 "ticketing tips" posts, and pre-orders. They got 375 to 807 views (0.6 to 1.25× normal). 01 §3 counts 14 BTS posts in the last 12 months. The owner made these posts.
- **Fix:** "BTS tour news, ticketing tips and pre-orders in 2026 did about normal. No BTS lightstick tutorial has been tried yet." The "Ticket day" row then has weak support for BTS. Say so.

### SHOULD FIX

**N3 · Phase A vs Phase B savings contradict each other.**
- §10 says "Phase B saves more of the owner's hours", but the same table shows Phase A at ~2.5 h and Phase B at 1.5 to 2.7 h.
- Phase A's "captions ~0.8 h" is 07's figure for about 10 WTS captions a week filled from the order sheet. That sheet only arrives in Phase B, yet §9 says captions take prices "from the order sheet".
- At 3 videos a week, Phase A realistically saves about 1.8 to 2 h.
- **Fix:** state the real Phase A saving and the sheet dependency.

**N4 · The owner-question numbers in STRATEGY §12 don't match OWNER-QUESTIONS.md.**
- §12 #3 is Q5, #5 is Q6 and #6 is Q7. §12 #2 merges Q2 and Q3.
- The other files cite the real numbers: "owner question 6" is Heeseung (that's §12 #5), and "owner questions 7 to 9" don't exist in §12's list of 6.
- "Top 6" also isn't the file's top 6.
- **Fix:** tag each §12 item with its Q number (Q1, Q2+Q3, Q5, Q4, Q6, Q7).

**N5 · "Demand for this right now is real" drops 10's caveat.**
- 10 says "Small sample, not geo-locked; treat as directional". STRATEGY leaves this out.
- Also: "Army Bomb version 4 videos from small accounts (95 to 3,400 followers) get 80,000 to 1.4 million views". The 95-follower post is a question post at 76.9K views, not a VER.4 video, and the largest results are Spanish or Indonesian.
- **Fix:** add "top search results, mostly outside PH".

**N6 · The kill rule no longer bites.** Clinic is already "1 to 2 a week", and §11 targets at least 12 Clinic videos in 12 weeks (1 a week). "Cut Clinic to 1 a week" therefore changes nothing. Use "1 every 2 weeks" or "pause until the next season".

**N7 · The Proof status contradicts PLAYBOOK.**
- STRATEGY §4 marks Proof (stock wall + "box from Korea") "Proven, when timed", and the AUTOMATION ranking treats it as proven too. That rests on n=2 stock walls.
- PLAYBOOK B2 calls the box series "a test" (n=1).

**N8 · The music rule conflicts with the Bonus card.** PLAYBOOK Bonus says "Use short performance cuts only, never full songs". The CML rule says every shop post must use the Commercial Music Library, and performance clips carry the song. **Fix:** say "mute or duck the performance audio".

**N9 · The first-frame rule clashes with Cards D and E.**
- PLAYBOOK rule 1 says "First frame = the real thing… Not a face on a plain wall… or a screenshot".
- Card D (and idea #6) opens on "the official announcement visual… then you". Card E says "Face on camera is fine".
- **Fix:** name the exceptions.

### LOW

- **N10:** "'Babalikan ko ito…' appears 63 times". 63 is the size of the ticket-first group. The phrase itself (babalikan/balikan) appears in only 19 comments, and 2 of the 63 are on a 2022 video. Write "63 comments say they'll buy after a ticket".
- **N11:** "The most-liked question on the account (283 likes)" (§1, ideas #8). It's the most-liked in the 1,057-comment sample, not on the whole account.
- **N12:** "8 times more comments per view than other sales posts". 01 compares installment posts with on-hand and sale posts only. Drop-schedule and slots-left posts are higher.
- **N13:** "sales posts that only reach existing followers". There is no traffic-source data behind this. Soften it.
- **N14:** Phase C line items add up to $30–46 and 2.6–4.5 h a week. The table says "$30 to 45" and "3 to 4 h".
- **N15:** The ideas file has 10 ideas plus a weekly stock wall for Oct 14 to Nov 1 (~2.7 weeks). That's 4+ a week, above the 3-a-week target. Mark which 3 a week are the core.
- **N16:** The AUTOMATION glossary defines "Plug-in editor" but never uses it. It also points to an internal project. Delete it.
- **N17:** "a few weeks before a Philippine concert". The Caratbong hit came 4 days before.

---

## 4. Readability (non-expert)

The core GO jargon is now explained. These terms are still unexplained:

| File | Terms |
|---|---|
| STRATEGY | Army Bomb / Caratbong / Engenebong (each group's lightstick nickname; add to the glossary), Weverse, HYBE, "Your brand" disclosure, "peer outliers", "Search share", "A/B test" |
| PLAYBOOK | ETA, "Your brand" disclosure, Commercial Music Library (what it is, where to find it), "self mode" |
| AUTOMATION | Apps Script, Buffer, PayMongo / QR Ph, DTI / BIR, KST, "deduped", `score_competitors.py`, `automations/...` paths (fine for Andrey, opaque to the owner) |
| Ideas / OWNER-Q | "SM group orders" (SM Entertainment, easily confused with SM Mall and SM Tickets in the same files), ENGENE, "For You" |

---

## 5. Numbers spot-checked (STRATEGY unless noted)

Checked as correct against the CSVs or research:
- **Reach and posting:** 2,793 → 608 median views. 53% zero-comment posts and 0.09% saves (last 12 months). 46 of the last 74 posts are sales. 7 posts in 90 days vs peers' 26 to 50.
- **Hits table:** 225,400, 30,500, 30,000, 71,600 with 45 ticket-first comments, 913, 571.
- **Comments:** 889 of 1,015. 1,057 sampled and 1,291 likes. 22% (220) availability questions. 283 likes. 10 of 29 videos with trust questions. 23% (12 of 53) non-Filipino languages.
- **Tutorials and formats:** 8 tutorials, median 21,250. 0.35% saves. "Pwede hulugan" 89,200 / 1,006. 8× (0.8% vs 0.1%). Memes 0 of 10 doubled, median 0.81.
- **Fandoms and offers:** BTS 1 of 21. ENHYPEN 41%. BABYMONSTER sequence. 42,500 / 1,342.
- **Peers and search:** milky_kshop 5,939 followers, 16.8×. KATSEYE 453,600 (iamurgrace_). Slideshows lost in 7 of 11 accounts. Tagging 22–38% vs 2%.
- **Channels:** X 18,662 followers, 693–1,128 views per post. FB 95.6M vs TikTok 64.0M.
- **Other:** 1 clean breakout in 12 months. DP ₱300 (2025–26 captions). Calendar dates (06, 08).

Wrong or overstated: the 571 and 913 flops framed as "same format, no concert" (N1), "no BTS concert-window content" (N2),
"appears 63 times" (N10), and "80K to 1.4M from 95 to 3,400 followers" (N5).
