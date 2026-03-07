<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUiStore } from '../../stores/ui'
import BaseButton from '../ui/BaseButton.vue'

const ui = useUiStore()
const router = useRouter()
const route = useRoute()

const q = ref('')

watch(
  () => ui.isSearchOpen,
  (open) => {
    if (open) q.value = typeof route.query.q === 'string' ? route.query.q : ''
  },
)

function submit() {
  ui.closeSearch()
  router.push({ path: '/shop', query: { ...route.query, q: q.value || undefined } })
}
</script>

<template>
  <div v-if="ui.isSearchOpen" class="wrap" role="dialog" aria-label="搜尋商品">
    <div class="container panel">
      <form class="form" @submit.prevent="submit">
        <input v-model="q" class="input" type="search" placeholder="搜尋商品..." aria-label="搜尋商品" autofocus />
        <BaseButton variant="primary" class="btn">搜尋</BaseButton>
        <BaseButton variant="ghost" class="btn" type="button" @click="ui.closeSearch()">關閉</BaseButton>
      </form>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.wrap {
  position: sticky;
  top: 72px;
  z-index: 39;
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 1px solid $gray-200;
  backdrop-filter: blur(10px);
}

.panel {
  padding: 14px 0;
}

.form {
  display: flex;
  gap: 10px;
  align-items: center;
}

.input {
  flex: 1;
  height: 44px;
  border-radius: 999px;
  border: 1px solid $gray-200;
  padding: 0 16px;
  outline: none;
  background: #fff;
}

.input:focus {
  @include focusRing;
}

.btn {
  height: 44px;
}
</style>

