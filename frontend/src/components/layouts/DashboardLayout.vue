<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans overflow-hidden text-slate-800">
    
    <!-- Sidebar -->
    <Sidebar 
      :isOpen="isSidebarOpen" 
      :userRole="currentUserRole" 
      @close-sidebar="isSidebarOpen = false" 
    />

    <!-- Main Content Wrapper -->
    <div class="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
      
      <!-- Top Navbar -->
      <DashboardNavbar 
        :userRole="currentUserRole" 
        :user="currentUser"
        :pageTitle="currentPageTitle"
        :breadcrumb="currentBreadcrumb"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen" 
      />

      <!-- Page Content (Router View) -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <!-- 
          The router-view is where pages like Profile.vue or Dashboard.vue render 
          Remove the div below and replace with <router-view /> in production.
        -->
        <router-view />
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '../dashboard/Sidebar.vue'
import DashboardNavbar from '../dashboard/DashboardNavbar.vue'

const route = useRoute()

const isSidebarOpen = ref(false)

const currentUser = ref(readUser())

function readUser() {
  const stored = localStorage.getItem('user')
  if (!stored) return null
  try {
    return JSON.parse(stored)
  } catch (err) {
    return null
  }
}

function syncUser() {
  currentUser.value = readUser()
}

onMounted(() => window.addEventListener('user-updated', syncUser))
onUnmounted(() => window.removeEventListener('user-updated', syncUser))

const currentUserRole = computed(() => currentUser.value?.role || 'Citizen')

const currentPageTitle = computed(() => route.meta?.pageTitle || 'Dashboard')
const currentBreadcrumb = computed(() => route.meta?.breadcrumb || '')
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>