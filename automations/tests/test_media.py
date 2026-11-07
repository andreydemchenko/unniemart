import datetime as dt
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import media  # noqa: E402

NOW = dt.datetime(2026, 10, 15, 4, 0, tzinfo=dt.timezone.utc)


def own(i, views, date, slideshow=False):
    return {'id': str(i), 'date': f'{date}T08:00:00+00:00', 'url': f'https://www.tiktok.com/@unniemart_/video/{i}',
            'views': views, 'caption': f'video {i}\n#tags', 'slideshow': slideshow}


def project(tmp_path, n=50):
    (tmp_path / 'data' / 'state').mkdir(parents=True)
    vids = {str(i): own(i, i * 10, f'2026-{1 + i % 9:02d}-{1 + i % 27:02d}') for i in range(1, n + 1)}
    vids['999'] = own(999, 225400, '2025-01-25')                          # an old hit
    vids['998'] = own(998, 5, '2020-01-01', slideshow=True)               # old, unseen, a photo post
    (tmp_path / 'data' / 'state' / 'own_videos.json').write_text(json.dumps(vids))
    (tmp_path / 'data' / 'stats').mkdir()
    (tmp_path / 'data' / 'stats' / '2026-W42.json').write_text(json.dumps({'videos': [own(50, 777, '2026-10-01')]}))
    (tmp_path / 'data' / 'peers').mkdir()
    (tmp_path / 'data' / 'peers' / '2026-W42.json').write_text(json.dumps({'outliers': [
        {'id': '555', 'account': 'koppashop', 'url': 'https://www.tiktok.com/@koppashop/video/555', 'views': 9000,
         'caption': 'peer', 'date': '2026-09-01T00:00:00+00:00'}]}))
    (tmp_path / 'content' / 'ideas').mkdir(parents=True)
    (tmp_path / 'content' / 'ideas' / '2026-W43.md').write_text(
        'sources: [O24](https://www.tiktok.com/@unniemart_/video/998), [P1](https://www.tiktok.com/@seoulstop/video/777)')
    (tmp_path / 'strategy').mkdir()
    (tmp_path / 'strategy' / 'plan.json').write_text(json.dumps({'week': {'kinds': [{'examples': ['999', '1']}]}}))
    return tmp_path


def test_which_videos(tmp_path):
    w = media.wanted(project(tmp_path))
    mine = {k for k, v in w.items() if v['mine']}
    assert '999' in mine and '998' in mine                       # most watched; pointed to by a brief
    assert len([k for k in mine if k not in ('999', '998')]) >= media.NEWEST
    assert w['50']['views'] == 777                                 # this week's numbers beat the old list
    assert w['50']['cap'] == 'video 50'                            # first line only
    assert w['555']['acc'] == 'koppashop' and not w['555']['mine']
    assert w['777']['acc'] == 'seoulstop' and w['777']['url'].endswith('/777')
    assert w['998']['slideshow'] and not w['999']['slideshow']


def test_what_still_needs_fetching():
    want = {'1': {'mine': True}, '2': {'mine': True, 'slideshow': True}, '3': {'mine': False}, '4': {'mine': True},
            '5': {'mine': True}, '6': {'mine': True}, '7': {'mine': True}}
    index = {
        '1': {'thumb': 't/1.webp', 'video': 'v/1.mp4'},                                  # done
        '2': {'thumb': 't/2.webp'},                                                      # photo post: no video
        '3': {'thumb': 't/3.webp'},                                                      # someone else's: video too
        '4': {'thumb': 't/4.webp', 'no_video': True},                                    # TikTok plays it
        '5': {'fail': {'n': 1, 'at': (NOW - dt.timedelta(hours=2)).isoformat()}},          # wait a day
        '6': {'fail': {'n': 3, 'at': (NOW - dt.timedelta(days=5)).isoformat()}},           # gave up
    }
    assert media.todo(want, index, NOW) == [('7', True), ('3', True)]      # hers first
    index['5']['fail']['at'] = (NOW - dt.timedelta(days=1)).isoformat()
    assert ('5', True) in media.todo(want, index, NOW)


def test_cover_picture_and_fast_start(tmp_path):
    assert media.cover_url({'thumbnails': [{'id': 'dynamicCover', 'url': 'a'}, {'id': 'originCover', 'url': 'b'}]}) == 'b'
    assert media.cover_url({'thumbnails': [], 'thumbnail': 'c'}) == 'c'
    from PIL import Image
    buf = io.BytesIO()
    Image.new('RGB', (540, 960), (200, 30, 60)).save(buf, 'JPEG')
    color, w, h = media.make_thumb(buf.getvalue(), tmp_path / 't' / '1.webp')
    assert (w, h) == (360, 640) and color.startswith('#c') and (tmp_path / 't' / '1.webp').stat().st_size < 20000
    good, bad = tmp_path / 'a.mp4', tmp_path / 'b.mp4'
    good.write_bytes(b'\0\0\0\x20ftypisom' + b'moov' + b'x' * 100 + b'mdat')
    bad.write_bytes(b'\0\0\0\x20ftypisom' + b'mdat' + b'x' * 100 + b'moov')
    assert media.fast_start(good) and not media.fast_start(bad)


def test_index_keeps_files_and_takes_new_numbers():
    index = {'1': {'thumb': 't/1.webp', 'video': 'v/1.mp4', 'views': 10, 'cap': 'old'}}
    want = {'1': {'acc': 'unniemart_', 'url': 'u', 'mine': True, 'cap': '', 'views': 25, 'date': '2026-10-01'}}
    out = media.merge(index, want)
    assert out['1'] == {'thumb': 't/1.webp', 'video': 'v/1.mp4', 'views': 25, 'cap': 'old', 'acc': 'unniemart_',
                        'url': 'u', 'mine': True, 'date': '2026-10-01'}


def test_heavy_videos_are_made_small(tmp_path):
    import shutil, subprocess
    import pytest
    if not shutil.which('ffmpeg'):
        pytest.skip('no ffmpeg')
    big = tmp_path / 'big.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=1080x1920:rate=30', '-t', '2',
                    '-c:v', 'libx264', '-b:v', '6M', '-pix_fmt', 'yuv420p', str(big)], check=True)
    out = tmp_path / 'v' / '1.mp4'
    out.parent.mkdir()
    assert media.lean(big, out)
    kbps, h = media.probe(out)
    assert h == media.LEAN_H and kbps < 1000 and media.fast_start(out)
    index = {'1': {'video': 'v/1.mp4'}, '2': {'video': 'v/2.mp4'}}           # 2: file gone, left alone
    assert media.shrink_old(index, tmp_path) == 1 and index['1']['lean'] and 'lean' not in index['2']
