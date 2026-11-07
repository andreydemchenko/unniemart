<script>
  import Icon from './Icon.svelte'
  import { route, link } from '../lib/router.svelte.js'
  import { app } from '../lib/live.svelte.js'
  import { openSheet } from '../lib/ui.svelte.js'

  const main = [
    { path: '/', icon: 'home', label: 'Home' },
    { path: '/orders', icon: 'orders', label: 'Orders' },
    { path: '/videos', icon: 'videos', label: 'Videos' },
    { path: '/plan', icon: 'plan', label: 'Plan' },
  ]
  const section = $derived('/' + (route.parts[0] || ''))
  const isOn = (p) => (p === '/' ? section === '/' : section === p || (p === '/orders' && section === '/go'))
  const late = $derived(app.desk?.lines?.filter((l) => l.bucket === 'late').length || 0)
  const badge = (p) => (p === '/orders' ? late : 0)
</script>

<nav class="bar" aria-label="Main">
  {#each main as it (it.path)}
    <a href={link(it.path)} class:on={isOn(it.path)} aria-current={isOn(it.path) ? 'page' : undefined}>
      <span class="ic"><Icon name={it.icon} fill={isOn(it.path)} size={23} />
        {#if badge(it.path)}<span class="badge num">{badge(it.path)}</span>{/if}</span>
      <span class="lb">{it.label}</span>
    </a>
  {/each}
</nav>

<aside class="side" aria-label="Main">
  <a class="brand" href={link('/')}><span class="mark"><svg viewBox="0 0 64 64" width="18" height="18"><path d="M20 18v17a12 12 0 0 0 24 0V18" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round"/></svg></span>Unnie Mart</a>
  {#each main as it (it.path)}
    <a href={link(it.path)} class="item" class:on={isOn(it.path)} aria-current={isOn(it.path) ? 'page' : undefined}>
      <Icon name={it.icon} fill={isOn(it.path)} size={21} /><span>{it.label}</span>
      {#if badge(it.path)}<span class="count num">{badge(it.path)}</span>{/if}
    </a>
  {/each}
  <div class="foot">
    <button class="item" onclick={() => openSheet('sync')}><Icon name="user" size={21} /><span class="clip">{app.me?.name}</span></button>
  </div>
</aside>

<style>
  /* phones: a floating bar at the bottom; computers: a quiet column on the left */
  .bar {
    position: fixed; z-index: 40; left: 12px; right: 12px; bottom: calc(10px + var(--safe-b));
    height: var(--nav-h); padding: 0 6px; border-radius: 24px;
    display: grid; grid-template-columns: repeat(4, 1fr);
    background: var(--surface); box-shadow: var(--shadow-lift);
  }
  .bar a {
    display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px;
    text-decoration: none; color: var(--ink-3); font-size: 11.5px; font-weight: 600; letter-spacing: 0.01em;
    transition: color 160ms ease;
  }
  .bar a.on { color: var(--accent-ink); }
  .ic { position: relative; display: grid; place-items: center; width: 56px; height: 32px; border-radius: 999px; transition: transform 140ms var(--ease-out); }
  .bar a:active .ic { transform: scale(0.92); }
  .ic::before {
    content: ''; position: absolute; inset: 0; border-radius: inherit; background: var(--accent-soft);
    opacity: 0; transform: scaleX(0.6); transition: opacity 180ms ease, transform 260ms var(--ease-out);
  }
  .on .ic::before { opacity: 1; transform: scaleX(1); }
  .ic :global(svg) { position: relative; }
  .badge {
    position: absolute; top: -4px; right: 6px; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 999px;
    background: var(--late); color: white; font-size: 11px; font-weight: 700; display: grid; place-items: center;
    box-shadow: 0 0 0 2px var(--surface);
  }
  .side { display: none; }

  @media (min-width: 900px) {
    .bar { display: none; }
    .side {
      position: fixed; z-index: 40; top: 0; bottom: 0; left: 0; width: 240px; padding: 22px 14px;
      display: flex; flex-direction: column; gap: 4px; background: var(--bg); box-shadow: 1px 0 0 var(--line);
    }
    .brand {
      display: flex; align-items: center; gap: 10px; padding: 4px 10px 24px; font-weight: 700; font-size: 18px;
      text-decoration: none; letter-spacing: -0.015em;
    }
    .mark { width: 34px; height: 34px; border-radius: 11px; display: grid; place-items: center; background: var(--hero); color: var(--on-hero); }
    .item {
      display: flex; align-items: center; gap: 12px; width: 100%; min-height: 44px; padding: 0 12px; border-radius: 14px;
      text-decoration: none; color: var(--ink-2); font-weight: 550; text-align: left;
      transition: background-color 140ms ease, color 140ms ease;
    }
    .item:hover { background: var(--surface-2); color: var(--ink); }
    .item.on { background: var(--surface); color: var(--accent-ink); font-weight: 650; box-shadow: var(--shadow); }
    .count { margin-left: auto; min-width: 22px; height: 20px; padding: 0 6px; border-radius: 99px; display: grid; place-items: center;
      font-size: 12px; font-weight: 700; background: var(--late-soft); color: var(--late-ink); }
    .foot { margin-top: auto; }
  }
</style>
