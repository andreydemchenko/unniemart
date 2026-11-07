<script>
  // A progress ring. It fills once when it first comes into view; later changes slide.
  import { inview } from '../lib/motion.js'
  let { value = 0, size = 64, stroke = 7, tone = 'ink', children } = $props()
  const r = $derived((size - stroke) / 2)
  const c = $derived(2 * Math.PI * r)
  const v = $derived(Math.max(0, Math.min(1, Number(value) || 0)))
  let shown = $state(false)
</script>

<span class="ring" style="width:{size}px;height:{size}px" use:inview={() => (shown = true)}>
  <svg viewBox="0 0 {size} {size}" aria-hidden="true">
    <circle class="track" cx={size / 2} cy={size / 2} {r} stroke-width={stroke} />
    {#if v > 0}
      <circle class="val {tone}" cx={size / 2} cy={size / 2} {r} stroke-width={stroke}
        stroke-dasharray={c} stroke-dashoffset={shown ? c * (1 - v) : c} transform="rotate(-90 {size / 2} {size / 2})" />
    {/if}
  </svg>
  {#if children}<span class="mid">{@render children()}</span>{/if}
</span>

<style>
  .ring { position: relative; display: inline-grid; place-items: center; flex: none; }
  svg { position: absolute; inset: 0; width: 100%; height: 100%; }
  circle { fill: none; }
  .track { stroke: var(--track); }
  .val { stroke-linecap: round; transition: stroke-dashoffset 900ms var(--ease-out); }
  .ink { stroke: var(--ink); }
  .accent { stroke: var(--accent); }
  .paid { stroke: var(--paid); }
  .late { stroke: var(--late); }
  .on-accent { stroke: var(--on-accent); }
  .mid { position: relative; display: grid; place-items: center; text-align: center; line-height: 1.1; }
</style>
