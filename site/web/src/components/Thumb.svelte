<script>
  // A video as a picture: its cover (tall, like on TikTok) with the views on it. Tap to play. The cover's own colour
  // shows while the picture loads, so a grid never flashes white.
  import Icon from './Icon.svelte'
  import { compact } from '../lib/format.js'
  let { c, onclick, views = true, hit = false, icon = 'tiktok', round = 14 } = $props()
  let loaded = $state(false)
  function seen(img) {
    if (img.complete && img.naturalWidth) loaded = true
  }
</script>

<button class="th" style:--c={c.color} style:border-radius="{round}px" {onclick} aria-label="Play video{c.cap ? ': ' + c.cap : ''}">
  {#if c.thumb}
    <img src={c.thumb} alt="" loading="lazy" decoding="async" class:on={loaded} onload={() => (loaded = true)} use:seen />
  {:else}
    <span class="ph"><Icon name={icon} duo size={30} /></span>
  {/if}
  {#if hit}<span class="hit"><Icon name="fire" fill size={13} />Hit</span>{/if}
  {#if views && c.views != null}
    <span class="v num"><Icon name="play" fill size={12} />{compact(c.views)}</span>
  {:else}
    <span class="pl"><Icon name="play" fill size={16} /></span>
  {/if}
</button>

<style>
  .th {
    position: relative; display: block; width: 100%; aspect-ratio: 9 / 16; overflow: hidden;
    background: var(--c, var(--surface-3)); isolation: isolate;
    transition: transform 160ms var(--ease-out);
  }
  .th:active { transform: scale(0.97); }
  img {
    position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0;
    transition: opacity 260ms ease;
  }
  img.on { opacity: 1; }
  .ph { position: absolute; inset: 0; display: grid; place-items: center; color: var(--ink-3); }
  .th::after {
    content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 42%; pointer-events: none;
    background: linear-gradient(to top, oklch(0 0 0 / 0.55), transparent);
  }
  .v, .pl {
    position: absolute; z-index: 1; left: 8px; bottom: 7px; display: inline-flex; align-items: center; gap: 4px;
    color: oklch(0.99 0 0); font-size: 13px; font-weight: 700; text-shadow: 0 1px 2px oklch(0 0 0 / 0.4);
  }
  .pl { left: 50%; bottom: 50%; transform: translate(-50%, 50%); width: 40px; height: 40px; justify-content: center;
    border-radius: 99px; background: oklch(0 0 0 / 0.35); }
  .hit {
    position: absolute; z-index: 1; top: 7px; left: 7px; display: inline-flex; align-items: center; gap: 3px;
    padding: 2px 8px 2px 6px; border-radius: 99px; background: oklch(0.99 0 0); color: oklch(0.21 0.025 264);
    font-size: 12px; font-weight: 700;
  }
</style>
