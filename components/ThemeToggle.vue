<template>
  <button
    class="theme-toggle grid size-8 place-items-center rounded-lg text-muted hover:text-foreground hover:bg-card transition-colors"
    :aria-label="isDark ? '切换到亮色主题' : '切换到暗色主题'"
    :title="isDark ? '切换到亮色主题' : '切换到暗色主题'"
    @click="onToggle"
  >
    <Transition name="theme-rotate" mode="out-in">
      <!-- 太阳:亮色模式 -->
      <svg v-if="!isDark" key="sun" viewBox="0 0 24 24" class="size-[18px]" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <circle cx="12" cy="12" r="4.5" />
        <path stroke-linecap="round" d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5 5l1.6 1.6M17.4 17.4L19 19M19 5l-1.6 1.6M6.6 17.4L5 19" />
      </svg>
      <!-- 月亮:暗色模式 -->
      <svg v-else key="moon" viewBox="0 0 24 24" class="size-[18px]" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11Z" stroke-linejoin="round" />
      </svg>
    </Transition>
  </button>
</template>

<script setup lang="ts">
const { theme, toggle, init } = useTheme()

const isDark = computed(() => theme.value === 'dark')

onMounted(init)

/** 切换主题并让全局色彩平滑过渡 200ms,期间禁止再次触发避免动画叠加 */
const TRANSITION_MS = 200
let transitioning = false
const onToggle = () => {
  if (transitioning) return
  transitioning = true
  document.documentElement.classList.add('theme-transition')
  toggle()
  window.setTimeout(() => {
    document.documentElement.classList.remove('theme-transition')
    transitioning = false
  }, TRANSITION_MS)
}
</script>
