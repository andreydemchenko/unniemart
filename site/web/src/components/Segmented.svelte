<script>
  // Two to four choices in one pill. The dark part slides to the one picked.
  let { options, value = $bindable(), onchange = null, label = '' } = $props()
  let wrap = $state()
  let pill = $state({ x: 0, w: 0, ready: false })

  function measure() {
    const el = wrap?.querySelector(`[data-v="${CSS.escape(String(value))}"]`)
    if (el) pill = { x: el.offsetLeft, w: el.offsetWidth, ready: true }
  }
  $effect(() => { value; options; requestAnimationFrame(measure) })
  $effect(() => {
    const ro = new ResizeObserver(measure)
    ro.observe(wrap)
    return () => ro.disconnect()
  })
  function pick(v) {
    value = v
    onchange?.(v)
  }
</script>

<div class="seg" bind:this={wrap} role="tablist" aria-label={label}>
  <span class="pill" class:ready={pill.ready} style="transform: translateX({pill.x}px); width: {pill.w}px"></span>
  {#each options as o (o.value)}
    <button role="tab" aria-selected={value === o.value} data-v={o.value} class:on={value === o.value}
      onclick={() => pick(o.value)}>
      {o.label}{#if o.count}<span class="n num">{o.count}</span>{/if}
    </button>
  {/each}
</div>

<style>
  .seg {
    position: relative; display: flex; padding: 4px; gap: 2px; border-radius: 999px; background: var(--surface-2);
    overflow-x: auto; scrollbar-width: none;
  }
  .seg::-webkit-scrollbar { display: none; }
  .pill {
    position: absolute; top: 4px; bottom: 4px; left: 0; border-radius: 999px; background: var(--ink);
    opacity: 0;
  }
  .pill.ready { opacity: 1; transition: transform 260ms var(--ease-out), width 260ms var(--ease-out); }
  button {
    position: relative; z-index: 1; flex: 1 0 auto; min-height: 38px; padding: 0 16px; border-radius: 999px;
    font-weight: 600; font-size: 14px; color: var(--ink-2); white-space: nowrap;
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
    transition: color 200ms ease;
  }
  button.on { color: var(--bg); }
  .n { font-size: 12px; font-weight: 600; opacity: 0.75; }
</style>
