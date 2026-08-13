<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">

          <!-- Header Section -->
          <div class="flex flex-col lg:flex-row justify-between lg:items-end gap-4">
            <div>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">{{ greeting }}, {{ dashboard.worker?.name || '...' }}</h1>
              <p class="text-slate-500 mt-1">Here's your work schedule and assigned tasks for today.</p>
            </div>

            <div class="flex flex-wrap items-center gap-3">
              <div v-if="dashboard.worker?.department" class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <MapPin class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">{{ dashboard.worker.department }}</span>
              </div>
              <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <Calendar class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">{{ currentDate }}</span>
              </div>
            </div>
          </div>

          <div v-if="loading" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-10 text-center text-slate-500">Loading dashboard…</div>
          <div v-else-if="loadError" class="bg-white rounded-2xl shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>

          <template v-else>
            <!-- Top KPI Summary Cards -->
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              <div v-for="(kpi, idx) in kpiCards" :key="idx" class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 relative overflow-hidden">
                <div class="flex justify-between items-start mb-2 relative z-10">
                  <div :class="`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${kpi.bg} ${kpi.color}`">
                    <component :is="kpi.icon" class="w-4 h-4" />
                  </div>
                </div>
                <div class="relative z-10">
                  <p class="text-xl lg:text-2xl font-extrabold text-slate-900">{{ kpi.value }}</p>
                  <p class="text-[11px] font-semibold text-slate-500 mt-0.5 leading-tight">{{ kpi.title }}</p>
                </div>
              </div>
            </div>

            <!-- Primary Workspace Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

              <!-- Left Main Column (8 cols) -->
              <div class="lg:col-span-8 flex flex-col gap-6">

                <!-- Current Active Task Highlight -->
                <div v-if="dashboard.current_task" class="bg-gradient-to-br from-[#1E40AF] to-[#2563EB] rounded-2xl shadow-md overflow-hidden relative text-white">
                  <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
                  <div class="p-6 relative z-10">
                    <div class="flex justify-between items-start mb-4">
                      <div>
                        <div class="flex items-center gap-2 mb-2">
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-white/20 backdrop-blur-sm border border-white/20 font-mono">{{ dashboard.current_task.id }}</span>
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/30">{{ dashboard.current_task.status }}</span>
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-red-500/20 text-red-200 border border-red-500/30">{{ dashboard.current_task.priority }}</span>
                        </div>
                        <h2 class="text-2xl font-bold mb-1">{{ dashboard.current_task.title }}</h2>
                        <div class="flex items-center gap-4 text-sm text-blue-100 font-medium">
                          <span class="flex items-center gap-1"><MapPin class="w-4 h-4" /> {{ dashboard.current_task.area }}</span>
                          <span v-if="dashboard.current_task.officer" class="flex items-center gap-1"><User class="w-4 h-4" /> Officer: {{ dashboard.current_task.officer }}</span>
                        </div>
                      </div>
                    </div>

                    <div class="flex flex-wrap gap-3">
                      <router-link :to="`/worker/task/${dashboard.current_task.raw_id}`" class="px-5 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white text-sm font-bold rounded-lg transition-colors backdrop-blur-sm flex items-center gap-2">
                        <FileText class="w-4 h-4" /> View Details
                      </router-link>
                      <router-link :to="`/worker/update/${dashboard.current_task.raw_id}`" class="px-5 py-2.5 bg-white text-[#2563EB] hover:bg-slate-50 text-sm font-bold rounded-lg transition-colors shadow-sm flex items-center gap-2">
                        <PlayCircle class="w-4 h-4" /> Update Complaint
                      </router-link>
                    </div>
                  </div>
                </div>
                <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 text-center text-slate-500">
                  No active task right now. Check your <router-link to="/worker/tasks" class="text-[#2563EB] font-semibold hover:underline">assigned tasks</router-link>.
                </div>

                <!-- Emergency Assignments -->
                <div v-if="dashboard.emergencies?.length > 0" class="bg-white rounded-2xl shadow-sm border border-red-200 overflow-hidden">
                  <div class="bg-red-50 px-5 py-3 border-b border-red-100 flex items-center justify-between">
                    <h3 class="font-bold text-red-700 flex items-center gap-2">
                      <div class="relative flex h-3 w-3"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span><span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span></div>
                      Emergency Assignments
                    </h3>
                  </div>
                  <div class="divide-y divide-slate-100">
                    <div v-for="em in dashboard.emergencies" :key="em.id" class="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50 transition-colors">
                      <div class="flex gap-4">
                        <div class="w-10 h-10 rounded-xl bg-red-100 text-red-600 flex items-center justify-center shrink-0">
                          <AlertTriangle class="w-5 h-5" />
                        </div>
                        <div>
                          <div class="flex items-center gap-2 mb-0.5">
                            <p class="font-bold text-slate-900">{{ em.title }}</p>
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-white border border-slate-200 text-slate-600 uppercase tracking-wider font-mono">{{ em.id }}</span>
                          </div>
                          <p class="text-xs text-slate-600 flex items-center gap-3">
                            <span class="flex items-center gap-1"><MapPin class="w-3 h-3 text-slate-400"/> {{ em.area }}</span>
                          </p>
                        </div>
                      </div>
                      <router-link :to="`/worker/update/${em.raw_id}`" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg shadow-sm transition-colors whitespace-nowrap">Start Immediately</router-link>
                    </div>
                  </div>
                </div>

                <!-- Quick Actions -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <router-link v-for="action in quickActions" :key="action.title" :to="action.link" class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all group text-left flex flex-col items-start">
                    <div class="w-10 h-10 rounded-xl bg-slate-50 group-hover:bg-blue-50 text-slate-500 group-hover:text-[#2563EB] flex items-center justify-center mb-3 transition-colors">
                      <component :is="action.icon" class="w-5 h-5" />
                    </div>
                    <h3 class="font-bold text-slate-900 text-sm mb-1">{{ action.title }}</h3>
                    <p class="text-xs text-slate-500">{{ action.desc }}</p>
                  </router-link>
                </div>

                <!-- Assigned Tasks Preview (Table) -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                  <div class="p-5 border-b border-slate-100 flex items-center justify-between">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><ClipboardList class="w-5 h-5 text-[#2563EB]" /> Assigned Tasks</h3>
                    <router-link to="/worker/tasks" class="text-sm font-medium text-[#2563EB] hover:underline">View All Tasks</router-link>
                  </div>
                  <div v-if="!dashboard.assigned_tasks?.length" class="p-8 text-center text-sm text-slate-500">No active tasks assigned right now.</div>
                  <div v-else class="overflow-x-auto">
                    <table class="w-full text-left text-sm whitespace-nowrap">
                      <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wider border-b border-slate-100">
                        <tr>
                          <th class="px-5 py-3">Task ID & Title</th>
                          <th class="px-5 py-3">Category</th>
                          <th class="px-5 py-3">Status</th>
                          <th class="px-5 py-3 text-right">Action</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-slate-100">
                        <tr v-for="task in dashboard.assigned_tasks" :key="task.id" class="hover:bg-slate-50 transition-colors group">
                          <td class="px-5 py-3">
                            <p class="font-bold text-slate-900 mb-0.5">{{ task.title }}</p>
                            <p class="text-[10px] text-slate-500 font-mono">{{ task.id }} • {{ task.area }}</p>
                          </td>
                          <td class="px-5 py-3 text-slate-600 text-xs font-medium">{{ task.category }}</td>
                          <td class="px-5 py-3">
                            <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${statusBadge(task.status)}`">{{ task.status }}</span>
                          </td>
                          <td class="px-5 py-3 text-right">
                            <div class="flex items-center justify-end gap-2">
                              <router-link :to="`/worker/task/${task.raw_id}`" class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-50 transition-colors">Details</router-link>
                              <router-link :to="`/worker/update/${task.raw_id}`" class="px-3 py-1.5 bg-[#2563EB] text-white text-xs font-bold rounded hover:bg-[#1E40AF] transition-colors shadow-sm">Update</router-link>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

              </div>

              <!-- Right Context Column (4 cols) -->
              <div class="lg:col-span-4 space-y-6">

                <!-- Safety Reminder -->
                <div class="bg-amber-50 rounded-2xl shadow-sm border border-amber-200 p-5">
                  <div class="flex items-center gap-2 mb-3">
                    <AlertTriangle class="w-5 h-5 text-amber-600" />
                    <h3 class="font-bold text-amber-800">Safety First</h3>
                  </div>
                  <ul class="text-sm text-amber-700 space-y-2">
                    <li class="flex items-start gap-2"><span class="font-bold">•</span> Always wear standard safety equipment.</li>
                    <li class="flex items-start gap-2"><span class="font-bold">•</span> Use warning cones before beginning road work.</li>
                    <li class="flex items-start gap-2"><span class="font-bold">•</span> Report hazardous situations immediately.</li>
                  </ul>
                </div>

                <!-- Recent Notifications -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col max-h-[400px]">
                  <div class="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><Bell class="w-4 h-4 text-[#2563EB]" /> Recent Notifications</h3>
                    <router-link to="/worker/notifications" class="text-xs font-medium text-[#2563EB] hover:underline">View All</router-link>
                  </div>
                  <div v-if="!recentNotifications.length" class="flex-1 flex items-center justify-center p-6 text-sm text-slate-500">No notifications yet.</div>
                  <div v-else class="flex-1 overflow-y-auto p-4 space-y-3">
                    <div v-for="note in recentNotifications" :key="note.id" class="bg-blue-50 border border-blue-100 rounded-xl p-3">
                      <p class="text-sm font-bold text-[#1E40AF] mb-1">{{ note.title }}</p>
                      <p class="text-xs text-blue-700 mb-2">{{ note.message }}</p>
                      <p class="text-[9px] text-blue-500 font-medium">{{ formatRelative(note.created_at) }}</p>
                    </div>
                  </div>
                </div>

                <!-- Performance Summary -->
                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Award class="w-5 h-5 text-purple-500" /> Performance Summary</h3>
                  <div class="grid grid-cols-2 gap-3">
                    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 text-center">
                      <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Completed Tasks</p>
                      <p class="text-xl font-bold text-slate-900">{{ profile.completedCount ?? '—' }}</p>
                    </div>
                    <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 text-center">
                      <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Citizen Rating</p>
                      <p class="text-xl font-bold text-slate-900 flex items-center justify-center gap-1">{{ profile.avgRating ?? '—' }} <Star class="w-4 h-4 text-amber-400 fill-amber-400"/></p>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </template>

        </div>
      </main>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import {
  MapPin, Calendar, ClipboardList, CheckCircle,
  Clock, AlertTriangle, FileText, PlayCircle, User,
  MessageSquare, Award, Star, Bell
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

const loading = ref(true)
const loadError = ref('')
const dashboard = reactive({})
const profile = reactive({})
const recentNotifications = ref([])

const currentDate = new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: '2-digit' })
const greeting = (() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good Morning'
  if (h < 17) return 'Good Afternoon'
  return 'Good Evening'
})()

const kpiCards = ref([])

const quickActions = [
  { title: 'My Tasks', desc: 'View assigned list', icon: ClipboardList, link: '/worker/tasks' },
  { title: 'Completed', desc: 'Work history', icon: CheckCircle, link: '/worker/completed' },
  { title: 'Alerts', desc: 'Recent updates', icon: Bell, link: '/worker/notifications' },
  { title: 'Profile', desc: 'Manage account', icon: User, link: '/worker/profile' }
]

const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Resolved': 'bg-green-100 text-green-700', 'Closed': 'bg-slate-200 text-slate-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

function formatRelative(iso) {
  if (!iso) return ''
  const diffMs = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diffMs / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins} min${mins > 1 ? 's' : ''} ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs} hour${hrs > 1 ? 's' : ''} ago`
  const days = Math.floor(hrs / 24)
  return `${days} day${days > 1 ? 's' : ''} ago`
}

async function loadDashboard() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/worker/dashboard`, { headers: authHeaders() })
    Object.assign(dashboard, data.dashboard)
    const c = data.dashboard.counts || {}
    kpiCards.value = [
      { title: 'Total Tasks', value: c.total ?? 0, icon: ClipboardList, bg: 'bg-blue-50', color: 'text-blue-600' },
      { title: 'Active', value: c.active ?? 0, icon: Clock, bg: 'bg-amber-50', color: 'text-amber-500' },
      { title: 'In Progress', value: c.in_progress ?? 0, icon: PlayCircle, bg: 'bg-purple-50', color: 'text-purple-500' },
      { title: 'Completed', value: c.completed ?? 0, icon: CheckCircle, bg: 'bg-green-50', color: 'text-green-500' },
      { title: 'Emergency', value: c.emergency ?? 0, icon: AlertTriangle, bg: 'bg-red-50', color: 'text-red-500' },
    ]
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load dashboard.'
  } finally {
    loading.value = false
  }
}

async function loadProfileSummary() {
  try {
    const { data } = await axios.get(`${API_BASE}/worker/profile`, { headers: authHeaders() })
    Object.assign(profile, data.profile)
  } catch (err) {
    // Non-fatal — performance card just stays blank.
  }
}

async function loadNotifications() {
  try {
    const { data } = await axios.get(`${API_BASE}/worker/notifications`, { headers: authHeaders() })
    recentNotifications.value = (data.notifications || []).slice(0, 4)
  } catch (err) {
    // Non-fatal.
  }
}

onMounted(() => {
  loadDashboard()
  loadProfileSummary()
  loadNotifications()
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