import tailwindcss from '@tailwindcss/vite'

// 种子数据在配置加载期即可读(nuxt.config 由 jiti 执行 TS)
const { projects } = (await import('./data/projects')) as typeof import('./data/projects')
const { categories } = (await import('./data/categories')) as typeof import('./data/categories')

const projectRoutes = projects.map((p) => `/p/${p.slug}`)
const categoryRoutes = categories.map((c) => `/c/${c.id}`)

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  modules: ['@nuxtjs/google-fonts'],
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
  },
  googleFonts: {
    families: {
      Inter: ['400', '500', '600', '700', '800'],
      'JetBrains+Mono': ['400', '500'],
    },
  },
  runtimeConfig: {
    public: {
      siteUrl: process.env.SITE_URL || 'https://agenthub-topaz-phi.vercel.app',
    },
  },
  app: {
    head: {
      titleTemplate: (t) => (t ? `${t} · AgentHub` : 'AgentHub — Discover the AI Agent Ecosystem: Frameworks, Coding Agents & Skills'),
      htmlAttrs: { lang: 'zh-CN' },
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
      link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    },
  },
  typescript: {
    strict: true,
    tsConfig: { compilerOptions: { resolveJsonModule: true } },
  },
  nitro: {
    prerender: {
      crawlLinks: true,
      routes: [
        '/',
        '/browse',
        '/submit',
        '/about',
        '/sitemap.xml',
        '/robots.txt',
        '/llms.txt',
        ...categoryRoutes,
        ...projectRoutes,
      ],
    },
  },
})
