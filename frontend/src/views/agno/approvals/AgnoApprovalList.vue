<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Approvals</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>

      <div class="filter-bar">
        <el-input v-model="query.agent_id" placeholder="Agent ID" clearable style="width: 160px" @keyup.enter="handleQuery" />
        <el-select v-model="query.status" placeholder="状态" clearable style="width: 130px" @change="handleQuery">
          <el-option label="Pending" value="pending" />
          <el-option label="Approved" value="approved" />
          <el-option label="Rejected" value="rejected" />
        </el-select>
        <el-button type="primary" @click="handleQuery">查询</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe highlight-current-row>
        <template #empty><el-empty :image-size="80" description="暂无数据" /></template>
        <el-table-column label="Approval ID" prop="approval_id" min-width="280" show-overflow-tooltip />
        <el-table-column label="Agent ID" prop="agent_id" min-width="140" show-overflow-tooltip />
        <el-table-column label="Tool" prop="tool_name" min-width="140" show-overflow-tooltip />
        <el-table-column label="状态" prop="status" min-width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.status === 'approved' ? 'success' : row.status === 'rejected' ? 'danger' : 'warning'"
              size="small"
            >{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_at" min-width="170" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" width="200" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">详情</el-button>
            <template v-if="row.status === 'pending'">
              <el-button link type="success" @click="handleResolve(row, true)">批准</el-button>
              <el-button link type="danger" @click="handleResolve(row, false)">拒绝</el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="Approval 详情" width="700px" top="5vh">
      <pre class="json-detail">{{ detailJson }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage } from "element-plus";
import AgnoApprovalsAPI from "@/api/agno/approvals";

const loading = ref(false);
const tableData = ref<any[]>([]);
const detailVisible = ref(false);
const detailJson = ref("");

const query = reactive({
  agent_id: undefined as string | undefined,
  status: undefined as string | undefined,
});

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoApprovalsAPI.listApprovals(query);
    tableData.value = Array.isArray(res.data) ? res.data : [];
  } catch (e) {
    console.error("loadData error:", e);
  } finally {
    loading.value = false;
  }
}

function handleQuery() {
  loadData();
}

async function showDetail(row: any) {
  try {
    const res = await AgnoApprovalsAPI.getApproval(row.approval_id);
    detailJson.value = JSON.stringify(res.data, null, 2);
  } catch {
    detailJson.value = JSON.stringify(row, null, 2);
  }
  detailVisible.value = true;
}

async function handleResolve(row: any, approved: boolean) {
  try {
    await AgnoApprovalsAPI.resolveApproval(row.approval_id, { approved });
    ElMessage.success(approved ? "已批准" : "已拒绝");
    loadData();
  } catch (e) {
    console.error("resolve error:", e);
  }
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.filter-bar { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 70vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
