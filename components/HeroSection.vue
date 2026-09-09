<template>
  <section class="relative overflow-hidden border-b border-border/70">
    <div class="hero-grid absolute inset-0" aria-hidden="true" />
    <div class="glow-primary absolute -top-32 left-1/4 size-96" aria-hidden="true" />
    <div class="glow-accent absolute -top-24 right-1/4 size-80" aria-hidden="true" />

    <div class="relative mx-auto max-w-6xl px-4 sm:px-6 pt-20 pb-16 sm:pt-28 sm:pb-20 text-center">
      <div class="float-in inline-flex items-center gap-2 rounded-full border border-border bg-card/80 px-3.5 py-1.5 text-[12.5px] text-muted">
        <span class="size-1.5 rounded-full bg-primary pulse-dot" />
        每日自动同步 GitHub 数据
      </div>

      <h1 class="float-in mt-6 text-4xl sm:text-6xl font-extrabold tracking-tight leading-[1.08]" style="animation-delay: 60ms">
        Discover the
        <span class="text-gradient">Agent Ecosystem</span>
        <br class="hidden sm:block" />
        Skills · Frameworks · Tools
      </h1>

      <p class="float-in mx-auto mt-5 max-w-2xl text-[15px] sm:text-base leading-relaxed text-muted" style="animation-delay: 120ms">
        一个开放、社区驱动的 Agent 生态目录。
        收录官方与社区最好的 Skills 与 Agent 框架,帮助你在碎片化的生态里
        快速找到真正干活的能力模块与智能体。
      </p>

      <div class="float-in mt-8 flex flex-wrap items-center justify-center gap-3" style="animation-delay: 180ms">
        <NuxtLink
          to="/browse"
          class="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-[14px] font-semibold text-background transition-all hover:bg-primary-strong hover:shadow-[0_0_24px_rgba(66,211,146,0.35)]"
        >
          浏览全部项目
          <svg viewBox="0 0 16 16" class="size-4" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </NuxtLink>
        <NuxtLink
          to="/submit"
          class="inline-flex items-center rounded-lg border border-border-strong bg-card px-5 py-2.5 text-[14px] text-foreground transition-colors hover:border-primary/40 hover:text-primary"
        >
          Contributing
        </NuxtLink>
      </div>

      <dl class="float-in mx-auto mt-14 grid max-w-2xl grid-cols-2 gap-px overflow-hidden rounded-xl border border-border bg-border/60 sm:grid-cols-4" style="animation-delay: 240ms">
        <div v-for="s in statItems" :key="s.label" class="bg-surface px-4 py-4">
          <dd class="font-mono text-xl font-semibold text-foreground tabular-nums">{{ s.value }}</dd>
          <dt class="mt-1 text-[11.5px] text-faint">{{ s.label }}</dt>
        </div>
      </dl>
    </div>
  </section>
</template>

<script setup lang="ts">
const { data: stats } = await useFetch('/api/stats', { default: () => ({}) })

const statItems = computed(() => [
  { label: '收录项目', value: String(stats.value.totalProjects ?? '—') },
  { label: '覆盖仓库', value: String(stats.value.totalRepos ?? '—') },
  { label: '分类', value: String(stats.value.totalCategories ?? '—') },
  { label: '生态 Stars', value: formatStars(stats.value.totalStars) },
])
</script>
