# Design

The website's look (`site/web`). Why it looks this way: `PRODUCT.md`.

## Theme

A calm, modern shop app, like a good banking app (Toss, KakaoBank): cool off-white, a deep navy card for the big
numbers, one cobalt blue for what you can press or what's picked, dark ink for text. Real pictures (video covers,
stock photos) bring the rest of the colour. Light by default (she reads it on her phone in daylight); follows the
phone's dark mode. Not purple, not pink, no glass, no glow. (Oct 15, evening: the warm yellow was dropped, Andrey
found it too bright.)

## Colour (OKLCH, tokens in `site/web/src/app.css`)

| Token | Light | Use |
|---|---|---|
| `--accent` | `oklch(0.55 0.19 259)` cobalt | Primary buttons (Remind, Copy, Save), the active tab, progress, goal dots |
| `--accent-soft` / `--accent-tile` / `--accent-ink` | pale blues, blue text | Tinted chips and buttons (`.btn.tint`, `.chip.accent`), the active tab's pill |
| `--hero`, `--hero-2`, `--on-hero(-2)`, `--hero-week` | deep navy, its tiles, white text, light blue | The money card on Home and Orders, the plan's one line, "Big text at the start", toasts, login |
| `--bg`, `--surface`, `--surface-2/3`, `--line` | cool off-white, tinted to hue 262 | Page, lists, fields, dividers |
| `--ink`, `--ink-2`, `--ink-3` | navy-black to muted | Text levels |
| `--late`, `--late-ink`, `--late-soft` | red | Late payments only |
| `--paid`, `--paid-soft` | green | Paid, posted, live, goal reached |
| `--t0` to `--t4` (+ `-ink`) | soft amber, blue, teal, apricot, lavender | Kinds of things and buyers' avatars (`.tint-0` to `.tint-4`, `.tint-n` neutral) |

Rule: red and green carry state, one meaning each. Red only means late; green only means paid/posted/live/done.
The soft tints only name a kind (shows are blue, releases teal, birthdays apricot, payment days amber) or tell
buyers apart (the same username always gets the same tint). They never warn, and there's no red or green among them.

## Type

Google Sans (self-hosted, 400 to 700, has ₱ and tabular figures), one family for everything. Body 16px, nothing
under 13px (chart labels 12px); titles
26 to 28px/700; the Home total 46px/700; amounts use `font-variant-numeric: tabular-nums`. Plain words, no labels
that explain labels.

## Show, don't tell (Andrey, Oct 14 and 15: "less text, more icons and graphs", "only what she needs")

- Only what she needs, on four pages (Andrey, Oct 15: "no need for so many screens"). Home: money to collect, late
  (with "Remind all"), due this week, next video, to-dos, one "Payment received" button. Orders: to collect, by GO,
  stock. Videos: this week's goal (3 circles), what to film, her videos as pictures, what gets views. Plan: the
  strategy in one line, each kind of video with her own best one, what's coming, four rules, goals; the long
  documents sit behind one "All documents" button.
- Words a child would get (Andrey, Oct 15: "even a child would understand"): "Money to collect", "Due this week",
  "6 people", "9 days late", "Film and post Oct 20 to 22", "Big text at the start", "Steps", "Get ready", "Text under
  the video", "First comment (pin it)", "A normal video gets about 600 views". No "x normal", no lone icons standing
  in for words (a camera icon is not "film on"), no "9d".
- Real pictures where there is a real thing (Andrey, Oct 15): a video is its cover (9:16, views on it, tap to play
  in the site's player), a video idea shows a video like it and the real fan comment behind it, a kind of video
  shows her own best one, a stock item shows its photo once she adds one. Buyers stay initials: no profile pictures
  (their data stays in her sheet). Drawn icons only where there is no picture yet.
- Say a thing once. Rows under a date header don't repeat the date; a GO page doesn't repeat the GO on every row.
  A badge that would be on most tiles ("Last one") is noise: leave it off.
- Amounts become shapes: the split bar under "Money to collect", rings for GO progress, dots for slots, three circles
  for the week's 3 videos, bars for "What gets views". A thin green bar under an amount means part
  of it is paid; the order panel shows each payment as a chip, and the payment screen shows paid, this payment and
  what's left as one bar.
- A chart must answer a question. No chart with one bar, no score from one video (kinds with one video go under
  Other), no ring stuck at 0 (goals are bars with "0 of 12").
- Every kind of thing has a two-tone icon in a soft square (`.glyph`, `<Icon duo>`): video formats, stock items,
  dates by type. K-pop merch has its own drawn icons (`lib/merch-icons.js`: lightstick, photocard, album, can badge,
  picket, slogan, plush keyring, pouch, photocard holder, face cushion) and a colour per kind of merch. Mapping in
  `site/web/src/lib/kinds.js`.
- People are faces: a round initial (`Avatar`); late buyers show "9 days late" in red under the amount.
- Show a number, not a description ("3 videos", "0 of 12").
- Detail and reasons go one tap deeper (the panel, or a fold like "Why this video, and sources").

## Shape and layout

- Radius: 28 (panels, the money card), 24 (lists), 22 (video posters), 18 (fields, tiles), 999 (buttons, chips).
- Pictures first: video ideas are posters (the cover of a video like it, the kind on top, the title at the bottom,
  `IdeaCard`), buyers are round faces in a row (a red ring when late), stock items are photo tiles.
- Lists are white rounded blocks with hairline dividers; rows are 60 to 70px with a date tile on the left, who and
  what in the middle, the amount on the right.
- Phone: a floating bottom bar (Home, Orders, Videos, Plan) with a pale blue pill behind the active icon. Computer
  (900px+): a left sidebar; panels open from the right instead of the bottom.
- Content max width 1080px; documents 68 characters per line.

## Motion (tokens `--ease-out`, `--ease-drawer`, `--ease-move`)

Motion only explains a change:
- Panels slide up from the bottom (460ms, iOS drawer curve) and can be dragged down to close; on a computer they
  slide in from the right. Back on the phone closes them.
- A paid order or a done task leaves its list by fading, then the gap closes (320ms); the rest of the list slides
  up (flip). Ticks draw in; a done task is struck through left to right.
- Charts grow the first time they scroll into view (`inview` in `motion.js`): columns rise from the bottom with a
  small stagger (700ms), rings fill (900ms), the split bar draws in from the left. Later changes slide; nothing
  replays while she's looking. Tapping a column picks it and the others dim.
- When money changes (a payment here, an edit in her sheet), the total's digits roll to the new value (700ms).
- Buttons scale to 0.97 when pressed. Tabs: the dark pill slides to the picked option.
- No page-load choreography. Page switches are a 160ms fade. Reduced motion: fades only.

## Video player (`Player.svelte`)

Black, full screen, the video as large as fits. Videos play from the site (small files, 540p, ~0.8 Mbit/s) with the cover showing until the first
frame (a spinner only after 350 ms). The next and previous video load whole in the background and play from memory
(about half a second); this week's example videos start loading when Home or Videos opens (not on a slow or
data-saving connection). The live security setting allows this (`media-src 'self' blob:`). Tap pauses, sideways swipe or
the arrows go to the next one, a swipe down, Back or Esc closes. If the phone blocks sound, it plays muted and the
speaker button turns sound on. Under the video: the caption without hashtags, views, likes, comments, date, "Open in
TikTok". Photo slideshows (no video file exists) play in TikTok's own player in the same frame.

## Components (`site/web/src/components`)

`Sheet` (panel), `LineRow` (an order: avatar, who, what, amount), `PeopleRail` (buyers side by side), `Avatar`,
`Money` (rolling digits), `Bars` (column chart), `Ring` (progress ring), `StackBar` (split bar), `SlotDots`,
`Calendar` (month grid with dots), `Donut` (shares of a whole), `Mono` (a group badge), `Segmented` (pill tabs),
`Toasts` (dark pill at the bottom, with Undo), `Nav`, `SyncPill` (Live / View only / Offline). Icons: Phosphor bold
for controls (filled when active), Phosphor duotone plus our merch icons for kinds of things.
