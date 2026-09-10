/**
 * 批量发现候选项目:GitHub search API 多路查询 → 去重 → 打分 → 输出 JSON
 * 只输出数据,由人工(或下一脚本)审核后并入 data/projects.ts
 */
const TOKEN = process.env.GITHUB_TOKEN || ''
const UA = 'agenthub-discovery/1.0'
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

async function gh(url) {
  for (let i = 0; i < 3; i++) {
    const res = await fetch(url, {
      headers: { 'User-Agent': UA, Accept: 'application/vnd.github+json', ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {}) },
    })
    if (res.ok) return res.json()
    if (res.status === 403 || res.status === 429) {
      const reset = res.headers.get('x-ratelimit-reset')
      const wait = reset ? Math.max(1, reset * 1000 - Date.now()) : 30000
      if (wait < 120000) { await sleep(wait); continue }
    }
    await sleep(2000)
  }
  return { items: [] }
}

const QUERIES = [
  // skills 生态
  'awesome+claude+skills', 'claude+skills+collection', 'agent+skills+list', 'skills+marketplace+claude', 'claude+code+skills',
  // agent 框架
  'agent+framework+llm', 'ai+agent+framework', 'multi-agent+framework', 'autonomous+agent+llm', 'agent+sdk',
  // coding agents
  'ai+coding+agent', 'terminal+ai+assistant+agent', 'coding+assistant+cli+llm',
  // browser/computer use
  'browser+agent+llm', 'computer+use+agent', 'web+automation+ai+agent',
  // workflow/orchestration platforms
  'ai+agent+workflow+platform', 'agent+orchestration', 'llm+agent+builder',
  // 第二轮:补充生态位
  'mcp+server+collection', 'model+context+protocol+toolkit',
  'rag+framework+llm', 'agent+memory+llm',
  'agent+evaluation+observability', 'llm+observability+tracing',
  'voice+agent+ai', 'speech+agent+realtime',
  'ai+agent+国内+开源', '智能体+框架',
  'claude+code+plugins', 'codex+agent+openai',
  'agent+security+pentest', 'research+agent+deep',
]

async function main() {
  const seen = new Map()
  for (const q of QUERIES) {
    const data = await gh(`https://api.github.com/search/repositories?q=${q}&sort=stars&order=desc&per_page=15`)
    for (const r of data.items ?? []) {
      if (r.archived || r.fork) continue
      if (seen.has(r.full_name)) continue
      seen.set(r.full_name, {
        repo: r.full_name,
        stars: r.stargazers_count,
        desc: (r.description || '').slice(0, 90),
        lang: r.language,
        pushed: r.pushed_at,
        topic: r.topics?.slice(0, 5) ?? [],
        query: q,
      })
    }
    await sleep(6500) // search API 限流:10 req/min
  }
  const list = [...seen.values()].sort((a, b) => b.stars - a.stars)
  console.log(JSON.stringify(list, null, 2))
}

main()
