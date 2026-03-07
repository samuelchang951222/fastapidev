import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({
    isCartOpen: false,
    isSearchOpen: false,
    isMemberEnabled: false, // UI-only
  }),
  actions: {
    openCart() {
      this.isCartOpen = true
    },
    closeCart() {
      this.isCartOpen = false
    },
    toggleCart() {
      this.isCartOpen = !this.isCartOpen
    },
    openSearch() {
      this.isSearchOpen = true
    },
    closeSearch() {
      this.isSearchOpen = false
    },
    toggleSearch() {
      this.isSearchOpen = !this.isSearchOpen
    },
    enableMember() {
      this.isMemberEnabled = true
    },
  },
  persist: false,
})

