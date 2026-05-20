# agno-manage 待办清单

> 后端重构已完成（v2 分支），当前架构：AgentOS base_app 混合模式 + ag_resources 组件管理。
> 本清单记录后续待开发功能，按优先级排序。

---

## 后端

### 一、资源管理 API 完善

- [ ] `GET /api/v1/agno_manage/resources/list` 支持按 `name` 模糊搜索
- [ ] 创建/更新资源时校验 `(category, type)` 是否在 `builder_registry` 中存在
- [ ] 创建/更新资源时校验 `config` 字段是否符合对应 builder 的 schema（必填字段检查）
- [ ] 禁用资源（status=1）时同步从 agno Registry 中移除对应 agent/team
- [ ] 启用资源（status=0）时重新 build 并注册到 agno Registry

### 二、组件 build 错误反馈

- [ ] `_build_and_register` 失败时将错误信息写回 `ag_resources.description` 字段，方便前端展示
- [ ] 新增 `GET /api/v1/agno_manage/resources/{uuid}/status` 接口，返回 agno Registry 中是否已注册

### 三、scripts 集成测试更新

- [ ] `scripts/agent_chat.py` — 改为使用新的 `resources` API 创建组件，替换旧的 `domains.*` 调用
- [ ] `scripts/agent_tools.py` — 同上

---

## 前端

> 前端目前基于旧的 domains 模型体系（Provider/ModelConfig/AgentConfig），
> 需要逐步迁移到新的通用资源管理体系（ag_resources + agno 内置路由）。

### 一、资源管理页（核心，优先）

> 对应后端 `/api/v1/agno_manage/resources/` + `/api/v1/agno_manage/schema`

- [ ] 新建模块 `frontend/src/modules/resources/`
- [ ] `ResourceList.vue` — 资源列表，支持按 category/type/status 筛选、分页
- [ ] `ResourceForm.vue` — 动态表单，根据 `GET /schema?category=&type=` 返回的 fields 自动渲染
  - 支持字段类型：str / int / bool / password / select / ref（引用其他资源）
  - ref 类型渲染为下拉框，从同 category 的已有资源中选择
- [ ] 创建/编辑/删除/启用禁用操作
- [ ] 侧边栏新增"资源管理"导航入口

### 二、对话页对接新 Agent 路由

> agno 内置路由：`/agents`、`/sessions`、`/sessions/{id}/runs`

- [ ] 对话页 Agent 列表改为从 `GET /agents` 获取（替换旧的 `/api/v1/agents`）
- [ ] 新建对话改为调用 agno 内置 `/sessions` + `/agents/{id}/runs`
- [ ] 消息历史改为从 `GET /sessions/{id}/runs` 解析

### 三、Agent 详情页

**路由**: `/agents/:agent_id`

- [ ] `AgentDetail.vue` — 展示 agno Registry 中 agent 的配置
- [ ] 对应 `ag_resources` 中的 config 可跳转编辑

### 四、前端待办（原有，仍有效）

- [ ] Agent 详情页提示词卡片（system_message / instructions）
- [ ] Agent 详情页工具 & 知识库卡片
- [ ] Agent 详情页 Memory / Learning 卡片
- [ ] 知识库文档预览功能
- [ ] Agent 列表搜索筛选
- [ ] 批量操作（批量删除、批量启用/禁用）

---

## 工程 / 基础设施

- [ ] `.gitignore` 补充 `backend/local.db`（开发库不应入库）
- [ ] 前端 `request.ts` baseURL 中的 `/api/v1` 前缀统一改为 `/api/v1/agno_manage`（或分接口配置）
- [ ] CI：添加 `cd backend && uv run pytest` 自动化测试步骤
- [ ] 生产环境：`DATABASE_URL` 切换为 PostgreSQL，`get_agno_db()` 自动切换为 `PostgresDb`

---

## 长期计划

- [ ] 用户认证与权限（登录 / Token / 角色）
- [ ] 多租户隔离
- [ ] 操作审计日志
- [ ] 国际化（i18n）
- [ ] 响应式 / 移动端适配

