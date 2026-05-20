<template>
  <div class="agent-node" :class="{ selected: props.selected }">
    <Handle type="target" :position="Position.Top" />
    <div class="agent-node__header">
      <el-icon class="agent-node__icon"><Service /></el-icon>
      <span class="agent-node__title">{{ data.name || '未命名智能体' }}</span>
    </div>
    <div class="agent-node__body">
      <div v-if="data.modelLabel" class="agent-node__info">
        <el-icon><Cpu /></el-icon>
        <span>{{ data.modelLabel }}</span>
      </div>
      <div v-if="data.instructions" class="agent-node__instructions">
        {{ truncate(data.instructions, 60) }}
      </div>
    </div>
    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>

<script setup lang="ts">
import { Handle, Position } from "@vue-flow/core";
import { Cpu, Service } from "@element-plus/icons-vue";

interface AgentNodeData {
  name?: string;
  modelLabel?: string;
  instructions?: string;
}

const props = defineProps<{
  id: string;
  data: AgentNodeData;
  selected?: boolean;
}>();

function truncate(str: string, len: number) {
  return str.length > len ? str.slice(0, len) + "…" : str;
}
</script>

<style scoped>
.agent-node {
  background: var(--el-bg-color);
  border: 2px solid var(--el-color-success);
  border-radius: 10px;
  min-width: 180px;
  max-width: 240px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s, border-color 0.2s;
}

.agent-node.selected {
  border-color: var(--el-color-success);
  box-shadow: 0 0 0 3px var(--el-color-success-light-7);
}

.agent-node__header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px 8px;
  border-bottom: 1px solid var(--el-border-color-light);
  background: var(--el-color-success-light-9);
  border-radius: 8px 8px 0 0;
}

.agent-node__icon {
  font-size: 16px;
  color: var(--el-color-success);
  flex-shrink: 0;
}

.agent-node__title {
  font-weight: 600;
  font-size: 13px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--el-text-color-primary);
}

.agent-node__body {
  padding: 8px 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.agent-node__info {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.agent-node__info .el-icon {
  font-size: 13px;
}

.agent-node__instructions {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
  margin-top: 2px;
  line-height: 1.4;
}
</style>
