<template>
  <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
    <div class="md:grid md:grid-cols-3 md:gap-6">
      <div class="md:col-span-1">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Personal Information</h3>
        <p class="mt-1 text-sm text-gray-500">Select a template to dynamically load fields.</p>
      </div>
      <div class="mt-5 md:mt-0 md:col-span-2">
        <form @submit.prevent="savePerson">
          <div class="grid grid-cols-6 gap-6">
            
            <!-- Template Selector -->
             <div class="col-span-6">
              <label class="block text-sm font-medium text-gray-700">Form Template</label>
              <select 
                v-model="selectedFormId" 
                @change="onFormSelect"
                class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
              >
                <option :value="null">-- Select a Form Template --</option>
                <option v-for="t in templates" :key="t.id" :value="t.id">
                    {{ t.name }}
                </option>
              </select>
              <p v-if="selectedDescription" class="mt-2 text-sm text-gray-500">{{ selectedDescription }}</p>
            </div>

            <!-- Fixed Fields -->
            <div class="col-span-6 sm:col-span-3">
              <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
              <input 
                v-model="form.name" 
                type="text" 
                id="name" 
                required 
                class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              >
            </div>

            <div class="col-span-6 sm:col-span-3">
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input 
                v-model="form.email" 
                type="email" 
                id="email" 
                required 
                class="mt-1 appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              >
            </div>

            <!-- Dynamic Fields -->
            <div v-if="customFields.length > 0" class="col-span-6 border-t border-gray-200 pt-6 mt-2">
               <h4 class="text-sm font-medium text-gray-900 mb-4 uppercase tracking-wider">Additional Information</h4>
               <FormRenderer 
                  :fields="customFields" 
                  v-model="form.custom_data"
                  :errors="errors"
               />
            </div>
            <div v-else-if="selectedFormId" class="col-span-6 text-center py-4 text-gray-500 text-sm">
                This template has no custom fields.
            </div>
          </div>
          
          <div class="mt-6 text-right">
             <button 
                type="submit" 
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-200"
             >
                Save Person
              </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import FormRenderer from '../components/DynamicForm/FormRenderer.vue'

const router = useRouter()
const templates = ref([])
const selectedFormId = ref(null)
const customFields = ref([])
const errors = ref({})

const form = ref({
  name: '',
  email: '',
  custom_data: {}
})

const API_URL = 'http://localhost:8000/api'

onMounted(async () => {
  try {
    // Fetch available forms
    const response = await axios.get(`${API_URL}/forms/`)
    templates.value = response.data
  } catch (error) {
    console.error('Error fetching forms:', error)
  }
})

const selectedDescription = computed(() => {
    const t = templates.value.find(t => t.id === selectedFormId.value)
    return t ? t.description : ''
})

const onFormSelect = async () => {
    if (!selectedFormId.value) {
        customFields.value = []
        form.value.custom_data = {}
        errors.value = {}
        return
    }
    
    try {
        const response = await axios.get(`${API_URL}/forms/${selectedFormId.value}`)
        // Map the fields from the association object
        customFields.value = response.data.fields.map(assoc => {
            const field = { ...assoc.field } // Create a copy of the field definition
            
            // Check if form requires this field
            if (assoc.is_required) {
                // Parse existing rules or default to empty object
                let rules = {}
                try {
                    rules = typeof field.validation_rules === 'string' 
                         ? JSON.parse(field.validation_rules) 
                         : (field.validation_rules || {})
                } catch { rules = {} }
                
                // Override/Set required to true
                rules.required = true
                field.validation_rules = rules // FormRenderer handles objects or strings
            }
            return field
        })
        
        // Reset custom data and errors
        form.value.custom_data = {}
        errors.value = {}
    } catch (e) {
        console.error("Error fetching form details", e)
    }
}

const validate = () => {
    errors.value = {}
    let isValid = true
    
    customFields.value.forEach(field => {
        const value = form.value.custom_data[field.key_name]
        let rules = {}
        
        try {
            rules = typeof field.validation_rules === 'string' 
                ? JSON.parse(field.validation_rules) 
                : field.validation_rules
        } catch(e) {
            rules = {}
        }
        
        // Required Check
        if (rules.required) {
            if (value === undefined || value === null || value === '' || (Array.isArray(value) && value.length === 0)) {
                errors.value[field.key_name] = `${field.label} is required.`
                isValid = false
                return
            }
        }
        
        // Skip further validation if empty and not required
        if (!value) return
        
        // Min/Max Length (Text)
        if (field.field_type === 'text') {
            if (rules.minLength && value.length < rules.minLength) {
                 errors.value[field.key_name] = `Minimum length is ${rules.minLength} characters.`
                 isValid = false
            }
            if (rules.maxLength && value.length > rules.maxLength) {
                 errors.value[field.key_name] = `Maximum length is ${rules.maxLength} characters.`
                 isValid = false
            }
        }
        
        // Min/Max Value (Number)
        if (field.field_type === 'number') {
            const numVal = Number(value)
            if (rules.min && numVal < rules.min) {
                 errors.value[field.key_name] = `Minimum value is ${rules.min}.`
                 isValid = false
            }
            if (rules.max && numVal > rules.max) {
                 errors.value[field.key_name] = `Maximum value is ${rules.max}.`
                 isValid = false
            }
        }
    })
    
    return isValid
}

const savePerson = async () => {
  if (!validate()) {
      return
  }

  try {
    const payload = {
        ...form.value,
        custom_data: JSON.stringify(form.value.custom_data)
    }
    
    await axios.post(`${API_URL}/people/`, payload)
    router.push('/')
  } catch (error) {
    console.error('Error saving person:', error)
    
    // Handle specific error cases
    if (error.response?.status === 500 && error.response?.data?.detail?.includes('UNIQUE constraint failed: people.email')) {
      alert('❌ Este email já está cadastrado. Por favor, use um email diferente.')
    } else {
      alert('❌ Erro ao salvar pessoa: ' + (error.response?.data?.detail || error.message))
    }
  }
}

</script>
