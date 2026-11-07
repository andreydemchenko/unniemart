<script>
  // One video idea, in the order she needs it: is it done, when, a video like it (tap to watch), what fans asked,
  // the big text for the start, the steps, what to bring, the text to paste. Why, and the sources, at the bottom.
  import Sheet from './Sheet.svelte'
  import Icon from './Icon.svelte'
  import Segmented from './Segmented.svelte'
  import Thumb from './Thumb.svelte'
  import { app } from '../lib/live.svelte.js'
  import { copy, toast } from '../lib/ui.svelte.js'
  import { ideaIcon } from '../lib/kinds.js'
  import { ideaTitle } from '../lib/derive.js'
  import { plannedDays, compact, shortDate } from '../lib/format.js'
  import { ideaMedia, play } from '../lib/media.js'
  import * as act from '../lib/actions.js'
  import { marked } from 'marked'
  let { key, top = true } = $props()

  const found = $derived.by(() => {
    for (const b of app.content?.briefs || []) {
      const i = b.ideas.find((x) => x.key === key)
      if (i) return { idea: i, brief: b }
    }
    return null
  })
  const idea = $derived(found?.idea)
  const week = $derived(found?.brief?.week)
  const saved = $derived(app.ideas?.[key] || { status: 'todo', shots: [], facts: [], needs: [], link: '' })
  const m = $derived(ideaMedia(idea))
  const title = $derived(ideaTitle(idea?.title))
  const admin = $derived(!!app.me?.admin)
  let status = $state('todo')
  let link = $state('')
  $effect(() => { status = saved.status || 'todo'; link = saved.link || '' })

  const inline = (s) => marked.parseInline(s || '')
  const statusOptions = [{ value: 'todo', label: 'To film' }, { value: 'filmed', label: 'Filmed' }, { value: 'posted', label: 'Posted' }]

  async function setStatus(v) {
    try { await act.ideaSet(idea, week, { status: v }) } catch (e) { toast(e.message, { tone: 'bad' }) }
  }
  async function tick(list, i) {
    const cur = new Set(saved[list] || [])
    cur.has(i) ? cur.delete(i) : cur.add(i)
    try { await act.ideaSet(idea, week, { [list]: [...cur] }) } catch (e) { toast(e.message, { tone: 'bad' }) }
  }
  async function saveLink() {
    await act.ideaSet(idea, week, { link })
    toast('Link saved')
  }
  async function cp(text, what) {
    if (await copy(text)) toast(`${what} copied`)
  }
  const done = (list, i) => (saved[list] || []).includes(i)
  const days = $derived(plannedDays(idea?.post))
  // "1 to 2 s: say ..." → the time part as a small tag, the rest as the step
  function step(s) {
    const t = s.match(/^(?:First frame|\d+(?:\.\d+)?\s*(?:to|-|–)\s*\d+(?:\.\d+)?\s*s|\d+(?:\.\d+)?\s*s)\s*:\s*/i)
    const rest = t ? s.slice(t[0].length) : s
    return { at: t ? t[0].replace(/:\s*$/, '').replace(' to ', '–') : '', text: rest.charAt(0).toUpperCase() + rest.slice(1) }
  }
</script>

<Sheet tall {top}>
  {#if !idea}
    <p class="empty">This idea isn't in the plan any more.</p>
  {:else}
    <div class="head">
      <div class="tags">
        <span class="chip"><Icon name={ideaIcon(idea.format)} size={14} />{m.kind?.name || idea.format}</span>
        {#if idea.season && idea.season !== 'no season'}<span class="chip accent">{idea.season}</span>{/if}
        {#if idea.section === 'waiting'}<span class="chip late">When the box arrives</span>{/if}
      </div>
      <h1>{title.text}</h1>
      {#if title.when}<p class="cond"><Icon name="info" size={16} />{title.when}</p>{/if}
    </div>

    {#if idea.section !== 'waiting'}
      <Segmented options={statusOptions} bind:value={status} onchange={setStatus} label="Progress" />
      {#if status === 'posted'}
        <div class="linkrow">
          <input class="field" bind:value={link} placeholder="Link to the TikTok (optional)" inputmode="url" />
          <button class="btn ink sm" onclick={saveLink}>Save</button>
        </div>
      {/if}
      {#if days.film || days.post}
        <div class="days">
          {#if days.both}
            <span class="day"><Icon name="camera" size={20} /><span><small>Film and post</small><b>{days.post}</b></span></span>
          {:else}
            {#if days.film}<span class="day"><Icon name="camera" size={20} /><span><small>Film</small><b>{days.film}</b></span></span>{/if}
            {#if days.post}<span class="day"><Icon name="send" size={20} /><span><small>Post</small><b>{days.post}</b></span></span>{/if}
          {/if}
        </div>
      {/if}
    {:else if idea.blocked}
      <p class="blocked"><Icon name="clock" size={18} /> {idea.blocked}</p>
    {/if}

    {#if m.examples.length}
      <section>
        <h3>{m.own.length ? 'Your video that worked' : 'Like your best ones'}</h3>
        {#if m.examples.length === 1}
          {@const c = m.examples[0]}
          <div class="ex-one">
            <div class="ex-pic"><Thumb {c} views={false} onclick={() => play(m.examples, 0)} /></div>
            <div class="ex-t">
              {#if c.cap}<p class="ex-cap1">“{c.cap}”</p>{/if}
              {#if c.views != null}<p class="ex-views num"><b>{compact(c.views)}</b> views</p>{/if}
              {#if c.date}<p class="faint">{shortDate(c.date)}</p>{/if}
              <button class="btn soft sm" onclick={() => play(m.examples, 0)}><Icon name="play" fill size={15} />Watch</button>
            </div>
          </div>
        {:else}
          <div class="examples">
            {#each m.examples.slice(0, 3) as c, i (c.id)}
              <div class="ex">
                <Thumb {c} onclick={() => play(m.examples, i)} />
                {#if c.cap}<span class="ex-cap">{c.cap}</span>{/if}
              </div>
            {/each}
          </div>
        {/if}
      </section>
    {/if}

    {#each m.asked as a (a.clip.id)}
      <section>
        <h3>A fan asked</h3>
        <div class="asked">
          <div class="bubbles">
            {#each a.words.slice(0, 3) as w}<p class="bubble">{w}</p>{/each}
            <button class="on-video" onclick={() => play([a.clip])}>
              <Icon name="play" fill size={13} />on your video{#if a.clip.views != null}, {compact(a.clip.views)} views{/if}
            </button>
          </div>
          <div class="asked-pic"><Thumb c={a.clip} views={false} round={10} onclick={() => play([a.clip])} /></div>
        </div>
      </section>
    {/each}

    {#if idea.hook}
      <figure class="hook">
        <span class="k">Big text at the start</span>
        <blockquote>{idea.hook}</blockquote>
        <button class="icon-btn" aria-label="Copy" onclick={() => cp(idea.hook, 'Text')}><Icon name="copy" size={19} /></button>
      </figure>
    {/if}

    {#if idea.shots.length}
      <section>
        <h3>Steps <span class="count num">{(saved.shots || []).length} of {idea.shots.length}</span></h3>
        <ol class="checks steps">
          {#each idea.shots as s, i}
            {@const p = step(s)}
            <li><button class:on={done('shots', i)} onclick={() => tick('shots', i)}>
              <span class="box num">{#if done('shots', i)}<Icon name="check" size={14} />{:else}{i + 1}{/if}</span>
              <span>{#if p.at}<span class="at num">{p.at}</span>{/if}{@html inline(p.text)}</span></button></li>
          {/each}
        </ol>
      </section>
    {/if}

    {#if idea.needs.length}
      <section>
        <h3>Get ready</h3>
        <ul class="checks">
          {#each idea.needs as n, i}
            <li><button class:on={done('needs', i)} onclick={() => tick('needs', i)}>
              <span class="box sq"><Icon name="check" size={14} /></span><span>{@html inline(n)}</span></button></li>
          {/each}
        </ul>
      </section>
    {/if}

    {#each [['caption', 'Text under the video'], ['pinned', 'First comment (pin it)']] as [f, label]}
      {#if idea[f]}
        <section class="copyable">
          <h3>{label}</h3>
          <p class="text">{idea[f]}</p>
          <button class="btn soft sm" onclick={() => cp(idea[f], label)}><Icon name="copy" size={16} /> Copy</button>
        </section>
      {/if}
    {/each}
    {#if idea.caption}<p class="note">Change any word so it sounds like you.</p>{/if}

    {#snippet facts()}
      <section>
        <h3>Facts to check <span class="count num">{(saved.facts || []).length} of {idea.facts.length}</span></h3>
        <ul class="checks facts">
          {#each idea.facts as f, i}
            <li><button class:on={done('facts', i)} onclick={() => tick('facts', i)}>
              <span class="box sq"><Icon name="check" size={14} /></span>
              <span>
                <span class="claim">{f.claim}</span>
                {#if f.quote}<span class="quote">“{f.quote}”</span>{/if}
              </span></button>
              {#if f.url}<a class="src" href={f.url} target="_blank" rel="noopener">{f.src} <Icon name="arrowUpRight" size={13} /></a>
              {:else if f.src}<span class="src">{f.src}</span>{/if}
            </li>
          {/each}
        </ul>
      </section>
    {/snippet}
    {#if admin && idea.facts.length}{@render facts()}{/if}

    {#if idea.why || idea.sources.length || (!admin && idea.facts.length)}
      <details class="more">
        <summary><Icon name="info" size={18} /> Why this video{#if !admin && idea.facts.length}, facts{/if} and sources<Icon name="down" size={16} /></summary>
        {#if idea.why}<p class="why">{@html inline(idea.why)}</p>{/if}
        {#if !admin && idea.facts.length}{@render facts()}{/if}
        {#if idea.sources.length}
        <ul class="sources">
          {#each idea.sources as s}
            <li>
              <b>{s.id}</b>
              <span>{s.text || s.kind}</span>
              {#if s.url}<a href={s.url} target="_blank" rel="noopener" aria-label="Open {s.id}"><Icon name="arrowUpRight" size={16} /></a>{/if}
            </li>
          {/each}
        </ul>
        {/if}
      </details>
    {/if}
  {/if}
</Sheet>

<style>
  .head { padding: 2px 0 16px; }
  .tags { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-bottom: 10px; }
  .head h1 { font-size: 24px; line-height: 1.2; }
  .cond { display: flex; align-items: center; gap: 6px; margin-top: 8px; font-size: 14.5px; color: var(--ink-2); }
  .linkrow { display: flex; gap: 8px; margin-top: 12px; align-items: center; }
  .blocked { display: flex; gap: 8px; align-items: flex-start; color: var(--ink-2); padding: 12px 14px; border-radius: var(--r); background: var(--surface-2); }

  .days { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin-top: 12px; }
  .day { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: var(--r); background: var(--surface-2); }
  .day > span { display: flex; flex-direction: column; line-height: 1.2; }
  .day small { font-size: 13px; color: var(--ink-2); font-weight: 500; }
  .day b { font-size: 17px; }

  section { margin-top: 24px; }
  h3 { display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 650; color: var(--ink); margin-bottom: 10px; }
  h3 .count { margin-left: auto; font-weight: 500; font-size: 14px; color: var(--ink-3); }
  section p { line-height: 1.5; }
  section :global(a) { text-underline-offset: 3px; }

  .examples { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }
  .ex { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
  .ex-cap { font-size: 13px; line-height: 1.3; color: var(--ink-2); display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

  .ex-one { display: flex; gap: 16px; align-items: center; }
  .ex-pic { flex: none; width: 112px; }
  .ex-t { display: flex; flex-direction: column; align-items: flex-start; gap: 4px; min-width: 0; }
  .ex-cap1 { font-weight: 500; line-height: 1.35; }
  .ex-views { font-size: 15px; color: var(--ink-2); }
  .ex-views b { font-size: 24px; color: var(--ink); }
  .ex-t .btn { margin-top: 8px; }
  .asked { display: flex; gap: 12px; align-items: flex-start; }
  .bubbles { flex: 1; min-width: 0; display: flex; flex-direction: column; align-items: flex-start; gap: 6px; }
  .bubble {
    padding: 10px 14px; border-radius: 18px 18px 18px 6px; background: var(--surface-2); font-size: 15px; line-height: 1.4;
    overflow-wrap: anywhere;
  }
  .on-video { display: inline-flex; align-items: center; gap: 5px; margin: 2px 0 0 4px; font-size: 13px; font-weight: 600; color: var(--ink-2); }
  .asked-pic { flex: none; width: 64px; }

  .hook { position: relative; margin: 24px 0 0; padding: 16px 52px 18px 18px; border-radius: var(--r-lg); background: var(--hero); color: var(--on-hero); }
  .hook .k { font-size: 13px; font-weight: 600; color: var(--on-hero-2); }
  .hook blockquote { margin: 6px 0 0; font-size: 21px; font-weight: 700; line-height: 1.25; }
  .hook .icon-btn { position: absolute; top: 8px; right: 8px; color: var(--on-hero); }

  .checks { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 2px; }
  .checks li { display: flex; align-items: flex-start; gap: 6px; }
  .checks button { flex: 1; display: flex; align-items: flex-start; gap: 12px; text-align: left; padding: 9px 4px; border-radius: 10px; line-height: 1.4; }
  .box {
    flex: none; width: 26px; height: 26px; border-radius: 99px; display: grid; place-items: center; font-size: 13px; font-weight: 700;
    box-shadow: inset 0 0 0 2px var(--surface-3); color: var(--ink-2); transition: background-color 160ms ease, box-shadow 160ms ease, color 160ms ease;
  }
  .box.sq { border-radius: 8px; color: transparent; }
  .on .box { background: var(--ink); box-shadow: none; color: var(--bg); }
  .on .box :global(svg) { animation: tickin 260ms var(--ease-out); }
  @keyframes tickin { from { transform: scale(0.4); opacity: 0; } }
  .checks button > span:last-child { padding-top: 2px; }
  .on > span:last-child { color: var(--ink-3); }
  .at { display: inline-block; margin-right: 6px; padding: 0 7px; border-radius: 6px; font-size: 12.5px; font-weight: 700; background: var(--accent-soft); color: var(--accent-ink); }
  .facts .claim { display: block; font-weight: 500; }
  .facts .quote { display: block; font-size: 13.5px; color: var(--ink-2); margin-top: 2px; }
  .src { flex: none; display: inline-flex; align-items: center; gap: 2px; font-size: 12.5px; font-weight: 600; margin-top: 10px;
    padding: 2px 8px; border-radius: 99px; background: var(--surface-2); text-decoration: none; color: var(--ink-2); }

  .copyable .text { padding: 14px 16px; border-radius: var(--r); background: var(--surface-2); white-space: pre-wrap; margin-bottom: 10px; }
  .note { font-size: 13.5px; color: var(--ink-3); margin-top: 10px; }

  .more { margin-top: 28px; border-top: 1px solid var(--line); }
  .more summary { display: flex; align-items: center; gap: 8px; min-height: 52px; cursor: pointer; font-weight: 600; color: var(--ink-2); list-style: none; }
  .more summary::-webkit-details-marker { display: none; }
  .more summary :global(svg:last-child) { margin-left: auto; transition: transform 200ms var(--ease-out); }
  .more[open] summary :global(svg:last-child) { transform: rotate(180deg); }
  .more section { margin-top: 8px; }
  .why { line-height: 1.5; margin-bottom: 12px; }
  .sources { list-style: none; margin: 16px 0 0; padding: 0; font-size: 13.5px; }
  .sources li { display: flex; gap: 10px; align-items: flex-start; padding: 8px 0; border-top: 1px solid var(--line); color: var(--ink-2); }
  .sources b { color: var(--ink); flex: none; min-width: 30px; }
  .sources span { flex: 1; overflow-wrap: anywhere; }
  .sources a { flex: none; color: var(--ink); }
</style>
