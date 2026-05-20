<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Agents</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>
      <el-table v-loading="loading" :data="tableData" border stripe highlight-current-row>
        <template #empty><el-empty :image-size="80" description="暂无数据" /></template>
        <el-table-column label="ID" prop="id" min-width="160" show-overflow-tooltip />
        <el-table-column label="名称" prop="name" min-width="160" show-overflow-tooltip />
        <el-table-column label="描述" prop="description" min-width="200" show-overflow-tooltip />
        <el-table-column label="DB ID" prop="db_id" min-width="280" show-overflow-tooltip />
        <el-table-column label="模型" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.model?.name || row.model?.model || '-' }}
            <span v-if="row.model?.provider" style="color: var(--el-text-color-secondary)">
              ({{ row.model.provider }})
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="80" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="Agent 详情" width="700px" top="5vh">
      <pre class="json-detail">{{ detailJson }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import AgnoAgentAPI from "@/api/agno/agent";

const loading = ref(false);
const tableData = ref<any[]>([]);
const detailVisible = ref(false);
const detailJson = ref("");

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoAgentAPI.listAgents();
    tableData.value = res.data ?? [];
  } catch (e) {
    console.error("loadData error:", e);
  } finally {
    loading.value = false;
  }
}

function showDetail(row: any) {
  detailJson.value = JSON.stringify(row, null, 2);
  detailVisible.value = true;
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 70vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
