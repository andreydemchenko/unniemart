<script>
  import Sheet from './Sheet.svelte'
  import Segmented from './Segmented.svelte'
  import { app } from '../lib/live.svelte.js'
  import { closeSheet, toast } from '../lib/ui.svelte.js'
  import { todayPH, parseDay } from '../lib/format.js'
  import * as act from '../lib/actions.js'
  let { id = null, top = true } = $props()

  // svelte-ignore state_referenced_locally
  const existing = id ? app.tasks.find((t) => t.id === id) : null
  let title = $state(existing?.title || '')
  let note = $state(existing?.note || '')
  let who = $state(existing ? existing.who || '' : app.me?.id)
  let due = $state(existing?.due || '')
  let busy = $state(false)
  let err = $state('')
  let input = $state()
  $effect(() => { if (!existing) setTimeout(() => input?.focus(), 350) })

  const people = $derived([
    ...Object.entries(app.people).map(([v, name]) => ({ value: v, label: v === app.me?.id ? 'Me' : name })),
    { value: '', label: 'Either' },
  ])
  const plus = (n) => { const d = parseDay(todayPH()); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10) }
  const quick = [{ l: 'Today', v: () => todayPH() }, { l: 'Tomorrow', v: () => plus(1) }, { l: 'In a week', v: () => plus(7) }, { l: 'No date', v: () => '' }]

  async function save() {
    if (!title.trim()) { err = 'Write the task first.'; return }
    busy = true
    try {
      await act.taskSave(existing, { title, note, who: who || null, due: due || null })
      if (!existing) toast('Task added')
      closeSheet()
    } catch (e) { err = e.message } finally { busy = false }
  }
</script>

<Sheet title={existing ? 'Task' : 'New task'} {top}>
  <div class="form">
    <textarea class="field title" rows="2" bind:this={input} bind:value={title} placeholder="What needs doing?" maxlength="300"></textarea>
    <div>
      <span class="lbl">Who</span>
      <Segmented options={people} bind:value={who} label="Who" />
    </div>
    <div>
      <span class="lbl">When</span>
      <div class="quick">
        {#each quick as q}<button class="chip" class:sel={due === q.v()} onclick={() => (due = q.v())}>{q.l}</button>{/each}
      </div>
      <input class="field" type="date" bind:value={due} aria-label="Date" />
    </div>
    <textarea class="field" bind:value={note} placeholder="Note (optional)"></textarea>
    {#if err}<p class="err">{err}</p>{/if}
    <button class="btn accent wide" disabled={busy} onclick={save}>{existing ? 'Save' : 'Add task'}</button>
    {#if existing}
      <div class="row">
        <button class="btn soft" onclick={async () => { await act.taskDone(existing, !existing.done_at); closeSheet() }}>{existing.done_at ? 'Not done yet' : 'Mark done'}</button>
        <button class="btn line del" onclick={async () => { await act.taskDelete(existing); closeSheet() }}>Delete</button>
      </div>
      <p class="by">Added by {existing.created_by === app.me?.id ? 'you' : app.people[existing.created_by] || 'someone'}</p>
    {/if}
  </div>
</Sheet>

<style>
  .form { display: flex; flex-direction: column; gap: 16px; padding-top: 4px; }
  .title { font-size: 18px; font-weight: 500; min-height: 72px; }
  .lbl { display: block; font-size: 13px; font-weight: 600; color: var(--ink-2); margin: 0 0 8px 4px; }
  .quick { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
  .quick .chip { height: 36px; padding: 0 14px; font-size: 14px; }
  .quick .chip.sel { background: var(--ink); color: var(--bg); }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .del { color: var(--late-ink); }
  .err { color: var(--late-ink); font-weight: 500; }
  .by { font-size: 13px; color: var(--ink-3); text-align: center; }
</style>
