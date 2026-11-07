<script>
  // One buyer's open balance: who, what, how much. The date lives in the group header above, unless showWhen.
  // A thin bar under the amount means part of it is paid already.
  import Avatar from './Avatar.svelte'
  import Money from './Money.svelte'
  import Icon from './Icon.svelte'
  import { handle, when } from '../lib/format.js'
  import { openSheet } from '../lib/ui.svelte.js'
  let { line, showWhen = false, paidView = false, onpick = null } = $props()

  const paid = $derived(paidView && !(line.bal > 0))
  const late = $derived(line.bucket === 'late' && !paid)
  const sub = $derived(!showWhen || paid ? '' : late ? when(line.due, { late: true }) : line.due ? when(line.due) : '')
  const part = $derived(!paid && line.paid > 0 && line.bal > 0 && line.total ? Math.min(100, (line.paid / line.total) * 100) : 0)
  const reminded = $derived(line.reminded && Date.now() - new Date(line.reminded).getTime() < 3 * 86400000)
</script>

<button class="row" class:paid onclick={() => (onpick ? onpick(line) : openSheet('line', { k: line.k, line }))}>
  <Avatar name={line.user} size={40} />
  <span class="mid">
    <span class="who clip">{handle(line.user)}</span>
    <span class="what clip">{line.item || line.go}</span>
  </span>
  <span class="end">
    {#if paid}
      <span class="ok"><Icon name="checkCircle" size={18} fill /></span>
    {:else}
      <span class="amt">{#if reminded}<span class="rem" title="Reminded"><Icon name="bell" size={14} /></span>{/if}<Money value={line.bal} /></span>
      {#if part}<span class="part" title="Part paid" aria-label="Part paid"><i style="width:{part}%"></i></span>{/if}
      {#if sub}<span class="sub" class:late-t={late}>{sub}</span>{/if}
    {/if}
  </span>
</button>

<style>
  .row {
    display: flex; align-items: center; gap: 12px; width: 100%; padding: 10px 16px; min-height: 62px; text-align: left;
    background: var(--surface); transition: background-color 160ms ease;
  }
  .row:active { background: var(--surface-2); }
  @media (hover: hover) and (pointer: fine) { .row:hover { background: var(--surface-2); } }
  .mid { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 1px; }
  .who { font-weight: 600; font-size: 15px; }
  .what { font-size: 13px; color: var(--ink-2); }
  .paid .who, .paid .what { color: var(--ink-3); }
  .end { display: flex; flex-direction: column; align-items: flex-end; gap: 1px; flex: none; }
  .amt { display: inline-flex; align-items: center; gap: 6px; font-weight: 650; font-size: 15.5px; }
  .rem { color: var(--ink-3); }
  .sub { font-size: 12.5px; color: var(--ink-2); white-space: nowrap; }
  .ok { color: var(--paid); }
  .part { width: 48px; height: 4px; border-radius: 99px; background: var(--track); overflow: hidden; margin: 3px 0 1px; }
  .part i { display: block; height: 100%; border-radius: inherit; background: var(--paid); }
</style>
