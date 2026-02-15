<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <nav class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <div class="h-8 w-8 bg-green-500 rounded-lg flex items-center justify-center mr-2">
                <span class="text-white font-bold">DF</span>
              </div>
              <h1 class="text-xl font-semibold text-gray-900">Dynamic Forms</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link 
                to="/" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-green-500 text-gray-900"
              >
                People List
              </router-link>
              <router-link 
                to="/create" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-green-500 text-gray-900"
              >
                New Person
              </router-link>
              <router-link 
                to="/admin" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-green-500 text-gray-900"
              >
                Admin Fields
              </router-link>
              <router-link 
                to="/builder" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-green-500 text-gray-900"
              >
                Form Builder
              </router-link>
              <router-link 
                to="/dashboard" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200"
                active-class="border-green-500 text-gray-900"
              >
                Dashboard
              </router-link>
            </div>
          </div>
          <!-- Mobile menu button -->
          <div class="-mr-2 flex items-center sm:hidden">
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen"
              type="button" 
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-green-500" 
              aria-controls="mobile-menu" 
              :aria-expanded="isMobileMenuOpen"
              aria-label="Main menu"
            >
              <span class="sr-only">Open main menu</span>
              <!-- Icon when menu is closed. -->
              <svg v-if="!isMobileMenuOpen" class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <!-- Icon when menu is open. -->
              <svg v-else class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile menu, show/hide based on menu state. -->
      <div v-show="isMobileMenuOpen" class="sm:hidden" id="mobile-menu">
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            to="/" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-green-50 border-green-500 text-green-700"
            exact-active-class="bg-green-50 border-green-500 text-green-700"
            :class="[$route.path === '/' ? '' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
            @click="isMobileMenuOpen = false"
          >
            People List
          </router-link>
          <router-link 
            to="/create" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-green-50 border-green-500 text-green-700"
            :class="[$route.path === '/create' ? '' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
             @click="isMobileMenuOpen = false"
          >
            New Person
          </router-link>
          <router-link 
            to="/admin" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-green-50 border-green-500 text-green-700"
            :class="[$route.path === '/admin' ? '' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
             @click="isMobileMenuOpen = false"
          >
            Admin Fields
          </router-link>
          <router-link 
            to="/builder" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-green-50 border-green-500 text-green-700"
            :class="[$route.path === '/builder' ? '' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
             @click="isMobileMenuOpen = false"
          >
            Form Builder
          </router-link>
          <router-link 
            to="/dashboard" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            active-class="bg-green-50 border-green-500 text-green-700"
            :class="[$route.path === '/dashboard' ? '' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
             @click="isMobileMenuOpen = false"
          >
            Dashboard
          </router-link>
        </div>
      </div>
    </nav>

    <main class="py-10">
      <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const isMobileMenuOpen = ref(false)
const route = useRoute()
</script>
