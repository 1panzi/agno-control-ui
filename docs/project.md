# Project Constraints

## 1. 项目概述

**agno-platform** — 基于 [Agno](https://github.com/agno-agi/agno) 框架的 Agent 管理平台。

- **后端**: FastAPI + SQLAlchemy + SQLite（开发）/ PostgreSQL（生产）
- **前端**: Vue 3 + TypeScript + Element Plus + Vite
- **Python**: >= 3.12，包管理用 `uv`
- **后端端口**: 8006（开发），前端端口: 5173

---

## 2. 架构约束

### 2.1 后端

- **响应格式统一**: 所有自定义 API 必须返回 `R[T]` 格式（`core/response.py`），禁止直接返回裸数据。
- **异常处理**: 业务异常通过 `AppException` 抛出，由全局 handler 统一处理，禁止在路由层 try/catch 后返回自定义格式。
- **配置管理**: 所有环境变量通过 `core/config.py` 的 `Settings` 读取，禁止在业务代码中直接读 `os.environ`。
- **数据库（agno 接管）**: 使用 `agno.db.sqlite.SqliteDb`（开发）/ `agno.db.postgres.PostgresDb`（生产）作为统一数据库实例，由 `AgentOS` 负责建表和生命周期管理，不再使用 SQLAlchemy `Base.metadata.create_all`。`ag_resources` 表（自定义资源管理）通过单独的 SQLAlchemy engine 维护，与 agno 表并存于同一数据库文件。
- **FastAPI（agno 接管）**: `main.py` 先创建自定义 `FastAPI` 实例挂载自定义路由，再作为 `base_app` 传给 `AgentOS`，通过 `agent_os.get_app()` 获取最终 app。启动改用 `agent_os.serve()`。
- **PYTHONPATH**: `pyproject.toml` 和 `uv.lock` 在 `backend/`，所有后端命令须在 `backend/` 目录下用 `uv run` 执行。

#### agno 源码路径

需要查阅 agno 源码时，优先使用项目内的 submodule：

```
reference_projects/agno/libs/agno/agno/
```

关键子路径：

| 功能 | 路径 |
|---|---|
| AgentOS 入口 | `os/app.py` |
| components CRUD 路由 | `os/routers/components/components.py` |
| 数据库基类 | `db/base.py` |
| SQLite 实现 | `db/sqlite/sqlite.py` |
| PostgreSQL 实现 | `db/postgres/postgres.py` |
| 表结构定义 | `db/sqlite/schemas.py` |
| OS schema | `os/schema.py` |
| Agent 实现 | `agent/agent.py` |
| Registry | `registry/` |
| Knowledge | `knowledge/` |
| Memory | `memory/` |

#### agno Cookbook

各模块的使用示例在 submodule 的 cookbook 目录下：

```
reference_projects/agno/cookbook/
```

| 目录 | 内容 |
|---|---|
| `02_agents/` | Agent 基础用法 |
| `03_teams/` | Team 多 Agent 协作 |
| `04_workflows/` | Workflow 编排 |
| `05_agent_os/` | AgentOS / base_app 集成 |
| `06_storage/` | 数据库存储 |
| `07_knowledge/` | 知识库 / RAG |
| `08_learning/` | LearningMachine |
| `10_reasoning/` | Reasoning |
| `11_memory/` | Memory Manager |
| `90_models/` | 各 LLM 接入示例 |
| `91_tools/` | Toolkit 工具用法 |
| `93_components/` | 组件配置示例 |

### 2.2 前端

- **HTTP 封装**: 所有请求必须通过 `frontend/src/shared/utils/request.ts`，自动解包 `R[T].data`，禁止直接使用裸 axios。
- **API 路径**: 函数内不带 `/api/v1` 前缀（由 `request.ts` baseURL 统一注入）。
- **UI 风格**: 深色主题（`#0d1117` / `#0f172a`），Element Plus 组件库，不引入其他 UI 框架。
- **模块结构**: 新功能模块放 `frontend/src/modules/<name>/`，包含 `api.ts`、`types.ts`、`views/`。

---

## 3. 开发命令

### 3.1 启动服务

```bash
# 后端（backend/ 目录）
cd backend && uv run python run.py
# 或
cd backend && uv run uvicorn main:app --host 0.0.0.0 --port 8006 --reload

# 前端
cd frontend && npm run dev
```

### 3.2 测试

```bash
# 单元测试（pytest，使用 SQLite test.db，无需启动服务）
cd backend && uv run pytest

# 集成测试脚本（需要服务运行 + 真实 LLM）
cd backend && uv run python scripts/agent_chat.py
cd backend && uv run python scripts/agent_tools.py
```

**修改后必须运行的检查：**

| 改动范围 | 需要运行 |
|---|---|
| 后端 core / api 层 | `cd backend && uv run pytest` |
| Agent / ModelConfig 逻辑 | `cd backend && uv run pytest` + `scripts/agent_chat.py` |
| 前端组件 | `npm run type-check` + `npm run lint` |
| 任何改动 | `cd backend && uv run pytest`（最低要求） |

### 3.3 代码格式化

```bash
# 后端（如已安装 ruff）
cd backend && ruff format . && ruff check .

# 前端
cd frontend && npm run lint && npm run format
```

---

## 4. 环境变量

文件：`backend/.env`

```bash
DATABASE_URL=sqlite:///./local.db          # 开发用 SQLite
API_CORS_ORIGINS=["http://localhost:5173"]
# 可选
VECTOR_DB_URL=                             # 空则复用 DATABASE_URL
EMBEDDER_BASE_URL=
EMBEDDER_API_KEY=
EMBEDDER_MODEL=BAAI/bge-large-zh-v1.5
EMBEDDER_DIMENSIONS=1024
```

测试环境自动使用 `DATABASE_URL=sqlite:///./test.db`（见 `pyproject.toml` `[tool.pytest.ini_options]`）。

---

## 5. 沟通规范

- **语言**: 所有与用户的沟通、代码注释、Git commit 消息均使用**中文**。
- **Commit 规范**: 遵循 `docs/git-commit.md` 的 Conventional Commits 规范。
