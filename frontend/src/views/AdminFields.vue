<template>
  <div class="space-y-6">
    <div class="md:grid md:grid-cols-3 md:gap-6">
      <div class="md:col-span-1">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Custom Fields</h3>
        <p class="mt-1 text-sm text-gray-500">Define the schema for your dynamic entities.</p>
      </div>
      <div class="mt-5 md:mt-0 md:col-span-2">
        <form @submit.prevent="createField">
          <div class="shadow sm:rounded-md sm:overflow-hidden">
            <div class="px-4 py-5 bg-white space-y-6 sm:p-6">
              
              <div class="grid grid-cols-6 gap-6">
                <!-- Label -->
                <div class="col-span-6 sm:col-span-3">
                  <label class="block text-sm font-medium text-gray-700">Label</label>
                  <input 
                    v-model="form.label" 
                    type="text" 
                    required 
                    placeholder="e.g. Favorite Color"
                    class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                  >
                </div>

                <!-- Key Name -->
                <div class="col-span-6 sm:col-span-3">
                  <label class="block text-sm font-medium text-gray-700">Key Name (Slug)</label>
                  <input 
                    v-model="form.key_name" 
                    type="text" 
                    required 
                    placeholder="e.g. favorite_color"
                    class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                  >
                </div>

                <!-- Field Type -->
                <div class="col-span-6 sm:col-span-3">
                  <label class="block text-sm font-medium text-gray-700">Type</label>
                  <select 
                    v-model="form.field_type" 
                    class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
                  >
                    <option value="text">Text</option>
                    <option value="number">Number</option>
                    <option value="date">Date</option>
                    <option value="select">Select</option>
                    <option value="multiselect">Multi-Select</option>
                  </select>
                </div>
                
                <!-- Options -->
                <div v-if="['select', 'multiselect'].includes(form.field_type)" class="col-span-6">
                   <label class="block text-sm font-medium text-gray-700">Options (comma separated)</label>
                   <input 
                      v-model="optionsInput" 
                      type="text" 
                      placeholder="Red, Green, Blue"
                      class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                   >
                </div>
                <!-- Validation Rules -->
                <div class="col-span-6 border-t border-gray-200 pt-4 mt-2">
                    <h4 class="text-sm font-medium text-gray-900 mb-2">Validation Rules</h4>
                    <div class="grid grid-cols-6 gap-6">
                        <div class="col-span-6 sm:col-span-2 flex items-center h-full pt-6">
                            <input
                              id="required"
                              v-model="validation.required"
                              type="checkbox"
                              class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
                            >
                            <label for="required" class="ml-2 block text-sm text-gray-900">Required</label>
                        </div>
                        
                        <div v-if="form.field_type === 'text'" class="col-span-6 sm:col-span-2">
                             <label class="block text-sm font-medium text-gray-700">Min Length</label>
                             <input v-model.number="validation.minLength" type="number" class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm">
                        </div>
                        <div v-if="form.field_type === 'text'" class="col-span-6 sm:col-span-2">
                             <label class="block text-sm font-medium text-gray-700">Max Length</label>
                             <input v-model.number="validation.maxLength" type="number" class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm">
                        </div>

                        <div v-if="form.field_type === 'number'" class="col-span-6 sm:col-span-2">
                             <label class="block text-sm font-medium text-gray-700">Min Value</label>
                             <input v-model.number="validation.min" type="number" class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm">
                        </div>
                         <div v-if="form.field_type === 'number'" class="col-span-6 sm:col-span-2">
                             <label class="block text-sm font-medium text-gray-700">Max Value</label>
                             <input v-model.number="validation.max" type="number" class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm sm:text-sm">
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
                Create Field
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- List Existing Fields -->
    <div class="flex flex-col mt-8">
      <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
          <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Label</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Key</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Options</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Validation</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="field in fields" :key="field.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ field.label }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ field.key_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      {{ field.field_type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ field.options }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span v-if="isValidJSON(field.validation_rules)">
                        {{ formatValidation(field.validation_rules) }}
                    </span>
                  </td>
                </tr>
                <tr v-if="fields.length === 0">
                    <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">No custom fields defined yet.</td>
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

const fields = ref([])
const optionsInput = ref('')

const validation = ref({
    required: false,
    minLength: null,
    maxLength: null,
    min: null,
    max: null
})

const form = ref({
  entity_type: 'person',
  key_name: '',
  label: '',
  field_type: 'text',
  options: [],
  validation_rules: {}
})

const API_URL = 'http://localhost:8001/api'

const fetchFields = async () => {
  try {
    const response = await axios.get(`${API_URL}/fields/person`)
    fields.value = response.data
  } catch (error) {
    console.error('Error fetching fields:', error)
  }
}

const createField = async () => {
  if (optionsInput.value) {
    form.value.options = JSON.stringify(optionsInput.value.split(',').map(s => s.trim()))
  } else {
    form.value.options = "[]"
  }
  
  // Construct validation rules JSON
  const rules = {}
  if (validation.value.required) rules.required = true
  if (validation.value.minLength) rules.minLength = validation.value.minLength
  if (validation.value.maxLength) rules.maxLength = validation.value.maxLength
  if (validation.value.min) rules.min = validation.value.min
  if (validation.value.max) rules.max = validation.value.max
  
  form.value.validation_rules = JSON.stringify(rules)

  try {
    await axios.post(`${API_URL}/fields/`, form.value)
    form.value.key_name = ''
    form.value.label = ''
    form.value.field_type = 'text'
    optionsInput.value = ''
    
    // Reset validation
    validation.value = {
        required: false,
        minLength: null,
        maxLength: null,
        min: null,
        max: null
    }
    
    await fetchFields()
  } catch (error) {
    alert('Error creating field: ' + error.message)
  }
}

const isValidJSON = (str) => {
    try { JSON.parse(str); return true } catch { return false }
}

const formatValidation = (str) => {
    try {
        const obj = JSON.parse(str)
        return Object.keys(obj).map(k => `${k}: ${obj[k]}`).join(', ')
    } catch { return '' }
}

onMounted(fetchFields)
</script>
