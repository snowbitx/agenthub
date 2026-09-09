<template>
  <div class="mx-auto max-w-3xl px-4 sm:px-6 py-10 sm:py-14">
    <h1 class="text-2xl sm:text-3xl font-bold tracking-tight">提交技能</h1>
    <p class="mt-2 text-[14px] leading-relaxed text-muted">
      SkillsHub 是开放目录:任何符合 Agent Skills 规范的项目都可以被收录。
      数据本身就在仓库里 —— 修改一个 TypeScript 文件,发 PR 即可,站点自动重新部署。
    </p>

    <section class="mt-8 rounded-2xl border border-border bg-card p-6 sm:p-7">
      <h2 class="text-[15px] font-semibold">三种提交方式</h2>
      <ol class="mt-4 space-y-4 text-[13.5px] leading-relaxed text-muted">
        <li class="flex gap-3">
          <span class="grid size-6 shrink-0 place-items-center rounded-md bg-primary-soft text-primary font-mono text-[12px]">1</span>
          <div><span class="text-foreground font-medium">直接改数据文件(推荐)</span><br />编辑 <code class="font-mono text-[12px] text-primary bg-primary-soft rounded px-1">data/projects.ts</code>,仿照现有条目调用 defineProjectMeta,发 PR。</div>
        </li>
        <li class="flex gap-3">
          <span class="grid size-6 shrink-0 place-items-center rounded-md bg-primary-soft text-primary font-mono text-[12px]">2</span>
          <div><span class="text-foreground font-medium">开 Issue</span><br />提供仓库链接和一句话描述,由维护者代为收录。</div>
        </li>
        <li class="flex gap-3">
          <span class="grid size-6 shrink-0 place-items-center rounded-md bg-primary-soft text-primary font-mono text-[12px]">3</span>
          <div><span class="text-foreground font-medium">调 API</span><br />程序化提交走 <code class="font-mono text-[12px] text-primary bg-primary-soft rounded px-1">POST /api/submit</code>,便于批量导入 awesome 列表。</div>
        </li>
      </ol>
    </section>

    <section class="mt-5 rounded-2xl border border-border bg-card p-6 sm:p-7">
      <h2 class="text-[15px] font-semibold">收录标准</h2>
      <ul class="mt-3 space-y-2 text-[13.5px] text-muted">
        <li class="flex gap-2"><span class="text-primary">✓</span>仓库包含至少一个 SKILL.md(位于根目录或子目录)</li>
        <li class="flex gap-2"><span class="text-primary">✓</span>SKILL.md 含 YAML frontmatter(name / description)</li>
        <li class="flex gap-2"><span class="text-primary">✓</span>有 README 或使用说明,技能可被真实加载</li>
        <li class="flex gap-2"><span class="text-primary">✓</span>非纯 fork,且有明确的开源许可证</li>
      </ul>
    </section>

    <section class="mt-5 rounded-2xl border border-border bg-card p-6 sm:p-7">
      <h2 class="text-[15px] font-semibold">条目模板</h2>
      <pre class="mt-3 overflow-x-auto rounded-lg border border-border bg-surface p-4 font-mono text-[12px] leading-relaxed text-muted"><code>defineProjectMeta({
  slug: 'my-skill',              // URL 标识,kebab-case
  name: 'my-skill',
  description: '一句话说明这个技能解决什么问题',
  category: 'devtools',          // official|devtools|docs|productivity
                                 // |creative|integrations|templates
  kind: 'skill',                 // skill | collection
  repo: 'https://github.com/you/my-skill',
  sourcePath: 'skills/my-skill', // 仓库内子路径(可选)
  author: 'you',
  tags: ['testing'],
  addedAt: '2026-09-09',
})</code></pre>
      <NuxtLink
        to="/browse"
        class="mt-5 inline-flex items-center gap-1.5 rounded-lg border border-border-strong px-4 py-2 text-[13px] text-foreground hover:border-primary/40 hover:text-primary transition-colors"
      >
        先浏览现有条目找找感觉 →
      </NuxtLink>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({ title: '提交技能' })
</script>
