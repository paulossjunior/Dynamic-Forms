<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
    <h4 class="text-sm font-medium text-gray-900 mb-4">
      {{ isEditing ? 'Edit Section' : 'Add New Section' }}
    </h4>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-xs font-medium text-gray-700 uppercase tracking-wider">Section Name</label>
        <input 
          v-model="formData.name" 
          type="text" 
          required 
          placeholder="e.g. Personal Information"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm"
        >
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-700 uppercase tracking-wider">Description</label>
        <textarea 
          v-model="formData.description" 
          rows="2"
          placeholder="Optional description..."
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm"
        ></textarea>
      </div>
      <div class="flex justify-end space-x-2">
        <button 
          v-if="isEditing"
          type="button" 
          @click="$emit('cancel')"
          class="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
        >
          Cancel
        </button>
        <button 
          type="submit"
          class="inline-flex items-center px-3 py-1.5 border border-transparent shadow-sm text-xs font-medium rounded text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          {{ isEditing ? 'Update Section' : 'Add Section' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({ name: '', description: '' })
  },
  isEditing: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = ref({ ...props.initialData })

watch(() => props.initialData, (newVal) => {
  formData.value = { ...newVal }
}, { deep: true })

const handleSubmit = () => {
  emit('submit', { ...formData.value })
  if (!props.isEditing) {
    formData.value = { name: '', description: '' }
  }
}
</script>
