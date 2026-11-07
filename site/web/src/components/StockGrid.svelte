<script>
  // Her "ONHAND items" tab as tiles: a photo (or a drawing of the kind of item until she adds one), the price, how
  // many are left. One button copies the whole list as a post. A tab of Orders.
  import { app } from '../lib/live.svelte.js'
  import { openSheet, copy, toast } from '../lib/ui.svelte.js'
  import { peso } from '../lib/format.js'
  import { itemIcon, itemTint } from '../lib/kinds.js'
  import { photoOf, stockPost } from '../lib/actions.js'
  import Icon from '../components/Icon.svelte'
  import SlotDots from '../components/SlotDots.svelte'

  let q = $state('')
  const sections = $derived.by(() => {
    const s = q.trim().toLowerCase()
    const out = []
    for (const it of app.desk?.stock || []) {
      if (s && !`${it.item} ${it.section} ${it.sub}`.toLowerCase().includes(s)) continue
      let sec = out.find((x) => x.name === it.section)
      if (!sec) out.push((sec = { name: it.section, items: [], out: [] }))
      ;(it.left != null && it.left <= 0 ? sec.out : sec.items).push(it)
    }
    return out
  })
  const forSale = $derived((app.desk?.stock || []).filter((it) => it.left == null || it.left > 0))

  async function share() {
    const ok = await copy(stockPost(app.desk?.stock || []))
    toast(ok ? 'List copied. Paste it in a post, then change any words.' : "Couldn't copy.", { tone: ok ? 'ok' : 'bad' })
  }
</script>

<div class="stock">
  <div class="tools">
    <label class="search">
      <Icon name="search" size={20} />
      <input bind:value={q} placeholder="Search" aria-label="Search items" autocomplete="off" />
      {#if q}<button class="icon-btn" aria-label="Clear" onclick={() => (q = '')}><Icon name="close" size={18} /></button>{/if}
    </label>
    {#if forSale.length}<button class="btn ink share" onclick={share}><Icon name="clipboard" size={18} />Copy list to post</button>{/if}
  </div>

  {#each sections as sec (sec.name)}
    <section class="section">
      <div class="section-head"><h2 class="sec">{sec.name || 'Items'}</h2><span class="count num">{sec.items.length}</span></div>
      <div class="grid">
        {#each sec.items as it (it.k)}
          {@const photo = photoOf(app.photos, it)}
          <button class="tile card" onclick={() => openSheet('slot', { k: it.k })}>
            <span class="pic tint-{itemTint(it.item)}">
              {#if photo}<img src={photo} alt="" loading="lazy" decoding="async" />
              {:else}<Icon name={itemIcon(it.item)} duo size={44} />{/if}
              {#if it.left != null && it.total > 1 && it.left <= 2}<span class="few">{it.left} left</span>{/if}
            </span>
            <span class="txt">
              <span class="name">{it.item}</span>
              {#if it.sub}<span class="sub clip">{it.sub}</span>{/if}
              <span class="bottom">
                {#if it.prices[0]}<b class="price num">{peso(it.prices[0][1])}</b>{/if}
                {#if it.left != null && it.total > 1}
                  <span class="slots"><SlotDots left={it.left} total={it.total} /><span class="left num">{it.left} of {it.total}</span></span>
                {/if}
              </span>
            </span>
          </button>
        {/each}
      </div>
      {#if sec.out.length}
        <p class="sold"><Icon name="archive" size={14} />Sold out: {sec.out.map((x) => x.item).join(' · ')}</p>
      {/if}
    </section>
  {:else}
    <div class="nothing"><span class="glyph tint-n"><Icon name={q ? 'search' : 'stock'} size={24} /></span><p>{app.ready ? (q ? 'No item matches' : 'Nothing in her stock tab yet') : 'Loading…'}</p></div>
  {/each}
</div>

<style>
  .stock { margin-top: 16px; }
  .tools { display: flex; flex-direction: column; gap: 10px; }
  .search { flex: 1; display: flex; align-items: center; gap: 10px; padding: 0 6px 0 16px; min-height: 48px; border-radius: var(--r); background: var(--surface); box-shadow: var(--shadow); color: var(--ink-2); }
  .search input { flex: 1; border: 0; outline: 0; background: none; font-size: 16px; color: var(--ink); min-width: 0; }
  @media (min-width: 700px) { .tools { flex-direction: row; } .share { flex: none; } }
  .sec { font-size: 17px; }
  .count { display: inline-grid; place-items: center; min-width: 26px; height: 24px; padding: 0 8px; border-radius: 99px; font-size: 13px; font-weight: 700; background: var(--surface-3); }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(156px, 1fr)); gap: 10px; }
  .tile { display: flex; flex-direction: column; text-align: left; overflow: hidden; transition: transform 140ms var(--ease-out); }
  .tile:active { transform: scale(0.97); }
  .pic { position: relative; display: grid; place-items: center; aspect-ratio: 4 / 3; overflow: hidden; }
  .pic img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .few { position: absolute; top: 8px; right: 8px; padding: 2px 9px; border-radius: 99px; font-size: 12.5px; font-weight: 700; background: var(--late); color: white; }
  .txt { flex: 1; display: flex; flex-direction: column; gap: 3px; padding: 12px 14px 14px; }
  .name { font-weight: 600; font-size: 15px; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .sub { font-size: 13.5px; color: var(--ink-2); }
  .bottom { margin-top: auto; padding-top: 6px; display: flex; flex-direction: column; gap: 6px; }
  .price { font-size: 18px; font-weight: 700; }
  .slots { display: flex; align-items: center; gap: 8px; }
  .slots :global(.dots), .slots :global(.bar) { flex: 1; }
  .left { flex: none; font-size: 13px; font-weight: 600; color: var(--ink-2); }
  .sold { display: flex; align-items: flex-start; gap: 6px; margin: 10px 4px 0; font-size: 14px; color: var(--ink-3); }
  .sold :global(svg) { margin-top: 2px; }
  .nothing { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 48px 20px; color: var(--ink-2); }
  .nothing .glyph { width: 52px; height: 52px; border-radius: 18px; }
</style>
