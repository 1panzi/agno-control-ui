<template>
  <div class="team-node" :class="{ selected: props.selected }">
    <Handle type="target" :position="Position.Top" />
    <div class="team-node__header">
      <el-icon class="team-node__icon"><UserFilled /></el-icon>
      <span class="team-node__title">{{ data.name || '未命名团队' }}</span>
      <el-tag size="small" class="team-node__mode">{{ modeLabel }}</el-tag>
    </div>
    <div class="team-node__body">
      <div v-if="data.modelLabel" class="team-node__info">
        <el-icon><Cpu /></el-icon>
        <span>{{ data.modelLabel }}</span>
      </div>
      <div v-if="data.memberCount !== undefined" class="team-node__info">
        <el-icon><Service /></el-icon>
        <span>{{ data.memberCount }} 个成员</span>
      </div>
      <div v-if="data.instructions" class="team-node__instructions">
        {{ truncate(data.instructions, 60) }}
      </div>
    </div>
    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { Handle, Position } from "@vue-flow/core";
import { UserFilled, Cpu, Service } from "@element-plus/icons-vue";

interface TeamNodeData {
  name?: string;
  mode?: string;
  modelLabel?: string;
  memberCount?: number;
  instructions?: string;
}

const props = defineProps<{
  id: string;
  data: TeamNodeData;
  selected?: boolean;
}>();

const MODE_LABELS: Record<string, string> = {
  coordinate: "协调",
  route: "路由",
  collaborate: "协作",
};

const modeLabel = computed(() => MODE_LABELS[props.data.mode ?? "coordinate"] ?? props.data.mode ?? "协调");

function truncate(str: string, len: number) {
  return str.length > len ? str.slice(0, len) + "…" : str;
}
</script>

<style scoped>
.team-node {
  background: var(--el-bg-color);
  border: 2px solid var(--el-color-primary);
  border-radius: 10px;
  min-width: 200px;
  max-width: 260px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s, border-color 0.2s;
}

.team-node.selected {
  border-color: var(--el-color-primary);
  box-shadow: 0 0 0 3px var(--el-color-primary-light-7);
}

.team-node__header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px 8px;
  border-bottom: 1px solid var(--el-border-color-light);
  background: var(--el-color-primary-light-9);
  border-radius: 8px 8px 0 0;
}

.team-node__icon {
  font-size: 16px;
  color: var(--el-color-primary);
  flex-shrink: 0;
}

.team-node__title {
  font-weight: 600;
  font-size: 13px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--el-text-color-primary);
}

.team-node__mode {
  flex-shrink: 0;
}

.team-node__body {
  padding: 8px 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.team-node__info {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.team-node__info .el-icon {
  font-size: 13px;
}

.team-node__instructions {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
  margin-top: 2px;
  line-height: 1.4;
}
</style>
