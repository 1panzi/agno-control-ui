# 组件映射表：项目 Builder ↔ Agno 参考源码

> 本文档记录项目 `backend/builders/` 中已实现的组件与 agno 仓库 `reference_projects/agno/libs/agno/agno/` 中可用组件的对应关系。
> 用于快速查看覆盖率和待添加的组件。
>
> **最后更新**: 2026-05-11 | **agno commit**: 3bb249c28

---

## 模型（Model）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `openai` | `models/openai/` | ✅ 已实现 |
| `anthropic` | `models/anthropic/` | ✅ 已实现 |
| `ollama` | `models/ollama/` | ✅ 已实现 |
| `groq` | `models/groq/` | ✅ 已实现 |
| `deepseek` | `models/deepseek/` | ✅ 已实现 |
| `mistral` | `models/mistral/` | ✅ 已实现 |
| `azure` | `models/azure/` | ✅ 已实现 |
| `cohere` | `models/cohere/` | ✅ 已实现 |
| `together` | `models/together/` | ✅ 已实现 |
| `openai_like` | `models/openai/`（自定义 base_url） | ✅ 已实现 |
| `google` | `models/google/` (Gemini) | ✅ 已实现 |
| `aws` | `models/aws/` (Bedrock) | ✅ 已实现 |
| `huggingface` | `models/huggingface/` | ✅ 已实现 |
| `litellm` | `models/litellm/` | ✅ 已实现 |
| `fireworks` | `models/fireworks/` | ✅ 已实现 |
| `cerebras` | `models/cerebras/` | ✅ 已实现 |
| `nvidia` | `models/nvidia/` | ✅ 已实现 |
| `vertexai` | `models/vertexai/` | ✅ 已实现 |
| `openrouter` | `models/openrouter/` | ✅ 已实现 |
| `perplexity` | `models/perplexity/` | ✅ 已实现 |
| `xai` | `models/xai/` | ✅ 已实现 |
| `sambanova` | `models/sambanova/` | ✅ 已实现 |
| `siliconflow` | `models/siliconflow/` | ✅ 已实现 |
| `dashscope` | `models/dashscope/` | ✅ 已实现 |
| `moonshot` | `models/moonshot/` | ✅ 已实现 |
| `deepinfra` | `models/deepinfra/` | ✅ 已实现 |
| `ibm` | `models/ibm/` (WatsonX) | ✅ 已实现 |
| `meta` | `models/meta/` (Llama) | ✅ 已实现 |
| `vllm` | `models/vllm/` | ✅ 已实现 |
| `llama_cpp` | `models/llama_cpp/` | ✅ 已实现 |
| `lmstudio` | `models/lmstudio/` | ✅ 已实现 |
| `internlm` | `models/internlm/` | ✅ 已实现 |
| `nebius` | `models/nebius/` | ✅ 已实现 |
| `portkey` | `models/portkey/` | ✅ 已实现 |
| `aimlapi` | `models/aimlapi/` | ✅ 已实现 |
| `cometapi` | `models/cometapi/` | ✅ 已实现 |
| `langdb` | `models/langdb/` | ✅ 已实现 |
| `n1n` | `models/n1n/` | ✅ 已实现 |
| `neosantara` | `models/neosantara/` | ✅ 已实现 |
| `nexus` | `models/nexus/` | ✅ 已实现 |
| `requesty` | `models/requesty/` | ✅ 已实现 |

**覆盖率**: 41/41 ✅

---

## 嵌入器（Embedder）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `openai` | `knowledge/embedder/openai.py` | ✅ 已实现 |
| `azure` | `knowledge/embedder/azure_openai.py` | ✅ 已实现 |
| `ollama` | `knowledge/embedder/ollama.py` | ✅ 已实现 |
| `cohere` | `knowledge/embedder/cohere.py` | ✅ 已实现 |
| `google` | `knowledge/embedder/google.py` | ✅ 已实现 |
| `aws_bedrock` | `knowledge/embedder/aws_bedrock.py` | ✅ 已实现 |
| `fireworks` | `knowledge/embedder/fireworks.py` | ✅ 已实现 |
| `huggingface` | `knowledge/embedder/huggingface.py` | ✅ 已实现 |
| `jina` | `knowledge/embedder/jina.py` | ✅ 已实现 |
| `mistral` | `knowledge/embedder/mistral.py` | ✅ 已实现 |
| `nebius` | `knowledge/embedder/nebius.py` | ✅ 已实现 |
| `openai_like` | `knowledge/embedder/openai_like.py` | ✅ 已实现 |
| `together` | `knowledge/embedder/together.py` | ✅ 已实现 |
| `fastembed` | `knowledge/embedder/fastembed.py` | ✅ 已实现 |
| `sentence_transformer` | `knowledge/embedder/sentence_transformer.py` | ✅ 已实现 |
| `vllm` | `knowledge/embedder/vllm.py` | ✅ 已实现 |
| `voyageai` | `knowledge/embedder/voyageai.py` | ✅ 已实现 |
| `langdb` | `knowledge/embedder/langdb.py` | ✅ 已实现 |

**覆盖率**: 18/18 ✅

---

## 向量数据库（VectorDB）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `pgvector` | `vectordb/pgvector/` | ✅ 已实现 |
| `qdrant` | `vectordb/qdrant/` | ✅ 已实现 |
| `chroma` | `vectordb/chroma/` | ✅ 已实现 |
| `pinecone` | `vectordb/pineconedb/` | ✅ 已实现 |
| `weaviate` | `vectordb/weaviate/` | ✅ 已实现 |
| `milvus` | `vectordb/milvus/` | ✅ 已实现 |
| `mongodb` | `vectordb/mongodb/` | ✅ 已实现 |
| `lancedb` | `vectordb/lancedb/` | ✅ 已实现 |
| `cassandra` | `vectordb/cassandra/` | ✅ 已实现 |
| `clickhouse` | `vectordb/clickhouse/` | ✅ 已实现 |
| `couchbase` | `vectordb/couchbase/` | ✅ 已实现 |
| `langchaindb` | `vectordb/langchaindb/` | ✅ 已实现（schema-only） |
| `lightrag` | `vectordb/lightrag/` | ✅ 已实现 |
| `llamaindex` | `vectordb/llamaindex/` | ✅ 已实现（schema-only） |
| `redis` | `vectordb/redis/` | ✅ 已实现 |
| `singlestore` | `vectordb/singlestore/` | ✅ 已实现 |
| `surrealdb` | `vectordb/surrealdb/` | ✅ 已实现 |
| `upstashdb` | `vectordb/upstashdb/` | ✅ 已实现 |

**覆盖率**: 18/18 ✅

---

## 数据库（DB / Storage）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `sqlite` | `db/sqlite/` | ✅ 已实现 |
| `postgres` | `db/postgres/` | ✅ 已实现 |
| `in_memory` | `db/in_memory/` | ✅ 已实现 |
| `async_postgres` | `db/async_postgres/` | ✅ 已实现 |
| `dynamo` | `db/dynamo/` | ✅ 已实现 |
| `firestore` | `db/firestore/` | ✅ 已实现 |
| `gcs_json` | `db/gcs_json/` | ✅ 已实现 |
| `json` | `db/json/` | ✅ 已实现 |
| `mongo` | `db/mongo/` | ✅ 已实现 |
| `mysql` | `db/mysql/` | ✅ 已实现 |
| `redis` | `db/redis/` | ✅ 已实现 |
| `singlestore` | `db/singlestore/` | ✅ 已实现 |
| `surrealdb` | `db/surrealdb/` | ✅ 已实现 |

**覆盖率**: 13/13 ✅

---

## 读取器（Reader）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `pdf` | `knowledge/reader/pdf_reader.py` | ✅ 已实现 |
| `docx` | `knowledge/reader/docx_reader.py` | ✅ 已实现 |
| `text` | `knowledge/reader/text_reader.py` | ✅ 已实现 |
| `csv` | `knowledge/reader/csv_reader.py` | ✅ 已实现 |
| `json` | `knowledge/reader/json_reader.py` | ✅ 已实现 |
| `website` | `knowledge/reader/website_reader.py` | ✅ 已实现 |
| `youtube` | `knowledge/reader/youtube_reader.py` | ✅ 已实现 |
| `arxiv` | `knowledge/reader/arxiv_reader.py` | ✅ 已实现 |
| `docling` | `knowledge/reader/docling_reader.py` | ✅ 已实现 |
| `excel` | `knowledge/reader/excel_reader.py` | ✅ 已实现 |
| `field_labeled_csv` | `knowledge/reader/field_labeled_csv_reader.py` | ✅ 已实现 |
| `firecrawl` | `knowledge/reader/firecrawl_reader.py` | ✅ 已实现 |
| `llms_txt` | `knowledge/reader/llms_txt_reader.py` | ✅ 已实现 |
| `markdown` | `knowledge/reader/markdown_reader.py` | ✅ 已实现 |
| `pptx` | `knowledge/reader/pptx_reader.py` | ✅ 已实现 |
| `s3` | `knowledge/reader/s3_reader.py` | ✅ 已实现 |
| `tavily` | `knowledge/reader/tavily_reader.py` | ✅ 已实现 |
| `web_search` | `knowledge/reader/web_search_reader.py` | ✅ 已实现 |
| `wikipedia` | `knowledge/reader/wikipedia_reader.py` | ✅ 已实现 |

**覆盖率**: 19/19 ✅

---

## 工具集（Toolkit）

项目通过 `TOOLKIT_CATALOG` 动态注册，使用 `GenericToolkitBuilder` 按 type 懒加载。

**已注册工具数**: 约 120 个（见 `backend/builders/toolkits/catalog.py`）

另有 `("toolkit", "custom")` 支持自定义工具定义。

agno 源码中全部用户侧 tools（`agno/tools/*.py`）已基本全覆盖。

未收录的为 agno 内部基础模块（`mcp_toolbox`、`decorator`、`function`、`toolkit`、`tool_registry`、`parallel`、`workflow`、`workspace`），非用户侧工具，无需注册。

**覆盖率**: ~98% ✅

---

## Agent

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `agent/agent.py` | ✅ 已实现 |

---

## Team

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `team/team.py` | ✅ 已实现 |

---

## Memory

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `memory/manager.py` | ✅ 已实现 |

---

## Learn（学习机器）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `learn/machine.py` | ✅ 已实现 |

---

## Knowledge（知识库）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `knowledge/knowledge.py` | ✅ 已实现 |

---

## Reasoning（推理）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `reasoning/manager.py` + 各 provider | ✅ 已实现 |

---

## Compression（压缩）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `compression/manager.py` | ✅ 已实现 |

---

## Culture（文化）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `culture/manager.py` | ✅ 已实现 |

---

## Guardrails（守卫）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `openai_moderation` | `guardrails/openai.py` | ✅ 已实现 |
| `pii_detection` | `guardrails/pii.py` | ✅ 已实现 |
| `prompt_injection` | `guardrails/prompt_injection.py` | ✅ 已实现 |

**覆盖率**: 3/3 ✅

---

## Session Summary（会话摘要）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `session/summary.py` | ✅ 已实现 |

---

## Skills（技能）

| 项目 Builder type | agno 源码路径 | 状态 |
|---|---|---|
| `base` | `skills/skill.py` | ✅ 已实现 |

---

## 未纳入管理的 agno 模块

以下 agno 顶层模块在项目中**没有对应的 builder 类别**（不需要通过资源管理配置）：

| agno 模块 | 说明 | 是否需要 Builder |
|---|---|---|
| `workflow/` | Workflow 编排 | ⚠️ 可能需要（当前 team 接管） |
| `approval/` | 人工审批流程 | 可选 |
| `context/` | 上下文管理 | 内部使用，无需 |
| `eval/` | 评估框架 | 开发工具，无需 |
| `factory/` | Agent/Team 工厂 | 内部使用，无需 |
| `hooks/` | 钩子系统 | 内部使用，无需 |
| `integrations/` | 第三方集成 | 可选 |
| `os/` | AgentOS | 已直接使用，无需 Builder |
| `registry/` | 注册表 | 已直接使用，无需 Builder |
| `remote/` | 远程 Agent | 可选 |
| `run/` | 运行管理 | 内部使用，无需 |
| `scheduler/` | 调度器 | 可选 |
| `tracing/` | 链路追踪 | 可选 |

---

## 总览

| 类别 | 已实现 | agno 可用 | 覆盖率 |
|---|---|---|---|
| Model | 41 | 41 | 100% |
| Embedder | 18 | 18 | 100% |
| VectorDB | 18 | 18 | 100% |
| DB/Storage | 13 | 13 | 100% |
| Reader | 19 | 19 | 100% |
| Toolkit | ~120 | ~120 | ~98% |
| Agent | 1 | 1 | 100% |
| Team | 1 | 1 | 100% |
| Memory | 1 | 1 | 100% |
| Learn | 1 | 1 | 100% |
| Knowledge | 1 | 1 | 100% |
| Reasoning | 1 | 1 | 100% |
| Compression | 1 | 1 | 100% |
| Culture | 1 | 1 | 100% |
| Guardrails | 3 | 3 | 100% |
| Session Summary | 1 | 1 | 100% |
| Skills | 1 | 1 | 100% |
