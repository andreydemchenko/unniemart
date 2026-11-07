// Everything the page shows, kept current. The server holds a request open until something changes (her sheet,
// a payment on another phone, new content), then the page reloads just that part.
import { get, whenSignedOut } from './api.js'

export const app = $state({
  signedIn: null,          // null = checking
  me: null,
  ready: false,            // first data arrived
  desk: null,              // orders, GOs, stock, sheet status
  sheetLoading: true,
  tasks: [], ideas: {}, activity: [], people: {}, photos: {},
  content: null,
  v: 0, cv: 0,
  online: true,
  updatedAt: 0,
})

let running = false
let ctrl = null
let hiddenAt = 0

whenSignedOut(() => { stop(); app.signedIn = false; app.ready = false })

export async function loadState() {
  const s = await get('/api/state')
  app.me = s.me
  app.desk = s.desk
  app.sheetLoading = s.loading
  app.tasks = s.tasks
  app.ideas = s.ideas
  app.activity = s.activity
  app.people = s.people
  app.photos = s.photos || {}
  app.v = s.v
  app.updatedAt = Date.now()
}

export async function loadContent() {
  const c = await get('/api/content')
  app.content = c
  app.cv = c.cv
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

async function loop() {
  while (running) {
    ctrl = new AbortController()
    try {
      const r = await get(`/api/wait?v=${app.v}&cv=${app.cv}`, { signal: ctrl.signal })
      if (!running) break
      const jobs = []
      if (r.v !== app.v) jobs.push(loadState())
      if (r.cv !== app.cv) jobs.push(loadContent())
      await Promise.all(jobs)
      app.online = true
    } catch (e) {
      if (e.name === 'AbortError' || !running) break
      app.online = false
      await sleep(4000)
    }
  }
}

export async function start() {
  if (running) return
  running = true
  try {
    await Promise.all([loadState(), app.content ? null : loadContent()])
    app.ready = true
    app.online = true
  } catch (e) {
    app.online = false
  }
  loop()
}

export function stop() {
  running = false
  ctrl?.abort()
}

export async function refresh() {
  await Promise.all([loadState(), loadContent()])
}

if (typeof document !== 'undefined') {
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      hiddenAt = Date.now()
    } else if (app.signedIn && Date.now() - hiddenAt > 30000) {
      // phones pause pages in the background: catch up straight away
      stop()
      start()
    }
  })
  window.addEventListener('online', () => { if (app.signedIn) { stop(); start() } })
}
