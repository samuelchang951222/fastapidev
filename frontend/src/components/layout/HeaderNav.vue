<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useUiStore } from '../../stores/ui'
import { useCartStore } from '../../stores/cart'
import BaseButton from '../ui/BaseButton.vue'

const ui = useUiStore()
const cart = useCartStore()
const router = useRouter()

const showBadge = computed(() => cart.totalCount > 0)

function goShop() {
  router.push('/shop')
}
</script>

<template>
  <header class="header">
    <div class="container headerInner">
      <RouterLink to="/" class="brand" aria-label="鮮採市集">
        <span class="logoBox" />
        <span class="brandText">鮮採市集</span>
      </RouterLink>

      <nav class="navLinks" aria-label="主選單">
        <RouterLink to="/" class="navLink">首頁</RouterLink>
        <RouterLink to="/shop" class="navLink">全部商品</RouterLink>
        <RouterLink to="/about" class="navLink">關於我們</RouterLink>
        <RouterLink to="/contact" class="navLink">聯絡我們</RouterLink>
      </nav>

      <div class="actions">
        <BaseButton variant="ghost" class="iconBtn" title="搜尋商品" aria-label="搜尋商品" @click="ui.toggleSearch()">
          <svg viewBox="0 0 24 24" class="icon" aria-hidden="true">
            <path
              fill="currentColor"
              d="M10 4a6 6 0 104.472 10.027l3.25 3.25a1 1 0 001.414-1.414l-3.25-3.25A6 6 0 0010 4zm-4 6a4 4 0 118 0 4 4 0 01-8 0z"
            />
          </svg>
        </BaseButton>

        <div class="cartWrap">
          <BaseButton
            variant="ghost"
            class="iconBtn"
            title="購物車"
            aria-label="購物車"
            @click="ui.toggleCart()"
          >
            <svg viewBox="0 0 24 24" class="icon" aria-hidden="true">
              <path
                fill="currentColor"
                d="M7 4a1 1 0 00-1 1v1H4a1 1 0 000 2h1.2l1.49 8.2A2 2 0 008.66 18H18a1 1 0 000-2H8.66l-.18-1H18a2 2 0 001.97-1.64L21 7H8V5a1 1 0 00-1-1z"
              />
              <path fill="currentColor" d="M9 21a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm9 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" />
            </svg>
          </BaseButton>
          <span v-if="showBadge" class="badge" aria-label="購物車數量">{{ cart.badgeText }}</span>
        </div>

        <BaseButton variant="primary" class="cta" @click="goShop">立即選購</BaseButton>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.header {
  position: sticky;
  top: 0;
  z-index: 40;
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid $gray-200;
}

.headerInner {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 900;
  letter-spacing: 0.2px;
}

.logoBox {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, $emerald-500, $emerald-700);
  box-shadow: $shadow-sm;
}

.brandText {
  font-size: 18px;
}

.navLinks {
  display: none;
  gap: 18px;
  align-items: center;
}

.navLink {
  color: $gray-700;
  font-weight: 700;
  font-size: 14px;
  padding: 8px 10px;
  border-radius: 999px;
  transition: background 160ms ease, color 160ms ease;
}

.navLink.router-link-active {
  color: $emerald-700;
  background: $emerald-50;
}

.navLink:hover {
  background: $gray-100;
}

.actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.iconBtn {
  width: 40px;
  height: 40px;
  padding: 0;
  border-radius: 999px;
}

.icon {
  width: 20px;
  height: 20px;
}

.cartWrap {
  position: relative;
}

.badge {
  position: absolute;
  top: -6px;
  right: -6px;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: $red-500;
  color: #fff;
  font-size: 12px;
  font-weight: 800;
  box-shadow: $shadow-sm;
}

.cta {
  display: none;
}

@media (min-width: 768px) {
  .navLinks {
    display: flex;
  }
}

@media (min-width: 1024px) {
  .cta {
    display: inline-flex;
  }
}
</style>

