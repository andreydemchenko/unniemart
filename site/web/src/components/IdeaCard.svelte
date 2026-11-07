<script>
  // A video idea as a poster: the picture of a video like it, the kind on top, the title and when at the bottom.
  // Tap to open it. Used on Home and Videos.
  import Icon from './Icon.svelte'
  import { app } from '../lib/live.svelte.js'
  import { openSheet } from '../lib/ui.svelte.js'
  import { plannedText } from '../lib/format.js'
  import { status, ideaTitle } from '../lib/derive.js'
  import { ideaMedia } from '../lib/media.js'
  import { ideaIcon } from '../lib/kinds.js'
  let { idea, size = 'lg', showWhen = true } = $props()

  const st = $derived(status(app.ideas, idea.key))
  const m = $derived(ideaMedia(idea))
  const t = $derived(ideaTitle(idea.title))
  const when = $derived(showWhen ? plannedText(idea.post) : '')
  let loaded = $state(false)
</script>

<button class="poster {size}" class:done={st === 'posted'} class:skipped={st === 'skipped'} style:--c={m.cover?.color}
  onclick={() => openSheet('idea', { key: idea.key })}>
  {#if m.cover?.thumb}
    <img src={m.cover.thumb} alt="" loading="lazy" decoding="async" class:on={loaded} onload={() => (loaded = true)} />
  {:else}
    <span class="ph"><Icon name={ideaIcon(idea.format)} duo size={size === 'lg' ? 44 : 32} /></span>
  {/if}
  <span class="kind"><Icon name={ideaIcon(idea.format)} size={13} />{m.kind?.name || idea.format}</span>
  {#if st === 'posted'}<span class="mark ok" aria-label="Posted"><Icon name="check" size={16} /></span>
  {:else if st === 'filmed'}<span class="mark film" aria-label="Filmed"><Icon name="camera" fill size={14} /></span>{/if}
  <span class="foot">
    <span class="title">{t.text}</span>
    {#if t.when}<span class="sub">{t.when}</span>
    {:else if when}<span class="sub num">{when}</span>{/if}
  </span>
</button>

<style>
  .poster {
    position: relative; display: block; flex: none; overflow: hidden; isolation: isolate; text-align: left;
    border-radius: 22px; background: var(--c, var(--hero)); color: oklch(0.99 0 0);
    box-shadow: var(--shadow); transition: transform 160ms var(--ease-out);
  }
  .poster:active { transform: scale(0.97); }
  .lg { width: min(64vw, 248px); aspect-ratio: 3 / 4.3; }
  .sm { width: min(42vw, 168px); aspect-ratio: 3 / 4.4; border-radius: 18px; }
  img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity 260ms ease; }
  img.on { opacity: 1; }
  .ph { position: absolute; inset: 0; display: grid; place-items: center; padding-bottom: 30%; color: var(--on-hero-2); background: var(--hero); }
  .poster::after {
    content: ''; position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background: linear-gradient(to top, oklch(0.12 0.02 264 / 0.92) 0%, oklch(0.12 0.02 264 / 0.55) 38%, transparent 64%),
      linear-gradient(to bottom, oklch(0.12 0.02 264 / 0.4), transparent 26%);
  }
  .kind, .mark, .foot { position: absolute; z-index: 1; }
  .kind {
    top: 10px; left: 10px; display: inline-flex; align-items: center; gap: 5px; max-width: calc(100% - 52px);
    height: 26px; padding: 0 10px 0 8px; border-radius: 99px; background: oklch(0.14 0.02 264 / 0.6);
    font-size: 12px; font-weight: 650; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .mark { top: 10px; right: 10px; width: 28px; height: 28px; border-radius: 99px; display: grid; place-items: center; }
  .mark.ok { background: var(--paid); color: white; }
  .mark.film { background: oklch(0.99 0 0); color: var(--ink); }
  .foot { left: 0; right: 0; bottom: 0; display: flex; flex-direction: column; gap: 4px; padding: 0 14px 14px; }
  .title { font-size: 17px; font-weight: 700; line-height: 1.22; letter-spacing: -0.01em; text-wrap: balance;
    display: -webkit-box; -webkit-line-clamp: 3; line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
  .sm .title { font-size: 14.5px; }
  .sub { font-size: 13px; font-weight: 550; color: oklch(0.99 0 0 / 0.78); }
  .sm .foot { padding: 0 12px 12px; }
  .done img { filter: saturate(0.3) brightness(0.8); }
  .skipped { opacity: 0.45; }
  @media (min-width: 900px) {
    .lg { width: auto; }
    .sm { width: auto; }
  }
</style>
