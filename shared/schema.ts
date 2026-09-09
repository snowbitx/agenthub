export type CategoryId =
  | 'official'
  | 'devtools'
  | 'docs'
  | 'productivity'
  | 'creative'
  | 'integrations'
  | 'templates'

export type ProjectKind = 'skill' | 'collection'

export interface ProjectMeta {
  slug: string
  name: string
  description: string
  category: CategoryId
  kind: ProjectKind
  repo: string
  /** 仓库内技能所在子目录(单仓库多技能时使用) */
  sourcePath?: string
  npm?: string
  author: string
  tags: string[]
  addedAt: string
  featured?: boolean
}

export interface Project extends ProjectMeta {
  stars?: number
  forks?: number
  issues?: number
  pushedAt?: string
  createdAt?: string
  lastSyncedAt?: string
}

export interface Category {
  id: CategoryId
  label: string
  description: string
  icon: string
}

/** 贡献者用这个函数声明项目元数据,获得完整的类型提示与校验 */
export function defineProjectMeta(meta: ProjectMeta): ProjectMeta {
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(meta.slug)) {
    throw new Error(`Invalid slug: ${meta.slug}`)
  }
  if (!meta.repo.startsWith('https://github.com/')) {
    throw new Error(`Invalid repo url: ${meta.repo}`)
  }
  return meta
}
