<template>
  <div class="team-builder">
    <!-- 顶部工具栏 -->
    <div class="team-builder__toolbar">
      <span class="team-builder__title">团队构建器</span>
      <div class="team-builder__toolbar-actions">
        <el-button size="small" icon="Plus" @click="addTeamNode">添加团队</el-button>
        <el-button size="small" icon="Service" @click="addAgentNode">添加智能体</el-button>
        <el-divider direction="vertical" />
        <el-select
          v-model="loadTeamId"
          placeholder="加载已有团队"
          clearable
          filterable
          size="small"
          style="width: 180px"
          @change="handleLoadTeam"
        >
          <el-option
            v-for="t in existingTeams"
            :key="t.id"
            :label="t.name"
            :value="t.id"
          />
        </el-select>
        <el-divider direction="vertical" />
        <el-button size="small" icon="Delete" @click="handleClear">清空</el-button>
        <el-button size="small" type="primary" icon="Check" :loading="saving" @click="handleSave">
          保存团队
        </el-button>
      </div>
    </div>

    <div class="team-builder__body">
      <!-- Vue Flow 画布 -->
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        :node-types="nodeTypes"
        fit-view-on-init
        class="team-builder__canvas"
        @node-click="onNodeClick"
        @pane-click="onPaneClick"
      >
        <Background />
        <Controls />
      </VueFlow>

      <!-- 右侧属性面板 -->
      <transition name="panel-slide">
        <div v-if="selectedNode" class="team-builder__panel">
          <div class="panel-header">
            <span class="panel-title">
              {{ selectedNode.type === 'teamNode' ? '团队属性' : '智能体属性' }}
            </span>
            <el-icon class="panel-close" @click="selectedNode = null"><Close /></el-icon>
          </div>
          <div class="panel-body">
            <!-- 公共：名称 -->
            <el-form label-position="top" size="small">
              <el-form-item label="名称" required>
                <el-input v-model="selectedNode.data.name" placeholder="请输入名称" />
              </el-form-item>
              <el-form-item label="指令/说明">
                <el-input
                  v-model="selectedNode.data.instructions"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入指令"
                />
              </el-form-item>

              <!-- 团队专属字段 -->
              <template v-if="selectedNode.type === 'teamNode'">
                <el-form-item label="协作模式">
                  <el-select v-model="selectedNode.data.mode" style="width: 100%">
                    <el-option value="coordinate" label="协调 (coordinate)" />
                    <el-option value="route" label="路由 (route)" />
                    <el-option value="collaborate" label="协作 (collaborate)" />
                  </el-select>
                </el-form-item>
                <el-form-item label="领队模型">
                  <LazySelect
                    v-model="selectedNode.data.modelUuid"
                    :fetcher="fetchModels"
                    placeholder="选择领队模型"
                    :initial-label="selectedNode.data.modelLabel"
                    preload
                    @change="(_, raw) => onModelChange(raw)"
                  />
                </el-form-item>
                <el-form-item label="最大迭代次数">
                  <el-input-number
                    v-model="selectedNode.data.maxIterations"
                    :min="1"
                    :max="100"
                    style="width: 100%"
                  />
                </el-form-item>
                <el-form-item label="显示成员响应">
                  <el-switch v-model="selectedNode.data.showMembersResponses" />
                </el-form-item>
                <el-form-item label="Markdown 渲染">
                  <el-switch v-model="selectedNode.data.markdown" />
                </el-form-item>
                <el-form-item label="成员（连线自动同步）">
                  <div class="member-list">
                    <el-tag
                      v-for="memberId in getMemberIds(selectedNode.id)"
                      :key="memberId"
                      size="small"
                      style="margin: 2px"
                    >
                      {{ getNodeLabel(memberId) }}
                    </el-tag>
                    <span v-if="getMemberIds(selectedNode.id).length === 0" class="member-hint">
                      从此节点向智能体/团队连线以添加成员
                    </span>
                  </div>
                </el-form-item>
              </template>

              <!-- 智能体专属字段 -->
              <template v-else>
                <el-form-item label="模型">
                  <LazySelect
                    v-model="selectedNode.data.modelUuid"
                    :fetcher="fetchModels"
                    placeholder="选择模型"
                    :initial-label="selectedNode.data.modelLabel"
                    preload
                    @change="(_, raw) => onModelChange(raw)"
                  />
                </el-form-item>
                <el-form-item label="Markdown 渲染">
                  <el-switch v-model="selectedNode.data.markdown" />
                </el-form-item>
                <el-form-item label="显示工具调用">
                  <el-switch v-model="selectedNode.data.showToolCalls" />
                </el-form-item>
              </template>

              <el-form-item label="描述（可选）">
                <el-input
                  v-model="selectedNode.data.description"
                  type="textarea"
                  :rows="2"
                  placeholder="可选描述"
                />
              </el-form-item>
            </el-form>
          </div>
          <div class="panel-footer">
            <el-button
              type="danger"
              size="small"
              icon="Delete"
              plain
              @click="deleteSelectedNode"
            >
              删除节点
            </el-button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, markRaw } from "vue";
import { VueFlow, useVueFlow, type Node, type Edge } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { Controls } from "@vue-flow/controls";
import { Close } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import TeamNode from "./nodes/TeamNode.vue";
import AgentNode from "./nodes/AgentNode.vue";
import LazySelect from "@/components/LazySelect/index.vue";
import ResourceAPI from "@/api/resources";
import type { ResourceTable } from "@/api/resources";

import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";

const nodeTypes = { teamNode: markRaw(TeamNode), agentNode: markRaw(AgentNode) };

const { removeNodes, removeEdges } = useVueFlow();

// ── 画布状态 ──────────────────────────────────────────────────────
const nodes = ref<Node[]>([]);
const edges = ref<Edge[]>([]);
const selectedNode = ref<Node | null>(null);
const saving = ref(false);
const loadTeamId = ref<number | undefined>(undefined);
const existingTeams = ref<ResourceTable[]>([]);
let nodeCounter = 0;

// ── 节点类型定义 ──────────────────────────────────────────────────
function makeId() {
  return `node_${++nodeCounter}_${Date.now()}`;
}

function addTeamNode() {
  const id = makeId();
  nodes.value.push({
    id,
    type: "teamNode",
    position: { x: 200 + Math.random() * 200, y: 100 + Math.random() * 100 },
    data: {
      name: "新团队",
      mode: "coordinate",
      modelUuid: undefined,
      modelLabel: undefined,
      maxIterations: 10,
      showMembersResponses: false,
      markdown: true,
      instructions: "",
      description: "",
    },
  });
}

function addAgentNode() {
  const id = makeId();
  nodes.value.push({
    id,
    type: "agentNode",
    position: { x: 200 + Math.random() * 200, y: 300 + Math.random() * 100 },
    data: {
      name: "新智能体",
      modelUuid: undefined,
      modelLabel: undefined,
      instructions: "",
      markdown: true,
      showToolCalls: false,
      description: "",
    },
  });
}

// ── 节点选中 ──────────────────────────────────────────────────────
function onNodeClick({ node }: { node: Node }) {
  selectedNode.value = node;
}

function onPaneClick() {
  selectedNode.value = null;
}

// ── 成员关系（通过边） ─────────────────────────────────────────────
function getMemberIds(teamNodeId: string): string[] {
  return edges.value
    .filter((e) => e.source === teamNodeId)
    .map((e) => e.target);
}

function getNodeLabel(nodeId: string): string {
  const n = nodes.value.find((n) => n.id === nodeId);
  return n?.data?.name || nodeId;
}

// ── 模型选择回调 ──────────────────────────────────────────────────
function onModelChange(raw?: any) {
  if (!selectedNode.value || !raw) return;
  selectedNode.value.data.modelLabel = raw.label;
}

// ── 删除节点 ──────────────────────────────────────────────────────
function deleteSelectedNode() {
  if (!selectedNode.value) return;
  removeNodes([selectedNode.value.id]);
  selectedNode.value = null;
}

// ── 清空 ──────────────────────────────────────────────────────────
async function handleClear() {
  await ElMessageBox.confirm("确认清空画布？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  });
  nodes.value = [];
  edges.value = [];
  selectedNode.value = null;
  loadTeamId.value = undefined;
}

// ── 模型懒加载 ───────────────────────────────────────────────────
async function fetchModels(params: { page_no: number; page_size: number; name?: string }) {
  const res = await ResourceAPI.listResources({
    category: "model",
    page_no: params.page_no,
    page_size: params.page_size,
    name: params.name,
    status: "0",
  });
  const items = (res.data.data.items ?? []).map((r: ResourceTable) => ({
    value: r.uuid ?? String(r.id),
    label: r.name ?? r.uuid ?? String(r.id),
    raw: r,
  }));
  return { items, total: res.data.data.total ?? 0 };
}

// ── 加载已有团队 ──────────────────────────────────────────────────
async function loadExistingTeams() {
  try {
    const res = await ResourceAPI.listResources({ category: "team", page_no: 1, page_size: 100 });
    existingTeams.value = res.data.data.items ?? [];
  } catch {
    /* ignore */
  }
}

async function handleLoadTeam(id: number | undefined) {
  if (!id) return;
  try {
    const res = await ResourceAPI.detailResource(id);
    const team = res.data.data;
    buildCanvasFromTeam(team, id);
  } catch (e) {
    ElMessage.error("加载团队失败");
  }
}

function buildCanvasFromTeam(team: ResourceTable, teamDbId: number) {
  nodes.value = [];
  edges.value = [];
  selectedNode.value = null;
  nodeCounter = 0;

  const cfg = team.config ?? {};

  const teamId = makeId();
  const teamNode: Node = {
    id: teamId,
    type: "teamNode",
    position: { x: 300, y: 80 },
    data: {
      _dbId: teamDbId,
      name: team.name ?? cfg.name ?? "团队",
      mode: cfg.mode ?? "coordinate",
      modelUuid: cfg.model?.ref ?? undefined,
      modelLabel: undefined,
      maxIterations: cfg.max_iterations ?? 10,
      showMembersResponses: cfg.show_members_responses ?? false,
      markdown: cfg.markdown ?? true,
      instructions: cfg.instructions ?? "",
      description: team.description ?? "",
    },
  };
  nodes.value.push(teamNode);

  const members: any[] = cfg.members ?? [];
  members.forEach((m, i) => {
    const agentId = makeId();
    nodes.value.push({
      id: agentId,
      type: "agentNode",
      position: { x: 100 + i * 220, y: 280 },
      data: {
        name: m.name ?? `成员 ${i + 1}`,
        modelUuid: m.model?.ref ?? undefined,
        modelLabel: undefined,
        instructions: m.instructions ?? "",
        markdown: m.markdown ?? true,
        showToolCalls: m.show_tool_calls ?? false,
        description: "",
        _refUuid: m.ref ?? undefined,
      },
    });
    edges.value.push({
      id: `e_${teamId}_${agentId}`,
      source: teamId,
      target: agentId,
    });
  });
}

// ── 保存 ──────────────────────────────────────────────────────────
async function handleSave() {
  const teamNodes = nodes.value.filter((n) => n.type === "teamNode");
  if (teamNodes.length === 0) {
    ElMessage.warning("请至少添加一个团队节点");
    return;
  }
  if (teamNodes.length > 1) {
    ElMessage.warning("当前只支持保存一个根团队，请保留一个团队节点");
    return;
  }

  const teamNode = teamNodes[0];
  if (!teamNode.data.name?.trim()) {
    ElMessage.warning("团队名称不能为空");
    return;
  }

  saving.value = true;
  try {
    const memberIds = getMemberIds(teamNode.id);
    const members = memberIds.map((mid) => {
      const n = nodes.value.find((x) => x.id === mid);
      if (!n) return null;
      if (n.data._refUuid) {
        return { ref: n.data._refUuid };
      }
      const agentConfig: Record<string, any> = {
        name: n.data.name,
        instructions: n.data.instructions || undefined,
        markdown: n.data.markdown,
        show_tool_calls: n.data.showToolCalls,
      };
      if (n.data.modelUuid) {
        agentConfig.model = { ref: n.data.modelUuid };
      }
      return {
        category: "agent",
        type: "agno_agent",
        ...agentConfig,
      };
    }).filter(Boolean);

    const teamConfig: Record<string, any> = {
      name: teamNode.data.name,
      mode: teamNode.data.mode ?? "coordinate",
      instructions: teamNode.data.instructions || undefined,
      markdown: teamNode.data.markdown,
      show_members_responses: teamNode.data.showMembersResponses,
      max_iterations: teamNode.data.maxIterations ?? 10,
      members,
    };
    if (teamNode.data.modelUuid) {
      teamConfig.model = { ref: teamNode.data.modelUuid };
    }

    const body = {
      name: teamNode.data.name,
      category: "team",
      type: "agno_team",
      config: teamConfig,
      status: "0",
      description: teamNode.data.description || undefined,
    };

    const dbId = teamNode.data._dbId;
    if (dbId) {
      await ResourceAPI.updateResource(dbId, body);
      ElMessage.success("团队已更新");
    } else {
      const res = await ResourceAPI.createResource(body);
      teamNode.data._dbId = res.data.data.id;
      loadTeamId.value = res.data.data.id;
      ElMessage.success("团队已保存");
      await loadExistingTeams();
    }
  } catch (e: any) {
    ElMessage.error(e?.message ?? "保存失败");
  } finally {
    saving.value = false;
  }
}

// ── 挂载 ──────────────────────────────────────────────────────────
onMounted(() => {
  loadExistingTeams();
});
</script>

<style scoped>
.team-builder {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  background: var(--el-bg-color-page);
}

.team-builder__toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
  flex-shrink: 0;
}

.team-builder__title {
  font-weight: 600;
  font-size: 14px;
  color: var(--el-text-color-primary);
  margin-right: 8px;
}

.team-builder__toolbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.team-builder__body {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
}

.team-builder__canvas {
  flex: 1;
  height: 100%;
}

/* 属性面板 */
.team-builder__panel {
  width: 300px;
  flex-shrink: 0;
  background: var(--el-bg-color);
  border-left: 1px solid var(--el-border-color-light);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--el-border-color-light);
  flex-shrink: 0;
}

.panel-title {
  font-weight: 600;
  font-size: 13px;
  flex: 1;
  color: var(--el-text-color-primary);
}

.panel-close {
  cursor: pointer;
  color: var(--el-text-color-secondary);
  font-size: 16px;
  transition: color 0.15s;
}

.panel-close:hover {
  color: var(--el-color-danger);
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 12px 14px;
}

.panel-footer {
  padding: 10px 14px;
  border-top: 1px solid var(--el-border-color-light);
  flex-shrink: 0;
}

.member-list {
  min-height: 28px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.member-hint {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
}

/* 面板动画 */
.panel-slide-enter-active,
.panel-slide-leave-active {
  transition: width 0.2s ease, opacity 0.2s ease;
}

.panel-slide-enter-from,
.panel-slide-leave-to {
  width: 0;
  opacity: 0;
}
</style>
