<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import BaseButton from '../components/ui/BaseButton.vue'
import ProductCard from '../components/product/ProductCard.vue'
import { useCatalogStore } from '../stores/catalog'
import { useUiStore } from '../stores/ui'

const route = useRoute()
const router = useRouter()
const catalog = useCatalogStore()
const ui = useUiStore()

const mobileFilterOpen = ref(false)

const q = computed(() => (typeof route.query.q === 'string' ? route.query.q : ''))
const category = computed(() => (typeof route.query.category === 'string' ? route.query.category : 'all'))
const sort = computed(() => (typeof route.query.sort === 'string' ? route.query.sort : 'featured'))

const sortOptions = [
  { value: 'featured', label: '精選推薦' },
  { value: 'priceAsc', label: '價格由低到高' },
  { value: 'priceDesc', label: '價格由高到低' },
  { value: 'newest', label: '最新上架' },
]

const categoryOptions = computed(() => {
  const list = catalog.categories || []
  return [{ slug: 'all', name: '全部商品' }, ...list]
})

const flashSaleProducts = computed(() => {
  const ids = new Set((catalog.flashSales || []).map((x) => String(x.productId)))
  const list = catalog.allProducts || catalog.products || []
  return list.filter((p) => ids.has(String(p.id))).slice(0, 3)
})

function setQuery(patch) {
  router.push({ path: '/shop', query: { ...route.query, ...patch } })
}

function clearSearch() {
  const next = { ...route.query }
  delete next.q
  router.push({ path: '/shop', query: next })
}

const products = computed(() => catalog.products || [])

const resultTitle = computed(() => {
  if (!q.value) return `共 ${products.value.length} 項商品`
  return `搜尋「${q.value}」 · 共 ${products.value.length} 項商品`
})

watch(
  () => route.query,
  () => {
    mobileFilterOpen.value = false
  },
)

function loadForQuery() {
  const params = {
    sort: sort.value,
    category: category.value !== 'all' ? category.value : undefined,
    q: q.value || undefined,
  }
  return catalog.loadProducts(params)
}

onMounted(async () => {
  if (catalog.status === 'idle') await catalog.loadAll()
  await loadForQuery()
})

watch([q, category, sort], () => {
  loadForQuery()
})
</script>

<template>
  <div class="page">
    <div class="container">
      <div class="head">
        <div>
          <h1 class="title">全部商品</h1>
          <div class="summary">
            <span>{{ resultTitle }}</span>
            <button v-if="q" type="button" class="clear" @click="clearSearch">清除</button>
          </div>
        </div>

        <div class="tools">
          <button class="filterBtn" type="button" @click="mobileFilterOpen = !mobileFilterOpen">
            篩選
          </button>

          <div class="sort">
            <select class="select" :value="sort" @change="setQuery({ sort: $event.target.value })">
              <option v-for="o in sortOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
            <span class="chev" aria-hidden="true">▾</span>
          </div>
        </div>
      </div>

      <section v-if="flashSaleProducts.length" class="flash">
        <div class="flashHead">
          <div>
            <div class="flashTitle">限時搶購</div>
            <div class="flashSub">今日限定的超值優惠（UI/假資料）</div>
          </div>
        </div>
        <div class="flashGrid">
          <ProductCard v-for="p in flashSaleProducts" :key="p.id" :product="p" />
        </div>
      </section>

      <div v-if="mobileFilterOpen" class="mobileFilters">
        <div class="mobileTitle">分類</div>
        <div class="chips">
          <button
            v-for="c in categoryOptions"
            :key="c.slug"
            class="chip"
            :class="{ active: category === c.slug }"
            type="button"
            @click="setQuery({ category: c.slug === 'all' ? undefined : c.slug })"
          >
            {{ c.name }}
          </button>
        </div>

        <BaseButton v-if="!ui.isMemberEnabled" variant="primary" class="memberBtn" @click="ui.enableMember()">
          加入會員享優惠
        </BaseButton>
      </div>

      <div class="layout">
        <aside class="sidebar">
          <section class="sideCard">
            <div class="sideTitle">分類篩選</div>
            <div class="sideList">
              <button
                v-for="c in categoryOptions"
                :key="c.slug"
                class="sideItem"
                :class="{ active: category === c.slug }"
                type="button"
                @click="setQuery({ category: c.slug === 'all' ? undefined : c.slug })"
              >
                {{ c.name }}
              </button>
            </div>
          </section>

          <section class="promo">
            <div class="promoTitle">當季特惠</div>
            <div v-if="!ui.isMemberEnabled" class="promoDesc">
              加入會員即享首購 9 折優惠，還有不定時滿額贈禮！
            </div>
            <div v-else class="promoEnabled">
              <span class="dot" aria-hidden="true" />
              會員優惠已啟用
            </div>
            <BaseButton v-if="!ui.isMemberEnabled" variant="primary" class="promoBtn" @click="ui.enableMember()">
              立即加入
            </BaseButton>
          </section>
        </aside>

        <section class="content">
          <div v-if="catalog.status === 'loading'" class="state">載入中...</div>
          <div v-else-if="catalog.status === 'error'" class="state error">載入失敗：{{ catalog.error }}</div>

          <div v-else>
            <div v-if="products.length === 0" class="empty">
              <div v-if="q" class="emptyTitle">找不到「{{ q }}」的相關商品</div>
              <div v-else class="emptyTitle">沒有找到相關商品</div>
              <BaseButton variant="ghost" @click="router.push('/shop')">
                <span v-if="q">清除搜尋，查看所有商品</span>
                <span v-else>查看所有商品</span>
              </BaseButton>
            </div>

            <div v-else class="grid">
              <ProductCard v-for="p in products" :key="p.id" :product="p" />
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/tokens' as *;

.page {
  padding: 22px 0 46px;
}

.head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.title {
  margin: 0;
  font-size: 26px;
  font-weight: 900;
}

.summary {
  margin-top: 8px;
  color: $gray-600;
  font-weight: 800;
  display: flex;
  gap: 10px;
  align-items: center;
}

.clear {
  border: 0;
  background: transparent;
  color: $red-600;
  font-weight: 900;
  cursor: pointer;
  text-decoration: underline;
}

.tools {
  display: flex;
  gap: 10px;
  align-items: center;
}

.flash {
  margin-top: 14px;
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: linear-gradient(135deg, rgba($emerald-50, 0.9), #fff);
  box-shadow: $shadow-sm;
  padding: 14px;
}

.flashHead {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.flashTitle {
  font-weight: 900;
  font-size: 18px;
}

.flashSub {
  margin-top: 6px;
  color: $gray-600;
  font-weight: 700;
  font-size: 14px;
}

.flashGrid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.filterBtn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 14px;
  border-radius: 999px;
  border: 1px solid $gray-200;
  background: #fff;
  font-weight: 900;
  cursor: pointer;
}

.sort {
  position: relative;
}

.select {
  appearance: none;
  height: 40px;
  padding: 0 42px 0 14px;
  border-radius: 999px;
  border: 1px solid $gray-200;
  background: #fff;
  font-weight: 900;
  cursor: pointer;
}

.chev {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: $gray-600;
  pointer-events: none;
}

.mobileFilters {
  margin-top: 14px;
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: #fff;
  box-shadow: $shadow-sm;
  padding: 14px;
  display: grid;
  gap: 10px;
}

.mobileTitle {
  font-weight: 900;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border: 1px solid $gray-200;
  background: #fff;
  border-radius: 999px;
  padding: 8px 12px;
  font-weight: 900;
  cursor: pointer;
}

.chip.active {
  background: $emerald-50;
  border-color: $emerald-100;
  color: $emerald-700;
}

.memberBtn {
  height: 44px;
  justify-content: center;
}

.layout {
  margin-top: 14px;
  display: grid;
  gap: 14px;
}

.sidebar {
  display: none;
}

.sideCard {
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: #fff;
  box-shadow: $shadow-sm;
  padding: 14px;
}

.sideTitle {
  font-weight: 900;
}

.sideList {
  margin-top: 10px;
  display: grid;
  gap: 6px;
}

.sideItem {
  text-align: left;
  border: 0;
  background: transparent;
  padding: 10px 10px;
  border-radius: 12px;
  font-weight: 900;
  color: $gray-700;
  cursor: pointer;
}

.sideItem:hover {
  background: $gray-100;
}

.sideItem.active {
  background: $emerald-50;
  color: $emerald-700;
}

.promo {
  margin-top: 12px;
  border: 1px solid $emerald-100;
  border-radius: $radius-xl;
  background: linear-gradient(135deg, $emerald-50, #fff);
  padding: 14px;
  display: grid;
  gap: 10px;
}

.promoTitle {
  font-weight: 900;
}

.promoDesc {
  color: $gray-700;
  font-weight: 700;
  font-size: 14px;
  line-height: 1.45;
}

.promoEnabled {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 900;
  color: $emerald-700;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: $emerald-500;
  box-shadow: 0 0 0 6px rgba($emerald-500, 0.18);
  animation: pulse 1.6s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 6px rgba($emerald-500, 0.18);
  }
  70% {
    box-shadow: 0 0 0 10px rgba($emerald-500, 0.06);
  }
  100% {
    box-shadow: 0 0 0 6px rgba($emerald-500, 0.18);
  }
}

.promoBtn {
  height: 44px;
  justify-content: center;
}

.state {
  padding: 16px 0;
  font-weight: 800;
  color: $gray-700;
}

.error {
  color: $red-600;
}

.empty {
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: #fff;
  box-shadow: $shadow-sm;
  padding: 18px;
  display: grid;
  gap: 12px;
  justify-items: start;
}

.emptyTitle {
  font-weight: 900;
  color: $gray-800;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

@media (min-width: 640px) {
  .flashGrid {
    grid-template-columns: repeat(2, 1fr);
  }
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .flashGrid {
    grid-template-columns: repeat(3, 1fr);
  }
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 768px) {
  .filterBtn {
    display: none;
  }
  .mobileFilters {
    display: none;
  }
  .layout {
    grid-template-columns: 260px 1fr;
    align-items: start;
  }
  .sidebar {
    display: block;
  }
}
</style>

