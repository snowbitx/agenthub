export function formatStars(n?: number): string {
  if (n == null) return '—'
  if (n >= 1000) {
    const v = n / 1000
    return `${v >= 100 ? Math.round(v) : v.toFixed(1).replace(/\.0$/, '')}k`
  }
  return String(n)
}

export function formatDate(iso?: string): string {
  if (!iso) return '—'
  const d = new Date(iso)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export function relativeDays(iso?: string): string {
  if (!iso) return ''
  const days = Math.floor((Date.now() - new Date(iso).getTime()) / 86400000)
  if (days <= 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 30) return `${days} 天前`
  if (days < 365) return `${Math.floor(days / 30)} 个月前`
  return `${Math.floor(days / 365)} 年前`
}

export function healthLabel(pushedAt?: string): { label: string; cls: string } {
  if (!pushedAt) return { label: '未知', cls: 'text-faint bg-white/5' }
  const days = Math.floor((Date.now() - new Date(pushedAt).getTime()) / 86400000)
  if (days <= 14) return { label: '活跃维护', cls: 'text-primary bg-primary-soft' }
  if (days <= 90) return { label: '近期更新', cls: 'text-warn bg-warn/10' }
  return { label: '少有更新', cls: 'text-faint bg-white/5' }
}
