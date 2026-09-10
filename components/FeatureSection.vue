<template>
  <section class="mx-auto max-w-6xl px-4 sm:px-6 py-16">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="f in features"
        :key="f.title"
        class="group rounded-xl border border-border bg-card p-5 transition-colors hover:border-border-strong"
      >
        <span class="grid size-9 place-items-center rounded-lg bg-primary-soft border border-primary/20 text-primary">{{ f.icon }}</span>
        <h3 class="mt-4 text-[14.5px] font-semibold">{{ f.title }}</h3>
        <p class="mt-1.5 text-[13px] leading-relaxed text-muted">{{ f.desc }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const features = [
  { icon: '🗂', title: 'Everything Skills, One Place', desc: '官方示例、社区精品、 awesome 合集统一收录,告别在散落的仓库间大海捞针。' },
  { icon: '📈', title: 'Discover What Matters', desc: 'GitHub star、fork、最近推送时间自动同步,热度与维护状态一目了然。' },
  { icon: '🧪', title: 'Curated for Builders', desc: '每条收录都经过 SKILL.md 格式校验,保证 Skill 在 Claude Code 中真实可运行。' },
  { icon: '🌱', title: 'Growing with the Ecosystem', desc: '社区通过 PR 提交新 Skill,类型安全的 defineProjectMeta 保证数据质量。' },
]
</script>
