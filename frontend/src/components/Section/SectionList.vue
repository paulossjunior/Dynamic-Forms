<template>
  <div class="space-y-4">
    <div v-if="sections.length === 0" class="text-center py-6 border-2 border-dashed border-gray-300 rounded-lg text-sm text-gray-500">
      No sections defined for this form yet.
    </div>
    <div v-else class="space-y-2">
      <div 
        v-for="(section, index) in sections" 
        :key="section.id || index"
        class="group bg-white p-3 rounded-md border border-gray-200 shadow-sm hover:border-green-300 transition-colors"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
             <div class="cursor-grab text-gray-400 group-hover:text-green-500">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                 <path d="M5 12a1 1 0 102 0 1 1 0 00-2 0zm0-4a1 1 0 102 0 1 1 0 00-2 0zm4 4a1 1 0 102 0 1 1 0 00-2 0zm0-4a1 1 0 102 0 1 1 0 00-2 0zm4 4a1 1 0 102 0 1 1 0 00-2 0zm0-4a1 1 0 102 0 1 1 0 00-2 0z" />
               </svg>
             </div>
             <div>
               <h5 class="text-sm font-semibold text-gray-900">{{ section.name }}</h5>
               <p v-if="section.description" class="text-xs text-gray-500 truncate max-w-xs">{{ section.description }}</p>
             </div>
          </div>
          <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button 
              @click="$emit('edit', section)"
              class="p-1 text-blue-600 hover:bg-blue-50 rounded"
              title="Edit Section"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
            <button 
              @click="$emit('delete', section.id)"
              class="p-1 text-red-600 hover:bg-red-50 rounded"
              title="Delete Section"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  sections: {
    type: Array,
    required: true
  }
})

defineEmits(['edit', 'delete', 'reorder'])
</script>
