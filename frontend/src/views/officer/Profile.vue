<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    <Sidebar userRole="Civic Officer" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      <DashboardNavbar userRole="Civic Officer" pageTitle="Officer Profile" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1400px] mx-auto space-y-6">
          
          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB]">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Profile</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Officer Profile</h1>
              <p class="text-slate-500 mt-1">Manage your professional details and monitor performance.</p>
            </div>
          </div>

          <!-- Overview Grid -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <!-- Left: Profile Info -->
            <div class="xl:col-span-4 space-y-6">
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex flex-col items-center text-center">
                <div class="relative mb-4">
                  <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop" class="w-24 h-24 rounded-full object-cover border-4 border-slate-50 shadow-sm" />
                  <div class="absolute bottom-1 right-1 w-5 h-5 bg-green-500 border-2 border-white rounded-full"></div>
                </div>
                <h2 class="text-xl font-bold text-slate-900">Chief Officer Rajesh Kumar</h2>
                <p class="text-sm text-slate-500 mb-4">ID: EMP-2026-9021 | Roads & Infrastructure</p>
                <div class="flex gap-2">
                  <button @click="activeModal = 'edit'" class="px-4 py-2 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors">Edit Profile</button>
                  <button @click="activeModal = 'password'" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-50 transition-colors">Password</button>
                </div>
              </div>

              <!-- Performance Stats -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><TrendingUp class="w-4 h-4 text-[#2563EB]" /> Performance Stats</h3>
                <div class="grid grid-cols-2 gap-3">
                  <div class="p-3 bg-slate-50 rounded-lg">
                    <p class="text-[10px] uppercase font-bold text-slate-500">Resolved</p>
                    <p class="text-lg font-bold text-slate-900">842</p>
                  </div>
                  <div class="p-3 bg-slate-50 rounded-lg">
                    <p class="text-[10px] uppercase font-bold text-slate-500">Rating</p>
                    <p class="text-lg font-bold text-slate-900">4.8 <span class="text-xs text-amber-500">★</span></p>
                  </div>
                </div>
              </div>

              <!-- Documents -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><FileText class="w-4 h-4 text-slate-400" /> Documents</h3>
                <div class="space-y-3">
                  <div v-for="doc in documents" :key="doc.name" class="flex items-center justify-between p-3 border border-slate-100 rounded-lg">
                    <span class="text-sm font-medium text-slate-700">{{ doc.name }}</span>
                    <button class="text-[#2563EB] hover:text-[#1E40AF]"><Download class="w-4 h-4" /></button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right: Detailed Analytics & Info -->
            <div class="xl:col-span-8 space-y-6">
              
              <!-- Personal/Professional Info -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 mb-6 flex items-center gap-2"><Briefcase class="w-4 h-4 text-slate-400" /> Professional Details</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div v-for="(val, label) in profInfo" :key="label">
                    <p class="text-xs font-medium text-slate-500 uppercase">{{ label }}</p>
                    <p class="text-sm font-bold text-slate-900 mt-1">{{ val }}</p>
                  </div>
                </div>
              </div>

              <!-- Resolution Trend Chart -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="font-bold text-slate-900 mb-6">Resolution Performance (Last 6 Months)</h3>
                <div class="h-[300px]">
                  <canvas ref="perfChartRef"></canvas>
                </div>
              </div>

              <!-- Activities & Work -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                  <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Activity class="w-4 h-4 text-slate-400" /> Recent Activities</h3>
                  <div class="space-y-6 relative pl-4 border-l border-slate-100">
                    <div v-for="act in activities" :key="act.id" class="relative">
                      <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#2563EB] rounded-full border-2 border-white"></div>
                      <p class="text-sm font-bold text-slate-900">{{ act.title }}</p>
                      <p class="text-xs text-slate-500">{{ act.date }} • {{ act.complaintId }}</p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                  <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><ShieldCheck class="w-4 h-4 text-green-500" /> Achievements</h3>
                  <div class="space-y-3">
                    <div v-for="ach in achievements" :key="ach.title" class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                      <div class="text-xl">{{ ach.icon }}</div>
                      <div>
                        <p class="text-sm font-bold text-slate-900">{{ ach.title }}</p>
                        <p class="text-xs text-slate-500">{{ ach.desc }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Modals (Teleported) -->
    <Teleport to="body">
      <!-- Edit Profile Modal -->
      <div v-if="activeModal === 'edit'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-lg shadow-2xl p-6">
          <h3 class="font-bold text-lg mb-4">Edit Profile</h3>
          <div class="space-y-4">
             <input type="text" placeholder="Full Name" class="w-full p-3 border rounded-lg text-sm" value="Rajesh Kumar" />
             <input type="email" placeholder="Email" class="w-full p-3 border rounded-lg text-sm" value="rajesh.k@civicdesk.in" />
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="activeModal = null" class="px-4 py-2 bg-slate-100 rounded-lg text-sm font-bold">Cancel</button>
            <button class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm font-bold">Save Changes</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  TrendingUp, TrendingDown, Download, FileText, Briefcase, 
  Activity, Star, ShieldCheck, User, Settings, Printer, 
  MapPin, Clock, Calendar, AlertTriangle, Users
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const activeModal = ref(null)
const perfChartRef = ref(null)
let chartInstance = null

const documents = [
  { name: 'Employee ID Card' },
  { name: 'Appointment Letter' },
  { name: 'Training Certificate' }
]

const profInfo = {
  'Employee ID': 'EMP-2026-9021',
  'Designation': 'Chief Civic Officer',
  'Department': 'Infrastructure',
  'Assigned Ward': 'Ward 14, 15',
  'Office Location': 'Municipal HQ, Block A',
  'Experience': '12 Years'
}

const achievements = [
  { title: 'Top Performer', desc: 'Q2 2026 Award', icon: '🏆' },
  { title: 'Fast Responder', desc: 'Avg 4h Resolution', icon: '⚡' },
  { title: 'Reliable Officer', desc: '100% Attendance', icon: '✅' }
]

const activities = [
  { id: 1, title: 'Complaint Closed (CMP-8902)', date: 'Jul 09, 2026', complaintId: 'CMP-8902' },
  { id: 2, title: 'Field Worker Assigned', date: 'Jul 08, 2026', complaintId: 'CMP-8945' },
  { id: 3, title: 'Verified Complaint', date: 'Jul 07, 2026', complaintId: 'CMP-8910' }
]

onMounted(() => {
  if (perfChartRef.value) {
    chartInstance = new Chart(perfChartRef.value, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Resolution Rate (%)',
          data: [78, 82, 85, 80, 92, 95],
          borderColor: '#2563EB',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
          fill: true,
          tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    })
  }
})

onUnmounted(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
.animate-fade-in { animation: fadeIn 0.2s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>