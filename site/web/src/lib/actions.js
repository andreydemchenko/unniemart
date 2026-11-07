// The things people do, with the message they see after. Each one reloads the data straight away.
import { post, upload } from './api.js'
import { loadState } from './live.svelte.js'
import { toast, copy } from './ui.svelte.js'
import { peso, handle, sum, dayParts } from './format.js'

// One payment from a buyer, put on one or more of their orders: parts = [{ line, amount }] (more than one when it
// covers several orders). Each part has its own request id (base-0, base-1...), so tapping Save again after a failure
// never pays a part twice: the parts already saved are answered from memory, the rest are tried again.
// quiet: the page shows the result itself (with its own Undo), so no message at the bottom.
export async function payMany(parts, base, { quiet = false } = {}) {
  const done = []
  try {
    for (const [i, p] of parts.entries()) {
      const r = await post('/api/pay', { tab: p.line.tab, r: p.line.r, user: p.line.user, item: p.line.ri,
                                         amount: p.amount, req: `${base}-${i}` })
      done.push({ ...p, bal: r.bal, change: r.change })
      if (r.warn) toast(r.warn, { tone: 'bad', ms: 9000 })
    }
  } catch (e) {
    e.done = done
    throw e
  } finally {
    loadState()
  }
  if (!quiet) {
    toast(`${peso(sum(done, (p) => p.amount))} from ${handle(parts[0].line.user)} is in the sheet`, {
      action: { label: 'Undo', fn: () => undo(done.map((p) => p.change).reverse()) },
    })
  }
  return done
}

export async function undo(changes) {
  try {
    for (const change of [changes].flat()) await post('/api/undo', { change })
    toast('Undone. The sheet is back as it was.')
  } catch (e) {
    toast(e.message, { tone: 'bad' })
  }
  loadState()
}

// The DM to send back after a payment: thanks, and what's left (if anything). A placeholder for her own words.
export function thanks(done, due = null) {
  const item = (l) => l.item || l.go
  const by = (d) => { const p = dayParts(d); return p ? `, due ${p.mon} ${p.day}` : '' }
  const left = (p, i) => (p.bal > 0.5 ? `${peso(p.bal)} left${by(i === 0 && due ? due : p.line.due)}` : 'fully paid')
  if (done.length === 1) {
    const p = done[0]
    return p.bal > 0.5
      ? `Hi po! Received your ${peso(p.amount)} for ${item(p.line)}, thank you po! 💜 Remaining balance: ${left(p, 0).replace(' left', '')}.`
      : `Hi po! Received your ${peso(p.amount)} for ${item(p.line)}. Fully paid na po kayo, thank you po! 💜`
  }
  return `Hi po! Received your ${peso(sum(done, (p) => p.amount))}, thank you po! 💜\n` +
    done.map((p, i) => `• ${item(p.line)}: ${left(p, i)}`).join('\n')
}

export async function remind(line) {
  const ok = await copy(line.msg)
  toast(ok ? 'Reminder copied. Paste it in the DM.' : "Couldn't copy. Long-press the text to copy it.",
        { tone: ok ? 'ok' : 'bad' })
  try {
    await post('/api/remind', { tab: line.tab, r: line.r, user: line.user, item: line.ri })
    loadState()
  } catch (e) {
    toast(`Copied, but not noted in the sheet: ${e.message}`, { tone: 'bad' })
  }
}

export async function edit(line, field, value, { quiet = false } = {}) {
  await post('/api/edit', { tab: line.tab, r: line.r, user: line.user, item: line.ri, field, value })
  loadState()
  if (!quiet) toast('Saved in the sheet')
}

export async function taskDone(t, done = true) {
  await post(`/api/tasks/${t.id}`, { done })
  loadState()
  if (done) toast('Done', { action: { label: 'Undo', fn: () => taskDone(t, false) } })
}

export async function taskSave(t, fields) {
  if (t?.id) await post(`/api/tasks/${t.id}`, fields)
  else await post('/api/tasks', fields)
  loadState()
}

export async function taskDelete(t) {
  await post(`/api/tasks/${t.id}`, { delete: true })
  loadState()
  toast('Task deleted')
}

export async function ideaSet(idea, week, fields) {
  await post('/api/idea', { key: idea.key, week, title: idea.title, ...fields })
  loadState()
}

export async function slot(item, delta, taker = '') {
  await post('/api/slot', { r: item.r, raw: item.raw, delta, taker })
  loadState()
  toast(delta > 0 ? `Slot taken · ${item.item}` : `Slot freed · ${item.item}`)
}

// ---- stock photos ----

// A stock item's photo is kept by its name (and section), so it stays when rows move in her sheet.
export const photoKey = (it) => `${it.section}|${it.raw || it.item}`.trim().toLowerCase()
export const photoOf = (photos, it) => (photos?.[photoKey(it)] ? `/photo/${photos[photoKey(it)]}` : null)

// A photo from the phone, made small first (1200 px, JPEG): quick to send, quick to show.
async function shrink(file, max = 1200) {
  const bmp = await createImageBitmap(file).catch(() => null)
  if (!bmp) throw new Error("That file isn't a photo.")
  const k = Math.min(1, max / Math.max(bmp.width, bmp.height))
  const c = document.createElement('canvas')
  c.width = Math.round(bmp.width * k)
  c.height = Math.round(bmp.height * k)
  c.getContext('2d').drawImage(bmp, 0, 0, c.width, c.height)
  return new Promise((ok, bad) => c.toBlob((b) => (b ? ok(b) : bad(new Error("Couldn't read that photo."))), 'image/jpeg', 0.85))
}

export async function photoAdd(it, file) {
  await upload(`/api/photo?key=${encodeURIComponent(photoKey(it))}`, await shrink(file))
  loadState()
  toast('Photo added')
}

export async function photoRemove(it) {
  await post('/api/photo/remove', { key: photoKey(it) })
  loadState()
  toast('Photo removed')
}

// The stock list as a post for X or Facebook (a placeholder in her words: she edits it before posting).
export function stockPost(items) {
  const by = {}
  for (const it of items) {
    if (it.left != null && it.left <= 0) continue
    const price = it.prices?.[0]?.[1]
    const left = it.left != null && it.total > 1 ? ` (${it.left} left)` : ''
    ;(by[it.section || 'Items'] ||= []).push(`• ${it.item}${price ? ` · ${peso(price)}` : ''}${left}`)
  }
  const parts = Object.entries(by).map(([sec, lines]) => `${sec.toUpperCase()}\n${lines.join('\n')}`)
  return `ONHAND ITEMS 💜\n\n${parts.join('\n\n')}\n\nDM lang po to order! 💜`
}
