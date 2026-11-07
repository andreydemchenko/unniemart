<script>
  // One order line: what's left, each payment so far, when it's due. "Payment received" takes a full or part
  // payment: a part payment can move the due date for the rest, and money over the balance can go to the same
  // buyer's other open orders. After saving, a thank-you message with what's left is ready to paste in the DM.
  import Sheet from './Sheet.svelte'
  import Icon from './Icon.svelte'
  import Money from './Money.svelte'
  import Avatar from './Avatar.svelte'
  import { app } from '../lib/live.svelte.js'
  import { get } from '../lib/api.js'
  import { LIVE } from '../lib/derive.js'
  import { peso, handle, when, shortDate, xLink, ago, todayPH } from '../lib/format.js'
  import { closeSheet, toast, copy } from '../lib/ui.svelte.js'
  import * as act from '../lib/actions.js'
  import { rise } from '../lib/motion.js'

  let { k, line: given = null, pay: startPay = false, top = true } = $props()

  const line = $derived(app.desk?.lines?.find((l) => l.k === k) || given)
  // svelte-ignore state_referenced_locally
  let mode = $state(startPay ? 'pay' : 'view')      // view | pay | done
  let amount = $state('')
  let spread = $state(true)                        // extra money goes to their other orders
  let restDue = $state(null)                       // a new due date for what's left; null keeps the one in the sheet
  let busy = $state(false)
  let err = $state('')
  let confirmOver = $state(false)
  let saved = $state(null)                         // what was saved: [{ line, amount, bal }]
  let editing = $state(null)
  let editValue = $state('')
  let history = $state(null)
  let parts = $state(undefined)                    // the separate payments in the Payment cell (undefined: loading)
  const uid = () => (crypto.randomUUID ? crypto.randomUUID() : String(Math.random()).slice(2))
  let base = $state(uid())                         // one id per intended payment (see act.payMany)
  const changed = () => { base = uid(); confirmOver = false; err = '' }

  const today = todayPH()
  const addDays = (n) => new Date(Date.parse(today) + n * 86400000).toISOString().slice(0, 10)

  $effect(() => {
    if (mode === 'pay' && amount === '' && line) amount = String(line.bal > 0 ? line.bal : '')
  })
  $effect(() => {
    if (!line) return
    get(`/api/history?tab=${encodeURIComponent(line.tab)}&user=${encodeURIComponent(line.user)}`)
      .then((r) => (history = r.changes)).catch(() => (history = []))
  })
  $effect(() => {
    if (!line) return
    line.paid                                      // load again after a payment
    const q = new URLSearchParams({ tab: line.tab, r: line.r, user: line.user, item: line.ri || '' })
    get(`/api/payments?${q}`).then((r) => (parts = r.parts)).catch(() => (parts = null))
  })

  const isLate = $derived(line?.bucket === 'late')
  const whole = $derived(line ? line.total || (line.paid || 0) + Math.max(line.bal || 0, 0) : 0)
  const paidPct = $derived(whole ? Math.min(100, Math.max(0, ((line.paid || 0) / whole) * 100)) : 0)
  const sheetUrl = $derived(app.desk?.sheet?.url && line?.gid != null
    ? `${app.desk.sheet.url}#gid=${line.gid}&range=A${line.r}` : app.desk?.sheet?.url)
  const readOnly = $derived(!line?.can?.pay)

  // ---------- the payment ----------
  const amt = $derived(Math.round((Number(String(amount).replace(/[^\d.]/g, '')) || 0) * 100) / 100)
  const same = (a, b) => a.replace(/^@/, '').toLowerCase() === b.replace(/^@/, '').toLowerCase()
  // the buyer's other open orders that can take a payment here, oldest due date first
  const others = $derived(!line ? [] : (app.desk?.lines || [])
    .filter((l) => l.k !== line.k && same(l.user, line.user) && l.bal > 0 && LIVE.includes(l.bucket) && l.can?.pay)
    .sort((a, b) => (a.due || '9999') < (b.due || '9999') ? -1 : 1))
  // how the money is split: this order first, then their other orders; anything still over stays on this order
  const plan = $derived.by(() => {
    if (!line || !amt) return []
    const r2 = (v) => Math.round(v * 100) / 100
    let left = amt
    const first = Math.min(left, Math.max(line.bal || 0, 0))
    const out = [{ line, amount: first }]
    left = r2(left - first)
    if (left > 0 && spread) {
      for (const o of others) {
        const a = Math.min(left, o.bal)
        out.push({ line: o, amount: a })
        left = r2(left - a)
        if (left <= 0) break
      }
    }
    out[0].amount = r2(out[0].amount + left)
    return out.map((p) => ({ ...p, after: r2((p.line.bal || 0) - p.amount) }))
  })
  const after = $derived(plan[0]?.after ?? line?.bal)
  const isPart = $derived(amt > 0 && after > 0.5)
  const isOver = $derived(amt > 0 && after < -0.5)
  const thisPct = $derived(whole && plan[0] ? Math.min(100 - paidPct, (Math.min(plan[0].amount, line.bal) / whole) * 100) : 0)
  const half = $derived(line?.bal >= 200 ? Math.round(line.bal / 2) : null)
  const dueChoices = $derived([addDays(7), addDays(14)].filter((d) => d !== line?.due))

  async function save() {
    err = ''
    if (!amt) { err = 'Enter the amount received.'; return }
    if (isOver && !confirmOver) { confirmOver = true; return }
    busy = true
    try {
      saved = await act.payMany(plan.filter((p) => p.amount > 0), base, { quiet: true })
      if (restDue && saved[0]?.bal > 0.5 && restDue !== line?.due) {
        try { await act.edit(saved[0].line, 'due', restDue, { quiet: true }) } catch (e) { toast(`Saved, but the due date wasn't: ${e.message}`, { tone: 'bad' }) }
      }
      mode = 'done'
    } catch (e) {
      err = e.done?.length ? `${peso(e.done.reduce((a, p) => a + p.amount, 0))} is saved. The rest wasn't: ${e.message} Tap Save to try the rest again.` : e.message
    } finally {
      busy = false
    }
  }

  async function copyThanks() {
    const ok = await copy(act.thanks(saved, restDue))
    toast(ok ? 'Copied. Paste it in the DM.' : "Couldn't copy.", { tone: ok ? 'ok' : 'bad' })
  }

  // ---------- editing a field ----------
  async function saveEdit() {
    busy = true
    err = ''
    try {
      await act.edit(line, editing, editValue)
      editing = null
    } catch (e) {
      err = e.message
    } finally {
      busy = false
    }
  }
  function startEdit(field) {
    editing = field
    editValue = field === 'due' ? (line.due || '') : (line[field] || '')
    err = ''
  }

  const words = { pay: 'Payment', undo: 'Undone', remind: 'Reminder', edit: 'Changed' }
  const fields = [
    { f: 'due', label: 'Due date' }, { f: 'status', label: 'Status' },
    { f: 'courier', label: 'Courier' }, { f: 'note', label: 'Note' },
  ]
  const savedLeft = $derived(saved?.[0]?.bal)
</script>

<Sheet title={mode === 'pay' ? 'Payment received' : ''} {top}>
  {#if mode === 'done' && saved}
    <div class="done" in:rise>
      <span class="seal" class:part={savedLeft > 0.5}><Icon name={savedLeft > 0.5 ? 'hourglass' : 'check'} size={34} /></span>
      <h2>{savedLeft > 0.5 ? `${peso(savedLeft)} left` : 'Paid in full'}</h2>
      <p class="sub">{peso(saved.reduce((a, p) => a + p.amount, 0))} from {handle(saved[0].line.user)}{#if savedLeft > 0.5 && (restDue || saved[0].line.due)}{' · '}rest due {shortDate(restDue || saved[0].line.due)}{/if}</p>
      {#if saved.length > 1}
        <ul class="split">
          {#each saved as p}
            <li><span class="clip">{p.line.item || p.line.go}</span><b class="num">{peso(p.amount)}</b>
              {#if p.bal > 0.5}<span class="left num">{peso(p.bal)} left</span>{:else}<span class="ok"><Icon name="checkCircle" size={18} fill /></span>{/if}</li>
          {/each}
        </ul>
      {/if}
      <button class="btn accent wide" onclick={copyThanks}><Icon name="copy" size={20} /> Copy thank-you message</button>
      <div class="two">
        <button class="btn soft" onclick={() => { act.undo(saved.map((p) => p.change).reverse()); closeSheet() }}><Icon name="undo" size={18} /> Undo</button>
        <button class="btn soft" onclick={closeSheet}>Done</button>
      </div>
    </div>

  {:else if !line}
    <p class="empty">This order isn't open any more.</p>

  {:else if mode === 'pay'}
    <div class="pay" in:rise>
      <p class="for"><Avatar name={line.user} size={28} /><b class="clip">{handle(line.user)}</b><span class="clip">{line.item || line.go}</span></p>
      <label class="big-field">
        <span class="peso">₱</span>
        <input inputmode="decimal" autocomplete="off" bind:value={amount} aria-label="Amount received" oninput={changed} />
      </label>
      <div class="quick">
        {#if line.bal > 0}<button class="chip" class:sel={amt === line.bal} onclick={() => { amount = String(line.bal); changed() }}>All {peso(line.bal)}</button>{/if}
        {#if half}<button class="chip" class:sel={amt === half} onclick={() => { amount = String(half); changed() }}>Half {peso(half)}</button>{/if}
      </div>

      {#if amt > 0}
        <div class="result" class:full={!isPart && !isOver}>
          <div class="bar3" aria-hidden="true">
            <span class="b-paid" style="width:{paidPct}%"></span><span class="b-now" style="width:{thisPct}%"></span>
          </div>
          {#if isPart}
            <p class="r-main"><b class="num">{peso(after)}</b> left after this</p>
          {:else}
            <p class="r-main ok"><Icon name="checkCircle" size={20} fill /> Paid in full</p>
          {/if}
          {#if plan.length > 1}
            <ul class="split">
              {#each plan.slice(1) as p}
                <li><span class="plus num">+{peso(p.amount)}</span><span class="clip">{p.line.item || p.line.go}</span>
                  {#if p.after > 0.5}<span class="left num">{peso(p.after)} left</span>{:else}<span class="ok"><Icon name="checkCircle" size={18} fill /></span>{/if}</li>
              {/each}
            </ul>
          {/if}
          {#if amt > line.bal + 0.5 && others.length}
            <button class="spread" onclick={() => { spread = !spread; changed() }}>
              <span class="box" class:on={spread}><Icon name="check" size={14} /></span>
              Extra goes to their other {others.length === 1 ? 'order' : `${others.length} orders`}
            </button>
          {/if}
          {#if isOver}<p class="warn">{peso(-after)} more than the balance.{#if confirmOver} Tap Save again to keep it.{/if}</p>{/if}
        </div>
      {/if}

      {#if isPart && line.can?.due}
        <div class="rest">
          <span class="rl"><Icon name="clock" size={17} />Rest due</span>
          <div class="chips">
            <button class="chip" class:sel={!restDue} class:late-c={line.due && line.due < today} onclick={() => (restDue = null)}>{line.due ? shortDate(line.due) : 'No date'}</button>
            {#each dueChoices as d}<button class="chip" class:sel={restDue === d} onclick={() => (restDue = d)}>{shortDate(d)}</button>{/each}
            <label class="chip pick" class:sel={restDue && !dueChoices.includes(restDue)}>
              <Icon name="dates" size={16} />{restDue && !dueChoices.includes(restDue) ? shortDate(restDue) : 'Pick'}
              <input type="date" min={today} onchange={(e) => (restDue = e.target.value || null)} />
            </label>
          </div>
        </div>
      {/if}

      {#if err}<p class="error" role="alert">{err}</p>{/if}
      <button class="btn accent wide save" disabled={busy} onclick={save}>
        <span class="lbl" class:hide={busy}>Save {amt ? peso(amt) : ''}</span>
        {#if busy}<span class="over"><span class="spin"></span>Saving</span>{/if}
      </button>
      {#if !startPay}<button class="btn soft wide" onclick={() => { mode = 'view'; err = '' }}>Back</button>{/if}
    </div>

  {:else}
    <div class="top">
      <Avatar name={line.user} size={52} />
      <div class="who">
        <h1 class="clip">{handle(line.user)}</h1>
        <p class="what">{line.item || line.go}{#if line.item && line.item !== line.go}<span class="faint">{' · '}{line.go}</span>{/if}</p>
      </div>
    </div>

    <div class="money-block" class:late={isLate}>
      {#if line.bal > 0}
        <div class="bal"><Money value={line.bal} roll /><span class="of">{whole ? `left of ${peso(whole)}` : 'left'}</span></div>
        {#if whole}<div class="bar" role="img" aria-label="{Math.round(paidPct)}% paid"><span style="width:{paidPct}%"></span></div>{/if}
        {#if parts?.length}
          <div class="parts" aria-label="Payments so far">
            {#each parts as p}<span class="pchip num"><Icon name="check" size={13} />{peso(p)}</span>{/each}
          </div>
        {:else if line.paid > 0}
          <p class="paid-so num">{peso(line.paid)} paid</p>
        {/if}
        <p class="due">
          {#if line.due}
            <Icon name={isLate ? 'alert' : 'clock'} size={16} />
            {shortDate(line.due)} · <b>{when(line.due, { late: true })}</b>
          {:else if line.due_text}
            <Icon name="clock" size={16} /> “{line.due_text}”
          {:else}
            <Icon name="clock" size={16} /> No due date
          {/if}
        </p>
      {:else}
        <div class="bal paid-t"><Icon name="checkCircle" size={28} fill /> Paid in full</div>
      {/if}
    </div>

    {#if line.bal > 0}
      <div class="actions">
        <button class="btn accent wide" disabled={readOnly} onclick={() => { mode = 'pay'; amount = ''; changed() }}>
          <Icon name="wallet" size={20} /> Payment received
        </button>
        <button class="btn soft wide" onclick={() => act.remind(line)}><Icon name="copy" size={20} /> Copy reminder</button>
      </div>
    {/if}

    <div class="links">
      {#if xLink(line.user)}<a class="btn line sm" href={xLink(line.user)} target="_blank" rel="noopener"><Icon name="x" size={16} /> X</a>{/if}
      {#if sheetUrl}<a class="btn line sm" href={sheetUrl} target="_blank" rel="noopener"><Icon name="sheet" size={16} /> Sheet</a>{/if}
    </div>

    <dl class="facts">
      {#if line.qty > 1}<div><dt>Quantity</dt><dd>{line.qty}</dd></div>{/if}
      {#each fields as fd}
        {#if editing === fd.f}
          <div class="editing">
            <dt>{fd.label}</dt>
            <dd>
              {#if fd.f === 'due'}
                <input class="field" type="date" bind:value={editValue} />
              {:else}
                <input class="field" bind:value={editValue} maxlength="200" />
              {/if}
              <span class="row-btns">
                <button class="btn soft sm" onclick={() => (editing = null)}>Cancel</button>
                <button class="btn ink sm" disabled={busy} onclick={saveEdit}>Save</button>
              </span>
            </dd>
          </div>
        {:else if (fd.f === 'due' ? line.due || line.due_text : line[fd.f]) || line.can?.[fd.f]}
          <div>
            <dt>{fd.label}</dt>
            <dd>
              <span>{fd.f === 'due' ? (line.due ? shortDate(line.due) : line.due_text || '–') : line[fd.f] || '–'}</span>
              {#if line.can?.[fd.f]}<button class="icon-btn sm" aria-label="Change {fd.label}" onclick={() => startEdit(fd.f)}><Icon name="edit" size={18} /></button>{/if}
            </dd>
          </div>
        {/if}
      {/each}
    </dl>
    {#if err}<p class="error" role="alert">{err}</p>{/if}

    {#if history?.length}
      <ul class="hist">
        {#each history.slice(0, 5) as h (h.id)}
          <li>
            <span class="dot" class:pay={h.kind === 'pay'}></span>
            <span class="clip">
              {words[h.kind] || h.kind}{#if h.kind === 'pay'}{' ' + peso(h.extra?.amount)}{/if}{#if h.kind === 'edit'}{' ' + (h.extra?.field || '')}{/if}{#if h.undone_at}{' '}<span class="faint">(undone)</span>{/if}
              <span class="faint">{' · '}{app.people[h.who] || h.who}</span>
            </span>
            <span class="faint when">{ago(h.at)}</span>
          </li>
        {/each}
      </ul>
    {/if}
  {/if}
</Sheet>

<style>
  .top { display: flex; align-items: center; gap: 14px; padding-top: 4px; }
  .who { min-width: 0; flex: 1; }
  .who h1 { font-size: 26px; }
  .what { color: var(--ink-2); margin-top: 4px; font-size: 14.5px; }

  .money-block { margin: 20px 0 18px; padding: 18px; border-radius: var(--r-lg); background: var(--accent-soft); }
  .money-block.late { background: var(--late-soft); }
  .bal { display: flex; align-items: baseline; gap: 10px; font-size: 34px; font-weight: 700; letter-spacing: -0.01em; }
  .bal :global(svg) { align-self: center; }
  .of { font-size: 15px; font-weight: 500; color: var(--ink-2); letter-spacing: 0; }
  .bar { height: 8px; border-radius: 999px; background: var(--track); margin: 14px 0 10px; overflow: hidden; }
  .bar span { display: block; height: 100%; border-radius: inherit; background: var(--ink); transition: width 700ms var(--ease-out); }
  .late .bar span { background: var(--late); }
  .parts { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
  .pchip { display: inline-flex; align-items: center; gap: 4px; height: 26px; padding: 0 9px; border-radius: 99px;
    background: var(--surface); font-size: 13.5px; font-weight: 600; }
  .pchip :global(svg) { color: var(--paid); }
  .paid-so { font-size: 14px; font-weight: 600; color: var(--ink-2); margin-bottom: 10px; }
  .due { display: flex; align-items: center; gap: 6px; font-size: 14.5px; color: var(--ink-2); }
  .late .due { color: var(--late-ink); }

  .actions { display: grid; gap: 10px; }
  .links { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 4px; }
  .links a { text-decoration: none; }

  .facts { margin: 14px 0 0; }
  .facts > div { display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 48px; border-top: 1px solid var(--line); }
  .facts dt { color: var(--ink-2); font-size: 14px; flex: none; }
  .facts dd { margin: 0; display: flex; align-items: center; gap: 4px; text-align: right; min-width: 0; font-weight: 500; }
  .facts .editing { flex-direction: column; align-items: stretch; padding: 10px 0 12px; gap: 8px; }
  .facts .editing dd { flex-direction: column; align-items: stretch; gap: 8px; }
  .row-btns { display: flex; gap: 8px; justify-content: flex-end; }
  .icon-btn.sm { width: 34px; height: 34px; }

  .hist { list-style: none; margin: 18px 0 0; padding: 12px 0 0; border-top: 1px solid var(--line); }
  .hist li { display: flex; align-items: center; gap: 10px; min-height: 36px; font-size: 14px; }
  .dot { width: 8px; height: 8px; border-radius: 99px; background: var(--surface-3); flex: none; }
  .dot.pay { background: var(--paid); }
  .when { margin-left: auto; flex: none; font-size: 13px; }

  .pay { display: flex; flex-direction: column; gap: 14px; padding-top: 4px; }
  .for { display: flex; align-items: center; gap: 8px; color: var(--ink-2); min-width: 0; }
  .for b { color: var(--ink); flex: none; max-width: 50%; }
  .big-field {
    display: flex; align-items: baseline; gap: 4px; padding: 14px 18px; border-radius: var(--r-lg);
    background: var(--surface-2); border: 2px solid transparent; transition: border-color 160ms ease;
  }
  .big-field:focus-within { border-color: var(--ink); background: var(--surface); }
  .peso { font-size: 34px; font-weight: 700; color: var(--ink-3); }
  .big-field input {
    flex: 1; min-width: 0; border: 0; outline: 0; background: none; font-size: 40px; font-weight: 700;
    font-variant-numeric: tabular-nums; letter-spacing: -0.01em; padding: 0;
  }
  .quick, .chips { display: flex; flex-wrap: wrap; gap: 8px; }
  .chip { height: 36px; padding: 0 14px; font-size: 14px; transition: background-color 140ms ease, color 140ms ease; }
  .chip.sel { background: var(--ink); color: var(--bg); }
  .chip.late-c:not(.sel) { color: var(--late-ink); }

  .result { padding: 14px 16px; border-radius: var(--r-lg); background: var(--surface-2); display: flex; flex-direction: column; gap: 10px; }
  .result.full { background: var(--paid-soft); }
  .bar3 { display: flex; height: 10px; border-radius: 99px; background: var(--track); overflow: hidden; }
  .bar3 span { height: 100%; transition: width 300ms var(--ease-out); }
  .b-paid { background: var(--ink); }
  .b-now { background: var(--accent-press); }
  .full .b-now { background: var(--paid); }
  .r-main { font-size: 16px; color: var(--ink-2); display: flex; align-items: center; gap: 6px; }
  .r-main b { font-size: 20px; color: var(--ink); }
  .r-main.ok { color: var(--paid); font-weight: 650; }
  .split { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
  .split li { display: flex; align-items: center; gap: 10px; font-size: 14.5px; min-height: 30px; }
  .split .clip { flex: 1; min-width: 0; }
  .plus { font-weight: 700; flex: none; }
  .left { flex: none; font-size: 13.5px; color: var(--ink-2); font-weight: 600; }
  .ok { color: var(--paid); flex: none; display: inline-flex; }
  .spread { display: flex; align-items: center; gap: 10px; text-align: left; font-size: 14.5px; font-weight: 500; min-height: 36px; }
  .box { width: 22px; height: 22px; border-radius: 7px; display: grid; place-items: center; flex: none; color: transparent;
    box-shadow: inset 0 0 0 2px var(--ink-3); transition: background-color 160ms ease; }
  .box.on { background: var(--ink); color: var(--bg); box-shadow: none; }

  .rest { display: flex; flex-direction: column; gap: 8px; }
  .rl { display: flex; align-items: center; gap: 6px; font-size: 14px; font-weight: 600; color: var(--ink-2); }
  .pick { position: relative; display: inline-flex; align-items: center; gap: 6px; cursor: pointer; }
  .pick input { position: absolute; inset: 0; opacity: 0; width: 100%; cursor: pointer; }

  .warn { color: var(--late-ink); font-size: 14px; font-weight: 500; }
  .error { color: var(--late-ink); font-size: 14px; font-weight: 500; margin-top: 10px; }

  .save { position: relative; overflow: hidden; margin-top: 4px; min-height: 54px; font-size: 16px; }
  .save .lbl { transition: opacity 160ms ease, filter 160ms ease; }
  .save .lbl.hide { opacity: 0; filter: blur(3px); }
  .over { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 8px;
    animation: pop 220ms var(--ease-out); }
  @keyframes pop { from { opacity: 0; transform: scale(0.94); filter: blur(2px); } }
  .spin { width: 18px; height: 18px; border-radius: 99px; border: 2.5px solid currentColor; border-right-color: transparent;
    animation: spin 700ms linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .done { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 8px 0 4px; text-align: center; }
  .seal { width: 72px; height: 72px; border-radius: 99px; display: grid; place-items: center; background: var(--paid); color: white;
    animation: seal 420ms var(--ease-out); }
  .seal.part { background: var(--accent); color: var(--on-accent); }
  @keyframes seal { from { transform: scale(0.6); opacity: 0; } }
  .done h2 { font-size: 28px; margin-top: 6px; }
  .done .sub { color: var(--ink-2); margin-bottom: 8px; }
  .done .split { width: 100%; text-align: left; padding: 12px 14px; border-radius: var(--r); background: var(--surface-2); margin-bottom: 6px; }
  .done .btn { width: 100%; }
  .two { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; width: 100%; }
</style>
