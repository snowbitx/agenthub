import { getAllProjects, getStats } from '../utils/projects'
import { categories } from '../../data/categories'

const SITE = process.env.SITE_URL || 'https://agenthub.example.vercel.app'

export default defineEventHandler((event) => {
  const projects = getAllProjects()
  const urls = [
    { loc: `${SITE}/`, priority: '1.0', changefreq: 'daily' },
    { loc: `${SITE}/browse`, priority: '0.9', changefreq: 'daily' },
    { loc: `${SITE}/submit`, priority: '0.4', changefreq: 'monthly' },
    { loc: `${SITE}/about`, priority: '0.4', changefreq: 'monthly' },
    ...categories.map((c) => ({
      loc: `${SITE}/c/${c.id}`,
      priority: '0.8',
      changefreq: 'daily',
    })),
    ...projects.map((p) => ({
      loc: `${SITE}/p/${p.slug}`,
      priority: '0.7',
      changefreq: 'weekly',
      lastmod: p.pushedAt || p.addedAt,
    })),
  ]
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (u) => `  <url>
    <loc>${u.loc}</loc>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>${u.lastmod ? `\n    <lastmod>${u.lastmod}</lastmod>` : ''}
  </url>`,
  )
  .join('\n')}
</urlset>`
  setHeader(event, 'Content-Type', 'application/xml; charset=utf-8')
  return xml
})
