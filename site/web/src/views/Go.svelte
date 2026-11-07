<script>
  // One GO tab: every buyer, paid or not.
  import { app } from '../lib/live.svelte.js'
  import { route, link } from '../lib/router.svelte.js'
  import { get } from '../lib/api.js'
  import { peso } from '../lib/format.js'
  import Segmented from '../components/Segmented.svelte'
  import LineRow from '../components/LineRow.svelte'
  import Icon from '../components/Icon.svelte'
  import Ring from '../components/Ring.svelte'

  const tab = $derived(route.parts.slice(1).join('/'))
  let lines = $state(null)
  let err = $state('')
  let show = $state('open')

  $effect(() => {
    app.v
    get(`/api/go?tab=${encodeURIComponent(tab)}`).then((r) => (lines = r.lines)).catch((e) => (err = e.message))
  })
  const g = $derived(app.desk?.gos?.find((x) => x.tab === tab))
  const owing = $derived((lines || []).filter((l) => l.bal > 0))
  const shown = $derived(show === 'all' ? lines || [] : owing)
  const pct = $derived(g?.total ? Math.min(1, g.paid / g.total) : 0)
</script>

<div class="content">
  <a class="back" href={link('/orders?view=gos')}><Icon name="left" size={18} /> Orders</a>
  <div class="page-head"><h1>{tab.trim()}</h1></div>
  {#if g}
    <div class="sum card">
      <Ring value={pct} size={104} stroke={10} tone={pct >= 0.999 ? 'paid' : 'ink'}>
        <b class="pc num">{Math.round(pct * 100)}%</b><span class="pl">paid</span>
      </Ring>
      <div class="nums">
        <div><span class="k"><i class="dot ink"></i>Collected</span><b class="num">{peso(g.paid)}</b></div>
        <div><span class="k"><i class="dot"></i>To collect</span><b class="num">{peso(g.owed)}</b></div>
        <div><span class="k"><Icon name="users" size={14} />Buyers</span><b class="num">{g.buyers}</b></div>
      </div>
    </div>
    {#if g.owed_old > 0}<p class="note"><Icon name="hourglass" size={16} />+{peso(g.owed_old)} over 3 months late</p>{/if}
  {/if}
  <div class="seg"><Segmented options={[{ value: 'open', label: 'Still owe', count: owing.length || null }, { value: 'all', label: 'Everyone' }]} bind:value={show} label="Show" /></div>
  {#if err}<p class="empty">{err}</p>
  {:else if !lines}<div class="list">{#each [1, 2, 3] as _}<div class="skel-row"><span class="skel" style="width:40px;height:40px;border-radius:99px"></span><span class="skel" style="flex:1;height:18px"></span></div>{/each}</div>
  {:else}
    <div class="list">
      {#each shown as l (l.k)}<LineRow line={l} paidView showWhen />{:else}<p class="empty">Nobody owes anything here.</p>{/each}
    </div>
  {/if}
</div>

<style>
  .back { display: inline-flex; align-items: center; gap: 4px; margin: 4px 0 0; color: var(--ink-2); text-decoration: none; font-weight: 500; }
  .sum { display: flex; align-items: center; gap: 22px; padding: 18px; }
  .pc { font-size: 24px; font-weight: 700; }
  .pl { font-size: 12px; color: var(--ink-2); }
  .nums { flex: 1; display: flex; flex-direction: column; gap: 10px; }
  .nums div { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; }
  .k { display: flex; align-items: center; gap: 6px; font-size: 13.5px; color: var(--ink-2); }
  .nums b { font-size: 17px; }
  .dot { width: 8px; height: 8px; border-radius: 99px; background: var(--track); box-shadow: inset 0 0 0 1px var(--ink-3); }
  .dot.ink { background: var(--ink); box-shadow: none; }
  .note { display: flex; align-items: center; gap: 8px; margin: 12px 4px 0; font-size: 13.5px; color: var(--ink-2); }
  .seg { margin: 20px 0 14px; }
  .skel-row { display: flex; align-items: center; gap: 14px; padding: 12px 16px; }
</style>
