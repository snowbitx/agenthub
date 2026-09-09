import { getAllProjects, getStats } from '../utils/projects'
import { categoryMap } from '../../data/categories'
import type { Project } from '../../shared/schema'

export type SortKey = 'stars' | 'newest' | 'updated' | 'name'

export function sortProjects(list: Project[], sort: string): Project[] {
  const sorted = [...list]
  switch (sort) {
    case 'newest':
      return sorted.sort((a, b) => (b.addedAt > a.addedAt ? 1 : -1))
    case 'updated':
      return sorted.sort((a, b) => ((b.pushedAt ?? '') > (a.pushedAt ?? '') ? 1 : -1))
    case 'name':
      return sorted.sort((a, b) => a.name.localeCompare(b.name))
    case 'stars':
    default:
      return sorted.sort((a, b) => (b.stars ?? 0) - (a.stars ?? 0))
  }
}

export function filterProjects(
  list: Project[],
  opts: { category?: string; q?: string; kind?: string },
): Project[] {
  let result = list
  const { category, q, kind } = opts
  if (category && categoryMap[category]) {
    result = result.filter((p) => p.category === category)
  }
  if (kind === 'skill' || kind === 'collection') {
    result = result.filter((p) => p.kind === kind)
  }
  if (q) {
    const needle = q.toLowerCase()
    result = result.filter(
      (p) =>
        p.name.toLowerCase().includes(needle) ||
        p.description.toLowerCase().includes(needle) ||
        p.author.toLowerCase().includes(needle) ||
        p.tags.some((t) => t.toLowerCase().includes(needle)),
    )
  }
  return result
}

export { getAllProjects, getStats }
