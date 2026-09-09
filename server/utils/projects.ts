import { projects as seedProjects } from '../../data/projects'
import { categories } from '../../data/categories'
import metricsJson from '../../data/metrics.json'
import type { Project } from '../../shared/schema'

/** GitHub 指标在构建期内联进 server bundle,运行时零文件系统依赖(serverless 友好) */
const metrics = metricsJson as Record<string, any>

export function getAllProjects(): Project[] {
  return seedProjects.map((p) => {
    const m = metrics[p.repo] ?? {}
    return {
      ...p,
      stars: m.stars,
      forks: m.forks,
      issues: m.issues,
      createdAt: m.createdAt,
      pushedAt: m.pushedAt,
      lastSyncedAt: m.lastSyncedAt,
    }
  })
}

export function getProjectBySlug(slug: string): Project | undefined {
  return getAllProjects().find((p) => p.slug === slug)
}

export function getStats() {
  const all = getAllProjects()
  const uniqueRepos = new Set(all.map((p) => p.repo))
  const totalStars = [...uniqueRepos].reduce((sum, repo) => sum + (metrics[repo]?.stars ?? 0), 0)
  const lastSyncedAt = all
    .map((p) => p.lastSyncedAt)
    .filter(Boolean)
    .sort()
    .pop()
  return {
    totalProjects: all.length,
    totalRepos: uniqueRepos.size,
    totalCategories: categories.length,
    totalStars,
    lastSyncedAt,
  }
}
