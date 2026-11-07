# 05. How TikTok distributes videos in 2025 to 2026, and what grows a small seller account

Prepared 2026-10-14 for Unnie Mart (TikTok [@unniemart_](https://www.tiktok.com/@unniemart_)).
Question: how does TikTok decide who sees a video now, what format choices have real evidence behind them, what kills reach, and what should a small Philippine K-pop group-order shop that won't use AI slop actually do.

## Evidence ratings used in this file

| Rating | Meaning |
|---|---|
| **A** | Official or primary source (TikTok, Meta or YouTube policy and product docs), peer-reviewed research, or a large data study (about 1M+ posts or 100K+ accounts) |
| **B** | Credible secondary source: trade press reporting on data, platform-commissioned surveys, data studies with undisclosed or smaller samples |
| **C** | Anecdote, marketer opinion, or our own small-sample observation |

An **A** on a TikTok statement means "this is what TikTok officially says". It does not mean "proven". TikTok has a commercial interest in pushing longer videos, Search, Shop and LIVE. I flag where a claim looks self-serving.

---

## TL;DR

1. **TikTok scores every video per viewer** by predicting likes, shares, comments, skips, follows, saves, finishes, time spent and "Not interested", then ranks, removes look-alikes, and applies rules. One of those rules guarantees some content from creators in the viewer's own region. Follower count is not a direct input. ([TikTok recommendation system](https://www.tiktok.com/safety/en/policies-and-engagement/recommendation-system), [TikTok Newsroom 2020](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you)) **A**
2. **Search ranks differently from the For You feed.** TikTok's creator guide says Search "values relevance over video views and engagement", and that relevance comes from captions, on-screen text, spoken words and hashtags. ([Creator Academy: Search](https://www.tiktok.com/creator-academy/en/article/driving-video-traffic-search)) **A**. Unnie Mart's two 225K hits (lightstick app tutorial, concert reaction) include one pure search video. Search is the cheapest growth channel the shop has.
3. **Small accounts are being squeezed.** Socialinsider's 2M-video benchmark shows average views per post for 5K to 10K-follower profiles fell from 1,575 (2024) to 945 (2025), while 100K to 1M accounts rose 38.5%. ([Socialinsider](https://www.socialinsider.io/social-media-benchmarks/tiktok)) **A**. Unnie Mart's last 30 posts have a median of 620 views, which is under that benchmark.
4. **Posting more helps, but mostly as a lottery.** Buffer (11.4M posts): going from 1 to 2 to 5 posts a week gave +17% views per post. Median views stayed flat at about 500; the gain came from more breakout posts. ([Buffer](https://buffer.com/resources/how-often-should-you-post-on-tiktok/)) **A**
5. **Real reach killers are written policy, not folklore.** These are excluded from the For You feed: reposts with no creative edit, someone else's watermark, low-effort GIF-style clips, like-for-like or fake incentives, misleading claims, and (on LIVE) pushing people to buy off-platform in TikTok Shop markets like the Philippines. Not disclosing your own business promotion can also cut visibility. ([Community Guidelines, Aug 2026 version](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)) **A**
6. **AI labeling by itself does not cut reach**, says TikTok. But AI content showing a public figure "supporting products" they never endorsed is banned outright. An AI idol promoting the shop would get removed. ([Creator Academy: AIGC label](https://www.tiktok.com/creator-academy/en/article/ai-generated-content-label), [CG](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)) **A**
7. **Video beats photo posts on reach.** Metricool (2.3M posts) found video gets 5x the views and 6x the interactions of image posts. Carousels earn a decent engagement *rate* but small absolute reach. ([Metricool 2026](https://metricool.com/tiktok-study/), [Metricool 2024](https://metricool.com/tiktok-study-2024/)) **A**. Unnie Mart's price-list slideshows get 440 to 1,520 views.
8. **The Creator Rewards Program's "1 minute+" rule does not apply in the Philippines.** The program runs only in the US, UK, DE, JP, KR, FR, MX and BR. Make videos as long as the content needs, not 61 seconds by default. ([Creator Academy: eligibility](https://www.tiktok.com/creator-academy/en/article/eligibility)) **A**
9. **The Philippines is a Facebook plus TikTok market.** Facebook ad reach is 95.8M, Messenger 65.8M, and TikTok reaches 64.0M adults (81.8% of all 18+) as of Oct 2025. ([DataReportal Digital 2026 Philippines](https://datareportal.com/reports/digital-2026-philippines)) **A**. Cross-post clean, watermark-free files to Facebook Reels. Meta and Instagram demote watermarked and duplicated reels. ([Facebook, Jul 2025](https://creators.facebook.com/blog/combating-unoriginal-content), [Instagram](https://about.instagram.com/blog/announcements/instagram-ranking-explained)) **A**
10. **LIVE:** TikTok says 60 to 80-minute streams get more views than 10 to 20-minute ones ([Creator Academy: Going LIVE](https://www.tiktok.com/creator-academy/en/article/Going-LIVE)) **A**. Sell through TikTok Shop on LIVE, not through DMs or forms, because off-platform purchase prompts make a LIVE ineligible for the For You feed in Shop markets. **A**

---

## 0. Method and limits (read this before trusting the file)

- **Sources read in full:** TikTok's transparency page on the recommendation system, the current Community Guidelines (labeled "2026 August" version), about 45 TikTok Creator Academy articles, TikTok Newsroom posts (2020 to 2025), TikTok for Business pages, Meta and YouTube policy pages, DataReportal, two peer-reviewed algorithm audits, and the Buffer, Socialinsider and Metricool data studies.
- **The session's web-search budget ran out early.** After that I found sources only through known primary URLs, site sitemaps and links inside pages I'd already fetched. Coverage of Philippine live-selling practice and TikTok Shop PH rules is therefore **thin**. See section 8.
- **www.tiktok.com's robots.txt disallows Claude agents.** I read the Community Guidelines, the recommendation-system page and the Creator Academy articles before I noticed this, and fetched nothing further from that host afterwards. All of those URLs are public, so a human can check them.
- **TikTok Shop Seller Center (PH)** pages load only with JavaScript or a login, so I could not verify the K-pop listing, brand-authorization or pre-order rules there.
- Creator Academy pages show no publish date. I treat them as current on the access date, 2026-10-14.
- **Own data:** references to Unnie Mart's numbers come from the 2026-10-14 scrapes in `data/raw/tiktok-popular-2026-10-14.json`, `data/raw/tiktok-latest-2026-10-14.json` and `data/raw/competitors/disc_search*.json`. All own-data points are rated **C** (small sample, no controls).

---

## 1. Ranking signals

### 1.1 What TikTok officially says about the For You feed (FYF)

| # | Claim | Source | Rating |
|---|---|---|---|
| 1 | The system creates "a prediction score for different videos... Videos with the highest score are selected to be served to your For You feed." Pipeline: select eligible videos, predict, rank, similarity check, recommendation rules. | [TikTok: Introduction to the recommendation system](https://www.tiktok.com/safety/en/policies-and-engagement/recommendation-system) | A |
| 2 | Predicted interactions include the likelihood to "Like, share, comment on, or mark a video as 'Not Interested'", "Follow the video's author or interact with their profile", "Finish, skip, or favorite [save] a video", "Spend a certain amount of time viewing a video", "Tap the video's soundtrack." | same | A |
| 3 | Viewer-side inputs: region, device language, OS, "videos you've recently interacted with, including those you watched, finished, liked, or skipped", follow relationships. It also uses others' behavior (collaborative filtering): if another user engaged with two of the same videos as you, the system may predict you'll like a third that they liked. | same | A |
| 4 | Video-side inputs: time posted, region posted from, the author's language setting, the soundtrack, video length, hashtags. | same | A |
| 5 | Strong vs weak signals: "whether a user finishes watching a longer video from beginning to end, would receive greater weight than a weak indicator, such as whether the video's viewer and creator are both in the same country." | [TikTok Newsroom, Jun 18 2020](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you) | A (6 years old) |
| 6 | "Neither follower count nor whether the account has had previous high-performing videos are direct factors in the recommendation system." | same | A (old; see 1.3 for what independent data shows) |
| 7 | Similarity check: "If some of the videos... are too similar to each other - for example, they use the same sound - we replace them." The feed generally won't show two videos in a row with the same sound or creator. | rec-system page; Newsroom 2020 | A |
| 8 | Rules ensure "videos in your For You feed include content from creators in your region." | rec-system page | A |
| 9 | Moderation comes first. Only videos that pass moderation enter the pool, and content "not suitable for a broad audience is made ineligible for recommendation." | rec-system page | A |
| 10 | Viewer controls: "Not interested" ("we will limit how much of that content we recommend"), keyword filters, feed refresh. | rec-system page | A |
| 11 | "Users spend 96% of their time on TikTok scrolling through the FYF." TikTok's advice to creators: watch time ("trim any lulls"), trends, engagement. | [Creator Academy: recommendation system intro](https://www.tiktok.com/creator-academy/en/article/guidelines-recommendation-system-intro) | A (self-reported stat) |
| 12 | The FYF system "looks at things like what you like, share, comment on, and search for, as well as what's trending." If a video is made FYF-ineligible, "this information will appear in the TikTok analytics tool." | [Creator Academy: video not recommended](https://www.tiktok.com/creator-academy/en/article/video-not-recommended) | A |
| 13 | What TikTok itself measures as "quality" (the Creator Rewards Program's Additional Reward): average watch time, retention ("how many viewers stay after 30s, 40s, 50s, 60s, or 90s"), completion rate, and search value. | [Creator Academy: RPM four key factors](https://www.tiktok.com/creator-academy/en/article/RPM-understanding-the-four-key-factors) | A |

**What TikTok does not publish:** the weights. No official source says "shares count X times more than likes". Every precise weighting you see in blogs is a guess. **C**

### 1.2 What independent research adds

| Finding | Source | Rating |
|---|---|---|
| In a TikTok data-donation study, TikTok "exploited users' interests between 30% and 50% of the time" in the first 1,000 videos shown. So 50 to 70% of a feed is exploration, and that exploration share is how unknown creators get shown at all. Following an account made its videos "significantly more likely" to appear; scrolling speed had less effect than expected. | Vombatkere, Mousavi, Zannettou, Roesner, Gummadi, *TikTok and the Art of Personalization*, ACM Web Conference 2024 ([arXiv](https://arxiv.org/abs/2403.12410), [UW summary](https://www.washington.edu/news/2024/04/24/tiktok-black-box-algorithm-and-design-user-behavior-recommendation/)) | A |
| Sock-puppet audit: follow had the strongest effect on personalization, then like, then video view rate. Language and location also changed what was recommended. | Boeker and Urman, *An Empirical Investigation of Personalization Factors on TikTok*, Web Conference 2022 ([arXiv](https://arxiv.org/abs/2201.12271)) | A (2022) |
| A leaked internal document ("TikTok Algo 101", reported by the NYT, Dec 2021) said the goal is daily active users through two metrics, **retention and time spent**. The simplified scoring formula was Plike×Vlike + Pcomment×Vcomment + Eplaytime×Vplaytime + Pplay×Vplay. | NYT report as summarized by [Inverse](https://inverse.com/input/culture/tiktok-internal-docs-reveal-just-how-simple-it-is-to-keep-you-addicted) (NYT original: nytimes.com/2021/12/05/business/media/tiktok-algorithm.html, paywalled, not fetched) | B |
| Shares are the fastest-growing interaction: +13% year on year overall, +44% for large accounts. 2025 engagement rate by views was 4.20%, dropping to 3.85% in Q2 2026. | [Socialinsider 2026 TikTok Benchmarks](https://www.socialinsider.io/social-media-benchmarks/tiktok), 2M videos, 214,507 profiles, Jan 2024 to Dec 2025 plus Q2 2026 update | A |
| Across 69M short videos, TikTok's average engagement rate fell from 3.70% (2025) to 2.60% (2026). TikTok still leads Reels (0.45%) and Shorts (0.30%) on engagement. | [Socialinsider: TikTok vs Reels vs Shorts](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/), Jan 2025 to Jul 2026 | A |
| Facebook Reels ranks on a near-identical set of predictions: watch duration, completion, likes, skip, hide, "see less". This suggests the same video craft works on both platforms. | [Meta Transparency: Facebook Reels ranking](https://transparency.meta.com/features/explaining-ranking/fb-reels/), updated Jun 19 2026 | A |

**Synthesis (my reading of the A sources, not a TikTok statement):** the signals that matter most are the ones TikTok both predicts and measures for "quality": watch time and completion, shares, saves, comments, follows and profile visits from the video, with "Not interested" as the main negative. Likes matter but are cheap. For a seller, **saves and shares** are the useful ones: a save means "I'll need this later" (tutorials, price checks), and a share means "my friend in the fandom needs this".

### 1.3 How small accounts get initial distribution

| Claim | Source | Rating |
|---|---|---|
| Follower count is not a direct ranking factor. | [Newsroom 2020](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you) | A (old) |
| Region rule: every viewer's feed includes creators from their region. A PH creator posting for PH fans gets a structural slot. | [rec-system page](https://www.tiktok.com/safety/en/policies-and-engagement/recommendation-system) | A |
| TikTok's own advice for more FYF traffic: "Post more often! The more videos you post, the more opportunities you give the recommendation system to understand your content." Pick a niche and "use common video topics, hashtags, and sounds from your community". Put "your own twists" on trends. | [Creator Academy: FYF traffic](https://www.tiktok.com/creator-academy/en/article/video-traffic-the-for-you-feed) | A |
| Smaller accounts get more than 75% of impressions from the For You feed. In 2026, the FYF drove 7 of every 10 views overall. | [Metricool 2024](https://metricool.com/tiktok-study-2024/) (87,600 accounts, 1M videos); [Metricool 2026](https://metricool.com/tiktok-study/) (92K accounts, 2.3M posts) | A |
| 2025 views per post fell 59% for 1K to 5K accounts (860 to 350) and 40% for 5K to 10K (1,575 to 945). 100K to 1M accounts rose 38.5% (25,198 to 34,900). Follower growth fell 33% across tiers. | [Socialinsider](https://www.socialinsider.io/social-media-benchmarks/tiktok) | A (mostly brand profiles) |
| The "every video is first shown to a test batch of 200 to 300 people" story. | No primary source found. Marketer lore. | C |

**Plain reading:** follower count isn't an input, but large accounts carry more accumulated signals and a bigger Following feed. In 2025 TikTok's reach visibly concentrated on bigger accounts. A 5.9K account can't count on its followers. It has to win per video on watch time and shares, or win on Search, where relevance beats popularity.

### 1.4 What changed recently (2024 to 2026)

| Change | Evidence | Rating |
|---|---|---|
| **Longer videos are pushed.** Uploads can now run up to 60 minutes. TikTok says "users now spend 50% of their time watching longer content" and that 1-minute+ watch time "has been 5x higher than short videos". | [Creator Academy: RPM](https://www.tiktok.com/creator-academy/en/article/RPM-understanding-the-four-key-factors), [one-minute tools](https://www.tiktok.com/creator-academy/en/article/tool-one-minute-feature-overview) | A (self-serving) |
| **The Creator Rewards Program (launched Mar 18 2024) pays only for 1-minute+ originals.** It scores originality, play duration, search value and audience engagement. It is open only in the US, UK, DE, JP, KR, FR, MX and BR, for personal accounts with 10K+ followers. Duets, Stitches and Photo Mode are ineligible. | [TikTok Newsroom](https://newsroom.tiktok.com/en-us/introducing-the-new-creator-rewards-program), [Creator Academy: eligibility](https://www.tiktok.com/creator-academy/en/article/eligibility) | A |
| Longer videos in independent data: >3 min got "more than double the views" of 6 to 10 s videos, and completion rates barely differed between 11 s and 10 min. Separately, 2 to 5 min had the highest average views. | [Buffer](https://buffer.com/resources/best-tiktok-video-length/) ("millions of videos", method not disclosed); [Metricool 2024](https://metricool.com/tiktok-study-2024/) | B / A. Correlational: creators who make long videos differ from those who don't. |
| **Search grew.** US internal data: "57% of users use TikTok's search functionality" and "23% search for something within 30 seconds of opening the app" (Jun 2024). Total searches were up 40% year on year (Jan to Feb 2025). Creator Search Insights launched Mar 13 2024. | [TikTok for Business: Search Ads](https://ads.tiktok.com/business/en-US/blog/introducing-search-ads-campaign), [Search Ads growth](https://ads.tiktok.com/business/en-US/blog/tiktok-search-ads-incremental-revenue-growth), [Newsroom](https://newsroom.tiktok.com/en-us/creator-search-insights) | A (TikTok internal, US) |
| **Photo posts surged but don't win reach.** Photo/carousel posting rose 140%, but video got 5x the views and 6x the interactions. | [Metricool 2026](https://metricool.com/tiktok-study/) | A |
| **Small-account squeeze** and falling engagement rates (section 1.2). | Socialinsider | A |
| **Commerce rules tightened.** Visibility is reduced for content directing people to buy off-platform in TikTok Shop markets. Own-brand promotion must use the content disclosure setting. | [CG: Accounts and Features](https://www.tiktok.com/community-guidelines/en/accounts-features), [CG: Regulated and Commercial](https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities) | A |
| **AI-content labeling formalized.** TikTok reads C2PA Content Credentials to auto-label AI content from other platforms (since May 2024). Creators must label realistic AI. TikTok says labeling doesn't affect distribution. | [Newsroom May 9 2024](https://newsroom.tiktok.com/en-us/partnering-with-our-industry-to-advance-ai-transparency-and-literacy), [Creator Academy](https://www.tiktok.com/creator-academy/en/article/ai-generated-content-label) | A |
| **Content commerce is now a third of SEA online retail:** 37% of Southeast Asia's platform e-commerce GMV comes from content commerce, up from 20% two years earlier. | [Momentum Works, Live Commerce in SEA 2026](https://momentum.asia/insights/detail/live-commerce-in-southeast-asia-2026) (Sep 2026, headline only; full report paid) | B |

---

## 2. TikTok Search and SEO

This matters most for Unnie Mart. "Connecting engenebong V2 to the app" (38 s) got 225.4K plays and 3,976 saves. "Connecting Caratbong V3 to app" (43 s) got 30.5K. Both are answers to a question people type into Search. (own data, `data/raw/tiktok-latest-2026-10-14.json`) **C**

### 2.1 How Search ranks (official)

| Claim | Source | Rating |
|---|---|---|
| "Search is different from the For You feed, as it values relevance over video views and engagement." | [Creator Academy: Driving traffic via Search](https://www.tiktok.com/creator-academy/en/article/driving-video-traffic-search) | A |
| "Videos in search results are sorted according to a combination of factors, including relevance to your search query and engagement. Relevance is determined based on things like video captions, video text, and hashtags." | [Creator Academy: Search](https://www.tiktok.com/creator-academy/en/article/search) | A |
| Use "your video's description, voiceovers, captions, and on-screen text to make it clear just what your video's all about." Titles and covers "should clearly showcase your topic." | [Creator Academy: Getting discovered with Search](https://www.tiktok.com/creator-academy/en/article/Getting-discovered-with-Search), [Driving traffic via Search](https://www.tiktok.com/creator-academy/en/article/driving-video-traffic-search) | A |
| Keyword stuffing backfires: tiny or swiped-off on-screen keyword text "can get your video flagged for spam", and "irrelevant text stacking will actually negatively affect your video traffic." | same two articles | A |
| A long hashtag list does not help. "What matters most is using relevant, accurate language." | [Getting discovered with Search](https://www.tiktok.com/creator-academy/en/article/Getting-discovered-with-Search) | A |
| You do not need to edit in-app for Search ("your contents' search performance won't be impacted"). | same | A |
| Search recommendations (the "Others searched for" bar above comments) "are generated based on... the content of comments and common searches made after watching a video." | [Creator Academy: Search](https://www.tiktok.com/creator-academy/en/article/search) | A |
| Search prioritizes "entertaining and informative content" and tries "to highlight content from reliable sources at the top." | [CG: Accounts and Features](https://www.tiktok.com/community-guidelines/en/accounts-features) | A |
| Search views of 30 s or more count as qualified views, and "search value" is a reward metric. This shows TikTok actively wants Search content. | [Creator Academy: qualified views](https://www.tiktok.com/creator-academy/en/article/monetization-creativity-program-qualified-view) | A |
| Spoken words are indexed through automatic speech transcription. | Implied by TikTok's "voiceovers" guidance (A). Specific claims like "say the keyword in the first 10 to 15 seconds" or "first 50 characters of the caption weigh most" come only from marketer blogs ([example](https://tlinky.com/tiktok-search/)). | A for "voiceover counts"; C for the specifics |

### 2.2 Tools Unnie Mart can use today

| Tool | What it gives | Source | Rating |
|---|---|---|---|
| **Creator Search Insights** (type it into the search bar) | Trending search topics. The **Content gap** tab shows topics "that have lots of searches but not many high-quality videos yet". **Searches by followers** shows what your own followers search and needs 1,000 followers (Unnie Mart has 5.9K). Available "in select regions"; check in app for PH. | [Creator Academy: Content gap](https://www.tiktok.com/creator-academy/en/article/search-insights-content-gap), [Getting discovered](https://www.tiktok.com/creator-academy/en/article/Getting-discovered-with-Search), [Newsroom](https://newsroom.tiktok.com/en-us/creator-search-insights) | A |
| **Analytics, Traffic source, Search queries** | "See what viewers searched before finding your post. This data covers the last 90 days. If a query fits your topic, try using those words in your captions." | [Creator Academy: analytics](https://www.tiktok.com/creator-academy/en/article/analytics-tool-video-performance) | A |
| **TikTok Studio, Creation inspiration** | Trending posts and searches in your niche. | same | A |

### 2.3 How many people search on TikTok

| Stat | Source | Rating |
|---|---|---|
| 86% of US Gen Z search on TikTok weekly (vs 90% on Google). Searches skew to fashion/beauty (+26%), cooking (+23%), entertainment (+22%), DIY (+15%). 1 in 5 TikTok search users bought something after searching. | TikTok + WARC survey, n>1,000 US, 2025 ([Tubefilter](https://www.tubefilter.com/2025/09/10/tiktok-search-engine-ads-new-research/), [TikTok for Business](https://ads.tiktok.com/business/en-US/blog/tiktok-search-ads-incremental-revenue-growth)) | B (TikTok-commissioned) |
| 65% of US Gen Z have used TikTok as a search engine, but only 4% now rely on it more than Google (down from 8% in 2024). | Adobe Express survey, n=1,007, Jan to Feb 2026 ([Search Engine Journal](https://www.searchenginejournal.com/gen-z-preference-for-tiktok-over-google-drops/568199/)) | B |
| 57% of US TikTok users use Search; 23% search within 30 s of opening the app. | [TikTok for Business](https://ads.tiktok.com/business/en-US/blog/introducing-search-ads-campaign) (internal, Jun 2024) | A (US only) |
| Philippines-specific search share. | **Not found.** All search stats above are US. | n/a |

**Reading:** TikTok is not replacing Google, but it is a habit for young users looking for "how do I..." answers about things they just bought or want to buy. "How to connect [lightstick] to the app" is exactly that kind of query: the user just paid ₱2,600 to ₱3,500 for a lightstick, the official app is in Korean or English, and the concert is days away.

Market check from our own scrape (C): the top results for "lightstick app connect tutorial" have 453.6K, 176.3K and 164.8K views, at 84 to 139 seconds long. Top results for "kpop store packing orders asmr" have 4.8M, 3.8M and 1.2M. (`data/raw/competitors/disc_search2.json`)

---

## 3. Format evidence

| Format | What the evidence says | Strength | Implication for Unnie Mart |
|---|---|---|---|
| **Video length** | TikTok pushes 1 min+ and says longer videos take 50% of watch time ([CA](https://www.tiktok.com/creator-academy/en/article/RPM-understanding-the-four-key-factors), A, self-serving). In Buffer's data, >3 min got 2x+ the views of 6 to 10 s ([Buffer](https://buffer.com/resources/best-tiktok-video-length/), B). In Metricool's, 2 to 5 min had the highest average views ([Metricool 2024](https://metricool.com/tiktok-study-2024/), A). No study controls for content type. Unnie Mart's two biggest hits ran 23 s and 38 s (C). | Medium (correlational) | Length should follow the job. Tutorials: as long as the steps need (45 to 120 s is typical for top "connect lightstick" results). Fan moments: short. Never pad to 61 s; the 1-minute rule pays nothing in PH. |
| **Posting frequency and consistency** | Buffer, 11.4M posts, fixed-effects within-account: going from 1 to 2 to 5 posts a week gave +17% views per post; 6 to 10 gave +29%; 11+ gave +34%. Median stayed flat at about 500. The 90th percentile went from 3,722 (1/wk) to 6,983 (2 to 5/wk) to 14,401 (11+/wk): "Posting more helps, but mostly because it increases your chances of getting lucky." ([Buffer](https://buffer.com/resources/how-often-should-you-post-on-tiktok/)). TikTok: "consistency matters more than perfection" ([CA](https://www.tiktok.com/creator-academy/en/article/building-a-sustainable-posting-routine)). | **Strong** (A) | 3 to 5 posts a week is the realistic sweet spot for one owner who films. Each extra good post is another lottery ticket. A weak post costs little, but it doesn't help either. |
| **Original audio vs trending sounds** | TikTok: "Using sounds that are already buzzing in the community can give your video that extra edge" ([CA](https://www.tiktok.com/creator-academy/en/article/the-importance-of-sound), A, vague). TikTok also says videos with background music average "+98.31% more views" than those without ([CA: elements](https://www.tiktok.com/creator-academy/en/article/elements-of-tiktok-video), A self-reported, correlational). The similarity check spaces out same-sound videos (A). Business use: "Businesses cannot use the general music library for commercial usage. Businesses should instead use the Commercial Music Library" ([TikTok Ads Help](https://ads.tiktok.com/help/article/commercial-music-library), A). No independent study isolates trending sound vs original audio. | Weak to medium | For tutorials and talking videos, the voice is the content; quiet music under it at about 25% ([CA](https://www.tiktok.com/creator-academy/en/article/choosing-background-music)). For sales and commercial posts, use Commercial Music Library tracks or original audio, not the latest K-pop single. The scrape shows `commerceUser=false`, `ttSeller=true`; check the account type in the app. |
| **Series and recurring formats** | TikTok recommends repeatable formats, a set day per format, consistent fonts and covers, and Playlists ([CA: posting routine](https://www.tiktok.com/creator-academy/en/article/building-a-sustainable-posting-routine), [Hook-Hold-Act](https://www.tiktok.com/creator-academy/en/article/build-a-repeatable-format), A advice, no data). Playlists need **10K followers** ([CA: Playlists](https://www.tiktok.com/creator-academy/en/article/tool-playlists-intro), A). Socialinsider's analyst says series content drives shares (opinion, C). | Medium (official advice, no outcome data) | A "Lightstick Clinic" series (one model per episode, same cover template) fits both Search and recurring viewing. Playlists unlock at 10K. |
| **Replying to comments with video** | TikTok recommends it ("Respond to comments with a video", stitch good comment ideas) ([CA](https://www.tiktok.com/creator-academy/en/article/video-traffic-the-for-you-feed), A advice). No independent reach data. Own data: "Replying to @msroxie0612 Here's how our installment/hulugan of caratbong v3 works" (175 s) got 42.5K plays (C). | Medium | Answer real buyer questions (installment, shipping, authenticity, GO timeline) with video replies. Each one is a search-friendly FAQ and shows real fans asking. |
| **Stitch / Duet** | TikTok suggests stitching follower comments ([CA](https://www.tiktok.com/creator-academy/en/article/video-traffic-the-for-you-feed), A). Duets and Stitches are excluded from Creator Rewards ([CA](https://www.tiktok.com/creator-academy/en/article/RPM-understanding-the-four-key-factors), A), which says nothing about reach. "Split screens, meaningless reactions" are flagged as low quality in reward reviews ([CA: eligibility](https://www.tiktok.com/creator-academy/en/article/eligibility), A). No reach data. | Weak | Use sparingly, and only with real added commentary (for example, reacting to an official lightstick announcement with what it means for PH buyers). |
| **Carousels / Photo Mode** | 2024: images and carousels had a higher engagement *rate* (6.46%), but videos earned ~60% more total interactions ([Metricool 2024](https://metricool.com/tiktok-study-2024/), A). 2026: video got 5x the views and 6x the interactions of images ([Metricool 2026](https://metricool.com/tiktok-study/), A). Photo posts are excluded from Creator Rewards; "low-quality images, or slide videos" count as low quality ([CA](https://www.tiktok.com/creator-academy/en/article/eligibility), A). TikTok says "76% of TikTok users say they enjoy a mix of images and video" (quoted by [Hootsuite](https://blog.hootsuite.com/tiktok-algorithm/), B). Own data: recent slideshows got 442 to 1,523 views (C). | **Strong for "video wins reach"** | Keep photo posts for save-worthy reference content (size charts, GO timeline, version comparison). Don't use them as the main reach format. Retention analytics work for photo posts with 2+ photos. |
| **LIVE (general)** | Must be 18+ ([CG](https://www.tiktok.com/community-guidelines/en/accounts-features), A). "LIVEs lasting between 60-80 minutes tend to get more views than LIVEs lasting 10-20 minutes"; "go LIVE more often to build a loyal audience" ([CA: Going LIVE](https://www.tiktok.com/creator-academy/en/article/Going-LIVE), A). Recommended business formats: demo, Q&A, behind-the-scenes, day-in-the-life ([CA: LIVE for business](https://www.tiktok.com/creator-academy/en/article/LIVE-for-your-business-engage-convert-and-grow), A). Promote with a video beforehand and go live at peak hours ([TikTok for Business](https://ads.tiktok.com/business/en-US/blog/tiktok-live-best-practice), A advice). These LIVEs are FYF-ineligible: unoriginal streams, "repeated or prolonged actions that lack clear objectives or direct interaction", black or blank screens, and pushing off-platform purchases in Shop markets ([CG](https://www.tiktok.com/community-guidelines/en/accounts-features), A). Commercial LIVEs must switch on the disclosure toggle (A). | Medium to strong on rules; weak on outcomes | A weekly 60 to 80 min LIVE: unboxing a box from Korea, on-hand items, lightstick troubleshooting, Q&A. Owner on camera and talking. No silent product loops. |
| **LIVE selling in PH** | TikTok PH runs live-selling training for sellers with DTI: Camp Asenso, about 400 sellers, Aug 2024 ([Newsroom PH](https://newsroom.tiktok.com/fil-ph/tiktok-shop-and-dti-empower-filipino-msmes)), and DigiCities across 27 cities, Dec 2024 ([Newsroom PH](https://newsroom.tiktok.com/fil-ph/tiktok-shop-and-gcash-for-business-unlock-msme-growth-across-the-philippines-with-digicities-program)) (A, promotional, no outcome data). Content commerce is 37% of SEA platform e-commerce GMV ([Momentum Works](https://momentum.asia/insights/detail/live-commerce-in-southeast-asia-2026), B). Practices like "mine"-style claiming, pasabuy and down-payment installments are common knowledge in PH selling, but **I found no citable study of PH TikTok LIVE practice**. | Weak (C) | Treat LIVE as a test. Run 4 to 6 weekly LIVEs, track viewers, orders and follows, then decide. Watch 3 to 5 PH K-pop seller LIVEs first and note what they do (competitor research file). |
| **TikTok Shop PH: can K-pop merch be sold?** | Counterfeit goods and IP violations are prohibited platform-wide ([CG](https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities), A). "Gambling-like activities... mystery boxes" and "mystery value products: goods with unknown or variable worth" are not allowed, except in some regions for verified sellers (A). This could affect random-photocard pulls or "lucky draw" listings; unclear. Unnie Mart is already flagged as a TikTok Shop seller (`ttSeller: true`), and three 2022 to 2023 lightstick videos carried Shop product links (own data, C). **Not verified:** whether official K-pop label merch needs brand authorization on TikTok Shop PH, and how long a pre-order can run versus GO timelines. Seller Center pages couldn't be read. | Rules A; PH specifics **unverified** | Sell on-hand official items through TikTok Shop. Keep authenticity proof (Korean store receipts, packaging) on camera. Verify brand-authorization and pre-order rules in Seller Center before moving group orders to Shop. Avoid random-pull or lucky-draw offers on TikTok until checked. |

---

## 4. Penalties and reach killers

| Reach killer | What the rule actually says | Source | Rating | Risk for Unnie Mart |
|---|---|---|---|---|
| **Unoriginal or reposted content** | FYF-ineligible: "Reused or unoriginal content posted without creative edits"; "Content is also ineligible for the FYF if it includes unoriginal or reused material without anything new." TikTok's definition covers content "copied completely from others", "largely repurposed... without adding any creative edits", or "combined from multiple sources with little or no additional information." | [CG: Integrity and Authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity), [CA: Originality policy](https://www.tiktok.com/creator-academy/en/article/tiktok-originality-policy) | A | **High** if the shop reposts agency teasers, Weverse product photos or other fans' fancams. |
| **Watermarks** | "Clips that show someone else's watermark or logo" are FYF-ineligible. TikTok also says "Avoid using materials with watermarks." | same; [CA: mistakes](https://www.tiktok.com/creator-academy/en/article/avoid-common-creation-mistakes) | A | Medium. Never use other sellers' or fan-site photos. |
| **Low-effort static or text-only posts** | FYF-ineligible: "Low-quality or minimally edited content, such as short clips made from GIFs only." Reward reviews flag "low-quality images, or slide videos." Instagram demotes reels that "are majority text." | [CG](https://www.tiktok.com/community-guidelines/en/integrity-authenticity); [CA](https://www.tiktok.com/creator-academy/en/article/eligibility); [Instagram, May 2023](https://about.instagram.com/blog/announcements/instagram-ranking-explained) | A | **High.** This describes the "WTS / LFB / price" slideshow posts. |
| **AI-generated content** | Must label AI or significantly edited content showing realistic people or scenes; unlabeled content "may be removed, restricted, or labeled". **Not allowed:** AI likeness of private people without consent, and AI content showing "a public figure... supporting products... they haven't actually addressed". AI audio that "mimics the voice of a real person" needs disclosure. Labeling "won't affect the distribution of your video as long as it doesn't violate our Community Guidelines." TikTok auto-labels via C2PA Content Credentials; 37M creators had used the label by May 2024. Generic text-to-speech needs no disclosure. | [CG: Integrity and Authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity); [CA: AIGC label](https://www.tiktok.com/creator-academy/en/article/ai-generated-content-label); [Newsroom May 2024](https://newsroom.tiktok.com/en-us/partnering-with-our-industry-to-advance-ai-transparency-and-literacy) | A | The shop's no-AI rule already avoids this. Note that an AI idol "recommending" the shop would be a **removal**, not just a reach drop. Reports that TikTok added a viewer setting to see less AI content in late 2025 are **unverified** here. |
| **Engagement bait** | FYF-ineligible: "'Like-for-like' promises", "False incentives for gifting or following", "Misleading claims meant to boost views or popularity". "Content that tries to manipulate people into giving gifts or inflating likes or follows isn't eligible for the FYF." Facebook also demotes engagement bait. | [CG](https://www.tiktok.com/community-guidelines/en/integrity-authenticity); [Meta: types of content we demote](https://transparency.meta.com/features/approach-to-ranking/types-of-content-we-demote/) (updated Jul 2 2025) | A | Medium. Avoid "follow + like to join" giveaways, fake "last 2 slots", and "comment MINE if..." used only to farm comments. |
| **Pointing people off-platform** | "We reduce visibility of content directing users to purchase products off-platform in markets where TikTok Shop is available." This is stated under LIVE commercial content; LIVEs that "direct users off-platform to purchase products online" in Shop markets are FYF-ineligible. For regular videos no equally explicit rule was found, but comments with "irrelevant promotions, or links" get sorted lower. | [CG: Accounts and Features](https://www.tiktok.com/community-guidelines/en/accounts-features) | A (LIVE explicit; videos inferred, C) | **High on LIVE.** The bio links to a bit.ly order form, and a 2023 caption carried a forms.gle link. In videos, keep CTAs soft ("details in bio / DM"). |
| **Undisclosed self-promotion** | Disclosure is required when "Promoting your own business, product, or service". If not disclosed, "we may reduce its visibility or apply the content disclosure setting"; repeated failure can restrict posting. | [CG: Regulated and Commercial](https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities) | A | **Medium to high.** Every sales post should have the content disclosure toggle on ("Your brand"). Whether disclosed posts get less reach is not documented (C). |
| **Keyword stuffing / hidden text** | Can be "flagged for spam"; "irrelevant text stacking will actually negatively affect your video traffic." | [CA](https://www.tiktok.com/creator-academy/en/article/Getting-discovered-with-Search) | A | Low if captions stay natural. |
| **Counterfeit and mystery-value goods** | Counterfeit is not allowed. Gambling-like activities and mystery-value products are not allowed outside verified-seller exceptions. | [CG](https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities) | A | Check before selling random pulls or lucky draws. |
| **Account strikes** | Strikes expire after 90 days; bans hit at feature or policy thresholds. Repeated FYF-ineligible content can restrict an account, including "appear[ing] in top search results, or in the FYF". | [Newsroom PH, Feb 2023](https://newsroom.tiktok.com/fil-ph/supporting-filipino-creators-with-an-updated-account-enforcement-system); [CG](https://www.tiktok.com/community-guidelines/en/integrity-authenticity) | A | Low today, but one copyright-heavy concert repost habit could build up. |
| **Deleting videos** | No TikTok statement says deleting hurts or helps reach. | none found | C | Don't delete evergreen tutorials: they keep pulling search traffic. Make low performers private only if they're wrong or embarrassing. |
| **Inconsistent posting** | No source shows a "penalty" for breaks. Buffer's data shows *fewer chances*, not punishment. | [Buffer](https://buffer.com/resources/how-often-should-you-post-on-tiktok/) | A (absence of penalty is my reading) | A two-week gap costs lottery tickets, not account health. |
| **Muted audio / copyright on concert clips** | Copyright violations are not allowed. Reaction content needs original commentary to make up "the majority of your video". | [CG](https://www.tiktok.com/community-guidelines/en/integrity-authenticity); [CA: Reaction content](https://www.tiktok.com/creator-academy/en/article/Create-unforgettable-reaction-content) | A | Concert reactions should centre on the owner's face, voice and story, with short performance cuts and no full songs. |

How to check: if a video is made FYF-ineligible, TikTok says it shows in analytics, and there's an "Account check" tool ([CA](https://www.tiktok.com/creator-academy/en/article/video-not-recommended)). **A**. Check this before blaming a "shadowban".

---

## 4b. Philippines specifics

### Platform reach (ad-audience data, not active users)

| Platform | Digital 2026 (data Oct 2025) | Digital 2025 (Feb 2025) | Source | Rating |
|---|---|---|---|---|
| Internet users | 98.0M (83.8% of pop.) | 97.5M | [DataReportal 2026](https://datareportal.com/reports/digital-2026-philippines), [2025](https://datareportal.com/reports/digital-2025-philippines) | A |
| Facebook | 95.8M (81.9% of pop.; 97.7% of internet users) | 90.8M | same | A |
| Messenger | 65.8M (56.2%) | 61.8M | same | A |
| TikTok (18+ only) | 64.0M = 81.8% of all adults; 55.3% female; +9.7% YoY, but −6.9% Jul to Oct 2025 (DataReportal warns this may be a data correction) | 62.3M | same | A |
| YouTube | 59.6M (50.9%) | 57.7M | same | A |
| Instagram | 26.9M (22.9%; +24.6% YoY) | 22.9M | same | A |

Caveat: these are platform ad-tool numbers. Meta's figure works out to "122.1% of adults", which shows they overcount. Use them for relative size, not head counts. TikTok's count excludes under-18s, and much of K-pop fandom is under 18.

### What it means for selling

- **Facebook is still the widest net, and Messenger is the order desk.** TikTok itself launched Messaging Ads in PH (Jan 2025) that "redirect users to third-party messaging platforms like Facebook Messenger or WhatsApp." ([Newsroom PH](https://newsroom.tiktok.com/fil-ph/tiktok-messaging-ads-in-the-philippines)) **A** for the product. The inference that Messenger is central to PH purchase flows is **B**.
- **Facebook Reels ranking** uses watch duration, completion, likes, skips and hides ([Meta](https://transparency.meta.com/features/explaining-ranking/fb-reels/)), so the same well-made vertical video can serve both. **A**
- **Peak times:** no PH-specific primary data found. Buffer's global analysis (7.1M posts, Sep 2026) found 6 p.m. to 11 p.m. local time strongest and 12 p.m. to 5 p.m. weakest, and says there's "no single best time" ([Buffer: best time to post](https://buffer.com/resources/best-time-to-post-on-tiktok/)). **B**. The reliable source is the account's own Analytics, **"Most active times"** (last 7 days) ([CA](https://www.tiktok.com/creator-academy/en/article/analytics-tool-video-performance)). **A**
- **Language:** the author's language setting and the viewer's device language are ranking inputs ([rec-system page](https://www.tiktok.com/safety/en/policies-and-engagement/recommendation-system)). **A**. Taglish captions with the English keyword ("how to connect lightstick", "Weverse", "official") match both PH viewers and English searches.
- **PH LIVE selling:** TikTok and DTI are training MSMEs in live selling (Aug and Dec 2024 Newsroom PH, above). **A**, promotional. No citable data on PH TikTok LIVE conversion or norms was found. **C**

---

## 5. Cross-posting to Facebook Reels, Instagram Reels and YouTube Shorts

| Platform | What it says about reposted, watermarked or "original" content | Source | Rating |
|---|---|---|---|
| **TikTok** | Penalizes *someone else's* watermark or unedited reuse (section 4). Posting your own original first elsewhere is not named as a problem. | [CG](https://www.tiktok.com/community-guidelines/en/integrity-authenticity), [CA](https://www.tiktok.com/creator-academy/en/article/tiktok-originality-policy) | A |
| **Facebook** (Jul 14 2025) | Accounts that repeatedly reuse others' content face "reduced distribution across all their shared content" and lose monetization. For duplicates, "we will reduce the distribution of copies so the original content creator receives appropriate visibility." Advice: "avoid using watermarks that are clearly from third parties". "Simply combining clips together or adding a watermark is insufficient" as an edit. | [Facebook Creators blog](https://creators.facebook.com/blog/combating-unoriginal-content) | A |
| **Instagram** (May 31 2023) | Less recommended: "low-resolution or watermarked reels, reels that are muted or contain borders, reels that are majority text, or reels that have already been posted on Instagram." | [Instagram ranking explained](https://about.instagram.com/blog/announcements/instagram-ranking-explained) | A (2023; later originality updates not verified here) |
| **YouTube** (Jul 15 2025) | "Repetitious content" was renamed "inauthentic content" (mass-produced, template AI). "Reused content" means *others'* content "without adding significant original commentary." Shorts that are "reuploading other creators' content from YouTube or other platform" can't earn revenue share. Shorts can now run up to 3 minutes, and Shorts view counting changed on Mar 31 2025. No YouTube help page found that penalizes a creator's *own* TikTok-watermarked upload; that's commonly claimed but **unverified**. | [YPP policies](https://support.google.com/youtube/answer/1311392), [Shorts monetization](https://support.google.com/youtube/answer/12504220), [Shorts help](https://support.google.com/youtube/answer/10059070) | A |
| **Independent** | "There's no clear evidence that major platforms directly penalize creators for crossposting... recycled content with visible watermarks or poor platform fit may perform worse." No data given. | [Buffer, May 2026](https://buffer.com/resources/cross-posting/) | C |
| **Benchmark** | Average views for 5K to 10K accounts: TikTok 945, Reels 1,182, Shorts 22,000. Shorts numbers are inflated by YouTube's broader view counting since Mar 2025, so don't compare them 1:1. | [Socialinsider](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/) | A (definitions differ) |

**Verdict:** cross-posting your **own** video helps if you upload a **clean master file** (exported from CapCut or the camera roll, not downloaded from TikTok with the watermark). Re-type the caption natively on each platform. Don't post the same video twice on the same platform. Evidence: **A** for the watermark and duplicate rules, **C** for "it helps".

---

## 6. What this means for a small K-pop shop

Ranked by expected impact times evidence strength. Own-data notes refer to the 2026-10-14 scrape.

### Do (ranked)

1. **Make search-first "how to" videos, in a series.** Topics: connect lightstick X to the app; fix "can't pair"; Bluetooth vs concert mode; stand setup; how installment/hulugan works; how a GO works from order to pickup; how to tell an official lightstick from a fake. Say the exact phrase out loud in the first seconds, put it as on-screen title and cover text, and write it in the caption in plain Taglish plus the English keyword. Use 3 to 5 relevant hashtags, no "#fyp" spam.
   *Evidence:* Search ranks on relevance from captions, on-screen text and voiceover (A); content-gap tools exist (A); own hits (C); scraped top results for the same query reach 165K to 454K (C).
2. **Mine the shop's own search data every week.** Check Analytics, Traffic source, **Search queries** (90 days), and Creator Search Insights, **Content gap** and **Searches by followers** (needs 1K followers, which the shop has). Turn real queries into the next videos. *Evidence:* A.
3. **Hook with the payoff, cut every pause, add captions.** Open on the result ("Ito na yung lightstick na naka-connect, step by step"), change the shot every few seconds, and add subtitles (over 30% watch muted). *Evidence:* TikTok Hook-Hold-Act guide and mute stat (A); retention metrics are what TikTok scores (A).
4. **Film real fan moments with the owner as narrator.** Concert reactions, opening the box from Korea, packing orders, a customer receiving a lightstick (with permission). The owner's face, voice and opinion must be most of the video. Use short performance cuts only, never full songs or other fans' fancams. *Evidence:* the original-commentary rule (A); own concert hit with 226K plays, 4,914 saves and 1,569 shares (C); packing-order videos with millions of views in scraped search (C).
5. **Answer buyer comments with video replies.** One "reply day" a week. *Evidence:* TikTok advice (A); the installment reply got 42.5K plays (C).
6. **Post 3 to 5 times a week, steadily.** For example: 2 search tutorials, 1 fan moment, 1 arrival or unboxing with price in the caption, plus one LIVE. Batch-film on one day and schedule in TikTok Studio web (15 minutes to 10 days ahead; scheduled posts can't be edited. Corrected 2026-10-14, see 08-fact-check claim 14). *Evidence:* Buffer (A); TikTok routine guide (A).
7. **Turn on the content disclosure toggle ("Your brand") on every sales post and LIVE.** *Evidence:* required, and non-disclosure can cut visibility (A).
8. **Run a weekly 60 to 80-minute LIVE as a 4 to 6-week test,** with sales going through TikTok Shop. Announce it the day before with a short video. Use the Q&A, unboxing and troubleshooting formats. Track viewers, follows and orders per LIVE. *Evidence:* TikTok length guidance (A); off-platform rule (A); PH outcomes unknown (C).
9. **Cross-post clean masters to Facebook Reels** (biggest PH reach) and YouTube Shorts. Keep Messenger as the place where GO orders are confirmed. *Evidence:* DataReportal (A); Meta and Instagram watermark rules (A).
10. **Review retention graphs monthly.** Find the second where viewers drop and fix that pattern next time. *Evidence:* TikTok analytics guidance (A).

### Don't (ranked)

1. **Don't make price lists and "WTS / LFB" slideshows the main content.** Turn them into a 20 to 40 s on-hand video (hold the item, switch it on, say the price) and keep the full list in the caption or pinned comment. *Evidence:* low-quality slides and images are flagged (A); video gets 5x the views of images (A); own slideshows got 442 to 1,523 views (C).
2. **Don't repost others' content:** agency teasers, Weverse photos, other sellers' photos, fan-site clips, anything with someone else's logo. *Evidence:* FYF-ineligible (A).
3. **Don't send buyers off-platform during a LIVE** ("DM to mine", "fill out the form"). Use the Shop showcase. *Evidence:* A.
4. **Don't use engagement bait or fake scarcity:** like-for-like, "follow to join", invented "2 slots left". *Evidence:* FYF-ineligible (A); also the shop's own no-hype rule.
5. **Don't use AI voices, AI faces, or AI idol images, ever.** An AI idol "recommending" the shop is a removal under policy, not just bad taste. *Evidence:* A.
6. **Don't stuff keywords or hide tiny text.** Don't use 10+ hashtags. *Evidence:* A.
7. **Don't use trending K-pop songs on sales posts.** Use the Commercial Music Library or original audio. *Evidence:* A.
8. **Don't download a TikTok (with watermark) to repost on Facebook or Instagram.** *Evidence:* A.
9. **Don't delete old evergreen tutorials.** *Evidence:* none for deleting (C); they're search assets.
10. **Don't offer random-pull, lucky-draw or "mystery" bundles on TikTok** until the Shop and policy check is done. *Evidence:* mystery-value products are restricted (A); applicability to photocard pulls is unclear.

---

## 7. Myths to ignore

| Myth | What the evidence says | Rating |
|---|---|---|
| "Add #fyp / #foryou / #viral to get on the For You page." | TikTok: a long hashtag list doesn't help; use relevant, accurate words ([CA](https://www.tiktok.com/creator-academy/en/article/Getting-discovered-with-Search)). No source shows #fyp works. | A |
| "Hide keywords as tiny or off-screen text to rank in Search." | Can get the video "flagged for spam" (same source). | A |
| "You're shadowbanned." | FYF-ineligibility is shown in analytics, and Account check exists ([CA](https://www.tiktok.com/creator-academy/en/article/video-not-recommended)). Low views usually mean low retention or engagement. TikTok: "it doesn't necessarily mean it wasn't recommended." | A |
| "Every video gets a 200 to 300-view test batch, then dies." | No primary source. The real mechanics are per-viewer prediction scores plus a large exploration share (50 to 70% of early feeds, Vombatkere 2024). | A against / C for the myth |
| "Follower count decides reach." | Not a direct factor (TikTok 2020). Big accounts do get more views (Socialinsider), but through accumulated signals, not a follower multiplier. | A |
| "Every video must be over 1 minute now." | That's a Creator Rewards payment rule, and it doesn't exist in PH. Length data is correlational. | A |
| "Edit inside the TikTok app or you get less reach." | TikTok: Search performance "won't be impacted" by which editing tool you use. | A |
| "Labeling AI content kills reach." | TikTok: the label won't affect distribution if the content is otherwise compliant. (The shop doesn't use AI anyway.) | A |
| "Deleting flops resets or helps the account." | No primary evidence either way. | C |
| "Taking a break gets you punished." | No evidence of a penalty; fewer posts just means fewer chances (Buffer). | A (inference) |
| "Cross-posting is penalized." | Watermarks and duplicates are penalized on Instagram and Facebook. Your own clean upload is not. | A |
| "There is one magic posting time." | Buffer: "there's no single best time." Use the account's own "Most active times." | B / A |
| "Business accounts get secretly less reach." | No primary source. The real Business constraints are the music library and Creator Rewards eligibility. | C |
| "Duets and Stitches are a growth hack." | No reach data. They're excluded from rewards and can read as low-effort if there's no real commentary. | C |

---

## 8. Open questions to verify in the app or Seller Center

1. **Account type:** the scrape shows `commerceUser=false`, `ttSeller=true`. Check Settings, Account. This decides music library access and which features are available.
2. **Creator Search Insights in PH:** type "Creator Search Insights" in search. Does it open, and does the Content gap tab show K-pop or lightstick topics?
3. **TikTok Shop PH rules for official K-pop merch:** brand authorization, category, maximum pre-order days versus the 3 to 8 week GO cycle, and whether random photocard pulls count as "mystery value".
4. **FYF eligibility of recent sales posts:** check Analytics for "not eligible for recommendation" flags on the WTS/LFB slideshows, and run Account check.
5. **Traffic source split:** what share of views on the lightstick tutorials comes from Search vs the For You feed? This is the most useful single number for deciding how much to invest in search content.
6. **PH LIVE norms:** observe 3 to 5 PH K-pop seller LIVEs (length, time of day, how they take orders, whether they use the Shop showcase). That belongs in the competitor research, since no published study covers it.

---

## Sources

**TikTok (primary)**
- Recommendation system (Safety/Transparency): https://www.tiktok.com/safety/en/policies-and-engagement/recommendation-system
- Newsroom, How TikTok recommends videos #ForYou (Jun 18 2020): https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- Community Guidelines ("2026 August" version): https://www.tiktok.com/community-guidelines/en/integrity-authenticity, https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities, https://www.tiktok.com/community-guidelines/en/accounts-features, https://www.tiktok.com/community-guidelines/en/fyf-standards
- Creator Academy (accessed 2026-10-14): originality policy, video-not-recommended, video-traffic-the-for-you-feed, driving-video-traffic-search, Getting-discovered-with-Search, search, search-insights-content-gap, analytics-tool-video-performance, RPM-understanding-the-four-key-factors, eligibility, monetization-creativity-program-qualified-view, tool-one-minute-feature-overview, building-a-sustainable-posting-routine, build-a-repeatable-format, tool-playlists-intro, the-importance-of-sound, choosing-background-music, elements-of-tiktok-video, avoid-common-creation-mistakes, ai-generated-content-label, Create-unforgettable-reaction-content, Going-LIVE, LIVE-for-your-business-engage-convert-and-grow, guidelines-recommendation-system-intro, Creating-high-quality-videos-on-TikTok. Base URL: `https://www.tiktok.com/creator-academy/en/article/<slug>`
- Newsroom: Creator Search Insights (Mar 13 2024) https://newsroom.tiktok.com/en-us/creator-search-insights; Creator Rewards Program (Mar 18 2024) https://newsroom.tiktok.com/en-us/introducing-the-new-creator-rewards-program; AI transparency and C2PA (May 9 2024) https://newsroom.tiktok.com/en-us/partnering-with-our-industry-to-advance-ai-transparency-and-literacy; PH enforcement system (Feb 8 2023) https://newsroom.tiktok.com/fil-ph/supporting-filipino-creators-with-an-updated-account-enforcement-system; PH Messaging Ads (Jan 9 2025) https://newsroom.tiktok.com/fil-ph/tiktok-messaging-ads-in-the-philippines; TikTok Shop + DTI (Aug 16 2024) https://newsroom.tiktok.com/fil-ph/tiktok-shop-and-dti-empower-filipino-msmes; DigiCities (Dec 9 2024) https://newsroom.tiktok.com/fil-ph/tiktok-shop-and-gcash-for-business-unlock-msme-growth-across-the-philippines-with-digicities-program
- TikTok for Business: Search Ads https://ads.tiktok.com/business/en-US/blog/introducing-search-ads-campaign; Search growth https://ads.tiktok.com/business/en-US/blog/tiktok-search-ads-incremental-revenue-growth; LIVE best practice (Feb 20 2025) https://ads.tiktok.com/business/en-US/blog/tiktok-live-best-practice; Commercial Music Library https://ads.tiktok.com/help/article/commercial-music-library

**Research and large data studies**
- Vombatkere et al., WWW 2024: https://arxiv.org/abs/2403.12410; UW summary: https://www.washington.edu/news/2024/04/24/tiktok-black-box-algorithm-and-design-user-behavior-recommendation/
- Boeker and Urman, WWW 2022: https://arxiv.org/abs/2201.12271
- Buffer, posting frequency (11.4M posts, Oct 8 2025): https://buffer.com/resources/how-often-should-you-post-on-tiktok/
- Buffer, best time (7.1M posts, Sep 14 2026): https://buffer.com/resources/best-time-to-post-on-tiktok/
- Buffer, video length: https://buffer.com/resources/best-tiktok-video-length/
- Socialinsider, 2026 TikTok Benchmarks: https://www.socialinsider.io/social-media-benchmarks/tiktok
- Socialinsider, TikTok vs Reels vs Shorts (69M videos): https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/
- Metricool 2024 TikTok study: https://metricool.com/tiktok-study-2024/; 2026: https://metricool.com/tiktok-study/
- DataReportal Digital 2026 Philippines: https://datareportal.com/reports/digital-2026-philippines; Digital 2025: https://datareportal.com/reports/digital-2025-philippines
- Momentum Works, Live Commerce in SEA 2026: https://momentum.asia/insights/detail/live-commerce-in-southeast-asia-2026

**Secondary**
- NYT "TikTok Algo 101" via Inverse: https://inverse.com/input/culture/tiktok-internal-docs-reveal-just-how-simple-it-is-to-keep-you-addicted
- TikTok/WARC Gen Z search via Tubefilter: https://www.tubefilter.com/2025/09/10/tiktok-search-engine-ads-new-research/
- Adobe Express 2026 via Search Engine Journal: https://www.searchenginejournal.com/gen-z-preference-for-tiktok-over-google-drops/568199/
- Hootsuite TikTok algorithm (quotes TikTok stats): https://blog.hootsuite.com/tiktok-algorithm/
- Buffer cross-posting: https://buffer.com/resources/cross-posting/

**Meta and YouTube (primary)**
- Facebook, unoriginal content (Jul 14 2025): https://creators.facebook.com/blog/combating-unoriginal-content
- Instagram ranking explained (May 31 2023): https://about.instagram.com/blog/announcements/instagram-ranking-explained
- Meta, Facebook Reels ranking (Jun 19 2026): https://transparency.meta.com/features/explaining-ranking/fb-reels/
- Meta, types of content Facebook demotes (Jul 2 2025): https://transparency.meta.com/features/approach-to-ranking/types-of-content-we-demote/
- YouTube Partner Program policies (inauthentic and reused content, Jul 15 2025): https://support.google.com/youtube/answer/1311392
- YouTube Shorts monetization: https://support.google.com/youtube/answer/12504220; Shorts help: https://support.google.com/youtube/answer/10059070

**Own data (C)**
- `data/raw/tiktok-popular-2026-10-14.json`, `data/raw/tiktok-latest-2026-10-14.json` (Unnie Mart posts)
- `data/raw/competitors/disc_search.json`, `data/raw/competitors/disc_search2.json` (search-result scrape)
