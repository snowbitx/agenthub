<template>
  <footer class="border-t border-border/70 mt-20">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 py-10">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div>
          <div class="flex items-center gap-2">
            <span class="grid size-6 place-items-center rounded-md bg-primary-soft border border-primary/25 text-primary text-xs">✦</span>
            <span class="font-semibold text-sm">AgentHub</span>
          </div>
          <p class="mt-2 text-[13px] text-faint max-w-sm">
            Discover the Agent Skills Ecosystem — 数据每日自动同步自 GitHub,收录标准:SKILL.md 格式完整可运行。
          </p>
        </div>
        <div class="flex items-center gap-5 text-[13px] text-muted">
          <NuxtLink to="/submit" class="hover:text-foreground transition-colors">提交 Skill</NuxtLink>
          <NuxtLink to="/about" class="hover:text-foreground transition-colors">关于</NuxtLink>
          <a href="/api/projects" class="hover:text-foreground transition-colors font-mono text-xs">API</a>
        </div>
      </div>
      <div class="mt-8 pt-5 border-t border-border/60 flex flex-col sm:flex-row justify-between gap-2 text-xs text-faint">
        <span>© 2026 AgentHub · made with <span class="text-primary">❤</span> for the agent community</span>
        <span class="font-mono">data synced {{ stats.lastSyncedAt ? formatDate(stats.lastSyncedAt) : '—' }}</span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const { data: stats } = await useFetch('/api/stats', { default: () => ({}) })
</script>
