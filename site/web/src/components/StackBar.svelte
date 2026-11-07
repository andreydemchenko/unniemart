<script>
  // One bar split into parts (late, this week, later). Draws in from the left the first time it is seen.
  import { inview } from '../lib/motion.js'
  let { parts = [], height = 10, gap = 3 } = $props()
  const total = $derived(parts.reduce((a, p) => a + Math.max(0, p.v || 0), 0))
  let shown = $state(false)
</script>

<div class="stack" class:shown style="height:{height}px;gap:{gap}px" use:inview={() => (shown = true)} role="img"
  aria-label={parts.map((p) => `${p.label}: ${p.text ?? p.v}`).join(', ')}>
  {#each parts.filter((p) => p.v > 0) as p (p.key)}
    <span class="seg {p.tone}" style="flex-grow:{p.v / (total || 1)}"></span>
  {/each}
  {#if !total}<span class="seg empty" style="flex-grow:1"></span>{/if}
</div>

<style>
  .stack { display: flex; width: 100%; clip-path: inset(0 100% 0 0 round 99px); transition: clip-path 900ms var(--ease-out); }
  .stack.shown { clip-path: inset(0 0 0 0 round 99px); }
  .seg { flex-basis: 0; min-width: 6px; border-radius: 99px; transition: flex-grow 600ms var(--ease-move); }
  .late { background: var(--late); }
  .ink { background: var(--ink); }
  .accent { background: var(--accent); }
  .week { background: var(--hero-week); }
  .hero-mid { background: oklch(1 0 0 / 0.55); }
  .hero-rest { background: oklch(1 0 0 / 0.24); }
  .soft { background: var(--ink-3); }
  .faint { background: var(--track); }
  .paid { background: var(--paid); }
  .empty { background: var(--track); }
</style>
