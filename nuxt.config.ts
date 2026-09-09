import tailwindcss from '@tailwindcss/vite'

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
  app: {
    head: {
      titleTemplate: (t) => (t ? `${t} · SkillsHub` : 'SkillsHub — Discover the Agent Skills Ecosystem'),
    },
  },
  typescript: {
    strict: true,
    tsConfig: { compilerOptions: { resolveJsonModule: true } },
  },
})
