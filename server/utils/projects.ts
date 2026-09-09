import { readFileSync, existsSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { projects as seedProjects } from '../../data/projects'
import { categories } from '../../data/categories'
import type { Project } from '../../shared/schema'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const METRICS_FILE = join(ROOT, 'data', 'metrics.json')

let metricsCache: Record<string, any> | null = null

function loadMetrics(): Record<string, any> {
  if (metricsCache) return metricsCache
  try {
    metricsCache = JSON.parse(readFileSync(METRICS_FILE, 'utf8'))
  } catch {
    metricsCache = {}
  }
  return metricsCache!
}

export function getAllProjects(): Project[] {
  const metrics = loadMetrics()
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
  const metrics = loadMetrics()
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
