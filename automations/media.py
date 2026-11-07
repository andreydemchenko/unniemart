#!/usr/bin/env python3
"""Pictures and videos for the website: a small cover picture for every TikTok the site shows, and her own videos
as small files that start playing at once.

Videos are kept as small copies (540p, at most about 0.8 Mbit/s, index at the front) so they start at once on her
phone, even far from the server. That covers her own videos and the other shops' videos the site points to (watched
only on the private site). Photo slideshows and posts TikTok only gives the sound of play in TikTok's own player.
Uses yt-dlp and ffmpeg: no account, no cost.

Which videos: her newest 40, her 24 most watched, and every video a weekly brief or the plan points to. Other shops'
videos: this week's standouts (peer_watch) and any a brief points to.

Files go to data/media/ (not in git): t/<id>.webp (cover), v/<id>.mp4 (the video), index.json (what's there, with
the caption and views the site shows). site_sync sends the folder to the server. A video that can't be fetched is
tried again the next day, at most 3 times (it may be deleted or private).

Usage:
  python3 automations/media.py             # fetch what's missing (daily and weekly, see run.sh)
  python3 automations/media.py --dry-run   # list what it would fetch
"""
import argparse
import datetime as dt
import io
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA, ROOT, UA, load_json, now_utc, save_json  # noqa: E402

MEDIA = DATA / 'media'
INDEX = MEDIA / 'index.json'
OWN = 'unniemart_'
NEWEST, TOP = 40, 24
THUMB_W = 360
MAX_MB = 25
LEAN_KBPS, LEAN_H = 800, 960         # bigger than this gets made smaller (fast start on a slow phone line)
TRIES = 3
VIDEO_URL = re.compile(r'https://www\.tiktok\.com/@([\w.]+)/video/(\d+)')


def ytdlp():
    return shutil.which('yt-dlp') or str(Path.home() / '.local' / 'bin' / 'yt-dlp')


# ---------- which videos ----------

def first_line(s, n=120):
    return (s or '').strip().split('\n')[0][:n]


def latest(folder):
    files = sorted(Path(folder).glob('2*.json'))
    return load_json(files[-1], {}) if files else {}


def wanted(root=ROOT):
    """Every video the site may show → {id: {acc, url, cap, views, date, mine}}. Her own numbers come from the newest
    weekly stats when they have the video, else from the full list (data/state/own_videos.json)."""
    out = {}

    def add(v, acc, url=None):
        vid = str(v.get('id') or '')
        if not vid:
            return
        cur = out.setdefault(vid, {'acc': acc, 'url': url or v.get('url') or f'https://www.tiktok.com/@{acc}/video/{vid}',
                                   'cap': '', 'views': None, 'date': '', 'mine': acc == OWN})
        for k, f in (('cap', lambda: first_line(v.get('caption'))), ('views', lambda: v.get('views')),
                     ('date', lambda: (v.get('date') or '')[:10])):
            val = f()
            if val not in (None, ''):
                cur[k] = val

    own = load_json(root / 'data' / 'state' / 'own_videos.json', {})
    vids = sorted(own.values(), key=lambda v: v.get('date') or '', reverse=True)
    for v in vids[:NEWEST]:
        add(v, OWN)
    for v in sorted(vids, key=lambda v: -(v.get('views') or 0))[:TOP]:
        add(v, OWN)
    for v in latest(root / 'data' / 'stats').get('videos', []):
        add(v, OWN)
    for o in latest(root / 'data' / 'peers').get('outliers', []):
        add(o, o.get('account') or 'tiktok')

    # anything a brief or the plan points to
    refs = []
    for p in sorted((root / 'content' / 'ideas').glob('*.md')):
        refs += [(m.group(1), m.group(2)) for m in VIDEO_URL.finditer(p.read_text())]
    plan = load_json(root / 'strategy' / 'plan.json', {})
    for k in (plan.get('week') or {}).get('kinds', []):
        refs += [(OWN, str(x)) for x in k.get('examples', [])]
    for acc, vid in refs:
        if vid in out:
            continue
        if acc == OWN and vid in own:
            add(own[vid], OWN)
        else:
            add({'id': vid}, acc)
    for vid, v in out.items():                       # slideshows have no video file to keep
        v['slideshow'] = bool((own.get(vid) or {}).get('slideshow'))
    return out


def todo(want, index, now=None):
    """What still needs fetching: a cover, and the video (not for slideshows). Failed ones wait a day."""
    now = now or now_utc()
    out = []
    for vid, w in want.items():
        have = index.get(vid) or {}
        fail = have.get('fail') or {}
        if fail.get('n', 0) >= TRIES:
            continue
        if fail.get('at') and now - dt.datetime.fromisoformat(fail['at']) < dt.timedelta(hours=20):
            continue
        need_video = not w.get('slideshow') and not have.get('video') and not have.get('no_video')
        if not have.get('thumb') or need_video:
            out.append((vid, need_video))
    return sorted(out, key=lambda x: not want[x[0]]['mine'])          # her videos first


# ---------- fetching ----------

def cover_url(info):
    """The plain cover picture from yt-dlp's info (not the animated one)."""
    thumbs = {t.get('id'): t.get('url') for t in info.get('thumbnails') or []}
    return thumbs.get('originCover') or thumbs.get('cover') or info.get('thumbnail') or next(iter(thumbs.values()), None)


def make_thumb(data, path):
    """Cover bytes → a 360 px wide WebP; returns its average colour (shown while the picture loads)."""
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.width > THUMB_W:
        im = im.resize((THUMB_W, round(im.height * THUMB_W / im.width)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, 'WEBP', quality=72, method=6)
    r, g, b = im.resize((1, 1), Image.BOX).getpixel((0, 0))
    return '#%02x%02x%02x' % (r, g, b), im.width, im.height


def fast_start(path):
    """True when the file can start playing before it has fully arrived (index at the front)."""
    head = path.read_bytes()[:262144]
    m, d = head.find(b'moov'), head.find(b'mdat')
    return m != -1 and (d == -1 or m < d)


def probe(path):
    """(kbit/s, height) of a video file, or (0, 0) when ffprobe can't tell."""
    try:
        p = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=height:format=bit_rate',
                            '-of', 'json', str(path)], capture_output=True, text=True, timeout=60)
        j = json.loads(p.stdout or '{}')
        return int(j.get('format', {}).get('bit_rate') or 0) // 1000, int((j.get('streams') or [{}])[0].get('height') or 0)
    except (OSError, subprocess.SubprocessError, ValueError):
        return 0, 0


def lean(src, dest):
    """A video small enough to start at once: 540p, ~0.8 Mbit/s, index at the front. Light files are only reordered.
    Returns False when ffmpeg isn't there (the file is kept as it is)."""
    if not shutil.which('ffmpeg'):
        return False
    kbps, h = probe(src)
    tmp = dest.with_name(dest.stem + '.lean.mp4')
    if kbps > LEAN_KBPS or h > LEAN_H + 100:
        cmd = ['-vf', f"scale=-2:'min({LEAN_H},ih)'", '-c:v', 'libx264', '-preset', 'slow', '-crf', '27',
               '-maxrate', '700k', '-bufsize', '1400k', '-profile:v', 'main', '-pix_fmt', 'yuv420p', '-g', '60',
               '-c:a', 'aac', '-b:a', '80k']
    elif not fast_start(src):
        cmd = ['-c', 'copy']
    else:
        if src != dest:
            shutil.copyfile(src, dest)
        return True
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), *cmd, '-movflags', '+faststart', str(tmp)],
                   timeout=600, check=True)
    tmp.replace(dest)
    return True


def fetch(vid, w, need_video, media=MEDIA):
    """One video: info (+ the small video file), then the cover. Returns the index fields."""
    import requests
    tmp = media / 'tmp'
    tmp.mkdir(parents=True, exist_ok=True)
    cmd = [ytdlp(), '--no-warnings', '-q', '--no-progress', '--write-info-json', '-o', str(tmp / f'{vid}.%(ext)s'),
           '--max-filesize', f'{MAX_MB}M']
    if need_video:
        cmd += ['-f', 'b[vcodec^=h264][height>=480][height<=1100]/b[vcodec^=h264]', '-S', '+size']
    else:
        cmd += ['--skip-download']
    p = subprocess.run(cmd + [w['url']], capture_output=True, text=True, timeout=240)
    info_path = tmp / f'{vid}.info.json'
    if need_video and p.returncode != 0 and 'format is not available' in (p.stderr or ''):
        # older posts only offer their sound: keep the cover, TikTok's player plays the video
        need_video = False
        cmd[cmd.index('-f'):cmd.index('-f') + 4] = ['--skip-download']
        p = subprocess.run(cmd + [w['url']], capture_output=True, text=True, timeout=240)
        if p.returncode == 0:
            for f in tmp.glob(f'{vid}.*'):
                if f.suffix != '.json':
                    f.unlink()
    if p.returncode != 0 or not info_path.exists():
        raise RuntimeError((p.stderr or p.stdout or 'yt-dlp failed').strip().splitlines()[-1][:160])
    info = json.loads(info_path.read_text())
    info_path.unlink()
    out = {'dur': round(info.get('duration') or 0)}
    if not need_video and not w.get('slideshow') and not (media / 'v' / f'{vid}.mp4').exists():
        out['no_video'] = True
    for k, f in (('cap', lambda: first_line(info.get('description') or info.get('title'))),
                 ('views', lambda: info.get('view_count')), ('likes', lambda: info.get('like_count')),
                 ('comments', lambda: info.get('comment_count'))):
        val = f()
        if val not in (None, ''):
            out[k] = val
    if info.get('timestamp'):
        out['date'] = dt.datetime.fromtimestamp(info['timestamp'], dt.timezone.utc).date().isoformat()

    if need_video:
        got = next((f for f in tmp.glob(f'{vid}.*') if f.suffix == '.mp4'), None)
        if got and got.stat().st_size > 10000:
            dest = media / 'v' / f'{vid}.mp4'
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not lean(got, dest):
                got.replace(dest)
            out.update({'video': f'v/{vid}.mp4', 'lean': True})
        else:
            out['no_video'] = True                  # a photo post, or too big: TikTok's player plays it
    for f in tmp.glob(f'{vid}.*'):
        f.unlink()

    url = cover_url(info)
    if not url:
        raise RuntimeError('no cover picture')
    r = requests.get(url, headers={'User-Agent': UA, 'Referer': 'https://www.tiktok.com/'}, timeout=30)
    r.raise_for_status()
    color, tw, th = make_thumb(r.content, media / 't' / f'{vid}.webp')
    out.update({'thumb': f't/{vid}.webp', 'color': color, 'w': tw, 'h': th})
    return out


def merge(index, want):
    """The site's list: what we know about each wanted video (newest numbers first), files that exist."""
    for vid, w in want.items():
        e = index.setdefault(vid, {})
        for k in ('acc', 'url', 'mine'):
            e[k] = w[k]
        for k in ('cap', 'views', 'date'):
            if w.get(k) not in (None, ''):
                e[k] = w[k]
    return index


def shrink_old(index, media=MEDIA):
    """Videos kept before files were made small: make them small once (same name, so the site needs no change)."""
    n = 0
    for e in index.values():
        f = media / e['video'] if e.get('video') else None
        if not f or e.get('lean') or not f.exists():
            continue
        try:
            if lean(f, f):
                e['lean'] = True
                n += 1
        except (OSError, subprocess.SubprocessError):
            pass
    return n


def main(argv=None):
    ap = argparse.ArgumentParser(description='Covers and small video files for the website')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=200, help='at most this many videos this run')
    a = ap.parse_args(argv)
    index = load_json(INDEX, {})
    want = wanted()
    jobs = todo(want, index)[:a.limit]
    if a.dry_run:
        for vid, v in jobs:
            print(vid, want[vid]['acc'], 'video+cover' if v else 'cover', want[vid]['cap'][:50])
        print(f'{len(jobs)} to fetch, {len(want)} wanted')
        return 0
    got = failed = 0
    for i, (vid, need_video) in enumerate(jobs):
        try:
            fields = fetch(vid, want[vid], need_video)
            index[vid] = {**{k: v for k, v in index.get(vid, {}).items() if k != 'fail'}, **fields}
            got += 1
        except (RuntimeError, OSError, subprocess.SubprocessError, ValueError) as e:
            n = ((index.get(vid) or {}).get('fail') or {}).get('n', 0) + 1
            index.setdefault(vid, {})['fail'] = {'n': n, 'at': now_utc().isoformat(), 'why': str(e)[:160]}
            failed += 1
        except Exception as e:                                          # noqa: BLE001  network etc.: try next run
            index.setdefault(vid, {})['fail'] = {'n': ((index.get(vid) or {}).get('fail') or {}).get('n', 0) + 1,
                                                 'at': now_utc().isoformat(), 'why': type(e).__name__}
            failed += 1
        if i % 10 == 9:
            save_json(INDEX, merge(index, want))
        time.sleep(1)
    save_json(INDEX, merge(index, want))
    made = shrink_old(index)
    if made:
        save_json(INDEX, index)
    shown = sum(1 for v in index.values() if v.get('thumb'))
    videos = sum(1 for v in index.values() if v.get('video'))
    print(f'Media: {got} new, {failed} failed, {made} made smaller · {shown} covers, {videos} videos ready')
    return 0


if __name__ == '__main__':
    sys.exit(main())
