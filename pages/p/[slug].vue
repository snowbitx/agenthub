<script setup lang="ts">
import { categoryMap } from '~/data/categories'
import type { Project } from '~/shared/schema'

const route = useRoute()
const slug = route.params.slug as string

const { data: project, error } = await useFetch<Project>(`/api/projects/${slug}`)
if (error.value || !project.value) {
  throw createError({ statusCode: 404, statusMessage: 'Project Not Found', fatal: true })
}

const cat = computed(() => categoryMap[project.value!.category])
const health = computed(() => healthLabel(project.value!.pushedAt))
const isCollection = computed(() => project.value!.kind === 'collection')

const installCmd = computed(() =>
  project.value!.sourcePath
    ? `npx skills add ${project.value!.repo.replace('https://github.com/', '')}/${project.value!.sourcePath}`
    : `npx skills add ${project.value!.repo.replace('https://github.com/', '')}`,
)

const copied = ref(false)
async function copyCmd() {
  try {
    await navigator.clipboard.writeText(installCmd.value)
    copied.value = true
    setTimeout(() => (copied.value = false), 1800)
  } catch {}
}

const { data: relatedData } = await useFetch('/api/projects', {
  query: { category: project.value!.category, sort: 'stars' },
})
const related = computed(() =>
  (relatedData.value?.projects ?? [])
    .filter((p: Project) => p.slug !== slug)
    .slice(0, 3),
)

useHead({ title: project.value.name })
useSeoMeta({
  description: project.value.description,
  ogTitle: `${project.value.name} · SkillsHub`,
  ogDescription: project.value.description,
})
</script>

<template>
  <div v-if="project" class="mx-auto max-w-6xl px-4 sm:px-6 py-10 sm:py-14">
    <div class="flex items-center gap-2 text-[12.5px] text-faint">
      <NuxtLink to="/" class="hover:text-muted transition-colors">首页</NuxtLink>
      <span>/</span>
      <NuxtLink :to="`/c/${project.category}`" class="hover:text-muted transition-colors">{{ cat?.label }}</NuxtLink>
      <span>/</span>
      <span class="text-muted font-mono">{{ project.name }}</span>
    </div>

    <div class="mt-5 grid gap-6 lg:grid-cols-[1fr_320px]">
      <div>
        <header class="rounded-2xl border border-border bg-card p-6 sm:p-7">
          <div class="flex items-start gap-4">
            <span
              class="grid size-12 shrink-0 place-items-center rounded-xl text-2xl"
              :class="isCollection ? 'bg-accent-soft' : 'bg-primary-soft border border-primary/20'"
            >{{ isCollection ? '📦' : '⚡' }}</span>
            <div class="min-w-0 flex-1">
              <div class="flex flex-wrap items-center gap-2">
                <h1 class="text-xl sm:text-2xl font-bold tracking-tight font-mono">{{ project.name }}</h1>
                <span class="rounded-md bg-white/[0.04] border border-border px-1.5 py-0.5 text-[10.5px] text-muted">{{ isCollection ? '技能合集' : '技能' }}</span>
                <span v-if="project.featured" class="rounded-md bg-warn/10 border border-warn/30 px-1.5 py-0.5 text-[10.5px] text-warn">精选</span>
              </div>
              <p class="mt-1 text-[12.5px] text-faint font-mono">by {{ project.author }}</p>
            </div>
          </div>
          <p class="mt-5 text-[14.5px] leading-relaxed text-muted">{{ project.description }}</p>
          <div class="mt-4 flex flex-wrap gap-1.5">
            <span v-for="t in project.tags" :key="t" class="rounded-md bg-white/[0.04] px-2 py-0.5 text-[11px] font-mono text-faint">#{{ t }}</span>
          </div>
        </header>

        <section class="mt-5 rounded-2xl border border-border bg-card p-6 sm:p-7">
          <h2 class="text-[15px] font-semibold">安装方式</h2>
          <p class="mt-1.5 text-[13px] text-muted">在 Claude Code 或支持 Agent Skills 的运行时中执行:</p>
          <div class="mt-3 flex items-stretch overflow-hidden rounded-lg border border-border bg-surface font-mono text-[12.5px]">
            <code class="flex-1 overflow-x-auto px-3.5 py-2.5 text-primary whitespace-nowrap">$ {{ installCmd }}</code>
            <button
              class="shrink-0 border-l border-border px-3 text-[11.5px] text-muted transition-colors hover:bg-white/[0.05] hover:text-foreground"
              @click="copyCmd"
            >
              {{ copied ? '✓ 已复制' : '复制' }}
            </button>
          </div>
          <p class="mt-3 text-[12px] leading-relaxed text-faint">
            Skill 即一个包含 SKILL.md 的文件夹:模型读取其元数据后按需加载指令与脚本。你也可以直接把仓库克隆到
            <code class="font-mono">~/.claude/skills/</code> 目录使用。
          </p>
        </section>

        <section class="mt-5 rounded-2xl border border-border bg-card p-6 sm:p-7">
          <h2 class="text-[15px] font-semibold">收录信息</h2>
          <dl class="mt-4 grid gap-x-8 gap-y-3 sm:grid-cols-2 text-[13px]">
            <div class="flex justify-between sm:justify-start sm:gap-3">
              <dt class="text-faint">来源仓库</dt>
              <dd><a :href="project.repo" target="_blank" rel="noopener" class="font-mono text-[12.5px] text-primary hover:underline">{{ project.repo.replace('https://github.com/', '') }}</a></dd>
            </div>
            <div class="flex justify-between sm:justify-start sm:gap-3">
              <dt class="text-faint">仓库内路径</dt>
              <dd class="font-mono text-[12.5px]">{{ project.sourcePath ?? '/' }}</dd>
            </div>
            <div class="flex justify-between sm:justify-start sm:gap-3">
              <dt class="text-faint">收录时间</dt>
              <dd>{{ formatDate(project.addedAt) }}</dd>
            </div>
            <div class="flex justify-between sm:justify-start sm:gap-3">
              <dt class="text-faint">最近同步</dt>
              <dd>{{ relativeDays(project.lastSyncedAt) }}</dd>
            </div>
          </dl>
        </section>
      </div>

      <aside class="space-y-4 lg:sticky lg:top-20 lg:self-start">
        <div class="rounded-2xl border border-border bg-card p-5">
          <div class="grid grid-cols-2 gap-3 text-center">
            <div class="rounded-xl bg-surface border border-border/60 p-3.5">
              <p class="font-mono text-lg font-semibold text-foreground">{{ formatStars(project.stars) }}</p>
              <p class="mt-0.5 text-[11px] text-faint">Stars</p>
            </div>
            <div class="rounded-xl bg-surface border border-border/60 p-3.5">
              <p class="font-mono text-lg font-semibold text-foreground">{{ project.forks != null ? formatStars(project.forks) : '—' }}</p>
              <p class="mt-0.5 text-[11px] text-faint">Forks</p>
            </div>
          </div>
          <div class="mt-3 flex items-center justify-between rounded-xl bg-surface border border-border/60 px-3.5 py-3">
            <span class="text-[12px] text-muted">维护状态</span>
            <span class="rounded-md px-2 py-0.5 text-[11px]" :class="health.cls">{{ health.label }}</span>
          </div>
          <div class="mt-3 rounded-xl bg-surface border border-border/60 px-3.5 py-3">
            <div class="flex items-center justify-between text-[12px]">
              <span class="text-muted">最近推送</span>
              <span class="font-mono text-faint">{{ formatDate(project.pushedAt) }}</span>
            </div>
            <div class="mt-2 flex items-center justify-between text-[12px]">
              <span class="text-muted">仓库创建</span>
              <span class="font-mono text-faint">{{ formatDate(project.createdAt) }}</span>
            </div>
          </div>
          <a
            :href="project.repo"
            target="_blank"
            rel="noopener"
            class="mt-4 flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-[13.5px] font-semibold text-background hover:bg-primary-strong transition-colors"
          >
            <svg viewBox="0 0 16 16" class="size-4" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>
            在 GitHub 查看
          </a>
        </div>

        <div v-if="related.length" class="rounded-2xl border border-border bg-card p-5">
          <h3 class="text-[13.5px] font-semibold text-muted">同分类项目</h3>
          <div class="mt-3 space-y-2">
            <NuxtLink
              v-for="r in related"
              :key="r.slug"
              :to="`/p/${r.slug}`"
              class="flex items-center justify-between gap-2 rounded-lg border border-border/60 bg-surface px-3 py-2.5 text-[12.5px] transition-colors hover:border-border-strong"
            >
              <span class="truncate font-mono">{{ r.name }}</span>
              <span class="shrink-0 font-mono text-[11px] text-faint">★{{ formatStars(r.stars) }}</span>
            </NuxtLink>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>
