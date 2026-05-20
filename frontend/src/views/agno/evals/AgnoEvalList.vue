<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Evals</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" border stripe highlight-current-row>
        <template #empty><el-empty :image-size="80" description="暂无数据" /></template>
        <el-table-column label="Eval Run ID" prop="eval_run_id" min-width="280" show-overflow-tooltip />
        <el-table-column label="名称" prop="name" min-width="160" show-overflow-tooltip />
        <el-table-column label="状态" prop="status" min-width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.status === 'completed' ? 'success' : row.status === 'failed' ? 'danger' : 'info'"
              size="small"
            >{{ row.status || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="总测试" prop="total_tests" min-width="80" align="center" />
        <el-table-column label="通过" prop="passed_tests" min-width="80" align="center" />
        <el-table-column label="失败" prop="failed_tests" min-width="80" align="center" />
        <el-table-column label="Agent ID" prop="agent_id" min-width="140" show-overflow-tooltip />
        <el-table-column label="创建时间" prop="created_at" min-width="170" show-overflow-tooltip />
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

    <el-dialog v-model="detailVisible" title="Eval Run 详情" width="700px" top="5vh">
      <pre class="json-detail">{{ detailJson }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import AgnoEvalsAPI from "@/api/agno/evals";
import Pagination from "@/components/Pagination/index.vue";

const loading = ref(false);
const tableData = ref<any[]>([]);
const total = ref(0);
const detailVisible = ref(false);
const detailJson = ref("");

const query = reactive({
  page: 1,
  limit: 20,
});

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoEvalsAPI.listEvalRuns(query);
    const body = res.data;
    if (Array.isArray(body)) {
      tableData.value = body;
      total.value = body.length;
    } else {
      tableData.value = body?.data ?? [];
      total.value = body?.meta?.total_count ?? 0;
    }
  } catch (e) {
    console.error("loadData error:", e);
  } finally {
    loading.value = false;
  }
}

async function showDetail(row: any) {
  try {
    const res = await AgnoEvalsAPI.getEvalRun(row.eval_run_id);
    detailJson.value = JSON.stringify(res.data, null, 2);
  } catch {
    detailJson.value = JSON.stringify(row, null, 2);
  }
  detailVisible.value = true;
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 70vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
