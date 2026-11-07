// TikTok videos as the site shows them: a cover picture, and her own videos as small files that play at once
// (automations/media.py). Other shops' videos, and any not fetched yet, play in TikTok's own player.
import { app } from './live.svelte.js'
import { openSheet } from './ui.svelte.js'

// A caption without its hashtags and @names (they're for TikTok's search, not for reading here)
function words(cap) {
  const w = cap.split('\n')[0].replace(/[#@][^\s#@]+/g, '').replace(/\s+/g, ' ').trim()
  return w || cap.split('\n')[0].trim()
}

export const videoId = (url) => (String(url || '').match(/\/video\/(\d+)/) || [])[1] || null

// One video, from its id or link, with whatever is known about it. extra fills gaps (caption, views...).
export function clip(idOrUrl, extra = {}) {
  const id = /^\d+$/.test(String(idOrUrl)) ? String(idOrUrl) : videoId(idOrUrl)
  const m = app.content?.media?.[id] || {}
  const acc = m.acc || extra.acc || (String(extra.url || idOrUrl).match(/@([\w.]+)/) || [])[1] || 'unniemart_'
  return {
    id,
    acc,
    mine: acc === 'unniemart_',
    url: m.url || extra.url || `https://www.tiktok.com/@${acc}/video/${id}`,
    thumb: m.thumb ? `/media/${m.thumb}` : null,
    video: m.video ? `/media/${m.video}` : null,
    color: m.color || null,
    cap: words(m.cap || extra.cap || extra.caption || ''),
    views: m.views ?? extra.views ?? null,
    likes: m.likes ?? extra.likes ?? null,
    comments: m.comments ?? extra.comments ?? null,
    date: m.date || (extra.date || '').slice(0, 10),
  }
}

// Open the player on one video of a list (swipe or arrows go through the rest).
export function play(list, i = 0) {
  if (list[i]?.id) openSheet('player', { list, i })
}

// TikTok's own player, for videos without a file here. Only the video: no music line, no "more videos".
export const tiktokPlayer = (id) =>
  `https://www.tiktok.com/player/v1/${id}?autoplay=1&music_info=0&description=0&rel=0&native_context_menu=0&closed_caption=1`

// ---------- videos behind a video idea ----------

// The plan's kind of video for an idea's format (Clinic, Money...), with her best examples of it.
export function kindFor(format) {
  const f = (format || '').toLowerCase()
  return (app.content?.plan?.week?.kinds || []).find((k) => k.format === f) || null
}

// An idea's videos: her own that the brief points to (do it like this), and the videos where fans asked the
// question it answers, with their words.
export function ideaMedia(idea) {
  const own = [], asked = []
  for (const s of idea?.sources || []) {
    const id = videoId(s.url)
    if (!id) continue
    if (/own video/i.test(s.kind)) {
      if (!own.some((c) => c.id === id)) own.push(clip(id, { url: s.url }))
    } else if (/fan question/i.test(s.kind)) {
      const words = (s.text || '').replace(/\s*\(type:.*\)\s*$/, '').trim()
      let a = asked.find((x) => x.clip.id === id)
      if (!a) asked.push((a = { clip: clip(id, { url: s.url }), words: [] }))
      if (words) a.words.push(words)
    }
  }
  const kind = kindFor(idea?.format)
  const examples = own.length ? own : (kind?.examples || []).map((id) => clip(id))
  return { own, asked, examples, kind, cover: own[0] || examples[0] || asked[0]?.clip || null }
}

// ---------- loading ahead ----------
// The server is far from her (a third of a second each way), so a video that starts loading on the tap needs a
// moment. Videos she's likely to watch next are fetched whole in the background and played from memory: the next and
// previous one in the player, this week's examples on the Videos page. Files never change, so the phone also keeps
// them (a second visit doesn't download again). On a slow or data-saving connection nothing loads ahead.
const KEEP = 8
const held = new Map()            // video path → { url (blob, once loaded), job }

function slow() {
  const c = typeof navigator !== 'undefined' && navigator.connection
  return !!c && (c.saveData || /(^|-)2g|3g/.test(c.effectiveType || ''))
}

export function ahead(src) {
  if (!src || held.has(src) || slow()) return
  const e = { url: null }
  e.job = fetch(src, { credentials: 'same-origin' })
    .then((r) => (r.ok ? r.blob() : Promise.reject(new Error(r.status))))
    .then((b) => { e.url = URL.createObjectURL(b) })
    .catch(() => held.delete(src))
  held.set(src, e)
  while (held.size > KEEP) {
    const [k, old] = held.entries().next().value
    if (old.url) URL.revokeObjectURL(old.url)
    held.delete(k)
  }
}

// What the player should play: from memory when it's there, else straight from the server.
export const ready = (src) => held.get(src)?.url || src

// Load a few videos one after another, when the phone is idle.
export function aheadAll(srcs) {
  const list = srcs.filter(Boolean).slice(0, 4)
  const idle = (f) => (typeof requestIdleCallback === 'function' ? requestIdleCallback(f, { timeout: 3000 }) : setTimeout(f, 1500))
  idle(async () => {
    for (const s of list) {
      ahead(s)
      await held.get(s)?.job
    }
  })
}
