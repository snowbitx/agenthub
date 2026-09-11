#!/usr/bin/env python3
"""第四轮扩充:Prompts 提示词分类,30 个精选项目。追加进 data/projects.ts。"""
import re

# (repo, category, kind, tags, featured, 中文描述)
ITEMS = [
    ("f/prompts.chat", "prompts", "collection", ["chatgpt", "classic"], True, "最经典的 ChatGPT 提示词合集:数百种角色与场景,开箱即用"),
    ("dair-ai/Prompt-Engineering-Guide", "prompts", "collection", ["guide", "papers"], True, "最系统的提示词工程指南:论文、课程与笔记本(DAIR.AI 出品)"),
    ("asgeirtj/system_prompts_leaks", "prompts", "collection", ["system-prompts"], False, "主流 AI 产品系统提示词提取合集:Claude/GPT/Gemini"),
    ("PlexPt/awesome-chatgpt-prompts-zh", "prompts", "collection", ["chinese", "chatgpt"], True, "ChatGPT 中文调教指南:各种场景的中文提示词大全"),
    ("elder-plinus/CL4R1T4S", "prompts", "collection", ["system-prompts"], False, "ChatGPT/Claude/Gemini/Grok/Perplexity 系统提示词大全"),
    ("freestylefly/awesome-gpt-image-2", "prompts", "collection", ["image", "chinese"], False, "GPT Image 2 提示词案例库:530+ 案例、20+ 工业级模板"),
    ("promptfoo/promptfoo", "devtools", "agent", ["testing", "security"], True, "测试提示词、Agent 与 RAG 的标准工具:红队测试与漏洞扫描"),
    ("EvoLinkAI/awesome-gpt-image-2-API-and-Prompts", "prompts", "collection", ["image", "api"], False, "GPT-Image-2 API 用法与提示词合集"),
    ("NVIDIA/SkillSpector", "devtools", "agent", ["security", "nvidia"], False, "NVIDIA 出品:AI Agent Skills 安全扫描器,检测恶意行为"),
    ("YouMind-OpenLab/awesome-nano-banana-pro-prompts", "prompts", "collection", ["image"], False, "全球最大 Nano Banana Pro 提示词库:10000+ 精选案例"),
    ("Piebald-AI/claude-code-system-prompts", "prompts", "collection", ["claude", "system-prompts"], False, "Claude Code 系统提示词全文与 27 个内置工具描述"),
    ("nidhinjs/prompt-master", "prompts", "skill", ["meta", "skill"], False, "帮你写提示词的 Skill:为任何 AI 工具生成精准提示"),
    ("langgptai/LangGPT", "prompts", "collection", ["methodology", "chinese"], True, "结构化提示词方法论:让每个人成为提示词专家(中文)"),
    ("LouisShark/chatgpt_system_prompt", "prompts", "collection", ["system-prompts", "gpts"], False, "GPT 系统提示词合集与注入案例研究"),
    ("YouMind-OpenLab/awesome-gpt-image-2", "prompts", "collection", ["image"], False, "最大的 GPT Image 2 提示词库:每日更新 2000+ 案例"),
    ("friuns2/BlackFriday-GPTs-Prompts", "prompts", "collection", ["gpts"], False, "免订阅即可使用的 GPTs 提示词清单"),
    ("ai-boost/awesome-prompts", "prompts", "collection", ["gpt-store"], False, "GPT Store 顶级 GPT 的提示词精选"),
    ("jamez-bondos/awesome-gpt4o-images", "prompts", "collection", ["image"], False, "GPT-4o 图像生成案例与提示词合集"),
    ("mufeedvh/code2prompt", "devtools", "agent", ["cli", "codegen"], False, "把代码库转成单个 LLM 提示词的 CLI 工具"),
    ("promptslab/Awesome-Prompt-Engineering", "prompts", "collection", ["awesome", "guide"], False, "提示词工程资源大全:论文、工具与课程"),
    ("langgptai/awesome-claude-prompts", "prompts", "collection", ["claude", "chinese"], False, "Claude 提示词精选:更好地使用 Claude"),
    ("0xeb/TheBigPromptLibrary", "prompts", "collection", ["library"], False, "提示词、系统提示词与 LLM 指令大合集"),
    ("thinkingjimmy/Learning-Prompt", "prompts", "collection", ["course", "chinese"], False, "免费提示词工程在线课程(中文):ChatGPT 与 Midjourney"),
    ("trigaten/Learn_Prompting", "prompts", "collection", ["course"], False, "Learn Prompting 官方仓库:提示工程与生成 AI 指南"),
    ("atfortes/Awesome-LLM-Reasoning", "prompts", "collection", ["reasoning", "papers"], False, "从 CoT 到 o1/DeepSeek-R1 的 LLM 推理研究合集"),
    ("Meirtz/Awesome-Context-Engineering", "prompts", "collection", ["context-engineering"], False, "上下文工程全景:从提示词工程到 Agent 记忆"),
    ("KhazP/vibe-coding-prompt-template", "prompts", "collection", ["vibe-coding"], False, "Vibe Coding 提示词模板:PRD/技术设计/MVP 生成"),
    ("LearnPrompt/LearnPrompt", "prompts", "collection", ["course", "chinese"], False, "永久免费开源 AIGC 课程(中文):Claude Code/Codex/OpenClaw"),
    ("EgoAlpha/prompt-in-context-learning", "prompts", "collection", ["icl", "academic"], False, "上下文学习与提示工程资源合集(含中译)"),
    ("YiVal/YiVal", "devtools", "agent", ["auto-prompt", "evaluation"], False, "自动提示词优化助手:GenAI 应用评测框架"),
]

TODAY = "2026-09-10"

def slug_of(repo: str) -> str:
    s = repo.lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

ts_path = "data/projects.ts"
src = open(ts_path).read()
existing = set(re.findall(r"github\.com/([\w.-]+/[\w.-]+)'", src))
used = set(re.findall(r"slug: '([^']+)'", src))

lines = []
added = 0
for repo, cat, kind, tags, featured, desc in ITEMS:
    if repo in existing:
        print(f"skip (already in): {repo}")
        continue
    slug = slug_of(repo)
    if slug in used:
        print(f"skip (dup slug): {repo} -> {slug}")
        continue
    used.add(slug)
    name = repo.split("/")[1]
    author = repo.split("/")[0]
    tag_str = ", ".join(f"'{t}'" for t in tags)
    feat = "\n    featured: true," if featured else ""
    lines.append(f"""  defineProjectMeta({{
    slug: '{slug}',
    name: '{name}',
    description: '{desc}',
    category: '{cat}',
    kind: '{kind}',
    repo: 'https://github.com/{repo}',
    author: '{author}',
    tags: [{tag_str}],
    addedAt: '{TODAY}',{feat}
  }}),""")
    added += 1

assert src.rstrip().endswith("]")
src = src.rstrip()[:-1] + "\n".join(lines) + "\n]\n"
open(ts_path, "w").write(src)
print(f"appended {added} entries")
