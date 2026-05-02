<script setup>
import { RouterLink } from 'vue-router'
import { useUiStore } from '../../stores/ui'
import { useAuthStore } from '../../stores/auth'

const ui = useUiStore()
const auth = useAuthStore()

function close() {
  ui.isMobileMenuOpen = false
}

function logout() {
  ui.isMobileMenuOpen = false
  auth.logout()
}
</script>

<template>
  <div
    v-if="ui.isMobileMenuOpen"
    class="overlay"
    @click="close"
  >
    <div class="drawer" @click.stop>
      <button class="closeBtn" @click="close">✕</button>

      <nav class="nav">
        <RouterLink to="/" class="item" @click="close">首頁</RouterLink>
        <RouterLink to="/shop" class="item" @click="close">全部商品</RouterLink>
        <RouterLink to="/about" class="item" @click="close">關於我們</RouterLink>
        <RouterLink to="/contact" class="item" @click="close">聯絡我們</RouterLink>

        <div class="sectionTitle">商品分類</div>
        <RouterLink to="/shop?category=vegetable" class="item" @click="close">蔬菜</RouterLink>
        <RouterLink to="/shop?category=fruit" class="item" @click="close">水果</RouterLink>
        <RouterLink to="/shop?category=mushroom" class="item" @click="close">菇類</RouterLink>
        <RouterLink to="/shop?category=juice" class="item" @click="close">蔬果汁</RouterLink>

        <hr class="divider" />

        <RouterLink v-if="!auth.isLoggedIn" to="/login" class="item" @click="close">登入</RouterLink>
        <RouterLink v-if="!auth.isLoggedIn" to="/register" class="item" @click="close">註冊</RouterLink>
        <button v-if="auth.isLoggedIn" class="item logoutBtn" @click="logout">登出</button>
      </nav>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  z-index: 9999999;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: flex-end;
}

.drawer {
  width: 280px;
  max-width: 85vw;
  height: 100%;
  background: #fff;
  padding: 16px;
  overflow-y: auto;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.1);
}

.closeBtn {
  display: block;
  margin-left: auto;
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 999px;
  font-size: 14px;
  cursor: pointer;
  font-weight: 900;
  color: #374151;
}

.nav {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item {
  display: block;
  padding: 10px 12px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 15px;
  color: #1f2937;
  text-align: left;
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
  text-decoration: none;
}

.item:hover {
  background: #f3f4f6;
}

.item:active {
  background: #e5e7eb;
}

.sectionTitle {
  padding: 8px 12px 2px;
  font-size: 11px;
  font-weight: 800;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.logoutBtn {
  color: #dc2626;
}

.divider {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 8px 0;
}

@media (min-width: 768px) {
  .overlay {
    display: none;
  }
}
</style>
