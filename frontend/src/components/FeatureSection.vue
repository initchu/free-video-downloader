<template>
  <section id="features" class="py-14 sm:py-16 bg-bg-section">
    <div class="max-w-4xl mx-auto px-4 sm:px-6">
      <h2 class="text-center text-lg font-semibold text-text-primary mb-8">核心功能</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <div
          v-for="f in features"
          :key="f.title"
          class="flex flex-col items-center gap-2 p-4 bg-white rounded-xl border border-border-light text-center"
        >
          <span class="text-2xl">{{ f.icon }}</span>
          <span class="text-sm font-medium text-text-primary">{{ f.title }}</span>
          <span class="text-xs text-text-muted leading-snug">{{ f.desc }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  { icon: '🌐', title: '1800+ 平台', desc: 'YouTube、B站、抖音等' },
  { icon: '⚡', title: '极速解析', desc: '秒级响应' },
  { icon: '📱', title: '手机可用', desc: '无需安装 App' },
  { icon: '🎬', title: '多种清晰度', desc: '最高支持 4K' },
  { icon: '🤖', title: 'AI 总结', desc: '一键生成摘要' },
]
</script>
