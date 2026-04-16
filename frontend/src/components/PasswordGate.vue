<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/80 backdrop-blur-sm">
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-sm mx-4">
      <div class="flex justify-center mb-6">
        <div class="w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center">
          <svg class="w-7 h-7 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
      </div>
      <h2 class="text-xl font-semibold text-center text-gray-800 mb-2">访问验证</h2>
      <p class="text-sm text-center text-gray-500 mb-6">请输入访问密码继续使用</p>
      <form @submit.prevent="submit">
        <input
          v-model="password"
          type="password"
          placeholder="请输入密码"
          class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary text-sm mb-3"
          autofocus
        />
        <p v-if="error" class="text-red-500 text-xs mb-3 text-center">密码错误，请重试</p>
        <button
          type="submit"
          class="w-full h-11 rounded-full bg-primary text-white text-sm font-semibold hover:bg-primary/90 transition-colors cursor-pointer"
        >
          进入
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['unlocked'])

const SITE_PASSWORD = import.meta.env.VITE_SITE_PASSWORD || 'saveany2025'

const password = ref('')
const error = ref(false)

function submit() {
  if (password.value === SITE_PASSWORD) {
    localStorage.setItem('site_unlocked', '1')
    emit('unlocked')
  } else {
    error.value = true
    password.value = ''
  }
}
</script>
