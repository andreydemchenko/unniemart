<script>
  // A buyer: the first letter of the username on a soft tint that stays the same for that buyer.
  import { tintOf } from '../lib/kinds.js'
  let { name = '', size = 40, badge = null } = $props()
  const clean = $derived((name || '').replace(/^@/, ''))
  const letter = $derived((clean.match(/[a-z]/i)?.[0] || clean.match(/[0-9]/)?.[0] || '?').toUpperCase())
</script>

<span class="av tint-{tintOf(clean)}" style="--s:{size}px" aria-hidden="true">
  {letter}
  {#if badge}<span class="badge">{badge}</span>{/if}
</span>

<style>
  .av {
    position: relative; flex: none; width: var(--s); height: var(--s); border-radius: 999px;
    display: grid; place-items: center; font-weight: 700; font-size: calc(var(--s) * 0.42); line-height: 1;
  }
  .badge {
    position: absolute; right: -4px; bottom: -3px; min-width: 20px; height: 18px; padding: 0 5px; border-radius: 99px;
    display: grid; place-items: center; font-size: 11px; font-weight: 700; font-variant-numeric: tabular-nums;
    background: var(--late); color: var(--surface); box-shadow: 0 0 0 2px var(--surface);
  }
</style>
