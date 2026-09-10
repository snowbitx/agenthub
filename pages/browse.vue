<script setup lang="ts">
import { categories, categoryMap } from '~/data/categories'

interface ExternalRepo {
  slug: string
  name: string
  description: string
  author: string
  stars: number
  pushedAt?: string
  language?: string
  url: string
}

const route = useRoute()

const activeCategory = computed(() => {
  const c = route.params.category
  return typeof c === 'string' && categoryMap[c] ? c : ''
})

const q = ref(typeof route.query.q === 'string' ? route.query.q : '')
const sort = ref(typeof route.query.sort === 'string' ? route.query.sort : 'stars')
const kind = ref(typeof route.query.kind === 'string' ? route.query.kind : '')

const debouncedQ = ref(q.value)
let timer: ReturnType<typeof setTimeout> | undefined
watch(q, (v) => {
  clearTimeout(timer)
  timer = setTimeout(() => (debouncedQ.value = v), 200)
})

const { data } = await useFetch('/api/projects', {  query: computed(() => ({
    category: activeCategory.value || undefined,
    q: debouncedQ.value || undefined,
    sort: sort.value,
    kind: kind.value || undefined,
  })),
})
const projects = computed(() => data.value?.projects ?? [])

// 站内无结果时,自动搜 GitHub 上的相关仓库
const external = ref<{ repos: ExternalRepo[] } | null>(null)
const externalPending = ref(false)
const externalError = ref(false)
let lastExternalQ = ''
watch(
  [debouncedQ, data] as const,
  async ([v, d]) => {
    if (!v) {
      lastExternalQ = ''
      external.value = null
      externalError.value = false
      return
    }
    if (!d) return // 等站内结果返回后再判断是否为空
    if (projects.value.length) {
      external.value = null
      externalError.value = false
      return
    }
    if (v === lastExternalQ) return
    lastExternalQ = v
    externalPending.value = true
    externalError.value = false
    try {
      external.value = await $fetch('/api/search-external', { query: { q: v } })
    } catch {
      externalError.value = true
    } finally {
      externalPending.value = false
    }
  },
  { immediate: true },
)

const sortOptions = [
  { value: 'stars', label: '最多 Star' },
  { value: 'newest', label: '最新收录' },
  { value: 'updated', label: '最近更新' },
  { value: 'name', label: '名称 A-Z' },
]

const header = computed(() =>
  activeCategory.value ? categoryMap[activeCategory.value].label : '全部项目',
)

watch(
  [debouncedQ, sort, kind, activeCategory],
  () => {
    const query: Record<string, string> = {}
    if (q.value) query.q = q.value
    if (sort.value !== 'stars') query.sort = sort.value
    if (kind.value) query.kind = kind.value
    useRouter().replace({ query })
  },
  { deep: true },
)

useHead({ title: () => (activeCategory.value ? categoryMap[activeCategory.value].label : '浏览全部') })
</script>

<template>
  <div class="mx-auto max-w-6xl px-4 sm:px-6 py-10 sm:py-14">
    <div class="flex items-center gap-2 text-[12.5px] text-faint">
      <NuxtLink to="/" class="hover:text-muted transition-colors">首页</NuxtLink>
      <span>/</span>
      <span class="text-muted">{{ header }}</span>
    </div>

    <div class="mt-4 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight">
          <span v-if="activeCategory" class="mr-2">{{ categoryMap[activeCategory].icon }}</span>{{ header }}
        </h1>
        <p class="mt-1.5 text-[13.5px] text-muted">
          {{ activeCategory ? categoryMap[activeCategory].description : '按分类、类型与排序条件筛选 Skills 与 Agent 框架' }}
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2.5">
        <label class="relative">
          <svg viewBox="0 0 24 24" class="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-faint" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5" stroke-linecap="round"/></svg>
          <input
            v-model="q"
            type="search"
            placeholder="搜索名称、描述、标签…"
            class="w-full sm:w-64 rounded-lg border border-border bg-card py-2 pl-9 pr-3 text-[13.5px] placeholder:text-faint outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/15 transition"
          />
        </label>
        <select
          v-model="sort"
          class="rounded-lg border border-border bg-card px-3 py-2 text-[13px] text-muted outline-none focus:border-primary/50 cursor-pointer"
          aria-label="排序方式"
        >
          <option v-for="o in sortOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
        </select>
      </div>
    </div>

    <div class="mt-6 flex flex-wrap items-center gap-2">
      <NuxtLink
        to="/browse"
        class="rounded-full border px-3.5 py-1.5 text-[12.5px] transition-colors"
        :class="!activeCategory ? 'border-primary/40 bg-primary-soft text-primary' : 'border-border bg-card text-muted hover:text-foreground'"
      >
        全部
      </NuxtLink>
      <NuxtLink
        v-for="c in categories"
        :key="c.id"
        :to="`/c/${c.id}`"
        class="rounded-full border px-3.5 py-1.5 text-[12.5px] transition-colors"
        :class="activeCategory === c.id ? 'border-primary/40 bg-primary-soft text-primary' : 'border-border bg-card text-muted hover:text-foreground'"
      >
        {{ c.icon }} {{ c.label }}
      </NuxtLink>
      <span class="mx-1 hidden sm:block h-4 w-px bg-border" />
      <button
        v-for="k in [{ v: '', l: '全部类型' }, { v: 'agent', l: '🤖 Agent' }, { v: 'skill', l: '⚡ Skill' }, { v: 'collection', l: '📦 合集' }]"
        :key="k.v"
        class="rounded-full border px-3 py-1.5 text-[12.5px] transition-colors"
        :class="kind === k.v ? 'border-accent/40 bg-accent-soft text-[#8fa2ff]' : 'border-border bg-card text-muted hover:text-foreground'"
        @click="kind = k.v"
      >
        {{ k.l }}
      </button>
    </div>

    <p class="mt-6 text-[12.5px] text-faint font-mono">
      {{ projects.length }} 个结果
      <template v-if="debouncedQ"> · “{{ debouncedQ }}”</template>
    </p>

    <div v-if="projects.length" class="mt-4 grid gap-3.5 sm:grid-cols-2 lg:grid-cols-3">
      <ProjectCard v-for="p in projects" :key="p.slug" :project="p" />
    </div>
    <div v-else class="mt-6">
      <div class="rounded-xl border border-dashed border-border py-10 text-center">
        <p class="text-3xl">🔍</p>
        <p class="mt-3 text-[14px] text-muted">站内没有匹配「{{ debouncedQ }}」的项目</p>
        <p class="mt-1 text-[12.5px] text-faint">以下是从 GitHub 上找到的相关仓库,或试试换个关键词</p>
        <div class="mt-4 flex items-center justify-center gap-2">
          <button class="rounded-lg border border-border-strong px-4 py-1.5 text-[13px] text-muted hover:text-foreground" @click="q = ''; kind = ''">
            清空筛选
          </button>
          <a
            :href="`https://github.com/search?q=${encodeURIComponent(debouncedQ + ' skill')}&type=repositories`"
            target="_blank"
            rel="noopener"
            class="rounded-lg border border-border-strong px-4 py-1.5 text-[13px] text-muted hover:text-foreground"
          >
            在 GitHub 打开完整搜索 ↗
          </a>
        </div>
      </div>

      <div v-if="externalPending" class="mt-8 text-center text-[13px] text-faint">
        <span class="inline-block animate-pulse">正在搜索 GitHub 上的相关仓库…</span>
      </div>
      <p v-else-if="externalError" class="mt-8 text-center text-[12.5px] text-faint">GitHub 搜索暂时不可用(限流),稍后再试。</p>

      <template v-if="external?.repos?.length">
        <h2 class="mt-8 flex items-center gap-2 text-[14px] font-semibold text-muted">
          <svg viewBox="0 0 16 16" class="size-3.5" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>
          GitHub 上的相关仓库
          <span class="font-mono text-[11px] font-normal text-faint">{{ external.repos.length }} 个结果</span>
        </h2>
        <div class="mt-4 grid gap-3.5 sm:grid-cols-2 lg:grid-cols-3">
          <a
            v-for="r in external.repos"
            :key="r.slug"
            :href="r.url"
            target="_blank"
            rel="noopener"
            class="group flex flex-col rounded-xl border border-border bg-card p-4 transition-all duration-200 hover:border-border-strong hover:bg-card-hover hover:-translate-y-0.5"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <h3 class="truncate text-[14px] font-semibold text-foreground group-hover:text-primary transition-colors font-mono">
                  {{ r.slug }}
                </h3>
                <p class="text-[11px] text-faint truncate">
                  {{ r.author }}<template v-if="r.language"> · {{ r.language }}</template>
                </p>
              </div>
              <span class="shrink-0 inline-flex items-center gap-1 rounded-md border border-border bg-surface px-2 py-0.5 text-[11px] font-mono text-muted" title="GitHub stars">
                <svg viewBox="0 0 16 16" class="size-3 text-warn" fill="currentColor" aria-hidden="true"><path d="M8 .8l2.1 4.4 4.9.7-3.5 3.4.8 4.9L8 11.9l-4.3 2.3.8-4.9L1 5.9l4.9-.7L8 .8z"/></svg>
                {{ formatStars(r.stars) }}
              </span>
            </div>
            <p class="mt-3 text-[13px] leading-relaxed text-muted line-clamp-2">{{ r.description || '暂无描述' }}</p>
            <div class="mt-auto pt-3 flex items-center justify-between">
              <span class="inline-flex items-center rounded-md bg-white/[0.04] border border-border px-1.5 py-0.5 text-[10.5px] text-muted">未收录</span>
              <span class="text-[10.5px] text-faint">在 GitHub 打开 ↗</span>
            </div>
          </a>
        </div>
        <p class="mt-4 text-[12px] text-faint">
          觉得哪个值得收录?
          <NuxtLink to="/submit" class="text-primary hover:underline">提交给我们 →</NuxtLink>
        </p>
      </template>
    </div>
  </div>
</template>
