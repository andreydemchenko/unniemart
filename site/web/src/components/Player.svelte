<script>
  // A video, full screen. Videos play from the site (small files; the next and previous one load in the background,
  // so swiping is instant); photo slideshows play in TikTok's own player. Tap to pause, swipe sideways or use the arrows for the next one,
  // swipe down (or Back, or Esc) to close.
  import { tick, untrack } from 'svelte'
  import Icon from './Icon.svelte'
  import { closeSheet, reduced } from '../lib/ui.svelte.js'
  import { compact, shortDate } from '../lib/format.js'
  import { tiktokPlayer, ahead, ready as fromMemory } from '../lib/media.js'
  let { list = [], i: first = 0, top = true } = $props()

  let i = $state(untrack(() => first))
  const c = $derived(list[i])
  const src = $derived(c?.video ? fromMemory(c.video) : null)
  let vid = $state()
  let ready = $state(false)
  let paused = $state(false)
  let muted = $state(false)
  let pct = $state(0)
  let drag = $state({ x: 0, y: 0 })
  let start = null

  $effect(() => {
    c?.id
    ready = false
    paused = false
    pct = 0
    if (c?.video) begin()
  })

  async function begin() {
    await tick()
    if (!vid) return
    vid.muted = muted
    try {
      await vid.play()
    } catch {
      // the phone wants a tap before sound: play without it, the speaker button turns it on
      muted = true
      vid.muted = true
      try { await vid.play() } catch { paused = true }
    }
  }
  function toggle() {
    if (!vid) return
    if (vid.paused) { vid.play(); paused = false } else { vid.pause(); paused = true }
  }
  function sound() {
    muted = !muted
    if (vid) {
      vid.muted = muted
      if (vid.paused) toggle()
    }
  }
  function go(d) {
    const j = i + d
    if (j >= 0 && j < list.length) i = j
  }
  function seek(e) {
    if (!vid?.duration) return
    const r = e.currentTarget.getBoundingClientRect()
    vid.currentTime = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * vid.duration
  }

  // swipes on the video: sideways = next / previous, down = close, a tap = pause
  function down(e) {
    if (e.button > 0 || e.target.closest('button')) return
    start = { x: e.clientX, y: e.clientY, t: performance.now() }
    e.currentTarget.setPointerCapture(e.pointerId)
  }
  function move(e) {
    if (!start) return
    const x = e.clientX - start.x, y = e.clientY - start.y
    drag = Math.abs(x) > Math.abs(y) ? { x, y: 0 } : { x: 0, y: Math.max(0, y) }
  }
  function up(e) {
    if (!start) return
    const { x, y } = drag
    const quick = performance.now() - start.t < 300
    start = null
    drag = { x: 0, y: 0 }
    if (Math.abs(x) > 60 || (quick && Math.abs(x) > 30)) go(x < 0 ? 1 : -1)
    else if (y > 110 || (quick && y > 50)) closeSheet()
    else if (Math.abs(x) < 8 && y < 8 && e.type === 'pointerup') toggle()
  }

  function key(e) {
    if (!top) return
    if (e.key === 'Escape') { e.stopPropagation(); closeSheet() }
    else if (e.key === ' ' || e.key === 'k') { e.preventDefault(); toggle() }
    else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); go(1) }
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); go(-1) }
    else if (e.key === 'm') sound()
  }
  $effect(() => {
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = prev }
  })

  function pop(node, { out = false } = {}) {
    if (reduced()) return { duration: 120, css: (t) => `opacity:${t}` }
    return { duration: out ? 180 : 260, css: (t) => `opacity:${t};transform:scale(${0.96 + 0.04 * t})` }
  }
</script>

<svelte:window onkeydown={key} />

<div class="pl" role="dialog" aria-modal="true" aria-label="Video" in:pop out:pop={{ out: true }}>
  <div class="top">
    {#if list.length > 1}<span class="count num">{i + 1} / {list.length}</span>{:else}<span></span>{/if}
    <button class="round" onclick={closeSheet} aria-label="Close"><Icon name="close" size={22} /></button>
  </div>

  <div class="row">
    {#if list.length > 1}
      <button class="round side" onclick={() => go(-1)} disabled={i === 0} aria-label="Previous video"><Icon name="left" size={22} /></button>
    {/if}

    {#key c?.id}
      <div class="stage" style:--c={c?.color} style:transform={drag.x || drag.y ? `translate(${drag.x}px, ${drag.y}px)` : ''}
        class:dragging={drag.x || drag.y}
        role="presentation" onpointerdown={down} onpointermove={move} onpointerup={up} onpointercancel={up}>
        {#if c?.video}
          <video bind:this={vid} {src} poster={c.thumb} playsinline loop preload="auto" muted={muted}
            onplaying={() => { ready = true; paused = false; ahead(list[i + 1]?.video); ahead(list[i - 1]?.video) }} onpause={() => (paused = true)}
            ontimeupdate={(e) => (pct = e.currentTarget.duration ? e.currentTarget.currentTime / e.currentTarget.duration : 0)}></video>
          {#if paused}<span class="big-play"><Icon name="play" fill size={34} /></span>{/if}
          {#if !ready && !paused}<span class="spin" aria-label="Loading"></span>{/if}
          <button class="bar" onclick={seek} aria-label="Skip to"><i style="transform:scaleX({pct})"></i></button>
        {:else if c}
          {#if c.thumb}<img class="poster" class:gone={ready} src={c.thumb} alt="" />{/if}
          <iframe src={tiktokPlayer(c.id)} title="TikTok video" allow="autoplay; fullscreen; encrypted-media; picture-in-picture"
            class:on={ready} onload={() => (ready = true)}></iframe>
          {#if !ready}<span class="spin" aria-label="Loading"></span>{/if}
        {/if}
      </div>
    {/key}

    {#if list.length > 1}
      <button class="round side" onclick={() => go(1)} disabled={i === list.length - 1} aria-label="Next video"><Icon name="right" size={22} /></button>
    {/if}
  </div>

  {#if c}
    <div class="info">
      {#if c.cap}<p class="cap">{c.cap}</p>{/if}
      <div class="meta num">
        {#if c.views != null}<span><Icon name="play" fill size={14} />{compact(c.views)} views</span>{/if}
        {#if c.likes != null}<span><Icon name="heart" size={14} />{compact(c.likes)}</span>{/if}
        {#if c.comments != null}<span><Icon name="chat" size={14} />{compact(c.comments)}</span>{/if}
        {#if c.date}<span>{shortDate(c.date)}</span>{/if}
        {#if !c.mine}<span>@{c.acc}</span>{/if}
      </div>
      <div class="acts">
        <a class="pill" href={c.url} target="_blank" rel="noopener"><Icon name="tiktok" size={16} />Open in TikTok</a>
        {#if c.video}
          <button class="round sm" onclick={sound} aria-label={muted ? 'Sound on' : 'Sound off'}><Icon name={muted ? 'volumeOff' : 'volume'} size={19} /></button>
        {/if}
        {#if list.length > 1}
          <span class="phone-nav">
            <button class="round sm" onclick={() => go(-1)} disabled={i === 0} aria-label="Previous video"><Icon name="left" size={19} /></button>
            <button class="round sm" onclick={() => go(1)} disabled={i === list.length - 1} aria-label="Next video"><Icon name="right" size={19} /></button>
          </span>
        {/if}
      </div>
    </div>
  {/if}

</div>

<style>
  .pl {
    position: fixed; inset: 0; z-index: 70; display: flex; flex-direction: column; color: oklch(0.97 0.005 90);
    background: oklch(0.13 0.008 85); padding: var(--safe-t) 0 var(--safe-b);
  }
  .top { display: flex; align-items: center; justify-content: space-between; padding: 8px 10px 6px 16px; min-height: 56px; }
  .count { font-size: 14px; font-weight: 600; opacity: 0.8; }
  .round {
    width: 44px; height: 44px; border-radius: 99px; display: grid; place-items: center; flex: none;
    background: oklch(1 0 0 / 0.12); color: inherit; transition: transform 140ms var(--ease-out), background-color 160ms ease, opacity 160ms ease;
  }
  .round:active { transform: scale(0.92); }
  .round:disabled { opacity: 0.3; cursor: default; }
  .round.sm { width: 40px; height: 40px; }
  @media (hover: hover) and (pointer: fine) { .round:not(:disabled):hover { background: oklch(1 0 0 / 0.2); } }

  .row { flex: 1; min-height: 0; display: flex; align-items: center; justify-content: center; gap: 20px; padding: 0 0 4px; }
  .side { display: none; }
  .stage {
    position: relative; height: 100%; max-width: 100%; aspect-ratio: 9 / 16; overflow: hidden;
    background: var(--c, oklch(0.2 0.01 85)); touch-action: none; user-select: none; -webkit-user-select: none;
    transition: transform 260ms var(--ease-out);
  }
  .stage.dragging { transition: none; }
  video, iframe, .poster { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
  video { object-fit: contain; background: transparent; }
  .poster { object-fit: cover; transition: opacity 300ms ease; }
  .poster.gone { opacity: 0; }
  iframe { opacity: 0; transition: opacity 300ms ease; }
  iframe.on { opacity: 1; }
  .big-play {
    position: absolute; left: 50%; top: 50%; width: 76px; height: 76px; margin: -38px 0 0 -38px; border-radius: 99px;
    display: grid; place-items: center; background: oklch(0 0 0 / 0.45); pointer-events: none;
    animation: popin 180ms var(--ease-out);
  }
  @keyframes popin { from { transform: scale(0.85); opacity: 0; } }
  .spin {
    position: absolute; left: 50%; top: 50%; width: 36px; height: 36px; margin: -18px 0 0 -18px; border-radius: 99px;
    border: 3px solid oklch(1 0 0 / 0.25); border-top-color: oklch(1 0 0 / 0.95); pointer-events: none;
    opacity: 0; animation: spin 700ms linear infinite, show 1ms 350ms forwards;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  @keyframes show { to { opacity: 1; } }
  .bar { position: absolute; left: 0; right: 0; bottom: 0; height: 22px; display: flex; align-items: flex-end; }
  .bar i { display: block; width: 100%; height: 3px; background: oklch(0.98 0 0); transform-origin: left; transition: transform 250ms linear; }
  .bar::before { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 3px; background: oklch(1 0 0 / 0.2); }

  .info { padding: 12px 16px 14px; display: flex; flex-direction: column; gap: 8px; max-width: 560px; width: 100%; margin: 0 auto; }
  .cap { font-size: 15px; font-weight: 500; line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden; }
  .meta { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 14px; opacity: 0.8; }
  .meta span { display: inline-flex; align-items: center; gap: 5px; }
  .acts { display: flex; align-items: center; gap: 8px; margin-top: 2px; }
  .pill {
    display: inline-flex; align-items: center; gap: 7px; height: 40px; padding: 0 16px; border-radius: 99px;
    background: oklch(1 0 0 / 0.12); color: inherit; text-decoration: none; font-weight: 600; font-size: 14px;
  }
  .phone-nav { margin-left: auto; display: flex; gap: 8px; }

  @media (min-width: 900px) {
    .row { padding: 0 24px 8px; }
    .side { display: grid; }
    .stage { border-radius: 18px; }
    .phone-nav { display: none; }
  }
</style>
