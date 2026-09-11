<script setup lang="ts">
useHead({ title: '关于' })
</script>

<template>
  <div class="mx-auto max-w-3xl px-4 sm:px-6 py-10 sm:py-14">
    <h1 class="text-2xl sm:text-3xl font-bold tracking-tight">关于 AgentHub</h1>
    <div class="mt-6 space-y-5 text-[14px] leading-relaxed text-muted">
      <p>
        AgentHub 是一个<strong class="text-foreground">开放、社区驱动的 AI Agent 生态目录</strong>,
        架构理念:数据即代码,构建期产出索引,运行时零数据库。
      </p>
      <p>
        Agent Skills 是一种开放的能力包格式 —— 一个包含 SKILL.md 的文件夹,
        让 Agent 在需要时加载对应的能力。生态正在爆发,但资源散落在无数仓库和 awesome 列表里,
        这里是它们的统一入口。
      </p>
      <div class="rounded-xl border border-border bg-card p-5">
        <h2 class="text-[14px] font-semibold text-foreground">架构一览</h2>
        <ul class="mt-3 space-y-2 text-[13px]">
          <li><span class="font-mono text-primary">Nuxt 3</span> + Tailwind CSS v4 — SSR 与 UI</li>
          <li><span class="font-mono text-primary">data/projects.ts</span> — 类型安全的种子数据(defineProjectMeta)</li>
          <li><span class="font-mono text-primary">scripts/sync-data.mjs</span> — GitHub API 同步 stars/forks/活跃度</li>
          <li><span class="font-mono text-primary">/api/projects</span> — 过滤、搜索、排序 API</li>
        </ul>
      </div>
      <p class="text-[12.5px] text-faint">
        数据来源:GitHub REST API · 本站与 Anthropic 无隶属关系,仅为社区索引服务。
      </p>
    </div>
  </div>
</template>
