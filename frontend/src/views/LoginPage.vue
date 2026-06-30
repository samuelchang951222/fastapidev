<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { apiPost } from '../api/client'
import BaseButton from '../components/ui/BaseButton.vue'

const router = useRouter()
const auth = useAuthStore()

// ── Login ──
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

// ── Password reset ──
// step: 'login' | 'request' | 'confirm' | 'done'
const step = ref('login')
const resetPhone = ref('')
const resetOtp = ref('')
const resetNewPassword = ref('')
const resetConfirmPassword = ref('')
const resetError = ref('')
const resetLoading = ref(false)

function goReset() {
  step.value = 'request'
  resetError.value = ''
}

function goLogin() {
  step.value = 'login'
  resetError.value = ''
  resetPhone.value = ''
  resetOtp.value = ''
  resetNewPassword.value = ''
  resetConfirmPassword.value = ''
}

async function sendOtp() {
  resetError.value = ''
  resetLoading.value = true
  try {
    await apiPost('/api/auth/password-reset/request', { phone: resetPhone.value })
    step.value = 'confirm'
  } catch (e) {
    resetError.value = e instanceof Error ? e.message : '發送失敗，請稍後再試'
  } finally {
    resetLoading.value = false
  }
}

async function confirmReset() {
  resetError.value = ''
  if (resetNewPassword.value !== resetConfirmPassword.value) {
    resetError.value = '兩次輸入的密碼不一致'
    return
  }
  if (resetNewPassword.value.length < 8) {
    resetError.value = '新密碼至少需要 8 個字元'
    return
  }
  resetLoading.value = true
  try {
    await apiPost('/api/auth/password-reset/confirm', {
      phone: resetPhone.value,
      otp: resetOtp.value,
      new_password: resetNewPassword.value,
    })
    step.value = 'done'
  } catch (e) {
    resetError.value = e instanceof Error ? e.message : '驗證失敗，請重試'
  } finally {
    resetLoading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div class="container">
      <div class="card">

        <!-- ── Login ── -->
        <template v-if="step === 'login'">
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
            <button type="button" class="forgotBtn" @click="goReset">忘記密碼？</button>
            <p v-if="error" class="error">{{ error }}</p>
            <BaseButton type="submit" variant="neutral" class="submitBtn" :disabled="loading">
              {{ loading ? '登入中…' : '登入' }}
            </BaseButton>
          </form>
          <p class="switch">
            還沒有帳號？
            <RouterLink to="/register">註冊</RouterLink>
          </p>
        </template>

        <!-- ── Step 1: Enter phone ── -->
        <template v-else-if="step === 'request'">
          <h1 class="title">重設密碼</h1>
          <p class="subtitle">輸入您註冊時使用的手機號碼，我們將傳送驗證碼給您。</p>
          <form class="form" @submit.prevent="sendOtp">
            <label class="field">
              <span class="label">手機號碼</span>
              <input v-model="resetPhone" type="tel" class="input" required placeholder="09xxxxxxxx" />
            </label>
            <p v-if="resetError" class="error">{{ resetError }}</p>
            <BaseButton type="submit" variant="neutral" class="submitBtn" :disabled="resetLoading">
              {{ resetLoading ? '傳送中…' : '傳送驗證碼' }}
            </BaseButton>
          </form>
          <p class="switch"><button type="button" class="forgotBtn" @click="goLogin">← 返回登入</button></p>
        </template>

        <!-- ── Step 2: Enter OTP + new password ── -->
        <template v-else-if="step === 'confirm'">
          <h1 class="title">輸入驗證碼</h1>
          <p class="subtitle">已傳送 6 位數驗證碼至 {{ resetPhone }}，請在 10 分鐘內完成。</p>
          <form class="form" @submit.prevent="confirmReset">
            <label class="field">
              <span class="label">驗證碼</span>
              <input v-model="resetOtp" type="text" class="input" required placeholder="123456" maxlength="6" inputmode="numeric" />
            </label>
            <label class="field">
              <span class="label">新密碼</span>
              <input v-model="resetNewPassword" type="password" class="input" required placeholder="至少 8 個字元" />
            </label>
            <label class="field">
              <span class="label">確認新密碼</span>
              <input v-model="resetConfirmPassword" type="password" class="input" required placeholder="再輸入一次" />
            </label>
            <p v-if="resetError" class="error">{{ resetError }}</p>
            <BaseButton type="submit" variant="neutral" class="submitBtn" :disabled="resetLoading">
              {{ resetLoading ? '更新中…' : '更新密碼' }}
            </BaseButton>
          </form>
          <p class="switch"><button type="button" class="forgotBtn" @click="goReset">重新傳送驗證碼</button></p>
        </template>

        <!-- ── Done ── -->
        <template v-else-if="step === 'done'">
          <div class="doneWrap">
            <div class="doneIcon">✓</div>
            <h1 class="title">密碼已更新</h1>
            <p class="subtitle">請使用新密碼重新登入。</p>
            <BaseButton variant="neutral" class="submitBtn" @click="goLogin">返回登入</BaseButton>
          </div>
        </template>

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

.subtitle {
  margin: 10px 0 0;
  text-align: center;
  color: $gray-500;
  font-size: 14px;
  line-height: 1.5;
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

.forgotBtn {
  background: none;
  border: none;
  padding: 0;
  color: $gray-500;
  font-size: 13px;
  cursor: pointer;
  text-align: left;

  &:hover {
    color: $emerald-600;
  }
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

.doneWrap {
  display: grid;
  gap: 10px;
  text-align: center;
}

.doneIcon {
  margin: 0 auto;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: $emerald-100;
  color: $emerald-600;
  font-size: 28px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
