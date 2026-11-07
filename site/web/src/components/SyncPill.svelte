<script>
  // Is the page in step with her sheet? Tap for details.
  import { app } from '../lib/live.svelte.js'
  import { openSheet } from '../lib/ui.svelte.js'
  const s = $derived(app.desk?.sheet)
  const state = $derived(!app.online ? 'off' : !s || app.sheetLoading ? 'wait' : s.error ? 'bad' : s.can_write ? 'live' : 'read')
  const text = { off: 'Offline', wait: 'Loading', bad: 'Sheet problem', live: 'Live', read: 'View only' }
</script>

<button class="pill {state}" onclick={() => openSheet('sync')} aria-label="Sync: {text[state]}">
  <span class="dot"></span>{text[state]}
</button>

<style>
  .pill {
    display: inline-flex; align-items: center; gap: 7px; height: 30px; padding: 0 12px; border-radius: 999px;
    background: var(--surface); color: var(--ink-2); font-size: 13px; font-weight: 600; box-shadow: var(--shadow);
  }
  .dot { width: 8px; height: 8px; border-radius: 99px; background: oklch(0.55 0.13 152); }
  .wait .dot { background: var(--ink-3); animation: blink 1.2s ease-in-out infinite; }
  .read .dot { background: var(--ink-3); }
  .bad .dot, .off .dot { background: oklch(0.55 0.19 27); }
  @keyframes blink { 50% { opacity: 0.3; } }
</style>
