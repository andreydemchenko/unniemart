// Small calculations shared by several pages.
import { sum, todayPH } from './format.js'

export const LIVE = ['late', 'week', 'soon', 'later', 'undated']

export function liveLines(desk) {
  return (desk?.lines || []).filter((l) => LIVE.includes(l.bucket))
}

export function byBucket(desk) {
  const out = { late: [], week: [], soon: [], later: [], undated: [], old: [] }
  for (const l of desk?.lines || []) (out[l.bucket] || (out[l.bucket] = [])).push(l)
  out.later = [...out.later, ...out.undated]
  return out
}

export const total = (lines) => Math.round(sum(lines, (l) => l.bal))

// The brief for this week (or the next one, if this week has none yet).
export function currentBrief(content, today = todayPH()) {
  const bs = content?.briefs || []
  return bs.find((b) => b.monday <= today && today <= b.sunday) ||
    [...bs].reverse().find((b) => b.monday > today) || bs[0] || null
}

export function status(ideas, key) {
  return ideas?.[key]?.status || 'todo'
}

export const STATUS = {
  todo: { label: 'To film', tone: '' },
  filmed: { label: 'Filmed', tone: 'accent' },
  posted: { label: 'Posted', tone: 'paid' },
  skipped: { label: 'Skipped', tone: '' },
}

// A brief's idea title, said simply: no kind in front (the kind shows on its own) and the "(only if ...)" part
// as its own line. "News: Renewal details (only if Weverse posts them)" → { text: 'Renewal details', when: 'Only if...' }
export function ideaTitle(title) {
  let text = (title || '').replace(/^(answer a fan|news|money|proof|lightstick clinic)\s*(#\d+)?\s*:\s*/i, '')
  let when = ''
  const m = text.match(/\s*\((only if [^)]*)\)\s*$/i)
  if (m) {
    when = m[1][0].toUpperCase() + m[1].slice(1)
    text = text.slice(0, m.index)
  }
  return { text: text[0] ? text[0].toUpperCase() + text.slice(1) : text, when }
}
