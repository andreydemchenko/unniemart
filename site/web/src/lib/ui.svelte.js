// Panels that slide over the page (one at a time, stacked), and small messages at the bottom.
// Opening a panel adds a history step, so Back on her phone closes the panel instead of leaving the page.

export const ui = $state({ sheets: [], toasts: [] })
let seq = 0

export function openSheet(kind, props = {}) {
  const id = ++seq
  ui.sheets.push({ id, kind, props })
  history.pushState({ sheet: id }, '')
  return id
}

// Swap the top panel for another (no extra history step).
export function swapSheet(kind, props = {}) {
  if (!ui.sheets.length) return openSheet(kind, props)
  ui.sheets[ui.sheets.length - 1] = { id: ++seq, kind, props }
}

export function closeSheet() {
  if (ui.sheets.length) history.back()
}

window.addEventListener('popstate', () => {
  if (ui.sheets.length) ui.sheets.pop()
})
window.addEventListener('hashchange', () => { ui.sheets.length = 0 })

export function toast(text, { action = null, tone = 'ok', ms = 5000 } = {}) {
  const id = ++seq
  ui.toasts.push({ id, text, action, tone })
  if (ui.toasts.length > 3) ui.toasts.shift()
  setTimeout(() => dismiss(id), action ? Math.max(ms, 8000) : ms)
  return id
}

export function dismiss(id) {
  const i = ui.toasts.findIndex((t) => t.id === id)
  if (i >= 0) ui.toasts.splice(i, 1)
}

export async function copy(text) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    const t = document.createElement('textarea')
    t.value = text
    t.style.cssText = 'position:fixed;opacity:0'
    document.body.appendChild(t)
    t.select()
    const ok = document.execCommand('copy')
    t.remove()
    return ok
  }
}

export const isWide = () => matchMedia('(min-width: 900px)').matches
export const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches
