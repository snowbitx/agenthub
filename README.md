# AgentHub ✦

**Discover the AI Agent Ecosystem** — an open, community-driven directory of AI Agent frameworks, coding agents, browser/computer-use agents, and Agent Skills.
Built from scratch following the architecture pattern of [vuejs-community](https://vuejs-community.vercel.app/): data as code, index generated at build time, zero runtime database.

**260 curated projects · 247 repos · 7.4M+ combined GitHub stars · metrics synced daily from the GitHub API**

![stack](https://img.shields.io/badge/Nuxt%203-SSR-42d392) ![style](https://img.shields.io/badge/Tailwind%20CSS%20v4-dark-647aff) ![data](https://img.shields.io/badge/GitHub%20API-daily%20sync-f5a524)

## Features

- **Home** — hero + live ecosystem stats (projects / repos / total stars) + featured projects + category explorer + latest additions
- **Browse** `/browse` — debounced keyword search, kind filter (Agent / Skill / Collection), four sort modes, URL state sync
- **Categories** `/c/[category]` — 9 categories (Agent frameworks & Prompts first) with repo-heat overview
- **Detail** `/p/[slug]` — stars/forks/maintenance status, one-click install command (`npm install` for agents, `npx skills add` for skills), related projects
- **Submit** `/submit` — PR-based contribution guide with entry template
- **API** — `GET /api/projects` (category/q/kind/sort), `GET /api/projects/:slug`, `GET /api/stats`

## SEO

- **Static prerender** — all 230 detail pages + 8 category pages pre-rendered at build time (crawlers get full HTML)
- **sitemap.xml** — 240+ URLs with `lastmod`
- **Per-page meta** — unique title/canonical/description per page, OG & Twitter cards site-wide
- **Structured data** — `WebSite` JSON-LD on the home page, `SoftwareApplication` JSON-LD on every detail page (rich snippets with ratings)
- **llms.txt** — full-site index for AI search engines (Perplexity, ChatGPT, etc.)

## Coverage

| Category | Highlights |
|---|---|
| 🤖 Agent Frameworks | LangChain, AutoGen, CrewAI, MetaGPT, OpenClaw, OpenCode, Hermes Agent, Gemini CLI |
| ⚡ Official Skills | anthropics/skills, claude-code, claude-cookbooks, official plugins directory |
| 🛠️ Dev Tools | Addy Osmani's agent-skills, claude-mem, claude-code-router, wshobson/agents |
| 📝 Docs & Writing | academic research skills, best-practice guides |
| 📅 Productivity | marketing, resume, internal comms skills |
| 🎨 Creative | design skills, taste-skill, canvas-design |
| 🔌 Integrations | awesome-mcp-servers, pathway, llmware, quivr, KAG |
| 💬 Prompts | prompts.chat (170k★), Prompt-Engineering-Guide, LangGPT, 中文调教指南, image prompt libraries |
| 📦 Templates & Collections | awesome lists, marketplaces, starter kits |

Plus dedicated ecosystem coverage: **memory layers** (mem0, Letta, MemOS), **deep research agents** (Tongyi DeepResearch, gpt-researcher), **voice agents** (pipecat, LiveKit, TEN), and **evaluation/observability** (MLflow, Cozeloop).

## Quick Start

```bash
npm install
npm run data:sync   # fetch GitHub stars/forks -> data/metrics.json (optional; GITHUB_TOKEN recommended)
npm run dev         # http://localhost:3000
npm run build && node .output/server/index.mjs   # production
```

## Architecture

```
data/projects.ts        # seed data: type-safe entries via defineProjectMeta()
data/categories.ts      # 8 category definitions (order = nav order)
data/metrics.json       # GitHub metrics produced by the sync script (do not edit by hand)
scripts/sync-data.mjs   # GitHub API sync (rate-limit checkpointing, 12h cache, idempotent resume)
scripts/discover.mjs    # batch discovery of candidate repos via GitHub search API
server/api/*            # Nitro API: filter / search / sort / detail / stats
server/routes/*         # sitemap.xml / robots.txt / llms.txt
pages/                  # index / browse / c/[category] / p/[slug] / submit / about
shared/schema.ts        # Project types + defineProjectMeta validation
.github/workflows/      # daily metrics sync (GitHub Actions cron)
```

GitHub metrics are inlined into the server bundle at build time, so the runtime has zero
filesystem or database dependencies — deploys cleanly to Vercel/serverless.

## Contributing a Project

Edit `data/projects.ts` and add an entry:

```ts
defineProjectMeta({
  slug: 'my-agent',
  name: 'my-agent',
  description: 'One sentence on what this project does',
  category: 'prompts',          // agents | prompts | official | devtools | docs | productivity | creative | integrations | templates
  kind: 'agent',                // agent | skill | collection
  repo: 'https://github.com/you/my-agent',
  author: 'you',
  tags: ['framework'],
  addedAt: '2026-09-10',
})
```

Then run `npm run data:sync` to backfill metrics and open a PR.

## Data Sync Strategy

Run `npm run data:sync` on a schedule (a GitHub Actions cron once a day works well —
`GITHUB_TOKEN` is injected automatically), commit the updated `data/metrics.json`, and let the
host redeploy. Same "data as code" model as vuejs-community.

## Deployment (Vercel)

1. Push to GitHub (this repo).
2. On [vercel.com/new](https://vercel.com/new), import the repo — the Nuxt preset is auto-detected.
3. Add one environment variable: `SITE_URL` = your production URL (e.g. `https://agenthub.vercel.app`). This powers canonical URLs, sitemap entries and llms.txt links.
4. Deploy. Every push to `main` and every daily metrics-sync commit redeploys automatically.

## License

MIT
