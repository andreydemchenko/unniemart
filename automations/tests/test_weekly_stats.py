"""Tests for weekly_stats helpers."""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import weekly_stats as W  # noqa: E402


def test_neighbour_normal_centres_and_clamps():
    vids = [{'views': v} for v in range(1, 31)]          # oldest first, views 1..30
    assert W.neighbour_normal(vids, 15) == 16            # window 5..25 -> median 16
    assert W.neighbour_normal(vids, 0) == 11             # clamped to the first 21 -> median 11
    assert W.neighbour_normal(vids, 29) == 20            # clamped to the last 21 -> median 20
    assert W.neighbour_normal(vids[:5], 2) == 3          # fewer than 21 videos: use them all


def test_question_types():
    assert W.question_type('Available pa po?') == 'stock: available pa?'
    assert W.question_type("what's the app po?") == 'setup: connect / app / battery'
    assert W.question_type('legit po ba kayo?') == 'trust: legit / fake'
    assert W.question_type('pwede hulugan?') == 'money: installment / DP'
    assert W.question_type('aabot po ba bago concert?') == 'timing: will it arrive?'
    assert W.question_type('mag kano ang lightstick nila?') == 'price'
    assert W.question_type('may Asa pa po na pc?') == 'stock: available pa?'
    assert W.question_type('ang ganda 😍') is None


def test_iso_week():
    assert W.iso_week(dt.date(2026, 10, 14)) == '2026-W42'


def test_is_clinic():
    assert W.is_clinic('Connecting engenebong V2 to the app.')
    assert not W.is_clinic('WTS / LFB / ENHYPEN / ENCHIN')
