<script>
  // The plan on one screen (strategy/plan.json): the idea in one line, what to post each week (each kind with her own
  // best video of it, tap to watch), what's coming, the rules for every video, and the goals with live progress.
  // The full documents are one tap away, and open here.
  import { app } from '../lib/live.svelte.js'
  import { route, link } from '../lib/router.svelte.js'
  import { get } from '../lib/api.js'
  import { marked } from 'marked'
  import { shortDate, dayParts, todayPH } from '../lib/format.js'
  import { inview } from '../lib/motion.js'
  import Icon from '../components/Icon.svelte'
  import Thumb from '../components/Thumb.svelte'
  import { clip, play } from '../lib/media.js'

  const today = todayPH()
  const id = $derived(route.parts.slice(1).join('/'))
  const plan = $derived(app.content?.plan)
  const docs = $derived(app.content?.docs || [])
  let showDocs = $state(false)

  // what's coming: the step we're in and the ones after it
  const steps = $derived((plan?.ahead?.steps || []).filter((x) => x.end >= today))
  function range(x) {
    if (x.start <= today) return `Now to ${shortDate(x.end)}`
    const a = dayParts(x.start), b = dayParts(x.end)
    return a.mon === b.mon && a.year === b.year ? `${a.mon} ${a.day} to ${b.day}` : `${shortDate(x.start)} to ${shortDate(x.end)}`
  }

  // the goals for mid-January (strategy section 11), filled from the weekly numbers
  const sb = $derived(app.content?.stats?.scoreboard || {})
  const goals = $derived([
    { k: 'Lightstick help videos', v: sb.clinic_count_latest30 || 0, goal: 12, show: `${sb.clinic_count_latest30 || 0} of 12` },
    { k: 'They get double the normal views', v: sb.clinic_median_x_normal || 0, goal: 2,
      show: sb.clinic_median_x_normal ? `${sb.clinic_median_x_normal.toFixed(1)}× now` : 'not yet' },
    { k: 'Videos that get comments', v: sb.zero_comment_share_12m == null ? 0 : 1 - sb.zero_comment_share_12m, goal: 0.6,
      show: sb.zero_comment_share_12m == null ? '–' : `${Math.round((1 - sb.zero_comment_share_12m) * 100)}% of 60%` },
    { k: 'Videos with 10,000+ views', v: sb.breakouts_since_plan?.length || 0, goal: 3, show: `${sb.breakouts_since_plan?.length || 0} of 3` },
  ].map((g) => ({ ...g, fill: Math.min(1, g.v / g.goal), ok: g.v >= g.goal })))
  let seenG = $state(false)

  // ---------- one document ----------
  let html = $state('')
  let err = $state('')
  let body = $state()
  $effect(() => {
    if (!id) return
    html = ''
    err = ''
    get(`/api/doc?id=${encodeURIComponent(id)}`).then((r) => (html = marked.parse(r.text))).catch((e) => (err = e.message))
  })
  $effect(() => {
    if (!html || !body) return
    // links to other documents open here; web links in a new tab
    body.querySelectorAll('a[href]').forEach((a) => {
      const href = a.getAttribute('href')
      if (/^https?:/.test(href)) { a.target = '_blank'; a.rel = 'noopener' }
      else {
        const target = docs.find((d) => d.id.endsWith(href.replace(/^\.{0,2}\//, '').split('#')[0]))
        if (target) a.setAttribute('href', link('/plan/' + target.id))
      }
    })
  })
</script>

<div class="content">
  {#if id}
    <a class="back" href={link('/plan')}><Icon name="left" size={18} /> Plan</a>
    {#if err}<p class="empty">{err}</p>
    {:else if !html}<div class="skel" style="height:28px;width:60%;margin:20px 0"></div><div class="skel" style="height:200px"></div>
    {:else}<article class="prose" bind:this={body}>{@html html}</article>{/if}

  {:else}
    <div class="page-head"><h1>Plan</h1></div>
    {#if !plan}
      <p class="empty">{app.content ? 'No plan yet.' : 'Loading…'}</p>
    {:else}
      <p class="idea">{plan.line}</p>

      <section class="section">
        <div class="section-head"><h2>Each week</h2><span class="target num"><Icon name="videos" size={16} />{plan.week.target} videos</span></div>
        <div class="rail kinds">
          {#each plan.week.kinds as x}
            {@const ex = (x.examples || []).map((id) => clip(id))}
            <div class="kind card">
              {#if ex.length}
                <Thumb c={ex[0]} onclick={() => play(ex, 0)} round={14} />
              {:else}
                <span class="kpic tint-0"><Icon name={x.icon} duo size={36} /></span>
              {/if}
              <span class="kn"><Icon name={x.icon} size={15} />{x.name}</span>
              {#if x.what}<span class="kd">{x.what}</span>{/if}
              <span class="often">{x.often}</span>
            </div>
          {/each}
        </div>
      </section>

      {#if steps.length}
        <section class="section">
          <div class="section-head"><h2>Coming up</h2></div>
          <ol class="line">
            {#each steps as x, i}
              <li class:now={x.start <= today}>
                <span class="when num">{range(x)}</span>
                <b class="what">{x.what}</b>
                <span class="post"><Icon name="videos" size={15} />Post: {x.post}</span>
              </li>
            {/each}
          </ol>
        </section>
      {/if}

      <section class="section">
        <div class="section-head"><h2>In every video</h2></div>
        <div class="rules">
          {#each plan.rules.items as r, i}
            <div class="rule card"><span class="rn num">{i + 1}</span><Icon name={r.icon} duo size={26} /><span>{r.text}</span></div>
          {/each}
        </div>
      </section>

      <section class="section">
        <div class="section-head"><h2>Goals</h2><span class="faint">by mid-January</span></div>
        <div class="card goals" use:inview={() => (seenG = true)}>
          {#each goals as g, i}
            <div class="goal">
              <span class="gk">{g.k}{#if g.ok}<Icon name="checkCircle" size={16} />{/if}</span>
              <span class="gv num" class:paid-t={g.ok}>{g.show}</span>
              <span class="gtrack"><span class="gfill" class:ok={g.ok} style="transform:scaleX({seenG ? Math.max(g.fill, 0.015) : 0});transition-delay:{i * 80}ms"></span></span>
            </div>
          {/each}
        </div>
      </section>
    {/if}

    <section class="section">
      <button class="btn soft wide" onclick={() => (showDocs = !showDocs)}>
        <Icon name="plan" size={18} /> {showDocs ? 'Hide documents' : `All documents (${docs.length})`}
      </button>
      {#if showDocs}
        <div class="list docs">
          {#each docs as d (d.id)}
            <a class="doc" href={link('/plan/' + d.id)}><span class="clip">{d.title}</span><span class="g">{d.group}</span></a>
          {/each}
        </div>
      {/if}
    </section>
  {/if}
</div>

<style>
  .back { display: inline-flex; align-items: center; gap: 4px; margin: 4px 0 16px; color: var(--ink-2); text-decoration: none; font-weight: 500; }
  .prose { padding: 4px 4px 0; overflow-wrap: anywhere; }

  .idea {
    padding: 24px 22px 26px; border-radius: var(--r-xl); background: var(--hero); color: var(--on-hero);
    font-size: 24px; font-weight: 700; line-height: 1.25; letter-spacing: -0.02em; text-wrap: balance;
    box-shadow: 0 18px 40px -22px oklch(0.25 0.06 263 / 0.7), inset 0 0 0 1px var(--hero-line);
  }
  .target { display: inline-flex; align-items: center; gap: 6px; font-weight: 700; font-size: 15px; }

  .kind { width: 150px; display: flex; flex-direction: column; gap: 4px; padding: 8px 8px 12px; }
  .kpic { display: grid; place-items: center; aspect-ratio: 9 / 16; border-radius: 14px; }
  .kn { display: flex; align-items: center; gap: 5px; margin: 6px 4px 0; font-weight: 650; font-size: 15px; line-height: 1.25; }
  .kd { margin: 0 4px; font-size: 13px; line-height: 1.3; color: var(--ink-2); }
  .often { align-self: flex-start; margin: 4px 4px 0; font-size: 13px; font-weight: 600; color: var(--accent-ink); background: var(--accent-soft); padding: 3px 10px; border-radius: 99px; }
  @media (min-width: 900px) { .kinds { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); } .kind { width: auto; } }

  .line { list-style: none; margin: 0; padding: 0 0 0 4px; }
  .line li { position: relative; display: flex; flex-direction: column; gap: 2px; padding: 0 0 18px 26px; }
  .line li::before { content: ''; position: absolute; left: 5px; top: 8px; bottom: -8px; width: 2px; background: var(--line); }
  .line li:last-child::before { display: none; }
  .line li::after {
    content: ''; position: absolute; left: 0; top: 4px; width: 12px; height: 12px; border-radius: 99px;
    background: var(--surface); box-shadow: inset 0 0 0 2px var(--ink-3);
  }
  .line li.now::after { background: var(--accent); box-shadow: 0 0 0 4px var(--accent-tile); }
  .when { font-size: 13.5px; font-weight: 600; color: var(--ink-2); }
  .now .when { color: var(--ink); }
  .what { font-size: 16px; line-height: 1.3; }
  .post { display: inline-flex; align-items: center; gap: 6px; font-size: 14.5px; color: var(--ink-2); }

  .rules { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .rule { position: relative; display: flex; flex-direction: column; gap: 10px; padding: 16px 14px; font-weight: 600; font-size: 15px; line-height: 1.3; }
  .rule :global(svg) { color: var(--accent-ink); }
  .rn { position: absolute; top: 12px; right: 14px; font-size: 13px; font-weight: 700; color: var(--ink-3); }

  .goals { padding: 4px 16px; }
  .goal { display: grid; grid-template-columns: 1fr auto; gap: 6px 12px; padding: 12px 0; }
  .goal + .goal { border-top: 1px solid var(--line); }
  .gk { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; font-size: 15px; }
  .gk :global(svg) { color: var(--paid); }
  .gv { font-size: 14px; color: var(--ink-2); font-weight: 500; }
  .gtrack { grid-column: 1 / -1; height: 8px; border-radius: 99px; background: var(--surface-2); overflow: hidden; }
  .gfill { display: block; height: 100%; border-radius: 99px; background: var(--accent); transform-origin: left; transition: transform 900ms var(--ease-out); }
  .gfill.ok { background: var(--paid); }

  .docs { margin-top: 12px; }
  .doc { display: flex; align-items: center; gap: 12px; padding: 13px 16px; background: var(--surface); text-decoration: none; }
  .doc:active { background: var(--surface-2); }
  @media (hover: hover) and (pointer: fine) { .doc:hover { background: var(--surface-2); } }
  .doc .clip { flex: 1; font-weight: 500; }
  .g { flex: none; font-size: 13px; color: var(--ink-3); }
</style>
