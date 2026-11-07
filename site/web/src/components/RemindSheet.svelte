<script>
  // Remind everyone who is late, one after another: the kind message is ready, copy it, open their chat, next.
  // Copying notes the reminder (the bell on the order, and her sheet's Desk log).
  import { untrack } from 'svelte'
  import Sheet from './Sheet.svelte'
  import Icon from './Icon.svelte'
  import Avatar from './Avatar.svelte'
  import { app } from '../lib/live.svelte.js'
  import { byBucket } from '../lib/derive.js'
  import { peso, handle, when, ago, xLink } from '../lib/format.js'
  import { closeSheet } from '../lib/ui.svelte.js'
  import * as act from '../lib/actions.js'
  let { which = 'late', top = true } = $props()

  // the list as it was when she opened this (reminding someone doesn't reorder it under her finger), most late first
  const list = untrack(() => (byBucket(app.desk)[which] || []).filter((l) => l.msg)
    .sort((a, b) => ((a.due || '') < (b.due || '') ? -1 : 1)))
  let i = $state(0)
  let sent = $state(0)
  let copied = $state(false)
  const l = $derived(list[i] && (app.desk?.lines?.find((x) => x.k === list[i].k) || list[i]))
  const recent = $derived(l?.reminded && Date.now() - new Date(l.reminded).getTime() < 3 * 86400000)
  const x = $derived(l ? xLink(l.user) : null)

  async function cp() {
    await act.remind(l)
    if (!copied) sent++
    copied = true
  }
  function next() {
    copied = false
    i++
  }
</script>

<Sheet {top} title={i < list.length ? `Remind ${list.length === 1 ? '1 person' : list.length + ' people'}` : ''}>
  {#if !list.length}
    <p class="empty">Nobody to remind.</p>
  {:else if i >= list.length}
    <div class="end">
      <span class="seal"><Icon name="check" size={34} /></span>
      <h2>All done</h2>
      <p class="muted">{sent === 0 ? 'No messages copied.' : sent === 1 ? 'You reminded 1 person.' : `You reminded ${sent} people.`}</p>
      <button class="btn ink wide" onclick={closeSheet}>Close</button>
    </div>
  {:else}
    <div class="steps" aria-label="{i + 1} of {list.length}">
      {#each list as _, n}<span class:on={n <= i}></span>{/each}
    </div>

    <div class="who">
      <Avatar name={l.user} size={56} />
      <div class="who-t">
        <b class="clip">{handle(l.user)}</b>
        <span class="clip muted">{l.item || l.go}</span>
      </div>
      <div class="amt">
        <b class="num late-t">{peso(l.bal)}</b>
        {#if l.due}<span class="late-t">{when(l.due, { late: true })}</span>{/if}
      </div>
    </div>
    {#if recent}<p class="chip accent again"><Icon name="bell" size={14} />Reminded {ago(l.reminded)}</p>{/if}

    <p class="msg">{l.msg}</p>

    <div class="acts">
      <button class="btn wide" class:accent={!copied} class:soft={copied} onclick={cp}>
        <Icon name={copied ? 'check' : 'copy'} size={18} />{copied ? 'Copied' : 'Copy message'}
      </button>
      {#if x}<a class="btn wide" class:soft={!copied} class:ink={copied} href={x} target="_blank" rel="noopener"><Icon name="x" size={18} />Open their X</a>{/if}
      <button class="btn line wide" onclick={next}>{i === list.length - 1 ? 'Finish' : copied ? 'Next person' : 'Skip'}<Icon name="arrowRight" size={18} /></button>
    </div>
    <p class="num count">{i + 1} of {list.length}</p>
  {/if}
</Sheet>

<style>
  .steps { display: flex; gap: 4px; margin: 2px 0 18px; }
  .steps span { flex: 1; height: 4px; border-radius: 99px; background: var(--surface-3); transition: background-color 240ms ease; }
  .steps span.on { background: var(--ink); }
  .who { display: flex; align-items: center; gap: 14px; }
  .who-t { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .who-t b { font-size: 18px; }
  .amt { display: flex; flex-direction: column; align-items: flex-end; flex: none; font-size: 14px; font-weight: 600; }
  .amt b { font-size: 22px; font-weight: 700; }
  .again { margin-top: 14px; height: 30px; }
  .msg { margin-top: 16px; padding: 16px 18px; border-radius: 20px 20px 20px 6px; background: var(--surface-2); line-height: 1.5; white-space: pre-wrap; }
  .acts { display: flex; flex-direction: column; gap: 8px; margin-top: 18px; }
  .count { text-align: center; margin-top: 12px; font-size: 14px; color: var(--ink-3); }
  .end { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 18px 0 4px; text-align: center; }
  .seal { width: 72px; height: 72px; border-radius: 99px; display: grid; place-items: center; background: var(--paid); color: white; margin-bottom: 6px;
    animation: pop 320ms var(--ease-out); }
  @keyframes pop { from { transform: scale(0.8); opacity: 0; } }
  .end .btn { margin-top: 16px; }
</style>
