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

      <form class="float-in mx-auto mt-8 flex max-w-xl items-center gap-2" style="animation-delay: 160ms" @submit.prevent="goSearch">
        <label class="relative flex-1">
          <svg viewBox="0 0 24 24" class="absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-faint" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5" stroke-linecap="round"/></svg>
          <input
            v-model="searchQ"
            type="search"
            placeholder="搜索 Skill,比如 packet-capture…"
            class="w-full rounded-lg border border-border bg-card py-2.5 pl-10 pr-3 text-[14px] placeholder:text-faint outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/15 transition"
          />
        </label>
        <button
          type="submit"
          class="shrink-0 rounded-lg bg-primary px-4 py-2.5 text-[13.5px] font-semibold text-background transition-all hover:bg-primary-strong hover:shadow-[0_0_24px_rgba(66,211,146,0.35)]"
        >
          搜索
        </button>
      </form>
      <div class="float-in mt-3 flex flex-wrap items-center justify-center gap-1.5 text-[11.5px] text-faint" style="animation-delay: 200ms">
        热门:
        <NuxtLink v-for="t in ['packet-capture', 'pdf', 'code-review', 'mcp']" :key="t" :to="`/browse?q=${t}`" class="rounded-full border border-border bg-card/70 px-2.5 py-0.5 font-mono text-[11px] text-muted hover:border-primary/40 hover:text-primary transition-colors">
          {{ t }}
        </NuxtLink>
      </div>

      <div class="float-in mt-8 flex flex-wrap items-center justify-center gap-3" style="animation-delay: 240ms">
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

const searchQ = ref('')
const goSearch = () => {
  const q = searchQ.value.trim()
  if (q) navigateTo({ path: '/browse', query: { q } })
}

const statItems = computed(() => [
  { label: '收录项目', value: String(stats.value.totalProjects ?? '—') },
  { label: '覆盖仓库', value: String(stats.value.totalRepos ?? '—') },
  { label: '分类', value: String(stats.value.totalCategories ?? '—') },
  { label: '生态 Stars', value: formatStars(stats.value.totalStars) },
])
</script>
