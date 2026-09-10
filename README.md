# AgentHub ✦

**Discover the Agent Skills Ecosystem** — an open, community-driven directory of Agent Skills.
Built from scratch following the architecture pattern of [vuejs-community](https://vuejs-community.vercel.app/): data as code, index generated at build time, zero runtime database.

![stack](https://img.shields.io/badge/Nuxt%203-SSR-42d392) ![style](https://img.shields.io/badge/Tailwind%20CSS%20v4-dark-647aff) ![data](https://img.shields.io/badge/GitHub%20API-daily%20sync-f5a524)

## Features

- **Home** — hero + live ecosystem stats (projects / repos / total stars) + featured skills + category explorer + latest additions
- **Browse** `/browse` — debounced keyword search, kind filter, four sort modes, URL state sync
- **Categories** `/c/[category]` — 7 categories with repo-heat overview
- **Detail** `/p/[slug]` — stars/forks/maintenance status, one-click install command, related projects
- **Submit** `/submit` — PR-based contribution guide with entry template
- **API** — `GET /api/projects` (category/q/kind/sort), `GET /api/projects/:slug`, `GET /api/stats`

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
data/categories.ts      # 7 category definitions
data/metrics.json       # GitHub metrics produced by the sync script (do not edit by hand)
scripts/sync-data.mjs   # GitHub API sync (rate-limit backoff, idempotent)
server/api/*            # Nitro API: filter / search / sort / detail / stats
pages/                  # index / browse / c/[category] / p/[slug] / submit / about
shared/schema.ts        # Project types + defineProjectMeta validation
```

GitHub metrics are inlined into the server bundle at build time, so the runtime has zero
filesystem or database dependencies — deploys cleanly to Vercel/serverless.

## Contributing a Skill

Edit `data/projects.ts` and add an entry:

```ts
defineProjectMeta({
  slug: 'my-skill',
  name: 'my-skill',
  description: 'One sentence on what this skill does',
  category: 'devtools',
  kind: 'skill',                // skill | collection
  repo: 'https://github.com/you/my-skill',
  author: 'you',
  tags: ['testing'],
  addedAt: '2026-09-09',
})
```

Then run `npm run data:sync` to backfill metrics and open a PR.

## Data Sync Strategy

Run `npm run data:sync` on a schedule (a GitHub Actions cron once a day works well —
`GITHUB_TOKEN` is injected automatically), commit the updated `data/metrics.json`, and let the
host redeploy. Same "data as code" model as vuejs-community.

## License

MIT
