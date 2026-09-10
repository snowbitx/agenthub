#!/usr/bin/env python3
"""第三轮扩充:记忆/语音/研究/MCP/评测/插件生态。追加进 data/projects.ts。"""
import re

# (repo, category, kind, tags, featured, 中文描述)
ITEMS = [
    # ===== 旗舰/个人助理 =====
    ("NousResearch/hermes-agent", "agents", "agent", ["assistant", "nous"], True, "Nous Research 旗舰 Agent:与你共同成长的个人智能体"),
    ("zhayujie/CowAgent", "agents", "agent", ["assistant", "chatbot"], False, "开源超级 AI 助理与 Agent Harness:规划、执行一条龙"),
    ("tinyhumansai/openhuman", "agents", "agent", ["personal", "cross-platform"], False, "Mac/Win/Linux 全平台个人 AI"),
    ("iOfficeAI/AionUi", "agents", "agent", ["desktop", "cowork"], False, "24/7 协作应用:统一驾驭 OpenClaw/Claude Code 等智能体"),
    ("holaboss-ai/holaOS", "agents", "agent", ["workspace", "enterprise"], False, "企业可私有化的开源 agentic 工作区"),
    # ===== 记忆层(新生态位) =====
    ("mem0ai/mem0", "agents", "agent", ["memory", "infrastructure"], True, "AI Agent 记忆层事实标准:即插即用的记忆基础设施"),
    ("letta-ai/letta", "agents", "agent", ["memory", "stateful"], False, "有状态 Agent 平台:自带高级记忆的 AI(MemGPT 团队)"),
    ("MemTensor/MemOS", "agents", "agent", ["memory", "os"], False, "自进化的 Agent 记忆操作系统:超持久记忆"),
    ("memvid/memvid", "agents", "agent", ["memory", "video"], False, "用视频做记忆层:取代复杂 RAG 管线"),
    ("MemoriLabs/Memori", "agents", "agent", ["memory", "sql"], False, "Agent 原生记忆基础设施,LLM 无关"),
    ("EverMind-AI/EverOS", "agents", "agent", ["memory", "local-first"], False, "可移植的 Agent 记忆层:本地优先"),
    ("activeloopai/deeplake", "agents", "agent", ["data", "vector"], False, "Agent 的 AI 数据运行时:向量检索服务化"),
    # ===== 深度研究 Agent(新生态位) =====
    ("Alibaba-NLP/DeepResearch", "agents", "agent", ["research", "alibaba"], True, "通义深度研究:领先的开源 Deep Research 智能体"),
    ("dzhng/deep-research", "agents", "agent", ["research"], False, "迭代式深度研究助手:广度优先搜索+反思"),
    ("assafelovic/gpt-researcher", None, None, None, None, None),  # 已入库,占位跳过
    ("zilliztech/deep-searcher", "agents", "agent", ["research", "zilliz"], False, "Zilliz 开源深度搜索:推理+检索一体"),
    ("MiroMindAI/MiroThinker", "agents", "agent", ["research"], False, "面向复杂问题的深度研究智能体"),
    ("nickscamara/open-deep-research", "agents", "agent", ["research", "openai"], False, "OpenAI Deep Research 的开源复刻"),
    ("virattt/dexter", "agents", "agent", ["finance", "research"], False, "自主金融深度研究智能体"),
    ("xbtlin/ai-berkshire", "agents", "agent", ["finance", "chinese"], False, "AI 时代价值投资研究框架:巴菲特/芒格/段永平/李录思维"),
    ("hsliuping/TradingAgents-CN", "agents", "agent", ["finance", "chinese"], False, "多智能体中文金融交易框架"),
    # ===== 语音 Agent(新生态位) =====
    ("pipecat-ai/pipecat", "agents", "agent", ["voice", "realtime"], True, "最流行的开源语音 Agent 框架:实时多模态应用"),
    ("livekit/agents", "agents", "agent", ["voice", "realtime"], False, "LiveKit 实时语音 AI Agent 框架"),
    ("TEN-framework/ten-framework", "agents", "agent", ["voice", "conversational"], False, "开源对话式语音 Agent 框架(TEN)"),
    ("huggingface/speech-to-speech", "agents", "agent", ["voice", "opensource"], False, "用全开源模型搭建语音 Agent(HF 官方)"),
    ("GetStream/Vision-Agents", "agents", "agent", ["voice", "vision"], False, "Stream 开源语音+视觉 Agent SDK"),
    ("PatterAI/Patter", "agents", "agent", ["voice", "sdk"], False, "开源语音 AI SDK:Vapi/Retell 的开源替代"),
    # ===== MCP / RAG / 检索 =====
    ("punkpeye/awesome-mcp-servers", "integrations", "collection", ["awesome", "mcp"], True, "最全 MCP server 合集(数万个工具的入口清单)"),
    ("pathwaycom/pathway", "integrations", "agent", ["etl", "realtime"], False, "实时流处理 ETL 框架,常用于 RAG 与 Agent 数据管道"),
    ("llmware-ai/llmware", "integrations", "agent", ["rag", "enterprise"], False, "企业 RAG 管线统一框架:小模型+检索对齐"),
    ("The-Vibe-Company/quivr", "integrations", "agent", ["rag"], False, "把 GenAI 集成进应用的 RAG 框架"),
    ("neuml/txtai", "integrations", "agent", ["search", "rag"], False, "语义搜索/LLM 编排/工作流一体化 AI 框架"),
    ("OpenSPG/KAG", "integrations", "agent", ["knowledge-graph", "rag"], False, "逻辑形式引导的知识增强生成框架(蚂蚁系)"),
    ("Marker-Inc-Korea/AutoRAG", "integrations", "agent", ["rag", "auto"], False, "自动为你的数据找到最优 RAG 管线"),
    # ===== 评测/可观测(新生态位) =====
    ("mlflow/mlflow", "agents", "agent", ["evaluation", "platform"], False, "老牌 ML 平台全面转向:Agent 与 LLM 工程一体化"),
    ("coze-dev/coze-loop", "agents", "agent", ["evaluation", "bytedance"], False, "字节新一代 Agent 评测与优化平台"),
    # ===== Claude Code 插件/工具生态 =====
    ("wshobson/agents", "devtools", "collection", ["plugins", "marketplace"], True, "多 harness 兼容的 Agent 插件市场:80+ 领域专家子智能体"),
    ("alirezarezvani/claude-skills", "devtools", "collection", ["skills", "plugins"], False, "380 个 Claude Code Skills 与插件(30+ Agent 工具)"),
    ("jarrodwatts/claude-hud", "devtools", "agent", ["plugin", "context"], False, "Claude Code 状态 HUD 插件:实时显示上下文/任务/变更"),
    ("EveryInc/compound-engineering-plugin", "devtools", "collection", ["engineering", "official"], False, "官方 Compound Engineering 插件:工程流程增强"),
    ("YishenTu/claudian", "devtools", "agent", ["obsidian"], False, "把 Claude Code/Codex 嵌入 Obsidian 的插件"),
    ("ykdojo/claude-code-tips", "docs", "collection", ["tips"], False, "45+ 条 Claude Code 实战技巧(从基础到高级)"),
    ("wanshuiyin/Auto-claude-code-research-in-sleep", "devtools", "agent", ["automation", "research"], False, "睡觉时自动做研究的轻量编排工具(ARIS)"),
    ("UfoMiao/zcf", "devtools", "agent", ["config", "workflow"], False, "Claude Code & Codex 零配置工作流切换器"),
    ("zhukunpenglinyutong/jetbrains-cc-gui", "devtools", "agent", ["jetbrains", "gui"], False, "JetBrains 的 Claude Code/Codex 图形界面插件"),
    ("trailhq/Graft", "devtools", "agent", ["context", "sdk"], False, "为 Claude Code/Cursor/Codex 提速的上下文引擎"),
    ("hashicorp/agent-skills", "devtools", "collection", ["hashicorp", "devops"], False, "HashiCorp 官方 Agent Skills:Terraform/Vault 工作流"),
    ("microsoft/power-platform-skills", "devtools", "collection", ["microsoft", "power-platform"], False, "微软官方 Power Platform Skills 插件市场"),
    ("K-Dense-AI/scientific-agent-skills", "devtools", "collection", ["science"], False, "把任意 AI Agent 变成 AI 科学家:科研 Skills 头部项目"),
    ("data-goblin/power-bi-agentic-development", "devtools", "collection", ["powerbi"], False, "Power BI 的 agentic 开发 Skills 与 Agents"),
    ("freshtechbro/claudedesignskills", "creative", "collection", ["design"], False, "现代设计工作的 Claude Code Skills 合集"),
    # ===== 更多平台/框架 =====
    ("danny-avila/LibreChat", "agents", "agent", ["chat", "multi-model"], False, "增强版多模型聊天平台:Agents/MCP/Skills 全支持"),
    ("ToolJet/ToolJet", "agents", "agent", ["low-code", "platform"], False, "企业级低代码平台的 AI 内核"),
    ("dataelement/bisheng", "agents", "agent", ["platform", "chinese"], False, "开源 LLM DevOps 平台:下一代企业智能体"),
    ("genkit-ai/genkit", "agents", "agent", ["typescript", "google"], False, "Google 开源的 agentic 应用框架(JS/Go/Python)"),
    ("VoltAgent/voltagent", "agents", "agent", ["typescript", "platform"], False, "开源 TypeScript Agent 工程平台"),
    ("GoogleCloudPlatform/agent-starter-pack", "agents", "collection", ["gcp", "starter"], False, "Google 官方 Agent 启动包:几分钟上云生产级智能体"),
    ("langchain4j/langchain4j", "agents", "agent", ["java"], False, "Java 生态的 LangChain:惯用地道开源库"),
    ("aiwaves-cn/agents", "agents", "agent", ["self-evolving"], False, "数据中心的自我进化 Agent 框架"),
    ("golutra/golutra", "agents", "agent", ["orchestration"], False, "多智能体编排平台:自动化与工作流"),
    ("UnicomAI/wanwu", "agents", "agent", ["enterprise", "chinese"], False, "联通元景万物:企业级 Agent 平台"),
    ("hexabot-ai/Hexabot", "agents", "agent", ["chatbot", "workflow"], False, "AI 工作流自动化平台:聊天智能体创建管理"),
    ("arc53/DocsGPT", "agents", "agent", ["docs", "assistant"], False, "私有化文档问答智能体平台"),
    ("rocketride-org/rocketride-server", "agents", "agent", ["pipeline", "cpp"], False, "C++ 内核高性能 AI 管线引擎"),
    # ===== 浏览器/设备补充 =====
    ("ntegrals/openbrowser", "agents", "agent", ["browser"], False, "让 AI 自主浏览网页的工具包"),
    ("keon/browser-control", "agents", "agent", ["browser", "rust"], False, "极小极快的 Rust CLI:驱动真实浏览器"),
    ("platonai/Browser4", "agents", "agent", ["browser", "engine"], False, "AI 原生浏览器引擎,面向自主 Agent"),
    ("showlab/computer_use_ootb", "agents", "agent", ["computer-use", "gui"], False, "开箱即用的 GUI Agent:Windows/macOS"),
    ("showlab/ShowUI", "agents", "agent", ["vision-language", "cvpr"], False, "CVPR 2025:端到端视觉-语言-动作模型"),
    ("TurixAI/TuriX-CUA", "agents", "agent", ["computer-use"], False, "TuriX 计算机使用智能体"),
    ("Open-Source-Legal/OpenContracts", "agents", "agent", ["legal", "documents"], False, "开放文档智能平台:法律文档解析"),
    ("tambo-ai/tambo", "agents", "agent", ["generative-ui", "react"], False, "React 生成式 UI SDK:Agent 驱动界面"),
    # ===== 安全 =====
    ("PurpleAILAB/Decepticon", "devtools", "agent", ["security", "red-team"], False, "红队自主渗透测试 Agent"),
    ("zhaoxuya520/reverse-skill", "devtools", "collection", ["security", "reverse"], False, "逆向工程与授权渗透测试 Skills"),
]

TODAY = "2026-09-10"

def slug_of(repo: str) -> str:
    s = repo.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

ts_path = "data/projects.ts"
src = open(ts_path).read()
existing = set(re.findall(r"github\.com/([\w.-]+/[\w.-]+)'".replace("\\x27", "'"), src))

lines = []
added = 0
used = set(re.findall(r"slug: '([^']+)'", src))
for row in ITEMS:
    repo, cat, kind, tags, featured, desc = row
    if cat is None:
        continue
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
