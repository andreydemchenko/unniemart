"""Tests for the banned-phrase checker."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from banned_check import check  # noqa: E402


def rules(text, **kw):
    return {(f.level, f.rule) for f in check(text, **kw)}


def test_clean_caption_passes():
    t = 'May Army Bomb VER.3 ka? Ito po sabi ng official notice para sa BTS Bulacan 💜 #armybomb #armybombv4 #btsbulacan'
    assert check(t) == []


def test_slop_phrases_block():
    assert ('BLOCK', 'slop phrase') in rules('Stay till the end para sa surprise!')
    assert ('BLOCK', 'slop phrase') in rules('This lightstick is a game-changer')
    assert ('BLOCK', 'AI leftover') in rules('Suggested title and hashtags: ...')
    assert ('BLOCK', 'legit claim') in rules('100% legit po kami!')


def test_markdown_stars_only_outside_md():
    assert ('BLOCK', 'AI leftover') in rules('**ON HAND** Engenebong')
    assert ('BLOCK', 'AI leftover') not in rules('**ON HAND** Engenebong', markdown=True)


def test_scarcity_needs_stock_check():
    assert ('BLOCK', 'scarcity') in rules('LAST 2 PCS na lang!')
    assert ('BLOCK', 'scarcity') in rules('3 slots na lang po')
    assert ('BLOCK', 'scarcity') not in rules('LAST 2 PCS na lang!', stock_checked=True)


def test_miss_out_needs_date():
    assert ('BLOCK', 'miss out') in rules("Don't miss out!")
    assert ('BLOCK', 'miss out') not in rules("Don't miss out, DOP is Oct 30")


def test_ai_visuals_block():
    assert ('BLOCK', 'AI or stock visual') in rules('Shot 2: AI voiceover explains the steps')
    assert ('BLOCK', 'AI or stock visual') in rules('use stock footage of a concert')


def test_warnings():
    assert ('WARN', 'hashtag') in rules('cute #fyp #kpop')
    assert ('WARN', 'hashtag') in rules('#a #b #c #d #e #f')
    assert ('WARN', 'fear selling') in rules('Your old one is useless na')
    assert ('WARN', 'price first') in rules('₱2,750 Army Bomb VER.4 pre-order')
    assert ('WARN', 'price first') not in rules('₱300 DP · total ₱2,750 Army Bomb VER.4')


def test_curly_apostrophe():
    assert ('BLOCK', 'slop phrase') in rules('You won’t believe this')
