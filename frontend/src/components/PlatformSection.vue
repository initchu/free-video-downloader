<template>
  <section id="platforms" class="py-10 bg-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6">
      <p class="text-center text-xs text-text-muted mb-5">支持 1800+ 平台，包括但不限于</p>
      <div class="flex flex-wrap justify-center gap-2">
        <div
          v-for="p in platforms"
          :key="p.name"
          class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-bg-section rounded-full border border-border-light text-xs text-text-secondary"
        >
          <span>{{ p.icon }}</span>
          <span>{{ p.name }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const platforms = [
  { icon: '▶️', name: 'YouTube' },
  { icon: '📺', name: 'Bilibili' },
  { icon: '🎵', name: '抖音 / TikTok' },
  { icon: '🐦', name: 'Twitter / X' },
  { icon: '📷', name: 'Instagram' },
  { icon: '📘', name: 'Facebook' },
  { icon: '🎬', name: 'Vimeo' },
  { icon: '🔴', name: 'Reddit' },
  { icon: '📌', name: 'Pinterest' },
  { icon: '💬', name: '微博' },
  { icon: '🎮', name: 'Twitch' },
  { icon: '🎧', name: 'SoundCloud' },
]
</script>
