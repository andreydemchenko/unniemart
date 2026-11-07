"""What the automations watch. Edit here, not in the scripts.

Groups: tier 1 = the shop's core fandoms (most videos and sales, research 01) plus BTS for the Bulacan season.
Tier 2 = groups the shop has sold, or with a PH show in the calendar (research 06).
Each group has a case-insensitive pattern, an optional case-SENSITIVE pattern (for short all-caps names like IVE or
EXO that would otherwise match normal words), and its Weverse Shop artist id (None if not on Weverse Shop).
"""

GROUPS = [
    # name,          tier, case-insensitive,                                  case-sensitive,               weverse id
    ('ENHYPEN',      1, r'\benhypen\b|\bengene\b|engene ?bong|\bheeseung\b|\bjungwon\b|\bsunghoon\b|\bsunoo\b|\bni-?ki\b',
                     None,                         10),
    ('BTS',          1, r'\bbangtan\b|army ?bomb|\barirang\b|\bjimin\b|\bjungkook\b|\bj-hope\b|\bsuga\b',
                     r'\bBTS\b',                   2),
    ('SEVENTEEN',    1, r'\bseventeen\b|carat ?bong|\bjeonghan\b|\bjoshua\b|\bhoshi\b|\bwoozi\b|\bmingyu\b|\bwonwoo\b|\bseungkwan\b|\bs\.coups\b',
                     r'\bSVT\b|\bCARAT\b|\bBSS\b',     7),
    ('BLACKPINK',    1, r'\bblackpink\b|\bjisoo\b|\bjennie\b',                r'\bBLINK\b',                 32),
    ('TXT',          2, r'tomorrow x together|moa ?bong',                     r'\bTXT\b',                   3),
    ('LE SSERAFIM',  2, r'le ?sserafim|\bfearnot\b',                          None,                         50),
    ('NCT',          2, r'\bnct\b',                                           None,                         None),
    ('EXO',          2, r'\bdoh kyung-?soo\b|\bbaekhyun\b',                   r'\bEXO\b|\bD\.O\.',          None),
    ('TREASURE',     2, None,                                                 r'\bTREASURE\b',              None),
    ('BABYMONSTER',  2, r'\bbabymonster\b',                                   None,                         172),
    ('BIGBANG',      2, r'\bbig ?bang\b|\bg-dragon\b',                        None,                         None),
    ('Stray Kids',   2, r'stray kids',                                        r'\bSKZ\b',                   None),
    ('TWICE',        2, None,                                                 r'\bTWICE\b',                 None),
    ('aespa',        2, r'\baespa\b',                                         None,                         None),
    ('IVE',          2, None,                                                 r'\bIVE\b',                   None),
    ('ATEEZ',        2, r'\bateez\b',                                         None,                         None),
    ('NewJeans',     2, r'\bnewjeans\b',                                      None,                         None),
    ('ILLIT',        2, r'\billit\b',                                         None,                         120),
    ('BOYNEXTDOOR',  2, r'\bboynextdoor\b',                                   None,                         112),
    ('KATSEYE',      2, r'\bkatseye\b',                                       None,                         206),
    ('CORTIS',       2, r'\bcortis\b',                                        None,                         255),
    ('&TEAM',        2, r'&team\b',                                           None,                         None),
    ('ZEROBASEONE',  2, r'\bzerobaseone\b',                                   r'\bZB1\b',                   None),
    ('RIIZE',        2, r'\briize\b',                                         None,                         None),
    ('TWS',          2, None,                                                 r'\bTWS\b',                   None),
]

# Topic signals (case-insensitive). PH_CS is case-sensitive so "PH" doesn't match "phone".
LIGHTSTICK = r'light ?stick|army ?bomb|engene ?bong|carat ?bong|moa ?bong|fanlight|official light'
# A lightstick headline is urgent only with one of these (a user guide or a tour notice is not urgent).
SALE = r'\bsale\b|on sale|release|pre-?order|renewal|available|launch|restock'
PH = r'manila|bulacan|philippine|filipino|pinoy|pasay|quezon city|moa arena|araneta|new frontier|cebu|davao'
PH_CS = r'\bPH\b'
CONCERT = r'concert|tour|fan ?meeting|fan-?con|fancon|live viewing|showcase|cheering party|cine ?fest'
TICKET = r'ticket|presale|pre-sale|seat ?plan|ticketing|selling'
MERCH = r"season'?s greetings|membership|pre-?order|comeback|album|merch|pop-?up|photocard|light ?stick"
KPOP = r'k-?pop|korean|hallyu'

# Google News RSS (research 06, 5a #1-5 plus targeted searches for this season).
# broad=True: the search covers all of K-pop (Weverse hosts ~100 artists), so keep only the shop's groups.
_G = 'https://news.google.com/rss/search?hl=en-PH&gl=PH&ceid=PH:en&q='
GNEWS = [
    ('gnews: K-pop concert Manila', _G + 'K-pop+concert+Manila+when:7d', False),
    ('gnews: K-pop Bulacan / Philippine Arena', _G + 'K-pop+(Bulacan+OR+%22Philippine+Arena%22)+when:7d', False),
    ('gnews: Weverse notices', _G + 'site:weverse.io+notice+when:7d', True),
    ('gnews: Weverse light stick', _G + 'site:weverse.io+%22LIGHT+STICK%22+when:30d', True),
    ('gnews: Weverse Season\'s Greetings', _G + 'site:weverse.io+%22SEASON%27S+GREETINGS%22+when:30d', True),
    ('gnews: Weverse membership', _G + 'site:weverse.io+MEMBERSHIP+when:30d', True),
    ('gnews: ENHYPEN light stick renewal', _G + 'ENHYPEN+%22light+stick%22+when:30d', False),
    ('gnews: allkpop (PH, lightstick)', _G + 'site:allkpop.com+(Manila+OR+Philippines+OR+lightstick)+when:7d', True),
]

# Plain RSS/Atom feeds (research 06, 5a). broad=True means keep only items that mention a watched group or K-pop.
FEEDS = [
    ('Soompi', 'https://www.soompi.com/feed', True),
    ('Koreaboo', 'https://www.koreaboo.com/feed/', True),
    ('kpopofficial', 'https://kpopofficial.com/feed/', True),
    ('Inquirer Entertainment', 'https://entertainment.inquirer.net/feed', True),
    ('GMA Showbiz', 'https://data.gmanetwork.com/gno/rss/showbiz/feed.xml', True),
    ('Philstar Entertainment', 'https://www.philstar.com/rss/entertainment', True),
    ('Rappler Entertainment', 'https://www.rappler.com/entertainment/feed/', True),
    ('ABS-CBN', 'https://www.abs-cbn.com/feed', True),
    ('SM Entertainment newsroom', 'https://www.smentertainment.com/newsroom/feed/', True),
]
SITEMAPS = [
    ('PEP.ph', 'https://www.pep.ph/sitemaps/sitemap-news.xml'),
]
# Reddit rate-limits hard: polled once per run with a pause, fan questions only.
REDDIT = [
    ('Reddit r/kpophelp', 'https://www.reddit.com/r/kpophelp/.rss'),
    ('Reddit r/kpop', 'https://www.reddit.com/r/kpop/.rss'),
]
REDDIT_UA = 'unniemart-newswatch/0.1 (small daily poll)'

# PH ticket sites and promoters: no feeds, so we diff event titles (research 06, 5b).
TICKET_SITES = [
    ('SM Tickets', 'https://www.smtickets.com/events/category/Concert', 'smtickets'),
    ('PULP Live World', 'https://www.pulpliveworld.com/', 'pulp'),
    ('Live Nation PH', 'https://www.livenation.ph/', 'livenation'),
    ('Ticketnet', 'https://www.ticketnet.com.ph/', 'ticketnet'),
]

WEVERSE_NOTICES = 'https://shop.weverse.io/en/shop/USD/artists/{id}/notices'
WEVERSE_NOTICE = 'https://shop.weverse.io/en/shop/USD/artists/{id}/notices/{nid}'

MAX_AGE_DAYS = 10       # dated items older than this are ignored
SEEN_KEEP_DAYS = 90     # how long dedupe remembers a headline
