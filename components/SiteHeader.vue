<template>
  <header class="site-header sticky top-0 z-40 border-b border-border/70">
    <div class="mx-auto max-w-6xl px-4 sm:px-6">
      <div class="flex h-14 items-center justify-between gap-4">
        <NuxtLink to="/" class="flex items-center gap-2.5 shrink-0 group">
          <span class="grid size-7 place-items-center rounded-lg bg-primary-soft border border-primary/25 text-primary text-sm">✦</span>
          <span class="font-semibold tracking-tight text-[15px] group-hover:text-primary transition-colors">AgentHub</span>
          <span class="hidden sm:inline text-[10px] font-mono text-faint border border-border rounded px-1.5 py-0.5 mt-0.5">beta</span>
        </NuxtLink>

        <nav class="hidden md:flex items-center gap-1">
          <NuxtLink
            v-for="c in categories"
            :key="c.id"
            :to="`/c/${c.id}`"
            class="px-3 py-1.5 rounded-lg text-[13px] text-muted hover:text-foreground hover:bg-card transition-colors"
          >
            {{ c.label }}
          </NuxtLink>
        </nav>

        <div class="flex items-center gap-2">
          <NuxtLink
            to="/submit"
            class="hidden sm:inline-flex items-center gap-1.5 rounded-lg border border-border bg-card px-3 py-1.5 text-[13px] text-muted hover:text-foreground hover:border-border-strong transition-colors"
          >
            <span class="text-primary">+</span> 提交 Skill
          </NuxtLink>
          <ThemeToggle />
          <a
            href="https://github.com/anthropics/skills"
            target="_blank"
            rel="noopener"
            class="grid size-8 place-items-center rounded-lg text-muted hover:text-foreground hover:bg-card transition-colors"
            aria-label="GitHub"
          >
            <svg viewBox="0 0 16 16" class="size-4" fill="currentColor" aria-hidden="true">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>
            </svg>
          </a>
          <button
            class="md:hidden grid size-8 place-items-center rounded-lg text-muted hover:text-foreground hover:bg-card"
            aria-label="打开菜单"
            @click="mobileOpen = !mobileOpen"
          >
            <svg viewBox="0 0 24 24" class="size-5" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path v-if="!mobileOpen" d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round" />
              <path v-else d="M6 6l12 12M18 6L6 18" stroke-linecap="round" />
            </svg>
          </button>
        </div>
      </div>

      <Transition name="drop">
        <nav v-if="mobileOpen" class="md:hidden pb-3 grid grid-cols-2 gap-1.5">
          <NuxtLink
            v-for="c in categories"
            :key="c.id"
            :to="`/c/${c.id}`"
            class="rounded-lg border border-border bg-card px-3 py-2 text-[13px] text-muted"
            @click="mobileOpen = false"
          >
            <span class="mr-1.5">{{ c.icon }}</span>{{ c.label }}
          </NuxtLink>
          <NuxtLink to="/submit" class="col-span-2 rounded-lg border border-primary/30 bg-primary-soft px-3 py-2 text-[13px] text-primary text-center" @click="mobileOpen = false">
            + 提交 Skill
          </NuxtLink>
        </nav>
      </Transition>
    </div>
  </header>
</template>

<script setup lang="ts">
import { categories } from '~/data/categories'

const mobileOpen = ref(false)
const route = useRoute()
watch(() => route.fullPath, () => (mobileOpen = false))
</script>

<style scoped>
.drop-enter-active,
.drop-leave-active {
  transition: all 0.18s ease;
}
.drop-enter-from,
.drop-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
