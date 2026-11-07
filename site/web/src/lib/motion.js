// Motion that explains what changed. Exponential ease-out for things arriving, quicker exits.
import { reduced } from './ui.svelte.js'

// cubic-bezier as a JS easing (for Svelte transitions)
export function bezier(x1, y1, x2, y2) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by
  const sx = (t) => ((ax * t + bx) * t + cx) * t
  const sy = (t) => ((ay * t + by) * t + cy) * t
  const dx = (t) => (3 * ax * t + 2 * bx) * t + cx
  return (x) => {
    let t = x
    for (let i = 0; i < 6; i++) {
      const e = sx(t) - x
      const d = dx(t)
      if (Math.abs(e) < 1e-5 || Math.abs(d) < 1e-6) break
      t -= e / d
    }
    return sy(Math.min(1, Math.max(0, t)))
  }
}

export const easeOut = bezier(0.23, 1, 0.32, 1)
export const easeDrawer = bezier(0.32, 0.72, 0, 1)
export const easeMove = bezier(0.65, 0, 0.35, 1)

// A row leaving a list (paid, done): fades, then the gap closes.
export function collapse(node, { duration = 320 } = {}) {
  if (reduced()) return { duration: 120, css: (t) => `opacity:${t}` }
  const h = node.offsetHeight
  return {
    duration,
    css: (t) => {
      const e = easeMove(t)
      return `overflow:hidden;opacity:${Math.min(1, t * 1.6)};height:${e * h}px;transform:scale(${0.98 + 0.02 * t})`
    },
  }
}

// Something new arriving in place.
export function rise(node, { delay = 0, y = 8, duration = 300 } = {}) {
  if (reduced()) return { duration: 150, css: (t) => `opacity:${t}` }
  return { delay, duration, easing: easeOut, css: (t) => `opacity:${t};transform:translateY(${(1 - t) * y}px)` }
}

export function fadeOut(node, { duration = 140 } = {}) {
  return { duration, css: (t) => `opacity:${t}` }
}

// Calls back once, the first time the element scrolls into view (charts grow then, not while off screen).
export function inview(node, cb) {
  if (reduced() || !('IntersectionObserver' in window)) { cb(); return }
  const io = new IntersectionObserver((es) => {
    if (es.some((e) => e.isIntersecting)) { io.disconnect(); requestAnimationFrame(() => cb()) }
  }, { rootMargin: '0px 0px -8% 0px' })
  io.observe(node)
  return { destroy: () => io.disconnect() }
}
