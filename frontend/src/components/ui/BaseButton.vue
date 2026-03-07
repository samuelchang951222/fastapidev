<script setup>
defineProps({
  variant: { type: String, default: 'primary' }, // primary | ghost | neutral
  type: { type: String, default: 'button' },
})
</script>

<template>
  <button class="btn" :class="`v-${variant}`" :type="type">
    <slot />
  </button>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid transparent;
  font-weight: 800;
  cursor: pointer;
  transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease, border-color 120ms ease;
  user-select: none;
}

.btn:active {
  transform: translateY(1px);
}

.v-primary {
  background: linear-gradient(135deg, $emerald-500, $emerald-700);
  color: #fff;
  box-shadow: $shadow-sm;
}

.v-primary:hover {
  box-shadow: $shadow-md;
}

.v-ghost {
  background: transparent;
  color: $gray-800;
  border-color: $gray-200;
}

.v-ghost:hover {
  background: $gray-100;
}

.v-neutral {
  background: $gray-900;
  color: #fff;
}

.btn:focus-visible {
  @include focusRing;
}
</style>

