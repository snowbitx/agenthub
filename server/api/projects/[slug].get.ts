import { getProjectBySlug } from '../../utils/projects'

export default defineEventHandler((event) => {
  const slug = getRouterParam(event, 'slug')
  const project = slug ? getProjectBySlug(slug) : undefined
  if (!project) {
    throw createError({ statusCode: 404, statusMessage: 'Project not found' })
  }
  return project
})
