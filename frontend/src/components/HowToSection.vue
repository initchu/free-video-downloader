<template>
  <section id="how-to-use" class="py-16 sm:py-20 bg-white" aria-labelledby="howto-heading">
    <div class="max-w-5xl mx-auto px-4 sm:px-6">
      <div class="text-center mb-10">
        <h2 id="howto-heading" class="text-lg font-semibold text-text-primary">三步完成下载</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
        <article v-for="step in steps" :key="step.number" class="relative text-center">
          <div class="w-14 h-14 rounded-2xl bg-primary/10 text-primary text-2xl font-bold flex items-center justify-center mx-auto mb-5">
            {{ step.number }}
          </div>
          <h3 class="text-lg font-semibold text-text-primary mb-2">{{ step.title }}</h3>
          <p class="text-sm text-text-secondary leading-relaxed">{{ step.desc }}</p>
        </article>
      </div>

      <div class="mt-8 text-center">
        <p class="text-xs text-text-muted">无需注册登录，手机浏览器同样可用</p>
      </div>
    </div>
  </section>
</template>

<script setup>
const steps = [
  {
    number: 1,
    title: '复制视频链接',
    desc: '找到想下载的视频，复制链接',
  },
  {
    number: 2,
    title: '粘贴并解析',
    desc: '粘贴到输入框，点击解析',
  },
  {
    number: 3,
    title: '选择清晰度下载',
    desc: '选好分辨率，一键保存到本地',
  },
]
</script>
