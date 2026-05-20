<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Components</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>

      <div class="filter-bar">
        <el-input v-model="filterType" placeholder="组件类型" clearable style="width: 160px" @keyup.enter="loadData" />
        <el-button type="primary" @click="loadData">查询</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe highlight-current-row>
        <template #empty><el-empty :image-size="80" description="暂无数据" /></template>
        <el-table-column label="Component ID" prop="component_id" min-width="280" show-overflow-tooltip />
        <el-table-column label="类型" prop="component_type" min-width="120" show-overflow-tooltip />
        <el-table-column label="名称" prop="name" min-width="160" show-overflow-tooltip />
        <el-table-column label="描述" prop="description" min-width="200" show-overflow-tooltip />
        <el-table-column label="创建时间" prop="created_at" min-width="170" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" width="140" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">详情</el-button>
            <el-button link type="primary" @click="showConfigs(row)">Configs</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="Component 详情" width="700px" top="5vh">
      <pre class="json-detail">{{ detailJson }}</pre>
    </el-dialog>

    <el-dialog v-model="configsVisible" title="Component Configs" width="700px" top="5vh">
      <pre class="json-detail">{{ configsJson }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import AgnoComponentsAPI from "@/api/agno/components";

const loading = ref(false);
const tableData = ref<any[]>([]);
const filterType = ref("");
const detailVisible = ref(false);
const detailJson = ref("");
const configsVisible = ref(false);
const configsJson = ref("");

async function loadData() {
  loading.value = true;
  try {
    const params = filterType.value ? { component_type: filterType.value } : undefined;
    const res = await AgnoComponentsAPI.listComponents(params);
    tableData.value = Array.isArray(res.data) ? res.data : [];
  } catch (e) {
    console.error("loadData error:", e);
  } finally {
    loading.value = false;
  }
}

async function showDetail(row: any) {
  try {
    const res = await AgnoComponentsAPI.getComponent(row.component_id);
    detailJson.value = JSON.stringify(res.data, null, 2);
  } catch {
    detailJson.value = JSON.stringify(row, null, 2);
  }
  detailVisible.value = true;
}

async function showConfigs(row: any) {
  try {
    const res = await AgnoComponentsAPI.getConfigs(row.component_id);
    configsJson.value = JSON.stringify(res.data, null, 2);
  } catch (e) {
    configsJson.value = "加载失败";
  }
  configsVisible.value = true;
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.filter-bar { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 70vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
