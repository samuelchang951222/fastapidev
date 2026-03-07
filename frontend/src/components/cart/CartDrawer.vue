<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { useUiStore } from '../../stores/ui'
import { useCartStore } from '../../stores/cart'
import BaseButton from '../ui/BaseButton.vue'
import QuantityStepper from './QuantityStepper.vue'

const ui = useUiStore()
const cart = useCartStore()
const router = useRouter()

const isEmpty = computed(() => cart.totalCount === 0)

function close() {
  ui.closeCart()
}

function checkout() {
  ui.closeCart()
  router.push('/checkout')
}

function fmt(n) {
  return `NT$ ${Number(n || 0).toLocaleString('zh-TW')}`
}
</script>

<template>
  <div v-if="ui.isCartOpen" class="overlay" role="dialog" aria-label="購物車" @click.self="close">
    <aside class="drawer">
      <div class="head">
        <div class="title">購物車</div>
        <BaseButton variant="ghost" class="closeBtn" aria-label="關閉" @click="close">✕</BaseButton>
      </div>

      <div v-if="isEmpty" class="empty">
        <div class="emptyTitle">購物車是空的</div>
        <BaseButton variant="primary" @click="close">去逛逛商品</BaseButton>
      </div>

      <div v-else class="body">
        <div class="list">
          <div v-for="it in cart.itemList" :key="it.product.id" class="row">
            <div class="thumb" aria-hidden="true">
              <img v-if="it.product.imageUrl" :src="it.product.imageUrl" alt="" />
              <div v-else class="thumbFallback" />
            </div>
            <div class="info">
              <div class="name">{{ it.product.name }}</div>
              <div class="price">{{ fmt(it.product.price) }}</div>
              <div class="controls">
                <QuantityStepper
                  :value="it.quantity"
                  @update:value="(v) => cart.setQuantity(it.product.id, v)"
                />
                <button class="remove" type="button" @click="cart.remove(it.product.id)">移除</button>
              </div>
            </div>
          </div>
        </div>

        <div class="summary">
          <div class="sumRow">
            <div class="label">總計</div>
            <div class="value">{{ fmt(cart.totalPrice) }}</div>
          </div>
          <div class="hint">運費將於結帳時計算</div>
          <BaseButton variant="neutral" class="checkoutBtn" @click="checkout">前往結帳</BaseButton>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.overlay {
  position: fixed;
  inset: 0;
  z-index: 55;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(6px);
  display: flex;
  justify-content: flex-end;
}

.drawer {
  height: 100%;
  width: 100%;
  max-width: 420px;
  background: #fff;
  box-shadow: $shadow-lg;
  display: flex;
  flex-direction: column;
}

.head {
  padding: 16px 16px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid $gray-200;
}

.title {
  font-weight: 900;
  font-size: 18px;
}

.closeBtn {
  width: 40px;
  height: 40px;
  padding: 0;
  border-radius: 999px;
}

.empty {
  padding: 28px 16px;
  display: grid;
  gap: 14px;
  justify-items: start;
}

.emptyTitle {
  font-weight: 900;
  color: $gray-800;
}

.body {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.list {
  padding: 16px;
  overflow: auto;
  display: grid;
  gap: 14px;
}

.row {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 12px;
  padding-bottom: 14px;
  border-bottom: 1px solid $gray-100;
}

.thumb {
  width: 72px;
  height: 72px;
  border-radius: 14px;
  background: $gray-100;
  overflow: hidden;
  box-shadow: $shadow-sm;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.thumbFallback {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, $emerald-100, $gray-100);
}

.info {
  display: grid;
  gap: 6px;
}

.name {
  font-weight: 900;
  color: $gray-900;
}

.price {
  color: $gray-600;
  font-weight: 800;
  font-size: 14px;
}

.controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 6px;
}

.remove {
  border: 0;
  background: transparent;
  color: $gray-500;
  font-weight: 800;
  cursor: pointer;
  text-decoration: underline;
}

.remove:hover {
  color: $red-600;
}

.summary {
  border-top: 1px solid $gray-200;
  padding: 16px;
  display: grid;
  gap: 10px;
}

.sumRow {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.label {
  color: $gray-700;
  font-weight: 800;
}

.value {
  font-weight: 900;
  font-size: 18px;
}

.hint {
  color: $gray-500;
  font-size: 13px;
  font-weight: 700;
}

.checkoutBtn {
  height: 46px;
}
</style>

