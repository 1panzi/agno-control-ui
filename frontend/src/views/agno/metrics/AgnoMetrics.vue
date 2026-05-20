<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Metrics</span>
          <div>
            <el-button type="warning" size="small" @click="refreshMetrics">刷新指标</el-button>
            <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <pre class="json-detail">{{ metricsJson }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import AgnoMetricsAPI from "@/api/agno/metrics";

const loading = ref(false);
const metricsJson = ref("");

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoMetricsAPI.getMetrics();
    metricsJson.value = JSON.stringify(res.data, null, 2);
  } catch (e) {
    console.error("loadData error:", e);
    metricsJson.value = "加载失败";
  } finally {
    loading.value = false;
  }
}

async function refreshMetrics() {
  loading.value = true;
  try {
    await AgnoMetricsAPI.refreshMetrics();
    ElMessage.success("指标已刷新");
    await loadData();
  } catch (e) {
    console.error("refresh error:", e);
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped>
.card-header { display: flex; align-items: center; justify-content: space-between; }
.json-detail { background: var(--el-fill-color-light); padding: 16px; border-radius: 6px; font-size: 12px; max-height: 80vh; overflow: auto; white-space: pre-wrap; word-break: break-all; }
</style>
