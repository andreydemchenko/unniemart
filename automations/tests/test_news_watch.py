"""Tests for the news watch filter and parsers. Headlines are real ones seen on 2026-10-14."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import news_watch as N  # noqa: E402


def prio(title, kind='news', broad=True):
    return N.classify(title, kind, broad)[0]


def test_groups_short_names_are_case_sensitive():
    assert N.match_groups("IVE's Jang Wonyoung") == ['IVE']
    assert N.match_groups("I've got five reasons") == []
    assert N.match_groups('Army Bomb VER.4') == ['BTS']
    assert N.match_groups('JEONGHAN X JOSHUA DREAMSCAPE POP-UP') == ['SEVENTEEN']
    assert N.match_groups('a new phone for the PH market') == []


def test_urgent_lightstick_sale_and_ph_shows():
    assert prio('ENHYPEN OFFICIAL LIGHT STICK VER.2 (RENEWAL EDITION) Release Notice') == 'urgent'
    assert prio('NCT WISH Announce Manila Stop For Concert Tour In 2027') == 'urgent'
    assert prio('BTS adds third Bulacan concert for ARIRANG tour') == 'urgent'


def test_lightstick_guide_is_not_urgent():
    t = "[NOTICE] ENHYPEN WORLD TOUR 'BLOOD SAGA' IN MACAU Official Light Stick & Band User Guide"
    assert prio(t) == 'normal'


def test_broad_feeds_drop_noise():
    assert prio('BTS’s “Hooligan” Becomes Their 3rd MV To Hit 100 Million Views') is None
    assert prio('Vilma Santos, Edgar Mortiz share concert stage again') is None
    assert prio('[NOTICE] 2027 Girls\' Generation SEASON’S GREETINGS SALES NOTICE') is None
    assert prio('TREASURE Announces November Comeback Date And Details For SHOCK') == 'normal'


def test_targeted_search_keeps_low():
    assert prio('Something about K-pop fans', broad=False) == 'low'


def test_ticket_sites():
    assert prio('2026 LE SSERAFIM TOUR PUREFLOW IN MANILA DECEMBER 5', 'ticket') == 'urgent'
    assert prio('JASON MRAZ ASIA TOUR 2026 IN MANILA', 'ticket') == 'low'


def test_reddit_keeps_fan_questions_only():
    assert prio('Is this Army Bomb fake? Bought it on Shopee', 'reddit') == 'normal'
    assert prio('Daily discussion thread', 'reddit') is None


def test_parse_google_news_strips_publisher():
    xml = b"""<rss><channel><item><title>NCT WISH Manila stop - Soompi</title><link>https://news.google.com/x</link>
    <pubDate>Tue, 13 Oct 2026 10:00:00 GMT</pubDate><source url="https://soompi.com">Soompi</source></item></channel></rss>"""
    [it] = N.parse_feed(xml)
    assert it['title'] == 'NCT WISH Manila stop'
    assert it['publisher'] == 'Soompi'
    assert it['published'].year == 2026


def test_parse_atom():
    xml = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Is my lightstick fake?</title>
    <link href="https://reddit.com/r/kpophelp/1"/><updated>2026-10-14T01:00:00+00:00</updated></entry></feed>"""
    [it] = N.parse_feed(xml)
    assert it['link'].endswith('/1') and it['published'].day == 14


def test_parse_smtickets_embedded_json():
    page = ("var original_array = JSON.parse('[{\"event_id\":\"18350\",\"event_long_title\":\"2026 LE SSERAFIM TOUR "
            "PUREFLOW IN MANILA DECEMBER 5\",\"event_date_time\":\"2026-12-05\"}]');")
    [ev] = N.parse_smtickets(page)
    assert ev['link'].endswith('/18350') and 'LE SSERAFIM' in ev['title']


def test_parse_weverse_notices_filters_artist():
    page = ('{"notices":[{"id":1,"title":"Shop promo","artistId":0,"artistName":"Weverse Shop",'
            '"displayStartAt":"2026-10-12T11:00:00+09:00"},'
            '{"id":2,"title":"[Notice] ENHYPEN LIGHT STICK","artistId":10,"artistName":"ENHYPEN",'
            '"displayStartAt":"2026-10-13T11:00:00+09:00"}]}')
    [n] = N.parse_weverse_notices(page, 10)
    assert n['link'].endswith('/artists/10/notices/2')


def test_dedupe_keeps_highest_priority():
    a = {'key': 'x', 'priority': 'low', 'published': None}
    b = {'key': 'x', 'priority': 'urgent', 'published': None}
    assert N.dedupe([a, b]) == [b]
