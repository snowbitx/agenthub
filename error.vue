<script setup lang="ts">
const { data: project } = await useFetch(`/api/projects/${useRoute().params.slug}`).catch(() => ({ data: ref(null) }))
if (project.value) {
  clearError({ redirect: `/p/${project.value.slug}` })
}

const { theme, init } = useTheme()
onMounted(init)
</script>

<template>
  <div class="mx-auto max-w-3xl px-4 sm:px-6 py-24 text-center">
    <p class="font-mono text-6xl font-bold text-gradient">404</p>
    <h1 class="mt-4 text-xl font-semibold">页面走丢了</h1>
    <p class="mt-2 text-[13.5px] text-muted">这个技能或分类不存在,可能还没被收录。</p>
    <div class="mt-6 flex items-center justify-center gap-3">
      <NuxtLink to="/" class="rounded-lg bg-primary px-4 py-2 text-[13.5px] font-semibold text-background hover:bg-primary-strong transition-colors">回首页</NuxtLink>
      <NuxtLink to="/browse" class="rounded-lg border border-border-strong px-4 py-2 text-[13.5px] text-muted hover:text-foreground transition-colors">浏览全部</NuxtLink>
    </div>
    <p class="mt-8 font-mono text-[11px] text-faint">agents / prompts / official / devtools / docs / productivity / creative / integrations / templates</p>
    <div class="mt-10 flex justify-center">
      <ThemeToggle />
    </div>
  </div>
</template>
