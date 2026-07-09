<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    <!-- Reusable Sidebar -->
    <Sidebar :userRole="userRole" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
      <!-- Reusable Dashboard Navbar -->
      <DashboardNavbar 
        :userRole="userRole" 
        pageTitle="Notifications"
        breadcrumb="Dashboard > Notifications"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
      />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto space-y-8">
          
          <!-- Summary Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div v-for="card in summaryCards" :key="card.title" class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4 transition-transform hover:shadow-md">
              <div :class="['p-3 rounded-xl', card.iconBg]">
                <component :is="card.icon" :class="['w-6 h-6', card.iconColor]" />
              </div>
              <div>
                <p class="text-sm font-medium text-slate-500">{{ card.title }}</p>
                <p class="text-2xl font-bold text-slate-900">{{ card.count }}</p>
              </div>
            </div>
          </div>

          <!-- Filter & Action Bar -->
          <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 items-center justify-between">
            <div class="flex flex-wrap gap-2 w-full lg:w-auto">
              <button 
                v-for="filter in filters" :key="filter"
                @click="activeFilter = filter"
                :class="['px-4 py-2 text-sm font-medium rounded-lg transition-colors', activeFilter === filter ? 'bg-[#2563EB] text-white' : 'text-slate-600 hover:bg-slate-50']"
              >
                {{ filter }}
              </button>
            </div>
            <div class="flex gap-2 w-full lg:w-auto">
              <button class="flex-1 lg:flex-none flex items-center justify-center gap-2 px-4 py-2.5 bg-slate-50 hover:bg-slate-100 text-slate-700 text-sm font-medium rounded-lg transition-colors">
                <Check class="w-4 h-4" /> Mark All Read
              </button>
            </div>
          </div>

          <!-- Notification List -->
          <div v-if="filteredNotifications.length > 0" class="space-y-3">
            <div 
              v-for="note in filteredNotifications" :key="note.id"
              @click="openDrawer(note)"
              :class="['group bg-white p-5 rounded-[14px] border shadow-sm flex gap-4 cursor-pointer transition-all hover:shadow-md', note.isRead ? 'border-slate-100' : 'border-l-4 border-l-[#2563EB] border-slate-200 bg-blue-50/10']"
            >
              <div :class="['p-2 rounded-full h-10 w-10 flex items-center justify-center shrink-0', note.iconBg]">
                <component :is="note.icon" :class="['w-5 h-5', note.iconColor]" />
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-bold text-slate-900">{{ note.title }}</h4>
                    <p class="text-sm text-slate-600 mt-1">{{ note.message }}</p>
                  </div>
                  <span class="text-xs text-slate-400 font-medium whitespace-nowrap ml-4">{{ note.time }}</span>
                </div>
                <div class="flex items-center justify-between mt-3">
                  <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2 py-1 rounded">CMP-2026-{{ note.complaintId }}</span>
                  <button class="text-sm font-medium text-[#2563EB] hover:underline">View Complaint</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-20 bg-white rounded-[14px] border border-slate-100">
            <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bell class="w-8 h-8 text-slate-300" />
            </div>
            <h3 class="text-lg font-bold text-slate-900">No Notifications Yet</h3>
            <p class="text-slate-500 mt-2">You will receive updates about your complaints here.</p>
          </div>
        </div>
      </main>
    </div>

    <!-- Details Drawer (UI Only) -->
    <transition name="drawer">
      <div v-if="selectedNotification" class="fixed inset-0 z-50 flex justify-end">
        <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="selectedNotification = null"></div>
        <div class="bg-white w-full max-w-md shadow-2xl h-full p-8 overflow-y-auto">
          <button @click="selectedNotification = null" class="mb-8 p-2 hover:bg-slate-100 rounded-lg"><X /></button>
          <h2 class="text-2xl font-bold text-slate-900 mb-4">{{ selectedNotification.title }}</h2>
          <div class="bg-blue-50 p-4 rounded-xl mb-6">
            <p class="text-sm text-[#2563EB] font-medium">Complaint #CMP-2026-{{ selectedNotification.complaintId }}</p>
          </div>
          <p class="text-slate-600 leading-relaxed mb-8">{{ selectedNotification.message }}</p>
          <div class="flex gap-3">
            <button class="flex-1 px-4 py-3 bg-[#2563EB] text-white rounded-lg font-medium">View Complaint</button>
            <button @click="selectedNotification = null" class="px-4 py-3 border border-slate-200 rounded-lg font-medium">Close</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Bell, CheckCircle, AlertCircle, Clock, 
  MessageSquare, User, Shield, SearchX, X,
  Check, Mail, Zap
} from 'lucide-vue-next'

const userRole = ref('Citizen') // Simulate different roles
const isSidebarOpen = ref(false)
const activeFilter = ref('All')
const selectedNotification = ref(null)

const summaryCards = [
  { title: 'All', count: 12, icon: Bell, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Unread', count: 3, icon: Mail, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Read', count: 9, icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'Important', count: 2, icon: Shield, iconBg: 'bg-red-50', iconColor: 'text-red-500' },
]

const filters = ['All', 'Unread', 'Complaint Updates', 'System Messages']

const allNotifications = ref([
  { id: 1, title: 'Complaint Submitted', message: 'Your complaint CMP-2026-00125 has been successfully submitted.', complaintId: '00125', time: '2m ago', isRead: false, icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-green-500' },
  { id: 2, title: 'Complaint Verified', message: 'Your complaint has been verified by the Civic Officer.', complaintId: '00124', time: '1h ago', isRead: false, icon: Shield, iconBg: 'bg-blue-50', iconColor: 'text-blue-500' },
  { id: 3, title: 'Worker Assigned', message: 'A field worker has been assigned to your complaint.', complaintId: '00120', time: '3h ago', isRead: true, icon: User, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { id: 4, title: 'Maintenance Alert', message: 'Scheduled maintenance on Sunday 2 AM to 4 AM.', complaintId: 'SYS', time: '1d ago', isRead: true, icon: AlertCircle, iconBg: 'bg-red-50', iconColor: 'text-red-500' }
])

const filteredNotifications = computed(() => {
  if (activeFilter.value === 'Unread') return allNotifications.value.filter(n => !n.isRead)
  if (activeFilter.value === 'System Messages') return allNotifications.value.filter(n => n.complaintId === 'SYS')
  if (activeFilter.value === 'Complaint Updates') return allNotifications.value.filter(n => n.complaintId !== 'SYS')
  return allNotifications.value
})

const openDrawer = (note) => {
  selectedNotification.value = note
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.drawer-enter-active, .drawer-leave-active { transition: opacity 0.3s; }
.drawer-enter-from, .drawer-leave-to { opacity: 0; }
</style>