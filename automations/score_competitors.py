#!/usr/bin/env python3
"""Score competitor TikTok scrapes (data/raw/competitors/prof_*.json) -> data/competitor-videos.csv.
Outlier score = video views / that account median. Format = first matching caption rule, or a manual override
from data/raw/competitors/format_overrides.json (set after checking covers). Used for research/03-competitors.md."""
import json, re, statistics as st, datetime as dt, collections, csv

RAW = '/Users/macbookpro/Documents/Projects/unniemart/data/raw/competitors'
OUT_CSV = '/Users/macbookpro/Documents/Projects/unniemart/data/competitor-videos.csv'
SP = RAW  # overrides + summary JSON live next to the raw scrapes
NOW = dt.datetime(2026, 10, 14, tzinfo=dt.timezone.utc)

# account metadata: group, country, seller model, in-niche flag
ACC = {
    'poppeshop':          ('PH seller', 'PH', 'Mall cabinets + online, TikTok LIVE', True),
    'seoulstop':          ('PH seller', 'PH', 'Physical stores (Manila) + Shopee/website', True),
    'nabishoppe':         ('PH seller', 'PH', 'Pasabuy/onhand, TikTok LIVE, Shopee; closing down Sep 2026', True),
    'ynawrap':            ('PH seller', 'PH', 'Onhand + PH GO pre-orders, TikTok Shop basket, carrd order form', True),
    'chulien07':          ('PH seller', 'PH', 'Aling Chulien: physical store (Malolos) + Shopee + LIVE', True),
    'forever9ph':         ('PH seller', 'PH', 'Mall stalls + onhand/pre-order, LIVE selling, yellow basket', True),
    'joahaeyoph':         ('PH seller', 'PH', 'Physical store (Angeles) + KR pasabuy, DM orders', True),
    'iammist.k':          ('PH seller', 'PH', 'PH GOM, sells via X/Twitter shop (dormant since 2024)', True),
    'meromiph':           ('PH seller', 'PH', 'Meromi K-pop store backup acct, LIVE selling + basket', True),
    'recordplanet_ph':    ('PH seller', 'PH', 'Record Planet mall store (Market! Market!)', True),
    'kpopmerch.official': ('SEA seller', 'KR/SEA', 'Shopee/Lazada store shipping to PH/ID/SG/MY/TH/TW', True),
    'chylcartz':          ('PH seller', 'PH', 'Small photocard seller, Shopee (active 2023 only)', True),
    'nelfoever':          ('PH seller', 'PH', 'Small photocard seller ("carts"), PWM creator', True),
    'purpledolphinshop':  ('PH seller (adjacent)', 'PH', 'PH GOM for Thai GMMTV merch, DM orders, X feedback tag', True),
    'chipopstore':        ('SEA seller', 'ID', 'Indonesian photocard/album store, TikTok Shop yellow basket', True),
    'milky_kshop':        ('SEA seller', 'ID', 'Indonesian K-shop (lightsticks), Shopee/Tokopedia/TikTok Shop', True),
    'koppashop':          ('Off-niche', 'PH', 'Korean ramyeon/food shop in Manila (not K-pop merch)', False),
    '0102zyoungwon':      ('Non-PH creator', 'CA', 'PWM ASMR photocard packer (kiyomidesign.ca)', True),
    'pinkcardz':          ('Non-PH creator', 'US', 'Photocard seller/PWM creator (hiatus since 2024)', True),
    'heyseokjinnie':      ('Non-PH creator', 'NL', 'K-pop collector: unboxings, lightsticks, concerts', True),
    'lilinanaunboxings':  ('Non-PH creator', 'PL', 'Album unboxings', True),
    'iamurgrace_':        ('Non-PH creator', 'US', 'Fan creator: lightstick tutorial, merch DIY, concerts', True),
    'unniemart_':         ('Client (baseline)', 'PH', 'Unnie Mart 2: PH GO + onhand, DM/reservation form, TikTok Shop', True),
}

# Ordered rules: first match wins for primary format.
RULES = [
    ('LIVE selling clip/promo', r'join our live|live selling|livehighlights|tiktoklive|live later|live tonight|live today|start live|our live|during live|nag live|mag live|live clearance|sa live|pm live|live price|live schedule|live ko|live\b.*(freebies|flash sale)|abangan din aming live'),
    ('Lightstick tutorial', r'connect|tutorial|pasang baterai|how i added|how to pair|pair / use|user guide'),
    ('Lightstick unbox/review', r'(lightstick|light stick|loghtstick|fanlight|army ?bomb|bong|mixx stick|lightiny).*(unbox|rating|review|perbandingan|perbedaan|comparison|vs)|(unbox|rating|perbandingan|perbedaan).*(lightstick|light stick|loghtstick|fanlight|army ?bomb|bong)|rating some of the kpop lightsticks'),
    ('Pack-with-me / packing / supplies', r'\bpack\b|packing|pwm|packwithme|organi[sz]e|packaging|this is how we pack|temenin pack|blind pack|haul|supplies|unboxing freebies|restock freebies|freebies check|unboxing & organize'),
    ('Album/merch unboxing', r'unbox|unpack|pulls?\b|inclusions|unlocked'),
    ('Concert/idol/fan moment', r'concert|world ?tour|fate tour|bts in |tour in |meet (heeseung|them)|got to meet|fanmeet|fan meet|fan event|stage|arena|ziggo|brussels|busan concert|blood saga|katseye in|svt fest|blink run|parking|lima day|chicago day'),
    ('Collection showcase/rating', r'collection tour|my .*collection|all \(korean\) bts|i own|my bts korean album|rating'),
    ('POV/humor/relatable', r'\bpov\b|be like|when you|when your|when they|how to say no|kidnap|bank account|acting broke|paycheck|merch addiction|money can|ifykyk|bestied|calm down|nothing can stop|nagaway|spawn point|balance your spending|uhmm how bout|2nd gen stan|i feel so old|merch ban who|jebal|set pa nga|supremacy|situation rn|hard to be surrounded|collector be like|how about both|you will buy me|did the math|anong seats|on or before the dop|what do you wanna|tingin gusto|di namin kaya|if there.s a will|literally!!|luluhuran|ngi|wait .til the end'),
    ('Sale/promo/giveaway', r'sale\b|sale!|% ?off|discount|promo|payday|flash|free pc|freebies?|giveaway|buy 1|take 1|clearance|paubos|pamigay|voucher|lucky draw|everything must go|daebak deals|as low as|ten ten|10\.10|9\.9|6\.6|11\.11|winners'),
    ('Pre-order / GO announcement', r'pre-?order|preorder|ph ?go|wts|lfb|downpayment|down payment|\bdp\b|\beta\b|order form|reserve|reservation|pooling|collecting orders|open for|now accepting orders|secured kay supplier|purchase assistance|pasabuy|ipasabay|long dop|dop\b'),
    ('Arrival/onhand/restock showcase', r'new arrival|arrivals|onhand|on hand|on-hand|restock|available|arrived|dumating|readystock|ready stock|in stock|is here|now here|just landed|box from korea|ready to ship|stocks|listed|latest arrival|new albums|3000 pcs|200pcs|150 pcs'),
    ('Store visit/tour/event', r'visit|store tour|tour of our|grand opening|branch|booth|cabinet|open today|we.re open|moving out|new chapter|closed our store|kpop store with me|pop-up|hangout|surprise to our first|new kpop shop|sponsor namin|oras ng store|line up|long line|pick up'),
    ('Trust/proof/feedback', r'trusting|feedback|proof|legit|thank you for checking out|returan|retur'),
    ('Seller life / behind the scenes', r'day in the life|work with me|morning routine|airport|sort ko lang|hirap maging|ang hirap|baha|parcels|wala ako mapost|flop|label'),
    ('Fan content (edits/bias/memes)', r'birthday|day🎂|ethereal|bias|chokehold|challenge|duet|award|goodnight|twin|melet|bonyok|cakep|magazine|larr|edit|cover by|doggo|queens are back|manligaw|manliligaw|tens on tens|ryul|kilig|insane energy|music award|stream|jyp'),
    ('Product showcase / generic sell', r'order yours|grab yours|message (us|me)|check ?out|pa-?budol|budol|twitter shop|twt|link in bio|choose your bias|to mine|smini|dm (us|to)|get yours|shop|album|photocard|pc\b|lightstick|merch|official|sealed|php|₱|basket|keranjang|kerkun'),
    ('Q&A/explainer', r'q&a|what to check|explanation|which version|versions|has how many|which one are you'),
]

def classify(text, v=None):
    t = (text or '').lower()
    if not t.strip() or re.fullmatch(r'(\s*#\S+)*\s*', t):
        if v is not None and v.get('hasTikTokShopProduct'):
            return 'Product showcase / generic sell'
    for name, pat in RULES:
        if re.search(pat, t):
            return name
    return 'Other/unclear'

def secondary_tags(v):
    t = (v.get('text') or '').lower()
    tags = []
    if v.get('isSlideshow'): tags.append('slideshow')
    if t.startswith('replying to') or 'reply to @' in t or 'membalas @' in t: tags.append('comment-reply')
    if re.search(r'\bpov\b', t): tags.append('POV')
    if '?' in t[:120]: tags.append('question-hook')
    if re.search(r'₱|php|\bp\d|harga|\d+rb', t): tags.append('price-in-caption')
    if re.search(r'dm (us|to|me)|message us|send us dm|dm/', t): tags.append('DM-CTA')
    if re.search(r'basket|keranjang|kerkun|check ?out|shopee|shapi|orange app|tiktok shop|tokped|lazada', t): tags.append('shop-link-CTA')
    if re.search(r'comment', t): tags.append('comment-CTA')
    if v.get('hasTikTokShopProduct'): tags.append('tiktok-shop-product')
    if v.get('isPinned'): tags.append('pinned')
    return tags

# manual overrides after reviewing captions + covers (video id -> format)
OVERRIDES = {}
try:
    OVERRIDES = json.load(open(f'{SP}/format_overrides.json'))
except FileNotFoundError:
    pass

def main():
    items = []
    for fn in ['prof_a.json', 'prof_b.json', 'prof_c.json']:
        items += json.load(open(f'{RAW}/{fn}'))

    by = collections.defaultdict(list)
    for v in items:
        by[v['authorMeta']['name']].append(v)

    rows, accounts = [], []
    for name, vs in by.items():
        grp, country, model, niche = ACC[name]
        a = vs[0]['authorMeta']
        plays = [v['playCount'] for v in vs]
        med = st.median(plays)
        dates = sorted(dt.datetime.fromisoformat(v['createTimeISO'].replace('Z', '+00:00')) for v in vs)
        nonpinned = sorted(dt.datetime.fromisoformat(v['createTimeISO'].replace('Z', '+00:00')) for v in vs if not v.get('isPinned'))
        span_days = max((nonpinned[-1] - nonpinned[0]).days, 1) if len(nonpinned) > 1 else 1
        last90 = sum(1 for d in dates if (NOW - d).days <= 90)
        eng = [ (v['diggCount'] + v['commentCount'] + v['shareCount']) / v['playCount'] for v in vs if v['playCount'] > 0]
        fmt_counts = collections.Counter()
        for v in vs:
            f = OVERRIDES.get(v['id']) or classify(v.get('text'), v)
            fmt_counts[f] += 1
            age = (NOW - dt.datetime.fromisoformat(v['createTimeISO'].replace('Z', '+00:00'))).days
            rows.append({
                'account': name, 'group': grp, 'country': country, 'in_niche': niche,
                'followers': a.get('fans'), 'account_median_views': med,
                'video_id': v['id'], 'url': v['webVideoUrl'], 'created': v['createTimeISO'][:10], 'age_days': age,
                'views': v['playCount'], 'likes': v['diggCount'], 'comments': v['commentCount'],
                'shares': v['shareCount'], 'saves': v.get('collectCount'),
                'outlier_score': round(v['playCount'] / med, 2) if med else None,
                'format': f, 'tags': '|'.join(secondary_tags(v)),
                'media': 'slideshow' if v.get('isSlideshow') else 'video',
                'duration_s': v['videoMeta'].get('duration'),
                'pinned': bool(v.get('isPinned')),
                'tiktok_shop_product': bool(v.get('hasTikTokShopProduct')),
                'sound': (v['musicMeta'].get('musicName') or '')[:60],
                'original_sound': bool(v['musicMeta'].get('musicOriginal')),
                'caption': (v.get('text') or '').replace('\n', ' ')[:300],
            })
        accounts.append({
            'account': name, 'group': grp, 'country': country, 'model': model, 'in_niche': niche,
            'followers': a.get('fans'), 'total_videos': a.get('video'), 'scraped': len(vs),
            'median_views': med, 'mean_views': round(st.mean(plays)), 'max_views': max(plays),
            'median_eng_rate': round(st.median(eng) * 100, 1) if eng else None,
            'first': dates[0].date().isoformat(), 'last': dates[-1].date().isoformat(),
            'posts_per_week_window': round((len(nonpinned)) / span_days * 7, 1),
            'posts_last_90d': last90,
            'slideshow_share': round(sum(1 for v in vs if v.get('isSlideshow')) / len(vs) * 100),
            'shop_product_share': round(sum(1 for v in vs if v.get('hasTikTokShopProduct')) / len(vs) * 100),
            'median_to_followers_pct': round(med / a['fans'] * 100, 1) if a.get('fans') else None,
            'top_formats': fmt_counts.most_common(4),
            'bio': (a.get('signature') or '').replace('\n', ' / '),
            'bioLink': a.get('bioLink'),
        })

    rows.sort(key=lambda r: -(r['outlier_score'] or 0))
    with open(OUT_CSV, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    json.dump(accounts, open(f'{SP}/accounts_summary.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(rows, open(f'{SP}/rows.json', 'w'), ensure_ascii=False)
    print('rows', len(rows), 'accounts', len(accounts))


if __name__ == '__main__':
    main()
