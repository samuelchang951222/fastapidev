<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { useCatalogStore } from '../stores/catalog'
import { useCartStore } from '../stores/cart'
import BaseButton from '../components/ui/BaseButton.vue'
import QuantityStepper from '../components/cart/QuantityStepper.vue'
import PriceDisplay from '../components/product/PriceDisplay.vue'

const props = defineProps({ id: { type: [String, Number], required: true } })

const route = useRoute()
const catalog = useCatalogStore()
const cart = useCartStore()

const status = ref('idle') // idle | loading | ready | error
const error = ref(null)
const product = ref(null)
const qty = ref(1)

const productId = computed(() => String(props.id ?? route.params.id))

async function load() {
  status.value = 'loading'
  error.value = null
  product.value = null
  try {
    product.value = await catalog.loadProductById(productId.value)
    status.value = 'ready'
    qty.value = 1
  } catch (e) {
    status.value = 'error'
    error.value = e instanceof Error ? e.message : String(e)
  }
}

watch(productId, load)

onMounted(async () => {
  if (catalog.status === 'idle') await catalog.loadAll()
  await load()
})

function add() {
  if (!product.value) return
  cart.add(product.value, qty.value)
}
</script>

<template>
  <div class="page">
    <div class="container">
      <div v-if="status === 'loading'" class="state">載入中...</div>
      <div v-else-if="status === 'error'" class="state error">載入失敗：{{ error }}</div>

      <div v-else-if="product" class="grid">
        <div class="media" aria-hidden="true">
          <img v-if="product.imageUrl" :src="product.imageUrl" alt="" />
          <div v-else class="fallback" />
        </div>

        <div class="info">
          <div class="tag">{{ product.categoryName || product.categorySlug }}</div>
          <h1 class="title">{{ product.name }}</h1>
          <p class="desc">{{ product.description }}</p>
          <PriceDisplay :price="product.price" :compare-at-price="product.compareAtPrice || null" />

          <div class="stock">庫存: {{ product.stock }} {{ product.unit }}</div>

          <div class="qtyRow">
            <div class="qtyLabel">數量:</div>
            <QuantityStepper :value="qty" @update:value="(v) => (qty = v)" />
          </div>

          <BaseButton variant="neutral" class="addBtn" @click="add">加入購物車</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/tokens' as *;

.page {
  padding: 28px 0 46px;
}

.state {
  padding: 24px 0;
  font-weight: 800;
  color: $gray-700;
}

.error {
  color: $red-600;
}

.grid {
  display: grid;
  gap: 14px;
}

.media {
  height: 320px;
  border-radius: $radius-xl;
  overflow: hidden;
  border: 1px solid $gray-200;
  background: $gray-100;
  box-shadow: $shadow-sm;
}

.media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.fallback {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, $emerald-100, $gray-100);
}

.info {
  display: grid;
  gap: 10px;
  align-content: start;
}

.tag {
  display: inline-flex;
  width: fit-content;
  padding: 6px 12px;
  border-radius: 999px;
  background: $emerald-50;
  color: $emerald-700;
  font-weight: 900;
  font-size: 12px;
  border: 1px solid $emerald-100;
}

.title {
  margin: 0;
  font-weight: 900;
  letter-spacing: -0.2px;
}

.desc {
  margin: 0;
  color: $gray-700;
  font-weight: 700;
  line-height: 1.5;
}

.stock {
  color: $gray-600;
  font-weight: 800;
  font-size: 13px;
}

.qtyRow {
  display: flex;
  align-items: center;
  gap: 12px;
}

.qtyLabel {
  color: $gray-700;
  font-weight: 900;
}

.addBtn {
  height: 46px;
  width: 100%;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }
  .addBtn {
    width: fit-content;
    padding: 0 18px;
  }
}
</style>

