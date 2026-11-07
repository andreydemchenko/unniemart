<script>
  // Videos: this week's goal (3 posts), what to film as pictures (each idea shows a video like it), then her own
  // videos (tap to watch) and which kinds get the most views.
  import { app } from '../lib/live.svelte.js'
  import { todayPH, daysFrom, rangeText } from '../lib/format.js'
  import { currentBrief, status } from '../lib/derive.js'
  import { ideaMedia, aheadAll } from '../lib/media.js'
  import Icon from '../components/Icon.svelte'
  import IdeaCard from '../components/IdeaCard.svelte'
  import MyVideos from '../components/MyVideos.svelte'

  const today = todayPH()
  const brief = $derived(currentBrief(app.content, today))
  const target = $derived(app.content?.plan?.week?.target || 3)
  const main = $derived((brief?.ideas || []).filter((i) => i.section === 'main'))
  const core = $derived(main.slice(0, target))
  const more = $derived([...main.slice(target), ...(brief?.ideas || []).filter((i) => i.section === 'also')])
  const waiting = $derived((brief?.ideas || []).filter((i) => i.section === 'waiting'))
  const posted = $derived((brief?.ideas || []).filter((i) => status(app.ideas, i.key) === 'posted').length)
  const lastPost = $derived((app.content?.stats?.videos || []).reduce((a, v) => (v.date > a ? v.date : a), ''))
  const quiet = $derived(lastPost ? -daysFrom(lastPost.slice(0, 10), today) : null)

  $effect(() => { if (core.length) aheadAll(core.map((i) => ideaMedia(i).cover?.video)) })
</script>

<div class="content">
  <div class="page-head">
    <h1>Videos</h1>
    {#if brief}
      <div class="goal" role="img" aria-label="{posted} of {target} posted this week">
        {#each Array(target) as _, n}
          <span class="dot" class:on={n < posted} style="transition-delay:{n * 80}ms">{#if n < posted}<Icon name="check" size={16} />{/if}</span>
        {/each}
      </div>
    {/if}
  </div>

  {#if !brief}
    <p class="empty">{app.content ? 'No plan for this week yet. It comes every Monday.' : 'Loading…'}</p>
  {:else}
    <div class="week">
      <span class="num"><b>{posted} of {target}</b> posted{#if brief.range}&nbsp;· {rangeText(brief.range)}{/if}</span>
      {#if quiet != null && quiet >= 7}<span class="quiet"><Icon name="hourglass" size={14} />Last video {quiet} days ago</span>{/if}
    </div>

    <section class="section first">
      <div class="section-head"><h2>Film these {core.length}</h2></div>
      <div class="rail posters">
        {#each core as idea (idea.key)}<IdeaCard {idea} />{/each}
      </div>
    </section>

    {#if more.length}
      <section class="section">
        <div class="section-head"><h2>If there is time</h2></div>
        <div class="rail posters sm">
          {#each more as idea (idea.key)}<IdeaCard {idea} size="sm" />{/each}
        </div>
      </section>
    {/if}

    {#if waiting.length}
      <section class="section">
        <div class="section-head"><h2>When the box arrives</h2></div>
        <div class="rail posters sm">
          {#each waiting as idea (idea.key)}<IdeaCard {idea} size="sm" showWhen={false} />{/each}
        </div>
      </section>
    {/if}
  {/if}

  <MyVideos />
</div>

<style>
  .goal { display: flex; gap: 6px; }
  .dot {
    width: 32px; height: 32px; border-radius: 99px; display: grid; place-items: center; color: var(--on-accent);
    box-shadow: inset 0 0 0 2.5px var(--surface-3); transition: background-color 300ms ease, box-shadow 300ms ease;
  }
  .dot.on { background: var(--accent); box-shadow: none; }
  .week { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; margin: -6px 4px 0; font-size: 15px; color: var(--ink-2); }
  .week b { color: var(--ink); font-weight: 700; }
  .quiet { display: inline-flex; align-items: center; gap: 6px; padding: 4px 11px; border-radius: 99px;
    font-size: 13.5px; font-weight: 650; color: var(--late-ink); background: var(--late-soft); }
  .first { margin-top: 20px; }
  .posters { gap: 12px; }
  .posters.sm { gap: 10px; }
  @media (min-width: 900px) {
    .posters { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); max-width: 820px; }
    .posters.sm { grid-template-columns: repeat(5, minmax(0, 1fr)); max-width: none; }
  }
</style>
