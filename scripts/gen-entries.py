#!/usr/bin/env python3
"""把精选候选项目生成为 data/projects.ts 的 TS 条目,追加进现有数组。"""
import re

# (repo, name, category, kind, tags, featured, 中文描述)
ITEMS = [
    # ===== Skills:devtools =====
    ("addyosmani/agent-skills", "devtools", "collection", ["engineering", "google"], True, "Addy Osmani 出品的生产级工程 Skills 集合:评审、性能与架构"),
    ("DietrichGebert/ponytail", "devtools", "skill", ["minimalism"], False, "让 AI 像最懒的资深工程师一样思考,写出更精简的代码"),
    ("JuliusBrussee/caveman", "devtools", "skill", ["token-saving"], False, "用最少 token 干最多活的极简主义 Skill"),
    ("Leonxlnx/taste-skill", "creative", "skill", ["design", "taste"], False, "给 AI 好品味:阻止 AI 生成廉价感设计的 Skill"),
    ("multica-ai/andrej-karpathy-skills", "devtools", "collection", ["claude-md"], False, "以 Karpathy 风格改进 Claude Code 行为的 CLAUDE.md 集合"),
    ("thedotmack/claude-mem", "devtools", "agent", ["memory", "context"], False, "跨会话持久记忆:为每个 Agent 保存上下文"),
    ("musistudio/claude-code-router", "devtools", "agent", ["router", "gateway"], False, "本地 AI 网关:在多个模型间路由任意 Agent 请求"),
    ("farion1231/cc-switch", "devtools", "agent", ["desktop", "manager"], False, "跨平台桌面 All-in-One 助手,统一管理 Claude Code 配置"),
    ("Yeachan-Heo/oh-my-claudecode", "devtools", "agent", ["orchestration"], False, "Teams 式多 Agent 编排,榨干 Claude Code 战斗力"),
    ("NanmiCoder/cc-haha", "devtools", "agent", ["desktop"], False, "本地优先的跨平台 Claude Code 桌面工作区"),
    ("Graphify-Labs/graphify", "devtools", "agent", ["knowledge-graph"], False, "把任意代码库变成 Agent 可查询的知识图谱"),
    ("headroomlabs-ai/headroom", "devtools", "agent", ["compression"], False, "压缩工具输出/日志/RAG 分块,Agent 省 token 利器"),
    ("utkusen/sast-skills", "devtools", "collection", ["security", "sast"], False, "在代码库中挖掘漏洞的安全审计 Skills 合集"),
    ("samber/cc-skills-golang", "devtools", "collection", ["golang"], False, "Golang 工程向 agentic Skills 合集"),
    ("softaworks/agent-toolkit", "devtools", "collection", ["toolkit"], False, "为 AI coding agent 精选的 Skills 合集"),
    ("NeoLabHQ/context-engineering-kit", "devtools", "collection", ["context-engineering"], False, "提升 Agent 上下文工程能力的 Claude Code Skills"),
    ("ConardLi/garden-skills", "devtools", "collection", ["frontend", "chinese"], False, "ConardLi 开源 Skills 合集:Web 开发与前端最佳实践"),
    ("microsoft/skills-for-fabric", "devtools", "collection", ["microsoft", "data"], False, "微软官方 Fabric 数据平台 Skills 与 MCP 系统"),
    ("numman-ali/n-skills", "devtools", "collection", ["marketplace"], False, "兼容 Claude Code 的 Agent 插件市场"),
    ("daymade/claude-code-skills", "devtools", "collection", ["marketplace"], False, "专业级 Claude Code Skills 市场"),
    ("GuDaStudio/skills", "devtools", "collection", ["community"], False, "社区开发的 Agent Skills 合集"),
    ("withkynam/vibecode-pro-max-kit", "devtools", "collection", ["spec-driven"], False, "规格驱动编程 harness:让 AI 不再遗忘上下文"),
    ("dmtrKovalenko/fff", "devtools", "agent", ["search", "sdk"], False, "最快的 AI Agent 文件搜索 SDK"),
    ("callstack/agent-device", "devtools", "agent", ["mobile", "automation"], False, "移动 App 自动化与验证,面向 AI coding agent"),
    ("mukul975/Anthropic-Cybersecurity-Skills", "devtools", "collection", ["security"], False, "817 个结构化网络安全 Skills,按 ATT&CK 映射"),
    ("new-silvermoon/awesome-android-agent-skills", "devtools", "collection", ["android"], False, "教 GitHub Copilot 写 Android 的标准化 Skills"),
    ("gptme/gptme", "devtools", "agent", ["terminal"], False, "终端里的 Agent:本地工具武装到牙齿"),
    # ===== Skills:docs =====
    ("Imbad0202/academic-research-skills", "docs", "collection", ["academic"], False, "学术研究 Skills:检索、写作到引用全流程"),
    ("brycewang-stanford/Awesome-Journal-Skills", "docs", "collection", ["academic", "stanford"], False, "斯坦福学者整理的期刊投稿 Skills 包"),
    ("OthmanAdi/planning-with-files", "docs", "skill", ["planning"], False, "基于文件的持久化规划,面向 AI coding agent"),
    ("humanlayer/12-factor-agents", "docs", "collection", ["methodology"], False, "构建 LLM 应用的 12 条原则,Agent 时代方法论"),
    ("shanraisshan/claude-code-best-practice", "docs", "collection", ["best-practice"], False, "从 vibe coding 到 agentic engineering 的实践指南"),
    ("wesammustafa/Claude-Code-Everything-You-Need-to-Know", "docs", "collection", ["guide"], False, "Claude Code 心智模型与实战指南"),
    # ===== Skills:productivity =====
    ("coreyhaines31/marketingskills", "productivity", "collection", ["marketing"], False, "市场营销 Skills:CRO、文案与增长"),
    ("Paramchoudhary/ResumeSkills", "productivity", "collection", ["resume"], False, "简历优化 AI Skills 合集"),
    # ===== Skills:creative =====
    ("bergside/awesome-design-skills", "creative", "collection", ["design"], False, "67 个 DESIGN.md / SKILL.md 设计 Skills 清单"),
    ("rohitg00/awesome-claude-design", "creative", "collection", ["design"], False, "按美学流派整理的 Claude 设计提示库"),
    # ===== Skills:templates / awesome =====
    ("ComposioHQ/awesome-claude-skills", "templates", "collection", ["awesome"], True, "精选 Claude Skills、资源与工具清单"),
    ("VoltAgent/awesome-agent-skills", "templates", "collection", ["awesome"], False, "来自官方文档的 1000+ agent skills 合集"),
    ("heilcheng/awesome-agent-skills", "templates", "collection", ["awesome"], False, "Agent Skills 教程、指南与目录大全"),
    ("BehiSecc/awesome-claude-skills", "templates", "collection", ["awesome"], False, "精选 Claude Skills 清单"),
    ("Prat011/awesome-llm-skills", "templates", "collection", ["awesome"], False, "LLM 与 AI Agent Skills 精选清单"),
    ("abubakarsiddik31/claude-skills-collection", "templates", "collection", ["awesome"], False, "官方与社区 Claude Skills 合集"),
    ("rohitg00/awesome-claude-code-toolkit", "templates", "collection", ["toolkit"], False, "最全 Claude Code 工具箱:135 个 agents/skills/hooks"),
    ("hesreallyhim/awesome-claude-code", "templates", "collection", ["awesome"], False, "手工精选的 Claude Code 优质资源"),
    ("x1xhlol/system-prompts-and-models-of-ai-tools", "templates", "collection", ["system-prompts"], False, "各大 AI 工具系统提示词全集:Claude Code/Cursor/Devin 等"),
    ("davepoon/buildwithclaude", "templates", "collection", ["hub"], False, "一站式发现 Claude Skills/Agents/Commands/Hooks"),
    ("glittercowboy/taches-cc-resources", "templates", "collection", ["resources"], False, "高质量 Claude Code 自定义资源合集"),
    ("trycua/acu", "templates", "collection", ["computer-use"], False, "Computer Use Agent 资源大全"),
    ("jnMetaCode/agency-agents-zh", "templates", "collection", ["roles", "chinese"], False, "277 个即插即用 AI 专家角色,支持 20+ 工具"),
    # ===== official =====
    ("anthropics/claude-plugins-official", "official", "collection", ["official", "plugins"], True, "Anthropic 官方维护的高质量 Claude 插件目录"),
    ("anthropics/claude-agent-sdk-python", "official", "agent", ["official", "sdk"], False, "Claude Agent SDK Python 版:构建自定义 coding agent"),
    # ===== Agent 框架 =====
    ("FoundationAgents/MetaGPT", "agents", "agent", ["multi-agent", "software"], True, "多智能体框架:输入一句需求,输出整个软件项目"),
    ("openai/swarm", "agents", "agent", ["openai", "educational"], False, "OpenAI 轻量多智能体编排教育框架"),
    ("microsoft/agent-framework", "agents", "agent", ["microsoft", "enterprise"], False, "微软新一代 Agent 框架:构建、编排与部署企业级智能体"),
    ("camel-ai/camel", "agents", "agent", ["multi-agent", "research"], False, "最早的多智能体框架,Agent Scaling 研究社区"),
    ("TransformerOptimus/SuperAGI", "agents", "agent", ["autonomous"], False, "开发者优先的开源自主 AI Agent 框架"),
    ("run-llama/llama_index", "agents", "agent", ["rag", "documents"], False, "领先的文档 Agent 与 OCR 平台,RAG 事实标准之一"),
    ("deepset-ai/haystack", "agents", "agent", ["orchestration"], False, "开源 AI 编排框架,构建生产级上下文应用"),
    ("JetBrains/koog", "agents", "agent", ["kotlin", "jvm"], False, "JetBrains 出品的 JVM(Kotlin/Java) Agent 框架"),
    ("kyegomez/swarms", "agents", "agent", ["multi-agent", "enterprise"], False, "企业级多智能体编排框架"),
    ("OpenBMB/XAgent", "agents", "agent", ["autonomous"], False, "面向复杂任务求解的自主 LLM Agent"),
    ("InternLM/MindSearch", "agents", "agent", ["search"], False, "多智能体搜索引擎框架,复刻 DeepResearch 体验"),
    ("MervinPraison/PraisonAI", "agents", "agent", ["low-code"], False, "低代码构建 24/7 AI 劳动力:多 Agent 编排"),
    ("omnigent-ai/omnigent", "agents", "agent", ["framework"], False, "开源 Agent 框架与 meta-harness"),
    ("Fosowl/agenticSeek", "agents", "agent", ["local", "privacy"], False, "全本地 Manus 替代品:无 API 依赖、无月费"),
    ("AstrBotDevs/AstrBot", "agents", "agent", ["chatbot", "multi-platform"], False, "多平台 AI 助手与开发框架:QQ/微信/Telegram 一站接入"),
    ("khoj-ai/khoj", "agents", "agent", ["second-brain"], False, "自托管 AI 第二大脑,连上你的笔记做研究"),
    ("CherryHQ/cherry-studio", "agents", "agent", ["desktop", "chat"], False, "AI 生产力工作室:智能对话与自主 Agent"),
    ("labring/FastGPT", "agents", "agent", ["knowledge-base"], False, "知识库驱动的 LLM 应用平台"),
    ("coze-dev/coze-studio", "agents", "agent", ["bytedance", "visual"], False, "字节 Coze 开源版:一站式可视化 Agent 开发平台"),
    ("Tencent/WeKnora", "agents", "agent", ["tencent", "knowledge"], False, "腾讯开源知识平台:原始文档到可检索智能"),
    ("assafelovic/gpt-researcher", "agents", "agent", ["research"], False, "自主深度研究 Agent:对任意数据源做深度调研"),
    ("bytedance/deer-flow", "agents", "agent", ["bytedance", "research"], True, "字节开源长程 SuperAgent harness:研究驱动智能体"),
    ("cline/cline", "agents", "agent", ["coding", "ide"], True, "自主编码 Agent:SDK、IDE 插件与 CLI 多形态"),
    ("aaif-goose/goose", "agents", "agent", ["block", "extensible"], False, "Block 开源的可扩展 AI Agent,能力超出代码范畴"),
    ("TauricResearch/TradingAgents", "agents", "agent", ["finance", "multi-agent"], False, "多智能体金融交易框架"),
    ("earendil-works/pi", "agents", "agent", ["toolkit", "tui"], False, "统一 LLM API 的 Agent 工具包:agent loop/TUI/coding"),
    ("affaan-m/ECC", "agents", "agent", ["harness"], False, "Agent harness 性能优化系统"),
    ("ruvnet/ruflo", "agents", "agent", ["workflow"], False, "最早的 agent meta-harness:智能多 Agent 工作流"),
    ("stablyai/orca", "agents", "agent", ["parallel", "ide"], False, "并行 Agent 舰队的 ADE 开发环境"),
    ("getpaseo/paseo", "agents", "agent", ["orchestration"], False, "从桌面和手机编排多个 coding agent"),
    ("superset-sh/superset", "agents", "agent", ["ide"], False, "agentic IDE:编排 100+ 编码智能体"),
    ("triggerdotdev/trigger.dev", "agents", "agent", ["background", "platform"], False, "构建全托管 AI agents 与工作流的后台平台"),
    ("alibaba/spring-ai-alibaba", "agents", "agent", ["java", "alibaba"], False, "Java 开发者的 Agentic AI 框架(阿里出品)"),
    ("TencentCloud/TencentDB-Agent-Memory", "agents", "agent", ["memory", "tencent"], False, "腾讯团队级 Agent 记忆中枢"),
    ("raga-ai-hub/RagaAI-Catalyst", "agents", "agent", ["observability"], False, "Agent 可观测性与评估平台 SDK"),
    ("openlit/openlit", "agents", "agent", ["observability"], False, "开源 AI Agent 可观测性与评估平台"),
    ("zenml-io/zenml", "agents", "agent", ["pipelines"], False, "从 Pipeline 到 Agent 的一站式 AI 平台"),
    ("dtyq/magic", "agents", "agent", ["productivity"], False, "Magicrew:首个开源一体化 AI 生产力套件"),
    ("iflytek/astron-agent", "agents", "agent", ["enterprise", "iflytek"], False, "讯飞企业级 agentic 工作流平台"),
    ("bytechefhq/bytechef", "agents", "agent", ["workflow"], False, "统一 AI Agent 编排与自动化的开源平台"),
    ("trypromptly/LLMStack", "agents", "agent", ["no-code"], False, "无代码多 Agent 框架,构建 LLM 应用"),
    ("PySpur-Dev/pyspur", "agents", "agent", ["visual"], False, "agentic 工作流可视化实验场"),
    ("HKUDS/nanobot", "agents", "agent", ["lightweight"], False, "超轻量自托管个人 AI agent"),
    ("the-open-agent/openagent", "agents", "agent", ["assistant"], False, "LLM+RAG 驱动的下一代个人 AI 助手"),
    ("nanocoai/nanoclaw", "agents", "agent", ["container"], False, "容器化运行的轻量 OpenClaw 替代"),
    ("netease-youdao/LobsterAI", "agents", "agent", ["desktop", "netease"], False, "网易有道桌面级 AI Agent:把活真干了"),
    ("osaurus-ai/osaurus", "agents", "agent", ["macos"], False, "macOS 原生 AI Agent harness,本地模型优先"),
    ("zai-org/Open-AutoGLM", "agents", "agent", ["phone", "glm"], False, "手机 Agent 模型与框架:解锁 AI Phone"),
    ("github/copilot-sdk", "agents", "agent", ["github", "sdk"], False, "多平台 SDK:把 GitHub Copilot Agent 集成到你的应用"),
    ("google/adk-go", "agents", "agent", ["go", "google"], False, "Go 版 Agent 开发套件:代码优先构建与评估"),
    # ===== Computer Use / Browser Agents =====
    ("microsoft/fara", "agents", "agent", ["microsoft", "computer-use"], False, "微软前沿 computer use 模型家族 Fara"),
    ("trycua/cua", "agents", "agent", ["computer-use"], False, "Computer Use 2.0:跨 OS 开源驱动与沙箱"),
    ("simular-ai/Agent-S", "agents", "agent", ["computer-use"], False, "像人一样使用计算机的开源 agentic 框架"),
    ("browserbase/stagehand", "agents", "agent", ["browser", "sdk"], True, "浏览器 Agent SDK:AI 浏览器自动化事实标准"),
    ("nanobrowser/nanobrowser", "agents", "agent", ["chrome-extension"], False, "AI 网页自动化开源 Chrome 扩展"),
    ("browseros-ai/BrowserOS", "agents", "agent", ["browser"], False, "开源 Agentic 浏览器:ChatGPT 浏览器版的开源替代"),
    ("steel-dev/steel-browser", "agents", "agent", ["browser", "api"], False, "面向 AI Agent 的开源浏览器 API"),
    ("hyperbrowserai/HyperAgent", "agents", "agent", ["browser", "sdk"], False, "AI 浏览器自动化 SDK"),
    ("EmergenceAI/Agent-E", "agents", "agent", ["browser", "automation"], False, "从网页开始的自动化 Agent"),
    ("nottelabs/notte", "agents", "agent", ["cloud", "browser"], False, "云端浏览器基础设施与 web 自动化平台"),
    ("lavague-ai/LaVague", "agents", "agent", ["large-action-model"], False, "Large Action Model 框架,开发 AI Web Agent"),
    ("tinyfish-io/agentql", "agents", "agent", ["scraping"], False, "把 AI 连到网页的结构化数据工具集"),
    ("spider-rs/spider", "agents", "agent", ["crawler", "rust"], False, "为 AI Agent 服务的极速网页爬取(Rust)"),
    ("yuruotong1/autoMate", "agents", "agent", ["computer-use", "macos"], False, "类 Manus 的 Computer Use Agent,自动化一切"),
    ("e2b-dev/open-computer-use", "agents", "agent", ["computer-use"], False, "开源 LLM 驱动的 AI computer use 桌面"),
    ("ghostwright/ghost-os", "agents", "agent", ["computer-use"], False, "Agent 完整 computer use 与自学习工作流"),
    ("openai/openai-cua-sample-app", "agents", "agent", ["openai", "cua"], False, "OpenAI 官方 CUA 示例应用"),
    ("feder-cr/AIHawk", "agents", "agent", ["job-hunting"], False, "开源求职浏览器 Agent:自动投递与申请"),
    ("HKUDS/DeepCode", "agents", "agent", ["coding"], False, "开源 agentic coding 引擎与 harness 研究"),
    # ===== integrations =====
    ("0x4m4/hexstrike-ai", "integrations", "agent", ["security", "mcp"], False, "AI 安全 Agent 的 MCP 服务器:百余攻击与防御工具"),
]

TODAY = "2026-09-10"

def slug_of(repo: str) -> str:
    s = repo.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

used = set()
lines = []
for repo, cat, kind, tags, featured, desc in ITEMS:
    slug = slug_of(repo)
    assert slug not in used, f"dup slug {slug}"
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

block = "\n".join(lines)
path = "data/projects.ts"
src = open(path).read()
assert src.rstrip().endswith("]"), "unexpected file ending"
src = src.rstrip()[:-1] + block + "\n]\n"
open(path, "w").write(src)
print(f"appended {len(ITEMS)} entries; slugs unique: {len(used)}")
