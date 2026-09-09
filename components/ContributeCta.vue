<template>
  <section class="relative overflow-hidden border-t border-border/70">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 py-16">
      <div class="rounded-2xl border border-border bg-card p-8 sm:p-10 text-center relative overflow-hidden">
        <div class="glow-primary absolute -top-24 left-1/2 -translate-x-1/2 size-80" aria-hidden="true" />
        <h2 class="relative text-2xl sm:text-3xl font-bold tracking-tight">发现了缺失的技能?</h2>
        <p class="relative mx-auto mt-3 max-w-xl text-[14px] leading-relaxed text-muted">
          通过 PR 提交你的技能,一个 <code class="font-mono text-[12.5px] text-primary bg-primary-soft rounded px-1.5 py-0.5">defineProjectMeta</code> 调用即可完成收录,类型安全,零门槛。
        </p>
        <div class="relative mt-7 flex flex-wrap items-center justify-center gap-3">
          <NuxtLink to="/submit" class="inline-flex items-center rounded-lg bg-primary px-5 py-2.5 text-[14px] font-semibold text-background hover:bg-primary-strong transition-colors">
            提交技能
          </NuxtLink>
          <a href="https://github.com/anthropics/skills" target="_blank" rel="noopener" class="inline-flex items-center rounded-lg border border-border-strong px-5 py-2.5 text-[14px] text-foreground hover:border-primary/40 hover:text-primary transition-colors">
            查看技能规范
          </a>
        </div>
      </div>
    </div>
  </section>
</template>
