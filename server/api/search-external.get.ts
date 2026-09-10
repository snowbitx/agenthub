/**
 * 站外搜索:站内目录没有时,代理 GitHub Search API 找相关仓库。
 * - 结果缓存在内存里,避免触发 GitHub 搜索 API 的 10 req/min 限流
 * - 支持 GITHUB_TOKEN 提高配额,没有也能用(匿名限流下够单页使用)
 */
interface ExternalRepo {
  slug: string
  name: string
  description: string
  repo: string
  author: string
  stars: number
  pushedAt?: string
  language?: string
  url: string
}

interface CacheEntry {
  at: number
  repos: ExternalRepo[]
}

const TTL = 10 * 60 * 1000
const UA = 'agenthub-site/1.0'
const cache = new Map<string, CacheEntry>()

export default defineEventHandler(async (event) => {
  const q = (getQuery(event).q ?? '').toString().trim().slice(0, 100)
  if (!q) return { query: '', repos: [] }

  const key = q.toLowerCase()
  const hit = cache.get(key)
  if (hit && Date.now() - hit.at < TTL) {
    return { query: q, repos: hit.repos, cached: true }
  }

  const token = process.env.GITHUB_TOKEN || ''
  const url =
    'https://api.github.com/search/repositories?q=' +
    encodeURIComponent(`${q} skill OR skills OR agent in:name,description,readme`) +
    '&sort=best-match&order=desc&per_page=9'

  const res = await fetch(url, {
    headers: {
      'User-Agent': UA,
      Accept: 'application/vnd.github+json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  })

  if (!res.ok) {
    throw createError({
      statusCode: res.status === 403 || res.status === 429 ? 429 : 502,
      statusMessage: res.status === 403 || res.status === 429 ? 'GitHub rate limited, try later' : 'GitHub search failed',
    })
  }

  const data = (await res.json()) as {
    items?: Array<{
      full_name: string
      name: string
      description: string | null
      html_url: string
      stargazers_count: number
      pushed_at?: string
      language?: string | null
      owner: { login: string }
    }>
  }

  const repos: ExternalRepo[] = (data.items ?? [])
    .filter((r) => !r.fork)
    .slice(0, 9)
    .map((r) => ({
      slug: r.full_name,
      name: r.name,
      description: r.description ?? '',
      repo: r.full_name,
      author: r.owner.login,
      stars: r.stargazers_count,
      pushedAt: r.pushed_at,
      language: r.language ?? undefined,
      url: r.html_url,
    }))

  cache.set(key, { at: Date.now(), repos })
  if (cache.size > 200) {
    const oldest = [...cache.entries()].sort((a, b) => a[1].at - b[1].at)[0]
    if (oldest) cache.delete(oldest[0])
  }

  return { query: q, repos }
})
