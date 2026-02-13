<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="md:flex md:items-center md:justify-between">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          Dashboard & Analytics
        </h2>
        <p class="mt-1 text-sm text-gray-500">
          Visualização de dados dinâmicos agregados
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
    </div>

    <!-- Stats Overview -->
    <div v-else>
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 mb-8">
        <!-- Total People Card -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Total de Pessoas</dt>
                  <dd class="text-3xl font-semibold text-gray-900">{{ stats.total_people }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Fields Card -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Campos Dinâmicos</dt>
                  <dd class="text-3xl font-semibold text-gray-900">{{ stats.field_stats?.length || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Response Rate Card -->
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Taxa de Resposta Média</dt>
                  <dd class="text-3xl font-semibold text-gray-900">{{ averageResponseRate }}%</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Chart for each field -->
        <div 
          v-for="field in stats.field_stats" 
          :key="field.field_key"
          class="bg-white shadow rounded-lg p-6"
        >
          <h3 class="text-lg font-medium text-gray-900 mb-4">{{ field.field_label }}</h3>
          
          <!-- Pie Chart for select/radio fields -->
          <div v-if="hasValueCounts(field)" class="h-64">
            <Pie :data="getPieChartData(field)" :options="chartOptions" />
          </div>

          <!-- Bar Chart for multiselect fields -->
          <div v-else-if="field.field_type === 'multiselect' && hasValueCounts(field)" class="h-64">
            <Bar :data="getBarChartData(field)" :options="chartOptions" />
          </div>

          <!-- Numeric Stats -->
          <div v-else-if="field.numeric_stats" class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Mínimo:</span>
              <span class="text-lg font-semibold text-gray-900">{{ field.numeric_stats.min.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Máximo:</span>
              <span class="text-lg font-semibold text-gray-900">{{ field.numeric_stats.max.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Média:</span>
              <span class="text-lg font-semibold text-green-600">{{ field.numeric_stats.avg.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">Total de Respostas:</span>
              <span class="text-lg font-semibold text-gray-900">{{ field.numeric_stats.count }}</span>
            </div>
          </div>

          <!-- Text fields (no visualization) -->
          <div v-else class="text-center py-8 text-gray-500">
            <p class="text-sm">{{ field.total_responses }} respostas</p>
            <p class="text-xs mt-1">Tipo: {{ field.field_type }}</p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!stats.field_stats || stats.field_stats.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhum dado disponível</h3>
        <p class="mt-1 text-sm text-gray-500">Comece criando campos e cadastrando pessoas.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Pie, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const API_URL = 'http://localhost:8000/api'

const loading = ref(true)
const stats = ref({
  total_people: 0,
  field_stats: []
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
}

const averageResponseRate = computed(() => {
  if (!stats.value.field_stats || stats.value.field_stats.length === 0 || stats.value.total_people === 0) {
    return 0
  }
  
  const totalResponses = stats.value.field_stats.reduce((sum, field) => sum + field.total_responses, 0)
  const possibleResponses = stats.value.field_stats.length * stats.value.total_people
  
  return possibleResponses > 0 ? Math.round((totalResponses / possibleResponses) * 100) : 0
})

const hasValueCounts = (field) => {
  return field.value_counts && Object.keys(field.value_counts).length > 0
}

const getPieChartData = (field) => {
  const labels = Object.keys(field.value_counts)
  const data = Object.values(field.value_counts)
  
  return {
    labels,
    datasets: [{
      data,
      backgroundColor: [
        'rgba(34, 197, 94, 0.8)',   // green
        'rgba(59, 130, 246, 0.8)',  // blue
        'rgba(251, 146, 60, 0.8)',  // orange
        'rgba(168, 85, 247, 0.8)',  // purple
        'rgba(236, 72, 153, 0.8)',  // pink
        'rgba(14, 165, 233, 0.8)',  // sky
        'rgba(234, 179, 8, 0.8)',   // yellow
        'rgba(239, 68, 68, 0.8)',   // red
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }]
  }
}

const getBarChartData = (field) => {
  const labels = Object.keys(field.value_counts)
  const data = Object.values(field.value_counts)
  
  return {
    labels,
    datasets: [{
      label: 'Quantidade',
      data,
      backgroundColor: 'rgba(34, 197, 94, 0.8)',
      borderColor: 'rgba(34, 197, 94, 1)',
      borderWidth: 1
    }]
  }
}

const fetchStats = async () => {
  try {
    loading.value = true
    const response = await axios.get(`${API_URL}/analytics/field-stats`)
    stats.value = response.data
  } catch (error) {
    console.error('Error fetching stats:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>
