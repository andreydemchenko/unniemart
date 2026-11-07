<script>
  // Slots as dots: filled = still available, hollow = taken. Many slots become a thin bar.
  let { left = 0, total = null } = $props()
  const all = $derived(total && total >= left ? total : left)
</script>

{#if all > 0 && all <= 12}
  <span class="dots" aria-hidden="true">
    {#each Array(all) as _, i}<i class:on={i < left}></i>{/each}
  </span>
{:else if all > 12}
  <span class="bar" aria-hidden="true"><span style="width:{(left / all) * 100}%"></span></span>
{/if}

<style>
  .dots { display: flex; flex-wrap: wrap; gap: 4px; }
  i { width: 8px; height: 8px; border-radius: 99px; box-shadow: inset 0 0 0 1.5px var(--line); transition: background-color 300ms ease; }
  i.on { background: var(--ink); box-shadow: none; }
  .bar { display: block; width: 100%; height: 6px; border-radius: 99px; background: var(--track); overflow: hidden; }
  .bar span { display: block; height: 100%; background: var(--ink); border-radius: inherit; transition: width 500ms var(--ease-out); }
</style>
