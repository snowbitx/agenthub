<template>
  <NuxtLink
    :to="`/p/${project.slug}`"
    class="group relative flex flex-col rounded-xl border border-border bg-card p-4 transition-all duration-200 hover:border-border-strong hover:bg-card-hover hover:-translate-y-0.5"
  >
    <div class="flex items-start justify-between gap-3">
      <div class="flex items-center gap-2.5 min-w-0">
        <span
          class="grid size-9 shrink-0 place-items-center rounded-lg text-base"
          :class="project.kind === 'collection' ? 'bg-accent-soft' : 'bg-primary-soft'"
        >
          {{ project.kind === 'collection' ? '📦' : '⚡' }}
        </span>
        <div class="min-w-0">
          <h3 class="truncate text-[14px] font-semibold text-foreground group-hover:text-primary transition-colors font-mono">
            {{ project.name }}
          </h3>
          <p class="text-[11px] text-faint truncate">
            {{ project.author }}<template v-if="project.sourcePath"> / {{ project.sourcePath }}</template>
          </p>
        </div>
      </div>
      <span
        v-if="project.stars != null"
        class="shrink-0 inline-flex items-center gap-1 rounded-md border border-border bg-surface px-2 py-0.5 text-[11px] font-mono text-muted"
        title="GitHub stars"
      >
        <svg viewBox="0 0 16 16" class="size-3 text-warn" fill="currentColor" aria-hidden="true"><path d="M8 .8l2.1 4.4 4.9.7-3.5 3.4.8 4.9L8 11.9l-4.3 2.3.8-4.9L1 5.9l4.9-.7L8 .8z"/></svg>
        {{ formatStars(project.stars) }}
      </span>
    </div>

    <p class="mt-3 text-[13px] leading-relaxed text-muted line-clamp-2">{{ project.description }}</p>

    <div class="mt-auto pt-3 flex items-center justify-between gap-2">
      <div class="flex flex-wrap items-center gap-1.5 min-w-0">
        <span class="inline-flex items-center rounded-md bg-white/[0.04] border border-border px-1.5 py-0.5 text-[10.5px] text-muted">
          {{ category?.icon }} {{ category?.label }}
        </span>
        <span
          v-for="t in project.tags.slice(0, 2)"
          :key="t"
          class="hidden sm:inline-flex items-center rounded-md px-1.5 py-0.5 text-[10.5px] text-faint font-mono"
        >#{{ t }}</span>
      </div>
      <span
        class="shrink-0 inline-flex items-center rounded-md px-1.5 py-0.5 text-[10.5px]"
        :class="health.cls"
      >{{ health.label }}</span>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { Project } from '~/shared/schema'
import { categoryMap } from '~/data/categories'

const props = defineProps<{ project: Project }>()
const category = computed(() => categoryMap[props.project.category])
const health = computed(() => healthLabel(props.project.pushedAt))
</script>
