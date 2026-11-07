<script>
  import { onMount } from 'svelte'
  import { app, start } from './lib/live.svelte.js'
  import { get } from './lib/api.js'
  import { route } from './lib/router.svelte.js'
  import { ui } from './lib/ui.svelte.js'
  import Nav from './components/Nav.svelte'
  import Toasts from './components/Toasts.svelte'
  import LineSheet from './components/LineSheet.svelte'
  import FindSheet from './components/FindSheet.svelte'
  import TaskSheet from './components/TaskSheet.svelte'
  import IdeaSheet from './components/IdeaSheet.svelte'
  import SlotSheet from './components/SlotSheet.svelte'
  import SyncSheet from './components/SyncSheet.svelte'
  import RemindSheet from './components/RemindSheet.svelte'
  import Player from './components/Player.svelte'
  import Login from './views/Login.svelte'
  import Home from './views/Home.svelte'
  import Orders from './views/Orders.svelte'
  import Go from './views/Go.svelte'
  import Videos from './views/Videos.svelte'
  import Plan from './views/Plan.svelte'
  import { go } from './lib/router.svelte.js'

  onMount(async () => {
    try {
      const r = await get('/api/me')
      app.me = r.me
      app.signedIn = true
      start()
    } catch {
      app.signedIn = false
    }
  })

  const pages = { home: Home, orders: Orders, go: Go, videos: Videos, plan: Plan }
  const sheets = { line: LineSheet, find: FindSheet, task: TaskSheet, idea: IdeaSheet, slot: SlotSheet, sync: SyncSheet,
                   remind: RemindSheet, player: Player }
  // pages that were merged into others (old links and home-screen bookmarks still land somewhere sensible)
  const moved = { stock: '/orders?view=stock', tasks: '/', more: '/', numbers: '/videos', dates: '/plan', news: '/plan' }
  $effect(() => { const to = moved[route.parts[0]]; if (to) go(to, { replace: true }) })
  const page = $derived(route.parts[0] || 'home')
  const Page = $derived(pages[page] || Home)

  $effect(() => {
    page
    window.scrollTo({ top: 0 })
  })

  function fade(node) {
    return { duration: 160, css: (t) => `opacity:${t}` }
  }
</script>

{#if app.signedIn === null}
  <div class="splash" aria-hidden="true"></div>
{:else if !app.signedIn}
  <Login />
{:else}
  <Nav />
  <main class="main">
    {#key page}
      <div class="page" in:fade>
        <Page />
      </div>
    {/key}
  </main>
  {#each ui.sheets as s, i (s.id)}
    {@const S = sheets[s.kind]}
    {#if S}<S {...s.props} top={i === ui.sheets.length - 1} />{/if}
  {/each}
  <Toasts />
{/if}

<style>
  .splash { min-height: 100dvh; background: var(--bg); }
  .main { padding-bottom: calc(var(--nav-h) + var(--safe-b) + 44px); min-height: 100dvh; }
  @media (min-width: 900px) {
    .main { margin-left: 240px; padding-bottom: 48px; }
  }
</style>
