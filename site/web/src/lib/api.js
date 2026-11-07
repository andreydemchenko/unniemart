// Talking to the server. Every change carries X-UM: 1 (the server refuses changes without it).

export class ApiError extends Error {
  constructor(message, status) { super(message); this.status = status }
}

let onSignedOut = () => {}
export function whenSignedOut(fn) { onSignedOut = fn }

async function call(method, url, { json, raw, headers = {}, signal } = {}) {
  let res
  try {
    res = await fetch(url, {
      method, signal, credentials: 'same-origin',
      headers: { ...(json !== undefined ? { 'Content-Type': 'application/json' } : {}),
                 ...(method !== 'GET' ? { 'X-UM': '1' } : {}), ...headers },
      body: json !== undefined ? JSON.stringify(json) : raw,
    })
  } catch (e) {
    if (e.name === 'AbortError') throw e
    throw new ApiError("Can't reach the site. Check the internet connection.", 0)
  }
  let data = null
  try { data = await res.json() } catch { /* not JSON */ }
  if (res.status === 401 && !url.endsWith('/login')) onSignedOut()
  if (!res.ok) throw new ApiError(data?.error || `Something went wrong (${res.status}).`, res.status)
  return data
}

export const get = (url, opts) => call('GET', url, opts)
export const post = (url, json, opts) => call('POST', url, { ...opts, json })
export const upload = (url, blob) => call('POST', url, { raw: blob, headers: { 'Content-Type': blob.type || 'image/jpeg' } })
