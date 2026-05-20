<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Traces</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>

      <div class="filter-bar">
        <el-input v-model="query.agent_id" placeholder="Agent ID" clearable style="width: 160px" @keyup.enter="handleQuery" />
        <el-input v-model="query.session_id" placeholder="Session ID" clearable style="width: 260px" @keyup.enter="handleQuery" />
        <el-select v-model="query.status" placeholder="状态" clearable style="width: 110px" @change="handleQuery">
          <el-option label="OK" value="OK" />
          <el-option label="ERROR" value="ERROR" />
        </el-select>
        <el-button type="primary" @click="handleQuery">查询</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe highlight-current-row>
        <template #empty><el-empty :image-size="80" description="暂无数据" /></template>
        <el-table-column label="Trace ID" prop="trace_id" min-width="160" show-overflow-tooltip />
        <el-table-column label="名称" prop="name" min-width="200" show-overflow-tooltip />
        <el-table-column label="状态" prop="status" min-width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'OK' ? 'success' : 'danger'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="耗时" prop="duration" min-width="100" />
        <el-table-column label="Spans" prop="total_spans" min-width="70" align="center" />
        <el-table-column label="错误" prop="error_count" min-width="70" align="center" />
        <el-table-column label="Input" prop="input" min-width="200" show-overflow-tooltip />
        <el-table-column label="Agent" prop="agent_id" min-width="140" show-overflow-tooltip />
        <el-table-column label="开始时间" prop="start_time" min-width="170" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" width="80" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <template #footer>
        <Pagination v-model:page="query.page" v-model:limit="query.limit" :total="total" @pagination="loadData" />
      </template>
    </el-card>

    <el-dialog v-model="detailVisible" title="Trace 详情" width="800px" top="5vh">
      <pre class="json-detail">{{ detailJson }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import AgnoTracesAPI from "@/api/agno/traces";
import Pagination from "@/components/Pagination/index.vue";

const loading = ref(false);
const tableData = ref<any[]>([]);
const total = ref(0);
const detailVisible = ref(false);
const detailJson = ref("");

const query = reactive({
  agent_id: undefined as string | undefined,
  session_id: undefined as string | undefined,
  status: undefined as string | undefined,
  page: 1,
  limit: 20,
});

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoTracesAPI.listTraces(query);
    const body = res.data;
    tableData.value = body?.data ?? [];
    total.value = body?.meta?.total_count ?? 0;
  } catch (e) {
    console.error("loadData error:", e);
  } finally {
    loading.value = false;
  }
}

function handleQuery() {
  query.page = 1;
  loadData();
}

async function showDetail(row: any) {
  try {
    const res = await AgnoTracesAPI.getTrace(row.trace_id);
    detailJson.value = JSON.stringify(res.data, null, 2);
    detailVisible.value = true;
  } catch {
    detailJson.value = JSON.stringify(row, null, 2);
    detailVisible.value = true;
  }
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.filter-bar { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 70vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
