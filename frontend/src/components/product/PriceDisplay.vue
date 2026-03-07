<script setup>
defineProps({
  price: { type: Number, required: true },
  compareAtPrice: { type: Number, default: null },
})

function fmt(n) {
  return `NT$ ${Number(n || 0).toLocaleString('zh-TW')}`
}
</script>

<template>
  <div class="wrap">
    <div v-if="compareAtPrice" class="compare">{{ fmt(compareAtPrice) }}</div>
    <div class="price">{{ fmt(price) }}</div>
  </div>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.wrap {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}

.compare {
  color: $gray-500;
  font-weight: 800;
  text-decoration: line-through;
  font-size: 13px;
}

.price {
  color: $gray-900;
  font-weight: 900;
}
</style>

