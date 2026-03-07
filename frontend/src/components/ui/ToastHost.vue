<script setup>
import { useToastStore } from '../../stores/toast'

const toast = useToastStore()
</script>

<template>
  <div class="host" aria-live="polite" aria-relevant="additions">
    <div v-for="t in toast.toasts" :key="t.id" class="toast" :class="`tone-${t.tone}`" role="status">
      {{ t.message }}
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.host {
  position: fixed;
  right: 16px;
  bottom: 16px;
  z-index: 60;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  min-width: 220px;
  max-width: 360px;
  padding: 12px 14px;
  border-radius: 14px;
  color: #fff;
  font-weight: 800;
  box-shadow: $shadow-lg;
  background: $gray-900;
}

.tone-success {
  background: linear-gradient(135deg, $emerald-600, $emerald-700);
}

.tone-neutral {
  background: $gray-900;
}
</style>

