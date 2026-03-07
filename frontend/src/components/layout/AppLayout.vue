<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

import HeaderNav from './HeaderNav.vue'
import SearchPanel from './SearchPanel.vue'
import CartDrawer from '../cart/CartDrawer.vue'
import ToastHost from '../ui/ToastHost.vue'
import { useUiStore } from '../../stores/ui'

const ui = useUiStore()
const route = useRoute()

function onKeydown(e) {
  if (e.key !== 'Escape') return
  ui.closeSearch()
  ui.closeCart()
}

watch(
  () => route.fullPath,
  () => {
    ui.closeSearch()
    ui.closeCart()
  },
)

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
  <div class="layout">
    <HeaderNav />
    <SearchPanel />

    <main class="main">
      <slot />
    </main>

    <footer class="footer">
      <div class="container footerInner">
        <div class="brand">鮮採市集</div>
        <div class="meta">© {{ new Date().getFullYear() }} Fresh Market</div>
      </div>
    </footer>

    <CartDrawer />
    <ToastHost />
  </div>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
}

.footer {
  border-top: 1px solid $gray-200;
  background: #fff;
}

.footerInner {
  padding: 22px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.brand {
  font-weight: 800;
  letter-spacing: 0.2px;
}

.meta {
  color: $gray-500;
  font-size: 14px;
}
</style>

