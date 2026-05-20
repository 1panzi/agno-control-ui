<template>
  <div class="app-layout">
    <aside class="app-sidebar" :class="{ collapsed }">
      <div class="sidebar-logo">
        <span class="logo-icon">🤖</span>
        <span v-if="!collapsed" class="logo-text">Agno 管理</span>
        <el-icon class="collapse-btn" @click="collapsed = !collapsed">
          <component :is="collapsed ? 'Expand' : 'Fold'" />
        </el-icon>
      </div>
      <nav class="sidebar-nav">
        <el-tooltip
          v-for="item in menuItems"
          :key="item.path"
          :content="item.label"
          placement="right"
          :disabled="!collapsed"
        >
          <router-link :to="item.path" class="nav-item" active-class="nav-item--active">
            <el-icon class="nav-icon"><component :is="item.icon" /></el-icon>
            <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
          </router-link>
        </el-tooltip>

        <div class="nav-divider">
          <span v-if="!collapsed" class="nav-divider__text">Agno 内部</span>
        </div>

        <el-tooltip
          v-for="item in agnoMenuItems"
          :key="item.path"
          :content="item.label"
          placement="right"
          :disabled="!collapsed"
        >
          <router-link :to="item.path" class="nav-item" active-class="nav-item--active">
            <el-icon class="nav-icon"><component :is="item.icon" /></el-icon>
            <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
          </router-link>
        </el-tooltip>
      </nav>
    </aside>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const collapsed = ref(false);

const menuItems = [
  { path: "/chat",            label: "聊天",       icon: "ChatDotRound" },
  { path: "/agents",          label: "智能体",     icon: "Service" },
  { path: "/teams",           label: "团队",       icon: "UserFilled" },
  { path: "/teams/visual",    label: "团队构建器", icon: "SetUp" },
  { path: "/workflows",       label: "工作流",     icon: "Share" },
  { path: "/models",          label: "模型",       icon: "Cpu" },
  { path: "/embedders",       label: "嵌入器",     icon: "Connection" },
  { path: "/vectordbs",       label: "向量数据库", icon: "DataBoard" },
  { path: "/knowledge",       label: "知识库",     icon: "Reading" },
  { path: "/toolkits",        label: "工具集",     icon: "Tools" },
  { path: "/readers",         label: "读取器",     icon: "Document" },
  { path: "/skills",          label: "技能",       icon: "MagicStick" },
  { path: "/memory",          label: "记忆",       icon: "Memo" },
  { path: "/learn",           label: "学习",       icon: "Collection" },
  { path: "/reasoning",       label: "推理",       icon: "Opportunity" },
  { path: "/guardrails",      label: "守卫",       icon: "Lock" },
  { path: "/culture",         label: "文化",       icon: "StarFilled" },
  { path: "/compress",        label: "压缩",       icon: "Sort" },
  { path: "/session-summary", label: "会话摘要",   icon: "ChatLineRound" },
];

const agnoMenuItems = [
  { path: "/agno/agents",     label: "Agents",     icon: "Service" },
  { path: "/agno/teams",      label: "Teams",      icon: "UserFilled" },
  { path: "/agno/workflows",  label: "Workflows",  icon: "Share" },
  { path: "/agno/sessions",   label: "Sessions",   icon: "ChatLineSquare" },
  { path: "/agno/traces",     label: "Traces",     icon: "DataLine" },
  { path: "/agno/registry",   label: "Registry",   icon: "Grid" },
  { path: "/agno/memories",   label: "Memories",   icon: "Memo" },
  { path: "/agno/metrics",    label: "Metrics",    icon: "TrendCharts" },
  { path: "/agno/components", label: "Components", icon: "Menu" },
  { path: "/agno/schedules",  label: "Schedules",  icon: "Timer" },
  { path: "/agno/approvals",  label: "Approvals",  icon: "CircleCheck" },
  { path: "/agno/evals",      label: "Evals",      icon: "DataAnalysis" },
];
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: var(--el-bg-color-page);
}

.app-sidebar {
  width: 160px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color-light);
  overflow-y: auto;
  overflow-x: hidden;
  transition: width 0.2s ease;
}

.app-sidebar.collapsed {
  width: 48px;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 10px;
  border-bottom: 1px solid var(--el-border-color-light);
  font-weight: 700;
  font-size: 15px;
  color: var(--el-color-primary);
  flex-shrink: 0;
  min-height: 48px;
}

.logo-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.logo-text {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
}

.collapse-btn {
  margin-left: auto;
  flex-shrink: 0;
  cursor: pointer;
  font-size: 16px;
  color: var(--el-text-color-secondary);
  transition: color 0.15s;
}

.collapse-btn:hover {
  color: var(--el-color-primary);
}

.app-sidebar.collapsed .sidebar-logo {
  justify-content: center;
  padding: 12px 0;
}

.app-sidebar.collapsed .collapse-btn {
  margin-left: 0;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  padding: 8px 0;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  font-size: 13px;
  color: var(--el-text-color-regular);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
  cursor: pointer;
  white-space: nowrap;
}

.app-sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 9px 0;
}

.nav-item:hover {
  background: var(--el-fill-color-light);
  color: var(--el-color-primary);
}

.nav-item--active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  font-weight: 600;
}

.nav-icon {
  flex-shrink: 0;
  font-size: 16px;
}

.nav-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-divider {
  margin: 8px 14px;
  border-top: 1px solid var(--el-border-color-light);
  padding-top: 8px;
}

.nav-divider__text {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.app-sidebar.collapsed .nav-divider {
  margin: 8px 6px;
}

.app-main {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>

