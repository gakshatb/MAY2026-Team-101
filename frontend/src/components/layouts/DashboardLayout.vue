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
import { ref } from 'vue'
import Sidebar from '../components/dashboard/Sidebar.vue'
import DashboardNavbar from '../components/dashboard/DashboardNavbar.vue'

// Local state for layout mechanics
const isSidebarOpen = ref(false)

// Simulated Authentication / Global State
const currentUserRole = ref('Citizen') // Change to 'Civic Officer' or 'Field Worker' to see dynamic menus
const currentPageTitle = ref('My Profile')
const currentBreadcrumb = ref('Profile Settings')
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}
</style>