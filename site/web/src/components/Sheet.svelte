<script>
  // A panel over the page: slides up from the bottom on a phone (drag it down to close), from the right on a
  // computer. Esc, the backdrop and the phone's Back button close it.
  import { closeSheet, isWide, reduced } from '../lib/ui.svelte.js'
  import { easeDrawer } from '../lib/motion.js'
  import Icon from './Icon.svelte'

  let { title = '', tall = false, children, top = true } = $props()
  let panel = $state()
  let dy = $state(0)
  let dragging = $state(false)
  let start = null

  function slide(node, { out = false } = {}) {
    if (reduced()) return { duration: 160, css: (t) => `opacity:${t}` }
    if (isWide()) {
      return { duration: out ? 200 : 380, easing: easeDrawer,
               css: (t) => `opacity:${t};transform:translateX(${(1 - t) * 32}px)` }
    }
    return { duration: out ? 260 : 460, easing: easeDrawer, css: (t) => `transform:translateY(${(1 - t) * 100}%)` }
  }
  function shade(node, { out = false } = {}) {
    return { duration: out ? 220 : 380, css: (t) => `opacity:${t}` }
  }

  function down(e) {
    if (isWide() || e.button > 0) return
    start = { y: e.clientY, t: performance.now() }
    dragging = true
    e.currentTarget.setPointerCapture(e.pointerId)
  }
  function move(e) {
    if (!start) return
    const d = e.clientY - start.y
    dy = d > 0 ? d : -Math.sqrt(-d) * 2          // pulling up meets resistance
  }
  function up() {
    if (!start) return
    const v = dy / Math.max(1, performance.now() - start.t)
    start = null
    dragging = false
    if (dy > 140 || (dy > 24 && v > 0.45)) closeSheet()
    else dy = 0
  }
  function key(e) {
    if (e.key === 'Escape' && top) { e.stopPropagation(); closeSheet() }
  }
  $effect(() => {
    panel?.focus({ preventScroll: true })
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = prev }
  })
</script>

<svelte:window onkeydown={key} />

<div class="wrap">
  <button class="shade" in:shade out:shade={{ out: true }} onclick={closeSheet} aria-label="Close" tabindex="-1"></button>
  <div class="panel" class:tall class:dragging bind:this={panel} tabindex="-1" role="dialog" aria-modal="true"
    aria-label={title || 'Details'} in:slide out:slide={{ out: true }}
    style={dy ? `transform: translateY(${dy}px)` : ''}>
    <div class="grab" role="presentation" onpointerdown={down} onpointermove={move} onpointerup={up} onpointercancel={up}>
      <span class="handle"></span>
    </div>
    <div class="head">
      {#if title}<h2 class="clip">{title}</h2>{:else}<span></span>{/if}
      <button class="icon-btn close" onclick={closeSheet} aria-label="Close"><Icon name="close" size={20} /></button>
    </div>
    <div class="body">
      {@render children()}
    </div>
  </div>
</div>

<style>
  .wrap { position: fixed; inset: 0; z-index: 60; }
  .shade { position: absolute; inset: 0; width: 100%; background: oklch(0.18 0.02 80 / 0.42); cursor: default; }
  @media (prefers-color-scheme: dark) { .shade { background: oklch(0 0 0 / 0.6); } }
  .panel {
    position: absolute; left: 0; right: 0; bottom: 0; max-height: calc(100dvh - 40px - var(--safe-t));
    display: flex; flex-direction: column; outline: none;
    background: var(--surface); border-radius: var(--r-xl) var(--r-xl) 0 0; box-shadow: var(--shadow-up);
    transition: transform 380ms var(--ease-drawer);
  }
  .panel.tall { height: calc(100dvh - 40px - var(--safe-t)); }
  .panel.dragging { transition: none; }
  .grab { padding: 10px 0 4px; display: grid; place-items: center; touch-action: none; cursor: grab; }
  .handle { width: 40px; height: 5px; border-radius: 999px; background: var(--surface-3); }
  .head { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 0 12px 0 20px; min-height: 44px; }
  .head h2 { font-size: 17px; }
  .close { display: none; }
  .body { overflow-y: auto; overscroll-behavior: contain; padding: 4px 20px calc(24px + var(--safe-b)); flex: 1; }

  @media (min-width: 900px) {
    .panel, .panel.tall {
      left: auto; top: 12px; right: 12px; bottom: 12px; width: 460px; max-height: none; height: auto;
      border-radius: var(--r-lg); box-shadow: 0 20px 60px -20px oklch(0.2 0.03 80 / 0.4);
    }
    .grab { display: none; }
    .close { display: inline-grid; }
    .head { padding-top: 12px; }
    .body { padding: 8px 24px 28px; }
  }
</style>
