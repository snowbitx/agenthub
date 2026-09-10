export type Theme = 'dark' | 'light'

const STORAGE_KEY = 'agenthub-theme'

/**
 * 预水合脚本:在水合前根据 localStorage / 系统偏好把主题 class 写到 <html> 上,
 * 避免亮色用户刷新页面时先闪一帧暗色(FOUC)。同时设置 colorScheme
 * 让浏览器原生控件(滚动条、表单)跟随主题。无框架依赖,只碰 documentElement。
 */
export const THEME_INIT_SCRIPT = `(function(){try{var t=localStorage.getItem('${STORAGE_KEY}');if(t!=='light'&&t!=='dark'){t=window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';}var d=document.documentElement;if(t==='light')d.classList.add('light');else d.classList.remove('light');d.style.colorScheme=t;}catch(e){}})();`

/** 读取初始主题:localStorage > 系统偏好 > 暗色(默认) */
export function resolveInitialTheme(): Theme {
  if (import.meta.client) {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'light' || saved === 'dark') return saved
    if (window.matchMedia?.('(prefers-color-scheme: light)').matches) return 'light'
  }
  return 'dark'
}

export function useTheme() {
  const theme = useState<Theme>('theme', () => 'dark')

  const apply = (t: Theme) => {
    if (import.meta.server) return
    document.documentElement.classList.toggle('light', t === 'light')
    document.documentElement.style.colorScheme = t
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', t === 'light' ? '#fafafa' : '#09090b')
  }

  const setTheme = (t: Theme) => {
    theme.value = t
    if (import.meta.client) {
      localStorage.setItem(STORAGE_KEY, t)
      apply(t)
    }
  }

  const toggle = () => setTheme(theme.value === 'dark' ? 'light' : 'dark')

  const init = () => {
    const t = resolveInitialTheme()
    theme.value = t
    apply(t)
  }

  return { theme, setTheme, toggle, init }
}
