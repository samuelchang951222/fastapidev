<script setup>
import { ref } from 'vue'
import BaseButton from '../components/ui/BaseButton.vue'

const name = ref('')
const email = ref('')
const message = ref('')
const submitted = ref(false)

function submit() {
  submitted.value = true
}
</script>

<template>
  <div class="page">
    <div class="container">
      <h1 class="title">聯絡我們</h1>
      <p class="lead">有任何合作或訂購問題，歡迎留言，我們會盡快回覆。（此版本先做 UI）</p>

      <div class="card">
        <form class="form" @submit.prevent="submit">
          <label class="field">
            <span class="label">姓名</span>
            <input v-model="name" class="input" required />
          </label>
          <label class="field">
            <span class="label">Email</span>
            <input v-model="email" class="input" type="email" required />
          </label>
          <label class="field">
            <span class="label">訊息</span>
            <textarea v-model="message" class="textarea" rows="5" required />
          </label>
          <div class="actions">
            <BaseButton variant="primary">送出</BaseButton>
            <div v-if="submitted" class="hint">已送出（示意）</div>
          </div>
        </form>
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

.card {
  margin-top: 18px;
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: #fff;
  box-shadow: $shadow-sm;
  padding: 16px;
}

.form {
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

.input,
.textarea {
  border: 1px solid $gray-200;
  border-radius: 14px;
  padding: 10px 12px;
  outline: none;
}

.input:focus,
.textarea:focus {
  @include focusRing;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hint {
  color: $emerald-700;
  font-weight: 800;
}
</style>

