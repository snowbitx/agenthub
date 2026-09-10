import type { Category } from '../shared/schema'

export const categories: Category[] = [
  {
    id: 'official',
    label: '官方 Skills',
    description: 'Anthropic 官方与示例 Skills:文档、Office 与构建器',
    icon: '⚡',
  },
  {
    id: 'devtools',
    label: '开发工具',
    description: '代码评审、调试、TDD 与工程工作流 Skills',
    icon: '🛠️',
  },
  {
    id: 'docs',
    label: '文档写作',
    description: '技术写作、共创文档与实施计划',
    icon: '📝',
  },
  {
    id: 'productivity',
    label: '效率办公',
    description: '内部沟通、状态报告与日常事务自动化',
    icon: '📅',
  },
  {
    id: 'creative',
    label: '创意设计',
    description: '视觉艺术、品牌规范与主题美化',
    icon: '🎨',
  },
  {
    id: 'integrations',
    label: '集成',
    description: '连接外部服务:MCP server 与 API 集成',
    icon: '🔌',
  },
  {
    id: 'agents',
    label: 'Agent 框架',
    description: '主流 Agent 框架、SDK 与自主智能体产品',
    icon: '🤖',
  },
  {
    id: 'templates',
    label: '模板与资源集',
    description: '脚手架、配置模板与 awesome 精选合集',
    icon: '📦',
  },
]

export const categoryMap = Object.fromEntries(categories.map((c) => [c.id, c]))
