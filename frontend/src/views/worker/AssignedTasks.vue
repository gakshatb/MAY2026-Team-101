<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">

          <!-- Header & Breadcrumbs -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Assigned Tasks</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Assigned Tasks</h1>
              <p class="text-slate-500 mt-1">View, organize, and manage all complaints assigned to you.</p>
            </div>
          </div>

          <!-- Summary Statistics Cards -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="stat in summaryStats" :key="stat.title" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start mb-2">
                <div :class="`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor}`">
                  <component :is="stat.icon" class="w-4 h-4" />
                </div>
              </div>
              <p class="text-2xl font-extrabold text-slate-900">{{ stat.value }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">{{ stat.title }}</p>
            </div>
          </div>

          <!-- Main Workspace Layout -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">

            <!-- Left Column: Task Management (8 cols) -->
            <div class="xl:col-span-8 flex flex-col gap-6">

              <!-- Toolbar: Search, Filters, View Toggle -->
              <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 justify-between items-center z-10">
                <div class="relative w-full lg:w-72 shrink-0">
                  <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    v-model="filters.search"
                    type="text"
                    placeholder="Search by ID, title, or area..."
                    class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none transition-all"
                  />
                </div>

                <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
                  <select v-model="filters.status" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                    <option value="All">All Statuses</option>
                    <option value="Assigned">Assigned</option>
                    <option value="In Progress">In Progress</option>
                  </select>

                  <select v-model="filters.priority" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                    <option value="All">All Priorities</option>
                    <option value="Emergency">Emergency</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                    <option value="Low">Low</option>
                  </select>

                  <select v-model="filters.sort" class="bg-white border border-slate-300 text-slate-900 font-medium text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none shadow-sm">
                    <option value="Priority">Sort by: Priority</option>
                    <option value="Newest">Sort by: Newest</option>
                  </select>

                  <!-- View Toggle -->
                  <div class="flex bg-slate-100 p-1 rounded-lg border border-slate-200 ml-auto lg:ml-2">
                    <button @click="viewMode = 'grid'" :class="`p-1.5 rounded-md transition-colors ${viewMode === 'grid' ? 'bg-white shadow-sm text-[#2563EB]' : 'text-slate-500 hover:text-slate-700'}`">
                      <LayoutGrid class="w-4 h-4" />
                    </button>
                    <button @click="viewMode = 'list'" :class="`p-1.5 rounded-md transition-colors ${viewMode === 'list' ? 'bg-white shadow-sm text-[#2563EB]' : 'text-slate-500 hover:text-slate-700'}`">
                      <List class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="loading" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-10 text-center text-slate-500">Loading tasks…</div>
              <div v-else-if="loadError" class="bg-white rounded-[14px] shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>

              <!-- Task List/Grid -->
              <template v-else>
                <div v-if="filteredTasks.length > 0">

                  <!-- GRID VIEW -->
                  <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div v-for="task in filteredTasks" :key="task.id"
                      class="bg-white rounded-[14px] shadow-sm border flex flex-col overflow-hidden transition-all duration-300 group hover:shadow-md"
                      :class="task.priority === 'Emergency' ? 'border-red-300 ring-1 ring-red-100' : 'border-slate-100'"
                    >
                      <!-- Emergency Banner -->
                      <div v-if="task.priority === 'Emergency'" class="bg-red-500 text-white text-[10px] font-bold uppercase tracking-wider px-3 py-1 text-center flex items-center justify-center gap-1.5">
                        <AlertTriangle class="w-3 h-3" /> Emergency Task - Immediate Action Required
                      </div>

                      <div class="p-4 flex-1">
                        <div class="flex justify-between items-start mb-3 gap-2">
                          <div>
                            <div class="flex items-center gap-2 mb-1">
                              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-600 font-mono">{{ task.id }}</span>
                              <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${priorityBadge(task.priority)}`">{{ task.priority }}</span>
                              <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${statusBadge(task.status)}`">{{ task.status }}</span>
                            </div>
                            <h3 class="font-bold text-slate-900 leading-tight group-hover:text-[#2563EB] transition-colors">{{ task.title }}</h3>
                          </div>
                        </div>

                        <div class="grid grid-cols-2 gap-y-2 text-xs text-slate-500 mb-4">
                          <span class="flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-slate-400"/> <span class="truncate">{{ task.area }}</span></span>
                          <span class="flex items-center gap-1.5"><Building class="w-3.5 h-3.5 text-slate-400"/> <span class="truncate">{{ task.category }}</span></span>
                          <span class="flex items-center gap-1.5"><UserCheck class="w-3.5 h-3.5 text-slate-400 shrink-0"/> {{ task.officer || 'Unassigned' }}</span>
                          <span class="flex items-center gap-1.5"><Clock class="w-3.5 h-3.5 text-slate-400 shrink-0"/> {{ formatDate(task.assigned_at) }}</span>
                        </div>

                        <!-- Progress Bar -->
                        <div>
                          <div class="flex justify-between text-[10px] font-bold text-slate-500 mb-1">
                            <span>Task Progress</span>
                            <span>{{ getProgress(task.status) }}%</span>
                          </div>
                          <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                            <div class="h-full rounded-full transition-all duration-700 bg-[#2563EB]" :style="`width: ${getProgress(task.status)}%`"></div>
                          </div>
                        </div>
                      </div>

                      <!-- Card Actions -->
                      <div class="bg-slate-50 border-t border-slate-100 p-3 flex gap-2">
                        <router-link :to="`/worker/task/${task.raw_id}`" class="px-3 py-2 bg-white border border-slate-200 text-slate-600 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors flex-1 flex justify-center items-center">
                          View Details
                        </router-link>
                        <router-link :to="`/worker/update/${task.raw_id}`" class="px-3 py-2 text-white text-xs font-bold rounded-lg transition-colors flex-1 shadow-sm flex items-center justify-center gap-1.5" :class="actionButtonTheme(task.status)">
                          <component :is="actionButtonIcon(task.status)" class="w-3.5 h-3.5" />
                          {{ actionButtonText(task.status) }}
                        </router-link>
                      </div>
                    </div>
                  </div>

                  <!-- TABLE VIEW -->
                  <div v-else class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                    <div class="overflow-x-auto">
                      <table class="w-full text-left text-sm whitespace-nowrap">
                        <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide border-b border-slate-100">
                          <tr>
                            <th class="px-5 py-4">Task Info</th>
                            <th class="px-5 py-4">Status & Priority</th>
                            <th class="px-5 py-4">Assigned</th>
                            <th class="px-5 py-4">Progress</th>
                            <th class="px-5 py-4 text-right">Actions</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                          <tr v-for="task in filteredTasks" :key="task.id" class="hover:bg-slate-50 transition-colors group" :class="task.priority === 'Emergency' ? 'bg-red-50/30' : ''">
                            <td class="px-5 py-4">
                              <p class="font-bold text-slate-900 mb-0.5">{{ task.id }}</p>
                              <p class="text-xs text-slate-500 flex items-center gap-1"><MapPin class="w-3 h-3"/> {{ task.area }}</p>
                            </td>
                            <td class="px-5 py-4 space-y-1.5">
                              <div><span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${priorityBadge(task.priority)}`">{{ task.priority }}</span></div>
                              <div><span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${statusBadge(task.status)}`">{{ task.status }}</span></div>
                            </td>
                            <td class="px-5 py-4">
                              <span class="text-slate-600 font-medium text-xs">{{ formatDate(task.assigned_at) }}</span>
                            </td>
                            <td class="px-5 py-4 min-w-[120px]">
                              <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                <div class="h-full rounded-full bg-[#2563EB]" :style="`width: ${getProgress(task.status)}%`"></div>
                              </div>
                              <p class="text-[10px] text-slate-400 mt-1 font-bold">{{ getProgress(task.status) }}%</p>
                            </td>
                            <td class="px-5 py-4 text-right">
                              <div class="flex items-center justify-end gap-2">
                                <router-link :to="`/worker/task/${task.raw_id}`" class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-50 transition-colors">Details</router-link>
                                <router-link :to="`/worker/update/${task.raw_id}`" class="px-3 py-1.5 text-white text-xs font-bold rounded transition-colors shadow-sm" :class="actionButtonTheme(task.status)">Update</router-link>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                </div>

                <!-- Empty State -->
                <div v-else class="bg-white p-12 rounded-[14px] border border-slate-100 text-center shadow-sm">
                  <CheckCircle class="w-12 h-12 text-green-300 mx-auto mb-4" />
                  <h3 class="text-lg font-bold text-slate-900 mb-1">You're all caught up!</h3>
                  <p class="text-slate-500 text-sm">No assigned tasks match your current filters.</p>
                </div>
              </template>
            </div>

            <!-- Right Column: Context (4 cols) -->
            <div class="xl:col-span-4 space-y-6">

              <!-- Safety Reminder -->
              <div class="bg-amber-50 rounded-[14px] shadow-sm border border-amber-200 p-5">
                <div class="flex items-center gap-2 mb-3">
                  <AlertTriangle class="w-5 h-5 text-amber-600" />
                  <h3 class="font-bold text-amber-800">Safety First</h3>
                </div>
                <ul class="text-sm text-amber-700 space-y-2">
                  <li class="flex items-start gap-2"><span class="font-bold">•</span> Always wear standard safety equipment.</li>
                  <li class="flex items-start gap-2"><span class="font-bold">•</span> Report hazardous situations immediately.</li>
                </ul>
              </div>

              <!-- Performance Summary -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Activity class="w-5 h-5 text-purple-500" /> Performance Summary</h3>
                <div class="grid grid-cols-2 gap-3">
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p class="text-[10px] font-bold text-slate-500 uppercase mb-1">Completed Tasks</p>
                    <p class="text-xl font-bold text-slate-900">{{ profile.completedCount ?? '—' }}</p>
                  </div>
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p class="text-[10px] font-bold text-slate-500 uppercase mb-1">Citizen Rating</p>
                    <p class="text-xl font-bold text-slate-900">{{ profile.avgRating ?? '—' }}</p>
                  </div>
                </div>
              </div>

              <!-- Quick Navigation -->
              <div class="grid grid-cols-2 gap-3">
                <router-link to="/worker/completed" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <CheckCircle class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Completed Tasks</span>
                </router-link>
                <router-link to="/worker/notifications" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <Bell class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Notifications</span>
                </router-link>
              </div>

            </div>
          </div>

        </div>
      </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import {
  ClipboardList, CheckCircle, Clock, MapPin, AlertTriangle,
  UserCheck, Building, Activity, PlayCircle,
  Search, LayoutGrid, List, Bell
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

// --- State ---
const viewMode = ref('grid')
const loading = ref(true)
const loadError = ref('')
const tasks = ref([])
const profile = reactive({})

const filters = reactive({
  search: '',
  status: 'All',
  priority: 'All',
  sort: 'Priority'
})

const summaryStats = computed(() => {
  const assigned = tasks.value.filter(t => t.status === 'Assigned').length
  const inProgress = tasks.value.filter(t => t.status === 'In Progress').length
  const emergency = tasks.value.filter(t => t.priority === 'Emergency').length
  return [
    { title: 'Total Active', value: tasks.value.length, icon: ClipboardList, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
    { title: 'Awaiting Start', value: assigned, icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
    { title: 'In Progress', value: inProgress, icon: Activity, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
    { title: 'Emergency', value: emergency, icon: AlertTriangle, iconBg: 'bg-red-50', iconColor: 'text-red-600' },
  ]
})

// --- Computed & Methods ---
const filteredTasks = computed(() => {
  let result = [...tasks.value]

  if (filters.search) {
    const q = filters.search.toLowerCase()
    result = result.filter(t => t.id.toLowerCase().includes(q) || t.title.toLowerCase().includes(q) || (t.area || '').toLowerCase().includes(q))
  }

  if (filters.status !== 'All') result = result.filter(t => t.status === filters.status)
  if (filters.priority !== 'All') result = result.filter(t => t.priority === filters.priority)

  if (filters.sort === 'Priority') {
    const pOrder = { 'Emergency': 1, 'High': 2, 'Medium': 3, 'Low': 4 }
    result.sort((a, b) => (pOrder[a.priority] || 5) - (pOrder[b.priority] || 5))
  } else if (filters.sort === 'Newest') {
    result.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
  }

  return result.sort((a, b) => (a.priority === 'Emergency' ? -1 : (b.priority === 'Emergency' ? 1 : 0)))
})

const getProgress = (status) => {
  const map = { 'Assigned': 15, 'In Progress': 60 }
  return map[status] || 0
}

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700 border border-red-200', 'High': 'bg-orange-100 text-orange-700 border border-orange-200', 'Medium': 'bg-blue-100 text-blue-700 border border-blue-200', 'Low': 'bg-slate-100 text-slate-600 border border-slate-200' }
  return map[priority] || 'bg-slate-100 text-slate-600 border border-slate-200'
}

const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'In Progress': 'bg-amber-100 text-amber-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const actionButtonTheme = (status) => {
  if (status === 'Assigned') return 'bg-[#2563EB] hover:bg-[#1E40AF]'
  return 'bg-[#F59E0B] hover:bg-amber-600'
}
const actionButtonText = (status) => status === 'Assigned' ? 'Start Work' : 'Update Status'
const actionButtonIcon = () => PlayCircle

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function loadTasks() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/worker/tasks`, {
      headers: authHeaders(),
      params: { status: 'active' }
    })
    tasks.value = data.tasks || []
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load assigned tasks.'
  } finally {
    loading.value = false
  }
}

async function loadProfileSummary() {
  try {
    const { data } = await axios.get(`${API_BASE}/worker/profile`, { headers: authHeaders() })
    Object.assign(profile, data.profile)
  } catch (err) {
    // Non-fatal.
  }
}

onMounted(() => {
  loadTasks()
  loadProfileSummary()
})
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