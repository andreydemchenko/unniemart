<script>
  import { ui, dismiss } from '../lib/ui.svelte.js'
  import { reduced } from '../lib/ui.svelte.js'
  import { easeOut } from '../lib/motion.js'
  import Icon from './Icon.svelte'

  function up(node) {
    if (reduced()) return { duration: 150, css: (t) => `opacity:${t}` }
    return { duration: 340, easing: easeOut, css: (t) => `opacity:${t};transform:translateY(${(1 - t) * 18}px) scale(${0.97 + 0.03 * t})` }
  }
  function away(node) {
    return { duration: 180, css: (t) => `opacity:${t};transform:translateY(${(1 - t) * 6}px)` }
  }
</script>

<div class="toasts" aria-live="polite">
  {#each ui.toasts as t (t.id)}
    <div class="toast {t.tone}" in:up out:away>
      {#if t.tone === 'bad'}<Icon name="alert" size={20} />{:else}<Icon name="checkCircle" size={20} />{/if}
      <span class="txt">{t.text}</span>
      {#if t.action}
        <button class="act" onclick={() => { t.action.fn(); dismiss(t.id) }}>{t.action.label}</button>
      {/if}
    </div>
  {/each}
</div>

<style>
  .toasts {
    position: fixed; z-index: 80; left: 12px; right: 12px; bottom: calc(var(--nav-h) + var(--safe-b) + 22px);
    display: flex; flex-direction: column; align-items: center; gap: 8px; pointer-events: none;
  }
  @media (min-width: 900px) { .toasts { bottom: 24px; left: 260px; } }
  .toast {
    pointer-events: auto; display: flex; align-items: center; gap: 10px; max-width: min(520px, 100%);
    min-height: 52px; padding: 8px 8px 8px 16px; border-radius: 18px;
    background: var(--hero); color: var(--on-hero); box-shadow: 0 10px 30px -8px oklch(0.2 0.04 264 / 0.5);
    font-size: 14.5px; font-weight: 500;
  }
  .toast :global(svg) { color: var(--hero-week); }
  .toast.bad :global(svg) { color: oklch(0.75 0.15 27); }
  .txt { padding: 6px 4px 6px 0; }
  .act {
    flex: none; min-height: 38px; padding: 0 14px; border-radius: 12px; font-weight: 600;
    background: var(--accent); color: var(--on-accent); transition: transform 140ms var(--ease-out);
  }
  .act:active { transform: scale(0.96); }
</style>
