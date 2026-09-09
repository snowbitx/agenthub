# SkillsHub ✦

**Discover the Agent Skills Ecosystem** — 一个开放、社区驱动的 Agent Skills 目录站。
参考 [vuejs-community](https://vuejs-community.vercel.app/) 的架构模式从零实现:数据即代码、构建期产索引、运行时零数据库。

![stack](https://img.shields.io/badge/Nuxt%203-SSR-42d392) ![style](https://img.shields.io/badge/Tailwind%20CSS%20v4-dark-647aff) ![data](https://img.shields.io/badge/GitHub%20API-daily%20sync-f5a524)

## 功能

- **首页**:Hero + 生态统计(项目/仓库/总 Stars)+ 精选技能 + 分类导航 + 最新收录
- **浏览页** `/browse`:关键词搜索(防抖)、类型筛选、四种排序、URL 状态同步
- **分类页** `/c/[category]`:7 个分类,含头部仓库热度概览
- **详情页** `/p/[slug]`:Stars/Forks/维护状态、安装命令一键复制、同分类推荐
- **提交页** `/submit`:PR 收录流程与条目模板
- **API**:`GET /api/projects`(category/q/kind/sort)、`GET /api/projects/:slug`、`GET /api/stats`

## 快速开始

```bash
npm install
npm run data:sync   # 拉取 GitHub stars/forks → data/metrics.json(可选,有 GITHUB_TOKEN 更稳)
npm run dev         # http://localhost:3000
npm run build && node .output/server/index.mjs   # 生产模式
```

## 架构

```
data/projects.ts        # 种子数据:defineProjectMeta() 类型安全声明
data/categories.ts      # 7 个分类定义
data/metrics.json       # sync 脚本产出的 GitHub 指标(勿手改)
scripts/sync-data.mjs   # GitHub API 同步(限流退避、幂等)
server/api/*            # Nitro API:过滤/搜索/排序/详情/统计
pages/                  # index / browse / c/[category] / p/[slug] / submit / about
shared/schema.ts        # Project 类型 + defineProjectMeta 校验
```

## 如何贡献一个新技能

编辑 `data/projects.ts`,添加一条:

```ts
defineProjectMeta({
  slug: 'my-skill',
  name: 'my-skill',
  description: '一句话说明这个技能解决什么问题',
  category: 'devtools',
  kind: 'skill',
  repo: 'https://github.com/you/my-skill',
  author: 'you',
  tags: ['testing'],
  addedAt: '2026-09-09',
})
```

然后运行 `npm run data:sync` 回填指标,发 PR 即可。

## 数据同步策略

本地/CI 定时跑 `npm run data:sync`(建议 GitHub Actions cron 每日一次,`GITHUB_TOKEN` 自动注入),提交 `data/metrics.json` 并触发重新部署——与 vuejs-community 相同的"数据即代码"模式。
