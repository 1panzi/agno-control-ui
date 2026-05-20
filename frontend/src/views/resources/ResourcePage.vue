<template>
  <ResourceList :category="category" :category-label="label" />
</template>

<script setup lang="ts">
import ResourceList from "./components/ResourceList.vue";

defineProps<{ category: string; label: string }>();
</script>
