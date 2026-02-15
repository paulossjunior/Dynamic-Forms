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

                <!-- Inline Section Creator -->
                <div class="col-span-6 border-t border-gray-200 pt-4">
                  <h4 class="text-sm font-medium text-gray-900 mb-2">Create Sections (Optional)</h4>
                  <div class="flex items-center space-x-2 mb-2">
                    <input 
                      v-model="newSectionName" 
                      type="text" 
                      placeholder="New Section Name"
                      @keydown.enter.prevent="addDraftSection"
                      class="flex-1 appearance-none block px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                    >
                    <button 
                      type="button" 
                      @click="addDraftSection"
                      class="inline-flex justify-center py-2 px-3 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Add Section
                    </button>
                  </div>
                  
                  <!-- List of Draft Sections -->
                  <div v-if="draftSections.length > 0" class="flex flex-wrap gap-2 mt-2">
                    <span 
                      v-for="(section, idx) in draftSections" 
                      :key="section.temp_id" 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {{ section.name }}
                      <button 
                        type="button" 
                        @click="removeDraftSection(idx)"
                        class="ml-1.5 inline-flex items-center justify-center h-4 w-4 rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-500 focus:outline-none"
                      >
                        <span class="sr-only">Remove section</span>
                        <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                          <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                        </svg>
                      </button>
                    </span>
                  </div>
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
                      
                      <!-- Section Selection & Required Checkbox (Only visible if field is selected) -->
                      <div v-if="isSelected(field.id)" class="flex items-center space-x-4">
                          <div class="flex items-center">
                              <label :for="`section-${field.id}`" class="mr-2 text-xs text-gray-500 uppercase tracking-wider">Section:</label>
                              <select 
                                :id="`section-${field.id}`"
                                :value="getFieldSectionValue(field.id)"
                                @change="updateFieldSection(field.id, $event.target.value)"
                                class="text-xs border-gray-300 rounded focus:ring-green-500 focus:border-green-500 py-0.5"
                              >
                                <option value="">No Section</option>
                                <optgroup v-if="draftSections.length > 0" label="New Sections">
                                  <option v-for="s in draftSections" :key="s.temp_id" :value="`temp:${s.temp_id}`">{{ s.name }}</option>
                                </optgroup>
                                <!-- Existing sections from other forms are NOT available here generally, unless we fetch all sections. 
                                     Assuming we replicate behavior: we map to sections being created OR null. 
                                     If we supported picking sections from existing forms to COPY, we would list them. 
                                     For now, let's list sectionsForDraft which seemed to be maybe for existing templates? 
                                     The original code had `sectionsForDraft` but it was not populated? 
                                     Actually `sectionsForDraft` was defined but never used/populated in the original code properly 
                                     link to a specific template. 
                                     Let's stick to the Draft Sections we just created.
                                -->
                              </select>
                          </div>
                          
                          <div class="flex items-center">
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
                  <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="t in templates" :key="t.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ t.name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ t.description }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ t.fields ? t.fields.length : 0 }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button @click="openSectionManager(t)" class="text-green-600 hover:text-green-900 mr-4">Manage Sections</button>
                  </td>
                </tr>
                 <tr v-if="templates.length === 0">
                    <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500">No templates found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Section Manager Modal (Simulated) -->
    <div v-if="selectedTemplateForSections" class="fixed inset-0 z-10 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="closeSectionManager"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-xl sm:w-full sm:p-6">
          <div class="absolute top-0 right-0 pt-4 pr-4">
            <button @click="closeSectionManager" type="button" class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none">
              <span class="sr-only">Close</span>
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
              Manage Sections: {{ selectedTemplateForSections.name }}
            </h3>
            <SectionManager :form-id="selectedTemplateForSections.id" />
          </div>
          <div class="mt-5 sm:mt-6">
            <button @click="closeSectionManager" type="button" class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:text-sm">
              Done
            </button>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SectionManager from '../components/Section/SectionManager.vue'

const availableFields = ref([])
const templates = ref([])
const selectedTemplateForSections = ref(null)

// Draft sections state
const draftSections = ref([]) // Array of { temp_id: string, name: string, description: string, order_index: int }
const newSectionName = ref('')

const form = ref({
  name: '',
  description: '',
  fields: [], // Array of { field_id: int, is_required: bool, section_id: int|null, section_temp_id: string|null }
  sections: []
})


const API_URL = 'http://localhost:8001/api'

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

const getFieldLink = (id) => {
    return form.value.fields.find(f => f.field_id === id)
}

const toggleField = (id) => {
    const index = form.value.fields.findIndex(f => f.field_id === id)
    if (index === -1) {
        // Add
        form.value.fields.push({ field_id: id, is_required: false, section_id: null, section_temp_id: null })
    } else {
        // Remove
        form.value.fields.splice(index, 1)
    }
}

const toggleRequired = (id) => {
    const field = getFieldLink(id)
    if (field) {
        field.is_required = !field.is_required
    }
}

// Logic for Draft Sections
const addDraftSection = () => {
    if (!newSectionName.value.trim()) return
    const tempId = 'temp_' + Date.now() + '_' + Math.floor(Math.random() * 1000)
    draftSections.value.push({
        temp_id: tempId,
        name: newSectionName.value.trim(),
        description: '',
        order_index: draftSections.value.length
    })
    newSectionName.value = ''
}

const removeDraftSection = (index) => {
    const section = draftSections.value[index]
    draftSections.value.splice(index, 1)
    // Clear references in fields
    form.value.fields.forEach(f => {
        if (f.section_temp_id === section.temp_id) {
            f.section_temp_id = null
        }
    })
}

const getFieldSectionValue = (fieldId) => {
    const field = getFieldLink(fieldId)
    if (!field) return ""
    if (field.section_temp_id) return `temp:${field.section_temp_id}`
    return ""
}

const updateFieldSection = (fieldId, value) => {
    const field = getFieldLink(fieldId)
    if (!field) return
    
    if (!value) {
        field.section_id = null
        field.section_temp_id = null
        return
    }
    
    if (value.startsWith('temp:')) {
        field.section_id = null
        field.section_temp_id = value.replace('temp:', '')
    } else {
        // Handle existing IDs if we were supporting them (not for now as per logic)
        field.section_id = parseInt(value, 10)
        field.section_temp_id = null
    }
}


const openSectionManager = (template) => {
    selectedTemplateForSections.value = template
}

const closeSectionManager = async () => {
    selectedTemplateForSections.value = null
    await fetchTemplates()
}



const createForm = async () => {
    try {
        // Prepare payload including sections
        const payload = {
            ...form.value,
            sections: draftSections.value
        }
        
        await axios.post(`${API_URL}/forms/`, payload)
        
        // Reset form
        form.value.name = ''
        form.value.description = ''
        form.value.fields = []
        draftSections.value = []
        newSectionName.value = ''
        
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
