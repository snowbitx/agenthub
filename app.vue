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
import { THEME_INIT_SCRIPT } from '~/composables/useTheme'

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

useHead({
  meta: [
    { name: 'description', content: 'AgentHub — 发现 AI Agent 生态最好的项目:Agent 框架、编程智能体、浏览器 Agent 与 Agent Skills。收录 150+ 项目,GitHub star 与活跃度每日自动同步。' },
    { name: 'theme-color', content: '#09090b' },
    { name: 'keywords', content: 'AI Agent, Agent 框架, Agent Skills, Claude Skills, coding agent, browser agent, LangChain, MCP, 智能体, Agent 目录' },
  ],
  script: [
    // 阻塞式内联脚本,在水合前把主题 class 写到 <html>,避免亮色用户刷新闪暗色
    { innerHTML: THEME_INIT_SCRIPT },
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        name: 'AgentHub',
        alternateName: 'AgentHub 生态目录',
        url: siteUrl,
        description: 'Discover the AI Agent Ecosystem — frameworks, coding agents, browser agents and Agent Skills, with GitHub metrics synced daily.',
      }),
    },
  ],
  link: [{ rel: 'canonical', href: siteUrl }],
  htmlAttrs: { lang: 'zh-CN' },
})

useSeoMeta({
  ogTitle: 'AgentHub — Discover the AI Agent Ecosystem',
  ogDescription: '开放、社区驱动的 AI Agent 生态目录:框架、编程智能体、Agent Skills,150+ 项目每日同步 GitHub 数据。',
  ogType: 'website',
  ogSiteName: 'AgentHub',
  twitterCard: 'summary_large_image',
  twitterTitle: 'AgentHub — Discover the AI Agent Ecosystem',
  twitterDescription: '150+ AI Agent 框架与 Skills,GitHub 数据每日同步。',
})
</script>
