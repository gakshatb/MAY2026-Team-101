<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Sidebar Placeholder -->
    <Sidebar userRole="Citizen" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      
      <!-- Navbar Placeholder -->
      <DashboardNavbar userRole="Citizen" pageTitle="Dashboard" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Welcome Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Good Morning, Shivam Gupta</h1>
              <p class="text-slate-500 mt-1">Track your complaints and stay updated with the latest progress.</p>
            </div>
            <div class="flex gap-2">
              <div class="bg-white px-4 py-2.5 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <Calendar class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">{{ currentDate }}</span>
              </div>
            </div>
          </div>

          <!-- Pending Feedback Alert -->
          <div v-if="hasPendingFeedback" class="bg-gradient-to-r from-amber-50 to-white border border-amber-200 rounded-[14px] p-5 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative overflow-hidden">
            <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-amber-500"></div>
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center shrink-0">
                <Star class="w-5 h-5 fill-amber-600" />
              </div>
              <div>
                <h3 class="font-bold text-slate-900">Action Required: Pending Feedback</h3>
                <p class="text-sm text-slate-600 mt-0.5">You have one completed complaint awaiting your feedback. Help us improve our services.</p>
              </div>
            </div>
            <router-link to="/citizen/feedback/CMP-8799" class="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 text-white text-sm font-bold rounded-lg shadow-sm transition-colors whitespace-nowrap text-center">
              Give Feedback
            </router-link>
          </div>

          <!-- Statistics Cards -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div v-for="stat in summaryStats" :key="stat.title" class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 group">
              <div class="flex justify-between items-start mb-3">
                <div :class="`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor}`">
                  <component :is="stat.icon" class="w-5 h-5" />
                </div>
                <span v-if="stat.trend" :class="`flex items-center gap-1 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${stat.trend === 'up' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`">
                  <TrendingUp v-if="stat.trend === 'up'" class="w-3 h-3" />
                  <TrendingDown v-else class="w-3 h-3" />
                </span>
              </div>
              <div>
                <p class="text-3xl font-extrabold text-slate-900">{{ stat.value }}</p>
                <p class="text-xs font-semibold text-slate-500 mt-1 uppercase tracking-wide">{{ stat.title }}</p>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <router-link v-for="action in quickActions" :key="action.title" :to="action.route" class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/40 hover:shadow-md transition-all duration-300 group flex flex-col items-center text-center gap-3 relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-b from-transparent to-slate-50/50 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div class="w-12 h-12 rounded-2xl bg-slate-50 group-hover:bg-[#2563EB]/10 text-slate-500 group-hover:text-[#2563EB] flex items-center justify-center transition-colors relative z-10">
                <component :is="action.icon" class="w-6 h-6" />
              </div>
              <div class="relative z-10">
                <h3 class="font-bold text-slate-900 text-sm mb-1 group-hover:text-[#2563EB] transition-colors">{{ action.title }}</h3>
                <p class="text-xs text-slate-500 line-clamp-1">{{ action.desc }}</p>
              </div>
            </router-link>
          </div>

          <!-- Main Layout Grid -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <!-- Left Column: Primary Content (8 cols) -->
            <div class="xl:col-span-8 flex flex-col gap-6">
              
              <!-- Recent Complaints -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden flex flex-col">
                <div class="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><ClipboardList class="w-5 h-5 text-[#2563EB]" /> Recent Complaints</h3>
                  <router-link to="/citizen/complaints" class="text-sm font-medium text-[#2563EB] hover:underline flex items-center gap-1">View All <ChevronRight class="w-4 h-4"/></router-link>
                </div>
                
                <div class="divide-y divide-slate-100">
                  <div v-for="comp in recentComplaints" :key="comp.id" class="p-5 hover:bg-slate-50/80 transition-colors group">
                    <div class="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-4">
                      <div class="flex-1">
                        <div class="flex items-center gap-2 mb-2">
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-white border border-slate-200 text-slate-600 font-mono">{{ comp.id }}</span>
                          <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${statusBadge(comp.status)}`">{{ comp.status }}</span>
                        </div>
                        <h4 class="text-base font-bold text-slate-900 group-hover:text-[#2563EB] transition-colors line-clamp-1">{{ comp.title }}</h4>
                        <div class="flex items-center gap-4 text-xs text-slate-500 font-medium mt-2">
                          <span class="flex items-center gap-1.5"><FileText class="w-3.5 h-3.5"/> {{ comp.category }}</span>
                          <span class="flex items-center gap-1.5"><Calendar class="w-3.5 h-3.5"/> Submitted: {{ comp.submittedDate }}</span>
                        </div>
                      </div>
                      
                      <!-- Action Buttons -->
                      <div class="flex items-center gap-2 md:self-end">
                        <router-link :to="`/citizen/track/${comp.id}`" class="px-4 py-2 bg-slate-100 text-slate-700 hover:bg-slate-200 text-xs font-bold rounded-lg transition-colors flex items-center gap-2">
                          <Navigation class="w-3.5 h-3.5"/> Track
                        </router-link>
                        <router-link :to="`/citizen/details/${comp.id}`" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-bold rounded-lg transition-colors">
                          Details
                        </router-link>
                      </div>
                    </div>

                    <!-- Progress Bar -->
                    <div>
                      <div class="flex justify-between text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1.5">
                        <span>Progress</span>
                        <span>{{ comp.progress }}%</span>
                      </div>
                      <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div class="h-full bg-[#2563EB] rounded-full transition-all duration-500" :style="`width: ${comp.progress}%`" :class="{'bg-[#22C55E]': comp.progress === 100}"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Charts Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Activity Chart -->
                <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100">
                  <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Activity class="w-4 h-4 text-[#2563EB]" /> Monthly Activity</h3>
                  <div class="h-[220px] w-full relative">
                    <canvas ref="lineChartRef"></canvas>
                  </div>
                </div>
                <!-- Progress Chart -->
                <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100">
                  <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><LayoutDashboard class="w-4 h-4 text-purple-500" /> Overview</h3>
                  <div class="h-[220px] w-full relative flex items-center justify-center">
                    <canvas ref="doughnutChartRef"></canvas>
                  </div>
                </div>
              </div>

              <!-- Categories Summary -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><MapPin class="w-5 h-5 text-amber-500" /> Issues by Category</h3>
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
                  <div v-for="cat in categories" :key="cat.name" class="p-3 bg-slate-50 border border-slate-100 rounded-xl text-center hover:border-slate-200 transition-colors">
                    <component :is="cat.icon" class="w-5 h-5 mx-auto mb-2 text-slate-400" />
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide truncate mb-1">{{ cat.name }}</p>
                    <p class="text-lg font-bold text-slate-900">{{ cat.count }}</p>
                  </div>
                </div>
              </div>

            </div>

            <!-- Right Column: Secondary Content (4 cols) -->
            <div class="xl:col-span-4 space-y-6">
              
              <!-- Recent Notifications -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><Bell class="w-5 h-5 text-[#2563EB]" /> Notifications</h3>
                </div>
                <div class="divide-y divide-slate-50">
                  <div v-for="(notif, idx) in notifications" :key="idx" class="p-4 flex gap-3 hover:bg-slate-50 transition-colors">
                    <div :class="`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5 ${notif.bg} ${notif.color}`">
                      <component :is="notif.icon" class="w-4 h-4" />
                    </div>
                    <div>
                      <p class="text-sm text-slate-800 leading-snug">{{ notif.text }}</p>
                      <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wide mt-1.5">{{ notif.time }}</p>
                    </div>
                  </div>
                </div>
                <div class="p-3 border-t border-slate-100 bg-slate-50 text-center">
                  <router-link to="/citizen/notifications" class="text-xs font-bold text-[#2563EB] hover:underline">View All Notifications</router-link>
                </div>
              </div>

              <!-- Activity Timeline -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Clock class="w-5 h-5 text-purple-500" /> Recent Activity</h3>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="(event, idx) in timeline" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 rounded-full ring-4 ring-white border-2" :class="idx === 0 ? 'bg-[#2563EB] border-[#2563EB]' : 'bg-slate-300 border-slate-300'"></div>
                    <p class="text-sm font-bold text-slate-900">{{ event.action }}</p>
                    <p class="text-[10px] font-medium text-slate-500 mt-0.5">{{ event.date }} • {{ event.time }}</p>
                    <p class="text-xs text-slate-600 font-mono mt-1">{{ event.id }}</p>
                  </div>
                </div>
              </div>

              <!-- Tips & Awareness -->
              <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-[14px] shadow-sm border border-green-100 p-5">
                <div class="flex items-center gap-2 mb-3">
                  <Lightbulb class="w-5 h-5 text-green-600" />
                  <h3 class="font-bold text-green-800">Civic Awareness</h3>
                </div>
                <div class="space-y-3">
                  <p class="text-sm text-green-700 flex items-start gap-2"><CheckCircle class="w-4 h-4 text-green-500 shrink-0 mt-0.5"/> Keep public areas clean and use designated dustbins.</p>
                  <p class="text-sm text-green-700 flex items-start gap-2"><CheckCircle class="w-4 h-4 text-green-500 shrink-0 mt-0.5"/> Report civic issues early to prevent larger damages.</p>
                  <p class="text-sm text-green-700 flex items-start gap-2"><CheckCircle class="w-4 h-4 text-green-500 shrink-0 mt-0.5"/> Be a responsible citizen, help keep the city safe.</p>
                </div>
              </div>

              <!-- Emergency Contact -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 text-center">
                <ShieldCheck class="w-8 h-8 text-red-500 mx-auto mb-2" />
                <h3 class="font-bold text-slate-900 mb-1">Emergency Contacts</h3>
                <p class="text-xs text-slate-500 mb-4">For immediate assistance</p>
                
                <div class="space-y-2">
                  <div class="p-3 bg-red-50 text-red-700 rounded-lg border border-red-100">
                    <p class="text-[10px] font-bold uppercase tracking-wide opacity-70">Toll-Free Helpline</p>
                    <p class="text-lg font-extrabold tracking-wide">1800-123-4567</p>
                  </div>
                  <div class="p-3 bg-slate-50 text-slate-700 rounded-lg border border-slate-100">
                    <p class="text-[10px] font-bold uppercase tracking-wide opacity-70">Email Support</p>
                    <p class="text-sm font-bold">support@civicdesk.in</p>
                  </div>
                </div>
                <p class="text-[10px] font-medium text-slate-400 mt-3">Available Mon-Sat (09:00 AM - 06:00 PM)</p>
              </div>

            </div>
          </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  ClipboardList, Bell, CheckCircle, Clock, AlertTriangle, MapPin, 
  Activity, TrendingUp, TrendingDown, Star, User, FileText, ShieldCheck, 
  Calendar, Trash2, Construction, Droplets, Lightbulb, ChevronRight, 
  PlusCircle, Navigation, LayoutDashboard
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const currentDate = 'Thursday, July 09, 2026'
const hasPendingFeedback = ref(true)

// --- Dummy Data ---
const summaryStats = [
  { title: 'Total Complaints', value: '12', icon: ClipboardList, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Pending', value: '2', icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'In Progress', value: '1', icon: Activity, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { title: 'Resolved', value: '8', icon: CheckCircle, trend: 'up', iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'Closed', value: '1', icon: FileText, iconBg: 'bg-slate-100', iconColor: 'text-slate-600' },
  { title: 'Unread Alerts', value: '3', icon: Bell, iconBg: 'bg-red-50', iconColor: 'text-red-500' }
]

const quickActions = [
  { title: 'New Complaint', desc: 'Report an issue', icon: PlusCircle, route: '/citizen/submit' },
  { title: 'My Complaints', desc: 'View history', icon: ClipboardList, route: '/citizen/complaints' },
  { title: 'Track Status', desc: 'Live updates', icon: Navigation, route: '/citizen/complaints' }, // Usually routes to list, then track
  { title: 'Notifications', desc: 'Recent alerts', icon: Bell, route: '/citizen/notifications' },
  { title: 'My Profile', desc: 'Manage account', icon: User, route: '/citizen/profile' }
]

const recentComplaints = [
  { id: 'CMP-8875', title: 'Deep Pothole on Main Road causing traffic', category: 'Road Damage', status: 'In Progress', submittedDate: 'Jul 05, 2026', progress: 65 },
  { id: 'CMP-8902', title: 'Streetlight not working near park', category: 'Electrical', status: 'Assigned', submittedDate: 'Jul 08, 2026', progress: 30 },
  { id: 'CMP-8799', title: 'Overflowing dustbin outside society', category: 'Garbage', status: 'Resolved', submittedDate: 'Jul 01, 2026', progress: 100 }
]

const notifications = [
  { text: 'Worker assigned to CMP-8902', time: '2 hours ago', icon: User, bg: 'bg-blue-100', color: 'text-blue-600' },
  { text: 'Complaint CMP-8799 marked as Resolved', time: '1 day ago', icon: CheckCircle, bg: 'bg-green-100', color: 'text-green-600' },
  { text: 'Officer requested more details for CMP-8875', time: '2 days ago', icon: AlertTriangle, bg: 'bg-amber-100', color: 'text-amber-600' }
]

const timeline = [
  { action: 'Work Started by Technician', date: 'Jul 09, 2026', time: '09:15 AM', id: 'CMP-8875' },
  { action: 'Worker Assigned', date: 'Jul 08, 2026', time: '04:30 PM', id: 'CMP-8902' },
  { action: 'Complaint Submitted', date: 'Jul 08, 2026', time: '10:00 AM', id: 'CMP-8902' },
  { action: 'Feedback Submitted', date: 'Jul 02, 2026', time: '11:20 AM', id: 'CMP-8750' }
]

const categories = [
  { name: 'Garbage', count: 4, icon: Trash2 },
  { name: 'Roads', count: 3, icon: Construction },
  { name: 'Electrical', count: 2, icon: Lightbulb },
  { name: 'Water', count: 2, icon: Droplets },
  { name: 'Drainage', count: 1, icon: AlertTriangle },
  { name: 'Property', count: 0, icon: ShieldCheck }
]

// --- Visual Helpers ---
const statusBadge = (status) => {
  const map = { 
    'Submitted': 'bg-slate-100 text-slate-700', 
    'Under Review': 'bg-slate-100 text-slate-700',
    'Assigned': 'bg-blue-100 text-blue-700 border border-blue-200', 
    'In Progress': 'bg-amber-100 text-amber-700 border border-amber-200', 
    'Resolved': 'bg-green-100 text-green-700 border border-green-200',
    'Closed': 'bg-slate-100 text-slate-600' 
  }
  return map[status] || 'bg-slate-100 text-slate-700'
}

// --- Charts Setup ---
const lineChartRef = ref(null)
const doughnutChartRef = ref(null)
let lineChart, doughnutChart

onMounted(() => {
  // 1. Monthly Activity Line Chart
  if (lineChartRef.value) {
    lineChart = new Chart(lineChartRef.value, {
      type: 'line',
      data: {
        labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Complaints',
          data: [1, 3, 2, 4, 2, 3],
          borderColor: '#2563EB',
          backgroundColor: 'rgba(37,99,235,0.1)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#2563EB'
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        plugins: { legend: { display: false } }, 
        scales: { 
          y: { beginAtZero: true, grid: { color: '#f1f5f9' }, ticks: { stepSize: 1 } }, 
          x: { grid: { display: false } } 
        } 
      }
    })
  }

  // 2. Progress Overview Doughnut Chart
  if (doughnutChartRef.value) {
    doughnutChart = new Chart(doughnutChartRef.value, {
      type: 'doughnut',
      data: {
        labels: ['Resolved', 'In Progress', 'Assigned', 'Pending'],
        datasets: [{
          data: [8, 1, 1, 2],
          backgroundColor: ['#22C55E', '#F59E0B', '#2563EB', '#94A3B8'],
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        cutout: '70%', 
        plugins: { 
          legend: { position: 'right', labels: { boxWidth: 10, font: { size: 11 } } } 
        } 
      }
    })
  }
})

onUnmounted(() => {
  if (lineChart) lineChart.destroy()
  if (doughnutChart) doughnutChart.destroy()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>