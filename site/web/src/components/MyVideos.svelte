<script>
  // Her own TikToks as pictures (newest or most watched, tap to watch), and which kinds of video get the most views.
  // Part of the Videos page.
  import { app } from '../lib/live.svelte.js'
  import { compact } from '../lib/format.js'
  import { formatOf } from '../lib/kinds.js'
  import { clip, play } from '../lib/media.js'
  import { inview } from '../lib/motion.js'
  import Icon from './Icon.svelte'
  import Thumb from './Thumb.svelte'

  const s = $derived(app.content?.stats)
  const normal = $derived(Math.round(s?.scoreboard?.median_views_2026 || 0))
  const byId = $derived(Object.fromEntries((s?.videos || []).map((v) => [v.id, v])))
  let sort = $state('new')
  let more = $state(false)

  // every video of hers the site has a picture of, plus this week's numbers (newest stats win)
  const all = $derived.by(() => {
    const ids = new Set((s?.videos || []).filter((v) => !v.pinned).map((v) => v.id))
    for (const [id, m] of Object.entries(app.content?.media || {})) if (m.mine) ids.add(id)
    return [...ids].map((id) => clip(id, byId[id] || {})).filter((c) => c.date)
  })
  const list = $derived(sort === 'new'
    ? [...all].sort((a, b) => (a.date < b.date ? 1 : -1))
    : [...all].sort((a, b) => (b.views || 0) - (a.views || 0)))
  const wide = typeof matchMedia !== 'undefined' && matchMedia('(min-width: 900px)').matches
  const shown = $derived(more ? list : list.slice(0, wide ? 12 : 9))

  // which kinds of video get views: a typical (middle) video of each kind, from the latest weekly numbers.
  // A kind with one video says nothing yet, so those go under Other.
  const kinds = $derived.by(() => {
    const by = {}
    for (const v of s?.videos || []) {
      if (v.views == null || v.pinned) continue
      const f = formatOf(v.format)
      ;(by[f.label] ||= { ...f, vids: [] }).vids.push(v)
    }
    const out = [], other = { icon: 'sparkle', label: 'Other', vids: [] }
    for (const k of Object.values(by)) {
      if (k.vids.length >= 2 && k.label !== 'Other') out.push(k)
      else other.vids.push(...k.vids)
    }
    if (other.vids.length >= 2) out.push(other)
    return out.map((k) => {
      const vs = [...k.vids].sort((a, b) => b.views - a.views)
      const mid = vs[Math.floor(vs.length / 2)].views
      return { ...k, n: vs.length, med: mid, list: vs.map((v) => clip(v.id, v)) }
    }).sort((a, b) => (a.label === 'Other') - (b.label === 'Other') || b.med - a.med)
  })
  const top = $derived(Math.max(1, ...kinds.map((k) => k.med)))
  let seen = $state(false)
</script>

{#if all.length}
  <section class="section">
    <div class="section-head">
      <h2>Your videos</h2>
      <div class="filters" role="group" aria-label="Order">
        <button class="chip" class:sel={sort === 'new'} onclick={() => (sort = 'new')} aria-pressed={sort === 'new'}>Newest</button>
        <button class="chip" class:sel={sort === 'top'} onclick={() => (sort = 'top')} aria-pressed={sort === 'top'}>Most views</button>
      </div>
    </div>
    <div class="grid">
      {#each shown as c, i (c.id)}
        <Thumb {c} hit={sort === 'new' && normal > 0 && c.views >= normal * 2} onclick={() => play(list, i)} />
      {/each}
    </div>
    {#if list.length > shown.length}
      <button class="btn soft wide more" onclick={() => (more = true)}>Show all {list.length}</button>
    {/if}
  </section>
{/if}

{#if kinds.length}
  <section class="section">
    <div class="section-head"><h2>What gets views</h2></div>
    <div class="list" use:inview={() => (seen = true)}>
      {#each kinds as k, i (k.label)}
        <button class="krow" onclick={() => play(k.list, 0)} aria-label="Watch the {k.label} videos">
          <span class="glyph sm" class:tint-best={i === 0} class:tint-n={i > 0}><Icon name={k.icon} duo size={19} /></span>
          <span class="kmid">
            <span class="kl"><b>{k.label}</b><span class="faint">{k.n} videos</span></span>
            <span class="track"><i class:best={i === 0} style="transform:scaleX({seen ? Math.max(0.03, k.med / top) : 0});transition-delay:{i * 70}ms"></i></span>
          </span>
          <span class="kv num">{compact(k.med)}<small>views</small></span>
        </button>
      {/each}
    </div>
  </section>
{/if}

<style>
  .section-head { align-items: center; }
  .filters .chip { height: 32px; padding: 0 12px; font-size: 13.5px; }
  .grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; border-radius: 20px; overflow: hidden; }
  @media (min-width: 900px) { .grid { grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 10px; } }
  .more { margin-top: 12px; }

  .tint-best { background: var(--accent-soft); color: var(--accent-ink); }
  .krow { display: flex; align-items: center; gap: 12px; width: 100%; padding: 12px 16px; text-align: left; background: var(--surface); transition: background-color 160ms ease; }
  .krow:active { background: var(--surface-2); }
  @media (hover: hover) and (pointer: fine) { .krow:hover { background: var(--surface-2); } }
  .kmid { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 7px; }
  .kl { display: flex; align-items: baseline; gap: 8px; font-size: 15px; }
  .kl b { font-weight: 600; }
  .kl span { font-size: 13px; }
  .track { display: block; height: 10px; border-radius: 99px; background: var(--surface-2); overflow: hidden; }
  .track i { display: block; height: 100%; border-radius: inherit; background: var(--ink-3); transform-origin: left; transition: transform 800ms var(--ease-out); }
  .track i.best { background: var(--accent); }
  .kv { flex: none; min-width: 52px; display: flex; flex-direction: column; align-items: flex-end; font-size: 17px; font-weight: 700; line-height: 1.1; }
  .kv small { font-size: 12px; font-weight: 500; color: var(--ink-3); }
</style>
