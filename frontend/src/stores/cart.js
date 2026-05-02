import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { useToastStore } from './toast'

function loadCart() {
  try {
    const raw = localStorage.getItem('xcm_cart_v1')
    if (!raw) return { items: {} }
    const parsed = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object') return { items: {} }
    if (!parsed.items || typeof parsed.items !== 'object') return { items: {} }
    return parsed
  } catch {
    return { items: {} }
  }
}

function saveCartLocal(state) {
  try {
    localStorage.setItem('xcm_cart_v1', JSON.stringify({ items: state.items }))
  } catch {
    // ignore
  }
}

// 防抖 — 避免每次加減數量都打 API
let _syncTimer = null
function scheduleSync(items) {
  if (_syncTimer) clearTimeout(_syncTimer)
  _syncTimer = setTimeout(() => syncToServer(items), 800)
}

async function syncToServer(items) {
  const auth = useAuthStore()
  if (!auth.isLoggedIn) return
  try {
    await fetch('/api/auth/cart', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth.token}`,
      },
      body: JSON.stringify({ items }),
    })
  } catch {
    // 靜默失敗
  }
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: loadCart().items, // { [productId]: { product, quantity } }
  }),
  getters: {
    itemList(state) {
      return Object.values(state.items)
    },
    totalCount(state) {
      return Object.values(state.items).reduce((acc, it) => acc + it.quantity, 0)
    },
    totalPrice(state) {
      return Object.values(state.items).reduce((acc, it) => {
        const price = Number(it.product?.price || 0)
        return acc + price * it.quantity
      }, 0)
    },
    badgeText() {
      const n = this.totalCount
      if (n > 99) return '99+'
      return String(n)
    },
  },
  actions: {
    add(product, quantity = 1) {
      const auth = useAuthStore()
      if (!auth.isLoggedIn) {
        const toast = useToastStore()
        toast.push('請先登入才能加入購物車', { tone: 'neutral' })
        // 延遲跳轉讓 toast 先顯示
        setTimeout(() => {
          import('vue-router').then(({ useRouter }) => {
            const router = useRouter()
            router.push('/login')
          })
        }, 600)
        return
      }

      const toast = useToastStore()
      const id = String(product.id)
      const existing = this.items[id]
      if (existing) {
        existing.quantity += quantity
        toast.push(`已更新 ${product.name} 數量`)
      } else {
        this.items[id] = { product, quantity }
        toast.push(`已加入 ${product.name} 到購物車`)
      }
      saveCartLocal(this)
      scheduleSync(this.items)
    },
    setQuantity(productId, quantity) {
      const id = String(productId)
      const q = Math.max(1, Number(quantity || 1))
      if (!this.items[id]) return
      this.items[id].quantity = q
      saveCartLocal(this)
      scheduleSync(this.items)
    },
    inc(productId) {
      const id = String(productId)
      if (!this.items[id]) return
      this.items[id].quantity += 1
      saveCartLocal(this)
      scheduleSync(this.items)
    },
    dec(productId) {
      const id = String(productId)
      if (!this.items[id]) return
      this.items[id].quantity = Math.max(1, this.items[id].quantity - 1)
      saveCartLocal(this)
      scheduleSync(this.items)
    },
    remove(productId) {
      const toast = useToastStore()
      const id = String(productId)
      if (!this.items[id]) return
      delete this.items[id]
      toast.push('商品已移除', { tone: 'neutral' })
      saveCartLocal(this)
      scheduleSync(this.items)
    },
    clear() {
      this.items = {}
      saveCartLocal(this)
      scheduleSync(this.items)
    },

    // 登入後從伺服器載入購物車
    async loadFromServer() {
      const auth = useAuthStore()
      if (!auth.isLoggedIn) return
      try {
        const res = await fetch('/api/auth/cart', {
          headers: { Authorization: `Bearer ${auth.token}` },
        })
        if (!res.ok) return
        const data = await res.json()
        const serverItems = data.items || {}

        // 只有本地空的才用伺服器的
        if (Object.keys(this.items).length === 0 && Object.keys(serverItems).length > 0) {
          this.items = serverItems
          saveCartLocal(this)
        }
      } catch {
        // 靜默失敗
      }
    },
  },
})
