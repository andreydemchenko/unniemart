<script>
  // A peso amount. When it changes (a payment came in), the digits roll to the new value.
  import { peso } from '../lib/format.js'
  let { value, roll = false } = $props()
  const text = $derived(peso(value))
  // keyed from the right, so ones stay ones when the number gets shorter or longer
  const chars = $derived(text.split('').map((ch, i, a) => ({ ch, key: a.length - i, digit: /\d/.test(ch) })))
</script>

{#if roll}
  <span class="money num"><span class="sr">{text}</span>
    {#each chars as c (c.key + (c.digit ? 'd' : c.ch))}
      {#if c.digit}
        <span class="d" aria-hidden="true"><span class="strip" style="transform: translateY({-Number(c.ch) * 10}%)">
          {#each [0,1,2,3,4,5,6,7,8,9] as n}<span>{n}</span>{/each}</span></span>
      {:else}<span aria-hidden="true">{c.ch}</span>{/if}
    {/each}
  </span>
{:else}
  <span class="num">{text}</span>
{/if}

<style>
  .money { display: inline-flex; align-items: baseline; white-space: nowrap; }
  .d { display: inline-block; height: 1.1em; line-height: 1.1em; overflow: hidden; vertical-align: bottom; }
  .strip { display: flex; flex-direction: column; transition: transform 700ms var(--ease-out); }
  .strip span { height: 1.1em; }
</style>
