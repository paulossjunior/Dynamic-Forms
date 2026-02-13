<template>
  <div class="flex flex-col">
    <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
        <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Custom Data</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="person in people" :key="person.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ person.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ person.email }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">
                  <pre class="whitespace-pre-wrap font-mono text-xs bg-gray-50 p-2 rounded border border-gray-100">{{ formatJSON(person.custom_data) }}</pre>
                </td>
              </tr>
              <tr v-if="people.length === 0">
                 <td colspan="3" class="px-6 py-10 text-center text-sm text-gray-500">
                    No people found. 
                    <router-link to="/create" class="text-green-600 hover:text-green-900 font-medium">Create one?</router-link>
                 </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const people = ref([])
const API_URL = 'http://localhost:8000/api'

onMounted(async () => {
  try {
    const response = await axios.get(`${API_URL}/people/`)
    people.value = response.data
  } catch (error) {
    console.error('Error fetching people:', error)
  }
})

const formatJSON = (jsonString) => {
    try {
        const obj = JSON.parse(jsonString)
        return JSON.stringify(obj, null, 2)
    } catch(e) {
        return jsonString
    }
}
</script>
