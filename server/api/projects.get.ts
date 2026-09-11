import { getAllProjects } from '../utils/projects'
import { filterProjects, sortProjects } from '../utils/query'

export default defineEventHandler((event) => {
  const q = getQuery(event)
  let list = getAllProjects()
  list = filterProjects(list, {
    category: typeof q.category === 'string' ? q.category : undefined,
    q: typeof q.q === 'string' ? q.q : undefined,
    kind: typeof q.kind === 'string' ? q.kind : undefined,
  })
  list = sortProjects(list, typeof q.sort === 'string' ? q.sort : 'stars')
  return {
    total: list.length,
    projects: list,
  }
})
