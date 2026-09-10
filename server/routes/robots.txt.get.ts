export default defineEventHandler((event) => {
  const SITE = process.env.SITE_URL || 'https://agenthub.example.vercel.app'
  setHeader(event, 'Content-Type', 'text/plain; charset=utf-8')
  return `User-agent: *
Allow: /

Sitemap: ${SITE}/sitemap.xml
`
})
