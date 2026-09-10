<script setup lang="ts">
import { categories } from '~/data/categories'

const { data } = await useFetch('/api/projects?sort=stars')
const all = computed(() => data.value?.projects ?? [])

const featured = computed(() => all.value.filter((p) => p.featured).slice(0, 8))
const newest = computed(() => [...all.value].sort((a, b) => (b.addedAt > a.addedAt ? 1 : -1)).slice(0, 4))

const config = useRuntimeConfig()
const siteUrl = config.public.siteUrl

useHead({
  title: 'AI Agent 生态目录',
  link: [{ rel: 'canonical', href: siteUrl }],
})
useSeoMeta({
  description: '发现 AI Agent 生态最好的项目:Agent 框架、编程智能体、浏览器 Agent 与 Agent Skills。150+ 精选项目,GitHub 数据每日同步。',
  ogTitle: 'AgentHub — Discover the AI Agent Ecosystem',
  ogDescription: '开放、社区驱动的 AI Agent 生态目录:Frameworks · Coding Agents · Skills',
  ogUrl: siteUrl,
})
</script>

<template>
  <div>
    <HeroSection />
    <FeatureSection />

    <section class="mx-auto max-w-6xl px-4 sm:px-6">
      <div class="flex items-end justify-between">
        <div>
          <h2 class="text-xl sm:text-2xl font-bold tracking-tight">精选项目</h2>
          <p class="mt-1 text-[13.5px] text-muted">由社区维护者人工筛选的高质量入口</p>
        </div>
        <NuxtLink to="/browse" class="text-[13px] text-muted hover:text-primary transition-colors">查看全部 →</NuxtLink>
      </div>
      <div class="mt-6 grid gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
        <ProjectCard v-for="p in featured" :key="p.slug" :project="p" class="float-in" />
      </div>
    </section>

    <section class="mx-auto max-w-6xl px-4 sm:px-6 mt-16">
      <h2 class="text-xl sm:text-2xl font-bold tracking-tight">按分类探索</h2>
      <p class="mt-1 text-[13.5px] text-muted">从官方示例到社区合集,按场景找到需要的能力</p>
      <div class="mt-6 grid gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
        <NuxtLink
          v-for="c in categories"
          :key="c.id"
          :to="`/c/${c.id}`"
          class="group rounded-xl border border-border bg-card p-5 transition-all hover:border-border-strong hover:bg-card-hover hover:-translate-y-0.5"
        >
          <span class="text-xl">{{ c.icon }}</span>
          <h3 class="mt-3 text-[14.5px] font-semibold group-hover:text-primary transition-colors">{{ c.label }}</h3>
          <p class="mt-1 text-[12.5px] leading-relaxed text-muted line-clamp-2">{{ c.description }}</p>
          <span class="mt-3 inline-block font-mono text-[11px] text-faint">
            {{ all.filter((p) => p.category === c.id).length }} 个项目
          </span>
        </NuxtLink>
      </div>
    </section>

    <section class="mx-auto max-w-6xl px-4 sm:px-6 mt-16">
      <div class="flex items-end justify-between">
        <div>
          <h2 class="text-xl sm:text-2xl font-bold tracking-tight">最新收录</h2>
          <p class="mt-1 text-[13.5px] text-muted">刚刚加入目录的项目</p>
        </div>
        <NuxtLink to="/browse?sort=newest" class="text-[13px] text-muted hover:text-primary transition-colors">更多 →</NuxtLink>
      </div>
      <div class="mt-6 grid gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
        <ProjectCard v-for="p in newest" :key="p.slug" :project="p" />
      </div>
    </section>

    <ContributeCta />
  </div>
</template>
