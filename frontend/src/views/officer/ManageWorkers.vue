<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1600px] mx-auto space-y-6">
          
          <!-- Header & Breadcrumbs -->
          <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Manage Workers</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Manage Workers</h1>
              <p class="text-slate-500 mt-1">Monitor workforce, track assignments, and manage field operations.</p>
            </div>
          </div>

          <div v-if="loadError" class="bg-red-50 border border-red-100 text-red-600 text-sm rounded-[14px] p-4 flex items-center justify-between">
            {{ loadError }} <button @click="fetchWorkers" class="font-bold underline shrink-0 ml-4">Retry</button>
          </div>

          <!-- Statistics Cards Grid -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div v-for="stat in statistics" :key="stat.title" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition-shadow">
              <div :class="`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor} mb-2`">
                <component :is="stat.icon" class="w-4 h-4" />
              </div>
              <div>
                <p class="text-xl font-bold text-slate-900">{{ stat.value }}</p>
                <p class="text-[11px] font-medium text-slate-500 mt-0.5 leading-tight">{{ stat.title }}</p>
              </div>
            </div>
          </div>

          <!-- Search & Filters Toolbar -->
          <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col xl:flex-row gap-4 justify-between items-center z-10">
            <div class="relative w-full xl:w-96 shrink-0">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input 
                v-model="filters.search"
                type="text" 
                placeholder="Search by name or ID..." 
                class="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
            
            <div class="flex flex-wrap items-center justify-end gap-3 w-full">
              <select v-model="filters.availability" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2.5 outline-none">
                <option value="All">All Statuses</option>
                <option value="Busy">Busy Now</option>
                <option value="Available">Available Now</option>
                <option value="suspended">Suspended</option>
              </select>

              <select v-model="filters.sort" class="bg-white border border-slate-300 text-slate-900 font-medium text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2.5 outline-none shadow-sm">
                <option value="Name">Sort by: Name</option>
                <option value="Completed">Sort by: Tasks Completed</option>
                <option value="Rating">Sort by: Rating</option>
                <option value="Active">Sort by: Active Tasks</option>
              </select>
            </div>
          </div>

          <div v-if="isLoading" class="text-center text-slate-400 py-16">Loading workers…</div>

          <template v-else>
          <!-- Worker Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div v-for="worker in filteredWorkers" :key="worker.id" class="bg-white rounded-[14px] shadow-sm border border-slate-100 hover:shadow-lg transition-all duration-300 flex flex-col overflow-hidden group">
              <div class="p-5 flex-1">
                <div class="flex justify-between items-start mb-4">
                  <div class="flex items-center gap-3">
                    <img :src="workerAvatar(worker)" class="w-14 h-14 rounded-full object-cover border-2 border-slate-100" />
                    <div>
                      <h3 class="font-bold text-slate-900 leading-tight">{{ worker.name }}</h3>
                      <p class="text-xs font-mono text-slate-500">{{ worker.empId }}</p>
                    </div>
                  </div>
                  <span :class="`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${availabilityBadge(availability(worker))}`">{{ availability(worker) }}</span>
                </div>
                
                <div class="grid grid-cols-2 gap-y-3 gap-x-2 text-xs mb-4">
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Department</span>
                    <span class="text-slate-700 font-semibold truncate">{{ worker.department || '—' }}</span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Rating</span>
                    <span class="text-amber-500 font-bold flex items-center gap-1">
                      <Star class="w-3 h-3 fill-amber-500"/> {{ worker.avgRating ?? '—' }}
                    </span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Completed</span>
                    <span class="text-slate-700 font-semibold">{{ worker.completedTasks }}</span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Avg Resolution</span>
                    <span class="text-slate-700 font-semibold">{{ worker.avgResolutionHours ? worker.avgResolutionHours + 'h' : '—' }}</span>
                  </div>
                </div>

                <div class="mb-2">
                  <div class="flex justify-between text-xs mb-1">
                    <span class="font-medium text-slate-500">Active Tasks</span>
                    <span class="font-bold text-slate-900">{{ worker.activeTasks }} in progress</span>
                  </div>
                  <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full rounded-full transition-all duration-500 bg-[#2563EB]" :style="`width: ${Math.min(100, worker.activeTasks * 25)}%`"></div>
                  </div>
                </div>
              </div>

              <div class="bg-slate-50 border-t border-slate-100 p-3 grid grid-cols-3 gap-2">
                <button @click="openDrawer(worker)" class="py-2 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors flex items-center justify-center gap-1.5 shadow-sm">
                  <Eye class="w-3.5 h-3.5" /> Profile
                </button>
                <button @click="openModal('assign', worker)" class="py-2 bg-[#2563EB] text-white text-xs font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex items-center justify-center gap-1.5 shadow-sm">
                  <Clipboard class="w-3.5 h-3.5" /> Assign
                </button>
                <button v-if="worker.accountStatus === 'active'" @click="openModal('deactivate', worker)" class="py-2 bg-red-50 text-red-600 text-xs font-bold rounded-lg hover:bg-red-100 transition-colors flex items-center justify-center gap-1.5 shadow-sm border border-red-100">
                  <UserX class="w-3.5 h-3.5" /> Suspend
                </button>
                <button v-else @click="reactivateWorker(worker)" class="py-2 bg-green-50 text-green-700 text-xs font-bold rounded-lg hover:bg-green-100 transition-colors flex items-center justify-center gap-1.5 shadow-sm border border-green-100">
                  <UserCheck class="w-3.5 h-3.5" /> Reactivate
                </button>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredWorkers.length === 0" class="bg-white p-12 rounded-[14px] border border-slate-100 text-center shadow-sm">
            <UserX class="w-12 h-12 text-slate-300 mx-auto mb-4" />
            <h3 class="text-lg font-bold text-slate-900 mb-1">No workers found</h3>
            <p class="text-slate-500 text-sm">Adjust your filters or search query to find workers.</p>
            <button @click="resetFilters" class="mt-4 px-4 py-2 bg-blue-50 text-[#2563EB] text-sm font-bold rounded-lg hover:bg-blue-100 transition-colors">Clear Filters</button>
          </div>

          <!-- Top Performers -->
          <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
            <div class="p-5 border-b border-slate-100 flex items-center justify-between">
              <h2 class="font-bold text-slate-900 flex items-center gap-2"><BadgeCheck class="w-5 h-5 text-[#2563EB]" /> Top Performers</h2>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm whitespace-nowrap">
                <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide">
                  <tr>
                    <th class="px-5 py-3">Worker</th>
                    <th class="px-5 py-3">Completed</th>
                    <th class="px-5 py-3">Avg Resolution</th>
                    <th class="px-5 py-3">Rating</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="perf in topPerformers" :key="perf.id" class="hover:bg-slate-50 transition-colors">
                    <td class="px-5 py-3 flex items-center gap-3">
                      <img :src="workerAvatar(perf)" class="w-8 h-8 rounded-full object-cover" />
                      <p class="font-bold text-slate-900 leading-none">{{ perf.name }}</p>
                    </td>
                    <td class="px-5 py-3 text-slate-700 font-medium">{{ perf.completedTasks }} Tasks</td>
                    <td class="px-5 py-3 text-slate-600">{{ perf.avgResolutionHours ? perf.avgResolutionHours + 'h' : '—' }}</td>
                    <td class="px-5 py-3">
                      <span v-if="perf.avgRating" class="px-2 py-1 bg-green-50 text-green-700 font-bold text-xs rounded-full">{{ perf.avgRating }} ★</span>
                      <span v-else class="text-slate-400 text-xs">No ratings yet</span>
                    </td>
                  </tr>
                  <tr v-if="topPerformers.length === 0">
                    <td colspan="4" class="px-5 py-6 text-center text-slate-500">No completed tasks yet.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          </template>

        </div>
      </main>

    <!-- Worker Profile Drawer -->
    <Teleport to="body">
      <div v-if="drawerOpen" class="fixed inset-0 z-50 bg-slate-900/30 backdrop-blur-sm flex justify-end animate-fade-in" @click="drawerOpen = false">
        <div class="w-full max-w-2xl bg-white h-full shadow-2xl flex flex-col transform transition-transform animate-slide-in" @click.stop>
          
          <div v-if="!activeWorker" class="p-12 text-center text-slate-400">Loading…</div>
          <template v-else>
          <div class="p-6 border-b border-slate-100 flex justify-between items-start bg-slate-50 shrink-0">
            <div class="flex items-center gap-5">
              <img :src="workerAvatar(activeWorker)" class="w-20 h-20 rounded-full object-cover border-4 border-white shadow-sm" />
              <div>
                <h2 class="text-2xl font-bold text-slate-900">{{ activeWorker.name }}</h2>
                <p class="text-sm text-slate-600 mb-2">{{ activeWorker.department || '—' }}</p>
                <div class="flex gap-2">
                  <span :class="`px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wider ${availabilityBadge(availability(activeWorker))}`">{{ availability(activeWorker) }}</span>
                  <span class="px-2.5 py-1 bg-slate-200 text-slate-700 rounded text-xs font-bold font-mono uppercase tracking-wider">{{ activeWorker.empId }}</span>
                </div>
              </div>
            </div>
            <button @click="drawerOpen = false" class="p-2 text-slate-400 hover:bg-slate-200 rounded-lg transition-colors"><X class="w-6 h-6"/></button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Completed</p>
                <p class="text-xl font-bold text-slate-900">{{ activeWorker.completedTasks }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Avg Rating</p>
                <p class="text-xl font-bold text-slate-900 flex items-center gap-1.5">
                  <Star class="w-5 h-5 text-amber-400 fill-amber-400"/> {{ activeWorker.avgRating ?? '—' }}
                </p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Avg Resolution</p>
                <p class="text-xl font-bold text-slate-900">{{ activeWorker.avgResolutionHours ? activeWorker.avgResolutionHours + 'h' : '—' }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Completion Rate</p>
                <p class="text-xl font-bold text-[#22C55E]">{{ activeWorker.completionRate != null ? activeWorker.completionRate + '%' : '—' }}</p>
              </div>
            </div>

            <div class="mb-8">
              <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><User class="w-4 h-4 text-slate-400" /> Contact & Info</h3>
              <div class="space-y-4 text-sm">
                <div class="flex items-center gap-3 text-slate-600"><Phone class="w-4 h-4 text-slate-400 shrink-0" /> {{ activeWorker.phone || '—' }}</div>
                <div class="flex items-center gap-3 text-slate-600"><Mail class="w-4 h-4 text-slate-400 shrink-0" /> {{ activeWorker.email }}</div>
                <div class="flex items-center gap-3 text-slate-600"><Calendar class="w-4 h-4 text-slate-400 shrink-0" /> Member since {{ activeWorker.memberSince || '—' }}</div>
              </div>
            </div>

            <div class="mb-8">
              <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Clipboard class="w-4 h-4 text-slate-400" /> Current Assignments</h3>
              <div class="overflow-x-auto border border-slate-100 rounded-xl">
                <table class="w-full text-left text-sm whitespace-nowrap">
                  <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide">
                    <tr>
                      <th class="px-4 py-3">ID</th>
                      <th class="px-4 py-3">Category</th>
                      <th class="px-4 py-3">Priority</th>
                      <th class="px-4 py-3">Status</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100">
                    <tr v-for="task in activeWorker.currentAssignments" :key="task.id" class="hover:bg-slate-50">
                      <td class="px-4 py-3 font-mono font-medium text-slate-900">{{ task.id }}</td>
                      <td class="px-4 py-3 text-slate-600">{{ task.category }}</td>
                      <td class="px-4 py-3"><span :class="`text-[10px] font-bold px-2 py-0.5 rounded ${priorityBadge(task.priority)}`">{{ task.priority }}</span></td>
                      <td class="px-4 py-3"><span :class="`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${statusBadgeColor(task.status)}`">{{ task.status }}</span></td>
                    </tr>
                    <tr v-if="!activeWorker.currentAssignments?.length">
                      <td colspan="4" class="px-4 py-6 text-center text-slate-500 font-medium">No active assignments</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div>
              <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Activity class="w-4 h-4 text-slate-400" /> Recent Activity</h3>
              <div v-if="activeWorker.recentActivity?.length" class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                <div v-for="(act, idx) in activeWorker.recentActivity" :key="idx" class="relative">
                  <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#2563EB] rounded-full ring-4 ring-white"></div>
                  <p class="text-sm font-bold text-slate-900">{{ act.action }}</p>
                  <p class="text-[11px] text-slate-500 mt-0.5 font-medium">{{ act.date }} • {{ act.complaintId }}</p>
                </div>
              </div>
              <p v-else class="text-sm text-slate-400">No activity yet.</p>
            </div>
          </div>
          
          <div class="p-6 border-t border-slate-100 bg-white grid grid-cols-1 shrink-0">
            <button @click="openModal('assign', activeWorker)" class="py-3 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm">Assign New Task</button>
          </div>
          </template>
        </div>
      </div>
    </Teleport>

    <!-- Modals (Teleported) -->
    <Teleport to="body">
      
      <!-- Assign Complaint Modal -->
      <div v-if="activeModal === 'assign'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-md shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Direct Assignment</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4">
            <div v-if="modalContextWorker" class="flex items-center gap-3 p-3 bg-blue-50 border border-blue-100 rounded-lg mb-4">
              <img :src="workerAvatar(modalContextWorker)" class="w-10 h-10 rounded-full object-cover" />
              <div>
                <p class="font-bold text-slate-900 text-sm leading-tight">Assigning to: {{ modalContextWorker.name }}</p>
                <p class="text-xs text-slate-600">{{ modalContextWorker.department }}</p>
              </div>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Complaint</label>
              <select v-model="assignForm.complaintId" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]">
                <option value="" disabled>Select an unassigned complaint…</option>
                <option v-for="c in unassignedComplaints" :key="c.rawId" :value="c.rawId">{{ c.id }} — {{ c.title }}</option>
              </select>
              <p v-if="unassignedComplaints.length === 0" class="text-xs text-amber-600 mt-1.5">No complaints awaiting a worker right now.</p>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Assignment Notes (Optional)</label>
              <textarea v-model="assignForm.notes" rows="3" placeholder="Add optional instructions..." class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]"></textarea>
            </div>
            <p v-if="assignError" class="text-red-600 text-xs">{{ assignError }}</p>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="closeModal" class="px-5 py-2.5 text-sm font-bold text-slate-600 hover:bg-slate-200 rounded-lg transition-colors">Cancel</button>
            <button @click="submitAssign" :disabled="!assignForm.complaintId || isAssigning" class="px-5 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg shadow-sm transition-colors disabled:opacity-50">
              {{ isAssigning ? 'Assigning…' : 'Assign Task' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Suspend Worker Modal -->
      <div v-if="activeModal === 'deactivate'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-red-50 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertTriangle class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">Suspend Worker?</h3>
            <p class="text-sm text-slate-600 mb-2">Are you sure you want to suspend <strong class="text-slate-900">{{ modalContextWorker?.name }}</strong>? They will not be able to receive new assignments.</p>
            <p v-if="deactivateError" class="text-red-600 text-xs mt-3">{{ deactivateError }}</p>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex gap-3">
            <button @click="closeModal" class="flex-1 py-2.5 text-sm font-bold text-slate-700 bg-white border border-slate-300 hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
            <button @click="confirmSuspend" :disabled="isSuspending" class="flex-1 py-2.5 text-sm font-bold text-white bg-red-600 hover:bg-red-700 rounded-lg shadow-sm transition-colors disabled:opacity-50">
              {{ isSuspending ? 'Suspending…' : 'Suspend' }}
            </button>
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
  Users, UserCheck, UserX, BadgeCheck, Clipboard, 
  Phone, Mail, Calendar, Clock, Star, Search, Eye, AlertTriangle, X, Activity, User
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
const defaultAvatar = 'https://images.unsplash.com/photo-1607746882042-944635dfe10e?w=200&h=200&fit=crop'

const isSidebarOpen = ref(false)
const isLoading = ref(true)
const loadError = ref('')
const drawerOpen = ref(false)
const activeModal = ref(null)
const activeWorker = ref(null)
const modalContextWorker = ref(null)

const workers = ref([])
const summary = ref({})
const unassignedComplaints = ref([])

const assignForm = reactive({ complaintId: '', notes: '' })
const isAssigning = ref(false)
const assignError = ref('')
const isSuspending = ref(false)
const deactivateError = ref('')

const filters = reactive({ search: '', availability: 'All', sort: 'Name' })

const workerAvatar = (w) => w?.profilePhoto ? `http://127.0.0.1:5000${w.profilePhoto}` : defaultAvatar

const availability = (w) => {
  if (w.accountStatus === 'suspended') return 'Suspended'
  return w.activeTasks > 0 ? 'Busy' : 'Available'
}

const statistics = computed(() => [
  { title: 'Total Workers', value: summary.value.total ?? '—', icon: Users, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Busy Now', value: summary.value.busyNow ?? '—', icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Suspended', value: summary.value.suspended ?? '—', icon: UserX, iconBg: 'bg-slate-100', iconColor: 'text-slate-500' },
  { title: 'Completed', value: summary.value.completedTotal ?? '—', icon: BadgeCheck, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'Active Tasks', value: summary.value.pendingTotal ?? '—', icon: Clipboard, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Avg Rating', value: summary.value.avgRating ?? '—', icon: Star, iconBg: 'bg-yellow-50', iconColor: 'text-yellow-500' },
])

const filteredWorkers = computed(() => {
  let result = workers.value.filter(w => {
    const matchSearch = !filters.search || w.name.toLowerCase().includes(filters.search.toLowerCase()) || w.empId.toLowerCase().includes(filters.search.toLowerCase())
    let matchAvail = true
    if (filters.availability === 'Busy') matchAvail = w.activeTasks > 0 && w.accountStatus === 'active'
    else if (filters.availability === 'Available') matchAvail = w.activeTasks === 0 && w.accountStatus === 'active'
    else if (filters.availability === 'suspended') matchAvail = w.accountStatus === 'suspended'
    return matchSearch && matchAvail
  })

  if (filters.sort === 'Name') result = [...result].sort((a, b) => a.name.localeCompare(b.name))
  if (filters.sort === 'Completed') result = [...result].sort((a, b) => b.completedTasks - a.completedTasks)
  if (filters.sort === 'Rating') result = [...result].sort((a, b) => (b.avgRating || 0) - (a.avgRating || 0))
  if (filters.sort === 'Active') result = [...result].sort((a, b) => b.activeTasks - a.activeTasks)

  return result
})

const topPerformers = computed(() =>
  [...workers.value].sort((a, b) => b.completedTasks - a.completedTasks).slice(0, 5)
)

const resetFilters = () => {
  filters.search = ''
  filters.availability = 'All'
}

const availabilityBadge = (status) => {
  if (status === 'Available') return 'bg-green-100 text-green-700'
  if (status === 'Busy') return 'bg-amber-100 text-amber-700'
  return 'bg-red-100 text-red-700'
}

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700', 'High': 'bg-orange-100 text-orange-700', 'Medium': 'bg-blue-100 text-blue-700', 'Low': 'bg-slate-100 text-slate-600' }
  return map[priority] || 'bg-slate-100 text-slate-600'
}

const statusBadgeColor = (status) => {
  const map = { 'Assigned': 'bg-purple-100 text-purple-700', 'In Progress': 'bg-amber-100 text-amber-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const fetchWorkers = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/workers`, authHeaders())
    workers.value = data.workers
    summary.value = data.summary
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load workers.'
  } finally {
    isLoading.value = false
  }
}

const fetchUnassignedComplaints = async () => {
  try {
    const { data } = await axios.get(`${API_BASE}/complaints`, { ...authHeaders(), params: { status: 'Assigned' } })
    unassignedComplaints.value = data.complaints
  } catch (err) {
    console.error(err)
  }
}

const openDrawer = async (worker) => {
  drawerOpen.value = true
  activeWorker.value = null
  try {
    const { data } = await axios.get(`${API_BASE}/workers/${worker.id}`, authHeaders())
    activeWorker.value = data.worker
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load worker details.'
    drawerOpen.value = false
  }
}

const openModal = (type, worker = null) => {
  modalContextWorker.value = worker
  activeModal.value = type
  assignError.value = ''
  deactivateError.value = ''
  if (type === 'assign') {
    assignForm.complaintId = ''
    assignForm.notes = ''
    fetchUnassignedComplaints()
  }
}

const closeModal = () => {
  activeModal.value = null
  modalContextWorker.value = null
}

const submitAssign = async () => {
  if (!assignForm.complaintId || !modalContextWorker.value) return
  isAssigning.value = true
  assignError.value = ''
  try {
    await axios.patch(`${API_BASE}/complaints/${assignForm.complaintId}/assign-worker`, {
      worker_id: modalContextWorker.value.id,
      notes: assignForm.notes,
    }, authHeaders())
    closeModal()
    await fetchWorkers()
    if (drawerOpen.value && activeWorker.value?.id === modalContextWorker.value.id) {
      await openDrawer(modalContextWorker.value)
    }
  } catch (err) {
    assignError.value = err.response?.data?.message || 'Failed to assign task.'
  } finally {
    isAssigning.value = false
  }
}

const confirmSuspend = async () => {
  if (!modalContextWorker.value) return
  isSuspending.value = true
  deactivateError.value = ''
  try {
    await axios.patch(`${API_BASE}/workers/${modalContextWorker.value.id}/status`, { status: 'suspended' }, authHeaders())
    closeModal()
    await fetchWorkers()
  } catch (err) {
    deactivateError.value = err.response?.data?.message || 'Failed to suspend worker.'
  } finally {
    isSuspending.value = false
  }
}

const reactivateWorker = async (worker) => {
  try {
    await axios.patch(`${API_BASE}/workers/${worker.id}/status`, { status: 'active' }, authHeaders())
    await fetchWorkers()
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to reactivate worker.'
  }
}

onMounted(fetchWorkers)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
.animate-fade-in { animation: fadeIn 0.2s ease-out forwards; }
.animate-slide-in { animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>