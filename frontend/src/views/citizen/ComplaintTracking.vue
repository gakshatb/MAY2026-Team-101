<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar userRole="Citizen" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
      <!-- Navbar -->
      <DashboardNavbar 
        userRole="Citizen" 
        pageTitle="Complaint Tracking"
        breadcrumb="My Complaints > Tracking"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
      />

      <!-- Main Scrollable Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        
        <!-- Complaint Not Found State -->
        <div v-if="!complaint" class="h-full flex items-center justify-center">
          <div class="text-center">
            <div class="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <SearchX class="w-10 h-10 text-slate-400" />
            </div>
            <h2 class="text-2xl font-bold text-slate-900 mb-2">Complaint Not Found</h2>
            <p class="text-slate-500 mb-6">The Complaint ID you are looking for does not exist.</p>
            <router-link to="/citizen/complaints" class="px-6 py-3 bg-[#2563EB] text-white rounded-lg font-medium hover:bg-[#1E40AF]">
              Return to My Complaints
            </router-link>
          </div>
        </div>

        <!-- Complaint Found State -->
        <div v-else class="max-w-7xl mx-auto space-y-8">
          
          <!-- Header -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h1 class="text-3xl font-bold text-slate-900">Complaint Tracking</h1>
              <div class="flex items-center gap-2 mt-1">
                <span class="text-sm text-slate-500">Complaint ID:</span>
                <span class="text-sm font-mono font-bold bg-slate-200 px-2 py-0.5 rounded">{{ complaint.id }}</span>
              </div>
            </div>
            <div class="flex gap-3">
              <button class="px-4 py-2 border border-slate-200 bg-white rounded-lg text-sm font-medium hover:bg-slate-50 flex items-center gap-2">
                <Download class="w-4 h-4" /> Download Report
              </button>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Left Column: Progress Tracker -->
            <div class="lg:col-span-2 space-y-6">
              
              <!-- Progress Tracker -->
              <div class="bg-white p-8 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="text-lg font-bold text-slate-900 mb-8">Progress Status</h3>
                <div class="space-y-0">
                  <div v-for="(step, index) in timelineSteps" :key="step.title" class="relative pl-8 pb-8 last:pb-0">
                    <!-- Line Connector -->
                    <div v-if="index !== timelineSteps.length - 1" class="absolute left-[15px] top-8 w-0.5 h-full bg-slate-100"></div>
                    
                    <!-- Icon -->
                    <div :class="[
                      'absolute left-0 w-8 h-8 rounded-full flex items-center justify-center border-2 z-10 transition-colors',
                      step.status === 'completed' ? 'bg-green-100 border-[#22C55E]' : 
                      step.status === 'active' ? 'bg-blue-100 border-[#2563EB]' : 'bg-white border-slate-200'
                    ]">
                      <Check v-if="step.status === 'completed'" class="w-4 h-4 text-[#22C55E]" />
                      <div v-else-if="step.status === 'active'" class="w-2.5 h-2.5 bg-[#2563EB] rounded-full animate-pulse"></div>
                      <div v-else class="w-2.5 h-2.5 bg-slate-200 rounded-full"></div>
                    </div>

                    <div class="pt-0.5">
                      <p :class="['font-bold', step.status === 'active' ? 'text-[#2563EB]' : 'text-slate-900']">{{ step.title }}</p>
                      <p class="text-xs text-slate-400 mt-1">{{ step.date || 'Pending' }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Activity Timeline Table -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="text-lg font-bold text-slate-900 mb-4">Activity Log</h3>
                <div class="overflow-x-auto">
                  <table class="w-full text-left text-sm">
                    <thead>
                      <tr class="text-slate-500 uppercase text-[10px] tracking-wider border-b border-slate-100">
                        <th class="pb-3 font-semibold">Date</th>
                        <th class="pb-3 font-semibold">Status</th>
                        <th class="pb-3 font-semibold">Officer</th>
                        <th class="pb-3 font-semibold">Remarks</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-50">
                      <tr v-for="act in activityLog" :key="act.id" class="text-slate-700">
                        <td class="py-4 font-medium">{{ act.date }}</td>
                        <td class="py-4">{{ act.status }}</td>
                        <td class="py-4">{{ act.officer }}</td>
                        <td class="py-4 text-slate-500">{{ act.remarks }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Right Column: Status & Map -->
            <div class="space-y-6">
              
              <!-- Status Card -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <div class="flex items-center justify-between mb-6">
                  <h3 class="font-bold text-slate-900">Current Overview</h3>
                  <span class="px-3 py-1 bg-blue-50 text-[#2563EB] text-xs font-bold rounded-full uppercase">IN PROGRESS</span>
                </div>
                <div class="space-y-4">
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-sm text-slate-500">Department</span>
                    <span class="text-sm font-semibold">Road Maintenance</span>
                  </div>
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-sm text-slate-500">Assigned To</span>
                    <span class="text-sm font-semibold">Amit Singh</span>
                  </div>
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-sm text-slate-500">Expected</span>
                    <span class="text-sm font-semibold text-[#22C55E]">25 Jul 2026</span>
                  </div>
                </div>
              </div>

              <!-- Map Placeholder -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="font-bold text-slate-900 mb-4">Location</h3>
                <div class="h-40 bg-slate-100 rounded-lg border border-slate-200 flex items-center justify-center text-slate-400">
                  <MapPin class="w-6 h-6 mr-2" /> Map View
                </div>
              </div>

              <!-- Summary -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="font-bold text-slate-900 mb-2">Pothole on Main Road</h3>
                <p class="text-sm text-slate-600 mb-4">Deep pothole causing risk to motorists.</p>
                <img src="https://images.unsplash.com/photo-1516905042453-2947f637f991?w=400" class="rounded-lg w-full h-32 object-cover" />
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
import Sidebar from '../../components/dashboard/Sidebar.vue'
import DashboardNavbar from '../../components/dashboard/DashboardNavbar.vue'
import { 
  Download, MapPin, SearchX, Check, 
  Printer 
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const complaint = ref({
  id: 'CMP-2026-00125',
  title: 'Large Pothole on Main Road',
  description: 'Reported deep pothole at sector 4 entrance.'
})

const timelineSteps = [
  { title: 'Complaint Submitted', status: 'completed', date: '21 Jul, 10:00 AM' },
  { title: 'Complaint Verified', status: 'completed', date: '22 Jul, 09:00 AM' },
  { title: 'Assigned to Dept', status: 'completed', date: '23 Jul, 11:00 AM' },
  { title: 'Assigned to Worker', status: 'completed', date: '23 Jul, 02:00 PM' },
  { title: 'Work Started', status: 'active', date: '24 Jul, 08:00 AM' },
  { title: 'Issue Resolved', status: 'pending', date: '' },
  { title: 'Complaint Closed', status: 'pending', date: '' },
]

const activityLog = [
  { id: 1, date: '24 Jul', status: 'Repair In Progress', officer: 'Amit Singh', remarks: 'Started filling the pothole' },
  { id: 2, date: '23 Jul', status: 'Assigned', officer: 'Mr. Rajesh', remarks: 'Worker assigned to site' },
  { id: 3, date: '22 Jul', status: 'Verified', officer: 'System', remarks: 'Site inspection confirmed' },
  { id: 4, date: '21 Jul', status: 'Submitted', officer: 'Citizen', remarks: 'Initial report' },
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>