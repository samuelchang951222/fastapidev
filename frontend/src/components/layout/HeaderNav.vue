<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { useUiStore } from '../../stores/ui'
import { useCartStore } from '../../stores/cart'
import { useAuthStore } from '../../stores/auth'
import BaseButton from '../ui/BaseButton.vue'

const ui = useUiStore()
const cart = useCartStore()
const auth = useAuthStore()
const router = useRouter()

const showBadge = computed(() => cart.totalCount > 0)
const showUserMenu = ref(false)

function goShop() {
  router.push('/shop')
}

function toggleUserMenu(e) {
  e.stopPropagation()
  showUserMenu.value = !showUserMenu.value
}

function handleLogout() {
  showUserMenu.value = false
  if (window.hmClose) window.hmClose()
  auth.logout()
  router.push('/')
}

function openMobileMenu() {
  window.hmOpen()
}

function onDocumentClick(e) {
  if (!showUserMenu.value) return
  const wrap = document.querySelector('.userMenuWrap')
  if (wrap && !wrap.contains(e.target)) {
    showUserMenu.value = false
  }
}

onMounted(() => document.addEventListener('click', onDocumentClick))
onUnmounted(() => document.removeEventListener('click', onDocumentClick))
</script>

<template>
  <header class="header" @click.self="showUserMenu = false">
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

        <!-- 登入/使用者選單 -->
        <div v-if="!auth.isLoggedIn" class="authLinks">
          <RouterLink to="/login" class="navLink">登入</RouterLink>
          <RouterLink to="/register" class="navLink registerLink">註冊</RouterLink>
        </div>
        <div v-else class="userMenuWrap">
          <BaseButton variant="ghost" class="iconBtn userBtn" @click="toggleUserMenu" :title="auth.userName">
            <span class="avatar">{{ auth.userName.charAt(0) }}</span>
          </BaseButton>
          <div v-if="showUserMenu" class="userDropdown" @click.stop>
            <div class="dropdownUser">{{ auth.userName }}</div>
            <div class="dropdownEmail">{{ auth.user?.email }}</div>
            <hr class="dropdownDivider" />
            <button class="dropdownItem" @click="handleLogout">登出</button>
          </div>
        </div>

        <BaseButton variant="primary" class="cta" @click="goShop">立即選購</BaseButton>

        <!-- 漢堡選單按鈕（手機版）— 使用全域 JS，完全繞過 Vue component 系統 -->
        <button class="hamburger" @click="openMobileMenu" aria-label="選單">
          <span class="hamLine" />
        </button>
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
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid $gray-200;
}

.headerInner {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 900;
  letter-spacing: 0.2px;
}

.logoBox {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: linear-gradient(135deg, $emerald-500, $emerald-700);
  box-shadow: $shadow-sm;
}

.brandText {
  font-size: 16px;
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

.authLinks {
  display: none;
  gap: 6px;
  align-items: center;
}

.registerLink {
  background: $emerald-50;
  color: $emerald-700 !important;
}

.userMenuWrap {
  position: relative;
}

.userBtn {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  padding: 0;
}

.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: $emerald-600;
  color: #fff;
  font-weight: 900;
  font-size: 14px;
}

.userDropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 200px;
  background: #fff;
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  box-shadow: $shadow-lg;
  padding: 8px;
  z-index: 50;
}

.dropdownUser {
  font-weight: 900;
  padding: 4px 8px;
  font-size: 14px;
}

.dropdownEmail {
  color: $gray-600;
  padding: 2px 8px 4px;
  font-size: 13px;
}

.dropdownDivider {
  border: none;
  border-top: 1px solid $gray-100;
  margin: 6px 0;
}

.dropdownItem {
  display: block;
  width: 100%;
  text-align: left;
  padding: 8px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  background: none;
  border: none;
  cursor: pointer;
  color: $red-600;
}

.dropdownItem:hover {
  background: $gray-100;
}

/* ── 漢堡選單（手機版） ── */
.hamburger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 999px;
  position: relative;
}

.hamLine,
.hamLine::before,
.hamLine::after {
  display: block;
  width: 20px;
  height: 2px;
  background: $gray-800;
  border-radius: 2px;
  transition: transform 200ms ease;
}

.hamLine {
  position: relative;
}

.hamLine::before,
.hamLine::after {
  content: '';
  position: absolute;
  left: 0;
}

.hamLine::before {
  top: -6px;
}

.hamLine::after {
  top: 6px;
}

.hamLine.open {
  background: transparent;
}

.hamLine.open::before {
  top: 0;
  transform: rotate(45deg);
}

.hamLine.open::after {
  top: 0;
  transform: rotate(-45deg);
}

/* ── 桌機隱藏漢堡選單 ── */
@media (min-width: 768px) {
  .hamburger {
    display: none;
  }
}

@media (min-width: 768px) {
  .headerInner {
    height: 72px;
    gap: 18px;
  }
  .logoBox {
    width: 34px;
    height: 34px;
    border-radius: 10px;
  }
  .brandText {
    font-size: 18px;
  }
  .navLinks {
    display: flex;
  }
  .authLinks {
    display: flex;
  }
}

@media (min-width: 1024px) {
  .cta {
    display: inline-flex;
  }
}
</style>
