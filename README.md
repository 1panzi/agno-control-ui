# Agno Platform

基于 [Agno](https://github.com/agno-agi/agno) 框架构建的 Agent 资源管理与控制面板（Dashboard），提供 Web UI 对 16 种 Agno 组件进行统一 CRUD 管理，并内置聊天调试界面。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI + AgentOS（Agno 应用内核） |
| 数据库 | SQLite（开发）/ PostgreSQL（生产），Agno 原生 ORM + SQLAlchemy 双轨 |
| 前端框架 | Vue 3.5 + TypeScript + Element Plus |
| 构建工具 | Vite 7 |
| 包管理 | Python: `uv` / Node: `npm` |

## 项目结构

```
agno-manage/
├── backend/                    # 后端（FastAPI + AgentOS）
│   ├── main.py                 #   应用入口：创建 FastAPI → AgentOS 接管 → serve
│   ├── run.py                  #   开发启动脚本
│   ├── core/                   #   配置 / 数据库 / 异常 / 响应 / 日志 / RefResolver
│   ├── api/v1/                 #   自定义 API 路由（资源 CRUD / Schema / Debug）
│   ├── builders/               #   Agno 组件构造器（16 类组件各一个 builder）
│   │   ├── builder_registry.py #     构造器注册表
│   │   ├── agents/ teams/ workflows/ models/ ...  # 各组件 Builder 实现
│   ├── catalog/                #   Schema 定义（每种组件类型配置了哪些字段）
│   ├── resources/              #   自定义资源存储层（model / schema / crud / service）
│   ├── tests/                  #   单元测试（pytest）
│   └── scripts/                #   集成测试脚本（agent_chat / agent_tools）
├── frontend/                   # 前端（Vue 3 + TypeScript + Element Plus）
│   └── src/
│       ├── api/                #   HTTP 层（自定义资源 API + Agno 原生 API）
│       ├── views/
│       │   ├── chat/           #   聊天页（Agent/Team/Workflow 调试）
│       │   └── resources/      #   统一资源管理页 + 动态表单组件
│       ├── components/         #   通用组件（LazySelect / Pagination）
│       ├── layouts/            #   主布局（侧边栏 + 内容区）
│       ├── router/             #   路由（Hash 模式，21 条路由）
│       └── store/              #   Pinia 状态管理
├── reference_projects/agno/    # Agno 源码 submodule
└── docs/                       # 项目文档（project.md / frontend.md）
```

## 核心功能

### 统一资源管理

v2 架构将 16 种 Agno 组件（Agent、Team、Workflow、Model、Embedder、VectorDB、Knowledge、Toolkit、Reader、Skill、Memory、Learn、Reasoning、Guardrail、Culture、Compress、SessionSummary）统一抽象为"资源"，共用一套 CRUD 页面：

- **列表页**：表格展示 + 搜索 + 批量启用/停用 + 分页
- **创建/编辑**：Schema 驱动的动态表单，后端定义字段类型，前端自动渲染
- **详情面板**：el-descriptions 展示完整配置

### 动态表单（Schema-Driven）

后端 `catalog/` 定义每个组件类型有哪些配置字段及其类型（`str` / `int` / `bool` / `select` / `ref_or_inline`），前端 `DynamicFormRenderer` 根据字段定义自动生成表单，支持：

- **嵌套引用**：`ref_or_inline` 字段支持引用已有资源、内联创建、或引用后覆盖部分字段
- **条件显示**：`depends_on` 实现字段间的条件联动
- **递归校验**：多层嵌套表单的提交前自动校验

### 聊天调试

内置双栏聊天界面，直接调试 Agent / Team / Workflow：

- 组件选择 → 会话列表 → 消息区域
- 普通请求 + SSE 流式输出
- 流式进度面板（RunStarted → ModelRequest → ToolCall → RunCompleted）
- 文件附件上传
- 会话管理（新建、切换、重命名、删除）
- Markdown 渲染 + 代码块主题切换

### Agno API 调试面板

内置 `/api/v1/agno_manage/debug/endpoints` 页面，展示全部 Agno 内部 API 分组，可在线测试各接口。

## 核心流程

### 启动流程

```
main.py
  ├── 创建 FastAPI 实例 → 挂载自定义路由（/api/v1/agno_manage/*）
  ├── 创建 AgentOS(base_app) → 挂载 Agno 原生路由（/agents, /teams, ...）
  ├── warm_up: 从 ag_resources 表加载启用的 Agent/Team 到 Registry
  └── agent_os.serve() → 启动 uvicorn
```

### 资源创建流程

```
用户填写表单 → ResourceFormDialog
  → 查 Schema（GET /schema?category=agent&type=openai_agent）
  → DynamicFormRenderer 渲染匹配字段的表单
  → 提交 POST /resources/create { category, type, name, config, ... }
  → 后端 Builder 解析 config → 调用 Agno SDK 创建组件实例
  → 写入 ag_resources 表 + Agno 原生表
```

### 聊天流程

```
用户输入消息 → POST /agents/:id/runs (FormData: message + stream + session_id)
  → Agno RunService 执行 Agent.run()
  → 流式模式: SSE 事件流（RunStarted → ModelRequest → ToolCall → RunCompleted）
  → 前端 markstream-vue 逐 token 渲染 markdown
```

## 快速开始

### 环境要求

- Python >= 3.12 + [uv](https://docs.astral.sh/uv/)
- Node.js >= 18 + npm

### 1. 克隆并初始化

```bash
git clone <repo-url> && cd agno-manage

# 拉取 Agno submodule
git submodule update --init reference_projects/agno

# 安装后端依赖
cd backend && uv sync && cd ..

# 安装前端依赖
cd frontend && npm install && cd ..
```

### 2. 配置环境变量

在 `backend/.env` 中设置（开发环境使用 SQLite，无需额外配置）：

```bash
DATABASE_URL=sqlite:///./local.db
API_CORS_ORIGINS=["http://localhost:5173"]

# 可选：配置 LLM API Key（模型通过 Web UI 创建，此处仅为默认值）
```

### 3. 启动开发服务

```bash
# 终端 1：后端（端口 8006）
cd backend && uv run python run.py

# 终端 2：前端（端口 5173）
cd frontend && npm run dev
```

浏览器打开 `http://localhost:5173` 即可访问。

### 4. 运行测试

```bash
# 后端单元测试（使用 test.db，无需启动服务）
cd backend && uv run pytest

# 前后端代码检查
cd backend && ruff check . && ruff format --check .
cd frontend && npm run type-check && npm run lint
```

## 开发规范

- 所有自定义 API 返回统一格式 `R[T]`（`{ code, data, msg }`）
- 业务异常通过 `AppException` 抛出，由全局 handler 统一处理
- 前端 HTTP 请求使用封装的 Axios 实例，不直接使用裸 axios
- Git Commit 遵循 [Conventional Commits](https://www.conventionalcommits.org/)
- 代码注释和沟通使用中文

更多细节见 `docs/project.md` 和 `docs/frontend.md`。
