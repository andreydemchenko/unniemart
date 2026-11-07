# 02 · Video breakdown: why some @unniemart_ videos work and most don't

Date: 2026-10-14. Account: TikTok [@unniemart_](https://www.tiktok.com/@unniemart_) ("Unnie Mart 2"), 5,909 followers, 396 videos, 135.1K total likes (Apify `authorMeta`, 2026-10-14).

**Status: research. Nothing here is posted or sent.**

---

## 1. Short answer

1. **The hits give a stranger a reason to watch that has nothing to do with buying.** They teach something (how to connect a lightstick to the app), let the viewer feel something (a fan on a video call with Heeseung), or show something big (a wall of 100+ lightstick boxes). The flops only give a reason to someone who is already shopping: a price, a DP schedule, "DM or comment".
2. **The hits show the real thing in the first frame and pay it off within 0 to 4 seconds.** The idol is on screen at 0s (H5) or 4s (H1). The lightstick lights up at 1.3s (H2). The wall of stock fills the screen from frame 1 (H4). The flops open on the seller's face, a stock render, a text wall or a white slide, and show the actual product late, small, or never.
3. **The hits barely talk.** None of the top six has a confirmed presenter voice. TikTok text-to-speech reads the steps (H1, H2, H6), music plays (H4), or the idol's own voice carries it (H5). H3 shows a face, but only its "Pink Venom" music track could be retrieved. The three recent talking-head videos I watched (L1, L3, L4) sit at 470 to 629 views. The one recent talking head that broke out (M1, 10.3K) opened with **news**, not a price.
4. **The cleanest test in the data:** M1 and L1 have the same presenter, the same concrete wall, the same caption style and the same sticker editing. M1 leads with "Engene, stop ka muna dyan. Enchin official merch is finally here!" and asks people to comment a keyword: **10,300 views, 33 comments.** L1 leads with a stock render, then "P2,750" over her head: **629 views, 2 comments.**
5. **This is an account-level slide, not one bad format.** All 18 of the 2022-2023 videos in the "popular" scrape got 13.7K to 226K views. The 75 videos posted from Oct 2025 to Oct 2026 have a **median of 612 views**: 48 of the 75 are under 700, and only 4 reached 5K or more.
6. **Three flags to check with the owner before acting:** (a) the last 4 posts (since 2026-09-15) were created from **NL**, not PH; (b) M2 (24.8K views, 16 likes, 0 shares) looks paid, not organic; (c) H5 captions the Heeseung call as "i got to meet heeseung". Confirm it is the owner's own call before reusing it.

---

## 2. Data and method

| Source | What | Where |
|---|---|---|
| Apify `clockworks~tiktok-scraper`, 2 calls, token #5 | 20 "popular" (sorted by likes, not views) + 30 "latest" videos with stats, captions, music. Cost about $0.19 | `data/raw/tiktok-popular-2026-10-14.json`, `data/raw/tiktok-latest-2026-10-14.json` |
| yt-dlp profile listing (free, worked once, then blocked) | 75 most recent videos (2025-10-07 to 2026-10-01), views + caption | `data/raw/tiktok-ytdlp-profile-first80-2026-10-14.tsv` |
| TikTok page JSON (free) | For 95 videos: on-screen sticker text, music title and whether it's original, `locationCreated`, duration, image-post flag | `data/raw/tiktok-page-meta-all-2026-10-14.json` |
| `watch` skill (yt-dlp + ffmpeg + Groq Whisper) | 12 videos downloaded; frames at about 1 fps, plus 8 frames in the first 3 s; ffmpeg scene-cut detection (threshold 0.30) | `data/raw/videos/<slug>/` (frames, `sheet_*.jpg`, `pacing.json`, transcripts) |
| Covers / slide images | For 3 posts yt-dlp could only fetch as audio when logged out (H3, M3, L6) | `data/raw/videos/<slug>/stills/`, `data/raw/videos/era2022-covers/` |

**Limits**
- **No watch-time or retention data.** Only TikTok Studio on the owner's phone has it. That data would confirm or kill most of the interpretations below (see section 12).
- View counts are as of 2026-10-14. The 2022-2023 hits ran in a different TikTok era, when the account was new. Format is not the only variable.
- H3 and M3 (video) and L6 (slideshow): judged from the cover or slides, the audio, and metadata only.
- Transcripts come from Whisper. For H1 and H5 I forced English, because auto-detect returned Indonesian for H5. Text-to-speech in H1 is inferred: the 0 to 3 s audio matches the sticker text.
- Ratios on videos under 1,000 views rest on single-digit counts. Treat them as noise.

---

## 3. Account context (facts)

| Period | Videos seen | Views |
|---|---|---|
| 2022-09 to 2022-12 | 11 in "popular" | 13.7K to 89.2K each. Almost all use trending sounds (BLACKPINK "Pink Venom" ×6) and lead with installment: "100 pesos DP", "Pwede hulugan", "Saan aabot 100 pesos mo?" |
| 2023-01 to 2023-10 | 7 in "popular" | 27.2K to 226.3K. Stock walls, Fate Tour reaction, a reply-to-comment installment explainer |
| 2025-01 | 2 connect tutorials (pinned) | 30.5K and 225.4K |
| 2025-02 to 2025-10-06 | **not in my data** (the listing was cut off) | unknown |
| 2025-10-07 to 2026-10-01 | 75 | median 612, mean 2,147 (pulled up by 4 outliers: 55.9K, 24.8K, 11.9K, 10.3K) |

- In the latest 27 non-pinned posts: 9 use the Facebook-style "WTS | LFB | ... [PH GO]" caption wall, and 5 are photo slideshows. Median like rate is 1.9%.
- In late April and May 2026 the account tried English "fan account" posts ("blind karaoke was a mistake", "these little guys are giving vampire overlords", "okay engenes we need to settle this"). They got 307 to 517 views each. Only the Heeseung call (55.9K) broke out.
- **Location:** `locationCreated` is PH for every post up to 2026-08-28 and **NL** for all 4 posts since 2026-09-15 (416, 896, 1,156, 578 views). Those numbers match the PH baseline just before, so NL isn't proven to be the cause. But TikTok seeds new posts to viewers in the posting region, so it's a risk for a PH-only shop.

---

## 4. The 15 videos

Links: `https://www.tiktok.com/@unniemart_/video/<id>`

| # | Group | Date | ID | What | Views | Likes % | Comments % | Shares % | Saves % |
|---|---|---|---|---|---|---|---|---|---|
| H1 | Top | 2023-07-27 | 7260516146452139269 | Fate Tour PH? + Heeseung video call | 226,300 | 21.2 | 0.16 | 0.69 | 2.17 |
| H2 | Top | 2025-01-25 | 7463827377362062610 | Engenebong V2 app-connect tutorial | 225,400 | 5.7 | 0.06 | 0.32 | 1.76 |
| H3 | Top | 2022-09-28 | 7148315872703122714 | "Pwede hulugan" (green-screen, stock) | 89,200 | 8.1 | **1.13** | 0.15 | 1.05 |
| H4 | Top | 2023-10-05 | 7286352737850199301 | 6 s pan over wall of Caratbong boxes | 71,600 | 5.8 | 0.45 | 0.60 | 1.75 |
| H5 | Top | 2026-04-30 | 7634520116150963476 | "i got to meet heeseung" (same call) | 55,900 | 6.2 | 0.03 | 0.10 | 0.57 |
| H6 | Top | 2025-01-14 | 7459643459536817416 | Caratbong V3 app-connect tutorial | 30,500 | 1.2 | 0.03 | 0.19 | 0.65 |
| M1 | Middle | 2026-05-12 | 7639031726462733586 | Enchin news + "comment Enchin" | 10,300 | 0.9 | 0.32 | 0.10 | 0.20 |
| M2 | Middle | 2026-06-15 | 7651506705339059464 | Walk the Line tote, modelled | 24,800 | **0.06** | 0.00 | 0.00 | 0.01 |
| M3 | Middle | 2025-11-14 | 7572490701754125576 | "11.11 Sale" over Caratbong stock | 11,900 | 2.1 | 0.03 | 0.09 | 0.26 |
| L1 | Low | 2026-06-28 | 7656394317807783176 | BABYMONSTER lightstick, talking head, price | 629 | 2.5 | 0.32 | 0.32 | 0.16 |
| L2 | Low | 2026-09-15 | 7685730268354825479 | "Box from Korea arrived" (Enchin) | 416 | 5.5 | 0.24 | 0 | 0 |
| L3 | Low | 2026-10-01 | 7691614144771951890 | "Sino wala pang bag?" Armybomb bag pitch | 578 | 1.0 | 0 | 0.17 | 0.17 |
| L4 | Low | 2026-05-20 | 7641988579924708615 | 114 s Enchin character profiles | 470 | 3.4 | 0.43 | 0.21 | 0.43 |
| L5 | Low | 2026-05-16 | 7640352064471715080 | Off-niche "200 views → 2 million" meme | 271 | 3.3 | 0 | 0 | 0 |
| L6 | Low | 2026-07-30 | 7668299364846062866 | Armybomb V4 slideshow (FB screenshot + price table) | 441 | 2.0 | 0.23 | 0 | 0 |

Selection: the top 6 are the highest-view videos chosen for format variety (both tutorials, the concert/idol videos, a 2022 installment hook, a stock wall). The middle 3 sit between 10K and 25K. The 6 low performers are from the latest 30, covering the common types: talking-head sales pitch, arrival clip, long explainer, off-niche trend, slideshow caption wall.

---

## 5. The first 3 seconds (what makes someone stop or swipe)

| # | 0 s visual | On-screen text | Audio 0 to 3 s | Payoff arrives |
|---|---|---|---|---|
| H1 | Official ENHYPEN "FATE" world tour poster, static | "Fate tour Philippines na ba to Heeseung? 😱" | Voice reads the sticker (Whisper: "Fate Tour Philippines Nor Bar Tahisi", likely TikTok text-to-speech), then music | **4.0 s**: cut to Heeseung on a live video call |
| H2 | Top-down: hand holds unlit ENHYPEN lightstick V2, phone shows ENHYPEN app (Concert / Self mode), photocards behind | "How to connect Engenebong V2 to app" (top) + 4-step list (small, bottom-right) | Text-to-speech: "First, long press left button to open the light stick." | **1.3 s**: lightstick switches on |
| H3 | Presenter's face (green screen) in front of a stack of ~15 ENHYPEN lightstick boxes (cover) | "Pwede hulugan 😁" (TikTok classic box) | BLACKPINK "Pink Venom" (only the music track was retrievable; voice unknown) | 0 s: offer + stock in one frame |
| H4 | Wall of 100+ boxed Caratbong V3, floor to ceiling | "Onhand stocks / Open for installment" | K-pop song (user sound), no voice | 0 s: the volume *is* the hook |
| H5 | Heeseung full screen, mid-sentence; fan in small corner window | none visible | Call audio: "yeah she loves you very much... where are you from?" "I'm from the Philippines" | 0 s |
| H6 | Hand holds unlit Caratbong V3, phone with SEVENTEEN app | Full title + 3-step block over the middle of the frame (thin serif, no background) | Text-to-speech: "How to connect Caratbong V3 to app? 1. Turn on the lightstick." | **2.5 s**: switches on |
| M1 | Official "ENCHIN Official Character POP-UP" poster, zooming | none for 1.2 s, then "Engene stop ka muna diyan" | Own voice: "Engene, stop ka muna dyan. Enchin official merch is finally here!" | 1.2 s: presenter waves; 2 s: "finally here" |
| M2 | Woman modelling the tote by a wooden door | none visible (checked at 4 fps) | GOT7 "A" | 0 s product, worn |
| M3 | Wall of ~40 bubble-wrapped Caratbong boxes + 7 upright boxes (cover) | "11.11 Sale" (TikTok classic) | Music only | 0 s |
| L1 | Official BABYMONSTER lightstick **render** (stock image) | none | Own voice: "Baby Monster Lightstick for only 2,750 pesos." | 2.0 s: cut to face + "P2,750" sticker |
| L2 | Blurry close-up of plush in plastic bags on a floor | "PH Ar…" typing in, "PH Arrivals 09/15/2026" (gone after ~2.2 s) | Dua Lipa "Training Season (Live)" | none; stays blurry |
| L3 | Presenter at home, low camera, ceiling visible | "CHECK OUT THIS BAG! ✨" + one-word captions "SUPER", "WITTY" | "…super witty ng bag. Hi, Army. Hear me out because this might change your life." | **12.6 s**: bag appears as a 1.4 s cut-out sticker |
| L4 | Presenter smiling at the camera | "Enchin Characters" typing in | Own voice: "Introducing your Enchin characters!" | 2.5 s: white screen with a pink "1" |
| L5 | Hand smearing across the lens, face behind | "Pov: Me as if my 200 views will magically turn to 2 million views" | Trend audio | none (no product) |
| L6 | Screenshot of the shop's own Facebook post (wall of text) | the whole caption wall | BTS "2.0" | slide 2: official stock photo |

---

## 6. Format at a glance

| # | Len | Who's on screen | Voice / sound | Language | Text style | Cuts (scene >0.30) | Product shown how | CTA in video | Angle |
|---|---|---|---|---|---|---|---|---|---|
| H1 | 24 s | Idol via screen recording (+ fan in corner) | TTS hook + user-uploaded "cupid twin version" sound; no call dialogue in the transcript | Taglish hook, English subtitles | TikTok default white text with outline; 3 short subtitle stickers | 1 | none | none | excited, fan joy, topical speculation |
| H2 | 39 s | Hands only, top-down | TTS reads steps + song (user sound "Some") | English | Serif text, semi-transparent white boxes | 0 (one take) | Real item in hand, lit, colours cycling every 2-3 s | none | helpful |
| H3 | 45 s | Face (green screen) over stock | Trending "Pink Venom" (voice unknown) | Tagalog | TikTok classic (white box, cyan/red offset) | n/a | Stock pile behind her | implicit ("pwede hulugan") | offer, affordability |
| H4 | 6 s | Camera pan, no person | K-pop song (user sound) | English text, Korean song | TikTok default white box | 0 | 100+ real boxes | "Open for installment" | proof, abundance |
| H5 | 21 s | Idol via screen recording | Original call audio (English) | English | none visible | 1 | none | none | fan joy |
| H6 | 43 s | Hands only | TTS + user sound "magnetic pluggnb remix" | English | Thin serif, no background, covers mid-frame | 12 (light flashes) | Real item, lit, colours cycling | none | helpful |
| M1 | 62 s | Presenter face, outdoor wall | Own voice | Taglish | Lower-third captions + animated stickers (date, bell, PRE-ORDER, "ENCHIN" keyword) | 3 | Official photo grid (12-14 s) | **"comment Enchin below or DM me"** | news, helpful-service |
| M2 | 18 s | Model, full body | GOT7 "A" | none | none | 0 | Worn, then filled with a cap | none | aspirational |
| M3 | 10 s | Stock photo/clip | Music (only track retrievable) | English | TikTok classic | n/a | Real stock wall | "11.11 Sale" | deal |
| L1 | 23 s | Render, then presenter face | Own voice | Taglish | Word-by-word red captions + price sticker | 4 | Official render 0-1.8 s; photocard overlay | "Huwag nang papalampasin... order na kayo" | sales pitch |
| L2 | 9 s | Handheld, blurry | Dua Lipa (trending) | English | Pink neon typewriter text | 0 | Real but blurry, bagged | none (caption: "dm us") | announcement |
| L3 | 42 s | Presenter face, indoor | Own voice | Taglish | One-word yellow captions; price card at 29 s | 2 + logo card | 1.4 s cut-out PNG | "Limited stock lang to, kaya order now! DM or comment!" + 1.4 s logo end card | sales pitch |
| L4 | 114 s | Face 2.4 s, then white slides | Own voice over slides | Taglish voice, English cards | Typewriter text on white | 6 | Official character cards | none in video; caption says "pre order closing in few hours" | info |
| L5 | 11 s | Selfie | Trend audio | English | TikTok default small white | 1 | none | none | relatable meme |
| L6 | slides | none | BTS "2.0" | English | Facebook screenshot + spreadsheet | n/a | Official stock photo + price table | Order form link (caption) | sales |

---

## 7. Beat-by-beat notes

### H1 · Fate Tour reaction (226.3K, 24 s)
- **0.0-4.0** Official FATE tour group poster (static) with "Fate tour Philippines na ba to Heeseung? 😱". The voice at 0-3 s reads the sticker.
- **4.0** Cut to a Weverse Shop video-call screen recording: Heeseung in a white tux jacket, the fan in a corner window labelled "Summer (夏)".
- **5-6** Subtitle "Btw, where are you from?" **11-12** "I wanna go there soon". **16-17** "As soon as possible".
- **18-20** Big smiles. The fan laughs in the corner window.
- **21-23** Heeseung waves both hands, then makes heart hands. The video loops back to the poster.
- Caption: "Fate Tour Philippines na ba to? #fatetour #fatetourenhypen #darkblood #enhypen #fyp".
- Why it travels (interpretation): an idol saying he wants to come to the Philippines "as soon as possible" is news for every PH ENGENE, and the hook is a question fans want to argue about. It has the highest like rate in the whole set (21.2%) and the most shares (1,569).

### H5 · "i got to meet heeseung" (55.9K, 21 s)
- **Same call footage as H1**, posted 33 months later, with no intro, no visible text and the original call audio.
- **0-12** "she loves you very much / where are you from / I'm from the Philippines / when will you come back next / as soon as possible".
- **15-19** Waves, heart hands. **~19.5** Staff: "okay hi miss, we need to move on to the next", "bye bye". **19.9-21.2** The call ends: black screen with an avatar icon, the fan waving alone.
- Caption: English, lowercase, emotional ("…and i'm not okay 🥺 some moments you just keep forever 🌹"), posted at the start of ENHYPEN's "Blood Saga" era.
- Fact: the same asset hit twice (226K, 56K). Interpretation: the asset carries itself. The 2023 version added a topical question hook and got 3.4x the likes per view.

### H2 · Engenebong V2 connect (225.4K, 39 s)
- **0.0** Unlit lightstick + phone on the ENHYPEN app home; title at the top edge (the first word is partly cut off); step list bottom-right; TTS starts step 1.
- **1.3** Lightstick switches on (white/lavender burst).
- **2.6-6.4** Taps Self mode, "yes" popup, pairing screen. TTS step 2 at 4 s, step 3 at 8 s.
- **10-12** Long-presses both buttons; it connects and turns blue.
- **14** TTS: "You may now change light effects, brightness, and color."
- **15-38** Colour demo: red, red-orange, pink, purple, magenta, off, pink, off, magenta (other hand waves through), white-blue, purple. A new colour every 2-3 s.
- Single take, hands only, no cuts. Caption: "Connecting engenebong V2 to the app." (no hashtags; reads like a search query).
- Note: the step list sits bottom-right, where TikTok's like/comment buttons usually cover it. The video still hit, so the TTS and the visual did the teaching.

### H6 · Caratbong V3 connect (30.5K, 43 s)
- Same template as H2, posted 11 days earlier.
- **0.0** Unlit Caratbong + SEVENTEEN app. The whole step block sits over the middle of the frame in thin white serif with no background, hard to read on the light parts. TTS reads the title and step 1.
- **2.5** Lights on. **4-7** App steps. **11.5** Connected (blue). **14-42** Colour demo: red, pink, off, purple, white, red, off, white, blue, teal, blue.
- Difference from H2 (observed): payoff at 2.5 s vs 1.3 s; text covers the product vs sitting in a corner; like rate 1.2% vs 5.7%; saves 0.65% vs 1.76%. **Not isolated:** product and fandom differ too, and I don't have the launch date of either lightstick version (unverified).

### H3 · "Pwede hulugan" (89.2K, 45 s, cover only)
- Cover: the presenter's face cut out over a photo of stacked ENHYPEN lightstick boxes. Sticker: "Pwede hulugan 😁" (installment is possible).
- Audio: "Pink Venom" (only the music track was retrievable, so a voice-over can't be ruled out). 1,006 comments: the highest comment rate in the set (1.13%). Interpretation: a short, affordable-access promise makes people ask "magkano?" and "paano?" in the comments.
- Same era, same look (covers in `data/raw/videos/era2022-covers/sheet.jpg`): "For Installment Enhypen SG2023, 100 Dp 😱" (43.3K), "Pano ba yung installment?" (23.9K), "MOABONG FOR INSTALLMENT" (15.8K), "Sabi ko na nga ba" over a Weverse "SOLD OUT" screenshot (42.9K), "OFFICIAL, SEALED AND ONHAND" over stock (45.2K).

### H4 · New arrival Caratbong (71.6K, 6 s)
- **0.0-6.2** One handheld pan across a floor-to-ceiling wall of pink and blue Caratbong V3 boxes (100+). "Onhand stocks / Open for installment" fixed at the top. K-pop song, no voice. Loops.
- Caption has the order form link. 1,256 saves (1.75%) and 430 shares on a 6-second clip.
- Interpretation: the volume proves "real seller, real stock" in one look, and 6 s loops make rewatches cheap.

### M1 · Enchin "comment to reserve" (10.3K, 62 s)
- **0.0-1.2** Official Enchin pop-up poster. Audio: "Engene, stop ka muna dyan."
- **1.2** Presenter waves at the camera. **2-5** "Enchin official merch is finally here!", poster floating above her head.
- **6-11** "HYBE just dropped the official concept photos… ang cute-cute nila, super!"
- **12.3-14.4** Cut to a 2×3 grid of official product photos. **16-21** "based sa iyong favorite ENHYPEN member", 6 member photos overlaid.
- **22.6** Bell sticker. **24.6** "May 21" burst sticker. **26.7** "9:30am dito sa Philippines". **34.9** "May 21-31" (offline, Korea).
- **36.9-45** "As your favorite K-pop seller… sa mga hindi kayang mag-order sa Weverse Shop on their own. No stress, no hassle, ako nang bahala sa inyo."
- **47-51** "comment 'Enchin' below or DM me para makapagpa-reserve ng slot" with an "ENCHIN" keyword sticker and a DM icon.
- **53-60** "Mark your calendars, Engenes", calendar sticker.
- 33 comments (the flops get 0 to 2). It's the same person, wall and editing as L1. What changed is the angle: news + dates + "I'll handle it for you" + a keyword CTA, vs a price pitch.

### M2 · Walk the Line tote (24.8K, 18 s)
- **0-10** Woman poses with the tote by a wooden door, turning to show the "WALK THE LINE" straps. **10-17** Opens it and stuffs a cap inside (shows capacity). No text, no voice.
- 24.8K views but 16 likes, 1 comment, 0 shares, 2 saves. That's a 0.06% like rate, against 5-21% on the organic hits. Interpretation: almost certainly paid (Promote) or non-target distribution. **Don't copy this as a "winning format" until the owner confirms whether it was promoted.**

### M3 · "11.11 Sale" (11.9K, 10 s, cover only)
- Cover: wall of bubble-wrapped Caratbong boxes + 7 upright boxes on a fur rug, "11.11 Sale" in TikTok classic style. Music only.
- Caption: "Ready to scream, shine, and support SEVENTEEN! 💎✨". Posted in a run of SEVENTEEN tour-tagged posts (#SVT_TOUR_NEW_ASIA, #NEW_BULACAN) that also did better than baseline: 2,211 / 2,766 / 3,862 / 2,038. The concert date is not verified here.
- Reads as H4's stock-wall format plus a date hook.

### L1 · BABYMONSTER lightstick pitch (629, 23 s)
- **0.0-1.8** Official product render (black background, red box). Voice: "Baby Monster Lightstick for only 2,750 pesos."
- **2.0-3.0** Presenter, concrete wall, "P2,750" sticker over her head.
- **4-9** "Kung naghahanap ka ng lightstick na aabot sa concert this September, ito na ang chance…"
- **9.9-11** "For only 300 pesos down payment pwede ka nang maka-avail…" The ₱300 entry price arrives at 9.9 s.
- **14.8-16.8** "SPECIAL GIFT photocard" overlay. **17-20** "Huwag nang papalampasin itong offer… order na kayo."
- **20.7-22.7** Unnie Mart logo end card (2 s of nothing).
- The lightstick is never shown for real, never lit, never held.
- This is at least the 5th post of the same BABYMONSTER lightstick offer: 1,186 (May 16), 629 (Jun 28), 598 (Jul 2, slideshow), 430 (Aug 23), 446 (Aug 28).

### L2 · "Our box from Korea has arrived" (416, 9 s)
- **0-2.2** Blurry handheld over plastic-bagged Enchin plush, "PH Arrivals 09/15/2026" typing in. **2.2-9** No text; the camera drifts over bagged plush, still soft-focus.
- No offer, no price and no person in the video. The caption carries everything ("dm us to inquire"). Created from NL.
- Compared with H4/M3: same idea (arrival/stock), but no clean wide shot, no sense of scale, products still in bags, no offer on screen.

### L3 · "Sino wala pang bag?" (578, 42 s)
- **0-3** "CHECK OUT THIS BAG! ✨", but no bag. "Hi, Army. Hear me out because this might change your life."
- **6-12** "Nakabili na ba lahat ng Army Bomb? … hindi lahat merong Army Bomb bag."
- **12.6-14.0** The bag appears as a cut-out PNG sticker ("IT'S NOT A BOMB" duffel) for 1.4 s. That's the only time it's shown.
- **20-28** "straight to your address… cash… installment… shipping 1 to 2 weeks". **29.4-30.8** Price card "PAYO 3500 / Oct 31 3600 / Nov 30 3700".
- **36-40** "Limited stock lang to, kaya order now! DM or comment!", pointing down. **40.6** Logo end card.
- One-word yellow captions throughout. Created from NL.

### L4 · Enchin character profiles (470, 114 s)
- **0-2.4** Presenter smiles, "Introducing your Enchin characters!", while "Enchin Characters" types in. **2.5** White screen, big pink "1".
- **3.8-110** Six characters, about 17 s each: two official cards plus Personality / Likes / Dislikes / Charming point / Motto typed line by line on white, with her voiceover tying each to a member ("Very Jake talaga"). Two member reaction clips are overlaid (1:08, 1:46).
- **110-114** Grid of all 6.
- Caption: "pre order closing in few hours. habol na!!!" The video never mentions the pre-order. The member-matching idea is fan-friendly. The packaging (white slides, typing, 114 s, no hook) is the problem.

### L5 · "200 views → 2 million" (271, 11 s)
- A selfie trend meme with no K-pop or product. The lowest-viewed video in the set. It tells TikTok the account is something other than a K-pop merch shop.

### L6 · BTS Armybomb V4 slideshow (441)
- Slide 1: a screenshot of the shop's Facebook post, "13m" timestamp visible, all text. Slide 2: official stock photo. Slide 3: a landscape price spreadsheet (4944×2060). On a vertical phone screen it shows as a thin, unreadable strip.
- Group-order jargon throughout: WTS, LFB, PH GO, DOP, PF, ISF, BOXSHARE, NETA.

---

## 8. Hits vs flops

### 8.1 What I observed (facts)

| Attribute | Top 6 | Low 6 | Evidence |
|---|---|---|---|
| What's in frame at 0 s | The idol (H1 poster, H5) or the real product (H2, H4, H6, H3 stock) | Seller's face (L3, L4, L5), stock render (L1), blur (L2), FB screenshot (L6) | Section 5 |
| Time to first visual payoff | 0 to 4 s | 2.5 s to never; L3's product at 12.6 s for 1.4 s | H2 1.3 s, H6 2.5 s, H1 4.0 s |
| Real product physically shown | 5 of 6 (H1/H5 show the idol instead) | 1 of 6 (L2, blurry) | L1 render, L3 cut-out, L4 cards, L6 stock photo |
| Presenter pitching to camera | 0 of 6 confirmed (H3 shows a face; its voice is unknown) | 3 of 6 (L1, L3, L4 voice) | Transcripts |
| Voice | TTS (H1, H2, H6), music only (H4; H3 unknown), idol audio (H5) | Own voice (L1, L3, L4), music (L2, L6), trend audio (L5) | |
| Price in the video | 0 of 6 | L1 (2 s), L3 (29 s), L6 (slide 3) | |
| Hard CTA in the video | 0 of 6 ("Open for installment" in H4 is the closest) | L1, L3 explicit; L2/L6 in caption | |
| Caption | One line, plain or a question ("Connecting engenebong V2 to the app.", "Fate Tour Philippines na ba to?") | 5 of 6 are a pitch or meme; L1 and L6 are FB-style walls with jargon | |
| Length | 6 to 45 s | 9 to 114 s | Overlaps; not a separator except L4 |
| Cuts | 0 to 1 hard cuts (H6's 12 are light flashes) | 0 to 6 | Hits are single takes; motion within the shot (light colours, idol gestures, pan) does the pacing |
| Trending / borrowed sound | 5 of 6 | 3 of 6 (L2, L5, L6) | Sound alone didn't rescue L2, L5, L6 |
| Saves per view | 0.57 to 2.17% | 0 to 0.43% | The clearest metric separator |
| Language | Mostly English on screen, Taglish hook (H1) or Tagalog (H3) | Mostly Taglish voice | Not a clear separator |

### 8.2 Controlled comparisons (same variable changed)

1. **M1 (10.3K) vs L1 (629): same presenter, wall, sticker editing and length band.**
   - M1 opens with news: an official poster, then "Engene stop ka muna dyan… finally here".
   - L1 opens with a sales line: a render, then "for only 2,750 pesos".
   - M1 sells a *service* ("hindi kayang mag-order sa Weverse Shop on their own… ako nang bahala"). L1 sells a *price*.
   - M1 asks for a one-word comment and got 33 comments. L1 asks people to "order na kayo" and got 2.
2. **H1 (226K) vs H5 (56K): same footage.**
   - H1 adds a topical question hook and subtitles, and trades the call audio for a trending song.
   - H5 is raw. Both work. H1 earned 3.4x the likes per view and 27x the shares.
3. **H2 (225K) vs H6 (30.5K): same template.**
   - H2: payoff at 1.3 s vs 2.5 s, text off the product vs over it, a different fandom and product.
   - Can't isolate which one matters. Both are far above baseline, so the template itself works.
4. **H4 (71.6K) and M3 (11.9K) vs L2 (416): stock/arrival footage.**
   - Winners: one clean, wide, sharp shot of many identical branded boxes, plus a 3-to-5-word offer ("Onhand stocks / Open for installment", "11.11 Sale").
   - Loser: blurry close-ups of bagged items, with a date as the only text.
5. **2022 talking heads (15K to 89K) vs 2026 talking heads (470 to 629).**
   - 2022: face over a photo of the stock, hook = the cheap way in ("100 Dp 😱", "Pwede hulugan", "Pano ba yung installment?"), trending sound.
   - 2026: face over a plain wall, hook = full price ("P2,750") or a generic line ("this might change your life"), the ₱300 DP buried at 9.9 s, own voice for 20 to 114 s.

### 8.3 What I think it means (interpretation, test before trusting)

- **Strangers decide in about 2 seconds whether a video is for them.** A face on a plain wall saying a price looks like an ad, so people swipe and the post never leaves the follower pool (about 600 views). A lit lightstick, an idol, or a wall of boxes looks like content, so it gets tested on wider audiences. Retention data from TikTok Studio would confirm this.
- **Saves are the signal that predicts reach here.** People save tutorials and spectacle to use later. Nobody saves a price list they can DM for.
- **The account's selling lives in the caption and DMs. The video's only job is to earn the view.** The hits have no CTA in the video at all, and they still sell: H4 links a form in the caption, and M1's keyword CTA comes *after* 45 s of value.
- **Repeating the same offer burns it.** The BABYMONSTER lightstick was posted at least 5 times between May and August 2026, and views went down each time.
- **Off-niche posts (L5) and fan-account posts (May 2026) don't build on each other.** The only one that hit had a rare asset: a real idol interaction.

---

## 9. Formula cards

Copy the structure. Every fact (dates, prices, release info) still needs a source link, per project rules.

### Card A · "How to use it" tutorial (H2 225K, H6 30.5K)
- **When:** a product just launched or arrived, and owners will search for how to use it (connect, pair, set up a wristband, open the box, change the battery, fix "won't connect").
- **Hook (0 to 1.5 s):** the product in hand, unlit or unboxed, the app open next to it. **First visual change by 1.5 s** (light on, lid off). TTS or own voice states the exact task: "How to connect [product] to the app."
- **Structure:** steps 1 to 3 with on-screen numbers (0 to 12 s) → success moment (connects, changes colour) by about 12 s → 20+ s of pure payoff (colour cycling every 2 to 3 s, effects, modes).
- **Length:** 30 to 45 s, one take, top-down, hands only.
- **Show:** the real item and the real app screens; photocards/boxes in the background are fine.
- **Say:** steps only. English, so international owners searching also land on it. Optional Taglish line in the caption.
- **Text:** short title + numbered steps, placed **top-left/centre-left, not bottom-right** (TikTok's buttons sit there) and not over the product. Use a solid or semi-solid background.
- **CTA:** none in the video. Caption = the search query ("Connecting [product] to the app."). Pin it. A soft line in the comments is fine ("May stocks pa kami, DM lang").

### Card B · "Fan moment" (H1 226K, H5 56K)
- **When:** the shop has a **real, own** fan moment: a fansign/video call, concert footage the owner filmed, a pop-up visit, an idol reaction to something. Never someone else's footage presented as own.
- **Hook (0 to 3 s):** a topical question in Taglish over an official event visual or the moment itself ("Fate tour Philippines na ba to Heeseung? 😱"), or start mid-moment on the idol's face.
- **Structure:** the moment in one take, with 2 to 4 short English subtitles of the key lines → end on the emotional peak (heart hands, wave, call ends).
- **Length:** 20 to 25 s.
- **Say:** nothing. Let the idol's words carry it; subtitle them.
- **Caption:** one line that invites argument or tagging ("…na ba to?"), event hashtags.
- **CTA:** none. This format earns followers and trust, not orders.

### Card C · "Stock wall" proof clip (H4 71.6K, M3 11.9K, 2022-23 covers 37K to 52K)
- **When:** a shipment lands (onhand), or a sale date (11.11, 12.12, payday).
- **Hook (0 s):** one wide, sharp, well-lit shot of **many identical branded boxes**, with a 3-to-5-word offer in TikTok classic or white-box style: "Onhand stocks / Open for installment", "11.11 Sale", "Official, sealed and onhand".
- **Structure:** one slow pan or a static shot. Optional last second: one box opened, item lit.
- **Length:** 6 to 12 s (loops).
- **Avoid:** close-ups of items still in plastic bags, blur, date-only text (L2).
- **CTA:** form link or "DM" in the caption, not spoken.

### Card D · "News drop + I'll handle it" talking head (M1 10.3K)
- **When:** an official drop is announced (new merch, pop-up, restock, Weverse sale) that PH fans can't easily buy themselves.
- **Hook (0 to 2 s):** the official announcement visual for 1 s → presenter calls out the fandom by name and the news: "[Fandom], stop ka muna dyan. [Product] is finally here!"
- **Structure:** what dropped (official photos, 5 to 15 s) → why it's cute or wanted (member link) → the dates to remember in PH time (animated date stickers) → "sa mga hindi kayang mag-order on their own… ako nang bahala" → keyword CTA → dates again.
- **Length:** 45 to 60 s.
- **CTA:** **comment a one-word keyword** ("comment 'Enchin'"). It got 33 comments vs 0 to 2 on the pitches. Reply to each comment (a reply-to-comment video is the 2023 format that got 42.5K: "Replying to @msroxie0612 Here's how our installment… works").
- **Don't:** lead with the full price.

### Card E · "Cheap way in" hook (2022 era: H3 89.2K, 100-DP posts 13.7K to 43.3K)
- **Test, not proven for 2026.** Same products and pricing logic, different era.
- **Hook (0 to 2 s):** the lowest entry number or the installment promise as the first words and the big text: "₱300 DP lang, may [product] ka na", "Pwede hulugan", "Pano ba yung installment?". Show it over the **real stock**, not a plain wall.
- **Structure:** 10 to 20 s: stock → how the DP works in one line → "comment 'hulugan' para sa schedule".
- **Why test it:** L1 says "₱300 down payment" only at 9.9 s, after opening on "₱2,750". In 2022 the DP was the headline.

---

## 10. What the low performers do wrong (specific)

1. **The product isn't shown for real.** L1 uses a stock render; L3 a 1.4 s cut-out PNG at 12.6 s; L4 character cards; L6 a stock photo and a FB screenshot. The hits physically handle or display the item.
2. **The first words are a price or a sales line.** L1: "for only 2,750 pesos" at 0 s with a "P2,750" sticker at 2 s. L3: "Hear me out because this might change your life."
3. **The biggest selling point is buried.** In L1 the ₱300 DP comes at 9.9 s; in L3 the bag appears at 12.6 s.
4. **Nothing for a non-buyer to learn, feel or watch.** No demo, no reaction, no spectacle. These videos only work on people already shopping, and those people are a small slice of a 600-view follower pool.
5. **The caption is a Facebook post.** "🌹 WTS | LFB | … [PH GO] #Unniemart_Go … 💸 DP — ₱300 💳 ₱2,750 ✅️ … ✈️ NETA 💰 … ISF and PF". L6 literally screenshots the FB post as slide 1. The jargon is opaque to anyone outside the GO scene.
6. **The same offer is reposted until it dies.** BABYMONSTER lightstick: 1,186 → 629 → 598 → 430 → 446.
7. **Caption and video don't match.** L4's caption "pre order closing in few hours. habol na!!!" sits on a 114 s character lore video.
8. **Dead time.** L1 and L3 end on a 1.4 to 2 s logo card. L4 has white screens with typing for 114 s.
9. **Off-niche trend posts.** L5 (271 views) and the May 2026 English fan-account run (307 to 517) dilute what the account is about.
10. **Arrival footage shot badly.** L2: blurry, bagged, close-up, date-only text, no offer.
11. **Possible distribution issue:** L2 and L3 (and 2 more) were created from NL.

---

## 11. Do / Don't

**Do**
- Show the real item in the first frame, and make something visibly change by about 1.5 s: light on, box open, colour change (H2 1.3 s).
- Make at least half the posts useful to people who will never buy: connect tutorials, setup, "does it work with the app", real fan moments (H1, H2: about 225K each).
- Film stock as one clean, wide, sharp shot with a 3-to-5-word offer (H4: 6 s, 71.6K, 1.75% saves).
- When talking to camera, lead with news and the fandom name, not the price, and ask for a one-word comment (M1: 33 comments).
- If you mention money, lead with the smallest number ("₱300 DP") not the full price (Card E, test it).
- Keep the caption to one line: a search phrase or a question. Put the order details in a pinned comment, the bio form, or the DMs.
- Use TikTok text-to-speech or music for tutorials and stock clips. The hits barely use the presenter's voice.
- Place text top-left or centre-left, away from the right-side buttons, never over the product.
- Pin the format winners and reply to comments with videos (the 2023 reply-to-comment explainer got 42.5K).
- Post from the Philippines.

**Don't**
- Open on a stock render, a Facebook screenshot, a white slide, or the presenter's face with no product.
- Put "₱2,750" in the first 3 seconds.
- Say "hear me out, this might change your life" or "check out this bag" without showing the bag.
- Paste the Facebook WTS/LFB caption wall onto TikTok, or screenshot it as a slide.
- Repost the same offer every few weeks with a new caption.
- Post off-niche memes or generic fan-account content without a real asset behind it.
- End on a logo card.
- Write a caption the video doesn't deliver (L4).
- Treat M2 (24.8K views, 16 likes) as a winning format until you know whether it was paid.

---

## 12. Open questions for the owner (these decide what's true)

1. **TikTok Studio retention** for H2, M1, L1, L3: the % still watching at 2 s and 5 s. If the flops lose most viewers in the first 2 s, section 8.3 is confirmed.
2. **Traffic source** (For You / Search / Profile / Following) for H2, H6, M1, L1. If H2/H6 are mostly Search, tutorials are a long-tail search play and should target new products.
3. **Was M2 (Walk the Line tote) promoted?** Also M1 and H6, whose like rates are low (0.9%, 1.2%).
4. **Who posts since 2026-09-15, and from where?** `locationCreated` = NL on the last 4 posts. A/B test: next 4 posts from a PH phone/SIM.
5. **Is the Heeseung call the owner's own?** H5's caption says "i got to meet heeseung". If not, stop reusing it.
6. Launch dates of Engenebong V2 and Caratbong V3 (not verified here). They would test the "recent launch = more search demand" idea from H2 vs H6.

---

*Raw files: `data/raw/` (scrapes, page metadata, listing), `data/raw/videos/<slug>/` (video, frames, contact sheets `sheet_hook.jpg` / `sheet_full_*.jpg`, `pacing.json`, transcripts, `page-meta.json`). All gitignored.*
