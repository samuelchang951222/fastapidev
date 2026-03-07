<template>
  <div class="page">
    <div class="container">
      <h1 class="title">關於鮮採市集</h1>
      <p class="lead">
        我們是一群熱愛土地的年輕人，致力於連結在地小農與消費者，讓每一口食物都充滿溫暖與安心。
      </p>

      <div class="grid">
        <section class="card">
          <h2 class="cardTitle">友善耕作</h2>
          <p class="cardDesc">堅持不使用化學農藥與肥料，保護土地生態，讓環境永續發展。</p>
        </section>
        <section class="card">
          <h2 class="cardTitle">公平交易</h2>
          <p class="cardDesc">以合理的價格收購農產品，保障農民收益，建立長期的合作夥伴關係。</p>
        </section>
        <section class="card">
          <h2 class="cardTitle">用心服務</h2>
          <p class="cardDesc">從產地到餐桌，我們嚴格把關每一個環節，只為給您最好的購物體驗。</p>
        </section>
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

.lead {
  margin-top: 12px;
  color: $gray-700;
  font-weight: 700;
  max-width: 65ch;
}

.grid {
  margin-top: 18px;
  display: grid;
  gap: 12px;
}

.card {
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  padding: 16px;
  background: #fff;
  box-shadow: $shadow-sm;
}

.cardTitle {
  margin: 0;
  font-weight: 900;
  font-size: 18px;
}

.cardDesc {
  margin: 10px 0 0;
  color: $gray-600;
  font-weight: 700;
  line-height: 1.5;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>

