// 留空 = 同源請求 (開發時靠 Vite proxy 轉到後端)
// 可透過環境變數 VITE_API_BASE_URL 覆蓋
const DEFAULT_BASE = ''

export function getApiBaseUrl() {
  return (import.meta?.env?.VITE_API_BASE_URL || DEFAULT_BASE).replace(/\/$/, '')
}

export async function apiGet(path, params = {}) {
  const base = getApiBaseUrl()
  // 如果 base 是相對路徑（空字串），補上當前網域當基底
  const resolved = base
    ? new URL(base + path).toString()
    : new URL(path, window.location.origin).toString()
  const url = new URL(resolved)
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

export async function apiPost(path, body) {
  const base = getApiBaseUrl()
  const resolved = base
    ? new URL(base + path).toString()
    : new URL(path, window.location.origin).toString()

  const res = await fetch(resolved, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`API ${res.status}: ${text || res.statusText}`)
  }

  return await res.json()
}

