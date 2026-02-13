<template>
  <div class="space-y-6">
    <div class="md:grid md:grid-cols-3 md:gap-6">
      <div class="md:col-span-1">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Form Builder</h3>
        <p class="mt-1 text-sm text-gray-500">Create reusable form templates by selecting from existing fields.</p>
      </div>
      <div class="mt-5 md:mt-0 md:col-span-2">
        <form @submit.prevent="createForm">
          <div class="shadow sm:rounded-md sm:overflow-hidden">
            <div class="px-4 py-5 bg-white space-y-6 sm:p-6">
              
              <div class="grid grid-cols-6 gap-6">
                <!-- Form Name -->
                <div class="col-span-6">
                  <label class="block text-sm font-medium text-gray-700">Form Name</label>
                  <input 
                    v-model="form.name" 
                    type="text" 
                    required 
                    placeholder="e.g. Employee Onboarding"
                    class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                  >
                </div>
                
                <!-- Description -->
                <div class="col-span-6">
                   <label class="block text-sm font-medium text-gray-700">Description</label>
                   <textarea
                      v-model="form.description"
                      rows="3"
                      class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                   ></textarea>
                </div>

                <!-- Fields Selection -->
                <div class="col-span-6">
                  <label class="block text-sm font-medium text-gray-700 mb-2">Select Fields</label>
                  <div class="space-y-2 max-h-80 overflow-y-auto border border-gray-200 rounded-md p-4">
                    <div v-for="field in availableFields" :key="field.id" class="flex items-start justify-between">
                      <div class="flex items-center h-5">
                        <input
                          :id="`field-${field.id}`"
                          type="checkbox"
                          :checked="isSelected(field.id)"
                          @change="toggleField(field.id)"
                          class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
                        >
                         <div class="ml-3 text-sm">
                            <label :for="`field-${field.id}`" class="font-medium text-gray-700">{{ field.label }}</label>
                            <span class="text-gray-500"> ({{ field.key_name }} - {{ field.field_type }})</span>
                          </div>
                      </div>
                      
                      <!-- Required Checkbox (Only visible if field is selected) -->
                      <div v-if="isSelected(field.id)" class="flex items-center">
                          <input
                            :id="`req-${field.id}`"
                            type="checkbox"
                            :checked="isRequired(field.id)"
                            @change="toggleRequired(field.id)"
                            class="focus:ring-red-500 h-4 w-4 text-red-600 border-gray-300 rounded"
                          >
                          <label :for="`req-${field.id}`" class="ml-2 text-xs text-gray-500">Required?</label>
                      </div>
                    </div>
                    <div v-if="availableFields.length === 0" class="text-sm text-gray-500 italic">
                        No custom fields available. Go to Admin Fields to create some.
                    </div>
                  </div>
                </div>

              </div>
            </div>
            <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
              <button 
                type="submit" 
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-200"
              >
                Create Template
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
    
    <!-- List Existing Forms -->
    <div class="flex flex-col mt-8">
      <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
          <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fields Cont.</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="t in templates" :key="t.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ t.name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ t.description }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ t.fields ? t.fields.length : 0 }}
                  </td>
                </tr>
                 <tr v-if="templates.length === 0">
                    <td colspan="3" class="px-6 py-4 text-center text-sm text-gray-500">No templates found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const availableFields = ref([])
const templates = ref([])

const form = ref({
  name: '',
  description: '',
  fields: [] // Array of { field_id: int, is_required: bool }
})

const API_URL = 'http://localhost:8000/api'

const fetchFields = async () => {
    try {
        const response = await axios.get(`${API_URL}/fields/person`)
        availableFields.value = response.data
    } catch (e) {
        console.error(e)
    }
}

const fetchTemplates = async () => {
    try {
        const response = await axios.get(`${API_URL}/forms/`)
        templates.value = response.data
    } catch (e) {
        console.error(e)
    }
}

const isSelected = (id) => {
    return form.value.fields.some(f => f.field_id === id)
}

const isRequired = (id) => {
    const field = form.value.fields.find(f => f.field_id === id)
    return field ? field.is_required : false
}

const toggleField = (id) => {
    const index = form.value.fields.findIndex(f => f.field_id === id)
    if (index === -1) {
        // Add
        form.value.fields.push({ field_id: id, is_required: false })
    } else {
        // Remove
        form.value.fields.splice(index, 1)
    }
}

const toggleRequired = (id) => {
    const field = form.value.fields.find(f => f.field_id === id)
    if (field) {
        field.is_required = !field.is_required
    }
}


const createForm = async () => {
    try {
        await axios.post(`${API_URL}/forms/`, form.value)
        form.value.name = ''
        form.value.description = ''
        form.value.fields = []
        await fetchTemplates()
    } catch (e) {
        alert("Error creating form: " + e.message)
    }
}

onMounted(() => {
    fetchFields()
    fetchTemplates()
})
</script>
