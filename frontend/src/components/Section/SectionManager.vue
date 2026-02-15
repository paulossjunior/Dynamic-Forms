<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h4 class="text-sm font-medium text-gray-900">Form Sections</h4>
      <button 
        v-if="!showForm"
        @click="openAddForm"
        class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-green-700 bg-green-100 hover:bg-green-200"
      >
        Add Section
      </button>
    </div>

    <!-- Section Form (Add/Edit) -->
    <div v-if="showForm" class="mb-4">
      <SectionForm 
        :is-editing="!!editingSection"
        :initial-data="editingSection || { name: '', description: '' }"
        @submit="handleFormSubmit"
        @cancel="closeForm"
      />
    </div>

    <!-- Section List -->
    <SectionList 
      :sections="sections"
      @edit="openEditForm"
      @delete="handleDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import SectionForm from './SectionForm.vue'
import SectionList from './SectionList.vue'

const props = defineProps({
  formId: {
    type: Number,
    required: true
  }
})

const API_URL = 'http://localhost:8001/api'
const sections = ref([])
const showForm = ref(false)
const editingSection = ref(null)

const fetchSections = async () => {
  try {
    const response = await axios.get(`${API_URL}/forms/${props.formId}/sections/`)
    sections.value = response.data
  } catch (e) {
    console.error('Error fetching sections:', e)
  }
}

const openAddForm = () => {
  editingSection.value = null
  showForm.value = true
}

const openEditForm = (section) => {
  editingSection.value = section
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  editingSection.value = null
}

const handleFormSubmit = async (data) => {
  try {
    if (editingSection.value) {
      await axios.put(`${API_URL}/sections/${editingSection.value.id}`, {
        ...data,
        form_id: props.formId,
        order_index: editingSection.value.order_index
      })
    } else {
      await axios.post(`${API_URL}/sections/`, {
        ...data,
        form_id: props.formId,
        order_index: sections.value.length
      })
    }
    await fetchSections()
    closeForm()
  } catch (e) {
    alert('Error saving section: ' + (e.response?.data?.detail || e.message))
  }
}

const handleDelete = async (sectionId) => {
  if (!confirm('Are you sure you want to delete this section? Fields will be preserved but unassociated.')) return
  try {
    await axios.delete(`${API_URL}/sections/${sectionId}`)
    await fetchSections()
  } catch (e) {
    alert('Error deleting section: ' + e.message)
  }
}

onMounted(fetchSections)
</script>
