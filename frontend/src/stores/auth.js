import { defineStore } from 'pinia'
import { apiPost, apiGet } from '../api/client'
import { useCartStore } from './cart'

function loadAuth() {
  try {
    const raw = localStorage.getItem('xcm_auth_v1')
    if (!raw) return null
    return JSON.parse(raw)
  } catch {
    return null
  }
}

function saveAuth(data) {
  localStorage.setItem('xcm_auth_v1', JSON.stringify(data))
}

function clearAuth() {
  localStorage.removeItem('xcm_auth_v1')
}

export const useAuthStore = defineStore('auth', {
  state: () => {
    const saved = loadAuth()
    return {
      token: saved?.token || null,
      user: saved?.user || null,
    }
  },

  getters: {
    isLoggedIn: (state) => !!state.token,
    userName: (state) => state.user?.name || '',
    userPhone: (state) => state.user?.phone || '',
    userAddress: (state) => state.user?.address || '',
  },

  actions: {
    async register(email, name, password, phone = '', address = '') {
      const res = await apiPost('/api/auth/register', { email, name, password, phone, address })
      this.token = res.token
      this.user = res.user
      saveAuth({ token: res.token, user: res.user })
      // 登入後載入雲端購物車
      useCartStore().loadFromServer()
    },

    async login(email, password) {
      const res = await apiPost('/api/auth/login', { email, password })
      this.token = res.token
      this.user = res.user
      saveAuth({ token: res.token, user: res.user })
      // 登入後載入雲端購物車
      useCartStore().loadFromServer()
    },

    async fetchMe() {
      if (!this.token) return null
      try {
        const res = await fetch('/api/auth/me', {
          headers: { Authorization: `Bearer ${this.token}` },
        })
        if (!res.ok) throw new Error('unauthorized')
        const data = await res.json()
        this.user = data.user
        saveAuth({ token: this.token, user: data.user })
        return data.user
      } catch {
        this.logout()
        return null
      }
    },

    async updateProfile(updates) {
      if (!this.token) return
      const res = await fetch('/api/auth/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.token}`,
        },
        body: JSON.stringify(updates),
      })
      if (!res.ok) throw new Error('更新失敗')
      const data = await res.json()
      this.user = data.user
      saveAuth({ token: this.token, user: data.user })
    },

    logout() {
      if (this.token) {
        fetch('/api/auth/logout', {
          method: 'POST',
          headers: { Authorization: `Bearer ${this.token}` },
        }).catch(() => {})
      }
      // 登出清空本地購物車（但伺服器保留）
      const cart = useCartStore()
      cart.items = {}
      localStorage.removeItem('xcm_cart_v1')
      this.token = null
      this.user = null
      clearAuth()
    },
  },
})
