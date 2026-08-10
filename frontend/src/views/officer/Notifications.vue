<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1600px] mx-auto space-y-6">
          
          <!-- Header & Breadcrumbs -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Notifications</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Notification Center</h1>
              <p class="text-slate-500 mt-1">Stay informed about complaint assignments and system updates.</p>
            </div>
          </div>

          <div v-if="loadError" class="bg-red-50 border border-red-100 text-red-600 text-sm rounded-[14px] p-4">
            {{ loadError }}
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-between">
              <div class="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 bg-blue-50 text-[#2563EB] mb-3"><Bell class="w-5 h-5" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ summary.all }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Total Notifications</p>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-between">
              <div class="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 bg-amber-50 text-amber-500 mb-3"><Clock class="w-5 h-5" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ summary.unread }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Unread</p>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-between">
              <div class="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 bg-green-50 text-[#22C55E] mb-3"><CheckCircle class="w-5 h-5" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ summary.read }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Read</p>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Column: Search & Filters -->
            <div class="lg:col-span-3 space-y-6">
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Search class="w-4 h-4 text-[#2563EB]" /> Search & Filter</h3>
                <div class="space-y-4">
                  <div class="relative">
                    <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Search title, message, ID..."
                      class="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]"
                    />
                  </div>
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Timeframe</label>
                    <select v-model="filters.date" class="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                      <option value="All">All Time</option>
                      <option value="Today">Today</option>
                      <option value="Week">This Week</option>
                      <option value="Month">This Month</option>
                    </select>
                  </div>
                </div>
                <div class="mt-5 pt-4 border-t border-slate-100 flex gap-2">
                  <button @click="resetFilters" class="flex-1 py-2 text-sm font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">Reset</button>
                </div>
              </div>

              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 hidden lg:block">
                <h3 class="font-bold text-slate-900 mb-4">Quick Links</h3>
                <div class="space-y-2">
                  <router-link to="/officer/complaints" class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <Clipboard class="w-4 h-4" /> Complaint Management
                  </router-link>
                  <router-link to="/officer/analytics" class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <Activity class="w-4 h-4" /> Open Analytics
                  </router-link>
                  <router-link to="/officer/workers" class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <Users class="w-4 h-4" /> Manage Workers
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Right Column: Notifications Feed -->
            <div class="lg:col-span-9 flex flex-col h-full bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
              
              <!-- Tabs -->
              <div class="border-b border-slate-100 bg-slate-50/50 flex overflow-x-auto no-scrollbar px-2">
                <button
                  v-for="tab in tabs" :key="tab.name"
                  @click="activeTab = tab.name"
                  class="px-4 py-4 text-sm font-bold whitespace-nowrap border-b-2 transition-colors flex items-center gap-2"
                  :class="activeTab === tab.name ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-slate-500 hover:text-slate-700'"
                >
                  {{ tab.name }}
                </button>
              </div>

              <!-- List Header -->
              <div class="px-5 py-3 border-b border-slate-100 flex items-center justify-between bg-white shrink-0">
                <span class="text-sm font-bold text-slate-600">{{ filteredNotifications.length }} notifications</span>
                <button @click="markAllRead" class="text-xs font-bold text-[#2563EB] hover:underline">Mark all as read</button>
              </div>

              <!-- Notification List -->
              <div class="flex-1 overflow-y-auto bg-slate-50/30">
                <div v-if="isLoading" class="p-12 text-center text-slate-400">Loading notifications…</div>
                <div v-else class="divide-y divide-slate-100">
                  <div
                    v-for="notif in filteredNotifications" :key="notif.id"
                    @click="openDrawer(notif)"
                    class="p-4 sm:p-5 flex items-start gap-4 hover:bg-slate-50 transition-colors cursor-pointer group relative"
                    :class="{'bg-white': notif.isRead, 'bg-blue-50/30': !notif.isRead}"
                  >
                    <div v-if="!notif.isRead" class="absolute left-0 top-0 bottom-0 w-1 bg-[#2563EB]"></div>

                    <div :class="`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${typeColors(notif.type).bg} ${typeColors(notif.type).text}`">
                      <component :is="typeIcon(notif.type)" class="w-5 h-5" />
                    </div>

                    <div class="flex-1 min-w-0">
                      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1">
                        <div class="flex items-center gap-2 flex-wrap">
                          <h4 class="text-sm font-bold text-slate-900 group-hover:text-[#2563EB] transition-colors line-clamp-1">{{ notif.title }}</h4>
                          <span v-if="notif.complaintId" class="px-2 py-0.5 rounded bg-slate-100 text-[10px] font-bold text-slate-600 border border-slate-200 font-mono">{{ notif.complaintId }}</span>
                        </div>
                        <span class="text-xs font-medium text-slate-400 shrink-0">{{ timeAgo(notif.createdAt) }}</span>
                      </div>
                      <p class="text-sm text-slate-600 line-clamp-2">{{ notif.message }}</p>
                    </div>

                    <div class="hidden sm:flex opacity-0 group-hover:opacity-100 transition-opacity gap-2 shrink-0">
                      <button @click.stop="toggleRead(notif)" class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded" title="Mark Read">
                        <CheckCircle class="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div v-if="filteredNotifications.length === 0" class="p-12 text-center text-slate-500 bg-white">
                    <Bell class="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <p class="font-bold text-slate-900">No notifications found</p>
                    <p class="text-sm mt-1">Try adjusting your filters or search query.</p>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>

    <!-- Notification Details Drawer -->
    <Teleport to="body">
      <div v-if="drawerOpen && activeNotif" class="fixed inset-0 z-50 bg-slate-900/30 backdrop-blur-sm flex justify-end animate-fade-in" @click="closeDrawer">
        <div class="w-full max-w-md bg-white h-full shadow-2xl flex flex-col transform transition-transform animate-slide-in" @click.stop>
          
          <div class="p-6 border-b border-slate-100 flex justify-between items-start bg-slate-50">
            <div class="flex items-center gap-3">
              <div :class="`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${typeColors(activeNotif.type).bg} ${typeColors(activeNotif.type).text}`">
                <component :is="typeIcon(activeNotif.type)" class="w-5 h-5" />
              </div>
              <div>
                <h2 class="text-lg font-bold text-slate-900 leading-tight capitalize">{{ activeNotif.type }} Notification</h2>
                <p class="text-xs text-slate-500 mt-0.5">{{ formatDateTime(activeNotif.createdAt) }}</p>
              </div>
            </div>
            <button @click="closeDrawer" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6 space-y-6">
            <div>
              <h3 class="text-xl font-bold text-slate-900 mb-2">{{ activeNotif.title }}</h3>
              <p class="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100">
                {{ activeNotif.message }}
              </p>
            </div>

            <div v-if="activeNotif.complaintId" class="space-y-3">
              <h4 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Related Complaint</h4>
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <p class="text-xs text-slate-500 font-bold mb-1">ID</p>
                <p class="font-mono font-medium text-[#2563EB]">{{ activeNotif.complaintId }}</p>
              </div>
            </div>
          </div>
          
          <div class="p-6 border-t border-slate-100 bg-white grid grid-cols-2 gap-3 shrink-0">
            <button v-if="!activeNotif.isRead" @click="toggleRead(activeNotif); closeDrawer()" class="py-2.5 border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors flex items-center justify-center gap-2 text-sm">
              <CheckCircle class="w-4 h-4" /> Mark Read
            </button>
            <button v-else @click="closeDrawer" class="py-2.5 border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors text-sm">
              Close
            </button>
            
            <router-link v-if="activeNotif.complaintId" :to="`/officer/complaints/${activeNotif.complaintId.replace('CMP-', '').replace(/^0+/, '')}`" class="py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex items-center justify-center gap-2 text-sm shadow-sm">
              <Eye class="w-4 h-4" /> Open Complaint
            </router-link>
            <span v-else></span>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import {
  Bell, CheckCircle, Clock, Clipboard, Users, Search, Eye, Activity, X
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })

const isSidebarOpen = ref(false)
const drawerOpen = ref(false)
const activeNotif = ref(null)
const isLoading = ref(true)
const loadError = ref('')

const activeTab = ref('All')
const searchQuery = ref('')
const filters = reactive({ date: 'All' })

const notifications = ref([])
const summary = ref({ all: 0, unread: 0, read: 0 })

const tabs = [
  { name: 'All' },
  { name: 'Unread' },
  { name: 'Read' },
  { name: 'Assignment' },
  { name: 'System' },
]

const fetchNotifications = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/notifications`, authHeaders())
    notifications.value = data.notifications
    summary.value = data.summary
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load notifications.'
  } finally {
    isLoading.value = false
  }
}

const withinTimeframe = (iso, frame) => {
  if (frame === 'All' || !iso) return true
  const created = new Date(iso)
  const now = new Date()
  const diffDays = (now - created) / (1000 * 60 * 60 * 24)
  if (frame === 'Today') return diffDays < 1
  if (frame === 'Week') return diffDays < 7
  if (frame === 'Month') return diffDays < 30
  return true
}

const filteredNotifications = computed(() => {
  let result = notifications.value

  if (activeTab.value === 'Unread') result = result.filter(n => !n.isRead)
  else if (activeTab.value === 'Read') result = result.filter(n => n.isRead)
  else if (activeTab.value === 'Assignment') result = result.filter(n => n.type === 'assigned')
  else if (activeTab.value === 'System') result = result.filter(n => n.type === 'system')

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(n =>
      n.title.toLowerCase().includes(q) ||
      n.message.toLowerCase().includes(q) ||
      (n.complaintId && n.complaintId.toLowerCase().includes(q))
    )
  }

  result = result.filter(n => withinTimeframe(n.createdAt, filters.date))

  return result
})

const resetFilters = () => {
  searchQuery.value = ''
  filters.date = 'All'
}

const toggleRead = async (notif) => {
  if (notif.isRead) return
  try {
    await axios.patch(`${API_BASE}/notifications/${notif.id}/read`, {}, authHeaders())
    notif.isRead = true
    summary.value.unread = Math.max(0, summary.value.unread - 1)
    summary.value.read += 1
  } catch (err) {
    console.error(err)
  }
}

const markAllRead = async () => {
  try {
    await axios.patch(`${API_BASE}/notifications/read-all`, {}, authHeaders())
    notifications.value.forEach(n => { n.isRead = true })
    summary.value.read = summary.value.all
    summary.value.unread = 0
  } catch (err) {
    console.error(err)
  }
}

const openDrawer = (notif) => {
  activeNotif.value = notif
  drawerOpen.value = true
  toggleRead(notif)
}

const closeDrawer = () => {
  drawerOpen.value = false
  setTimeout(() => activeNotif.value = null, 300)
}

const timeAgo = (iso) => {
  if (!iso) return ''
  const diffMs = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diffMs / 60000)
  if (mins < 1) return 'Just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: '2-digit' })
}

const formatDateTime = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleString('en-US', { month: 'short', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const typeIcon = (type) => {
  const map = { 'assigned': Clipboard, 'system': Activity }
  return map[type] || Bell
}

const typeColors = (type) => {
  const map = {
    'assigned': { bg: 'bg-purple-100', text: 'text-purple-600' },
    'system':   { bg: 'bg-slate-200', text: 'text-slate-600' },
  }
  return map[type] || { bg: 'bg-blue-100', text: 'text-[#2563EB]' }
}

onMounted(fetchNotifications)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}
.animate-slide-in {
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>