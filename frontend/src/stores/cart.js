import { defineStore } from 'pinia'
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

function saveCart(state) {
  try {
    localStorage.setItem('xcm_cart_v1', JSON.stringify({ items: state.items }))
  } catch {
    // ignore
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
      saveCart(this)
    },
    setQuantity(productId, quantity) {
      const id = String(productId)
      const q = Math.max(1, Number(quantity || 1))
      if (!this.items[id]) return
      this.items[id].quantity = q
      saveCart(this)
    },
    inc(productId) {
      const id = String(productId)
      if (!this.items[id]) return
      this.items[id].quantity += 1
      saveCart(this)
    },
    dec(productId) {
      const id = String(productId)
      if (!this.items[id]) return
      this.items[id].quantity = Math.max(1, this.items[id].quantity - 1)
      saveCart(this)
    },
    remove(productId) {
      const toast = useToastStore()
      const id = String(productId)
      if (!this.items[id]) return
      delete this.items[id]
      toast.push('商品已移除', { tone: 'neutral' })
      saveCart(this)
    },
    clear() {
      this.items = {}
      saveCart(this)
    },
  },
})

