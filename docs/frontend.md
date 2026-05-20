# 前端架构文档

## 项目概述

基于 Vue 3 + TypeScript + Element Plus 构建的 Agno Platform 前端管理界面。
v2 重构后采用**统一资源管理**架构，所有 agno 组件（agent、team、model、knowledge 等 16 种）
共用一套通用 CRUD 页面 + 动态表单渲染，不再按功能模块拆分。

## 技术栈

- **框架**: Vue 3.5 (Composition API, `<script setup>`)
- **语言**: TypeScript 5.9
- **UI 库**: Element Plus 2.13 + @element-plus/icons-vue
- **构建工具**: Vite 7
- **路由**: Vue Router 5（Hash 模式）
- **状态管理**: Pinia 3 + pinia-plugin-persistedstate
- **HTTP 客户端**: Axios（双实例：自定义 API + Agno API）
- **Markdown 渲染**: markstream-vue（聊天消息流式渲染）
- **自动导入**: unplugin-auto-import（vue/vue-router/pinia）、unplugin-vue-components（Element Plus）

## 目录结构

```
frontend/src/
├── api/
│   ├── resources.ts              # 自定义资源 CRUD API（baseURL: /api/v1/agno_manage）
│   └── agno/                     # Agno 原生 API（baseURL: 空，直接代理到后端）
│       ├── agnoRequest.ts        #   Axios 实例
│       ├── agent.ts              #   Agent 列表/详情
│       ├── chat.ts               #   Agent 聊天（普通 + SSE 流式）
│       ├── session.ts            #   会话管理（CRUD + runs 历史）
│       ├── team.ts               #   Team 列表 + 聊天
│       └── workflow.ts           #   Workflow 列表 + 聊天
├── components/
│   ├── LazySelect/index.vue      # 分页懒加载下拉选择器（IntersectionObserver 触底加载）
│   └── Pagination/index.vue      # 通用分页组件
├── layouts/
│   └── AppLayout.vue             # 主布局（侧边栏 + 内容区）
├── views/
│   ├── chat/index.vue            # 聊天页（双栏：会话列表 + 消息区）
│   └── resources/
│       ├── ResourcePage.vue      # 统一资源页入口（接收 category prop）
│       └── components/
│           ├── ResourceList.vue          # 资源列表（表格 + 搜索 + 工具栏 + 分页）
│           ├── ResourceDetail.vue        # 资源详情（el-descriptions 面板）
│           ├── ResourceFormDialog.vue    # 创建/编辑弹窗（动态 schema 驱动）
│           ├── DynamicFormRenderer.vue   # 动态表单渲染器（根据 FieldSchema[] 生成表单）
│           ├── RefOrInlineField.vue      # ref_or_inline 字段（引用/内联/引用+覆盖）
│           └── RefOrInlineArrayField.vue # ref_or_inline 数组字段
├── store/modules/
│   └── user.store.ts             # 用户状态（目前只有 basicInfo.id）
├── plugins/
│   └── icons.ts                  # Element Plus 图标全局注册
├── router/
│   └── index.ts                  # 路由定义
├── styles/                       # 全局样式
├── types/                        # 全局 TS 类型声明
│   └── global.d.ts               #   ApiResponse、PageQuery、PageResult、BaseType 等
├── utils/
│   └── request.ts                # 自定义后端 Axios 实例（baseURL: /api/v1/agno_manage）
├── App.vue
└── main.ts                       # 入口：Pinia + ElementPlus + Router + v-hasPerm 指令
```

## 架构核心

### 双 API 层

前端同时对接两套后端 API：

| API 层 | Axios 实例 | baseURL | 用途 |
|---|---|---|---|
| 自定义 API | `utils/request.ts` | `/api/v1/agno_manage` | 资源 CRUD、Schema 查询 |
| Agno 原生 API | `api/agno/agnoRequest.ts` | 空（直接路径） | Agent/Team/Workflow 列表、聊天、会话管理 |

自定义 API 响应格式为 `ApiResponse<T>`（`{ code, data, msg }`），拦截器自动判断 `code !== 0` 报错。
Agno API 直接返回原始数据，不走 `ApiResponse` 包装。

### 统一资源管理

所有 agno 组件类型通过同一套组件处理：

1. **路由注册**：`resourceRoute(path, category, label)` 工厂函数批量注册
2. **ResourcePage.vue**：仅接收 `category` + `label` prop，渲染 `ResourceList`
3. **ResourceList.vue**：调用 `ResourceAPI.listResources({ category })` 获取数据，支持搜索、批量操作
4. **ResourceFormDialog.vue**：创建/编辑时先查 Schema（类型列表 → 字段定义），再用 `DynamicFormRenderer` 渲染表单
5. **DynamicFormRenderer.vue**：根据后端返回的 `FieldSchema[]` 动态生成表单，支持嵌套

### 动态表单字段类型

`DynamicFormRenderer` 支持以下字段类型（由后端 Schema 驱动）：

| 字段类型 | 渲染组件 | 说明 |
|---|---|---|
| `str` | `el-input` | 文本输入 |
| `password` | `el-input[type=password]` | 密码输入（show-password） |
| `int` / `float` | `el-input-number` | 数字输入（支持 min/max/step） |
| `bool` | `el-switch` | 开关 |
| `select` | `el-select` | 下拉选择（支持 `affects` 联动 + `depends_on` 条件显示） |
| `ref_or_inline` | `RefOrInlineField` | 引用已有资源 / 内联定义 / 引用+覆盖（三种模式切换） |
| `ref_or_inline_array` | `RefOrInlineArrayField` | 多个 `ref_or_inline` 项的列表 |

**RefOrInlineField 三种模式**：
- **引用**：通过 `LazySelect` 选择已有资源的 UUID，值为 `{ ref: uuid }`
- **内联**：选择类型后展开完整 schema 表单，值为 `{ category, type, ...config }`
- **引用+覆盖**：选择资源后可覆盖部分字段，值为 `{ ref: uuid, override: {...} }`

嵌套层级用不同颜色的左边框区分（primary → success → warning → danger → gray 循环）。

### 资源 CRUD API

| 操作 | 方法 | 路径 |
|---|---|---|
| 列表 | GET | `/resources/list?category=agent&page=1&page_size=10` |
| 详情 | GET | `/resources/detail/:id` |
| 创建 | POST | `/resources/create` |
| 更新 | PUT | `/resources/update/:id` |
| 删除 | DELETE | `/resources/delete`（body: `[id1, id2]`） |
| 批量状态 | PATCH | `/resources/status`（body: `{ ids, status }`） |
| Schema 分类 | GET | `/schema` |
| Schema 类型 | GET | `/schema?category=agent` |
| Schema 字段 | GET | `/schema?category=agent&type=openai_agent` |

### 资源数据结构

```typescript
interface ResourceTable {
  id?: number
  uuid?: string
  name?: string
  category?: string    // "agent" | "team" | "model" | ...
  type?: string        // "openai_agent" | "claude_agent" | ...
  config?: Record<string, any>
  status?: string      // "0"=启用, "1"=停用
  description?: string
  created_at?: string
  updated_at?: string
}

interface ResourceForm {
  name: string
  category: string
  type: string
  config: Record<string, any>
  status?: string
  description?: string
}
```

## 路由配置

```
/              → 重定向到 /chat
/chat          → 聊天页（views/chat/index.vue）
/agents        → 资源页（category="agent", label="智能体"）
/teams         → 资源页（category="team", label="团队"）
/workflows     → 资源页（category="workflow", label="工作流"）
/models        → 资源页（category="model", label="模型"）
/embedders     → 资源页（category="embedder", label="嵌入器"）
/vectordbs     → 资源页（category="vectordb", label="向量数据库"）
/knowledge     → 资源页（category="knowledge", label="知识库"）
/toolkits      → 资源页（category="toolkit", label="工具集"）
/readers       → 资源页（category="reader", label="读取器"）
/skills        → 资源页（category="skill", label="技能"）
/memory        → 资源页（category="memory", label="记忆"）
/learn         → 资源页（category="learn", label="学习"）
/reasoning     → 资源页（category="reasoning", label="推理"）
/guardrails    → 资源页（category="guardrail", label="守卫"）
/culture       → 资源页（category="culture", label="文化"）
/compress      → 资源页（category="compress", label="压缩"）
/session-summary → 资源页（category="session_summary", label="会话摘要"）
/*             → 重定向到 /chat
```

## 聊天功能

**文件**: `views/chat/index.vue`

双栏布局：

- **左侧（260px）**：类型切换（Agent/Team/Workflow segmented control）→ 组件选择 → 会话列表
- **右侧（flex: 1）**：工具栏（流式开关、清空、刷新）→ 消息列表 → 输入区域

**功能特性**：
- 支持 Agent、Team、Workflow 三种组件类型的聊天
- 普通请求 + SSE 流式输出（可切换）
- 流式进度面板：显示 RunStarted → ModelRequest → ToolCall → RunCompleted 各阶段
- 文件附件上传（FormData multipart）
- 会话管理：新建、切换、重命名（双击）、删除
- Markdown 渲染（markstream-vue）
- 消息指标显示（tokens、耗时）

**Agno 聊天 API**：

| 操作 | 路径 |
|---|---|
| Agent 运行 | `POST /agents/:id/runs` |
| Team 运行 | `POST /teams/:id/runs` |
| Workflow 运行 | `POST /workflows/:id/runs` |
| 会话列表 | `GET /sessions?type=agent&component_id=xxx` |
| 会话 runs | `GET /sessions/:id/runs` |
| 删除会话 | `DELETE /sessions/:id` |
| 重命名会话 | `POST /sessions/:id/rename` |

所有运行请求使用 `FormData`，包含 `message`、`stream`、`session_id`、`user_id`、`files` 字段。

## 布局系统

**AppLayout.vue**：Flexbox 全屏布局

- 侧边栏（160px，可折叠至 48px）：logo + 18 个导航项，带 tooltip 和路由高亮
- 内容区（flex: 1）：`<router-view />`
- 折叠/展开按钮在标题栏，收起后只显示图标

## Vite 配置

```typescript
server: {
  host: '0.0.0.0',       // 支持局域网访问
  allowedHosts: true,     // 允许所有 host（frp 等场景）
  port: 5173,
  hmr: false,             // 禁用 HMR（frp 环境兼容）
  proxy: {
    '/api':       { target: 'http://localhost:8006', changeOrigin: true },
    '/agents':    { target: 'http://localhost:8006', changeOrigin: true },
    '/teams':     { target: 'http://localhost:8006', changeOrigin: true },
    '/workflows': { target: 'http://localhost:8006', changeOrigin: true },
    '/sessions':  { target: 'http://localhost:8006', changeOrigin: true },
  }
}
```

`/api` 代理自定义后端路由，`/agents`、`/teams`、`/workflows`、`/sessions` 代理 Agno 原生路由。

## 开发注意事项

1. **双 API 实例**：自定义资源用 `utils/request.ts`（有 `ApiResponse` 解包），Agno 原生 API 用 `api/agno/agnoRequest.ts`（直接返回数据），不要混用
2. **v-hasPerm 指令**：已注册但目前是空实现（`mounted() {}`），权限判断不生效
3. **用户状态**：`user.store.ts` 目前硬编码 `id: 1`，无认证登录流程
4. **Schema 驱动表单**：新增资源类型只需后端注册 builder + schema，前端无需改动
5. **RefOrInlineField 递归校验**：`DynamicFormRenderer.validate()` 会递归调用嵌套子组件的 `validate()`，提交前自动校验所有层级

## 最后更新

- **日期**: 2026-05-11
- **版本**: v2
- **状态**: 开发中
