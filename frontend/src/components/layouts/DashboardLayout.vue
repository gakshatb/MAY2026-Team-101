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
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '../components/dashboard/Sidebar.vue'
import DashboardNavbar from '../components/dashboard/DashboardNavbar.vue'

const route = useRoute()

// Local state for layout mechanics
const isSidebarOpen = ref(false)

// The logged-in user, as stored by Login.vue after a successful /api/login
// call. This same object backs the DashboardNavbar profile display and the
// role shown there — Sidebar.vue separately derives role from the URL,
// which is fine as long as route guards keep users on their own section.
const currentUser = computed(() => {
  const stored = localStorage.getItem('user')
  return stored ? JSON.parse(stored) : null
})

const currentUserRole = computed(() => currentUser.value?.role || 'Citizen')

// Page title/breadcrumb come from each route's meta fields, e.g.:
//   { path: '/citizen/submit', meta: { title: 'Submit Complaint', breadcrumb: 'New Complaint' } }
// Falls back to sensible defaults if a route hasn't set meta yet.
const currentPageTitle = computed(() => route.meta?.title || 'Dashboard')
const currentBreadcrumb = computed(() => route.meta?.breadcrumb || '')
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}
</style>