<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1200px] mx-auto space-y-6 animate-fade-in">

          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Notifications</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Notifications</h1>
              <p class="text-slate-500 mt-1">Stay updated on task assignments and status changes.</p>
            </div>
            <button v-if="unreadCount > 0" @click="markAllRead" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
              <CheckCircle class="w-4 h-4 text-[#2563EB]" /> Mark All Read
            </button>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-blue-50 text-[#2563EB] mb-2"><Bell class="w-4 h-4" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ notifications.length }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Total</p>
            </div>
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-amber-50 text-amber-500 mb-2"><Clock class="w-4 h-4" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ unreadCount }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Unread</p>
            </div>
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-red-50 text-red-500 mb-2"><AlertTriangle class="w-4 h-4" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ emergencyCount }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Emergency</p>
            </div>
          </div>

          <!-- Tabs -->
          <div class="flex gap-2 bg-white p-2 rounded-2xl shadow-sm border border-slate-100 w-fit">
            <button v-for="tab in tabs" :key="tab" @click="activeTab = tab" :class="`px-4 py-2 rounded-xl text-sm font-bold transition-colors ${activeTab === tab ? 'bg-[#2563EB] text-white' : 'text-slate-500 hover:bg-slate-50'}`">
              {{ tab }}
            </button>
          </div>

          <div v-if="loading" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-10 text-center text-slate-500">Loading notifications…</div>
          <div v-else-if="loadError" class="bg-white rounded-2xl shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>
          <div v-else-if="filteredNotifications.length === 0" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-10 text-center text-slate-500">Nothing here.</div>

          <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-100 divide-y divide-slate-100 overflow-hidden">
            <div
              v-for="note in filteredNotifications"
              :key="note.id"
              class="p-4 flex items-start gap-4 hover:bg-slate-50 transition-colors"
              :class="{ 'bg-blue-50/40': !note.is_read }"
            >
              <div :class="`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${typeStyle(note.type).bg} ${typeStyle(note.type).color}`">
                <component :is="typeStyle(note.type).icon" class="w-5 h-5" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-2">
                  <p class="font-bold text-slate-900 text-sm">{{ note.title }}</p>
                  <span v-if="!note.is_read" class="w-2 h-2 rounded-full bg-[#2563EB] shrink-0 mt-1.5"></span>
                </div>
                <p class="text-sm text-slate-600 mt-0.5">{{ note.message }}</p>
                <div class="flex items-center gap-3 mt-2">
                  <p class="text-[11px] text-slate-400 font-medium">{{ formatDate(note.created_at) }}</p>
                  <router-link v-if="note.complaint_id" :to="`/worker/task/${note.complaint_id}`" class="text-[11px] font-bold text-[#2563EB] hover:underline">View Task</router-link>
                  <button v-if="!note.is_read" @click="markRead(note)" class="text-[11px] font-bold text-slate-500 hover:text-slate-700">Mark Read</button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import {
  Bell, CheckCircle, AlertTriangle, Clock, Activity, MessageSquare, Info
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

const loading = ref(true)
const loadError = ref('')
const notifications = ref([])
const activeTab = ref('All')

const tabs = ['All', 'Unread']

const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)
const emergencyCount = computed(() => notifications.value.filter(n => n.type === 'emergency' || n.title?.toLowerCase().includes('emergency')).length)

const filteredNotifications = computed(() => {
  if (activeTab.value === 'Unread') return notifications.value.filter(n => !n.is_read)
  return notifications.value
})

function typeStyle(type) {
  const map = {
    resolved: { icon: CheckCircle, bg: 'bg-green-50', color: 'text-green-600' },
    status_updated: { icon: Activity, bg: 'bg-purple-50', color: 'text-purple-500' },
    assigned: { icon: Bell, bg: 'bg-blue-50', color: 'text-[#2563EB]' },
    emergency: { icon: AlertTriangle, bg: 'bg-red-50', color: 'text-red-500' },
    system: { icon: Info, bg: 'bg-slate-100', color: 'text-slate-500' },
  }
  return map[type] || { icon: MessageSquare, bg: 'bg-slate-100', color: 'text-slate-500' }
}

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
}

async function loadNotifications() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/worker/notifications`, { headers: authHeaders() })
    notifications.value = data.notifications || []
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load notifications.'
  } finally {
    loading.value = false
  }
}

async function markRead(note) {
  try {
    await axios.patch(`${API_BASE}/worker/notifications/${note.id}/read`, {}, { headers: authHeaders() })
    note.is_read = true
  } catch (err) {
    // Non-fatal — leave it unread in the UI if the request fails.
  }
}

async function markAllRead() {
  try {
    await axios.patch(`${API_BASE}/worker/notifications/read-all`, {}, { headers: authHeaders() })
    notifications.value.forEach(n => n.is_read = true)
  } catch (err) {
    // Non-fatal.
  }
}

onMounted(loadNotifications)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>