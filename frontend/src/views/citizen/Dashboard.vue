<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    <Sidebar :userRole="userRole" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      <DashboardNavbar :userRole="userRole" pageTitle="Dashboard" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto space-y-8">
          
          <!-- Greeting Header -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h1 class="text-2xl font-bold text-slate-900">Good Morning, Shivam</h1>
              <p class="text-slate-500 mt-1">Welcome back to CivicDesk. Here's your daily overview.</p>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-sm font-medium text-slate-600 bg-white px-4 py-2 rounded-lg border border-slate-200">{{ currentDate }}</span>
              <span class="px-4 py-2 bg-[#2563EB]/10 text-[#2563EB] text-sm font-bold rounded-lg">{{ userRole }}</span>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="flex flex-wrap gap-3">
            <button 
              v-for="action in quickActions" 
              :key="action.name" 
              @click="router.push(action.route)"
              class="px-5 py-2.5 bg-white border border-slate-200 rounded-lg text-sm font-medium hover:border-[#2563EB] hover:text-[#2563EB] transition-all flex items-center gap-2"
            >
              <component :is="action.icon" class="w-4 h-4" /> {{ action.name }}
            </button>
          </div>

          <!-- Statistics Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <StatisticsCard 
              v-for="stat in dashboardStats" :key="stat.title"
              v-bind="stat"
            />
          </div>

          <!-- Main Layout Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <!-- Recent Activity Table -->
            <div class="lg:col-span-8 bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
              <div class="flex justify-between items-center mb-6">
                <h3 class="font-bold text-slate-900">Recent Activity</h3>
                <button @click="router.push('/citizen/complaints')" class="text-sm text-[#2563EB] font-medium hover:underline">View All</button>
              </div>
              <table class="w-full text-sm">
                <thead>
                  <tr class="text-slate-500 text-left border-b border-slate-100">
                    <th class="pb-3">Complaint ID</th>
                    <th class="pb-3">Title</th>
                    <th class="pb-3">Status</th>
                    <th class="pb-3">Action</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="item in recentItems" :key="item.id" class="hover:bg-slate-50 transition-colors">
                    <td class="py-4 font-mono font-medium">{{ item.id }}</td>
                    <td class="py-4">{{ item.title }}</td>
                    <td class="py-4"><span :class="['px-2 py-1 rounded text-xs font-bold', statusColor(item.status)]">{{ item.status }}</span></td>
                    <td class="py-4">
                      <button @click="router.push(`/citizen/details/${item.id}`)" class="text-[#2563EB] font-medium hover:underline">View</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Charts & Quick Help -->
            <div class="lg:col-span-4 space-y-6">
              <!-- Chart Placeholder -->
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
                <h3 class="font-bold text-slate-900 mb-6">Complaint Status</h3>
                <div class="h-48 flex items-center justify-center border-2 border-dashed border-slate-200 rounded-lg text-slate-400">
                  [ Pie Chart Visualization ]
                </div>
              </div>
              
              <!-- Quick Help -->
              <div class="bg-[#0F172A] p-6 rounded-[14px] text-white">
                <h3 class="font-bold mb-2">Need Help?</h3>
                <p class="text-sm text-slate-400 mb-4">View our user guide or contact support for assistance.</p>
                <div class="space-y-2">
                  <router-link to="/faq" class="block text-sm hover:text-[#2563EB] transition-colors">→ FAQs</router-link>
                  <router-link to="/contact" class="block text-sm hover:text-[#2563EB] transition-colors">→ Contact Support</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import StatisticsCard from '@/components/dashboard/StatisticsCard.vue'
import { 
  ClipboardList, CheckCircle, Clock, AlertTriangle, 
  MapPin, Plus, ArrowUpRight, Search, FileText, Settings
} from 'lucide-vue-next'

const router = useRouter()
const userRole = ref('Citizen') // Toggle 'Citizen', 'Officer', or 'Worker'
const isSidebarOpen = ref(false)
const currentDate = new Date().toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' })

// Role-based logic updated with routes
const quickActions = computed(() => {
  if (userRole.value === 'Citizen') {
    return [
      { name: 'Submit Complaint', icon: Plus, route: '/citizen/submit' }, 
      { name: 'My Complaints', icon: ClipboardList, route: '/citizen/complaints' }
    ]
  }
  return [
    { name: 'Manage Complaints', icon: ClipboardList, route: '/dashboard' }, 
    { name: 'Analytics', icon: Search, route: '/dashboard' }
  ]
})

const dashboardStats = computed(() => {
  if (userRole.value === 'Citizen') return [
    { title: 'Total', count: 12, trend: '+2', icon: ClipboardList, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
    { title: 'Pending', count: 3, trend: '0', icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
    { title: 'Resolved', count: 8, trend: '+1', icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
    { title: 'In Progress', count: 1, trend: '0', icon: AlertTriangle, iconBg: 'bg-red-50', iconColor: 'text-red-500' }
  ]
  return [] // Add Officer/Worker stats similarly
})

const recentItems = ref([
  { id: 'CMP-001', title: 'Streetlight Repair', status: 'Resolved' },
  { id: 'CMP-002', title: 'Pothole Filling', status: 'Pending' },
  { id: 'CMP-003', title: 'Garbage Collection', status: 'In Progress' }
])

const statusColor = (status) => {
  if (status === 'Resolved') return 'bg-green-100 text-green-700'
  if (status === 'Pending') return 'bg-amber-100 text-amber-700'
  return 'bg-blue-100 text-blue-700'
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>