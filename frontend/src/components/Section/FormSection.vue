<template>
  <div class="border-t border-gray-100 first:border-0 pt-6 mt-6 first:pt-0 first:mt-0">
    <div class="mb-4">
      <h3 class="text-lg font-bold text-gray-900">{{ section.name }}</h3>
      <p v-if="section.description" class="text-sm text-gray-500 mt-1">{{ section.description }}</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  section: {
    type: Object,
    required: true
  }
})
</script>
