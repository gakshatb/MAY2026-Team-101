<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1400px] mx-auto space-y-6">
          
          <!-- Breadcrumb & Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB]">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900">Complaint Management</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Complaint Management</h1>
              <p class="text-slate-500 mt-1">Review, assign, and monitor complaints assigned to you.</p>
            </div>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div v-for="stat in topStats" :key="stat.label" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
              <div :class="`w-8 h-8 rounded-lg flex items-center justify-center mb-2 ${stat.bg} ${stat.color}`">
                <component :is="stat.icon" class="w-4 h-4" />
              </div>
              <p class="text-2xl font-bold text-slate-900">{{ stat.value }}</p>
              <p class="text-xs font-medium text-slate-500 mt-1 truncate">{{ stat.label }}</p>
            </div>
          </div>

          <!-- Toolbar (Search & Filters) -->
          <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 justify-between items-center z-10">
            <!-- Search -->
            <div class="relative w-full lg:w-96">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Search by ID, Title, or Citizen..." 
                class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
            
            <!-- Filters -->
            <div class="flex flex-wrap items-center gap-3 w-full lg:w-auto">
              <select v-model="filters.status" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                <option value="All">All Statuses</option>
                <option value="Assigned">Assigned</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Closed">Closed</option>
              </select>

              <select v-model="filters.priority" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                <option value="All">All Priorities</option>
                <option value="Emergency">Emergency</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>
          </div>

          <div v-if="loadError" class="bg-red-50 border border-red-100 text-red-600 text-sm rounded-[14px] p-4">
            {{ loadError }}
          </div>

          <!-- Data Table -->
          <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm whitespace-nowrap">
                <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-100">
                  <tr>
                    <th class="px-6 py-4">Complaint ID</th>
                    <th class="px-6 py-4">Title & Citizen</th>
                    <th class="px-6 py-4">Category</th>
                    <th class="px-6 py-4">Status</th>
                    <th class="px-6 py-4">Priority</th>
                    <th class="px-6 py-4">Assigned Worker</th>
                    <th class="px-6 py-4">Date</th>
                    <th class="px-6 py-4 text-center">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-if="isLoading">
                    <td colspan="8" class="px-6 py-12 text-center text-slate-400">Loading complaints…</td>
                  </tr>
                  <tr v-for="cmp in complaints" :key="cmp.id" v-else class="hover:bg-slate-50 transition-colors group">
                    <td class="px-6 py-4 font-mono font-medium text-slate-900">{{ cmp.id }}</td>
                    <td class="px-6 py-4">
                      <p class="font-bold text-slate-900">{{ cmp.title }}</p>
                      <p class="text-xs text-slate-500">{{ cmp.citizen }} • {{ cmp.area }}</p>
                    </td>
                    <td class="px-6 py-4 text-slate-600">{{ cmp.category }}</td>
                    <td class="px-6 py-4">
                      <span :class="`px-2.5 py-1 rounded-full text-xs font-bold ${statusColor(cmp.status)}`">
                        {{ cmp.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <span :class="`px-2.5 py-1 rounded text-xs font-bold flex items-center gap-1 w-max ${priorityColor(cmp.priority)}`">
                        <AlertTriangle v-if="cmp.priority === 'Emergency'" class="w-3 h-3" />
                        {{ cmp.priority }}
                      </span>
                    </td>
                    <td class="px-6 py-4 text-slate-600">
                      {{ cmp.worker || 'Unassigned' }}
                    </td>
                    <td class="px-6 py-4 text-slate-600">{{ cmp.date }}</td>
                    <td class="px-6 py-4">
                      <div class="flex items-center justify-center gap-2">
                        <router-link :to="`/officer/complaints/${cmp.rawId}`" class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded transition-colors inline-flex" title="View Details">
                          <Eye class="w-4 h-4" />
                        </router-link>
                        <button @click="openModal('assign', cmp)" v-if="!cmp.worker && cmp.status !== 'Resolved' && cmp.status !== 'Closed'" class="p-1.5 text-slate-400 hover:text-purple-600 hover:bg-purple-50 rounded transition-colors" title="Assign Worker">
                          <Users class="w-4 h-4" />
                        </button>
                        <button @click="openModal('return', cmp)" v-if="cmp.status === 'Assigned' && !cmp.worker" class="p-1.5 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded transition-colors" title="Send Back to Admin">
                          <Undo2 class="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="!isLoading && complaints.length === 0">
                    <td colspan="8" class="px-6 py-12 text-center text-slate-500">
                      <Search class="w-8 h-8 text-slate-300 mx-auto mb-3" />
                      <p class="font-medium">No complaints found</p>
                      <p class="text-sm">Try adjusting your search or filters.</p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </main>

    <!-- Teleport Modals to Body for correct z-indexing -->
    <Teleport to="body">
      <!-- Assign Worker Modal -->
      <div v-if="activeModal === 'assign'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
          <div class="p-6 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Assign Field Worker — {{ activeComplaint.id }}</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 bg-slate-50 border-b border-slate-100">
            <div class="relative">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input v-model="workerSearch" type="text" placeholder="Search available workers..." class="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
            </div>
          </div>
          <div class="max-h-64 overflow-y-auto p-2">
            <p v-if="workersLoading" class="text-sm text-slate-400 text-center py-6">Loading workers…</p>
            <p v-else-if="filteredWorkers.length === 0" class="text-sm text-slate-400 text-center py-6">No workers found in your department.</p>
            <div v-for="worker in filteredWorkers" :key="worker.id" class="p-3 hover:bg-slate-50 rounded-lg flex items-center justify-between cursor-pointer border border-transparent hover:border-slate-200 transition-colors">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center font-bold text-slate-500">{{ worker.name.charAt(0) }}</div>
                <div>
                  <p class="font-bold text-slate-900 text-sm">{{ worker.name }}</p>
                  <p class="text-xs text-slate-500">{{ worker.activeTasks }} Active Tasks</p>
                </div>
              </div>
              <button @click="assignWorker(worker.id)" :disabled="isAssigning" class="px-3 py-1.5 bg-blue-50 text-[#2563EB] hover:bg-[#2563EB] hover:text-white text-xs font-bold rounded transition-colors disabled:opacity-50">
                Assign
              </button>
            </div>
          </div>
          <p v-if="modalError" class="text-red-600 text-xs px-6 pb-4">{{ modalError }}</p>
        </div>
      </div>

      <!-- Return to Admin Modal -->
      <div v-if="activeModal === 'return'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden">
          <div class="p-6 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Send Back to Admin — {{ activeComplaint.id }}</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4">
            <p class="text-sm text-slate-600">This unassigns the complaint from you and returns it to the admin queue for re-review.</p>
            <textarea v-model="returnRemark" rows="3" placeholder="Explain why this is being sent back (required)..." class="w-full p-3 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"></textarea>
          </div>
          <div class="p-6 bg-slate-50 border-t border-slate-100 flex gap-3 justify-end">
            <button @click="closeModal" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg">Cancel</button>
            <button @click="returnToAdmin" :disabled="!returnRemark.trim() || isReturning" class="px-4 py-2 text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 shadow-sm rounded-lg disabled:opacity-50">
              {{ isReturning ? 'Sending…' : 'Send Back' }}
            </button>
          </div>
          <p v-if="modalError" class="text-red-600 text-xs px-6 pb-4">{{ modalError }}</p>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Search, AlertTriangle, Eye, Users, X, Undo2, ClipboardList, Clock, CheckCircle, Zap
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })

// Core Layout State
const isSidebarOpen = ref(false)

// Data State
const searchQuery = ref('')
const activeModal = ref(null)
const activeComplaint = ref({})
const modalError = ref('')

const filters = reactive({
  status: 'All',
  priority: 'All'
})

const complaints = ref([])
const isLoading = ref(false)
const loadError = ref('')

const summary = ref({ total: 0, assigned: 0, in_progress: 0, resolved: 0, emergency: 0, avg_resolution: 'N/A' })

const topStats = computed(() => ([
  { label: 'Total Complaints', value: summary.value.total, icon: ClipboardList, bg: 'bg-blue-50', color: 'text-[#2563EB]' },
  { label: 'Assigned', value: summary.value.assigned, icon: Users, bg: 'bg-purple-50', color: 'text-purple-500' },
  { label: 'In Progress', value: summary.value.in_progress, icon: Clock, bg: 'bg-amber-50', color: 'text-amber-500' },
  { label: 'Resolved', value: summary.value.resolved, icon: CheckCircle, bg: 'bg-green-50', color: 'text-[#22C55E]' },
  { label: 'Emergency', value: summary.value.emergency, icon: Zap, bg: 'bg-red-50', color: 'text-red-500' },
  { label: 'Avg. Resol. Time', value: summary.value.avg_resolution, icon: Clock, bg: 'bg-slate-100', color: 'text-slate-600' },
]))

let searchDebounce = null
const fetchComplaints = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/complaints`, {
      ...authHeaders(),
      params: {
        search: searchQuery.value || undefined,
        status: filters.status,
        priority: filters.priority,
      }
    })
    complaints.value = data.complaints
    summary.value = data.summary_stats
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load complaints.'
  } finally {
    isLoading.value = false
  }
}

watch(searchQuery, () => {
  clearTimeout(searchDebounce)
  searchDebounce = setTimeout(fetchComplaints, 300)
})
watch(() => [filters.status, filters.priority], fetchComplaints)

onMounted(fetchComplaints)

// Workers (for Assign modal)
const workers = ref([])
const workersLoading = ref(false)
const workerSearch = ref('')
const isAssigning = ref(false)
const isReturning = ref(false)
const returnRemark = ref('')

const filteredWorkers = computed(() => {
  if (!workerSearch.value) return workers.value
  const q = workerSearch.value.toLowerCase()
  return workers.value.filter(w => w.name.toLowerCase().includes(q))
})

const fetchWorkers = async () => {
  workersLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/workers`, authHeaders())
    workers.value = data.workers
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to load workers.'
  } finally {
    workersLoading.value = false
  }
}

// Visual Helpers
const statusColor = (status) => {
  const map = {
    'Assigned': 'bg-purple-100 text-purple-700',
    'In Progress': 'bg-amber-100 text-amber-700',
    'Resolved': 'bg-green-100 text-green-700',
    'Closed': 'bg-slate-200 text-slate-600'
  }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const priorityColor = (priority) => {
  const map = {
    'Emergency': 'bg-red-100 text-red-700 border border-red-200',
    'High': 'bg-orange-100 text-orange-700 border border-orange-200',
    'Medium': 'bg-blue-100 text-blue-700 border border-blue-200',
    'Low': 'bg-slate-100 text-slate-600 border border-slate-200'
  }
  return map[priority]
}

const openModal = (type, complaint) => {
  activeComplaint.value = complaint
  activeModal.value = type
  modalError.value = ''
  returnRemark.value = ''
  if (type === 'assign') {
    workerSearch.value = ''
    fetchWorkers()
  }
}

const closeModal = () => {
  activeModal.value = null
  activeComplaint.value = {}
}

const assignWorker = async (workerId) => {
  isAssigning.value = true
  modalError.value = ''
  try {
    await axios.patch(
      `${API_BASE}/complaints/${activeComplaint.value.rawId}/assign-worker`,
      { worker_id: workerId },
      authHeaders()
    )
    closeModal()
    await fetchComplaints()
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to assign worker.'
  } finally {
    isAssigning.value = false
  }
}

const returnToAdmin = async () => {
  if (!returnRemark.value.trim()) return
  isReturning.value = true
  modalError.value = ''
  try {
    await axios.patch(
      `${API_BASE}/complaints/${activeComplaint.value.rawId}/return-to-admin`,
      { remark: returnRemark.value },
      authHeaders()
    )
    closeModal()
    await fetchComplaints()
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to send complaint back.'
  } finally {
    isReturning.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Custom Scrollbar */
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