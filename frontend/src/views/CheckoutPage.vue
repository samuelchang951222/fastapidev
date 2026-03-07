<script setup>
import { computed, ref } from 'vue'
import { useCartStore } from '../stores/cart'
import BaseButton from '../components/ui/BaseButton.vue'

const cart = useCartStore()

const name = ref('')
const phone = ref('')
const address = ref('')

const total = computed(() => cart.totalPrice)

function fmt(n) {
  return `NT$ ${Number(n || 0).toLocaleString('zh-TW')}`
}

function submit() {
  // UI only
  cart.clear()
  alert('已送出訂單（示意）')
}
</script>

<template>
  <div class="page">
    <div class="container">
      <h1 class="title">結帳</h1>
      <div class="grid">
        <section class="card">
          <h2 class="cardTitle">收件資訊</h2>
          <form class="form" @submit.prevent="submit">
            <label class="field">
              <span class="label">姓名</span>
              <input v-model="name" class="input" required />
            </label>
            <label class="field">
              <span class="label">電話</span>
              <input v-model="phone" class="input" required />
            </label>
            <label class="field">
              <span class="label">地址</span>
              <input v-model="address" class="input" required />
            </label>
            <BaseButton variant="neutral" class="submitBtn">送出訂單</BaseButton>
          </form>
        </section>

        <aside class="card">
          <h2 class="cardTitle">訂單摘要</h2>
          <div v-if="cart.totalCount === 0" class="empty">購物車是空的</div>
          <div v-else class="summary">
            <div v-for="it in cart.itemList" :key="it.product.id" class="line">
              <div class="lineName">{{ it.product.name }}</div>
              <div class="lineMeta">x{{ it.quantity }}</div>
              <div class="linePrice">{{ fmt(it.product.price * it.quantity) }}</div>
            </div>
            <div class="divider" />
            <div class="totalRow">
              <div class="totalLabel">總計</div>
              <div class="totalValue">{{ fmt(total) }}</div>
            </div>
            <div class="hint">運費將於結帳時計算</div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/tokens' as *;

.page {
  padding: 28px 0 46px;
}

.title {
  margin: 0;
  font-size: 28px;
  font-weight: 900;
}

.grid {
  margin-top: 18px;
  display: grid;
  gap: 12px;
}

.card {
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: #fff;
  box-shadow: $shadow-sm;
  padding: 16px;
}

.cardTitle {
  margin: 0;
  font-weight: 900;
  font-size: 18px;
}

.form {
  margin-top: 12px;
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 6px;
}

.label {
  font-weight: 800;
  color: $gray-800;
  font-size: 13px;
}

.input {
  border: 1px solid $gray-200;
  border-radius: 14px;
  padding: 10px 12px;
  outline: none;
}

.input:focus {
  @include focusRing;
}

.submitBtn {
  margin-top: 6px;
  height: 46px;
}

.summary {
  margin-top: 12px;
  display: grid;
  gap: 10px;
}

.line {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 10px;
  align-items: baseline;
}

.lineName {
  font-weight: 900;
}

.lineMeta {
  color: $gray-600;
  font-weight: 800;
  font-size: 13px;
}

.linePrice {
  font-weight: 900;
}

.divider {
  height: 1px;
  background: $gray-200;
  margin: 4px 0;
}

.totalRow {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: baseline;
}

.totalLabel {
  color: $gray-700;
  font-weight: 800;
}

.totalValue {
  font-weight: 900;
  font-size: 18px;
}

.hint {
  color: $gray-500;
  font-weight: 700;
  font-size: 13px;
}

.empty {
  margin-top: 12px;
  color: $gray-600;
  font-weight: 800;
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: 1.2fr 0.8fr;
    align-items: start;
  }
}
</style>

