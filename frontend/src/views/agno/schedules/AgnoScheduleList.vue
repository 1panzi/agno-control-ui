<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Schedules</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" border stripe highlight-current-row>
        <template #empty><el-empty :image-size="80" description="暂无数据" /></template>
        <el-table-column label="Schedule ID" prop="schedule_id" min-width="280" show-overflow-tooltip />
        <el-table-column label="名称" prop="name" min-width="160" show-overflow-tooltip />
        <el-table-column label="Cron" prop="cron_expression" min-width="140" show-overflow-tooltip />
        <el-table-column label="状态" min-width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.enabled ? 'success' : 'info'" size="small">{{ row.enabled ? '启用' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Agent ID" prop="agent_id" min-width="140" show-overflow-tooltip />
        <el-table-column label="上次运行" prop="last_run_at" min-width="170" show-overflow-tooltip />
        <el-table-column label="下次运行" prop="next_run_at" min-width="170" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" width="220" align="center">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">详情</el-button>
            <el-button link type="success" v-if="!row.enabled" @click="handleEnable(row)">启用</el-button>
            <el-button link type="warning" v-if="row.enabled" @click="handleDisable(row)">停用</el-button>
            <el-button link type="primary" @click="handleTrigger(row)">触发</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailVisible" title="Schedule 详情" width="700px" top="5vh">
      <pre class="json-detail">{{ detailJson }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import AgnoSchedulesAPI from "@/api/agno/schedules";

const loading = ref(false);
const tableData = ref<any[]>([]);
const detailVisible = ref(false);
const detailJson = ref("");

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoSchedulesAPI.listSchedules();
    tableData.value = Array.isArray(res.data) ? res.data : [];
  } catch (e) {
    console.error("loadData error:", e);
  } finally {
    loading.value = false;
  }
}

async function showDetail(row: any) {
  try {
    const res = await AgnoSchedulesAPI.getSchedule(row.schedule_id);
    detailJson.value = JSON.stringify(res.data, null, 2);
  } catch {
    detailJson.value = JSON.stringify(row, null, 2);
  }
  detailVisible.value = true;
}

async function handleEnable(row: any) {
  try {
    await AgnoSchedulesAPI.enableSchedule(row.schedule_id);
    ElMessage.success("已启用");
    loadData();
  } catch (e) {
    console.error("enable error:", e);
  }
}

async function handleDisable(row: any) {
  try {
    await AgnoSchedulesAPI.disableSchedule(row.schedule_id);
    ElMessage.success("已停用");
    loadData();
  } catch (e) {
    console.error("disable error:", e);
  }
}

async function handleTrigger(row: any) {
  try {
    await AgnoSchedulesAPI.triggerSchedule(row.schedule_id);
    ElMessage.success("已触发");
  } catch (e) {
    console.error("trigger error:", e);
  }
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 70vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
