<script>
  // "Who paid?" Find the buyer, then record the payment.
  import Sheet from './Sheet.svelte'
  import LineRow from './LineRow.svelte'
  import Icon from './Icon.svelte'
  import { app } from '../lib/live.svelte.js'
  import { liveLines } from '../lib/derive.js'
  import { swapSheet } from '../lib/ui.svelte.js'
  let { top = true } = $props()
  let q = $state('')
  let input = $state()
  $effect(() => { setTimeout(() => input?.focus(), 350) })
  const all = $derived(app.desk?.lines || [])
  const found = $derived.by(() => {
    const s = q.trim().toLowerCase().replace(/^@/, '')
    const pool = s ? all : liveLines(app.desk)
    if (!s) return pool.slice(0, 40)
    return pool.filter((l) => l.user.toLowerCase().replace(/^@/, '').includes(s) ||
      (l.item || '').toLowerCase().includes(s) || l.go.toLowerCase().includes(s)).slice(0, 60)
  })
</script>

<Sheet title="Who paid?" tall {top}>
  <label class="search">
    <Icon name="search" size={20} />
    <input bind:this={input} bind:value={q} placeholder="Username or item" autocomplete="off" autocapitalize="off" spellcheck="false" />
  </label>
  <div class="list rows">
    {#each found as l (l.k)}
      <LineRow line={l} onpick={(x) => swapSheet('line', { k: x.k, line: x, pay: true })} />
    {:else}
      <p class="empty">{q ? `No open balance for “${q}”.` : 'No open balances.'}</p>
    {/each}
  </div>
</Sheet>

<style>
  .search {
    position: sticky; top: 0; z-index: 2; display: flex; align-items: center; gap: 10px; padding: 0 16px; min-height: 52px;
    border-radius: var(--r); background: var(--surface-2); color: var(--ink-2); margin-bottom: 12px;
  }
  .search input { flex: 1; border: 0; outline: 0; background: none; font-size: 16px; color: var(--ink); min-width: 0; }
  .rows { box-shadow: none; border: 1px solid var(--line); }
</style>
