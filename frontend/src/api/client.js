const DEFAULT_BASE = 'http://localhost:8000'

export function getApiBaseUrl() {
  return (import.meta?.env?.VITE_API_BASE_URL || DEFAULT_BASE).replace(/\/$/, '')
}

export async function apiGet(path, params = {}) {
  const base = getApiBaseUrl()
  const url = new URL(base + path)
  Object.entries(params).forEach(([k, v]) => {
    if (v === undefined || v === null || v === '') return
    url.searchParams.set(k, String(v))
  })

  const res = await fetch(url.toString(), {
    method: 'GET',
    headers: { Accept: 'application/json' },
  })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`API ${res.status}: ${text || res.statusText}`)
  }

  return await res.json()
}

