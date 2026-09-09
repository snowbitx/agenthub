<template>
  <div class="min-h-screen flex flex-col">
    <a
      href="#main"
      class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-2 focus:left-2 focus:bg-card focus:px-3 focus:py-1.5 focus:rounded-lg focus:text-sm"
    >跳到主要内容</a>
    <SiteHeader />
    <main id="main" class="flex-1">
      <NuxtPage />
    </main>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
useHead({
  meta: [
    { name: 'description', content: 'SkillsHub — 发现、学习并使用最好的 Agent Skills。聚合 Anthropic 官方与社区技能,自动同步 GitHub star 与活跃度。' },
    { name: 'theme-color', content: '#09090b' },
  ],
  htmlAttrs: { lang: 'zh-CN' },
})
</script>
