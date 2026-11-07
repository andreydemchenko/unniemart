<script>
  import { icons, iconsFill, iconsDuo } from '../lib/icons.js'
  // duo: the two-tone version (used inside the soft squares); fill: the solid one (the selected tab)
  let { name, size = 22, fill = false, duo = false, label = null } = $props()
  const svg = $derived((fill && iconsFill[name]) || (duo && iconsDuo[name]) || icons[name] || iconsDuo[name] || '')
</script>

<svg viewBox="0 0 256 256" width={size} height={size} fill="currentColor"
  aria-hidden={label ? undefined : 'true'} role={label ? 'img' : undefined} aria-label={label}>{@html svg}</svg>

<style>
  svg { display: block; flex: none; }
</style>
