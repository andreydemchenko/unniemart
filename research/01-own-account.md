# 01 · Own account analysis: @unniemart_ (Unnie Mart 2)

Date: 2026-10-14 · Data pulled: 2026-10-14 (all 396 videos, 2022-09-05 to 2026-10-01) · Author: research agent

Files: `data/own-videos.csv` (396 rows), `data/comments.csv` (1,057 rows), raw scrapes in `data/raw/` (not committed).
Profile at scrape time: 5,909 followers, 135.1K likes, 396 videos, bio "Your KPOP One-Stop Shop / ENCHIN ORDER FORM", TikTok Shop seller.

---

## TL;DR

1. **Reach has collapsed, not just dipped.** Median views per post: 2,793 (2023) → 1,364 (2024) → 932 (2025) → 608 (2026). Last 6 months: median 578. Half of 2026 posts got zero comments (7% in 2022).
2. **Plain sales posts are 68% of everything posted and perform exactly at the account's own baseline.** In 2022-23 they still reached 20K-89K views; since 2024 they don't. The new "WTS | LFB" caption-wall GO template (11 posts since 2025-10-14) is no better: median 612 views vs 609 for other posts in the same period.
3. **Two formats produce almost all outsized results:**
   - **Lightstick "how to connect / how to use" tutorials.** Median 21K views across 8 videos (6.3× the surrounding posts). They also earn the most saves.
   - **An idol video-call clip.** One Weverse video call with ENHYPEN's Heeseung has been posted 3 times: 226K views (2023), 2.9K (2025) and 56K (2026). It is the #1 and #5 video.
   Together the top 2 videos hold 19% of all views ever and **51% of all saves**.
4. **The #1 hit ("Fate Tour Philippines na ba to?", 226K) is not concert footage.** It is a Weverse video-call screen recording where Heeseung says he wants to come to the Philippines "as soon as possible". I first inferred this from comments ("bakit nakakausap nila?", "how can they talk to him?"). `research/02-video-breakdown.md` then confirmed it by watching the video.
   - The 2026 "i got to meet heeseung" hit (56K) is **the same call footage reposted**.
   - The 2025-07-04 "Take me back on this time" post (2.9K) has matching transcript lines, so it is very likely the same call too.
   - **One recording, three posts:** 226K, 2.9K, 56K.
5. **Fans' #1 question is "available pa po?".** Out of 1,015 fan comments on 29 videos:
   - 22% ask about stock or slots
   - 9% ask how to order or how installment works
   - 6% ask the price
   The posts are not answering the questions buyers actually have.
6. **Two buying blockers are explicit in fans' own words:**
   - **Ticket first.** 63 comments say "babalikan ko pag naka-secure na ako ng ticket" ("I'll come back once I get a ticket"). The top one has 168 likes.
   - **Budget anxiety.** 96 comments. The most-liked comment in the dataset is "next year na lang please 😭" with 1,291 likes.
   Installment is the shop's real offer. The 2022 post "Pwede hulugan" ("you can pay in installments") got 89K views and 1,006 comments.
7. **Order-path friction is visible:** broken Google Form links ("action can't be completed"), items missing from the yellow basket, and "can't DM you". Buyers also ask for Shopee or Lazada, and for a way to order without Twitter/X.
8. **No reliable effect** from day of week, hour, video length, audio type, caption length, caption language or hashtag count. With this sample, the content itself is what matters.

Apify spend for this report: **$2.58** (details in section 11).

---

## 0. Data and method (read this before the numbers)

**What was collected**
- **All 396 videos.** This matches the profile count, so nothing is missing. Fields: views, likes, comments, shares, saves, duration, caption, hashtags, music, slideshow flag, pinned flag, TikTok Shop product tag.
- A second scrape sorted by "popular" (25 videos) found no video missing from the main pull.
- **TikTok auto-captions (speech-to-text) for 110 videos**, downloaded free from TikTok's servers. Used to understand what videos say.
- **1,057 top-level comments on 29 videos:** the top 15 by views, 2 more tutorials, and 12 typical sales or announcement posts. Of these, 42 are the shop's own comments and 1,015 are from fans. Replies under comments were not collected.

**What is NOT in the data** (only TikTok Studio has it):
- watch time, completion rate, follows gained per video, traffic source (For You / Search / profile)
- whether a post was promoted with paid ads
- sales per post

"Completion" below therefore means proxies only: likes, saves and shares per view.

**The relative-performance score.** Raw views mostly reflect *when* a video was posted, because 2022-23 posts got far more reach. So most tables also show **relative performance**: a video's views divided by the median of the 21 posts around it in time.
- 1.0 means normal for that period. 2.0 means double.
- This removes the era effect and lets formats, days and lengths be compared fairly.
- "% ≥2× local" means the share of videos that at least doubled their neighbours.

**How videos were labelled**
- Every video was labelled by hand-checked rules, using caption, hashtags, transcript and duration.
- I read every caption, and 200+ labels were set or corrected manually.
- Judgement calls:
  - FAQ and explainer videos about buying (installment explainer, "is it legit", courier tips) count as **tutorial/how-to**.
  - Sales posts that use a concert as the reason to buy stay **sales posts**, with a `concert_angle` flag.
  - **Concert content** means non-sales concert news, ticket tips or at-concert clips.
- Comment clusters were set the same way: rules first, then I read all 1,057 comments and fixed about 300 labels by hand.

**Data-quality notes**
- The scraper's "effect stickers" field is unreliable and was not used. Examples: a "Green Screen" effect appears on photo slideshows, and an "iPhone 17" effect on a January 2025 video.
- One post looks non-organic: the Walk The Line tote bag post (2026-06-15) has 24,800 views but 16 likes, 2 saves and 0 shares. That is a 0.06% like rate, about 30× below normal. **Possibly paid promotion. Ask the owner.** It is flagged in the CSV (`low_engagement_spike_flag`).
- 3 videos are pinned (#1, #2 and the Caratbong V3 tutorial). Pinning adds profile-visit views, but all three were already big.
- Views are lifetime totals at 2026-10-14, so older videos have had more time to collect them.

---

## 1. Performance overview

### 1.1 Distribution

| window | posts | median | p75 | p90 | max |
|---|---|---|---|---|---|
| all time | 396 | 1,461 | 2,800 | 12,300 | 226,300 |
| last 12 months | 74 | 614 | 1,136 | 2,030 | 55,900 |
| last 6 months | 45 | 578 | 849 | 1,684 | 55,900 |

- All-time mean is 5,888 views, pulled up by a few huge hits.
- The top 20 videos hold **53.5%** of all 2.33M views. The top 2 hold 19.4%.

### 1.2 By year

| year | posts | median | p75 | p90 | max | total views | posts ≥10K |
|---|---|---|---|---|---|---|---|
| 2022 (Sep-Dec) | 151 | 1,475 | 2,798 | 12,500 | 89,200 | 699,385 | 18 |
| 2023 | 81 | 2,793 | 12,000 | 33,500 | 226,300 | 1,034,162 | 23 |
| 2024 | 52 | 1,364 | 2,160 | 3,375 | 10,700 | 100,200 | 1 |
| 2025 | 54 | 932 | 2,012 | 7,498 | 225,400 | 366,912 | 5 |
| 2026 (to Oct 1) | 58 | 608 | 871 | 1,805 | 55,900 | 131,106 | 3 |

**Quarterly trend** (the monthly table is in the Appendix):

| quarter | posts | median | p90 | max |
|---|---|---|---|---|
| 2022Q3 | 51 | 942 | 22,200 | 89,200 |
| 2022Q4 | 100 | 1,701 | 8,753 | 43,300 |
| 2023Q1 | 39 | 3,294 | 30,700 | 45,200 |
| 2023Q2 | 9 | 4,869 | 7,470 | 10,600 |
| 2023Q3 | 23 | 2,219 | 26,940 | 226,300 |
| 2023Q4 | 10 | 10,546 | 54,500 | 71,600 |
| 2024Q1 | 25 | 1,385 | 3,098 | 10,700 |
| 2024Q2 | 7 | 1,393 | 4,341 | 8,260 |
| 2024Q3 | 8 | 1,625 | 2,727 | 2,969 |
| 2024Q4 | 12 | 1,237 | 3,327 | 5,617 |
| 2025Q1 | 10 | 1,337 | 49,990 | 225,400 |
| 2025Q2 | 4 | 3,352 | 6,778 | 8,129 |
| 2025Q3 | 23 | 589 | 2,685 | 10,300 |
| 2025Q4 | 17 | 818 | 3,204 | 11,900 |
| 2026Q1 | 13 | 672 | 1,825 | 2,011 |
| 2026Q2 | 36 | 587 | 1,835 | 55,900 |
| 2026Q3 | 8 | 522 | 974 | 1,156 |

**Engagement fell even faster than views.** Sales posts only (medians):

| year | likes/view | comments/view | saves/view | median comments per post (all posts) | % of posts with 0 comments |
|---|---|---|---|---|---|
| 2022 | 5.1% | 0.83% | 0.25% | 12 | 7% |
| 2023 | 1.6% | 0.20% | 0.15% | 11 | 15% |
| 2024 | 1.9% | 0.08% | 0.11% | 1 | 37% |
| 2025 | 1.5% | 0.00% | 0.14% | 1 | 46% |
| 2026 | 1.9% | 0.00% | 0.12% | 0.5 | 50% |

### 1.3 Outliers

- 54 videos reached ≥5× the account median (≥7,300 views). 43 of them are from 2022-23.
- The full top 20 is in the Appendix.

**Since 2024, only these posts beat their neighbours by ≥3×:**

| date | views | × neighbours | what it is |
|---|---|---|---|
| 2025-01-25 | 225,400 | 169× | Engenebong V2 "connecting to the app" tutorial |
| 2026-04-30 | 55,900 | 98× | Heeseung video-call clip |
| 2026-06-15 | 24,800 | 43× | Walk The Line tote arrival (**suspicious**: 16 likes, 0 shares) |
| 2025-11-14 | 11,900 | 23× | Caratbong "ready to scream, shine, support SEVENTEEN" (concert angle, Nov SVT tour) |
| 2025-01-14 | 30,500 | 23× | Caratbong V3 "connecting to app" tutorial |
| 2025-08-06 | 10,300 | 19× | "Binagsak na namin presyo" ("we dropped our prices"), BLACKPINK lightstick |
| 2026-05-12 | 10,300 | 18× | "Comment 'Enchin' or DM us to reserve" |
| 2025-01-27 | 23,800 | 18× | Engenebong V2 for sale or installment (2 days after the V2 tutorial) |
| 2024-01-24 | 10,700 | 8× | Official ENHYPEN lightstick onhand |
| 2025-06-29 | 8,129 | 7× | "check out na" BLACKPINK lightstick (BP tour window) |
| 2024-04-04 | 8,260 | 6× | Pre-order Fate+ Japan merch |

Notes on the list:
- The Binagsak (0.6%) and Enchin (0.9%) posts have like rates well below the ~2% norm. That fits paid promotion or a cold audience. **Ask the owner which posts were promoted.**
- The 2025-01-27 sales post (23.8K) came right after the tutorial blew up. That may be a spillover effect (inference).

---

## 2. Content type

### 2.1 All time

| type | videos | median views | median rel. perf | % ≥2× local | likes/view | saves/view | shares/view | comments/view |
|---|---|---|---|---|---|---|---|---|
| tutorial/how-to | 19 | 12,100 | **4.47** | **68%** | 1.9% | 0.3% | 0.1% | 0.2% |
| personal fan moment/reaction | 10 | 1,324 | 1.14 | 40% | 5.1% | 0.2% | 0.1% | 0.2% |
| order status/arrival update | 25 | 1,389 | 1.11 | 24% | 3.8% | 0.2% | 0.1% | 0.5% |
| price list/catalog/sales post | 271 | 1,495 | 1.01 | 23% | 2.8% | 0.2% | 0.1% | 0.3% |
| trend/meme/skit | 23 | 554 | 0.84 | 9% | 3.3% | 0.0% | 0.0% | 0.0% |
| other (feedback, giveaways, no caption, personal) | 27 | 1,556 | 0.82 | 4% | 3.1% | 0.1% | 0.0% | 0.1% |
| unboxing/haul | 12 | 1,152 | 0.66 | 17% | 2.6% | 0.2% | 0.0% | 0.2% |
| concert prep/concert content | 9 | 512 | 0.60 | 11% | 2.5% | 0.2% | 0.0% | 0.0% |

- Type matters statistically: Kruskal-Wallis p = 0.0002. Tutorials vs everything else: Mann-Whitney p = 0.00007.
- Follows per video are not available (see section 0).

### 2.2 Split by era (2022-23 vs 2024-26)

| era | type | videos | median views | median rel. perf | % ≥2× local |
|---|---|---|---|---|---|
| 2022-23 | tutorial/how-to | 14 | 12,300 | 5.01 | 79% |
| 2022-23 | price list/catalog/sales post | 160 | 2,136 | 1.02 | 24% |
| 2022-23 | order status/arrival update | 17 | 1,836 | 1.08 | 18% |
| 2022-23 | trend/meme/skit | 11 | 1,824 | 1.00 | 18% |
| 2022-23 | personal fan moment/reaction | 4 | 1,764 | 0.72 | 25% |
| 2022-23 | unboxing/haul | 6 | 616 | 0.39 | 0% |
| 2024-26 | personal fan moment/reaction | 6 | 1,232 | **1.77** | **50%** |
| 2024-26 | order status/arrival update | 8 | 1,387 | 1.14 | 38% |
| 2024-26 | unboxing/haul | 6 | 1,440 | 1.12 | 33% |
| 2024-26 | tutorial/how-to | 5 | 1,342 | 1.01 | 40% |
| 2024-26 | price list/catalog/sales post | 111 | 1,050 | 1.00 | 23% |
| 2024-26 | trend/meme/skit | 12 | 526 | 0.81 | **0%** |
| 2024-26 | concert prep/concert content | 7 | 512 | 0.63 | 14% |

Small samples everywhere except sales posts. Treat anything with fewer than 10 videos as a direction, not proof.

### 2.3 Tutorials split by kind

| kind | videos | median views | median rel. perf | saves/view |
|---|---|---|---|---|
| lightstick use / connect to app | 8 | 21,250 | 6.35 | 0.35% |
| buying process / FAQ / tips (installment explainer, legit check, why cheaper, courier, pooling) | 11 | 5,600 | 2.88 | 0.29% |

**The 2024-26 tutorials:**

| date | views | what | note |
|---|---|---|---|
| 2025-01-25 | 225,400 | Engenebong V2 to app | Short (38s), numbered steps. Transcript: "First, long press left button… Second, select self mode in the app…" |
| 2025-01-14 | 30,500 | Caratbong V3 to app | Same format, 43s. Transcript: "1. Turn on the lightstick 2. open the app and select Self Mode…" |
| 2025-02-03 | 1,342 | reply: how installment works (ENHYPEN) | |
| 2025-06-28 | 913 | BLACKPINK V2 connect | 82s, opens with talk about a previous video before the steps |
| 2026-05-01 | 571 | ENHYPEN V2 "user guide is OUT on YouTube" | Points viewers off TikTok and does not show the steps |

**Fact:** both tutorials that worked are short, step-by-step, and name one exact model ("Caratbong V3", "engenebong V2") plus "to the app". The two that flopped did not follow that pattern.

**Fact:** only 1 tutorial has been posted in 2026.

### 2.4 Idol video-call clips (a sub-type of "personal fan moment"): one call, posted three times

| date | views | × neighbours | saves | shares | likes/view | caption |
|---|---|---|---|---|---|---|
| 2023-07-27 | 226,300 | 89× | 4,914 | 1,569 | 21.2% | "Fate Tour Philippines na ba to?" |
| 2023-07-28 | 2,669 | 1.1× | 16 | 1 | 12.1% | "Sige Sunoo, lapit ka pa sa camera 😍" #enhypenfansign |
| 2025-07-04 | 2,873 | 2.4× | 20 | 9 | 5.5% | "Take me back on this time." (POV video call with ENHYPEN) |
| 2026-04-30 | 55,900 | 98× | 316 | 57 | 6.2% | "i got to meet heeseung and now blood saga is playing…" |

**Facts:**
- The 2023-07-27, 2025-07-04 and 2026-04-30 posts are one Weverse video call with Heeseung (call "A").
  - 2023 and 2026: confirmed by `research/02-video-breakdown.md`, which watched them ("same call footage as H1").
  - 2025: the transcripts match ("she loves you very much… where you from"). Very likely the same call.
- The 2023-07-28 Sunoo clip is a different fansign call.
- In call A, the idol talks *to a Filipino fan about the Philippines*: "where are you from?" / "I wanna go there soon" / "as soon as possible".
- The 21% like rate and 1,569 shares on the 2023 post are the highest on the account.

**The same footage got 226K, 2.9K and 56K views.**
- 2023: posted right as the Fate tour was being discussed, with a topical question as the hook.
- 2025: posted in a quiet period with a "POV" overlay.
- 2026: posted at the start of the Blood Saga era.

Inference: timing and the framing of the hook decided the outcome, not the footage.

**Not verified: whose call this is.** The fan's window shows the name "Summer (夏)", and the 2026 caption says "i got to meet heeseung". Confirm with the owner that the footage is hers before reusing it. The project rules forbid passing off someone else's footage as your own.

### 2.5 Sales posts by sub-type (subtypes with ≥4 videos)

| subtype | videos | median views | median rel. perf | % ≥2× local | comments/view |
|---|---|---|---|---|---|
| onhand / for sale | 36 | 2,180 | 1.50 | 39% | 0.1% |
| product showcase (no offer in caption) | 30 | 1,692 | 1.12 | 17% | 0.3% |
| concert angle ("be concert ready") | 15 | 2,011 | 1.06 | 33% | 0.1% |
| pre-order / GO | 22 | 1,049 | 1.05 | 27% | 0.1% |
| installment / reservation | 55 | 1,617 | 1.00 | 29% | 0.8% |
| GO caption-wall template (WTS / LFB) | 7 | 598 | 1.00 | 0% | 0.2% |
| sale / discount | 29 | 2,038 | 0.98 | 21% | 0.1% |
| teaser ("soon") | 6 | 1,230 | 0.87 | 0% | 0.4% |
| slots left / scarcity | 5 | 1,141 | 0.82 | 20% | 1.4% |
| off-niche products (hair wax, bags, sneakers, notebook, skincare) | 8 | 472 | 0.60 | 0% | 0.0% |

- **Onhand / "ready to ship"** is the only sales angle clearly above baseline.
- **Off-niche products flop every time.** 0 of 8 beat their neighbours, and they had 0 saves and 0 comments.
- **Installment posts** get far more comments per view than onhand or sale posts (0.8% vs 0.1%). Only the small drop-schedule and slots-left groups are higher. That fits the comment mining: people want to ask how installment works.
- **Concert angle** sales posts as a whole sit at baseline (rel. 1.01 for 57 flagged posts). The ones that did well were posted *inside a real concert window*: SVT tour Nov 2025, BLACKPINK tour Jun-Jul 2025, Caratbong Sep-Nov 2023.

---

## 3. Artists

| artist | videos | median views | median rel. perf | % ≥2× local | posts last 12m | median views last 12m |
|---|---|---|---|---|---|---|
| ENHYPEN | 164 | 1,364 | 1.00 | 23% | 27 | 529 |
| SEVENTEEN | 66 | 1,980 | **1.33** | 38% | 16 | **1,652** |
| BLACKPINK | 41 | 1,849 | 1.16 | 41% | 4 | 636 |
| general / no artist | 24 | 634 | 0.70 | 8% | 5 | 335 |
| BTS | 21 | 672 | 0.97 | **5%** | 14 | 568 |
| multi-artist | 19 | 1,495 | 1.00 | 16% | 1 | 849 |
| non-K-pop | 10 | 592 | 0.60 | 0% | 1 | 450 |
| TREASURE | 10 | 2,209 | 0.66 | 0% | 0 | – |
| EXO | 10 | 1,292 | 0.80 | 20% | 0 | – |
| TXT | 8 | 1,263 | 0.74 | 12% | 0 | – |
| BABYMONSTER | 6 | 614 | 1.03 | 0% | 6 | 614 |
| NCT | 4 | 4,877 | 1.33 | 25% | 0 | – |
| NewJeans | 4 | 9,830 | 1.85 | 50% | 0 | – |
| TWICE | 3 | 2,147 | 0.83 | 0% | 0 | – |

Singletons (1 video each): aespa, ATEEZ, &TEAM, IVE, Red Velvet, Dreamcatcher.

**Facts**
- **ENHYPEN is the core of the account.** It has 41% of all videos and both mega-hits (#1 and #2). Its everyday posts are only average, though, and in the last 12 months the median is 529.
- **SEVENTEEN (Caratbong) is the most consistent seller-content artist.**
  - Best relative performance overall.
  - Best median in the last 12 months.
  - 7 of the 12 SEVENTEEN posts between Sep and Nov 2023 got 16.5K-71.6K views.
- **BTS has had 14 posts in the last 12 months**, mostly ARIRANG tour and album pre-orders. Only 1 of 21 BTS posts ever doubled its neighbours.
  - Comments still ask for BTS stock: "may army bomb po kayo?" is the most-requested other item.
  - So the demand exists, but the BTS posts so far did not catch it.
- **The shop stopped posting most other fandoms** after 2023. Fans still ask for them in comments (section 8).

---

## 4. Timing (all times Philippine time, UTC+8)

### 4.1 Frequency and gaps

**Posts per year:**
- 2022: 151 posts in 4 months, often 2-5 a day
- 2023: 81
- 2024: 52
- 2025: 54
- 2026: 58 (28 of them in May)

**Gaps of 21 days or more, and what happened next:**

| resumed on | gap (days) | median of 5 posts before | median of 5 posts after | first post |
|---|---|---|---|---|
| 2023-07-24 | 61 | 6,332 | 2,552 | sales |
| 2024-03-12 | 26 | 1,085 | 1,245 | sales |
| 2024-05-28 | 51 | 1,393 | 2,225 | sales |
| 2024-08-01 | 64 | 1,343 | 2,225 | other |
| 2024-09-14 | 27 | 2,225 | 1,248 | sales |
| 2025-01-07 | 33 | 1,306 | 999 | unboxing |
| 2025-06-28 | 142 | 1,556 | 3,078 | sales (BLACKPINK tour window) |
| 2025-09-03 | 28 | 544 | 302 | sales |
| 2026-01-12 | 42 | 2,038 | 512 | sales |
| 2026-04-28 | 63 | 1,133 | 517 | fan moment (then the Heeseung hit) |
| 2026-07-30 | 27 | 629 | 442 | sales |
| 2026-08-23 | 23 | 629 | 446 | sales |

**Fact:** there is no consistent pattern. Some comebacks rose, some fell. A gap neither killed the account nor boosted it.

**Fact:** more posts per month did not lower views per post. The Spearman correlation between posts per month and that month's median views is 0.05 (p = 0.74). So posting volume is a lever for total reach.

The one exception is heavy same-day posting:

| posts that day | videos | median rel. perf | % ≥2× local |
|---|---|---|---|
| 1 | 185 | 1.04 | 28% |
| 2 | 128 | 0.93 | 18% |
| 3 | 45 | 1.10 | 27% |
| 4 | 28 | 0.81 | 14% |
| 5 | 10 | 0.80 | 10% |

On days with 4-5 posts, each post did about 20% worse. This is a weak signal (inference: the posts may compete with each other).

### 4.2 Day of week

| day | videos (all) | median rel. perf (all) | videos 2024-26 | median rel. perf 2024-26 |
|---|---|---|---|---|
| Monday | 51 | 1.01 | 21 | 1.05 |
| Tuesday | 55 | **0.75** | 28 | **0.78** |
| Wednesday | 66 | 1.05 | 23 | 1.08 |
| Thursday | 72 | 1.08 | 29 | 1.00 |
| Friday | 64 | 1.03 | 25 | 0.95 |
| Saturday | 57 | 0.89 | 25 | 0.88 |
| Sunday | 31 | 1.13 | 13 | 1.13 |

- Tuesday is lowest in both periods.
- The test is borderline all-time (Kruskal-Wallis p = 0.047) and **not significant for 2024-26** (p = 0.54).
- Conclusion: no reliable day effect. At most, avoid putting the most important post on a Tuesday.

### 4.3 Hour block

| hours | videos (all) | median rel. perf | videos 2024-26 | median rel. perf 2024-26 |
|---|---|---|---|---|
| 00-05 | 16 | 1.11 | 7 | 1.46 |
| 06-09 | 19 | 0.81 | 1 | 0.94 |
| 10-12 | 71 | 1.00 | 20 | 1.04 |
| 13-15 | 104 | 1.00 | 49 | 1.00 |
| 16-18 | 99 | 1.02 | 43 | 0.97 |
| 19-21 | 62 | 0.78 | 29 | 0.95 |
| 22-23 | 25 | 1.25 | 15 | 1.10 |

- Late-night posts (22:00-05:00) look slightly better, but only 7-25 videos are behind that.
- The hour effect is not significant (Kruskal-Wallis p = 0.13).
- Most recent posts go out at 15:00-16:00. This is a cheap thing to A/B test, not a finding.

---

## 5. Video length

| length | videos | median views | median rel. perf | % ≥2× local | likes/view | saves/view |
|---|---|---|---|---|---|---|
| photo slideshow | 22 | 1,207 | 0.96 | 18% | 2.2% | 0.1% |
| 1-10s | 50 | 1,602 | 1.07 | 34% | 2.8% | 0.2% |
| 11-20s | 100 | 1,243 | 0.94 | 15% | 2.9% | 0.1% |
| 21-30s | 70 | 1,462 | 1.00 | 30% | 3.5% | 0.2% |
| 31-45s | 89 | 1,590 | 1.00 | 24% | 3.7% | 0.2% |
| 46-60s | 45 | 1,915 | 1.03 | 18% | 2.9% | 0.2% |
| 61-120s | 14 | 1,617 | 1.06 | 21% | 2.6% | 0.3% |
| >120s | 6 | 4,339 | 1.63 | 50% | 2.7% | 0.2% |

- **No relationship between length and relative performance** (Spearman 0.02, p = 0.74). Top-quartile and bottom-quartile videos have the same median length: 25s vs 23s (Mann-Whitney p = 0.66).
- Longer videos get **saved slightly more** (Spearman 0.14 with saves per view, p = 0.009).
- The 6 videos over 120s are all explainers (installment, pooling, courier pros and cons, giveaway, merch rundowns) and did well. That is a small sample.
- **The real completion data is in TikTok Studio, not here.**

---

## 6. Audio

| audio | videos | median rel. perf | % ≥2× local | 2024-26 median rel. perf |
|---|---|---|---|---|
| licensed / trending music | 246 | 1.00 | 19% | 0.97 |
| other creator's original sound | 78 | 1.13 | 36% | 1.00 |
| own original sound (owner's voice-over) | 72 | 1.00 | 24% | 1.06 |

- **No meaningful audio effect.**
- The "other creator's sound" lead comes mostly from one sound ("original sound - chay daisy…"). It was used on 8 Caratbong posts in Sep 2023-Jan 2024, with a median of 20,950 views. That sound overlaps with the SEVENTEEN tour ticketing window, so the two effects can't be separated.
- In 2022 the shop rode "Pink Venom" (38 uses, median rel. 1.15).
- Since late 2024 the shop mostly uses its own voice-over: "original sound - Unnie Mart 2", 47 uses, median 651 views, rel. 1.05. Voice is not hurting.

---

## 7. Captions and hashtags

| caption feature | finding |
|---|---|
| Length (hashtags removed) | No effect. Every bucket has a median rel. perf of 0.96-1.08; only empty captions sit lower at 0.81. Top vs bottom quartile median length: 49 vs 52 characters (p = 0.85). |
| Language | No effect: English 1.00, Taglish 1.03, mostly-English 1.06. |
| Question in caption | No effect: 0.97 vs 1.00. |
| GO caption-wall template ("WTS / LFB / PH GO", prices, DOP dates; used since 2025-10-14) | 11 posts: median 612 views vs 609 for other posts in the same period. Only 9% doubled their neighbours vs 25%. Not worse, but not working. The price lists themselves are clear and buyers need them. |
| Hashtag count | No effect: 0 tags = 1.00, 5 tags = 1.00, 8+ = 1.00. |
| #fyp / #fypシ | No effect: 164 uses, rel. 1.00. |
| Product-model hashtags (#svtlightstick, #blackpinklightstickversion2, #hammerbongv2, #caratbongv3) | Highest median rel. perf: 12.5, 3.05, 2.42 and 1.37. These are the words people search for. Inference: model-name search matters more than generic tags. |
| Shop and mismatched tags (#unniemart_, #enhypenedit on sales posts) | Below baseline: 0.65 and 0.73. |
| TikTok Shop product tagged | 101 posts, rel. 1.38 overall. Within the same period (Dec 2022-2024) the gap is not significant (p = 0.16). The difference mostly reflects which era the posts came from. |

**Inference, small sample:** several 2025-26 captions read like pasted AI text:
- a caption that literally contains "Suggested title and hashtags" (2025-07-21, 240 views)
- markdown `**bold**` that TikTok doesn't render (2026-04-28)
- English hype lines like "stay till the end — the surprise will make your day" (2026-05-07, 374 views)

None of these beat their neighbours, except the Heeseung clip, where the video carried it. It is also off-voice for a Taglish shop, and this project's rules forbid it.

---

## 8. Comment mining (audience voice)

**Sample:** 29 videos and 1,057 top-level comments, of which 1,015 are from fans and 42 from the shop.

**Caveats:**
- 889 of the 1,015 fan comments come from 2022-23 videos, because recent posts get few comments.
- Some clusters are concentrated on one or two videos. The **videos** column shows how many videos each cluster appears on.
- Quotes are verbatim. Every comment with its label is in `data/comments.csv`.

### 8.1 Cluster counts

| cluster | comments | share of fan comments | videos | total likes |
|---|---|---|---|---|
| Q: availability / stock / slots / restock ("available pa po?") | 220 | 21.7% | 18 | 8 |
| Fear: budget, saving, can't afford | 96 | 9.5% | 13 | 1,618 |
| Q: payment / installment / how to order | 91 | 9.0% | 15 | 15 |
| Order intent (interested, reserve, "nag-PM po ako", keyword) | 78 | 7.7% | 17 | 30 |
| Request: another artist or item | 73 | 7.2% | 14 | 30 |
| Ticket-first: will buy after getting a concert ticket | 63 | 6.2% | 4 | 304 |
| Q: price ("hm po?") | 58 | 5.7% | 17 | 13 |
| Q: lightstick setup / connect / tech help | 48 | 4.7% | 4 | 496 |
| Other / unclear (emoji, noise) | 47 | 4.6% | 16 | 17 |
| Q: product details (version, inclusions, POB, size) | 34 | 3.3% | 14 | 10 |
| Fan reaction / idol talk | 33 | 3.3% | 6 | 89 |
| Tag-a-friend (with or without text) | 63 | 6.2% | 16 | 46 |
| Q: legit / official / original? | 27 | 2.7% | 10 | 7 |
| Q: shipping / ETA / "will it arrive before the concert?" | 26 | 2.6% | 7 | 5 |
| Friction: form, link, DM or checkout not working, or no reply | 25 | 2.5% | 6 | 4 |
| Q: other sales channel (Shopee, Lazada, store, no Twitter) | 18 | 1.8% | 8 | 6 |
| Praise / testimonial | 8 | 0.8% | 2 | 4 |
| Complaint: price change, inconsistency or delay | 7 | 0.7% | 6 | 2 |

**Grouped:**
- Buying questions (stock, how to order, price, details, legit, shipping, channel) make up **47%** of fan comments (54% including requests for other artists).
- Explicit blockers (budget, ticket-first, friction, complaints) make up **19%**.

### 8.2 Clusters with real quotes

**Q: availability / stock / slots (220 comments, 18 videos)**

The single most common comment on the account, typically 20-40 copies per big sales post.
- "may stock pa po ba?" ("do you still have stock?"). [Payday sale, Caratbong v3, 2023-11-15](https://www.tiktok.com/@unniemart_/video/7301496055420488966). This one video has 43 availability questions.
- "may slot pa po ba" ("any slots left?"). [Enhypen SG 2023 for installment, 2022-12-02](https://www.tiktok.com/@unniemart_/video/7172362216790838554). 42 on this video.
- "HELLO PO WHEN PO ULIT RESTOCK NG CARATBONG VER 3😭" ("when will Caratbong ver 3 be restocked?"). [Onhand Caratbong v3, 2023-10-13](https://www.tiktok.com/@unniemart_/video/7289280910229376262)

**Q: payment / installment / how to order (91 comments, 15 videos)**
- "pano Po Maka utang😅" ("how do I buy on credit?"). [Pwede hulugan, 2022-09-28](https://www.tiktok.com/@unniemart_/video/7148315872703122714)
- "how much po weekly??" Same video.
- "kapag po ba na full n yung payment before mag feb 2023 makukuha na rin yung lightstick? or mismong feb din makukuha? thanks!" ("if I pay in full before Feb 2023, do I get the lightstick then, or only in Feb?"). [Naku iMessage, 2022-09-26](https://www.tiktok.com/@unniemart_/video/7147618684377304346)
- "yung Dp po monthly po ba yun or everyday? 😅" ("is the downpayment monthly or daily?"). [Enchin reservation form, 2026-05-19](https://www.tiktok.com/@unniemart_/video/7641579351523200274)

**Q: price (58 comments, 17 videos)**

Mostly a bare "hm po?" ("how much?").
- "San po makikita kung magkano ?" ("where can I see the price?"). [SOLD OUT Hammerbong, 2022-10-08](https://www.tiktok.com/@unniemart_/video/7151993441289817370)
- "2850 Po talaga price ?" ("is the price really 2,850?"). [New arrival Caratbong, 2023-10-05](https://www.tiktok.com/@unniemart_/video/7286352737850199301)
- "magkano po mga price" ("how much are they?"). [Enchin reservation form, 2026-05-19](https://www.tiktok.com/@unniemart_/video/7641579351523200274). That caption said "Check comment for the price".

**Q: legit / official / original? (27 comments, 10 videos)**
- "legit po ba?" [Go to our TikTok shop, Enhypen lightstick, 2023-01-03](https://www.tiktok.com/@unniemart_/video/7184286239791648027)
- "galing po sa sokor po talaga?" ("is it really from South Korea?"). [Onhand items, 2023-01-10](https://www.tiktok.com/@unniemart_/video/7186903723065511195)
- "100 pesos lang? so ibig-sabihin peke yan?" ("only 100 pesos? so it's fake?"). [SOLD OUT Hammerbong, 2022-10-08](https://www.tiktok.com/@unniemart_/video/7151993441289817370). The 100-peso downpayment confused people: 16 comments mention "100".
- "legit Po ba tong shop na toooooo..... surprising my sister huhuuu" ("is this shop legit? I'm surprising my sister"). [Engenebong V2 tutorial, 2025-01-25](https://www.tiktok.com/@unniemart_/video/7463827377362062610)

**Q: lightstick setup / tech help (48 comments, 4 videos; the most-liked questions on the account)**
- "the app name "EN-official light stick ver. 2" it this right?" (**283 likes**). [Engenebong V2 tutorial](https://www.tiktok.com/@unniemart_/video/7463827377362062610)
- "Ate can you help po my lightstick cannot connect to concert mode it says po wala pa pong concert on going" (45 likes). Same video.
- "y en el concierto se conecta automático?" (Spanish: "does it connect automatically at the concert?"). Same video.
- "yung sa akin naman, nacoconnect siya sa app pero hindi ko mapagana yung pagsync sa music huhu can anyone help ano pwede gawin 🥹" ("mine connects to the app but won't sync to music, can anyone help?"). [Hammerbong V2 connect tutorial, 2023-03-02](https://www.tiktok.com/@unniemart_/video/7205968214898019610)

**Q: shipping / "will it arrive before the concert?" (26 comments, 7 videos)**
- "Sa makati po ilang days po kaya? Baka dina po kasi umabot sa day 2 concert😭" ("how many days to Makati? it might not make day 2 of the concert"). [Restock Blackpink V2, 2023-03-17](https://www.tiktok.com/@unniemart_/video/7211459808828968198)
- "Hello! Aabot po ba sa feb 4 yung engene bong?" ("will the Engenebong arrive by Feb 4?"). [Onhand items, 2023-01-10](https://www.tiktok.com/@unniemart_/video/7186903723065511195)
- "Hi po, may same day delivery po kayo?" [Restock Blackpink V2, 2023-03-17](https://www.tiktok.com/@unniemart_/video/7211459808828968198)

**Q: product details (34 comments, 14 videos)**
- "haiii anong version po ito?" ("which version is this?"). [New arrival Caratbong, 2023-10-05](https://www.tiktok.com/@unniemart_/video/7286352737850199301)
- "wala na pong ls only? huhu" ("is there no lightstick-only option anymore?"). Buyers didn't want the bundle. [Payday sale Caratbong v3, 2023-11-15](https://www.tiktok.com/@unniemart_/video/7301496055420488966)
- "what's the difference between feta and neta box po?" [Estimated time post, 2023-12-27](https://www.tiktok.com/@unniemart_/video/7317225951765597445)
- "I am seeing a v2 that comes in a black box like this one and another with a white box. What is the difference in the actual product? I need to buy one for my daughter but very confused what to choose. Help." (a parent buyer). [Enhypen lightstick, 2023-01-03](https://www.tiktok.com/@unniemart_/video/7184286239791648027)

**Q: other sales channel (18 comments, 8 videos)**
- "is there any other shop we can buy this from aside tiktok shop? i'm not familiar with tiktok shop po kase huhu" [Payday sale, 2023-11-15](https://www.tiktok.com/@unniemart_/video/7301496055420488966)
- "how to order po without a Twitter account??" [Enhypen SG 2023, 2022-12-02](https://www.tiktok.com/@unniemart_/video/7172362216790838554)
- "May Lazada po ba kayo?" Same video. That video also has 4 more Shopee ("orange app") questions, and the Onhand Caratbong post has 5.

**Friction: form, link, DM, checkout, no reply (25 comments, 6 videos)**
- "action cant be completed when clicking the form." [Installment explainer, 2023-09-15](https://www.tiktok.com/@unniemart_/video/7278924600619191557). This video has 10 form complaints. The shop later commented a workaround: "copy and paste this in Google if form is not working".
- "Di ko po kayo mamessage" ("I can't message you"). [Restock Blackpink V2, 2023-03-17](https://www.tiktok.com/@unniemart_/video/7211459808828968198)
- "Hi how to order po? Wala sa yellow basket" ("it's not in the yellow basket"). Same video.
- "Please reply po 😭" Same video.

**Fear: budget, saving, can't afford (96 comments, 13 videos; 65 of them on the 2023 Heeseung clip)**
- "next year na lang please 😭" (**1,291 likes**, the most-liked comment in the whole sample). [Fate Tour clip, 2023-07-27](https://www.tiktok.com/@unniemart_/video/7260516146452139269). Fans are begging the tour to wait until they have saved up. Budget comments hold 1,601 of the 1,671 likes on that video.
- "huwag muna nag iipon pa ako 😭😭😭" ("not yet, I'm still saving", 267 likes). Same video.
- "natatakot ako baka hindi ko mafullypaid sa dop 😭" ("I'm afraid I won't finish paying by the due date"). [Naku iMessage, 2022-09-26](https://www.tiktok.com/@unniemart_/video/7147618684377304346)
- "Im really planning to get an NCT bong, feeling ko naman makaya ko yung installment pero yung "practicality" talaga grrrr.... ❤️" ("I think I can handle the installment, but practicality…"). [Installment explainer, 2023-09-15](https://www.tiktok.com/@unniemart_/video/7278924600619191557)

**Ticket-first: will buy after getting a concert ticket (63 comments, 4 videos; all SEVENTEEN Caratbong, Sep-Oct 2023)**
- "Babalikan ko ito kapag naka secured na ako ng ticket. Manifestinggg!!!" ("I'll come back to this once I've secured a ticket", **168 likes**). [New arrival Caratbong, 2023-10-05](https://www.tiktok.com/@unniemart_/video/7286352737850199301). 45 comments like this on one video.
- "Sabi ko babalikan ko ito kapag naka secured ako, and guess what? Naka secured akoo. May stock pa rin po baa?" ("I said I'd come back once I got a ticket, and I did. Is there still stock?"). Same video. The follow-through happens.
- "WAG NYO AKO UBUSAN. MAGSESECURE MUNA AKO NG TICKEEEEET 😭" ("don't sell out on me, I'm getting my ticket first"). [Onhand Caratbong v3, 2023-10-13](https://www.tiktok.com/@unniemart_/video/7289280910229376262)

**Request: another artist or item (73 comments, 14 videos)**

What was asked for: BTS / Army Bomb 15, SEVENTEEN / Caratbong 12, TWICE 8, TREASURE 8, ENHYPEN items (cases, mini lightstick, albums) 7, NCT 4, EXO 3, BLACKPINK 3, Stray Kids 2, TXT 2, plus Kep1er, ILLIT, SNSD, ATEEZ, Red Velvet and others.
- "may army bomb po kayo?" [SOLD OUT Hammerbong, 2022-10-08](https://www.tiktok.com/@unniemart_/video/7151993441289817370)
- "StrayKids LS when kaya🤧" [Onhand items, 2023-01-10](https://www.tiktok.com/@unniemart_/video/7186903723065511195)
- "Do you have Illit? and if have pls show" [Caratbong, TikTok Shop and Shopee, 2025-11-27](https://www.tiktok.com/@unniemart_/video/7577326187291184391)
- "may mini lightstick po ba kayo ng enhypen?" [Engenebong V2 tutorial](https://www.tiktok.com/@unniemart_/video/7463827377362062610)

**Order intent (78 comments, 17 videos)**

Includes 26 keyword comments where the shop asked for a keyword: "Inch, pls follow" in 2022 and "Enchin" in 2026.
- "inch, pls follow" (one of 22 copies). [Naku iMessage, 2022-09-26](https://www.tiktok.com/@unniemart_/video/7147618684377304346). The shop's own comment asked people to type it.
- "ENCHIN!!" [Comment "Enchin" to reserve, 2026-05-12](https://www.tiktok.com/@unniemart_/video/7639031726462733586). This post had a 0.32% comment rate when the 2026 median is 0%.
- "nag pm po ako:)" ("I sent a PM"). [BABYMONSTER lightstick GO, 2026-05-16](https://www.tiktok.com/@unniemart_/video/7640334648203169031). On recent sales posts, most comments are "I DM'd you".

**Praise / testimonial (8 comments, 2 videos; rare)**
- "highly recommend this shop super secured ng lightstick" ("the lightstick was packed super securely"). [Installment explainer, 2023-09-15](https://www.tiktok.com/@unniemart_/video/7278924600619191557)
- "OMG! Bumili ako sa Kpop Merch for 3500 sayang huhuhuhu" ("I bought it elsewhere for 3,500, what a waste"). Same video. Price advantage seen by a buyer.
- "omg! nakakita rin hahahaha nag struggle ako dito. tysm" ("finally found this, I struggled with it, thank you so much"). [Engenebong V2 tutorial](https://www.tiktok.com/@unniemart_/video/7463827377362062610)

**Complaints: price change or delay (7 comments, 6 videos)**
- "@Unnie Mart pls clarify the updated price, 3.3k + here sa yellow basket then sa reservation form sa bio niyo 3k? what's the real price?" [Payday sale, 2023-11-15](https://www.tiktok.com/@unniemart_/video/7301496055420488966)
- "ung sakin po umorder ng October pa gang ngayon wala padin..🥺" ("I ordered in October and still nothing"). [Onhand Caratbong v3, 2023-10-13](https://www.tiktok.com/@unniemart_/video/7289280910229376262)

**Fan reaction / idol talk (33 comments, 6 videos)**
- "what if yung fanmeet?????????????" (24 likes). [Fate Tour clip, 2023-07-27](https://www.tiktok.com/@unniemart_/video/7260516146452139269)
- "Kaya siguro andami nilang binibigay na sign na may 2nd world tour dito sa ph" ("maybe that's why they keep hinting at a 2nd world tour in PH"). Same video.
- "omg grabi napakaswerte naman ni ate ☺️☺️☺️" ("wow, ate is so lucky"). [Heeseung clip, 2026-04-30](https://www.tiktok.com/@unniemart_/video/7634520116150963476)

### 8.3 Language

| language (heuristic) | comments | share |
|---|---|---|
| Taglish (mixed) | 409 | 40.3% |
| Tagalog | 393 | 38.7% |
| English | 135 | 13.3% |
| emoji / mention only | 64 | 6.3% |
| Spanish / Portuguese | 8 | 0.8% |
| Indonesian / Sundanese | 5 | 0.5% |
| Korean | 1 | 0.1% |

- The buyer audience writes Tagalog or Taglish (79%), with "po" everywhere. The shop's captions are 70% English.
- Exception: on the 225K Engenebong V2 tutorial, at least 12 of 53 fan comments (23%) are Spanish, Indonesian or Korean. The tutorial reached a global audience of lightstick owners, not only PH buyers. That is good for reach and saves, but **those viewers are mostly not customers**.

### 8.4 What the comments say, in one paragraph

- **Facts:**
  - Fans mostly ask things the post could have answered: is it in stock, how installment works, the price, the version, will it arrive before the concert, and is it legit.
  - Purchases are gated by two real-life events: getting a concert ticket, and saving money or payday ("pahintay po ng 13 month ko", "wait for my 13th-month pay").
  - People ask for artists the shop no longer posts, BTS above all.
  - The shop's order path has broken more than once (form errors, item missing from the basket, Twitter-only DMs).
- **Inference:**
  - The "available pa po?" flood is a missed-content signal, not just noise. A post that says "X left, ships Y, ₱Z or ₱300 DP" would answer most of it.
  - On recent posts the comments are mostly "nag-PM po ako", so buyers move to DM fast. That is good for sales but invisible to the algorithm.
- **Limit:** the data can't show how fast or how often the shop answered. Replies were not scraped. 60% of question comments have at least one reply, but the replies could come from anyone.

---

## 9. What the hits have in common vs the flops

### 9.1 Top 25% vs bottom 25% by relative performance (99 videos each)

| feature | bottom 25% | top 25% |
|---|---|---|
| median views | 785 | 10,100 |
| median length | 23s | 25s |
| share that are sales posts | 63% | 71% |
| share that are tutorials | **1%** | **13%** |
| share that are fan moments or concert content | 8% | 5% |
| share that are slideshows | 3% | 4% |
| share using own voice-over sound | 21% | 18% |
| median caption length (characters) | 52 | 49 |
| median hashtag count | 5 | 5 |
| share with a TikTok Shop product tag | 18% | 46% (mostly an era effect, see section 7) |
| share SEVENTEEN | 8% | 26% |
| share ENHYPEN | 41% | 42% |

**Facts (data-backed):**
1. **Format is the difference, not packaging.** Length, caption length, hashtags, audio, language, day and hour show no reliable difference between hits and flops. Tutorials are 13× more common among top performers.
2. **The two biggest hits are a lightstick tutorial and an idol video-call clip.** The shop has made 8 lightstick tutorials and posted the one video call 3 times. Between them the two hits hold 51% of all saves.
3. **The working tutorials are short (38-44s)**, step-by-step, and named for one specific model plus "to the app". The 2025-26 tutorials that broke this pattern flopped (82s with a long intro; "watch it on YouTube").
4. **The 2022-23 sales hits sat inside fan buying windows**, by fans' own comments:
   - "march 26 concert" and "day 2" (BLACKPINK, Mar 2023; Hammerbong posts 14K-38K)
   - "feb 4" (ENHYPEN, early 2023; Engenebong posts 10K-38K)
   - Follow tour ticket selling around "nov 11" (SEVENTEEN, Sep-Nov 2023; Caratbong posts 16.5K-72K)

   The concert dates come from comments and are **not verified**.
5. **The installment offer drives conversation more than views.**
   - "Pwede hulugan" got 89K views and 1,006 comments.
   - Installment posts get 0.8% comments per view vs 0.1% for onhand or sale posts.
   - But as a group, posts mentioning the 100-peso DP or installment are only slightly above baseline (rel. 1.16 vs 1.00 in 2022-23).
6. **Since 2024 nothing in the sales-post family reliably breaks out.** Sales posts in 2024-26: median rel. 1.00, and 23% doubled their neighbours, the same rate as in 2022-23. The baseline itself fell about 4×.
7. **Off-niche products and generic trend/meme skits are consistent flops.** Off-niche: 0 of 8 ever doubled. Skits since 2024: 0 of 12.

**Inferences (not proven by this data):**
- Tutorials win because they are **searched and saved**: people type "how to connect caratbong v3" when the box arrives. That makes them evergreen. Checking TikTok Studio's traffic source for these two videos would confirm or refute this.
- The video call wins because it is **rare, emotional and specific to the Philippines** ("I'm from the Philippines", "as soon as possible"), and because the comments fill up with "next year please" banter. The 2.9K repost shows the footage alone is not enough.
- The 2022-23 boom was partly the platform and timing: more reach for small sellers then, a TikTok Shop push, and tours coming back after COVID. Format alone can't bring it back.
- Sales posts are necessary for business but are not the growth engine. They should ride on demand that other content creates.

### 9.2 Open questions the data can't answer

1. **Traffic source** for the two tutorials and the Heeseung clip (Search vs For You). Get it from TikTok Studio.
2. **Follows gained per video**, and **average watch time and completion**. Get them from TikTok Studio, ideally exported for the last 60 days plus the hits.
3. **Were any posts promoted?** Especially the 24.8K tote post (16 likes) and the 10K "Binagsak" and "Enchin" posts.
4. **Did the hits sell?** Orders and DMs in the 7 days after the 2025-01-25 tutorial, the 2026-04-30 clip and the 2026-05-12 Enchin post. Needs the shop's order log.
5. **Whose video call is it?** The content is confirmed (Weverse video call with Heeseung), but not who the fan is ("Summer (夏)"). Are there more unposted video-call or fansign recordings the owner made herself?
6. **Why did engagement per view fall 2-3× from 2022 to 2024?** The audience changed (fans vs strangers), distribution changed, or the content changed. These can't be separated with one snapshot.
7. **Response speed in comments and DMs.** Can't measure; replies were not scraped.
8. **Can international tutorial viewers buy?** (Does the shop ship outside PH?) If not, tutorial reach is brand awareness, not sales.
9. **Unwatched visuals.** Hooks, face vs product shots and on-screen text were not analysed. Only 110 of 396 videos have auto-transcripts. A manual watch of the top 20 and 20 random flops would close this gap.

---

## 10. Conclusions, ranked by confidence

| # | conclusion | confidence | basis |
|---|---|---|---|
| 1 | Per-post reach fell about 4-5× from 2023 to 2026 (median 2,793 → 608), and comment activity collapsed (50% of 2026 posts have 0 comments). | **High, fact** | All 396 videos |
| 2 | Lightstick setup tutorials are the most reliable outperformers on this account: 8 videos, median 21K views, 6.3× their neighbours. The working pattern is short, numbered steps, and one named model "to the app". | **High, fact** (pattern: medium) | Sections 2.1, 2.3; p < 0.001 |
| 3 | Plain sales posts (68% of output) perform at baseline. The new GO caption-wall template has not changed that. | **High, fact** | Sections 2, 7 |
| 4 | Fans' main need in comments is basic purchase info: stock, how to order or pay in installments, price, version, arrival date, and is it legit. Together these are about 47% of fan comments. | **High, fact** | 1,015 labelled comments |
| 5 | Purchases are gated by concert tickets and by money or payday, in fans' own words. Installment is a real draw. | **High, fact** (quotes); medium on how much it matters | Section 8.2 |
| 6 | Timing, length, audio, caption length, caption language and hashtag count have no reliable effect on this account. | **Medium-high** | Section 4-7 stats; small samples per bucket |
| 7 | An idol video-call clip that speaks to PH fans is a high-ceiling format. One call posted 3 times became the #1 and #5 videos. The same footage ranged from 2.9K to 226K, so timing and hook framing matter. | **Medium**: fact for performance (n = 1 recording); who owns the footage is unverified | Section 2.4; confirmed by 02-video-breakdown |
| 8 | SEVENTEEN is currently the most responsive artist for sales content. BTS demand shows up in comments but not yet in views. | **Medium** | Sections 3, 8 |
| 9 | Tutorial and clip hits are search- and emotion-driven and reach non-buyers (23% non-PH-language comments on the V2 tutorial). | **Medium-low, inference** | Comments; no traffic data |
| 10 | Order-path friction (forms, basket, Twitter-only, no Shopee) has cost sales. | **Medium-low, inference** | 25 friction and 18 channel comments, mostly 2023; current state unknown |
| 11 | AI-sounding English captions underperform and are off-voice. | **Low, inference** | A few 2025-26 posts |
| 12 | A comment-keyword call to action ("Comment Enchin") lifts comment rate. | **Low** (2 examples: "Inch, pls follow" 2022, "Enchin" 2026) | Section 8.2 |

---

## 11. Apify spend (actual, from each run's `usageTotalUsd`)

All runs used token #4 (`apify_api_…U4B`, the one with the most room). I used `clockworks~tiktok-profile-scraper` instead of `clockworks~tiktok-scraper`: same vendor and same fields, but $0.0030 vs $0.0037 per video.

| run id | actor | what | items | cost |
|---|---|---|---|---|
| juHCAmFJ2jJnxZpMG | clockworks/tiktok-profile-scraper | all videos, latest-first | 396 | $1.188 |
| KegakR0vdUvqVhBFb | clockworks/tiktok-profile-scraper | popular-first cross-check | 25 | $0.075 |
| z991ynK0vHLqjJ8yj | clockworks/tiktok-comments-scraper ($0.00125 per comment) | comments on 29 videos, max 100 each, top-level only | 1,057 | $1.321 |
| | | | **total** | **$2.584** (cap was $4.00) |

The auto-caption files (110 videos) were downloaded straight from TikTok's servers at no cost.

---

## Appendix A · Top 20 videos

| # | date | views | × account median | saves | comments | shares | sec | type | what it is | artist | link |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2023-07-27 | 226,300 | 155 | 4,914 | 355 | 1,569 | 23 | fan moment | Weverse video call with Heeseung ("as soon as possible"), 1st post of call A | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7260516146452139269) |
| 2 | 2025-01-25 | 225,400 | 154 | 3,976 | 144 | 712 | 38 | tutorial | lightstick connect (Engenebong V2) | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7463827377362062610) |
| 3 | 2022-09-28 | 89,200 | 61 | 937 | 1,006 | 131 | 45 | sales | "Pwede hulugan" installment teaser | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7148315872703122714) |
| 4 | 2023-10-05 | 71,600 | 49 | 1,256 | 320 | 430 | 6 | sales | new arrival + installment form | SEVENTEEN | [video](https://www.tiktok.com/@unniemart_/video/7286352737850199301) |
| 5 | 2026-04-30 | 55,900 | 38 | 316 | 18 | 57 | 21 | fan moment | same call A reposted ("Where are you from? Philippines") | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7634520116150963476) |
| 6 | 2023-10-13 | 52,600 | 36 | 105 | 48 | 27 | 12 | sales | onhand Caratbong v3 | SEVENTEEN | [video](https://www.tiktok.com/@unniemart_/video/7289280910229376262) |
| 7 | 2023-11-15 | 50,600 | 35 | 113 | 74 | 40 | 25 | sales | payday sale Caratbong v3 | SEVENTEEN | [video](https://www.tiktok.com/@unniemart_/video/7301496055420488966) |
| 8 | 2023-01-10 | 45,200 | 31 | 244 | 92 | 51 | 6 | sales | onhand items (multi) | multi | [video](https://www.tiktok.com/@unniemart_/video/7186903723065511195) |
| 9 | 2022-12-02 | 43,300 | 30 | 476 | 157 | 70 | 32 | sales | Enhypen SG 2023 for installment | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7172362216790838554) |
| 10 | 2022-10-08 | 42,900 | 29 | 156 | 197 | 11 | 18 | order update | "SOLD OUT NA ULIT" Hammerbong | BLACKPINK | [video](https://www.tiktok.com/@unniemart_/video/7151993441289817370) |
| 11 | 2023-09-15 | 42,500 | 29 | 507 | 160 | 199 | 175 | tutorial | how our installment works (reply to a comment) | SEVENTEEN | [video](https://www.tiktok.com/@unniemart_/video/7278924600619191557) |
| 12 | 2023-01-03 | 38,600 | 26 | 143 | 47 | 31 | 30 | sales | onhand Enhypen lightstick, TikTok Shop | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7184286239791648027) |
| 13 | 2023-03-17 | 38,200 | 26 | 73 | 110 | 28 | 7 | sales | restock Blackpink V2 (concert week) | BLACKPINK | [video](https://www.tiktok.com/@unniemart_/video/7211459808828968198) |
| 14 | 2022-09-26 | 37,000 | 25 | 198 | 172 | 26 | 17 | sales | "100 pesos lang", DM to reserve | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7147618684377304346) |
| 15 | 2022-09-18 | 36,400 | 25 | 155 | 8 | 25 | 44 | tutorial | how to use Enhypen lightstick first time | ENHYPEN | [video](https://www.tiktok.com/@unniemart_/video/7144618818113998106) |
| 16 | 2023-03-29 | 33,500 | 23 | 158 | 51 | 35 | slideshow | sales | pre-order Binkybong | NewJeans | [video](https://www.tiktok.com/@unniemart_/video/7215876142018923782) |
| 17 | 2025-01-14 | 30,500 | 21 | 199 | 10 | 57 | 43 | tutorial | lightstick connect (Caratbong V3) | SEVENTEEN | [video](https://www.tiktok.com/@unniemart_/video/7459643459536817416) |
| 18 | 2023-03-02 | 30,000 | 21 | 81 | 58 | 33 | 114 | tutorial | lightstick connect (Hammerbong V2) | BLACKPINK | [video](https://www.tiktok.com/@unniemart_/video/7205968214898019610) |
| 19 | 2023-03-04 | 28,700 | 20 | 47 | 58 | 8 | 54 | sales | WTS LFB Hammerbong V2 | BLACKPINK | [video](https://www.tiktok.com/@unniemart_/video/7206552157598911771) |
| 20 | 2023-03-01 | 28,500 | 20 | 104 | 57 | 21 | 8 | sales | WTS LFB Hammerbong V2 + Engenebong | multi | [video](https://www.tiktok.com/@unniemart_/video/7205522038142848283) |

## Appendix B · Monthly views

| month | posts | median views | max views | total views |
|---|---|---|---|---|
| 2022-09 | 51 | 942 | 89,200 | 314,101 |
| 2022-10 | 64 | 1,679 | 42,900 | 239,087 |
| 2022-11 | 21 | 1,495 | 22,500 | 63,645 |
| 2022-12 | 15 | 2,741 | 43,300 | 82,552 |
| 2023-01 | 16 | 2,651 | 45,200 | 140,035 |
| 2023-02 | 11 | 2,210 | 17,000 | 50,874 |
| 2023-03 | 12 | 15,850 | 38,200 | 211,384 |
| 2023-04 | 7 | 4,869 | 6,688 | 30,465 |
| 2023-05 | 2 | 6,374 | 10,600 | 12,747 |
| 2023-06 | 0 | – | – | – |
| 2023-07 | 6 | 1,739 | 226,300 | 234,156 |
| 2023-08 | 6 | 1,398 | 2,962 | 9,686 |
| 2023-09 | 11 | 2,523 | 42,500 | 113,989 |
| 2023-10 | 4 | 28,596 | 71,600 | 131,870 |
| 2023-11 | 3 | 16,500 | 50,600 | 68,598 |
| 2023-12 | 3 | 2,604 | 25,400 | 30,358 |
| 2024-01 | 13 | 1,587 | 10,700 | 31,885 |
| 2024-02 | 3 | 1,085 | 2,385 | 4,526 |
| 2024-03 | 9 | 1,118 | 2,148 | 11,392 |
| 2024-04 | 6 | 1,450 | 8,260 | 15,257 |
| 2024-05 | 1 | 1,343 | 1,343 | 1,343 |
| 2024-06 | 0 | – | – | – |
| 2024-07 | 0 | – | – | – |
| 2024-08 | 5 | 2,225 | 2,969 | 10,274 |
| 2024-09 | 3 | 1,491 | 1,759 | 4,498 |
| 2024-10 | 5 | 751 | 2,224 | 5,122 |
| 2024-11 | 6 | 1,890 | 5,617 | 14,597 |
| 2024-12 | 1 | 1,306 | 1,306 | 1,306 |
| 2025-01 | 8 | 1,166 | 225,400 | 283,964 |
| 2025-02 | 2 | 1,449 | 1,556 | 2,898 |
| 2025-03 | 0 | – | – | – |
| 2025-04 | 0 | – | – | – |
| 2025-05 | 0 | – | – | – |
| 2025-06 | 4 | 3,352 | 8,129 | 15,746 |
| 2025-07 | 15 | 697 | 6,027 | 19,124 |
| 2025-08 | 3 | 1,935 | 10,300 | 12,779 |
| 2025-09 | 5 | 302 | 1,191 | 2,503 |
| 2025-10 | 5 | 339 | 1,344 | 2,743 |
| 2025-11 | 11 | 894 | 11,900 | 25,117 |
| 2025-12 | 1 | 2,038 | 2,038 | 2,038 |
| 2026-01 | 9 | 621 | 2,011 | 6,545 |
| 2026-02 | 4 | 1,457 | 1,836 | 5,421 |
| 2026-03 | 0 | – | – | – |
| 2026-04 | 4 | 1,154 | 55,900 | 58,620 |
| 2026-05 | 28 | 544 | 10,300 | 27,477 |
| 2026-06 | 4 | 1,009 | 24,800 | 27,430 |
| 2026-07 | 3 | 598 | 651 | 1,691 |
| 2026-08 | 2 | 438 | 446 | 876 |
| 2026-09 | 3 | 896 | 1,156 | 2,468 |
| 2026-10 (to Oct 1) | 1 | 578 | 578 | 578 |

## Appendix C · Columns in the CSVs

- **`data/own-videos.csv`** has these columns:
  - `url`, `video_id`, `date_pht`, `day_of_week`
  - `views`, `likes`, `comments`, `shares`, `saves`, `duration_s`, `slideshow`
  - `caption`, `hashtags`, `music`, `music_author`, `audio_type`
  - `type`, `subtype`, `artist`, `concert_angle_in_caption`, `tiktok_shop_product_tagged`, `pinned`
  - `views_x_account_median`, `rel_perf_vs_21_neighbours`
  - `likes_per_view`, `saves_per_view`, `shares_per_view`, `comments_per_view`
  - `low_engagement_spike_flag`, `asr_transcript_excerpt` (first 300 characters of TikTok's auto-caption, where available)
- **`data/comments.csv`** has these columns:
  - `video_url`, `video_date`, `video_group` (top15 / tutorial / typical sales)
  - `comment_text`, `likes`, `date` (PHT), `cluster`, `language`
  - `is_shop_comment`, `reply_count`, `liked_by_author`
  - Commenter usernames are left out on purpose, since they aren't needed for the analysis.
- **Scripts that rebuild everything** from the raw JSON live in `data/raw/_work/` (gitignored): `base.py` → `classify.py` → `analyze.py` → `comments_label.py` → `export.py`. A rerun reproduces both CSVs exactly.
