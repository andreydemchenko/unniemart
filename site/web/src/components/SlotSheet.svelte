<script>
  // A stock item: its photo, prices and slots. "Slot taken" writes to her ONHAND tab; her formula does the rest.
  // The photo is the site's own (her sheet has no place for pictures).
  import Sheet from './Sheet.svelte'
  import Icon from './Icon.svelte'
  import { app } from '../lib/live.svelte.js'
  import { peso } from '../lib/format.js'
  import { closeSheet, toast } from '../lib/ui.svelte.js'
  import * as act from '../lib/actions.js'
  import { itemIcon, itemTint } from '../lib/kinds.js'
  let { k, top = true } = $props()
  const it = $derived(app.desk?.stock?.find((s) => s.k === k))
  let taker = $state('')
  let busy = $state(false)
  let picking = $state(false)
  let fileInput = $state()
  const photo = $derived(it ? act.photoOf(app.photos, it) : null)

  async function addPhoto(e) {
    const f = e.currentTarget.files?.[0]
    e.currentTarget.value = ''
    if (!f) return
    picking = true
    try { await act.photoAdd(it, f) } catch (err) { toast(err.message, { tone: 'bad' }) } finally { picking = false }
  }
  async function removePhoto() {
    try { await act.photoRemove(it) } catch (err) { toast(err.message, { tone: 'bad' }) }
  }

  async function change(delta) {
    busy = true
    try {
      await act.slot(it, delta, delta > 0 ? taker : '')
      taker = ''
      if (delta > 0) closeSheet()
    } catch (e) {
      toast(e.message, { tone: 'bad' })
    } finally {
      busy = false
    }
  }
</script>

<Sheet {top}>
  {#if !it}
    <p class="empty">This item moved in the sheet. Pull down to refresh.</p>
  {:else}
    <div class="photo tint-{itemTint(it.item)}" class:has={photo}>
      {#if photo}
        <img src={photo} alt={it.item} />
      {:else}
        <Icon name={itemIcon(it.item)} duo size={64} />
      {/if}
      <input bind:this={fileInput} type="file" accept="image/*" onchange={addPhoto} hidden />
      <div class="ph-acts">
        <button class="btn sm" class:soft={!photo} class:glass={photo} disabled={picking} onclick={() => fileInput.click()}>
          <Icon name="cameraPlus" size={17} />{picking ? 'Adding…' : photo ? 'Change photo' : 'Add a photo'}
        </button>
        {#if photo}<button class="btn sm glass" onclick={removePhoto} aria-label="Remove photo"><Icon name="trash" size={17} /></button>{/if}
      </div>
    </div>
    <div class="head">
      <p class="sec">{it.section}{#if it.sub}{' · '}{it.sub}{/if}</p><h1>{it.item}</h1>
    </div>
    {#if it.left != null}
      <div class="slots" class:out={it.left <= 0}>
        <span class="big num">{Math.max(0, it.left)}</span>
        <span>{it.left <= 0 ? 'sold out' : it.left === 1 ? 'slot left' : 'slots left'}{it.total ? ` of ${it.total}` : ''}</span>
      </div>
      {#if it.total}
        <div class="dots" aria-hidden="true">
          {#each Array(Math.min(it.total, 30)) as _, i}<span class:taken={i >= Math.max(0, it.left)}></span>{/each}
        </div>
      {/if}
    {/if}
    {#if it.prices.length}
      <ul class="prices">
        {#each it.prices as [label, a]}<li><span>{label}</span><b class="num">{peso(a)}</b></li>{/each}
        {#if it.dp}<li><span>Down payment</span><b class="num">{peso(it.dp)}</b></li>{/if}
      </ul>
      {#if it.carried}<p class="hint">Same prices as the item above it in her sheet.</p>{/if}
    {/if}
    {#if it.can}
      {#if it.left == null || it.left > 0}
        <label class="lbl" for="taker">Who took it? (optional)</label>
        <input id="taker" class="field" bind:value={taker} placeholder="@username" autocapitalize="off" autocomplete="off" />
        <button class="btn accent wide go" disabled={busy} onclick={() => change(1)}><Icon name="plus" size={20} /> 1 slot taken</button>
      {/if}
      {#if it.taken > 0}<button class="btn soft wide" disabled={busy} onclick={() => change(-1)}><Icon name="minus" size={20} /> Free a slot</button>{/if}
    {:else}
      <p class="hint">{app.desk?.sheet?.mode === 'read' ? 'Slots can be changed here once her sheet is a Google Sheet.' : 'Slots can be changed here once her sheet is shared with the site.'}</p>
    {/if}
  {/if}
</Sheet>

<style>
  .photo { position: relative; display: grid; place-items: center; aspect-ratio: 4 / 3; margin: 0 0 16px; border-radius: var(--r-lg); overflow: hidden; }
  .photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .ph-acts { position: absolute; left: 12px; bottom: 12px; display: flex; gap: 8px; }
  .glass { background: oklch(0.2 0.01 80 / 0.55); color: white; }
  .head { display: flex; flex-direction: column; }
  .sec { color: var(--ink-2); font-size: 14px; }
  h1 { font-size: 24px; margin-top: 2px; line-height: 1.2; }
  .slots { display: flex; align-items: baseline; gap: 8px; margin-top: 18px; color: var(--ink-2); }
  .big { font-size: 40px; font-weight: 700; color: var(--ink); }
  .slots.out .big { color: var(--late-ink); }
  .dots { display: flex; flex-wrap: wrap; gap: 5px; margin: 10px 0 4px; }
  .dots span { width: 14px; height: 14px; border-radius: 99px; background: var(--ink); transition: background-color 300ms ease; }
  .dots span.taken { background: none; box-shadow: inset 0 0 0 2px var(--line); }
  .prices { list-style: none; margin: 18px 0 0; padding: 0; }
  .prices li { display: flex; justify-content: space-between; min-height: 44px; align-items: center; border-top: 1px solid var(--line); }
  .prices span { color: var(--ink-2); }
  .hint { font-size: 13.5px; color: var(--ink-3); margin-top: 10px; }
  .lbl { margin-top: 22px; }
  .go { margin: 12px 0 10px; }
</style>
