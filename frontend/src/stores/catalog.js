import { defineStore } from 'pinia'
import { apiGet } from '../api/client'

export const useCatalogStore = defineStore('catalog', {
  state: () => ({
    categories: [],
    products: [],
    allProducts: [],
    flashSales: [],
    status: 'idle', // idle | loading | ready | error
    error: null,
  }),
  actions: {
    async loadAll() {
      this.status = 'loading'
      this.error = null
      try {
        const [categories, products, flashSales] = await Promise.all([
          apiGet('/api/categories'),
          apiGet('/api/products'),
          apiGet('/api/flash-sales').catch(() => []),
        ])
        this.categories = categories
        this.products = products
        this.allProducts = products
        this.flashSales = flashSales
        this.status = 'ready'
      } catch (e) {
        this.status = 'error'
        this.error = e instanceof Error ? e.message : String(e)
      }
    },
    async loadProducts(params = {}) {
      this.status = 'loading'
      this.error = null
      try {
        const products = await apiGet('/api/products', params)
        this.products = products
        this.status = 'ready'
      } catch (e) {
        this.status = 'error'
        this.error = e instanceof Error ? e.message : String(e)
      }
    },
    async loadProductById(id) {
      return await apiGet(`/api/products/${id}`)
    },
  },
})

