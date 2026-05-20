import type { App } from "vue";
import { createRouter, createWebHashHistory, type RouteRecordRaw } from "vue-router";

const AppLayout = () => import("@/layouts/AppLayout.vue");

const resourceRoute = (path: string, category: string, label: string): RouteRecordRaw => ({
  path,
  component: () => import("@/views/resources/ResourcePage.vue"),
  props: { category, label },
});

const routes: RouteRecordRaw[] = [
  { path: "/", redirect: "/chat" },
  {
    path: "/",
    component: AppLayout,
    children: [
      { path: "chat", component: () => import("@/views/chat/index.vue") },
      resourceRoute("agents",          "agent",           "智能体"),
      resourceRoute("teams",           "team",            "团队"),
      { path: "teams/visual", component: () => import("@/views/team-builder/TeamVisualBuilder.vue") },
      resourceRoute("workflows",       "workflow",        "工作流"),
      resourceRoute("models",          "model",           "模型"),
      resourceRoute("embedders",       "embedder",        "嵌入器"),
      resourceRoute("vectordbs",       "vectordb",        "向量数据库"),
      resourceRoute("knowledge",       "knowledge",       "知识库"),
      resourceRoute("toolkits",        "toolkit",         "工具集"),
      resourceRoute("readers",         "reader",          "读取器"),
      resourceRoute("skills",          "skill",           "技能"),
      resourceRoute("memory",          "memory",          "记忆"),
      resourceRoute("learn",           "learn",           "学习"),
      resourceRoute("reasoning",       "reasoning",       "推理"),
      resourceRoute("guardrails",      "guardrail",       "守卫"),
      resourceRoute("culture",         "culture",         "文化"),
      resourceRoute("compress",        "compress",        "压缩"),
      resourceRoute("session-summary", "session_summary", "会话摘要"),
      // Agno 内部接口管理
      { path: "agno/agents",     component: () => import("@/views/agno/agents/AgnoAgentList.vue") },
      { path: "agno/teams",      component: () => import("@/views/agno/teams/AgnoTeamList.vue") },
      { path: "agno/workflows",  component: () => import("@/views/agno/workflows/AgnoWorkflowList.vue") },
      { path: "agno/sessions",   component: () => import("@/views/agno/sessions/AgnoSessionList.vue") },
      { path: "agno/traces",     component: () => import("@/views/agno/traces/AgnoTraceList.vue") },
      { path: "agno/registry",   component: () => import("@/views/agno/registry/AgnoRegistry.vue") },
      { path: "agno/memories",   component: () => import("@/views/agno/memories/AgnoMemoryList.vue") },
      { path: "agno/metrics",    component: () => import("@/views/agno/metrics/AgnoMetrics.vue") },
      { path: "agno/components", component: () => import("@/views/agno/components/AgnoComponentList.vue") },
      { path: "agno/schedules",  component: () => import("@/views/agno/schedules/AgnoScheduleList.vue") },
      { path: "agno/approvals",  component: () => import("@/views/agno/approvals/AgnoApprovalList.vue") },
      { path: "agno/evals",      component: () => import("@/views/agno/evals/AgnoEvalList.vue") },
    ],
  },
  { path: "/:pathMatch(.*)*", redirect: "/chat" },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

export function setupRouter(app: App<Element>) {
  app.use(router);
}

export default router;
