<template>
  <section
    class="relative bg-white transition-all"
    :class="compact ? 'pt-8 pb-6' : 'pt-20 pb-16 sm:pt-28 sm:pb-20'"
  >
    <div class="relative max-w-2xl mx-auto px-4 sm:px-6 text-center">
      <template v-if="showSlogan">
        <h1 class="font-bold text-text-primary leading-tight mb-3"
          :class="compact ? 'text-xl sm:text-2xl' : 'text-3xl sm:text-4xl'"
        >
          粘贴链接，立刻下载
        </h1>
        <p class="text-text-muted text-sm mb-8">支持 YouTube、Bilibili、抖音、TikTok 等 1800+ 平台</p>
      </template>

      <!-- URL input -->
      <form @submit.prevent="onSubmit" class="flex items-center gap-2" role="search">
        <label for="video-url-input" class="sr-only">粘贴视频链接</label>
        <div class="relative flex-1">
          <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
          <input
            id="video-url-input"
            v-model="url"
            type="url"
            placeholder="粘贴视频链接..."
            class="w-full h-11 pl-10 pr-4 rounded-lg border border-border bg-white text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
            :disabled="loading"
            autocomplete="url"
          />
        </div>
        <button
          type="submit"
          :disabled="loading || !url.trim()"
          class="flex items-center gap-1.5 h-11 px-5 rounded-lg bg-primary hover:bg-primary-dark text-white text-sm font-medium transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-sm cursor-pointer shrink-0"
        >
          <svg v-if="loading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ loading ? '解析中...' : '解析' }}
        </button>
      </form>

      <!-- Quick examples -->
      <div v-if="showSlogan" class="flex items-center justify-center gap-2 mt-4 text-xs text-text-muted flex-wrap">
        <span>试试：</span>
        <button
          v-for="example in examples"
          :key="example.label"
          @click="url = example.url"
          class="px-2.5 py-1 rounded-md border border-border-light hover:border-primary hover:text-primary transition-all cursor-pointer"
        >
          {{ example.label }}
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  loading: Boolean,
  compact: Boolean,
  showSlogan: { type: Boolean, default: true },
})
const emit = defineEmits(['parse'])

const url = ref('')

const examples = [
  { label: 'YouTube', url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' },
  { label: 'Bilibili', url: 'https://www.bilibili.com/video/BV1GJ411x7h7' },
  { label: 'Twitter/X', url: 'https://x.com/elonmusk/status/1234567890' },
]

function normalizeUrl(raw) {
  let u = raw
  if (u.includes('bilibili.com') && !u.includes('www.bilibili.com')) {
    u = u.replace('bilibili.com', 'www.bilibili.com')
  }
  return u
}

function onSubmit() {
  const trimmed = url.value.trim()
  if (trimmed) emit('parse', normalizeUrl(trimmed))
}
</script>
