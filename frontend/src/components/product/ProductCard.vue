<script setup>
import { useRouter } from 'vue-router'
import { useCartStore } from '../../stores/cart'
import BaseButton from '../ui/BaseButton.vue'
import PriceDisplay from './PriceDisplay.vue'

const props = defineProps({
  product: { type: Object, required: true },
})

const router = useRouter()
const cart = useCartStore()

function openDetail() {
  router.push(`/product/${props.product.id}`)
}

function add() {
  cart.add(props.product, 1)
}
</script>

<template>
  <article class="card">
    <button class="clickable" type="button" @click="openDetail">
      <div class="media" aria-hidden="true">
        <img v-if="product.imageUrl" :src="product.imageUrl" alt="" />
        <div v-else class="mediaFallback" />
        <div v-if="product.badge" class="badge">{{ product.badge }}</div>
      </div>

      <div class="body">
        <div class="meta">
          <span class="tag">{{ product.categoryName || product.categorySlug }}</span>
        </div>
        <div class="name">{{ product.name }}</div>
        <div class="desc">{{ product.description }}</div>
        <PriceDisplay :price="product.price" :compare-at-price="product.compareAtPrice || null" />
      </div>
    </button>

    <div class="foot">
      <BaseButton variant="primary" class="addBtn" @click="add">
        <svg viewBox="0 0 24 24" class="icon" aria-hidden="true">
          <path
            fill="currentColor"
            d="M7 4a1 1 0 00-1 1v1H4a1 1 0 000 2h1.2l1.49 8.2A2 2 0 008.66 18H18a1 1 0 000-2H8.66l-.18-1H18a2 2 0 001.97-1.64L21 7H8V5a1 1 0 00-1-1z"
          />
        </svg>
        <span class="text">加入</span>
      </BaseButton>
    </div>
  </article>
</template>

<style scoped lang="scss">
@use '../../styles/tokens' as *;

.card {
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: #fff;
  box-shadow: $shadow-sm;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 140ms ease, box-shadow 140ms ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: $shadow-md;
}

.clickable {
  text-align: left;
  border: 0;
  background: transparent;
  padding: 0;
  cursor: pointer;
}

.media {
  position: relative;
  height: 180px;
  background: $gray-100;
}

.media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.mediaFallback {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, $emerald-100, $gray-100);
}

.badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  background: $red-500;
  color: #fff;
  font-weight: 900;
  font-size: 12px;
  box-shadow: $shadow-sm;
}

.body {
  padding: 14px 14px 12px;
  display: grid;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  background: $gray-100;
  color: $gray-700;
  font-weight: 800;
  font-size: 12px;
}

.name {
  font-weight: 900;
  font-size: 16px;
  color: $gray-900;
}

.desc {
  color: $gray-600;
  font-weight: 700;
  font-size: 13px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.foot {
  padding: 0 14px 14px;
  margin-top: auto;
}

.addBtn {
  width: 100%;
  height: 44px;
  justify-content: center;
}

.icon {
  width: 18px;
  height: 18px;
}

.text {
  display: none;
}

@media (min-width: 640px) {
  .text {
    display: inline;
  }
}
</style>

