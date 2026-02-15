<template>
  <div class="flex flex-col">
    <!-- Desktop Table -->
    <div class="hidden md:block -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
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

    <!-- Mobile Cards -->
    <div class="md:hidden space-y-4">
      <div v-for="person in people" :key="person.id" class="bg-white shadow rounded-lg p-4 border border-gray-200">
        <div class="flex items-center space-x-3 mb-3">
          <div class="flex-shrink-0">
            <div class="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center text-green-600 font-bold">
              {{ person.name.charAt(0).toUpperCase() }}
            </div>
          </div>
          <div>
             <h3 class="text-sm font-medium text-gray-900">{{ person.name }}</h3>
             <p class="text-sm text-gray-500 truncate">{{ person.email }}</p>
          </div>
        </div>
        <div v-if="person.custom_data" class="mt-2 border-t border-gray-100 pt-2">
           <p class="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">Details</p>
           <dl class="grid grid-cols-1 gap-x-4 gap-y-2 sm:grid-cols-2">
             <div v-for="item in parseCustomData(person.custom_data)" :key="item.key" class="sm:col-span-1">
               <dt class="text-xs font-medium text-gray-500 capitalize">{{ item.key.replace(/_/g, ' ') }}</dt>
               <dd class="mt-1 text-sm text-gray-900">{{ item.value }}</dd>
             </div>
           </dl>
        </div>
      </div>
      
      <div v-if="people.length === 0" class="text-center py-10 bg-white rounded-lg shadow">
          <p class="text-gray-500 text-sm">No people found.</p>
          <router-link to="/create" class="mt-2 inline-block text-green-600 hover:text-green-900 font-medium text-sm">Create one?</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const people = ref([])
const API_URL = 'http://localhost:8001/api'

onMounted(async () => {
  try {
    const response = await axios.get(`${API_URL}/people/`)
    people.value = response.data
  } catch (error) {
    console.error('Error fetching people:', error)
  }
})

const parseCustomData = (jsonString) => {
    try {
        const obj = JSON.parse(jsonString)
        return Object.entries(obj).map(([key, value]) => ({ key, value }))
    } catch(e) {
        return []
    }
}
</script>
