// Pages live in the address after # (so the phone's back button works and links can be shared between the two of you).
export const route = $state({ path: '/', parts: [], query: {} })

function parse() {
  const h = decodeURI(location.hash.slice(1)) || '/'
  const [p, q] = h.split('?')
  route.path = p || '/'
  route.parts = (p || '/').split('/').filter(Boolean)
  route.query = Object.fromEntries(new URLSearchParams(q || ''))
}
parse()
window.addEventListener('hashchange', parse)

export function go(path, { replace = false } = {}) {
  const target = '#' + encodeURI(path)
  if (replace) history.replaceState(history.state, '', target)
  else location.hash = encodeURI(path)
  if (replace) parse()
}

export const link = (path) => '#' + encodeURI(path)
