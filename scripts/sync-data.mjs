/**
 * 数据同步脚本:
 * 1. 用 ncc/esbuild-free 方式(直接正则解析)从 data/projects.ts 提取 repo 列表
 * 2. 调 GitHub API 拉取 stars / forks / pushedAt
 * 3. 写入 data/metrics.json,供 Nitro 运行时合并
 *
 * 设计为幂等:失败的字段保持缺失,下次运行补齐。限流时逐个退避重试。
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = dirname(fileURLToPath(import.meta.url))
const PROJECTS_FILE = join(ROOT, '..', 'data', 'projects.ts')
const METRICS_FILE = join(ROOT, '..', 'data', 'metrics.json')
const TOKEN = process.env.GITHUB_TOKEN || ''
const UA = 'skillsHub-sync/1.0'

function extractRepos(ts) {
  const repos = new Set()
  const re = /repo:\s*'([^']+)'/g
  let m
  while ((m = re.exec(ts))) repos.add(m[1])
  return [...repos]
}

async function ghFetch(url, tries = 3) {
  for (let i = 0; i < tries; i++) {
    const res = await fetch(url, {
      headers: {
        'User-Agent': UA,
        Accept: 'application/vnd.github+json',
        ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}),
      },
    })
    if (res.ok) return res.json()
    if (res.status === 404) {
      console.warn(`  404 ${url}`)
      return null
    }
    if (res.status === 403 || res.status === 429) {
      const reset = res.headers.get('x-ratelimit-reset')
      const wait = reset ? Math.max(1, (reset * 1000 - Date.now()) / 1000) : 30 * (i + 1)
      if (wait > 120) break
      console.warn(`  rate-limited, waiting ${Math.ceil(wait)}s`)
      await new Promise((r) => setTimeout(r, wait * 1000))
      continue
    }
    await new Promise((r) => setTimeout(r, 1000 * (i + 1)))
  }
  return null
}

async function main() {
  const ts = readFileSync(PROJECTS_FILE, 'utf8')
  const repos = extractRepos(ts)
  console.log(`Syncing ${repos.length} repos...`)

  const metrics = existsSync(METRICS_FILE)
    ? JSON.parse(readFileSync(METRICS_FILE, 'utf8'))
    : {}
  let ok = 0
  for (const repo of repos) {
    const path = repo.replace('https://github.com/', '')
    const data = await ghFetch(`https://api.github.com/repos/${path}`)
    if (data) {
      metrics[repo] = {
        stars: data.stargazers_count,
        forks: data.forks_count,
        issues: data.open_issues_count,
        createdAt: data.created_at,
        pushedAt: data.pushed_at,
        description: data.description,
        lastSyncedAt: new Date().toISOString(),
      }
      ok++
      console.log(`  ✓ ${path}: ★${data.stargazers_count}`)
    } else {
      console.warn(`  ✗ ${path} failed, keeping previous metrics`)
    }
  }

  mkdirSync(dirname(METRICS_FILE), { recursive: true })
  writeFileSync(METRICS_FILE, JSON.stringify(metrics, null, 2) + '\n')
  console.log(`Done: ${ok}/${repos.length} synced -> data/metrics.json`)
  if (ok === 0) process.exit(1)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
