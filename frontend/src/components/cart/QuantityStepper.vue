<script setup>
import BaseButton from '../ui/BaseButton.vue'

defineProps({
  value: { type: Number, required: true },
  min: { type: Number, default: 1 },
  max: { type: Number, default: 999 },
})

const emit = defineEmits(['update:value'])

function set(v) {
  const n = Math.max(Number.isFinite(v) ? v : 1, 1)
  emit('update:value', n)
}
</script>

<template>
  <div class="stepper" role="group" aria-label="數量">
    <BaseButton variant="ghost" class="btn" type="button" aria-label="減少" @click="set(Math.max(min, value - 1))">
      −
    </BaseButton>
    <div class="val" aria-label="目前數量">{{ value }}</div>
    <BaseButton variant="ghost" class="btn" type="button" aria-label="增加" @click="set(Math.min(max, value + 1))">
      +
    </BaseButton>
  </div>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.stepper {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px;
  border: 1px solid $gray-200;
  border-radius: 999px;
  background: #fff;
}

.btn {
  width: 34px;
  height: 34px;
  padding: 0;
  border-radius: 999px;
  font-size: 18px;
  font-weight: 900;
}

.val {
  min-width: 22px;
  text-align: center;
  font-weight: 900;
  color: $gray-900;
}
</style>

