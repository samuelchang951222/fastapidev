<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import BaseButton from '../components/ui/BaseButton.vue'
import ProductCard from '../components/product/ProductCard.vue'
import { useCatalogStore } from '../stores/catalog'

const router = useRouter()
const catalog = useCatalogStore()

onMounted(() => {
  if (catalog.status === 'idle') catalog.loadAll()
})

const weeklyPicks = computed(() => {
  const list = catalog.allProducts || catalog.products || []
  return list.filter((p) => p.isWeeklyPick).slice(0, 4)
})

const flashSaleProducts = computed(() => {
  const ids = new Set((catalog.flashSales || []).map((x) => String(x.productId)))
  const list = catalog.allProducts || catalog.products || []
  return list.filter((p) => ids.has(String(p.id))).slice(0, 3)
})

function goShop() {
  router.push('/shop')
}
</script>

<template>
  <div class="page">
    <section class="hero">
      <div class="container heroInner">
        <div class="heroCopy">
          <h1 class="heroTitle">從產地到餐桌最新鮮的選擇</h1>
          <p class="heroDesc">
            我們堅持提供最優質的有機蔬果，支持在地小農，讓您每一口都吃得安心、健康。
          </p>
          <div class="heroCtas">
            <BaseButton variant="primary" @click="goShop">立即選購</BaseButton>
            <BaseButton variant="ghost" @click="router.push('/about')">了解我們</BaseButton>
          </div>
        </div>

        <div class="heroArt" aria-hidden="true">
          <div class="artCard a1" />
          <div class="artCard a2" />
          <div class="artCard a3" />
        </div>
      </div>
    </section>

    <section class="features">
      <div class="container">
        <div class="featureGrid">
          <div class="featureCard">
            <div class="featureTitle">有機認證</div>
            <div class="featureDesc">嚴格把關，無農藥殘留</div>
          </div>
          <div class="featureCard">
            <div class="featureTitle">產地直送</div>
            <div class="featureDesc">每日清晨採收，當日配送</div>
          </div>
          <div class="featureCard">
            <div class="featureTitle">品質保證</div>
            <div class="featureDesc">不滿意包退，購物無憂</div>
          </div>
          <div class="featureCard">
            <div class="featureTitle">友善耕作</div>
            <div class="featureDesc">愛護土地，永續發展</div>
          </div>
        </div>
      </div>
    </section>

    <section class="categories">
      <div class="container">
        <h2 class="secTitle">熱門分類</h2>
        <div class="catGrid">
          <button class="catCard" type="button" @click="router.push({ path: '/shop', query: { category: 'vegetable' } })">
            <div class="catName">蔬菜</div>
          </button>
          <button class="catCard" type="button" @click="router.push({ path: '/shop', query: { category: 'fruit' } })">
            <div class="catName">水果</div>
          </button>
          <button class="catCard" type="button" @click="router.push({ path: '/shop', query: { category: 'mushroom' } })">
            <div class="catName">菇類</div>
          </button>
          <button class="catCard" type="button" @click="router.push({ path: '/shop', query: { category: 'juice' } })">
            <div class="catName">蔬果汁</div>
          </button>
        </div>
      </div>
    </section>

    <section class="flashSale" v-if="flashSaleProducts.length">
      <div class="container">
        <div class="secHead">
          <h2 class="secTitle">限時搶購</h2>
          <div class="secSub">今日限定的超值優惠（UI/假資料）</div>
        </div>
        <div class="prodGrid">
          <ProductCard v-for="p in flashSaleProducts" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <section class="weekly">
      <div class="container">
        <div class="secHead">
          <div>
            <h2 class="secTitle">本週精選</h2>
            <div class="secSub">店長推薦的超值好物</div>
          </div>
          <BaseButton variant="ghost" class="moreBtn" @click="goShop">查看更多</BaseButton>
        </div>

        <div class="prodGrid">
          <ProductCard v-for="p in weeklyPicks" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <section class="newsletter">
      <div class="container newsInner">
        <div>
          <h2 class="newsTitle">訂閱我們的電子報</h2>
          <div class="newsDesc">
            掌握最新到貨資訊與獨家優惠，首次訂閱再送 50 元購物金！
          </div>
        </div>
        <BaseButton variant="primary">立即訂閱</BaseButton>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/tokens' as *;

.hero {
  padding: 44px 0 28px;
  background: radial-gradient(1000px 500px at 10% 0%, $emerald-50, transparent),
    radial-gradient(900px 500px at 80% 20%, rgba($emerald-200, 0.55), transparent);
}

.heroInner {
  display: grid;
  gap: 22px;
  align-items: center;
}

.heroTitle {
  margin: 0;
  font-size: 34px;
  line-height: 1.12;
  letter-spacing: -0.2px;
}

.heroDesc {
  margin: 12px 0 0;
  color: $gray-700;
  font-weight: 700;
  max-width: 42ch;
}

.heroCtas {
  margin-top: 18px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.heroArt {
  height: 220px;
  position: relative;
}

.artCard {
  position: absolute;
  border-radius: 18px;
  box-shadow: $shadow-lg;
  background: linear-gradient(135deg, $emerald-100, $gray-100);
}

.a1 {
  width: 56%;
  height: 70%;
  left: 0;
  top: 10%;
}
.a2 {
  width: 48%;
  height: 56%;
  right: 0;
  top: 0;
  background: linear-gradient(135deg, $emerald-200, $emerald-50);
}
.a3 {
  width: 44%;
  height: 50%;
  right: 10%;
  bottom: 0;
  background: linear-gradient(135deg, rgba($emerald-500, 0.22), $gray-100);
}

.features {
  padding: 18px 0 8px;
}

.featureGrid {
  display: grid;
  gap: 12px;
}

.featureCard {
  border: 1px solid $gray-200;
  border-radius: $radius-lg;
  padding: 14px 14px;
  background: #fff;
  box-shadow: $shadow-sm;
}

.featureTitle {
  font-weight: 900;
}

.featureDesc {
  margin-top: 6px;
  color: $gray-600;
  font-weight: 700;
  font-size: 14px;
}

.categories {
  padding: 26px 0 6px;
}

.secTitle {
  margin: 0;
  font-size: 20px;
  font-weight: 900;
}

.catGrid {
  margin-top: 12px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.catCard {
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  padding: 18px 16px;
  background: #fff;
  cursor: pointer;
  text-align: left;
  box-shadow: $shadow-sm;
  transition: transform 140ms ease, box-shadow 140ms ease;
}

.catCard:hover {
  transform: translateY(-2px);
  box-shadow: $shadow-md;
}

.catName {
  font-weight: 900;
}

.flashSale,
.weekly {
  padding: 26px 0;
}

.secHead {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.secSub {
  margin-top: 6px;
  color: $gray-600;
  font-weight: 700;
  font-size: 14px;
}

.prodGrid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.moreBtn {
  height: 40px;
}

.newsletter {
  padding: 26px 0 46px;
}

.newsInner {
  border-radius: $radius-xl;
  border: 1px solid $gray-200;
  background: linear-gradient(135deg, $emerald-50, #fff);
  padding: 18px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.newsTitle {
  margin: 0;
  font-weight: 900;
  font-size: 18px;
}

.newsDesc {
  margin-top: 8px;
  color: $gray-600;
  font-weight: 700;
  font-size: 14px;
}

@media (min-width: 640px) {
  .heroInner {
    grid-template-columns: 1.1fr 0.9fr;
  }
  .featureGrid {
    grid-template-columns: repeat(2, 1fr);
  }
  .catGrid {
    grid-template-columns: repeat(4, 1fr);
  }
  .prodGrid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .heroTitle {
    font-size: 44px;
  }
  .prodGrid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>

