// Money and dates the way she'd say them. Philippine time.

const peso0 = new Intl.NumberFormat('en-PH', { maximumFractionDigits: 0 })
const peso2 = new Intl.NumberFormat('en-PH', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

export function peso(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return '₱?'
  const n = Number(v)
  return (n < 0 ? '−₱' : '₱') + (Math.abs(n % 1) > 0.004 ? peso2 : peso0).format(Math.abs(n))
}

export const sum = (xs, f = (x) => x) => xs.reduce((a, x) => a + (Number(f(x)) || 0), 0)

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

export function todayPH() {
  const s = new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Manila' })
  return s // YYYY-MM-DD
}

export function parseDay(iso) {
  if (!iso) return null
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number)
  return new Date(Date.UTC(y, m - 1, d))
}

export function daysFrom(iso, today = todayPH()) {
  const a = parseDay(today), b = parseDay(iso)
  return a && b ? Math.round((b - a) / 86400000) : null
}

export function dayParts(iso) {
  const d = parseDay(iso)
  return d ? { wd: DAYS[d.getUTCDay()], day: d.getUTCDate(), mon: MONTHS[d.getUTCMonth()], year: d.getUTCFullYear() } : null
}

export function shortDate(iso, today = todayPH()) {
  const p = dayParts(iso)
  if (!p) return ''
  const sameYear = p.year === Number(today.slice(0, 4))
  return `${p.mon} ${p.day}${sameYear ? '' : ', ' + p.year}`
}

// "today", "tomorrow", "Fri", "in 12 days", "yesterday", "5 days late"
export function when(iso, { late = false, today = todayPH() } = {}) {
  const n = daysFrom(iso, today)
  if (n === null) return ''
  if (n === 0) return 'today'
  if (n === 1) return 'tomorrow'
  if (n === -1) return late ? '1 day late' : 'yesterday'
  if (n < 0) return late ? `${-n} days late` : `${-n} days ago`
  if (n < 7) return dayParts(iso).wd
  return `in ${n} days`
}

export function ago(isoTime) {
  if (!isoTime) return ''
  const s = (Date.now() - new Date(isoTime).getTime()) / 1000
  if (s < 45) return 'just now'
  if (s < 3600) return `${Math.round(s / 60)} min ago`
  if (s < 86400) return `${Math.round(s / 3600)} h ago`
  const d = Math.round(s / 86400)
  if (d < 7) return d === 1 ? 'yesterday' : `${d} days ago`
  return shortDate(new Date(isoTime).toLocaleDateString('en-CA', { timeZone: 'Asia/Manila' }))
}

export function clock(isoTime) {
  if (!isoTime) return ''
  return new Date(isoTime).toLocaleTimeString('en-PH', { timeZone: 'Asia/Manila', hour: 'numeric', minute: '2-digit' })
}

export const plural = (n, one, many = one + 's') => `${n} ${n === 1 ? one : many}`

export function handle(user) {
  const u = (user || '').trim()
  return u.startsWith('@') ? u : '@' + u
}

// An X profile link when the username looks like a handle.
export function xLink(user) {
  const u = (user || '').trim().replace(/^@/, '')
  return /^[A-Za-z0-9_]{2,15}$/.test(u) ? `https://x.com/${u}` : null
}

export function initials(name) {
  return (name || '?').replace(/^@/, '').slice(0, 1).toUpperCase()
}

// ₱650, ₱2.6K, ₱24K, ₱1.2M: for chart labels where a full amount doesn't fit.
export function pesoShort(v) {
  const n = Math.abs(Number(v) || 0), s = v < 0 ? '−₱' : '₱'
  if (n < 1000) return s + Math.round(n)
  if (n < 10000) return s + (n / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  if (n < 1e6) return s + Math.round(n / 1000) + 'K'
  return s + (n / 1e6).toFixed(1).replace(/\.0$/, '') + 'M'
}

export function compact(v) {
  if (v == null) return '–'
  return Intl.NumberFormat('en', { notation: v >= 10000 ? 'compact' : 'standard', maximumFractionDigits: 1 }).format(v)
}

// "Film Oct 21 to 23. Post Sat Oct 24, the day before…" → { film: 'Oct 21–23', post: 'Oct 24' }
// "Film and post Oct 20 to 22" → { film: '', post: 'Oct 20–22', both: true }
const RANGE = /(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\d{1,2})(?:\s*(?:to|or|-|–)\s*(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* )?(\d{1,2}))?/
function range(s) {
  const m = RANGE.exec(s || '')
  if (!m) return ''
  return m[4] ? `${m[1]} ${m[2]}–${m[3] ? m[3] + ' ' : ''}${m[4]}` : `${m[1]} ${m[2]}`
}
export function plannedDays(text) {
  const t = text || ''
  const both = /film and post/i.test(t)
  const pi = t.search(/\bpost/i), fi = t.search(/\bfilm/i)
  const post = pi >= 0 ? range(t.slice(pi).split(/\.\s/)[0]) : ''
  const film = !both && fi >= 0 ? range(t.slice(fi).split(/\.\s/)[0]) : ''
  return { film, post, both: both && !!post }
}

// The same, as she'd read it: "Film Oct 21–23 · Post Oct 24", "Film and post Oct 20–22"
export function plannedText(text) {
  const d = plannedDays(text)
  if (d.both) return `Film and post ${d.post}`
  return [d.film && `Film ${d.film}`, d.post && `Post ${d.post}`].filter(Boolean).join(' · ')
}

// "Oct 19 to Oct 25" → "Oct 19–25", "Oct 26 to Nov 1" → "Oct 26–Nov 1"
export function rangeText(s) {
  const m = /^([A-Z][a-z]{2}) (\d{1,2}) to ([A-Z][a-z]{2}) (\d{1,2})$/.exec(s || '')
  if (!m) return s || ''
  return m[1] === m[3] ? `${m[1]} ${m[2]}–${m[4]}` : `${m[1]} ${m[2]}–${m[3]} ${m[4]}`
}
