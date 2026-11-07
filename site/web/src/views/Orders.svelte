<script>
  import { app } from '../lib/live.svelte.js'
  import { route, go, link } from '../lib/router.svelte.js'
  import { openSheet } from '../lib/ui.svelte.js'
  import { peso, pesoShort, shortDate, when, dayParts, daysFrom, todayPH, plural } from '../lib/format.js'
  import { byBucket, total } from '../lib/derive.js'
  import { flip } from 'svelte/animate'
  import { collapse } from '../lib/motion.js'
  import Segmented from '../components/Segmented.svelte'
  import LineRow from '../components/LineRow.svelte'
  import Icon from '../components/Icon.svelte'
  import Ring from '../components/Ring.svelte'
  import StackBar from '../components/StackBar.svelte'
  import StockGrid from '../components/StockGrid.svelte'

  let view = $state(route.query.view || 'collect')
  let filter = $state(route.query.f || 'all')
  let q = $state('')
  let showOld = $state(false)
  let showPaidGos = $state(false)
  let open = $state({})              // Coming up / Later: the first few until she asks for all
  const today = todayPH()

  // a link to another view or filter while already on this page
  $effect(() => {
    view = route.query.view || 'collect'
    filter = route.query.f || 'all'
  })
  const b = $derived(byBucket(app.desk))
  const views = [
    { value: 'collect', label: 'To collect' },
    { value: 'gos', label: 'By GO' },
    { value: 'stock', label: 'Stock' },
  ]
  const BUCKETS = [
    { k: 'late', title: 'Late', tone: 'late' },
    { k: 'week', title: 'Due this week', short: 'This week', tone: 'week' },
    { k: 'soon', title: 'Coming up', tone: 'hero-mid' },
    { k: 'later', title: 'Later', tone: 'hero-rest' },
    { k: 'old', title: 'Older', tone: '' },
  ]
  const sums = $derived(Object.fromEntries(BUCKETS.map((x) => [x.k, total(b[x.k] || [])])))

  const match = (s) => (l) => !s || l.user.toLowerCase().replace(/^@/, '').includes(s) ||
    (l.item || '').toLowerCase().includes(s) || l.go.toLowerCase().includes(s)
  // each bucket, its lines grouped by due date (one header per day instead of the date on every row)
  const groups = $derived.by(() => {
    const s = q.trim().toLowerCase().replace(/^@/, '')
    return BUCKETS
      .filter((x) => filter === 'all' || filter === x.k)
      .map((x) => {
        const lines = (b[x.k] || []).filter(match(s))
        const days = []
        for (const l of lines) {
          const key = l.due || ''
          let d = days.find((y) => y.key === key)
          if (!d) days.push((d = { key, lines: [] }))
          d.lines.push(l)
        }
        return { ...x, lines, days }
      })
      .filter((g) => g.lines.length)
  })
  const gos = $derived(app.desk?.gos || [])
  const openGos = $derived(gos.filter((g) => g.owed > 0))
  const otherGos = $derived(gos.filter((g) => g.owed <= 0))

  function setView(v) {
    go(`/orders?view=${v}`, { replace: true })
  }
  function setFilter(v) {
    filter = filter === v ? 'all' : v
    go(filter === 'all' ? '/orders' : `/orders?f=${filter}`, { replace: true })
  }
  // Coming up and Later show their first 3 people until she asks for all (searching or filtering shows everything)
  const folded = (g) => ['soon', 'later'].includes(g.k) && !open[g.k] && !q && filter === 'all' && g.lines.length > 4
  function fold(g) {
    if (g.k === 'old') return g.days.slice(0, 60)
    if (!folded(g)) return g.days
    const out = []
    let n = 0
    for (const d of g.days) {
      if (n >= 3) break
      out.push({ ...d, lines: d.lines.slice(0, 3 - n) })
      n += out.at(-1).lines.length
    }
    return out
  }
  const pct = (g) => (g.total ? Math.min(1, g.paid / g.total) : 0)
  function dayHead(iso, late) {
    if (!iso) return 'No date'
    const p = dayParts(iso)
    const n = daysFrom(iso, today)
    const rel = late ? when(iso, { late: true }) : n === 0 ? 'today' : n === 1 ? 'tomorrow' : n < 7 ? '' : when(iso)
    return `${p.wd}, ${p.mon} ${p.day}${p.year !== Number(today.slice(0, 4)) ? ' ' + p.year : ''}${rel ? ' · ' + rel : ''}`
  }
</script>

<div class="content">
  <div class="page-head"><h1>Orders</h1></div>
  <Segmented options={views} bind:value={view} onchange={setView} label="Orders view" />

  {#if view === 'collect'}
    <div class="summary">
      <p class="s-k">To collect</p>
      <p class="s-v num">{peso(BUCKETS.slice(0, 4).reduce((a, x) => a + sums[x.k], 0))}</p>
      <StackBar height={8} parts={BUCKETS.slice(0, 4).map((x) => ({ key: x.k, v: sums[x.k], tone: x.tone, label: x.short || x.title, text: peso(sums[x.k]) }))} />
      <div class="legend" role="toolbar" aria-label="Show">
        {#each BUCKETS.slice(0, 4) as x}
          {#if (b[x.k] || []).length}
            <button class="lg" class:sel={filter === x.k} class:dimmed={filter !== 'all' && filter !== x.k} onclick={() => setFilter(x.k)} aria-pressed={filter === x.k}>
              <span class="lk"><i class="dot {x.tone}"></i>{x.short || x.title}</span>
              <b class="num">{pesoShort(sums[x.k])}</b>
            </button>
          {/if}
        {/each}
      </div>
    </div>

    <label class="search">
      <Icon name="search" size={20} />
      <input bind:value={q} placeholder="Search" aria-label="Search username, item or GO" autocomplete="off" autocapitalize="off" spellcheck="false" />
      {#if q}<button class="icon-btn" aria-label="Clear" onclick={() => (q = '')}><Icon name="close" size={18} /></button>{/if}
    </label>

    {#if !app.ready}
      <div class="list">{#each [1, 2, 3, 4] as _}<div class="skel-row"><span class="skel" style="width:40px;height:40px;border-radius:99px"></span><span class="skel" style="flex:1;height:18px"></span></div>{/each}</div>
    {/if}

    {#each groups as g (g.k)}
      <section class="section">
        <div class="section-head">
          <h2>{g.title} <span class="count" class:late={g.k === 'late'}>{g.lines.length}</span></h2>
          {#if g.k !== 'old'}<span class="sum num" class:late-t={g.k === 'late'}>{peso(total(g.lines))}</span>{/if}
        </div>
        {#if g.k === 'late' && !q}
          <button class="btn accent wide remind" onclick={() => openSheet('remind', { which: 'late' })}><Icon name="send" size={18} />Remind {g.lines.length === 1 ? 'them' : `all ${g.lines.length}`}</button>
        {/if}
        {#if g.k === 'old' && !showOld && filter !== 'old' && !q}
          <button class="old card" onclick={() => (showOld = true)}>
            <span class="glyph tint-n"><Icon name="archive" size={22} /></span>
            <span class="old-t">Over 3 months late</span>
            <span class="btn soft sm">Show</span>
          </button>
        {:else}
          <div class="list">
            {#each fold(g) as dgrp (dgrp.key)}
              <div class="dh" class:late-t={g.k === 'late'}><span>{dayHead(dgrp.key, g.k === 'late')}</span>{#if dgrp.lines.length > 1}<span class="num">{peso(total(dgrp.lines))}</span>{/if}</div>
              {#each dgrp.lines as l (l.k)}
                <div animate:flip={{ duration: 300 }} out:collapse><LineRow line={l} /></div>
              {/each}
            {/each}
          </div>
          {#if folded(g)}<button class="btn soft wide more" onclick={() => (open = { ...open, [g.k]: true })}>Show all {g.lines.length}</button>{/if}
        {/if}
      </section>
    {:else}
      {#if app.ready}
        <div class="nothing"><span class="glyph tint-n"><Icon name={q ? 'search' : 'checkCircle'} size={24} /></span><p>{q ? `Nothing open for “${q}”` : 'Nothing to collect here'}</p></div>
      {/if}
    {/each}

  {:else if view === 'gos'}
    <section class="section">
      <div class="section-head"><h2>Still collecting <span class="count">{openGos.length}</span></h2></div>
      <div class="list">
        {#each openGos as g (g.tab)}
          <a class="go" href={link('/go/' + g.tab)}>
            <Ring value={pct(g)} size={48} stroke={5}><span class="pc num">{Math.round(pct(g) * 100)}%</span></Ring>
            <span class="mid">
              <span class="name clip">{g.go}</span>
              <span class="go-sub">{plural(g.open, 'order')} unpaid{#if g.last} · last due {shortDate(g.last)}{/if}</span>
            </span>
            <span class="owed num">{peso(g.owed)}<small>left</small></span>
          </a>
        {:else}
          <div class="nothing"><span class="glyph tint-n"><Icon name="checkCircle" size={24} /></span><p>Every GO is paid up</p></div>
        {/each}
      </div>
    </section>
    <section class="section">
      <div class="section-head"><h2>Paid up or older <span class="count">{otherGos.length}</span></h2></div>
      <div class="list">
        {#each (showPaidGos ? otherGos : otherGos.slice(0, 8)) as g (g.tab)}
          <a class="go small" href={link('/go/' + g.tab)}>
            <span class="glyph sm" class:paidg={!(g.owed_old > 0)} class:tint-n={g.owed_old > 0}><Icon name={g.owed_old > 0 ? 'hourglass' : 'check'} size={16} /></span>
            <span class="name clip">{g.go}</span>
            <span class="faint small num">{g.owed_old > 0 ? pesoShort(g.owed_old) : g.last ? shortDate(g.last) : ''}</span>
          </a>
        {/each}
      </div>
      {#if !showPaidGos && otherGos.length > 8}<button class="btn soft wide more" onclick={() => (showPaidGos = true)}>Show all {otherGos.length}</button>{/if}
    </section>

  {:else}
    <StockGrid />
  {/if}
</div>

<style>
  .summary {
    padding: 18px 16px 10px; margin-top: 16px; border-radius: var(--r-xl); background: var(--hero); color: var(--on-hero);
    box-shadow: 0 18px 40px -24px oklch(0.25 0.06 263 / 0.7), inset 0 0 0 1px var(--hero-line);
  }
  .s-k { padding: 0 4px; font-size: 14px; font-weight: 550; color: var(--on-hero-2); }
  .s-v { padding: 0 4px; margin: 2px 0 14px; font-size: 34px; font-weight: 700; letter-spacing: -0.025em; line-height: 1.1; }
  .legend { display: grid; grid-template-columns: repeat(auto-fit, minmax(84px, 1fr)); gap: 4px; margin-top: 12px; }
  .lg {
    display: flex; flex-direction: column; align-items: flex-start; gap: 1px; padding: 8px 10px; border-radius: 14px; text-align: left;
    transition: background-color 160ms ease, opacity 160ms ease, transform 140ms var(--ease-out);
  }
  .lg:active { transform: scale(0.96); }
  .lg.sel { background: var(--hero-2); }
  .lg.dimmed { opacity: 0.45; }
  .lk { display: flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600; color: var(--on-hero-2); white-space: nowrap; }
  .lg b { font-size: 17px; }
  .dot { width: 8px; height: 8px; border-radius: 99px; flex: none; }
  .dot.late { background: var(--late); }
  .dot.week { background: var(--hero-week); }
  .dot.hero-mid { background: oklch(1 0 0 / 0.55); }
  .dot.hero-rest { background: oklch(1 0 0 / 0.24); }
  @media (hover: hover) and (pointer: fine) { .lg:hover { background: var(--hero-2); } }

  .search {
    display: flex; align-items: center; gap: 10px; padding: 0 6px 0 16px; min-height: 48px; margin-top: 12px;
    border-radius: var(--r); background: var(--surface); box-shadow: var(--shadow); color: var(--ink-2);
  }
  .search input { flex: 1; border: 0; outline: 0; background: none; font-size: 16px; color: var(--ink); min-width: 0; }
  .count { display: inline-grid; place-items: center; min-width: 24px; height: 22px; padding: 0 7px; margin-left: 4px; border-radius: 99px;
    font-size: 13px; font-weight: 700; background: var(--surface-3); color: var(--ink); vertical-align: 2px; }
  .count.late { background: var(--late-soft); color: var(--late-ink); }
  .sum { font-weight: 650; }
  .remind { margin-bottom: 10px; }
  .skel-row { display: flex; align-items: center; gap: 14px; padding: 12px 16px; }
  .dh {
    display: flex; justify-content: space-between; gap: 12px; padding: 14px 16px 2px; font-size: 13px; font-weight: 650;
    color: var(--ink-3); background: var(--surface); border-top: 0 !important;
  }
  .dh + div { border-top: 0; }
  .list > div:not(.dh) + .dh { border-top: 1px solid var(--line) !important; margin-top: 4px; }
  .nothing { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 48px 20px; color: var(--ink-2); text-align: center; }
  .nothing .glyph { width: 52px; height: 52px; border-radius: 18px; }
  .nothing.wide { grid-column: 1 / -1; }
  .old { width: 100%; display: flex; align-items: center; gap: 12px; text-align: left; padding: 12px 14px 12px 12px; color: var(--ink-2); font-size: 14px; }
  .old-t { flex: 1; }
  .old .btn { flex: none; }

  .go { display: flex; align-items: center; gap: 12px; padding: 12px 16px; text-decoration: none; background: var(--surface); transition: background-color 160ms ease; }
  .go:active { background: var(--surface-2); }
  @media (hover: hover) and (pointer: fine) { .go:hover { background: var(--surface-2); } }
  .go.small { padding: 10px 16px; }
  .pc { font-size: 12px; font-weight: 700; }
  .mid { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
  .name { font-weight: 600; flex: 1; }
  .go-sub { display: flex; align-items: center; gap: 4px; font-size: 14px; color: var(--ink-2); }
  .sep { width: 10px; }
  .owed { font-weight: 650; flex: none; display: flex; flex-direction: column; align-items: flex-end; line-height: 1.2; }
  .owed small { font-size: 12.5px; font-weight: 500; color: var(--ink-3); }
  .small { font-size: 13px; }
  .paidg { background: var(--paid-soft); color: var(--paid); }
  .more { margin-top: 12px; }

</style>
