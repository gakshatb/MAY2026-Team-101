<template>
  <div class="max-w-7xl mx-auto space-y-8">

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div v-for="card in summaryCards" :key="card.title"
        class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4 transition-transform hover:shadow-md">
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
    <div
      class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 items-center justify-between">
      <div class="flex flex-wrap gap-2 w-full lg:w-auto">
        <button v-for="filter in filters" :key="filter" @click="activeFilter = filter"
          :class="['px-4 py-2 text-sm font-medium rounded-lg transition-colors', activeFilter === filter ? 'bg-[#2563EB] text-white' : 'text-slate-600 hover:bg-slate-50']">
          {{ filter }}
        </button>
      </div>
      <div class="flex gap-2 w-full lg:w-auto">
        <button @click="markAllRead"
          class="flex-1 lg:flex-none flex items-center justify-center gap-2 px-4 py-2.5 bg-slate-50 hover:bg-slate-100 text-slate-700 text-sm font-medium rounded-lg transition-colors">
          <Check class="w-4 h-4" /> Mark All Read
        </button>
      </div>
    </div>

    <!-- Notification List -->
    <div v-if="filteredNotifications.length > 0" class="space-y-3">
      <div v-for="note in filteredNotifications" :key="note.id" @click="openDrawer(note)"
        :class="['group bg-white p-5 rounded-[14px] border shadow-sm flex gap-4 cursor-pointer transition-all hover:shadow-md', note.isRead ? 'border-slate-100' : 'border-l-4 border-l-[#2563EB] border-slate-200 bg-blue-50/10']">
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
            <span v-if="note.complaintId !== 'SYS'"
              class="text-[10px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2 py-1 rounded">{{
                note.complaintId }}</span>
            <span v-else></span>
            <button v-if="note.complaintId !== 'SYS'" @click.stop="goToComplaint(note)"
              class="text-sm font-medium text-[#2563EB] hover:underline">View Complaint</button>
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

  <!-- Details Drawer (UI Only) -->
  <transition name="drawer">
    <div v-if="selectedNotification" class="fixed inset-0 z-50 flex justify-end">
      <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="selectedNotification = null"></div>
      <div class="bg-white w-full max-w-md shadow-2xl h-full p-8 overflow-y-auto">
        <button @click="selectedNotification = null" class="mb-8 p-2 hover:bg-slate-100 rounded-lg">
          <X />
        </button>
        <h2 class="text-2xl font-bold text-slate-900 mb-4">{{ selectedNotification.title }}</h2>
        <div v-if="selectedNotification.complaintId !== 'SYS'" class="bg-blue-50 p-4 rounded-xl mb-6">
          <p class="text-sm text-[#2563EB] font-medium">Complaint #{{ selectedNotification.complaintId }}</p>
        </div>
        <p class="text-slate-600 leading-relaxed mb-8">{{ selectedNotification.message }}</p>
        <div class="flex gap-3">
          <button v-if="selectedNotification.complaintId !== 'SYS'" @click="goToComplaint(selectedNotification)"
            class="flex-1 px-4 py-3 bg-[#2563EB] text-white rounded-lg font-medium">View Complaint</button>
          <button @click="selectedNotification = null"
            class="px-4 py-3 border border-slate-200 rounded-lg font-medium">Close</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  Bell, CheckCircle, AlertCircle, Clock,
  MessageSquare, User, Shield, SearchX, X,
  Check, Mail, Zap
} from 'lucide-vue-next'

const router = useRouter()
const activeFilter = ref('All')
const selectedNotification = ref(null)
const isLoading = ref(true)

const summaryCards = ref([
  { title: 'All', count: 0, icon: Bell, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Unread', count: 0, icon: Mail, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Read', count: 0, icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'System', count: 0, icon: Shield, iconBg: 'bg-red-50', iconColor: 'text-red-500' },
])

const filters = ['All', 'Unread', 'Complaint Updates', 'System Messages']

const allNotifications = ref([])

// The backend doesn't support server-side filtering on this endpoint —
// it always returns the full list — so filtering happens client-side.
const filteredNotifications = computed(() => {
  if (activeFilter.value === 'All') return allNotifications.value
  if (activeFilter.value === 'Unread') return allNotifications.value.filter(n => !n.isRead)
  if (activeFilter.value === 'Complaint Updates') return allNotifications.value.filter(n => n.complaintId !== 'SYS')
  if (activeFilter.value === 'System Messages') return allNotifications.value.filter(n => n.complaintId === 'SYS')
  return allNotifications.value
})

const fetchNotifications = async () => {
  isLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://127.0.0.1:5000/api/citizen/notifications', {
      headers: { Authorization: `Bearer ${token}` }
    })
    allNotifications.value = data.notifications.map(n => ({
      id: n.id,
      title: n.title,
      message: n.message,
      complaintId: n.complaint_id || 'SYS',
      time: new Date(n.created_at).toLocaleString(),
      isRead: n.is_read,
      icon: CheckCircle,
      iconBg: n.type === 'system' ? 'bg-red-50' : 'bg-green-50',
      iconColor: n.type === 'system' ? 'text-red-500' : 'text-green-500',
    }))

    summaryCards.value[0].count = data.summary.all
    summaryCards.value[1].count = data.summary.unread
    summaryCards.value[2].count = data.summary.read
    summaryCards.value[3].count = allNotifications.value.filter(n => n.complaintId === 'SYS').length
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
  } finally { isLoading.value = false }
}

const openDrawer = async (note) => {
  selectedNotification.value = note
  if (!note.isRead) {
    try {
      const token = localStorage.getItem('token')
      await axios.patch(
        `http://127.0.0.1:5000/api/citizen/notifications/${note.id}/read`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      note.isRead = true
    } catch (err) { console.error(err) }
  }
}

const markAllRead = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.patch(
      'http://127.0.0.1:5000/api/citizen/notifications/read-all',
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    )
    allNotifications.value.forEach(n => n.isRead = true)
  } catch (err) { console.error(err) }
}

const goToComplaint = (note) => {
  if (note.complaintId === 'SYS') return
  const rawId = parseInt(note.complaintId.replace('CMP-', ''), 10)
  router.push(`/citizen/complaintdetails/${rawId}`)
}

onMounted(fetchNotifications)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
.drawer-enter-active,
.drawer-leave-active { transition: opacity 0.3s; }
.drawer-enter-from,
.drawer-leave-to { opacity: 0; }
</style>