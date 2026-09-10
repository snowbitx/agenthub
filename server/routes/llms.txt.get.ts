import { getAllProjects, getStats } from '../utils/projects'
import { categories } from '../../data/categories'

const SITE = process.env.SITE_URL || 'https://agenthub-topaz-phi.vercel.app'

export default defineEventHandler((event) => {
  const { totalProjects, totalStars } = getStats()
  const projects = getAllProjects()

  const byCategory = categories
    .map((c) => {
      const list = projects.filter((p) => p.category === c.id)
      const top = [...list].sort((a, b) => (b.stars ?? 0) - (a.stars ?? 0)).slice(0, 5)
      return `- ${c.label} (${c.id}): ${list.length} projects. Top: ${top.map((p) => `${p.name}(${p.stars ?? '?'}★)`).join(', ')}`
    })
    .join('\n')

  const list = projects
    .sort((a, b) => (b.stars ?? 0) - (a.stars ?? 0))
    .map((p) => `- [${p.name}](${SITE}/p/${p.slug}): ${p.description} (${p.stars ?? '?'}★, ${p.kind})`)
    .join('\n')

  const text = `# AgentHub

> Discover the Agent Ecosystem — an open, community-driven directory of AI Agent frameworks, coding agents, browser agents, and Agent Skills. ${totalProjects} curated projects, ${Math.round(totalStars / 1000)}k+ combined GitHub stars, metrics synced daily from the GitHub API.

AgentHub indexes the fast-moving AI agent ecosystem so developers can find the right tool in one place: agent frameworks (LangChain, AutoGen, CrewAI, MetaGPT), coding agents (OpenCode, Cline, Gemini CLI), computer-use and browser agents (Browser Use, Stagehand), and Agent Skills collections compatible with Claude Code and other runtimes.

## Categories

${byCategory}

## All Projects (by stars)

${list}

## How to contribute

Submit a PR editing data/projects.ts with a defineProjectMeta() call, or open an issue. Repository: https://github.com/snowbitx/agenthub
`

  setHeader(event, 'Content-Type', 'text/plain; charset=utf-8')
  return text
})
