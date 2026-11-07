<script>
  // Buyers side by side, like stories: a face (a red ring when late), name, amount (and how late). Tap one to open it.
  import Avatar from './Avatar.svelte'
  import Icon from './Icon.svelte'
  import { handle, peso, when } from '../lib/format.js'
  import { openSheet } from '../lib/ui.svelte.js'
  import { link } from '../lib/router.svelte.js'
  let { lines = [], late = false, max = 12, more = null } = $props()
  const shown = $derived(lines.slice(0, max))
</script>

<div class="rail">
  {#each shown as l (l.k)}
    <button class="p" onclick={() => openSheet('line', { k: l.k, line: l })}>
      <span class="face" class:late><Avatar name={l.user} size={54} /></span>
      <span class="n clip">{handle(l.user).slice(1)}</span>
      <b class="a num" class:late-t={late}>{peso(l.bal)}</b>
      {#if late && l.due}<span class="d late-t">{when(l.due, { late: true })}</span>{/if}
    </button>
  {/each}
  {#if more && lines.length > shown.length}
    <a class="p all" href={link(more)}>
      <span class="plus"><Icon name="arrowRight" size={20} /></span>
      <span class="n">{lines.length - shown.length} more</span>
    </a>
  {/if}
</div>

<style>
  .rail { gap: 4px; }
  .p {
    width: 84px; display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 4px 2px 6px;
    border-radius: var(--r); text-decoration: none; transition: transform 140ms var(--ease-out);
  }
  .p:active { transform: scale(0.95); }
  .face { padding: 3px; border-radius: 99px; box-shadow: inset 0 0 0 2px var(--accent-tile); margin-bottom: 4px; }
  .face.late { box-shadow: inset 0 0 0 2.5px var(--late); }
  .face :global(.av) { box-shadow: 0 0 0 2px var(--bg); }
  .n { max-width: 100%; font-size: 13px; font-weight: 500; color: var(--ink-2); }
  .a { font-size: 15px; font-weight: 700; letter-spacing: -0.01em; }
  .d { font-size: 12px; font-weight: 600; white-space: nowrap; }
  .plus { width: 60px; height: 60px; border-radius: 99px; display: grid; place-items: center; background: var(--surface); color: var(--ink); box-shadow: var(--shadow); margin-bottom: 4px; }
</style>
