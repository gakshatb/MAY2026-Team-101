<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    <!-- Reusable Sidebar -->
    <Sidebar userRole="Citizen" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
      <!-- Reusable Dashboard Navbar -->
      <DashboardNavbar 
        userRole="Citizen" 
        pageTitle="Complaint Details"
        breadcrumb="My Complaints > Details"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
      />

      <!-- Main Scrollable Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto space-y-6">
          
          <!-- Header Actions -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Complaint #{{ complaint.id }}</h1>
              <p class="text-sm text-slate-500 mt-1">{{ complaint.title }}</p>
            </div>
            <div class="flex items-center gap-3">
              <button class="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-2">
                <Printer class="w-4 h-4" /> Print
              </button>
              <button class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm font-medium hover:bg-[#1E40AF] transition-colors flex items-center gap-2">
                <Download class="w-4 h-4" /> Download PDF
              </button>
            </div>
          </div>

          <!-- Main Layout Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Left Column (Main Content - 2/3 width) -->
            <div class="lg:col-span-2 space-y-6">
              
              <!-- Complaint Info Card -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h2 class="text-lg font-bold text-slate-900 mb-4">Description</h2>
                <p class="text-slate-600 leading-relaxed">{{ complaint.description }}</p>
              </div>

              <!-- Location Card -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h2 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <MapPin class="w-5 h-5 text-slate-400" /> Location Details
                </h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-6">
                  <div v-for="(val, label) in locationDetails" :key="label">
                    <p class="text-xs text-slate-500 uppercase font-medium">{{ label }}</p>
                    <p class="text-sm font-bold text-slate-900">{{ val }}</p>
                  </div>
                </div>
                <!-- Maps Placeholder -->
                <div class="w-full h-48 bg-slate-100 rounded-lg border border-slate-200 flex items-center justify-center text-slate-400">
                  <span class="flex items-center gap-2"><MapPin class="w-4 h-4" /> Google Maps Placeholder</span>
                </div>
              </div>

              <!-- Evidence Card -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h2 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Camera class="w-5 h-5 text-slate-400" /> Uploaded Evidence
                </h2>
                <div class="grid grid-cols-2 gap-4">
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg h-32 border border-slate-200">
                    <img src="https://images.unsplash.com/photo-1621451537084-482c73073a0f?q=80&w=400&auto=format" alt="Evidence" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
                    <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                      <Maximize2 class="w-6 h-6 text-white" />
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <!-- Right Column (Status & Assigned Info - 1/3 width) -->
            <div class="lg:col-span-1 space-y-6">
              
              <!-- Status Card -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 text-center">
                <p class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">Current Status</p>
                <span class="inline-block px-4 py-2 rounded-full text-sm font-bold bg-blue-50 text-[#2563EB]">IN PROGRESS</span>
              </div>

              <!-- Assigned Personnel Card -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="text-sm font-bold text-slate-900 mb-4">Assigned Personnel</h3>
                <div class="space-y-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center">
                      <User class="w-5 h-5 text-slate-500" />
                    </div>
                    <div>
                      <p class="text-sm font-bold text-slate-900">Mr. Rajesh Kumar</p>
                      <p class="text-xs text-slate-500">Civic Officer</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center">
                      <HardHat class="w-5 h-5 text-slate-500" />
                    </div>
                    <div>
                      <p class="text-sm font-bold text-slate-900">Amit Singh</p>
                      <p class="text-xs text-slate-500">Field Worker</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Timeline Preview -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="text-sm font-bold text-slate-900 mb-6">Timeline</h3>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="step in timeline" :key="step.title" class="relative">
                    <div :class="['absolute -left-[21px] w-2.5 h-2.5 rounded-full mt-1', step.completed ? 'bg-[#22C55E]' : 'bg-slate-300']"></div>
                    <p :class="['text-sm font-medium', step.completed ? 'text-slate-900' : 'text-slate-400']">{{ step.title }}</p>
                    <p class="text-[10px] text-slate-400">{{ step.date }}</p>
                  </div>
                </div>
                <button class="w-full mt-6 text-sm font-medium text-[#2563EB] hover:underline">View Complete Timeline</button>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Printer, Download, MapPin, Camera, Maximize2, 
  User, HardHat, ShieldCheck 
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)

const complaint = ref({
  id: 'CMP-2026-00125',
  title: 'Large Pothole causing traffic hazards',
  category: 'Road Damage',
  status: 'In Progress',
  priority: 'High',
  submittedAt: 'July 05, 2026',
  description: 'There is a large pothole measuring approximately 2 feet in diameter located right at the entrance of the society gate. It is causing severe traffic congestion and poses a safety risk to two-wheeler riders, especially during night hours as the streetlight nearby is also not functioning.'
})

const locationDetails = {
  City: 'Bhiwandi',
  Ward: 'Ward 12',
  Area: 'Kalyan Naka',
  Street: 'Agra Road',
  Landmark: 'Near City Hospital'
}

const timeline = [
  { title: 'Complaint Submitted', date: 'July 05, 2026', completed: true },
  { title: 'Verified', date: 'July 05, 2026', completed: true },
  { title: 'Assigned', date: 'July 06, 2026', completed: true },
  { title: 'In Progress', date: 'July 06, 2026', completed: true },
  { title: 'Resolved', date: 'Pending', completed: false }
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>