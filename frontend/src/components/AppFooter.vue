<template>
  <footer class="border-t border-border-light py-6">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-text-muted">
      <a href="/" class="flex items-center gap-2 hover:text-text-primary transition-colors">
        <div class="w-6 h-6 rounded-md bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center">
          <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
        </div>
        <span class="font-medium text-text-secondary">褚成志的在线视频下载器</span>
      </a>
      <p class="text-center">仅供学习交流，请尊重版权，勿用于商业用途</p>
      <p>&copy; {{ new Date().getFullYear() }}</p>
    </div>
  </footer>
</template>
