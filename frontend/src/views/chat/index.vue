<template>
  <div class="chat-layout">
    <!-- 左侧：可折叠的层级列表 -->
    <div class="chat-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- 折叠状态下的小图标 -->
      <template v-if="sidebarCollapsed">
        <div class="sidebar-toggle" @click="sidebarCollapsed = false">
          <el-icon><ArrowRight /></el-icon>
        </div>
        <div class="sidebar-mini">
          <el-tooltip v-for="cat in categoryList" :key="cat.type" :content="cat.label" placement="right">
            <div class="mini-cat" @click="sidebarCollapsed = false; toggleCategory(cat.type)">
              <span class="mini-label">{{ cat.label[0] }}</span>
            </div>
          </el-tooltip>
        </div>
      </template>

      <!-- 展开状态：完整层级列表 -->
      <template v-else>
        <div class="sidebar-toggle" @click="sidebarCollapsed = true">
          <el-icon><ArrowLeft /></el-icon>
        </div>
        <div class="sidebar-body">
          <div
            v-for="cat in categoryList"
            :key="cat.type"
            class="category-section"
          >
            <div class="category-header" @click="toggleCategory(cat.type)">
              <el-icon class="category-chevron" :class="{ expanded: expandedCategories.has(cat.type) }">
                <ArrowRight />
              </el-icon>
              <span class="category-label">{{ cat.label }}</span>
              <span class="category-count">{{ cat.items.length }}</span>
            </div>
            <div v-show="expandedCategories.has(cat.type)" class="category-body">
              <div v-for="item in cat.items" :key="item.id" class="component-group">
                <div class="component-header" :class="{ active: selectedComponentId === item.id }" @click="toggleComponent(item)">
                  <el-icon class="component-chevron" :class="{ expanded: expandedComponents.has(item.id) }">
                    <ArrowRight />
                  </el-icon>
                  <span class="component-name">{{ item.name }}</span>
                  <el-tooltip content="新建会话" placement="right">
                    <el-button class="component-new-btn" :icon="Plus" text size="small" @click.stop="createSessionFor(item)" />
                  </el-tooltip>
                </div>
                <div v-show="expandedComponents.has(item.id)" class="component-sessions">
                  <div v-if="loadingComponentId === item.id" class="sessions-loading">
                    <el-icon class="spinning"><Loading /></el-icon>
                  </div>
                  <div
                    v-for="s in (sessionsByComponent[item.id] || [])"
                    :key="s.id"
                    class="session-item"
                    :class="{ active: currentSessionId === s.id }"
                    @click="switchSession(s.id)"
                    @dblclick="startRename(s)"
                  >
                    <el-icon class="session-icon"><ChatDotRound /></el-icon>
                    <div class="session-info">
                      <template v-if="editingSessionId === s.id">
                        <el-input
                          v-model="editingName"
                          size="small"
                          autofocus
                          @blur="confirmRename(s.id)"
                          @keydown.enter.prevent="confirmRename(s.id)"
                          @keydown.esc.prevent="cancelRename"
                          @click.stop
                        />
                      </template>
                      <template v-else>
                        <span class="session-name">{{ s.name }}</span>
                      </template>
                    </div>
                    <div class="session-actions">
                      <el-tooltip content="重命名" placement="top">
                        <el-button class="action-btn" :icon="Edit" size="small" text @click.stop="startRename(s)" />
                      </el-tooltip>
                      <el-tooltip content="删除" placement="top">
                        <el-button class="action-btn" :icon="Delete" size="small" text type="danger" @click.stop="deleteSession(s.id)" />
                      </el-tooltip>
                    </div>
                  </div>
                  <div v-if="!loadingComponentId || loadingComponentId !== item.id" class="sessions-empty" v-show="(sessionsByComponent[item.id] || []).length === 0">
                    暂无会话
                  </div>
                </div>
              </div>
              <div v-if="cat.items.length === 0" class="empty-hint">暂无 {{ cat.label }}</div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- 右侧：聊天区域 -->
    <div class="chat-main">
      <template v-if="currentSession">
        <div ref="messageListRef" class="message-list" v-loading="loadingMessages" @scroll="onMessageListScroll">
          <div
            v-for="msg in currentSession.messages"
            :key="msg.id"
            class="message-row"
            :class="msg.role"
          >
            <el-avatar
              :size="28"
              :icon="msg.role === 'user' ? UserFilled : Service"
              :class="['msg-avatar', msg.role]"
            />
            <div class="message-bubble">
              <div class="bubble-role">
                {{ msg.role === 'user' ? '我' : 'AI' }}
                <span v-if="msg.streaming" class="bubble-status">正在输出…</span>
              </div>
              <!-- 进度面板（仅 assistant 且有进度项时显示） -->
              <div
                v-if="msg.role === 'assistant' && msg.progress?.length"
                class="run-progress"
                :class="{ streaming: msg.streaming }"
              >
                <div class="run-progress-header" @click="toggleProgress(msg.id)">
                  <el-icon class="progress-icon" :class="{ spinning: msg.streaming }">
                    <Loading v-if="msg.streaming" /><CircleCheck v-else />
                  </el-icon>
                  <span class="progress-title">
                    {{ msg.streaming ? '运行中…' : `已完成 · ${msg.progress.length} 步` }}
                  </span>
                  <el-icon class="progress-chevron" :class="{ expanded: expandedProgress.has(msg.id) }"><ArrowRight /></el-icon>
                </div>
                <transition name="progress-collapse">
                  <div v-if="expandedProgress.has(msg.id)" class="run-progress-body">
                    <div v-for="(item, idx) in msg.progress" :key="idx" class="progress-item" :class="item.status">
                      <span class="item-dot"></span>
                      <div class="item-body">
                        <span class="item-label">{{ item.label }}</span>
                        <span v-if="item.tokens" class="item-meta">{{ item.tokens }} tk</span>
                        <span v-if="item.duration" class="item-meta">{{ item.duration.toFixed(2) }}s</span>
                        <div v-if="item.detail" class="item-detail">{{ item.detail }}</div>
                      </div>
                    </div>
                  </div>
                </transition>
              </div>
              <div class="bubble-content" :class="{ 'bubble-markdown': msg.role === 'assistant' }">
                <template v-if="msg.role === 'user'">{{ msg.content }}</template>
                <template v-else>
                  <MarkdownRenderer
                    :content="msg.content"
                    :final="!msg.streaming"
                    :theme="hljsTheme"
                  />
                  <span v-if="msg.streaming" class="typing-caret" aria-hidden="true"></span>
                </template>
              </div>
              <div v-if="msg.files?.length" class="bubble-files">
                <el-tag v-for="f in msg.files" :key="f.name" size="small" type="info" effect="plain">
                  <el-icon style="margin-right:3px"><Paperclip /></el-icon>{{ f.name }}
                </el-tag>
              </div>
              <div v-if="msg.metrics && msg.role === 'assistant'" class="bubble-metrics">
                <span v-if="msg.metrics.total_tokens">{{ msg.metrics.total_tokens }} tokens</span>
                <span v-if="msg.metrics.duration">· {{ msg.metrics.duration?.toFixed(2) }}s</span>
              </div>
            </div>
          </div>
          <div ref="bottomRef" />
        </div>

        <!-- 回到底部（消息列表与输入框之间） -->
        <transition name="scroll-btn-fade">
          <div v-if="showScrollToBottom" class="scroll-to-bottom-wrap">
            <el-button
              class="scroll-to-bottom-btn"
              :icon="ArrowDown"
              size="small"
              round
              @click="scrollToBottom"
            >
              回到底部
            </el-button>
          </div>
        </transition>

        <div class="chat-input-area">
          <div v-if="pendingFiles.length" class="pending-files">
            <el-tag v-for="(f, i) in pendingFiles" :key="i" closable size="small" effect="plain" @close="removeFile(i)">
              <el-icon style="margin-right:3px"><Paperclip /></el-icon>{{ f.name }}
            </el-tag>
          </div>
          <div class="input-shell">
            <el-input
              v-model="inputText"
              type="textarea"
              :autosize="{ minRows: 2, maxRows: 8 }"
              placeholder="输入消息…  Ctrl+Enter 发送"
              resize="none"
              @keydown.ctrl.enter.prevent="sendMessage"
            />
            <div class="input-footer">
              <div class="input-tools">
                <el-tooltip content="上传附件：支持图片、音视频、PDF 等" placement="top">
                  <el-upload ref="uploadRef" :auto-upload="false" :show-file-list="false" multiple :on-change="onFileChange">
                    <el-button :icon="Paperclip" circle text />
                  </el-upload>
                </el-tooltip>
                <el-dropdown trigger="click" placement="top">
                  <el-button :icon="Setting" circle text title="聊天设置" />
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item>
                        <div class="settings-item">
                          <span>流式输出</span>
                          <el-switch v-model="options.stream" size="small" @click.stop />
                        </div>
                      </el-dropdown-item>
                      <el-dropdown-item divided>
                        <div class="settings-group">
                          <span class="settings-group-label">代码主题</span>
                          <div class="theme-options">
                            <el-radio-group v-model="hljsTheme" size="small" @change="(v: string) => setHljsTheme(v)" @click.stop>
                              <el-radio value="atom-one-dark">Atom</el-radio>
                              <el-radio value="github-dark">GitHub</el-radio>
                              <el-radio value="monokai">Monokai</el-radio>
                              <el-radio value="github">Light</el-radio>
                            </el-radio-group>
                          </div>
                        </div>
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
                <el-tooltip content="清空消息（仅本地）" placement="top">
                  <el-button :icon="Delete" circle text @click="clearMessages" />
                </el-tooltip>
                <el-tooltip content="重新加载历史" placement="top">
                  <el-button :icon="Refresh" circle text :loading="loadingMessages" @click="reloadMessages" />
                </el-tooltip>
              </div>
              <div class="input-send">
                <span class="kbd-hint">Ctrl + Enter</span>
                <el-button type="primary" :icon="Promotion" :loading="sending" :disabled="!inputText.trim()" @click="sendMessage">
                  发送
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </template>

      <div v-else class="chat-empty">
        <div class="empty-card">
          <div class="empty-icon"><el-icon><ChatDotRound /></el-icon></div>
          <div class="empty-title">开始对话</div>
          <div class="empty-desc">在左侧展开 Agent / Team / Workflow，点 + 新建会话</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted, onUnmounted, watch } from "vue";
import { Plus, Delete, Paperclip, Promotion, UserFilled, Service, ChatDotRound, Edit, Refresh, Loading, CircleCheck, CircleClose, ArrowRight, ArrowDown, Setting, ArrowLeft } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import MarkdownRenderer from "@/components/MarkdownRenderer/index.vue";
import AgnoAgentAPI from "@/api/agno/agent";
import AgnoTeamChatAPI, { AgnoTeamAPI } from "@/api/agno/team";
import AgnoWorkflowChatAPI, { AgnoWorkflowAPI } from "@/api/agno/workflow";
import AgnoAgentChatAPI from "@/api/agno/chat";
import AgnoSessionAPI from "@/api/agno/session";
import type { ChatSession, ChatMessage, SessionType, AgentStreamEvent, RunProgressItem } from "@/api/agno/chat";
import { useUserStoreHook } from "@/store/modules/user.store";

// 扩展 ChatSession 加入 category 字段，用于侧栏分类路由
interface LocalChatSession extends ChatSession { category: SessionType }

const uuidv4 = () =>
  "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });

const userStore = useUserStoreHook();
const userId = computed(() => userStore.basicInfo.id ?? 1);

// ─── 侧栏：三类组件 + 会话层级列表 ──────────────
const agents = ref<{ id: string; name: string }[]>([]);
const teams = ref<{ id: string; name: string }[]>([]);
const workflows = ref<{ id: string; name: string }[]>([]);

const categoryList = computed(() => [
  { type: "agent" as SessionType, label: "Agent", items: agents.value },
  { type: "team" as SessionType, label: "Team", items: teams.value },
  { type: "workflow" as SessionType, label: "Workflow", items: workflows.value },
]);

const expandedCategories = ref(new Set<string>(["agent", "team", "workflow"]));
const expandedComponents = ref(new Set<string>());
const sessionsByComponent = ref<Record<string, LocalChatSession[]>>({});
const loadingComponentId = ref<string | null>(null);
const selectedComponentId = ref<string | null>(null);

function toggleCategory(type: string) {
  if (expandedCategories.value.has(type)) expandedCategories.value.delete(type);
  else expandedCategories.value.add(type);
}

async function toggleComponent(item: { id: string; name: string }) {
  selectedComponentId.value = item.id;
  if (expandedComponents.value.has(item.id)) {
    expandedComponents.value.delete(item.id);
  } else {
    expandedComponents.value.add(item.id);
    if (!sessionsByComponent.value[item.id]) {
      await loadSessionsForComponent(item);
    }
  }
}

async function loadSessionsForComponent(item: { id: string; name: string }) {
  loadingComponentId.value = item.id;
  try {
    const res = await AgnoSessionAPI.listSessions({
      type: findComponentCategory(item.id),
      component_id: item.id,
      user_id: String(userId.value),
      limit: 50,
      sort_by: "updated_at",
      sort_order: "desc",
    });
    const list: any[] = (res.data as any)?.data ?? [];
    sessionsByComponent.value[item.id] = (Array.isArray(list) ? list : []).map((s: any) => ({
      id: s.session_id,
      name: s.session_name || s.session_id.slice(0, 8),
      componentId: item.id,
      componentName: item.name,
      category: findComponentCategory(item.id),
      createdAt: s.created_at ? new Date(s.created_at).getTime() : Date.now(),
      messages: [],
      loaded: false,
    }));
  } catch { /* ignore */ }
  finally { loadingComponentId.value = null; }
}

function findComponentCategory(id: string): SessionType {
  if (agents.value.some((a) => a.id === id)) return "agent";
  if (teams.value.some((t) => t.id === id)) return "team";
  return "workflow";
}

async function loadAllComponents() {
  const [a, t, w] = await Promise.allSettled([
    AgnoAgentAPI.listAgents(),
    AgnoTeamAPI.listTeams(),
    AgnoWorkflowAPI.listWorkflows(),
  ]);
  agents.value = a.status === "fulfilled" ? ((a.value.data as any) ?? []).map((r: any) => ({ id: r.id, name: r.name ?? r.id })) : [];
  teams.value = t.status === "fulfilled" ? ((t.value.data as any) ?? []).map((r: any) => ({ id: r.id, name: r.name ?? r.id })) : [];
  workflows.value = w.status === "fulfilled" ? ((w.value.data as any) ?? []).map((r: any) => ({ id: r.id, name: r.name ?? r.id })) : [];
}

// ─── 会话 ────────────────────────────────────────
const currentSessionId = ref<string | null>(null);

// 从 sessionsByComponent 中查找当前会话
const currentSession = computed(() => {
  if (!currentSessionId.value) return null;
  for (const list of Object.values(sessionsByComponent.value)) {
    const found = list.find((s) => s.id === currentSessionId.value);
    if (found) return found;
  }
  return null;
});

// 从 sessionsByComponent 查找 session 所属的 category
function findSessionCategory(sessionId: string): SessionType {
  for (const [compId, list] of Object.entries(sessionsByComponent.value)) {
    if (list.some((s) => s.id === sessionId)) return findComponentCategory(compId);
  }
  return "agent";
}

// 加载状态
const loadingSessions = ref(false);
const loadingMessages = ref(false);
const sending = ref(false);

// 侧栏折叠（整个面板宽度收缩）
const sidebarCollapsed = ref(false);

// 代码高亮主题
const hljsTheme = ref(localStorage.getItem("hljs-theme") || "atom-one-dark");
function setHljsTheme(t: string) { hljsTheme.value = t; localStorage.setItem("hljs-theme", t); }

// 输入
const inputText = ref("");
const pendingFiles = ref<File[]>([]);
const messageListRef = ref<HTMLElement | null>(null);
const bottomRef = ref<HTMLElement | null>(null);
const uploadRef = ref();
const options = ref({ stream: true });

// 重命名状态
const editingSessionId = ref<string | null>(null);
const editingName = ref("");

// 进度面板展开状态
const expandedProgress = ref<Set<string>>(new Set());
function toggleProgress(msgId: string) {
  if (expandedProgress.value.has(msgId)) expandedProgress.value.delete(msgId);
  else expandedProgress.value.add(msgId);
}

// 流式控制
let streamController: AbortController | null = null;

// 回到底部按钮
const showScrollToBottom = ref(false);
const SCROLL_BOTTOM_THRESHOLD = 80; // 距底部小于此值视为"在底部"

function onMessageListScroll() {
  const el = messageListRef.value;
  if (!el) return;
  showScrollToBottom.value = el.scrollHeight - el.scrollTop - el.clientHeight > SCROLL_BOTTOM_THRESHOLD;
}

function isNearBottom(): boolean {
  const el = messageListRef.value;
  if (!el) return true;
  return el.scrollHeight - el.scrollTop - el.clientHeight <= SCROLL_BOTTOM_THRESHOLD;
}

onMounted(() => loadAllComponents());
onUnmounted(() => streamController?.abort());

watch(currentSessionId, async (id) => {
  if (!id) return;
  const session = currentSession.value;
  if (session && !session.loaded) await loadSessionMessages(id);
  else await scrollToBottom();
});

// ─── 会话操作 ────────────────────────────────────

async function loadSessionMessages(sessionId: string) {
  const session = currentSession.value;
  if (!session || session.id !== sessionId) return;
  loadingMessages.value = true;
  try {
    const cat = findSessionCategory(sessionId);
    const res = await AgnoSessionAPI.getSessionRuns(sessionId, {
      type: cat,
      user_id: String(userId.value),
    });
    const runs: any[] = Array.isArray(res.data) ? (res.data as any) : [];
    const messages: ChatMessage[] = [];
    for (const run of runs) {
      if (run.run_input) {
        messages.push({ id: `${run.run_id}-user`, role: "user", content: run.run_input, createdAt: (run.created_at ?? 0) * 1000 });
      }
      if (run.content) {
        messages.push({ id: `${run.run_id}-assistant`, role: "assistant", content: run.content, createdAt: (run.created_at ?? 0) * 1000, metrics: run.metrics });
      }
    }
    session.messages = messages;
    session.loaded = true;
  } catch {
    session.loaded = true;
  } finally {
    loadingMessages.value = false;
    await scrollToBottom();
  }
}

async function reloadMessages() {
  if (!currentSession.value) return;
  currentSession.value.loaded = false;
  currentSession.value.messages = [];
  await loadSessionMessages(currentSession.value.id);
}

function createSessionFor(item: { id: string; name: string }) {
  const category = findComponentCategory(item.id);
  const newId = uuidv4();
  const arr = sessionsByComponent.value[item.id] || [];
  const newSession: LocalChatSession = {
    id: newId,
    name: `新会话 ${arr.length + 1}`,
    componentId: item.id,
    componentName: item.name,
    category,
    createdAt: Date.now(),
    messages: [],
    loaded: true,
  };
  if (!sessionsByComponent.value[item.id]) sessionsByComponent.value[item.id] = [];
  sessionsByComponent.value[item.id]!.unshift(newSession);
  selectedComponentId.value = item.id;
  expandedComponents.value.add(item.id);
  currentSessionId.value = newId;
}

function switchSession(id: string) {
  currentSessionId.value = id;
}

async function deleteSession(id: string) {
  try {
    await ElMessageBox.confirm("确定删除该会话吗？此操作不可撤销。", "删除会话", {
      type: "warning", confirmButtonText: "删除", cancelButtonText: "取消",
    });
  } catch { return; }
  for (const compId of Object.keys(sessionsByComponent.value)) {
    sessionsByComponent.value[compId] = sessionsByComponent.value[compId]!.filter((s) => s.id !== id);
  }
  if (currentSessionId.value === id) {
    currentSessionId.value = null;
    // 找第一个可用的 session
    for (const list of Object.values(sessionsByComponent.value)) {
      if (list.length > 0) { currentSessionId.value = list[0]!.id; break; }
    }
  }
  try { await AgnoSessionAPI.deleteSession(id, { user_id: String(userId.value) }); } catch { /* 非关键 */ }
}

function startRename(session: ChatSession) {
  editingSessionId.value = session.id;
  editingName.value = session.name;
}
function cancelRename() {
  editingSessionId.value = null;
  editingName.value = "";
}
async function confirmRename(id: string) {
  const name = editingName.value.trim();
  editingSessionId.value = null;
  editingName.value = "";
  if (!name) return;
  const session = currentSession.value;
  if (!session || session.id !== id || session.name === name) return;
  const cat = findSessionCategory(id);
  const oldName = session.name;
  session.name = name;
  try {
    await AgnoSessionAPI.renameSession(id, name, { type: cat, user_id: String(userId.value) });
  } catch {
    session.name = oldName;
    ElMessage.error("重命名失败");
  }
}

function clearMessages() {
  if (!currentSession.value) return;
  currentSession.value.messages = [];
  currentSession.value.loaded = false;
}

// ─── 发送消息 ────────────────────────────────────
function onFileChange(file: any) {
  const raw = file.raw as File;
  if (!pendingFiles.value.some((f) => f.name === raw.name && f.size === raw.size)) {
    pendingFiles.value.push(raw);
  }
}
function removeFile(index: number) { pendingFiles.value.splice(index, 1); }

async function sendMessage() {
  const text = inputText.value.trim();
  if (!text || !currentSession.value || sending.value) return;
  streamController?.abort();
  streamController = null;
  const session = currentSession.value;
  const files = [...pendingFiles.value];
  session.messages.push({ id: uuidv4(), role: "user", content: text, createdAt: Date.now(), files: files.map((f) => ({ name: f.name, size: f.size })) });
  inputText.value = "";
  pendingFiles.value = [];
  uploadRef.value?.clearFiles?.();
  await scrollToBottom();
  sending.value = true;
  if (options.value.stream) await sendStream(session, text, files);
  else await sendNormal(session, text, files);
  sending.value = false;
}

async function sendNormal(session: ChatSession, text: string, files: File[]) {
  const body = { message: text, session_id: session.id, user_id: Number(userId.value), files };
  const cat = findSessionCategory(session.id);
  try {
    let data: any;
    if (cat === "agent") {
      data = (await AgnoAgentChatAPI.runAgent(session.componentId, body)).data;
    } else if (cat === "team") {
      data = (await AgnoTeamChatAPI.runTeam(session.componentId, body)).data;
    } else {
      data = (await AgnoWorkflowChatAPI.runWorkflow(session.componentId, body)).data;
    }
    session.messages.push({ id: uuidv4(), role: "assistant", content: data?.content ?? "", createdAt: Date.now(), metrics: data?.metrics });
  } catch { ElMessage.error("发送失败"); }
  await scrollToBottom();
}

async function sendStream(session: ChatSession, text: string, files: File[]) {
  session.messages.push({ id: uuidv4(), role: "assistant", content: "", createdAt: Date.now(), streaming: true, progress: [] });
  await scrollToBottom();
  const reactiveMsg = session.messages[session.messages.length - 1]!;
  const body = { message: text, session_id: session.id, user_id: Number(userId.value), files };

  const onChunk = async (_event: string, data: AgentStreamEvent) => {
    const progress = reactiveMsg.progress!;
    // agno team 的 SSE event 名带 "Team" 前缀(TeamRunStarted / TeamRunContent / TeamToolCallStarted ...)
    // 字段结构与 agent 一致,去掉前缀即可复用同一套分支;agent 事件本身不以 Team 开头,replace 是 no-op
    const evt = _event.startsWith("Team") ? _event.slice(4) : _event;

    if (evt === "RunStarted") {
      progress.push({ event: evt, label: `运行开始`, status: "running", detail: data.model ? `${data.model_provider} · ${data.model}` : undefined });
    } else if (evt === "ModelRequestStarted") {
      progress.push({ event: evt, label: "模型请求中", status: "running", detail: data.model ? `${data.model_provider} · ${data.model}` : undefined });
    } else if (evt === "ModelRequestCompleted") {
      const last = [...progress].reverse().find(p => p.event === "ModelRequestStarted");
      if (last) { last.status = "done"; last.label = "模型请求完成"; last.tokens = data.total_tokens; }
      else progress.push({ event: evt, label: "模型请求完成", status: "done", tokens: data.total_tokens });
    } else if (evt === "ToolCallStarted") {
      const toolName = data.tool?.tool_name ?? "工具";
      const args = data.tool?.tool_args ? JSON.stringify(data.tool.tool_args) : undefined;
      progress.push({ event: evt, label: `调用工具: ${toolName}`, status: "running", detail: args });
    } else if (evt === "ToolCallCompleted") {
      const toolName = data.tool?.tool_name ?? "工具";
      const last = [...progress].reverse().find(p => p.event === "ToolCallStarted" && p.label.includes(toolName));
      const dur = data.tool?.metrics?.duration;
      if (last) { last.status = "done"; last.label = `工具完成: ${toolName}`; last.duration = dur; }
      else progress.push({ event: evt, label: `工具完成: ${toolName}`, status: "done", duration: dur });
    } else if (evt === "ToolCallError") {
      const toolName = data.tool?.tool_name ?? "工具";
      const last = [...progress].reverse().find(p => p.label.includes(toolName));
      if (last) { last.status = "error"; last.label = `工具错误: ${toolName}`; last.detail = data.error ?? data.tool?.result ?? undefined; }
      else progress.push({ event: evt, label: `工具错误: ${toolName}`, status: "error", detail: data.error ?? undefined });
    } else if (evt === "RunContent" && data.content) {
      reactiveMsg.content += data.content;
      await smartScrollToBottom();
    } else if (evt === "RunCompleted") {
      reactiveMsg.metrics = data.metrics;
      // 将所有还在 running 的进度项标记为 done
      progress.forEach(p => { if (p.status === "running") p.status = "done"; });
    }
  };
  const onDone = async () => { reactiveMsg.streaming = false; await scrollToBottom(); };
  const onError = (err: Error) => { reactiveMsg!.streaming = false; reactiveMsg!.content = reactiveMsg!.content || `[错误: ${err.message}]`; };

  return new Promise<void>((resolve) => {
    const wrappedDone = () => { onDone(); resolve(); };
    const wrappedError = (err: Error) => { onError(err); resolve(); };
    const cat = findSessionCategory(session.id);
    if (cat === "agent") {
      streamController = AgnoAgentChatAPI.runAgentStream(session.componentId, body, onChunk, wrappedDone, wrappedError);
    } else if (cat === "team") {
      streamController = AgnoTeamChatAPI.runTeamStream(session.componentId, body, onChunk, wrappedDone, wrappedError);
    } else {
      streamController = AgnoWorkflowChatAPI.runWorkflowStream(session.componentId, body, onChunk, wrappedDone, wrappedError);
    }
  });
}

async function scrollToBottom() {
  showScrollToBottom.value = false;
  await nextTick();
  bottomRef.value?.scrollIntoView({ behavior: "smooth" });
}

async function smartScrollToBottom() {
  if (isNearBottom()) {
    await nextTick();
    bottomRef.value?.scrollIntoView({ behavior: "smooth" });
  } else {
    showScrollToBottom.value = true;
  }
}
</script>

<style scoped>
/* ── 根部：填充 AppLayout 弹性容器 ── */
.chat-layout {
  display: flex;
  height: 100%;
  background: var(--el-bg-color);
  overflow: hidden;
}

/* ── 左侧栏 ── */
.chat-sidebar {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--el-border-color-light);
  background: var(--el-fill-color-extra-light);
  overflow: hidden;
  transition: width .25s ease;
}
.chat-sidebar.collapsed {
  width: 48px;
}

/* 折叠切换按钮 */
.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  cursor: pointer;
  color: var(--el-text-color-secondary);
  border-bottom: 1px solid var(--el-border-color-light);
  flex-shrink: 0;
  transition: color .15s;
  font-size: 15px;
}
.sidebar-toggle:hover { color: var(--el-color-primary); }
.chat-sidebar.collapsed .sidebar-toggle {
  border-bottom: none;
}

/* 折叠态：小图标列 */
.sidebar-mini {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0;
  gap: 6px;
  overflow-y: auto;
}
.mini-cat {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background .15s;
  font-size: 14px;
  font-weight: 700;
  color: var(--el-text-color-secondary);
}
.mini-cat:hover { background: var(--el-fill-color); color: var(--el-color-primary); }

/* 展开态：层级滚动区 */
.sidebar-body {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
}

/* 分类区块 */
.category-section { border-bottom: 1px solid var(--el-border-color-light); }
.category-section:last-child { border-bottom: none; }

.category-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--el-text-color-regular);
  cursor: pointer;
  user-select: none;
  transition: background .15s;
}
.category-header:hover { background: var(--el-fill-color); }

.category-chevron {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  transition: transform .2s;
  flex-shrink: 0;
}
.category-chevron.expanded { transform: rotate(90deg); }

.category-label { flex: 1; }
.category-count {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
  font-weight: 400;
}

.category-body { overflow: hidden; }

/* 组件项 */
.component-group { border-top: 1px solid var(--el-border-color-extra-light); }

.component-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px 7px 22px;
  font-size: 12px;
  color: var(--el-text-color-regular);
  cursor: pointer;
  user-select: none;
  transition: background .15s;
}
.component-header:hover { background: var(--el-fill-color); }
.component-header.active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.component-chevron {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
  transition: transform .2s;
  flex-shrink: 0;
}
.component-chevron.expanded { transform: rotate(90deg); }

.component-name { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.component-new-btn {
  opacity: 0;
  transition: opacity .15s;
  flex-shrink: 0;
}
.component-header:hover .component-new-btn { opacity: 1; }

/* 会话列表 */
.component-sessions {
  padding-left: 28px;
  padding-bottom: 4px;
}

.sessions-loading,
.sessions-empty {
  padding: 8px 12px;
  font-size: 11px;
  color: var(--el-text-color-placeholder);
  text-align: center;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px 6px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: background .15s;
  margin-bottom: 1px;
}
.session-item:hover { background: var(--el-fill-color); }
.session-item.active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.session-icon {
  flex-shrink: 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
.session-item.active .session-icon { color: var(--el-color-primary); }

.session-info { flex: 1; min-width: 0; }

.session-name {
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.3;
}

.session-actions {
  display: flex;
  gap: 2px;
  opacity: 0;
  transition: opacity .15s;
  flex-shrink: 0;
}
.session-item:hover .session-actions,
.session-item.active .session-actions { opacity: 1; }

.action-btn { padding: 2px !important; }

.empty-hint {
  padding: 12px;
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  text-align: center;
}

/* ── 右侧主区域 ── */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: var(--el-bg-color);
}

/* ── 回到底部 ── */
.scroll-to-bottom-wrap {
  display: flex;
  justify-content: center;
  padding: 0 0 4px;
}

/* ── 消息列表 ── */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  scroll-behavior: smooth;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(var(--el-color-primary-rgb, 64 158 255) / .03), transparent 60%);
}

.message-row { display: flex; gap: 10px; align-items: flex-start; }
.message-row.user { flex-direction: row-reverse; }

.msg-avatar { flex-shrink: 0; margin-top: 1px; }
.msg-avatar.user {
  background: var(--el-color-primary);
  color: #fff;
}
.msg-avatar.assistant {
  background: var(--el-color-success);
  color: #fff;
}

.message-bubble {
  max-width: 88%;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* 角色标签 */
.bubble-role {
  font-size: 10px;
  color: var(--el-text-color-placeholder);
  padding: 0 4px;
  display: flex;
  align-items: center;
  gap: 6px;
  user-select: none;
}
.message-row.user .bubble-role { justify-content: flex-end; }

.bubble-status {
  color: var(--el-color-primary);
  font-size: 10px;
  animation: pulse-text 1.4s ease-in-out infinite;
}

/* 气泡内容 */
.bubble-content {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  background: var(--el-fill-color);
  color: var(--el-text-color-primary);
  box-shadow: 0 1px 2px rgba(0,0,0,.06);
}

.message-row.user .bubble-content {
  background: var(--el-color-primary);
  color: #fff;
  border-radius: 12px 4px 12px 12px;
  box-shadow: 0 2px 8px var(--el-color-primary-light-7);
}
.message-row.assistant .bubble-content {
  border-radius: 4px 12px 12px 12px;
}

.bubble-content.bubble-markdown {
  white-space: normal;
  max-width: 100%;
}

/* 打字光标 */
.typing-caret {
  display: inline-block;
  width: 2px;
  height: 1.2em;
  background: var(--el-color-primary);
  margin-left: 1px;
  vertical-align: text-bottom;
  animation: blink-caret 0.8s step-end infinite;
}
@keyframes blink-caret {
  50% { opacity: 0; }
}
@keyframes pulse-text {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}

/* 附件标签 */
.bubble-files { display: flex; flex-wrap: wrap; gap: 4px; padding-top: 2px; }

/* 统计指标 */
.bubble-metrics {
  font-size: 10px;
  color: var(--el-text-color-placeholder);
  padding: 2px 4px 0;
  display: flex;
  gap: 4px;
}

/* ── 进度面板 ── */
.run-progress {
  margin-bottom: 6px;
  border: 1px solid var(--el-border-color-light);
  border-radius: 10px;
  overflow: hidden;
  font-size: 12px;
  background: var(--el-fill-color-extra-light);
  transition: border-color .3s;
}
.run-progress.streaming {
  border-color: var(--el-color-primary-light-5);
}

.run-progress-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  cursor: pointer;
  user-select: none;
  transition: background .15s;
}
.run-progress-header:hover { background: var(--el-fill-color); }

.progress-icon { color: var(--el-color-primary); flex-shrink: 0; font-size: 13px; }
.progress-title { flex: 1; color: var(--el-text-color-regular); font-size: 11px; font-weight: 500; }
.progress-chevron {
  color: var(--el-text-color-placeholder);
  font-size: 12px;
  transition: transform .25s;
}
.progress-chevron.expanded { transform: rotate(90deg); }

.run-progress-body {
  border-top: 1px solid var(--el-border-color-light);
  padding: 8px 10px 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* 时间轴风格步骤 */
.progress-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 6px 0 6px 0;
  position: relative;
}
/* 时间轴连接线 */
.progress-item::before {
  content: "";
  position: absolute;
  left: 7px;
  top: 22px;
  bottom: -6px;
  width: 1px;
  background: var(--el-border-color-light);
}
.progress-item:last-child::before { display: none; }

/* 圆点 */
.item-dot {
  flex-shrink: 0;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: var(--el-fill-color);
  border: 2px solid var(--el-border-color);
  margin-top: 1px;
  position: relative;
  z-index: 1;
  transition: background .3s, border-color .3s;
}
.progress-item.running .item-dot {
  background: var(--el-color-primary-light-5);
  border-color: var(--el-color-primary);
  box-shadow: 0 0 0 3px var(--el-color-primary-light-8);
}
.progress-item.done .item-dot {
  background: var(--el-color-success);
  border-color: var(--el-color-success);
}
.progress-item.error .item-dot {
  background: var(--el-color-danger);
  border-color: var(--el-color-danger);
}

.item-body {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  min-width: 0;
  flex: 1;
}

.item-label { color: var(--el-text-color-primary); font-size: 11px; font-weight: 500; }
.item-meta { color: var(--el-text-color-placeholder); font-size: 10px; }
.item-detail {
  width: 100%;
  color: var(--el-text-color-secondary);
  font-size: 10px;
  font-family: "JetBrains Mono", "Fira Code", monospace;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 64px;
  overflow-y: auto;
  background: var(--el-fill-color);
  border-radius: 6px;
  padding: 5px 8px;
  margin-top: 4px;
  line-height: 1.5;
}

/* 折叠过渡 */
.progress-collapse-enter-active,
.progress-collapse-leave-active { transition: all 0.25s ease; overflow: hidden; }
.progress-collapse-enter-from,
.progress-collapse-leave-to { max-height: 0; opacity: 0; }
.progress-collapse-enter-to,
.progress-collapse-leave-from { max-height: 600px; opacity: 1; }

@keyframes spin { to { transform: rotate(360deg); } }
.spinning { animation: spin 1s linear infinite; }

/* ── 回到底部按钮 ── */
.scroll-to-bottom-btn {
  box-shadow: 0 1px 6px rgba(0,0,0,.12);
  transition: transform .2s, box-shadow .2s;
  font-size: 12px;
}
.scroll-to-bottom-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 10px rgba(0,0,0,.18);
}

.scroll-btn-fade-enter-active,
.scroll-btn-fade-leave-active { transition: opacity .2s, transform .2s ease; }
.scroll-btn-fade-enter-from,
.scroll-btn-fade-leave-to { opacity: 0; transform: translateY(4px); }

/* ── 输入区域 ── */
.chat-input-area {
  padding: 14px 20px 16px;
  border-top: 1px solid var(--el-border-color-light);
  background: var(--el-bg-color);
  flex-shrink: 0;
}

.pending-files {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

/* 输入外壳：带圆角渐变框 */
.input-shell {
  background: var(--el-fill-color-extra-light);
  border: 1px solid var(--el-border-color-light);
  border-radius: 12px;
  padding: 10px 14px 10px 14px;
  transition: border-color .25s, box-shadow .25s;
}
.input-shell:focus-within {
  border-color: var(--el-color-primary-light-3);
  box-shadow: 0 0 0 3px var(--el-color-primary-light-8);
}

.input-shell :deep(.el-textarea__inner) {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  padding: 0;
  font-size: 13px;
  line-height: 1.6;
  resize: none;
}

/* 输入底部栏 */
.input-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  gap: 12px;
}

.input-tools {
  display: flex;
  align-items: center;
  gap: 4px;
}

.settings-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  gap: 16px;
  width: 100%;
}
.settings-group { display: flex; flex-direction: column; gap: 8px; width: 100%; }
.settings-group-label { font-size: 13px; color: var(--el-text-color-regular); }
.theme-options :deep(.el-radio) { margin-right: 12px; }

.input-send {
  display: flex;
  align-items: center;
  gap: 10px;
}

.kbd-hint {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
  background: var(--el-fill-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
  padding: 2px 7px;
  line-height: 1.6;
  white-space: nowrap;
}

/* ── 空状态 ── */
.chat-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(ellipse at 50% 40%, rgba(var(--el-color-primary-rgb, 64 158 255) / .04), transparent 65%);
}

.empty-card {
  text-align: center;
  padding: 48px 32px;
  max-width: 380px;
}

.empty-icon {
  font-size: 48px;
  color: var(--el-text-color-disabled);
  margin-bottom: 16px;
}

.empty-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin-bottom: 24px;
  line-height: 1.6;
}
</style>
