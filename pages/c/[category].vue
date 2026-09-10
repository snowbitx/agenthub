<script setup lang="ts">
import { categories, categoryMap } from '~/data/categories'

const route = useRoute()
const category = route.params.category as string
const cat = categoryMap[category]
if (!cat) throw createError({ statusCode: 404, statusMessage: 'Category Not Found', fatal: true })

const { data } = await useFetch('/api/projects', {
  query: { category, sort: 'stars' },
})
const projects = computed(() => data.value?.projects ?? [])

const repoStars = computed(() => {
  const m = new Map<string, number>()
  for (const p of projects.value) {
    if (p.stars != null) m.set(p.repo, Math.max(m.get(p.repo) ?? 0, p.stars))
  }
  return [...m.values()].sort((a, b) => b - a)
})

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

useHead({
  title: () => `${cat.label} — AI Agent 生态目录`,
  link: [{ rel: 'canonical', href: `${siteUrl}/c/${category}` }],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        name: `${cat.label} · AgentHub`,
        description: cat.description,
        url: `${siteUrl}/c/${category}`,
        numberOfItems: projects.value.length,
      }),
    },
  ],
})
useSeoMeta({
  description: `${cat.description}。${projects.value.length} 个精选项目,GitHub star 与维护状态每日同步。`,
  ogTitle: `${cat.label} · AgentHub`,
  ogDescription: cat.description,
})
</script>

<template>
  <div class="mx-auto max-w-6xl px-4 sm:px-6 py-10 sm:py-14">
    <div class="flex items-center gap-2 text-[12.5px] text-faint">
      <NuxtLink to="/" class="hover:text-muted transition-colors">首页</NuxtLink>
      <span>/</span>
      <span class="text-muted">{{ cat.label }}</span>
    </div>

    <header class="mt-4 rounded-2xl border border-border bg-card p-6 sm:p-8 relative overflow-hidden">
      <div class="glow-primary absolute -top-20 -right-10 size-64" aria-hidden="true" />
      <div class="relative flex items-start gap-4">
        <span class="grid size-12 place-items-center rounded-xl bg-primary-soft border border-primary/20 text-2xl">{{ cat.icon }}</span>
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold tracking-tight">{{ cat.label }}</h1>
          <p class="mt-1.5 max-w-2xl text-[13.5px] leading-relaxed text-muted">{{ cat.description }}</p>
          <p class="mt-3 font-mono text-[12px] text-faint">
            {{ projects.length }} 个项目
            <template v-if="repoStars.length"> · 头部仓库 ★{{ formatStars(repoStars[0]) }}</template>
          </p>
        </div>
      </div>
    </header>

    <div v-if="projects.length" class="mt-6 grid gap-3.5 sm:grid-cols-2 lg:grid-cols-3">
      <ProjectCard v-for="p in projects" :key="p.slug" :project="p" />
    </div>
    <div v-else class="mt-10 rounded-xl border border-dashed border-border py-16 text-center text-muted">
      该分类下还没有收录项目,欢迎
      <NuxtLink to="/submit" class="text-primary hover:underline">提交</NuxtLink>。
    </div>

    <div class="mt-10 flex flex-wrap gap-2">
      <NuxtLink v-for="(c, i) in categories.filter((x) => x.id !== cat.id)" :key="c.id" :to="`/c/${c.id}`" class="rounded-full border border-border bg-card px-3.5 py-1.5 text-[12.5px] text-muted hover:text-foreground transition-colors">
        {{ i === 0 ? '其他分类：' : '' }}{{ c.icon }} {{ c.label }}
      </NuxtLink>
    </div>
  </div>
</template>
