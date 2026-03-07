import { defineStore } from 'pinia'

let nextId = 1

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [],
  }),
  actions: {
    push(message, { tone = 'success', timeoutMs = 2400 } = {}) {
      const id = nextId++
      this.toasts.push({ id, message, tone })
      window.setTimeout(() => this.dismiss(id), timeoutMs)
      return id
    },
    dismiss(id) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },
    clear() {
      this.toasts = []
    },
  },
})

