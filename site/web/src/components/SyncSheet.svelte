<script>
  import Sheet from './Sheet.svelte'
  import Icon from './Icon.svelte'
  import { app, refresh, stop } from '../lib/live.svelte.js'
  import { post } from '../lib/api.js'
  import { ago } from '../lib/format.js'
  import { toast } from '../lib/ui.svelte.js'
  let { top = true } = $props()
  const s = $derived(app.desk?.sheet || {})
  let busy = $state(false)
  async function again() {
    busy = true
    try { await refresh(); toast('Up to date') } catch (e) { toast(e.message, { tone: 'bad' }) } finally { busy = false }
  }
  async function signOut() {
    await post('/api/logout', {})
    stop()
    location.hash = ''
    location.reload()
  }
</script>

<Sheet title="Her sheet" {top}>
  <div class="state">
    {#if !app.online}
      <p class="big">Offline</p>
      <p>Catches up by itself when the connection is back.</p>
    {:else if s.error}
      <p class="big bad">Can't read the sheet</p>
      <p>{s.error}</p>
    {:else if s.can_write}
      <p class="big ok">Live</p>
      <p>Two-way with her sheet. Every change is listed in its “Desk log” tab.</p>
    {:else}
      <p class="big">View only</p>
      <p>Payments can't be saved from here yet.</p>
    {/if}
    {#if s.read_at}<p class="when">Read {ago(s.read_at)}</p>{/if}
  </div>

  {#if app.me?.admin && !s.can_write}
    <div class="setup">
      <h3>To connect it</h3>
      {#if s.robot && s.mode === 'read'}
        <p>She opens the masterlist, <b>File, Save as Google Sheets</b>, shares the new copy with this address as <b>Editor</b>, and sends you its link:</p>
        <p class="mail">{s.robot}</p>
      {:else if s.robot}
        <p>She shares the sheet with this address as <b>Editor</b>:</p>
        <p class="mail">{s.robot}</p>
      {:else}
        <p>The robot key isn't on the server yet.</p>
      {/if}
      {#if s.robot_error && s.mode !== 'read'}<p class="faint">Now: {s.robot_error}</p>{/if}
    </div>
  {/if}

  <div class="btns">
    {#if s.url}<a class="btn line" href={s.url} target="_blank" rel="noopener"><Icon name="sheet" size={18} /> Open her sheet</a>{/if}
    <button class="btn soft" disabled={busy} onclick={again}>Check now</button>
  </div>
  <div class="me">
    <span><Icon name="user" size={18} />{app.me?.name}</span>
    <button class="btn soft sm" onclick={signOut}><Icon name="signOut" size={18} /> Sign out</button>
  </div>
</Sheet>

<style>
  .state p { line-height: 1.5; color: var(--ink-2); }
  .big { font-size: 24px; font-weight: 700; color: var(--ink) !important; margin-bottom: 6px; }
  .ok { color: var(--paid) !important; }
  .bad { color: var(--late-ink) !important; }
  .when { margin-top: 10px; font-size: 14px; }
  .setup { margin-top: 20px; padding: 16px; border-radius: var(--r); background: var(--surface-2); }
  .setup h3 { margin-bottom: 6px; }
  .setup p { font-size: 14px; color: var(--ink-2); margin-top: 4px; }
  .mail { font-weight: 600; color: var(--ink) !important; overflow-wrap: anywhere; user-select: all; }
  .btns { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px; }
  .btns a { text-decoration: none; }
  .me { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 22px; padding-top: 16px; border-top: 1px solid var(--line); }
  .me span { display: inline-flex; align-items: center; gap: 8px; font-weight: 600; }
</style>
