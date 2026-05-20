<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Agno Registry</span>
          <el-button type="primary" icon="Refresh" circle size="small" @click="loadData" />
        </div>
      </template>
      <div v-loading="loading">
        <pre class="json-detail">{{ registryJson }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import AgnoRegistryAPI from "@/api/agno/registry";

const loading = ref(false);
const registryJson = ref("");

async function loadData() {
  loading.value = true;
  try {
    const res = await AgnoRegistryAPI.getRegistry();
    registryJson.value = JSON.stringify(res.data, null, 2);
  } catch (e) {
    console.error("loadData error:", e);
    registryJson.value = "加载失败";
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
