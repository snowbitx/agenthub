<script setup lang="ts">
import { categories, categoryMap } from '~/data/categories'

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

const { data } = await useFetch('/api/projects', {
  query: computed(() => ({
    category: activeCategory.value || undefined,
    q: debouncedQ.value || undefined,
    sort: sort.value,
    kind: kind.value || undefined,
  })),
})
const projects = computed(() => data.value?.projects ?? [])

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
    <div v-else class="mt-10 rounded-xl border border-dashed border-border py-16 text-center">
      <p class="text-3xl">🔍</p>
      <p class="mt-3 text-[14px] text-muted">没有匹配的项目</p>
      <p class="mt-1 text-[12.5px] text-faint">换个关键词,或者清空筛选条件试试</p>
      <button class="mt-4 rounded-lg border border-border-strong px-4 py-1.5 text-[13px] text-muted hover:text-foreground" @click="q = ''; kind = ''">
        清空筛选
      </button>
    </div>
  </div>
</template>
