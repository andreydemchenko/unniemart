<script>
  // Only what she needs at a glance: money to collect, who is late (remind them in one go), who pays this week,
  // this week's videos as pictures, the to-dos.
  import { app } from '../lib/live.svelte.js'
  import { link } from '../lib/router.svelte.js'
  import { openSheet } from '../lib/ui.svelte.js'
  import { peso, when, todayPH, dayParts, daysFrom, plural } from '../lib/format.js'
  import { liveLines, byBucket, total, currentBrief, status } from '../lib/derive.js'
  import { ideaMedia, aheadAll } from '../lib/media.js'
  import * as act from '../lib/actions.js'
  import { collapse } from '../lib/motion.js'
  import { flip } from 'svelte/animate'
  import Icon from '../components/Icon.svelte'
  import Money from '../components/Money.svelte'
  import SyncPill from '../components/SyncPill.svelte'
  import StackBar from '../components/StackBar.svelte'
  import PeopleRail from '../components/PeopleRail.svelte'
  import IdeaCard from '../components/IdeaCard.svelte'

  const today = todayPH()
  const b = $derived(byBucket(app.desk))
  const collect = $derived(total(liveLines(app.desk)))
  const weekSum = $derived(total(b.week))
  const lateSum = $derived(total(b.late))
  // to-dos with a date first (soonest first), then the rest
  const openTasks = $derived(app.tasks.filter((t) => !t.done_at)
    .sort((a, b) => (a.due || '9999') < (b.due || '9999') ? -1 : (a.due || '9999') > (b.due || '9999') ? 1 : a.id - b.id))
  let allTasks = $state(false)
  let ticking = $state(new Set())
  function tick(t) {
    ticking = new Set([...ticking, t.id])
    setTimeout(() => act.taskDone(t), 420)          // let the tick show before the row leaves
  }
  const brief = $derived(currentBrief(app.content, today))
  const target = $derived(app.content?.plan?.week?.target || 3)
  const week = $derived((brief?.ideas || []).filter((i) => i.section === 'main').slice(0, target))
  const posted = $derived((brief?.ideas || []).filter((i) => status(app.ideas, i.key) === 'posted').length)
  const lastPost = $derived((app.content?.stats?.videos || []).reduce((a, v) => (v.date > a ? v.date : a), ''))
  const quiet = $derived(lastPost ? -daysFrom(lastPost.slice(0, 10), today) : null)
  const d = dayParts(today)

  // the example videos of this week's ideas start loading while she looks, so a tap plays at once
  $effect(() => { if (week.length) aheadAll(week.map((i) => ideaMedia(i).cover?.video)) })

  const person = (id) => (id === app.me?.id ? 'You' : app.people[id] || 'Anyone')
</script>

<div class="home">
  <div class="top">
    <span class="date">{d.wd}, {d.mon} {d.day}</span>
    <SyncPill />
  </div>

  <div class="grid">
    <header class="hero">
      <p class="label">Money to collect</p>
      {#if app.ready}
        <p class="total"><Money value={collect} roll /></p>
      {:else}
        <p class="total"><span class="skel dark" style="display:inline-block;width:210px;height:46px"></span></p>
      {/if}
      <div class="stack">
        <StackBar height={8} parts={[
          { key: 'late', v: lateSum, tone: 'late', label: 'Late', text: peso(lateSum) },
          { key: 'week', v: weekSum, tone: 'week', label: 'This week', text: peso(weekSum) },
          { key: 'rest', v: Math.max(0, collect - lateSum - weekSum), tone: 'hero-rest', label: 'Later' },
        ]} />
      </div>
      <div class="split">
        <a class="stat" href={link('/orders?f=late')}>
          <span class="k"><i class="dot late"></i>Late</span>
          <span class="v num">{peso(lateSum)}</span>
          <span class="n">{plural(b.late.length, 'person', 'people')}</span>
        </a>
        <a class="stat" href={link('/orders?f=week')}>
          <span class="k"><i class="dot week"></i>This week</span>
          <span class="v num">{peso(weekSum)}</span>
          <span class="n">{plural(b.week.length, 'person', 'people')}</span>
        </a>
      </div>
      <button class="paybtn" onclick={() => openSheet('find')}><Icon name="wallet" size={22} />Payment received</button>
    </header>

    <div class="col">
      {#if b.late.length}
        <section class="section">
          <div class="section-head">
            <h2>Late <span class="count late">{b.late.length}</span></h2>
            <button class="btn sm accent remind" onclick={() => openSheet('remind', { which: 'late' })}><Icon name="send" size={16} />Remind {b.late.length === 1 ? '' : 'all'}</button>
          </div>
          <PeopleRail lines={b.late} late more="/orders?f=late" max={10} />
        </section>
      {/if}

      <section class="section">
        <div class="section-head"><h2>This week {#if b.week.length}<span class="count">{b.week.length}</span>{/if}</h2>{#if b.week.length}<a class="more" href={link('/orders?f=week')}>See all</a>{/if}</div>
        {#if !app.ready}
          <span class="skel" style="display:block;height:110px;border-radius:18px"></span>
        {:else if b.week.length}
          <PeopleRail lines={b.week} more="/orders?f=week" />
        {:else}
          <div class="calm card"><span class="glyph tint-n"><Icon name="checkCircle" duo size={22} /></span><span>Nobody pays this week</span></div>
        {/if}
      </section>
    </div>
  </div>

  {#if week.length}
    <section class="section">
      <div class="section-head">
        <h2>Videos to film</h2>
        <a class="goal" href={link('/videos')} aria-label="{posted} of {target} posted">
          {#each Array(target) as _, n}<i class:on={n < posted}></i>{/each}
          <span class="num">{posted}/{target}</span>
        </a>
      </div>
      {#if quiet != null && quiet >= 7}<p class="quiet"><Icon name="hourglass" size={15} />Last video {quiet} days ago</p>{/if}
      <div class="rail posters">
        {#each week as idea (idea.key)}<IdeaCard {idea} />{/each}
      </div>
    </section>
  {/if}

  <section class="section">
    <div class="section-head"><h2>To do</h2><button class="icon-btn add" aria-label="New task" onclick={() => openSheet('task')}><Icon name="plus" size={20} /></button></div>
    <div class="list">
      {#each (allTasks ? openTasks : openTasks.slice(0, 5)) as t (t.id)}
        <div class="task" animate:flip={{ duration: 300 }} out:collapse>
          <button class="tick" class:on={ticking.has(t.id)} aria-label="Done: {t.title}" onclick={() => tick(t)}><span class="ring"><Icon name="check" size={15} /></span></button>
          <button class="tt" onclick={() => openSheet('task', { id: t.id })}>
            <span class="clip" class:struck={ticking.has(t.id)}>{t.title}</span>
            {#if t.due || (t.who && t.who !== app.me?.id)}<span class="meta">{#if t.due}<span class:late-t={t.due < today}>{t.due < today ? when(t.due, { late: true }) : when(t.due)}</span>{/if}{#if t.who && t.who !== app.me?.id}{t.due ? ' · ' : ''}{person(t.who)}{/if}</span>{/if}
          </button>
        </div>
      {:else}
        <div class="calm"><span class="glyph tint-n"><Icon name="checkCircle" duo size={22} /></span><span>All done</span></div>
      {/each}
    </div>
    {#if openTasks.length > 5}<button class="btn soft wide more-t" onclick={() => (allTasks = !allTasks)}>{allTasks ? 'Less' : `${openTasks.length - 5} more`}</button>{/if}
  </section>
</div>

<style>
  .home { max-width: 1080px; margin: 0 auto; padding: calc(10px + var(--safe-t)) 16px 8px; }
  .top { display: flex; align-items: center; justify-content: space-between; min-height: 44px; margin: 0 4px 10px; }
  .date { font-weight: 700; font-size: 20px; letter-spacing: -0.015em; }

  .hero {
    position: relative; overflow: hidden; isolation: isolate;
    padding: 22px 20px 20px; border-radius: var(--r-xl); background: var(--hero); color: var(--on-hero);
    box-shadow: 0 18px 40px -22px oklch(0.25 0.06 263 / 0.7), inset 0 0 0 1px var(--hero-line);
  }
  .label { font-size: 15px; font-weight: 550; color: var(--on-hero-2); }
  .total { font-size: 46px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.05; margin-top: 4px; }
  .stack { margin-top: 18px; }
  .split { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 14px; }
  .stat {
    display: flex; flex-direction: column; gap: 2px; padding: 12px 14px; border-radius: 18px; background: var(--hero-2);
    text-decoration: none; transition: transform 140ms var(--ease-out);
  }
  .stat:active { transform: scale(0.97); }
  .k { display: flex; align-items: center; gap: 7px; font-size: 13.5px; font-weight: 600; color: var(--on-hero-2); }
  .dot { width: 8px; height: 8px; border-radius: 99px; }
  .dot.late { background: var(--late); }
  .dot.week { background: var(--hero-week); }
  .v { font-size: 21px; font-weight: 700; letter-spacing: -0.01em; }
  .n { font-size: 13.5px; font-weight: 500; color: var(--on-hero-2); }
  .paybtn {
    width: 100%; margin-top: 12px; min-height: 54px; border-radius: 18px; display: flex; align-items: center; justify-content: center;
    gap: 10px; background: var(--on-hero); color: oklch(0.21 0.025 264); font-size: 16px; font-weight: 650;
    transition: transform 140ms var(--ease-out);
  }
  .paybtn:active { transform: scale(0.97); }
  .skel.dark { background: var(--hero-2); }
  .skel.dark::after { display: none; }

  .count { display: inline-grid; place-items: center; min-width: 24px; height: 22px; padding: 0 7px; margin-left: 6px; border-radius: 99px;
    font-size: 13px; font-weight: 700; background: var(--surface-3); color: var(--ink); vertical-align: 2px; }
  .count.late { background: var(--late-soft); color: var(--late-ink); }
  .calm { display: flex; align-items: center; gap: 12px; padding: 14px 16px; color: var(--ink-2); font-weight: 500; }

  .goal { display: inline-flex; align-items: center; gap: 5px; text-decoration: none; font-size: 14px; font-weight: 700; color: var(--ink-2); }
  .goal i { width: 10px; height: 10px; border-radius: 99px; box-shadow: inset 0 0 0 2px var(--surface-3); }
  .goal i.on { background: var(--accent); box-shadow: none; }
  .goal span { margin-left: 4px; }
  .quiet { display: inline-flex; align-items: center; gap: 6px; margin: -4px 4px 12px; padding: 5px 12px; border-radius: 99px;
    font-size: 13.5px; font-weight: 650; color: var(--late-ink); background: var(--late-soft); }
  .posters { gap: 12px; }

  .task { display: flex; align-items: center; background: var(--surface); }
  .tick { width: 54px; height: 58px; display: grid; place-items: center; flex: none; }
  .ring {
    width: 24px; height: 24px; border-radius: 99px; display: grid; place-items: center; color: transparent;
    box-shadow: inset 0 0 0 2px var(--ink-3); transition: background-color 200ms ease, box-shadow 200ms ease, transform 140ms var(--ease-out);
  }
  .tick:active .ring { transform: scale(0.88); }
  .tick.on .ring { background: var(--paid); box-shadow: none; color: white; }
  .tt { flex: 1; min-width: 0; display: flex; flex-direction: column; text-align: left; padding: 10px 16px 10px 0; font-weight: 500; }
  .struck { color: var(--ink-3); text-decoration: line-through; }
  .meta { font-size: 14px; color: var(--ink-2); font-weight: 400; }
  .add { width: 36px; height: 36px; background: var(--surface); box-shadow: var(--shadow); color: var(--ink); }
  .more-t { margin-top: 10px; }

  @media (min-width: 900px) {
    .home { padding: 28px 40px 0; }
    .grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.1fr); gap: 28px; align-items: start; }
    .grid .col > .section:first-child { margin-top: 0; }
    .hero { padding: 26px 26px 24px; }
    .total { font-size: 52px; }
    .posters { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
  }
</style>
