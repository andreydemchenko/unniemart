<script>
  import { post } from '../lib/api.js'
  import { app, start } from '../lib/live.svelte.js'
  let pw = $state('')
  let busy = $state(false)
  let err = $state('')
  let shake = $state(false)

  async function submit(e) {
    e.preventDefault()
    if (!pw.trim()) return
    busy = true
    err = ''
    try {
      const r = await post('/api/login', { password: pw })
      app.me = r.me
      app.signedIn = true
      start()
    } catch (x) {
      err = x.message
      shake = true
      setTimeout(() => (shake = false), 400)
    } finally {
      busy = false
    }
  }
</script>

<main class="login">
  <div class="card" class:shake>
    <div class="mark"><svg viewBox="0 0 64 64" width="30" height="30"><path d="M20 18v17a12 12 0 0 0 24 0V18" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></svg></div>
    <h1>Unnie Mart</h1>
    <form onsubmit={submit}>
      <label class="sr" for="pw">Password</label>
      <input id="pw" class="field" type="password" autocomplete="current-password" placeholder="Password"
        bind:value={pw} autocapitalize="off" spellcheck="false" />
      {#if err}<p class="err" role="alert">{err}</p>{/if}
      <button class="btn ink wide" disabled={busy}>{busy ? 'Opening…' : 'Open'}</button>
    </form>
    <p class="small">Stays signed in on this device.</p>
  </div>
</main>

<style>
  .login {
    min-height: 100dvh; display: grid; place-items: center; padding: 24px;
    background: var(--hero); color: var(--on-hero);
  }
  .card { width: 100%; max-width: 340px; display: flex; flex-direction: column; align-items: center; gap: 18px; }
  .mark { width: 64px; height: 64px; border-radius: 20px; display: grid; place-items: center; background: var(--on-hero); color: var(--hero); }
  h1 { font-size: 30px; letter-spacing: -0.02em; }
  form { width: 100%; display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
  .field { background: var(--surface); color: var(--ink); text-align: center; font-size: 17px; letter-spacing: 0.04em; }
  .field:focus { border-color: var(--accent); }
  .btn.ink { background: var(--accent); color: var(--on-accent); min-height: 52px; font-size: 16px; }
  .err { text-align: center; font-weight: 600; color: oklch(0.78 0.13 25); }
  .small { font-size: 13.5px; color: var(--on-hero-2); }
  .shake { animation: shake 360ms var(--ease-out); }
  @keyframes shake { 20% { transform: translateX(-8px); } 45% { transform: translateX(6px); } 70% { transform: translateX(-3px); } }
</style>
