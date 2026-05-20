<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Memories</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>

      <div class="filter-bar">
        <el-input v-model="query.user_id" placeholder="用户 ID" clearable style="width: 160px" @keyup.enter="handleQuery" />
        <el-input v-model="query.topic" placeholder="主题" clearable style="width: 160px" @keyup.enter="handleQuery" />
        <el-button type="primary" @click="handleQuery">查询</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe highlight-current-row>
        <template #empty><el-empty :image-size="80" description="暂无数据" /></template>
        <el-table-column label="ID" prop="id" min-width="280" show-overflow-tooltip />
        <el-table-column label="Memory" prop="memory" min-width="300" show-overflow-tooltip />
        <el-table-column label="Topic" prop="topic" min-width="120" show-overflow-tooltip />
        <el-table-column label="User ID" prop="user_id" min-width="120" show-overflow-tooltip />
        <el-table-column label="创建时间" prop="created_at" min-width="170" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" width="140" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">详情</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <template #footer>
        <Pagination v-model:page="query.page" v-model:limit="query.limit" :total="total" @pagination="loadData" />
      </template>
    </el-card>

    <el-dialog v-model="detailVisible" title="Memory 详情" width="700px" top="5vh">
      <pre class="json-detail">{{ detailJson }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import AgnoMemoriesAPI from "@/api/agno/memories";
import Pagination from "@/components/Pagination/index.vue";

const loading = ref(false);
const tableData = ref<any[]>([]);
const total = ref(0);
const detailVisible = ref(false);
const detailJson = ref("");

const query = reactive({
  user_id: undefined as string | undefined,
  topic: undefined as string | undefined,
  page: 1,
  limit: 20,
});

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoMemoriesAPI.listMemories(query);
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

function handleQuery() {
  query.page = 1;
  loadData();
}

function showDetail(row: any) {
  detailJson.value = JSON.stringify(row, null, 2);
  detailVisible.value = true;
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确认删除该 Memory?`, "警告", { type: "warning" });
  try {
    await AgnoMemoriesAPI.deleteMemory(row.id);
    ElMessage.success("删除成功");
    loadData();
  } catch (e) {
    console.error("delete error:", e);
  }
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.filter-bar { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 70vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
