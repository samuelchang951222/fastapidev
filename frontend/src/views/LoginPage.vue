<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import BaseButton from '../components/ui/BaseButton.vue'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(email.value, password.value)
    const redirect = router.currentRoute.value.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    error.value = e instanceof Error ? e.message : '登入失敗'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div class="container">
      <div class="card">
        <h1 class="title">登入</h1>
        <form class="form" @submit.prevent="submit">
          <label class="field">
            <span class="label">Email</span>
            <input v-model="email" type="email" class="input" required placeholder="example@email.com" />
          </label>
          <label class="field">
            <span class="label">密碼</span>
            <input v-model="password" type="password" class="input" required placeholder="請輸入密碼" />
          </label>
          <p v-if="error" class="error">{{ error }}</p>
          <BaseButton type="submit" variant="neutral" class="submitBtn" :disabled="loading">
            {{ loading ? '登入中…' : '登入' }}
          </BaseButton>
        </form>
        <p class="switch">
          還沒有帳號？
          <RouterLink to="/register">註冊</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '../styles/tokens' as *;

.page {
  padding: 60px 0;
}

.card {
  max-width: 400px;
  margin: 0 auto;
  border: 1px solid $gray-200;
  border-radius: $radius-xl;
  background: #fff;
  box-shadow: $shadow-sm;
  padding: 28px 24px;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 900;
  text-align: center;
}

.form {
  margin-top: 20px;
  display: grid;
  gap: 14px;
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
  font-size: 15px;
}

.input:focus {
  @include focusRing;
}

.submitBtn {
  height: 46px;
  margin-top: 6px;
}

.error {
  color: #e53e3e;
  font-weight: 800;
  font-size: 13px;
  margin: 0;
}

.switch {
  margin-top: 18px;
  text-align: center;
  color: $gray-600;
  font-size: 14px;

  a {
    color: $emerald-600;
    font-weight: 800;
  }
}
</style>
