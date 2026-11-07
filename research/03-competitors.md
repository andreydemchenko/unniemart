# 03 · Competitors: which TikTok formats really work in K-pop merch

Date: 2026-10-14. Data: Apify `clockworks~tiktok-scraper`, 1,038 profile videos from 23 accounts, plus 385 discovery results (search, hashtags, profile search).
Processed table: `data/competitor-videos.csv` (one row per video). Raw scrapes: `data/raw/competitors/`.

**How to read this.** Lines marked **Fact** come straight from the scraped numbers. Lines marked **Read** are my interpretation. Treat them as hypotheses to test, not proof.

---

## 0. TL;DR

1. **Fact:** The highest-performing format in the niche is the **lightstick tutorial**. Only 7 of 923 peer videos are tutorials, but their median outlier score is **27x** and 71% of them hit 5x or more. Unnie Mart's own two tutorials scored **371x and 50x**. Its last tutorial was posted in Jan 2025.
2. **Fact:** **Lightstick unboxing, review and comparison videos** come next: 14 videos, median **7.6x**, 57% at 5x or more. Unnie Mart sells lightsticks (BABYMONSTER, Armybomb v4, Caratbong) but has posted none of these. It only posts "WTS/LFB" clips, which score about 1x.
3. **Fact:** Pre-order and GO announcements, and price-list slideshows, are the most crowded seller format: 14% of peer posts, median 1.0x, only 5% at 5x or more. In 7 of 11 accounts, slideshows did worse than that same account's videos. YNA Wrap's GO slideshows have a median of **0.18x**.
4. **Fact:** The PH seller videos that broke out tell a story or show the process. Examples: a GOM's "day in the life", arrival day with boxes from Korea (**151x**), a store's blindfold "grab any album for free" game (**75x**, 2.3M views), a real clearance sale shown as a wall of albums (**167x**), and a hot item "IS HERE" (**74x**).
5. **Fact:** TikTok LIVE is widely used for **selling** (by 6 of 13 PH and SEA sellers). LIVE promo and highlight clips are among the weakest content: median 0.77x and the lowest save rate (0.04%).
6. **Read:** Unnie Mart's best path is to become the **"lightstick help desk" for PH fans, in Taglish**. That means one tutorial, unboxing or comparison video per lightstick it sells, with the GO or price info in the caption and a comment-keyword call to action. Its "Comment 'Enchin'" post (17x) shows that last part works for this audience.

**Apify spend: $5.27 of the $6 cap** (see section 8).

---

## 1. Method (short)

- **Discovery.** I ran 7 search queries, 7 hashtags and 5 profile-search queries, plus 6 more searches for format leaders such as "pack kpop orders with me" and "lightstick app connect tutorial". Web search was used to cross-check well-known PH shops; it found Aling Chulien, N.CAT and CNA, but none of their TikTok handles. N.CAT and CNA did not show up as active TikTok sellers in the discovery data.
- **Scrape.** I pulled the latest 50 videos for each account (45 for 3 of them). Accounts with fewer videos returned all they had. Pinned posts are included and flagged.
- **Outlier score** = views ÷ that account's median views over the scraped videos. 1.0x is an ordinary post for that account. Videos under 3 days old are left out of all rankings.
- **Format tagging.** Each caption was matched against ordered keyword rules, then corrected by hand after I reviewed the cover images of the top 40 outliers and watched 5 videos with the `watch` skill. About 5.6% of videos are still "unclear" (mostly captions that are only hashtags). Rules and overrides are in `automations/score_competitors.py` and `data/raw/competitors/format_overrides.json`.
- **Caveats.**
  - View counts are lifetime totals, so older videos have had more time to collect views.
  - 20 of the top 30 outliers are pinned, because sellers pin their hits. To balance this, section 3b lists the last 12 months only.
  - Several sample sizes are small, so the n is given everywhere.
  - Search results were not geo-locked to PH (no PH proxy was used, to save cost).
  - `#kpopgo` turned out to be dance content ("K-pop go" random play), not group orders.
- **Off-niche.** `@koppashop` (55.1K) came out of profile search as "K-Oppa Shop Manila", but it is a Korean ramyeon and food shop. It stays in the CSV with `in_niche=False` and is left out of all niche numbers. One side fact: its best video is a TikTok LIVE highlight with 649K views.
- **Adjacent.** `@purpledolphinshop` is a PH GOM, but it sells Thai GMMTV merch, not K-pop. I kept it because its selling model (DM orders, feedback hashtag, slideshows) matches Unnie Mart's.

---

## 2. Account table

Posts in the last 90 days count from 2026-07-16. "Median/followers" is median views as a share of followers.

### PH and SEA sellers (13 PH, 3 SEA)

| Account | What it is | Followers | Videos scraped (range) | Median views | Median/ followers | Posts last 90d | Main formats (from scraped videos) |
|---|---|---:|---|---:|---:|---:|---|
| [@poppeshop](https://www.tiktok.com/@poppeshop) | Mall cabinets (Festival Mall, One Ayala) + TikTok LIVE | 96,900 | 50 (Apr–Oct 2026) | 12,850 | 13% | 26 | 6–15s product clips, LIVE promos, POV memes, x.x sale dates |
| [@seoulstop](https://www.tiktok.com/@seoulstop) | Physical stores (Sampaloc, Las Piñas), Shopee, website | 44,900 | 50 (2020–Oct 2026; 51 videos ever) | 30,550 | 68% | 2 | Store events and games, freebies, sales, early album unboxings |
| [@nabishoppe](https://www.tiktok.com/@nabishoppe) | Online + KR pasabuy, website, LIVE; started closing down Sep 2026 | 35,800 | 50 (Aug–Oct 2026) | 1,062 | 3% | 50 | LIVE clips (19), clearance sale, on-hand stock walk-throughs |
| [@ynawrap](https://www.tiktok.com/@ynawrap) | On-hand + PH GO pre-orders, TikTok Shop, carrd forms | 32,800 | 50 (May 2025–Oct 2026) | 4,385 | 13% | 13 | New-arrival box openings (video), GO price slideshows |
| [@chylcartz](https://www.tiktok.com/@chylcartz) | Small photocard seller (Shopee), **inactive since Aug 2023** | 25,800 | 38 (May–Aug 2023) | 10,750 | 42% | 0 | Pack-with-me, hauls |
| [@nelfoever](https://www.tiktok.com/@nelfoever) | Small photocard seller ("carts") | 15,500 | 50 (Apr 2025–Sep 2026) | 5,398 | 35% | 3 | Pack-with-me only |
| [@chulien07](https://www.tiktok.com/@chulien07) | Aling Chulien: store (Malolos) + Shopee + LIVE | 14,400 | 50 (2023–Jun 2026) | 1,224 | 8% | 0 | Sale slideshows, POV memes, LIVE schedules |
| [@forever9ph](https://www.tiktok.com/@forever9ph) | Mall stalls, on-hand/pre-order, LIVE selling, yellow basket | 12,300 | 50 (2022–Oct 2026) | 12,350 | 100% | 8 | LNGSHOT on-hand unboxings, LIVE-selling clips |
| [@joahaeyoph](https://www.tiktok.com/@joahaeyoph) | Physical store (Angeles) + KR pasabuy, DM reservations | 11,700 | 50 (May–Oct 2026) | 3,207 | 27% | 26 | New-arrival slideshows, relatable/POV clips, squishies |
| [@meromiph](https://www.tiktok.com/@meromiph) | Backup account of Meromi store, nightly LIVE selling | 6,826 | 27 (2024–Oct 2025) | 8,559 | 125% | 0 | LIVE announcements, restock clips |
| [@iammist.k](https://www.tiktok.com/@iammist.k) | PH GOM selling via X shop, **inactive since Feb 2024** | 4,651 | 50 (2021–2024) | 633 | 14% | 0 | GO pre-order clips, seller POV memes, day-in-the-life |
| [@recordplanet_ph](https://www.tiktok.com/@recordplanet_ph) | Record Planet mall store (Market! Market!) | 2,521 | 45 (May–Oct 2026) | 1,478 | 59% | 42 | "Now available" arrivals, promo slideshows, POV |
| [@purpledolphinshop](https://www.tiktok.com/@purpledolphinshop) | PH GOM, Thai GMMTV merch (adjacent) | 778 | 50 (Sep–Oct 2026) | 1,001 | 129% | 50 | "WTS on-hand" slideshows, "preorders arrived" clips |
| [@chipopstore](https://www.tiktok.com/@chipopstore) 🇮🇩 | Indonesian photocard/album store, TikTok Shop | 222,200 | 50 (2024–Sep 2026) | 246,650 | 111% | 2 | Organize-freebies/packing ASMR, album unboxing + basket, free-PC promos |
| [@milky_kshop](https://www.tiktok.com/@milky_kshop) 🇮🇩 | Indonesian lightstick shop (Shopee/Tokopedia/TikTok Shop) | 5,939 | 50 (Jun–Oct 2026) | 618 | 10% | 34 | **Lightstick tutorials, unboxing and comparisons**, pack-with-me |
| [@kpopmerch.official](https://www.tiktok.com/@kpopmerch.official) 🇰🇷 | KR Shopee/Lazada store shipping to PH and SEA | 8,885 | 45 (Jun–Oct 2026) | 649 | 7% | 38 | Album-version explainers, unboxings, MD reveals |

### Non-PH creators (for format ideas)

| Account | Country | Followers | Videos scraped | Median views | Posts last 90d | Main formats |
|---|---|---:|---|---:|---:|---|
| [@heyseokjinnie](https://www.tiktok.com/@heyseokjinnie) | NL | 79,300 | 50 (2021–2026) | 2,230 | 21 | Concert diary, lightstick and album unboxings, collection showcases |
| [@0102zyoungwon](https://www.tiktok.com/@0102zyoungwon) | CA | 78,000 | 50 | 118,700 | 15 | Long (3–8 min) photocard packing ASMR |
| [@pinkcardz](https://www.tiktok.com/@pinkcardz) | US | 212,400 | 25 (all; on hiatus since Jul 2024) | 758,500 | 0 | "Pack a sale with me", supply hauls |
| [@lilinanaunboxings](https://www.tiktok.com/@lilinanaunboxings) | PL | 30,200 | 14 (all) | 226,800 | 6 | Two-minute album unboxings |
| [@iamurgrace_](https://www.tiktok.com/@iamurgrace_) | US | 3,811 | 44 | 1,445 | 28 | Lightstick app tutorial, merch DIY, concert clips |

### Client baseline (same method)

| Account | Followers | Videos scraped | Median views | Median/ followers | Posts last 90d | Format mix |
|---|---:|---|---:|---:|---:|---|
| [@unniemart_](https://www.tiktok.com/@unniemart_) | 5,909 | 50 (2023–Oct 2026, 3 pinned) | 608 | 10% | **7** (last post Oct 1) | Concert/fan posts 32%, GO/WTS posts 22%, product clips 12%, lightstick tutorials 2 |

- **Fact:** Unnie Mart's median reach (10% of followers) is in the same band as active PH sellers that rely on routine posts: Poppe 13%, YNA Wrap 13%, Aling Chulien 8%, Nabi 3%. The reach is not unusually bad.
- **Fact:** Unnie Mart's output is low. It posted 7 videos in 90 days, while the active peers posted 26 to 50.

---

## 3. Top outliers

### 3a. Top 30 across the niche

How this list was built:
- Ranked by outlier score, with at most 3 videos per account so one creator cannot fill the list.
- Unnie Mart and the off-niche account are excluded, and so are videos under 3 days old.
- **P** = pinned.
- Hooks come from the caption, the on-screen text on the cover, and (★) the 5 videos I watched.
- "Fit" means how easily Unnie Mart could copy the format.

| # | Account | Video | Views | Score | Format | Hook | Why it likely worked (Read) | Fit |
|---|---|---|---:|---:|---|---|---|---|
| 1 | heyseokjinnie | [link](https://www.tiktok.com/@heyseokjinnie/video/7196785871553613062) P 2023 | 1,500,000 | 673x | Lightstick rating ★ | Text: "rating KPOP LIGHTSTICKS i own" over a shelf of sticks | Each stick gets a star score and 3 short pros on screen. Ranking makes fans argue in the comments, and every fandom waits for its own stick. 13.9K saves | High |
| 2 | heyseokjinnie | [link](https://www.tiktok.com/@heyseokjinnie/video/6945824664140696837) P 2021 | 1,300,000 | 583x | Collection showcase | "my bts korean album collection… i own every version" | Completionist flex plus nostalgia. 4.2K comments | Med |
| 3 | heyseokjinnie | [link](https://www.tiktok.com/@heyseokjinnie/video/7121698753408503046) P 2022 | 955,100 | 428x | POV/humor | "hold me back guys" over a K-pop store's album wall (6s) | A 6-second loop, and impulse buying is relatable. 2.7K comments | High |
| 4 | iamurgrace_ | [link](https://www.tiktok.com/@iamurgrace_/video/7575359100272381214) 2025 | 453,600 | 314x | Lightstick tutorial | Text: "connect your KATSEYE lightstick to the app 💡", posted the day the app launched | Answers a question people were searching for, right when the need was highest. 10K saves | **High** |
| 5 | chylcartz | [link](https://www.tiktok.com/@chylcartz/video/7270512656006581509) P 2023 | 3,100,000 | 288x | Pack-with-me ★ | Voice: "So I got my first order and I'm really nervous". Text: "Pack my first shopee order with me!!" | Underdog milestone. On-screen note "Alot of freebies since she's my first buyer". 80s of calm packing. 25K saves | Med |
| 6 | nabishoppe | [link](https://www.tiktok.com/@nabishoppe/video/7680134582393834770) P 2026 | 177,000 | 167x | Clearance sale ★ | Sticker: "CLEARANCE / PALUGI SALE". Voice: "everything must go… as low as ₱199" | Slow 65s pan across a full wall of albums, so fans scan for their group. Low anchor price. A real reason (the shop was closing). Checkout link and Google Sheet in the comments (344 comments) | Med (only if real) |
| 7 | iammist.k | [link](https://www.tiktok.com/@iammist.k/video/6999215658995076357) P 2021 | 95,400 | 151x | GOM day in the life ★ | "Day in the life of a young K-pop Shop Owner, Ep. 4" | Shows the GO process buyers worry about: drive to the courier warehouse, "We got my 2 boxes from South Korea", shelf set-up, inventory check, packing, "That's all for today". Made by a PH GOM at 4.6K followers | **High** |
| 8 | milky_kshop | [link](https://www.tiktok.com/@milky_kshop/video/7665347321718230293) 2026 | 68,000 | 110x | Lightstick tutorial | "tutorial pasang baterai… lightstick bigbang" (how to fit and remove the batteries) | Solves a real, practical problem. A seller with 5.9K followers | **High** |
| 9 | chulien07 | [link](https://www.tiktok.com/@chulien07/video/7472328026827558151) P 2025 | 128,800 | 105x | POV/humor | Text: "POV: You and your work bestie have an age gap" (2nd-gen stan) | Generational K-pop joke. 1.9K shares, meaning people sent it to friends | High |
| 10 | seoulstop | [link](https://www.tiktok.com/@seoulstop/video/7276848388610460934) P 2023 | 2,300,000 | 75x | Store event game ★ | Voice: "Since last customer namin kayo, ipa-blindfold ka namin… kung ano mahawakan mong album, sa'yo na. For free" | Game, suspense and real reactions, over two rounds. 13K saves, 4.3K shares. The store repeated it in 2025 (55.7K views) | Med-High |
| 11 | recordplanet_ph | [link](https://www.tiktok.com/@recordplanet_ph/video/7638542205786787090) P 2026 | 109,400 | 74x | Hot arrival | "HEY ARMYs! BTS Arirang Vinyl IS HERE" (10s in-store) | A hot comeback item, available first | **High** |
| 12 | iammist.k | [link](https://www.tiktok.com/@iammist.k/video/7235922859707698478) 2023 | 45,000 | 71x | POV/humor | Text: "k-pop fan na walang pera pero nag fill out nang pre-order form" | Buyers roasting themselves about GOs, in Tagalog | **High** |
| 13 | iamurgrace_ | [link](https://www.tiktok.com/@iamurgrace_/video/7413830452856884510) 2024 | 87,600 | 61x | Fan content (not K-pop) | Custom fan flag of a YouTuber | Off-topic for this niche | Low |
| 14 | iammist.k | [link](https://www.tiktok.com/@iammist.k/video/7067040863804804398) P 2022 | 34,400 | 54x | Seller POV | Text: "POV K-pop shop owner seeing a lot of unanswered DMs on a Monday morning" with the Choi San "jebal" sound | A seller-life joke set to a well-known fandom sound | **High** |
| 15 | milky_kshop | [link](https://www.tiktok.com/@milky_kshop/video/7655695478444576007) 2026 | 31,600 | 51x | Lightstick tutorial | "cara connect lightstick boynextdoor ke aplikasinya" | Search-driven how-to | **High** |
| 16 | recordplanet_ph | [link](https://www.tiktok.com/@recordplanet_ph/video/7653786329091788053) P 2026 | 73,000 | 49x | On-hand arrival | "ENGENEs, check this out! Our ONHAND ENHYPEN ALBUMS are here!" | Speaks to the fandom by name and shows every version on a pegboard. 2.2K saves | **High** (Unnie Mart's core fandom) |
| 17 | nabishoppe | [link](https://www.tiktok.com/@nabishoppe/video/7680918392500489492) P 2026 | 48,300 | 46x | Closing-sale letter (slideshow) | "CLOSING SALE / PAUBOS SALE… I've decided to take a little step back" | Personal story plus real scarcity | Low |
| 18 | iamurgrace_ | [link](https://www.tiktok.com/@iamurgrace_/video/7679942877522316575) 2026 | 55,900 | 39x | Concert moment | "I KEEP REWATCHING AND IT MAKES ME LAUGH" (BTS Chicago) | A funny moment from the concert | Med |
| 19 | forever9ph | [link](https://www.tiktok.com/@forever9ph/video/7077458983883246875) P 2022 | 476,700 | 39x | Store location reveal | Text: "AFFORDABLE K-POP MERCH AT FARMERS PLAZA MALL CUBAO!!!" | "Where to buy, near you". 1.6K comments tagging friends | Med |
| 20 | milky_kshop | [link](https://www.tiktok.com/@milky_kshop/video/7661620773408312597) 2026 | 19,300 | 31x | Lightstick unboxing | "unboxing official lightstick IVE ver 2" | Product-detail close-ups | **High** |
| 21 | forever9ph | [link](https://www.tiktok.com/@forever9ph/video/7597794799076347156) 2026 | 320,200 | 26x | First-in-PH unboxing | "[ONHAND] Unboxing LNGSHOT SHOT CALLERS debut album… Onhand & Ready to ship" | Owns a rookie fandom early: 29 of its 2026 videos are about LNGSHOT | **High** (do it for ENHYPEN) |
| 22 | forever9ph | [link](https://www.tiktok.com/@forever9ph/video/7138909071691779355) P 2022 | 314,100 | 25x | Store location reveal | "Your new kpop shop @ MOA. Tag your moots!!" | Location plus a tag call to action | Med |
| 23 | chulien07 | [link](https://www.tiktok.com/@chulien07/video/7347149387518250246) P 2024 | 29,200 | 24x | Seller life | Text: "a day in a life of a kpop seller" (boxes of stock) | Process content again | **High** |
| 24 | seoulstop | [link](https://www.tiktok.com/@seoulstop/video/6996536942980582682) P 2021 | 726,300 | 24x | Volume shot | "thank you 🇵🇭 armys", hundreds of Butter albums stacked | Abundance plus a thank-you to the fandom | Med |
| 25 | chulien07 | [link](https://www.tiktok.com/@chulien07/video/7235493453910658310) P 2023 | 24,800 | 20x | Event freebies | Text: "Exo Sc fancon giveaway" (fan money with members' faces) | Presence at the event, plus freebies | Med-High |
| 26 | ynawrap | [link](https://www.tiktok.com/@ynawrap/video/7544650710470692097) 2025 | 83,200 | 19x | Arrival box opening | "New arrivals ulit hehe di pa listed sa basket" | Raw box opening. "Not listed yet" gives early access | **High** |
| 27 | nabishoppe | [link](https://www.tiktok.com/@nabishoppe/video/7682677552804089108) 2026 | 19,500 | 18x | On-hand walk-through | Text: "Remaining SEVENTEEN ALBUMS". Caption: "For those asking for seventeen albums…" | Answers a demand that was already there | **High** |
| 28 | chipopstore | [link](https://www.tiktok.com/@chipopstore/video/7347706991491632389) P 2024 | 4,300,000 | 17x | Organize freebies/packing ASMR | "organize freebies & packing supplies w/me" | Calm, colourful desk content. 40K saves | Low-Med (saturated) |
| 29 | chipopstore | [link](https://www.tiktok.com/@chipopstore/video/7445181963356458258) P 2024 | 4,100,000 | 17x | Same | "unboxing freebies & organize freebies" | Same | Low-Med |
| 30 | seoulstop | [link](https://www.tiktok.com/@seoulstop/video/6917524347661962497) P 2021 | 496,600 | 16x | Packing process | "this is how we pack albums ♡" | Shows the shop takes care with packing (trust) | Med |

### 3b. Last 12 months only, PH and SEA sellers (top 12)

| Account | Video | Views | Score | Format | Hook |
|---|---|---:|---:|---|---|
| nabishoppe | [link](https://www.tiktok.com/@nabishoppe/video/7680134582393834770) | 177,000 | 167x | Clearance sale | "CLEARANCE / PALUGI SALE", ₱199 |
| milky_kshop | [link](https://www.tiktok.com/@milky_kshop/video/7665347321718230293) | 68,000 | 110x | Lightstick tutorial | Battery fitting, BIGBANG stick |
| recordplanet_ph | [link](https://www.tiktok.com/@recordplanet_ph/video/7638542205786787090) | 109,400 | 74x | Hot arrival | "BTS Arirang Vinyl IS HERE" |
| milky_kshop | [link](https://www.tiktok.com/@milky_kshop/video/7655695478444576007) | 31,600 | 51x | Lightstick tutorial | Connect BOYNEXTDOOR stick to app |
| recordplanet_ph | [link](https://www.tiktok.com/@recordplanet_ph/video/7653786329091788053) | 73,000 | 49x | On-hand arrival | "ENGENEs… ONHAND ENHYPEN ALBUMS are here" |
| nabishoppe | [link](https://www.tiktok.com/@nabishoppe/video/7680918392500489492) | 48,300 | 46x | Closing-sale letter | Owner steps back |
| milky_kshop | [link](https://www.tiktok.com/@milky_kshop/video/7661620773408312597) | 19,300 | 31x | Lightstick unboxing | IVE ver 2 |
| forever9ph | [link](https://www.tiktok.com/@forever9ph/video/7597794799076347156) | 320,200 | 26x | First-in-PH unboxing | LNGSHOT debut album |
| milky_kshop | [link](https://www.tiktok.com/@milky_kshop/video/7664099637128826133) | 13,700 | 22x | Lightstick comparison | "ATEEZ ver 2 vs ver 3" |
| nabishoppe | [link](https://www.tiktok.com/@nabishoppe/video/7682677552804089108) | 19,500 | 18x | On-hand walk-through | "Remaining SEVENTEEN albums" |
| poppeshop | [link](https://www.tiktok.com/@poppeshop/video/7637818613218495764) | 177,200 | 14x | Packing orders | "Thank you for checking out coers 💚" (box of CORTIS orders) |
| poppeshop | [link](https://www.tiktok.com/@poppeshop/video/7655187744821415189) | 154,600 | 12x | POV + LIVE CTA | Text: "pov: seller gave you more kpop freebies than the actual items you bought" |

- **Fact:** 4 of the 12 recent seller breakouts are from one small Indonesian shop (5.9K followers), and all 4 are lightstick tutorials, unboxings or comparisons. Its other 36 videos ("temenin packing yuk", stock clips) have a median of 0.93x.

### 3c. Unnie Mart's own outliers (same method)

| Video | Views | Score | Format |
|---|---:|---:|---|
| "Fate Tour Philippines na ba to?" (P, 2023) | 226,300 | 372x | Concert reaction |
| "Connecting engenebong V2 to the app." (P, 2025) | 225,400 | 371x | Lightstick tutorial. **3,976 saves, 712 shares** |
| "i got to meet heeseung…" (2026) | 55,900 | 92x | Idol moment |
| "Connecting Caratbong V3 to app." (P, 2025) | 30,500 | 50x | Lightstick tutorial |
| "Latest arrival coming through today, ENGENES!" tote bag, price ladder in caption (2026) | 24,800 | 41x | Arrival video |
| "Comment 'Enchin' or DM us to reserve yours." (2026) | 10,300 | 17x | GO with comment-keyword CTA |
| WTS/LFB lightstick and GO posts (several) | 430–1,400 | 0.7–2.3x | Pre-order announcements |

---

## 4. Format patterns, with numbers

The base is 923 peer videos (all in-niche accounts except Unnie Mart, 3 days or older). Outlier medians are relative to each account's own median, so 1.0 means an ordinary post. Save rate = saves ÷ views, as a median.

| Format | Share of peer posts | Median score, sellers (n) | Median score, all (n) | Videos at 5x or more | Save rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Lightstick tutorial (connect app, batteries, add-ons) | 0.8% | 16.8x (5) | **27.3x (7)** | 71% | 0.91% | **Underused, strongest** |
| Lightstick unbox / review / compare / rating | 1.5% | 2.4x (11) | **7.6x (14)** | 57% | 0.46% | **Underused** |
| Collection showcase / rating | 0.5% | (1) | 2.5x (5) | 40% | 0.76% | Underused (creator-led) |
| Store / event visit, games, booth | 2.7% | 1.39x (23) | 1.39x (25) | 28% | 0.32% | Underused, big upside |
| Seller life / behind the scenes | 1.4% | 1.36x (13) | 1.36x (13) | 38% | 0.22% | Underused |
| Arrival / on-hand / restock video | 7.5% | 1.15x (67) | 1.15x (69) | 14% | 0.23% | Solid when the item is hot |
| Sale / promo / giveaway | 6.4% | 1.07x (59) | 1.07x (59) | 15% | 0.15% | Average; real clearance stories spike |
| Pack-with-me / packing / supplies | **21.8%** | 1.09x (129) | 1.04x (201) | 9% | **1.13%** | **Saturated**, big tail, high saves |
| Album / merch unboxing | 8.1% | 0.95x (52) | 1.03x (75) | 13% | 0.57% | Average; first-in-PH unboxings spike |
| Pre-order / GO announcement | **14.0%** | 1.01x (129) | 1.01x (129) | **5%** | 0.22% | **Saturated, rarely breaks out** |
| Generic product clip ("DM to order") | 9.1% | 0.94x (72) | 0.90x (84) | 6% | 0.17% | Saturated |
| POV / humor / relatable | 7.2% | 0.84x (59) | 0.86x (66) | 18% | 0.20% | Hit-or-miss, cheap to make |
| Concert / idol / fan moment | 6.2% | 0.70x (21) | 0.79x (57) | 7% | 0.39% | Hit-or-miss (Unnie Mart's 2 hits sit here) |
| LIVE promo / highlight clip | 4.2% | 0.77x (39) | 0.77x (39) | 8% | **0.04%** | **Weak as content** |

### Other cuts

- **Slideshows vs videos (Fact).** For sellers, slideshows have a median of 0.86x and videos 1.09x.
  - Within accounts, slideshows lost in 7 of 11: Unnie Mart 0.92 vs 1.01, Aling Chulien 0.66 vs 1.85, YNA Wrap **0.22 vs 1.29**, Record Planet 0.79 vs 1.21, Forever9 0.88 vs 1.15, Joahaeyo 0.96 vs 1.07, Purple Dolphin 0.95 vs 1.10.
  - The exceptions are announcement-style slideshows: Nabi's closing letter, and desk-setup photo posts.
- **GO price slideshows (Fact).** YNA Wrap's "Random ₱420 / Set ₱2,870 / DP ₱100 / ETA late Sept" slideshows sit at 0.1–0.3x. Its box-opening videos run 1–19x. Aling Chulien's "DP 50% / DOP 1 week" lists are 0.3–0.4x.
- **LIVE (Fact).** Nabi Shoppe posted 19 LIVE clips, 16 of them captioned "Join our LIVE and get exclusive promotions!". Their median is 0.39x. Poppe's LIVE clips do better (1.5x) when they carry a hook: a POV joke about freebies (12x), or a specific product with a time ("cortis pypd mini ball keyring live later at 3pm", 10.5x).
- **TikTok Shop product tag (Fact, weak signal).** Tagged videos have a median of 1.27x vs 1.0x for untagged ones (n=61). YNA Wrap tags 38% of its videos, Chipop 36%, Forever9 28%, Meromi 22%. Unnie Mart tags 2%.
- **Duration and sound (Fact).** I found no clear duration effect: medians were 1.0 to 1.24x in every bucket from 0–10s up to 90s+. Videos with trending or licensed sounds scored 1.21x vs 1.02x for original sound (n=142 vs 432), a weak signal.
- **Search demand (Fact, discovery data).**
  - The "lightstick app connect tutorial" search returned videos with a **median of 31,600 views from authors with a median of 2,311 followers**.
  - "onhand kpop ph" returned a median of only 1,710 views (authors' median 2,177 followers).
  - The `#lightstick` tag has 2.9B total views. `#kpopunboxing` has 1.4B, `#kpopph` 649M, `#kpopmerchph` 37.8M, `#kpopshopph` 31M and `#onhandph` 4.3M.
  - **Read:** Fans search for help with their lightsticks. Nobody searches for "on-hand" stock lists.

---

## 5. Selling methods and trust tactics

### How the successful sellers sell (Fact, from bios and captions)

| Channel | Who uses it | Notes |
|---|---|---|
| **TikTok Shop / yellow basket** | Chipop (ID), YNA Wrap, Forever9 (separate basket account), Meromi, Nabi, Joahaeyo ("tiktok c/o") | Captions say "di pa listed sa basket", "check out na". Chipop puts "cek keranjang kuning" in every unboxing |
| **TikTok LIVE selling** | Poppe, Nabi (daily in Aug 2026), Meromi (nightly, "3:50 PL UP STOCKS! 4PM live"), Forever9 ("LIVE selling day 3&4… 6 steal for 1 pc"), Aling Chulien (posted schedules), Joahaeyo (LIVE clearance) | Used to sell. Its promo clips do not bring reach (section 4) |
| **Physical store or mall cabinet** | Poppe, Seoul Stop, Forever9, Joahaeyo, Aling Chulien, Record Planet | "📍" location in nearly every caption. Store pick-up, walk-ins, same-day delivery |
| **Shopee / Lazada** | Seoul Stop (COD), Aling Chulien ("Shapi store"), Nabi, chylcartz, milky_kshop, kpopmerch.official | Shopee COD named as a reason to buy: "Order now and pay later via shopee's COD" |
| **DM / comment to reserve** | Purple Dolphin ("DM to order", every post), Joahaeyo, Unnie Mart, Poppe (DP for CORTIS lightstick) | Comment CTAs are rare among peers: 10 of 923 posts. Unnie Mart already uses them in 7 of its 50, and "Comment 'Enchin'" was its best sales post (17x) |
| **Order form / website / sheet** | YNA Wrap and Forever9 (carrd), Nabi (website + Google Sheet), Aling Chulien (carrd), Unnie Mart (bit.ly ENCHIN form) | — |
| **X/Twitter shop** | Mist.K (sold only via X), Purple Dolphin, Joahaeyo | Older GOM model |
| **Payment terms in public** | YNA Wrap (₱100 DP, ETA, "rembal once onhand"), Aling Chulien (DP 50%, DOP), Joahaeyo (MOP GCash/bank, MOD), Unnie Mart (PAYO / DP price ladder) | — |

### Trust and proof tactics seen

| Tactic | Example | Result (Fact) |
|---|---|---|
| "Official / sealed / on-hand" labels | YNA Wrap bio "✅ All Items Are Official", Record Planet, Forever9 | Standard everywhere, no measurable effect |
| Feedback hashtag | Purple Dolphin bio: "REVIEW: #purpledolphinshopfeedback" | — |
| "Pre-orders arrived, thank you for trusting us" | Purple Dolphin | 3.6x (its #3 video). Another of these got 0.8x |
| Sourcing transparency | Forever9: "Secured via proxy (BUSAN OFFLINE) hence the price". "FETA batch" hand-carried, "Sunday na flight ni madam dala ang albums". YNA Wrap: "Arrived at KR address" | 1.0x, 0.9x, 2.1x |
| Delay transparency | Nabi: J&T will not accept parcels because of floods, asks buyers to switch to PAYO/direct so orders are not cancelled | 6.4x |
| Process as proof | Mist.K GOM day in the life (boxes from Korea → packing) | **151x** |
| Packing quality as proof | Seoul Stop "this is how we pack albums" | 16x |
| Calling out bad buyers | YNA Wrap names a blocked buyer (103 comments, 154 shares). Chipop lists buyers who returned parcels | 9.3x; 2.2x at 545K (610–723 comments) |
| "Legit / trusted shop" claim posts | Mist.K "TRUSTED SHOP? LONG DOP ALWAYS?…", Unnie Mart "100% legit", Koppa "Proof of transactions" slideshow | **0.5x, 0.6x, 0.2x** |

- **Read:** Claims of being legit do not travel. Showing the process does: boxes arriving, receipts, packing, being honest about delays.
- **Read:** Calling out buyers drives comments but carries brand risk. It is not recommended for a small GO.

---

## 6. Gaps and opportunities for Unnie Mart, ranked by evidence

Evidence strength: **Strong** means several accounts plus Unnie Mart's own data. **Medium** means 2–3 accounts or a small n. **Weak** means 1 account or a directional signal only.

| # | Gap or opportunity | Evidence | Strength |
|---|---|---|---|
| 1 | **Make lightstick tutorials a weekly series** (connect to app, batteries, add-ons/charms, wristband sync, "why won't it connect"). One for every stick Unnie Mart sells or fans ask about. | Unnie Mart: 2 of 2 tutorials hit (371x, 50x), but none since Jan 2025. Niche: 7 videos, median 27x, 71% at 5x+. milky_kshop (seller, 5.9K followers): 110x, 51x, 17x. Search: tutorial videos get a median of 31.6K views from authors with a median of 2.3K followers. Unnie Mart's tutorial has 3,976 saves (a utility signal). No PH seller in the sample makes these. | **Strong** |
| 2 | **Lightstick unboxing, comparison and rating videos** for the sticks Unnie Mart already sells (BABYMONSTER, Armybomb v4, Caratbong, Engenebong). Examples: "ver 2 vs ver 3", "rating every lightstick we've sold". | 14 videos across 4 accounts, median 7.6x, 57% at 5x+. heyseokjinnie's rating video: 1.5M. milky_kshop: comparison 22x, IVE unboxing 31x. Unnie Mart currently sells these sticks through WTS clips at 0.7–2.3x. | **Strong** |
| 3 | **Move GO and price info out of slideshows and into a video with the price in the caption**: one item, one video, a reveal first, then the price ladder in the caption and a comment-keyword CTA. | GO announcements: 14% of peer posts, median 1.0x, 5% at 5x+. Slideshows lost to videos in 7 of 11 accounts (YNA Wrap 0.22 vs 1.29). Unnie Mart's own tote-bag arrival video with the price ladder in the caption: 41x. "Comment 'Enchin'": 17x. | **Strong** |
| 4 | **"GO arrival day" / day-in-the-life vlogs**: Weverse order screenshot → box from Korea → sorting → packing with names blurred. Run it as a numbered series ("Ep. 1"). | Mist.K (PH GOM, 4.6K followers) 151x. Aling Chulien 24x. YNA Wrap box opening 19x. Seller-life format median 1.36x, 38% at 5x+. Unnie Mart's own "Our box from Korea has arrived" was 8s with no story: 0.7x. | **Medium** |
| 5 | **Hot-arrival and first-in-PH videos for ENHYPEN items**: "ENGENEs, it's here", showing every version or every member. | Record Planet: ENHYPEN on-hand albums 49x, BTS vinyl 74x. Forever9 owned LNGSHOT early (320K unboxing). Unnie Mart's top content is already ENHYPEN (Fate Tour, Engenebong, Heeseung, Enchin). | **Medium** |
| 6 | **Events and concert days as content with a game or a freebie**, for example a "blindfold pick" or "first 10 buyers at the venue" drop. Only with real items; no fake scarcity. | Seoul Stop blindfold game 75x (2.3M), repeated a year later (1.8x). Aling Chulien fancon giveaway 20x. Joahaeyo SVT fan-event booth 1.8x. Unnie Mart's concert reaction is its #1 video (372x). | **Medium** |
| 7 | **Taglish POV jokes about GO life**: no money but filled out the pre-order form, DOP feelings, unanswered DMs, freebies outnumbering the items. | Mist.K 71x and 54x. Aling Chulien 105x. Poppe 12x. The format is hit-or-miss (median 0.86x, 18% at 5x+). Unnie Mart's attempts asked viewers for tips instead of making a joke ("Ang hirap maging content creator. Penge tips?", 0.4x). | **Medium** |
| 8 | **Proof shown as process, not "100% legit" claims**: arrival receipts, "pre-orders arrived, thank you for trusting us", honest delay updates. | Process 151x, delay update 6.4x, "thank you for trusting" 3.6x vs legit-claim posts at 0.2–0.6x. Small n. | **Medium-Weak** |
| 9 | **Tag TikTok Shop products on on-hand item videos.** | Tagged videos 1.27x vs 1.0x (n=61). Peers tag 22–38% of videos, Unnie Mart 2%. Directional only. | **Weak** |
| 10 | **Post more often.** | Unnie Mart: 7 posts in 90 days. Active peers: 26–50. A 50-video sample shows that most posts are around 1x and the hits are rare, so volume buys more lottery tickets. Interpretation only; I measured no direct causal effect. | **Weak** (logic, not data) |

### Formats to avoid or not over-invest in

- **LIVE promo clips** ("Join our LIVE…"): median 0.77x and 0.04% saves. If Unnie Mart tests LIVE selling, treat LIVE as a checkout channel and do not expect reach from the promo clips. **Fact.**
- **Pack-with-me as a main format.** It is 22% of niche posts and dominated by photocard "carts" sellers and ASMR creators. Its median is about 1.0x even though it has a huge tail (3.1M for a "first order" story). Use it only for milestones, such as a 1,000th order or a big ENHYPEN batch. **Read.**
- **Generic concert repost and fan-edit posts.** Unnie Mart has 16 of them, median 0.73x. Its hits in this format were personal moments with a question hook ("Fate Tour Philippines na ba to?"), not reposted news. **Fact plus Read.**

### Things peers do badly that Unnie Mart could own

1. **Lightstick help in Taglish.** Not one PH seller in the sample makes lightstick tutorials. The only seller-made ones are Indonesian. **Fact.**
2. **Clear GO pricing that people actually watch.** Every PH GOM in the sample posts walls of text in slideshows that score 0.1–0.4x. One price-ladder video plus a comment keyword is already proven on Unnie Mart's own account. **Fact plus Read.**
3. **Explaining the GO process for new fans** (what DP, PAYO, DOP and ETA mean, and why it takes weeks). Peers only joke about long DOPs. A collecting-tutorial creator's "what is a group order" explainer (@yoongis_garden) reached 30K views in discovery. **Weak, one data point.**
4. **ENHYPEN specialization.** Forever9's LNGSHOT focus shows that owning one fandom works for a small PH store. **Read.**

---

## 7. Watched videos: notes

| Video | What's in it |
|---|---|
| [nabishoppe clearance](https://www.tiktok.com/@nabishoppe/video/7680134582393834770) | 65s. A single slow pan along floor-to-ceiling album shelves. A fixed pink sticker reads "CLEARANCE / PALUGI SALE". Taglish voice-over: "everything must go… as low as ₱199… help us maubos yung stocks para makapag-restock". Photocards ₱100, random member, boy or girl group only. The checkout site and Google Sheet links are in the comments. PAYO/direct orders only. No face. |
| [chylcartz first order](https://www.tiktok.com/@chylcartz/video/7270512656006581509) | 83s. Opens on the voice "So I got my first order and I'm really nervous". Hands only, at a pink desk. Text overlay: "Alot of freebies since she's my first buyer". Toploader, deco, sleeves, pink bubble mailer. Calm sounds, trending sped-up audio. |
| [iammist.k day in the life](https://www.tiktok.com/@iammist.k/video/6999215658995076357) | 59s, text overlays only, music bed. In order: "Otw to the courier's warehouse" → "Ofc, I need a rice meal" → "We got my 2 boxes from South Korea" (balikbayan boxes loaded into the car) → "organize my new shelf" → "organized the albums and checked inventory" → "Started packing right away to ship orders" → "That's all for today!" |
| [seoulstop blindfold](https://www.tiktok.com/@seoulstop/video/7276848388610460934) | 129s. "Since you're our last customer, we'll blindfold you; whatever album you touch is yours, for free." Staff guide each customer by the hand ("hold my hand"). The crowd teases them ("Final na ba yan, ate?"), then the blindfold comes off for the reveal. Two customers. Grand opening in Lacson. |
| [heyseokjinnie rating lightsticks](https://www.tiktok.com/@heyseokjinnie/video/7196785871553613062) | 37s. Opens on a shelf of lightsticks with the title "rating KPOP LIGHTSTICKS i own". Each stick is held to camera with its name, 2–3 bullet pros ("pretty holo, v2 is superior") and a star rating (BLACKPINK JP 4/5, Caratbong v2 5/5, Moabong "mine won't turn on anymore??"). K-pop audio. |

---

## 8. Apify spend (actual, read from each run's `usageTotalUsd`)

| Run | Run ID | Token | Items | USD |
|---|---|---|---:|---:|
| Search: 7 discovery queries ×20 | wIqUXvOzPPvAUm5WT | #6 | 140 | 0.519 |
| Hashtags: 7 ×15 | aQMAdjvja4s2LixJ6 | #7 | 105 | 0.390 |
| Profile search: 5 queries ×10 | LxJlImQPnE1Pv7Vba | #6 | 50 | 0.186 |
| Search: 6 format-leader queries ×15 | cbBMXSuMNmohGKw46 | #7 | 90 | 0.334 |
| Profiles A (10 accounts ×50) | ZEWeE8ATwqW52m4fa | #6 | 488 | 1.807 |
| Profiles B (10 accounts ×50, incl. @unniemart_) | epEIw6jI0UXYCAG55 | #7 | 433 | 1.603 |
| Profiles C (3 accounts ×45) | 18k576XRNGNwXkAP3 | #7 | 117 | 0.434 |
| **Total** | | | **1,423** | **$5.272** |

- Rate: about $0.0037 per result (FREE tier) plus $0.001 per run start. Video, cover and transcript add-ons were off.
- One extra start attempt was rejected before it ran (HTTP 400, the max-charge value was below the actor minimum) and cost nothing.
- Token #6 is now at $3.13 of $10 for the month, token #7 at $3.32 of $10. Token #2 was not used.
- Cover images for the top 40 were fetched directly from TikTok's CDN, outside Apify, at no cost. The 5 watched videos used yt-dlp plus Groq Whisper through the `watch` skill.

---

## 9. Open questions

- I did not test whether **TikTok LIVE drives sales** for peers. View data cannot show conversion. Worth a 2-week test if the owner wants to.
- How fast Unnie Mart's tutorial views accumulate over time is unknown (one snapshot only). A re-scrape in 30 days would show whether tutorials keep growing as search content.
- **N.CAT** and **CNA Philippines** (large PH chains named in web sources) did not show up as active TikTok accounts in discovery, so they are not in this set.
