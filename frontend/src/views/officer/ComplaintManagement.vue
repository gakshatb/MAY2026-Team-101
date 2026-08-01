<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1400px] mx-auto space-y-6">
          
          <!-- Breadcrumb & Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <span class="hover:text-[#2563EB] cursor-pointer">Dashboard</span>
                <span class="mx-2">›</span>
                <span class="text-slate-900">Complaint Management</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Complaint Management</h1>
              <p class="text-slate-500 mt-1">Review, verify, assign, and monitor all citizen complaints.</p>
            </div>
            <div class="flex gap-3">
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-50 flex items-center gap-2 transition-colors">
                <BarChart class="w-4 h-4" /> Export Report
              </button>
            </div>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
            <div v-for="stat in summaryStats" :key="stat.label" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start mb-2">
                <div :class="`w-8 h-8 rounded-lg flex items-center justify-center ${stat.bg} ${stat.color}`">
                  <component :is="stat.icon" class="w-4 h-4" />
                </div>
                <span :class="`text-xs font-bold ${stat.trendColor}`">{{ stat.trend }}</span>
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
                <option value="Submitted">Submitted</option>
                <option value="Verified">Verified</option>
                <option value="Assigned">Assigned</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
              </select>

              <select v-model="filters.priority" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                <option value="All">All Priorities</option>
                <option value="Emergency">Emergency</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>

              <select v-model="filters.category" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                <option value="All">All Categories</option>
                <option value="Garbage">Garbage</option>
                <option value="Streetlight">Streetlight</option>
                <option value="Pothole">Pothole</option>
                <option value="Drainage">Drainage</option>
              </select>
            </div>
          </div>

          <!-- Bulk Actions (Appears when items are selected) -->
          <div v-if="selectedComplaints.length > 0" class="bg-[#2563EB]/10 border border-[#2563EB]/20 p-3 rounded-[14px] flex items-center justify-between animate-fade-in">
            <span class="text-sm font-bold text-[#1E40AF]">{{ selectedComplaints.length }} complaints selected</span>
            <div class="flex gap-2">
              <button class="px-3 py-1.5 bg-white text-sm font-medium text-slate-700 rounded border border-slate-200 hover:bg-slate-50 transition-colors">Assign Selected</button>
              <button class="px-3 py-1.5 bg-white text-sm font-medium text-slate-700 rounded border border-slate-200 hover:bg-slate-50 transition-colors">Change Priority</button>
              <button class="px-3 py-1.5 bg-red-50 text-sm font-medium text-red-600 rounded border border-red-100 hover:bg-red-100 transition-colors">Delete</button>
            </div>
          </div>

          <!-- Data Table -->
          <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm whitespace-nowrap">
                <thead class="bg-slate-50 text-slate-500 font-medium border-b border-slate-100">
                  <tr>
                    <th class="px-6 py-4"><input type="checkbox" @change="toggleAll" :checked="isAllSelected" class="rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" /></th>
                    <th class="px-6 py-4">Complaint ID</th>
                    <th class="px-6 py-4">Title & Citizen</th>
                    <th class="px-6 py-4">Category</th>
                    <th class="px-6 py-4">Status</th>
                    <th class="px-6 py-4">Priority</th>
                    <th class="px-6 py-4">Assigned To</th>
                    <th class="px-6 py-4">Date</th>
                    <th class="px-6 py-4 text-center">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="cmp in filteredComplaints" :key="cmp.id" class="hover:bg-slate-50 transition-colors group">
                    <td class="px-6 py-4">
                      <input type="checkbox" v-model="selectedComplaints" :value="cmp.id" class="rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                    </td>
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
                        <button @click="openDrawer(cmp)" class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded transition-colors" title="View Details">
                          <Eye class="w-4 h-4" />
                        </button>
                        <button @click="openModal('verify', cmp)" v-if="cmp.status === 'Submitted'" class="p-1.5 text-slate-400 hover:text-green-600 hover:bg-green-50 rounded transition-colors" title="Verify">
                          <CheckCircle class="w-4 h-4" />
                        </button>
                        <button @click="openModal('assign', cmp)" v-if="cmp.status === 'Verified'" class="p-1.5 text-slate-400 hover:text-purple-600 hover:bg-purple-50 rounded transition-colors" title="Assign Worker">
                          <Users class="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="filteredComplaints.length === 0">
                    <td colspan="9" class="px-6 py-12 text-center text-slate-500">
                      <Search class="w-8 h-8 text-slate-300 mx-auto mb-3" />
                      <p class="font-medium">No complaints found</p>
                      <p class="text-sm">Try adjusting your search or filters.</p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Simple Pagination -->
            <div class="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-slate-50">
              <span class="text-sm text-slate-500">Showing 1 to {{ filteredComplaints.length }} of {{ filteredComplaints.length }} entries</span>
              <div class="flex gap-1">
                <button class="px-3 py-1 bg-white border border-slate-200 rounded text-sm text-slate-400 cursor-not-allowed">Prev</button>
                <button class="px-3 py-1 bg-[#2563EB] border border-[#2563EB] rounded text-sm text-white">1</button>
                <button class="px-3 py-1 bg-white border border-slate-200 rounded text-sm text-slate-600 hover:bg-slate-50">Next</button>
              </div>
            </div>
          </div>

          <!-- Charts & Analytics (Visual representations only) -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-6">
            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
              <h3 class="font-bold text-slate-900 mb-4">Complaints by Category</h3>
              <div class="flex items-center gap-6">
                <!-- CSS Pie Chart Representation -->
                <div class="w-32 h-32 rounded-full border-4 border-slate-50" style="background: conic-gradient(#2563EB 0% 40%, #F59E0B 40% 70%, #22C55E 70% 90%, #EF4444 90% 100%);"></div>
                <div class="space-y-2 flex-1">
                  <div class="flex items-center justify-between text-sm"><span class="flex items-center gap-2"><div class="w-3 h-3 bg-[#2563EB] rounded"></div>Garbage</span><span class="font-bold">40%</span></div>
                  <div class="flex items-center justify-between text-sm"><span class="flex items-center gap-2"><div class="w-3 h-3 bg-[#F59E0B] rounded"></div>Potholes</span><span class="font-bold">30%</span></div>
                  <div class="flex items-center justify-between text-sm"><span class="flex items-center gap-2"><div class="w-3 h-3 bg-[#22C55E] rounded"></div>Lighting</span><span class="font-bold">20%</span></div>
                  <div class="flex items-center justify-between text-sm"><span class="flex items-center gap-2"><div class="w-3 h-3 bg-[#EF4444] rounded"></div>Drainage</span><span class="font-bold">10%</span></div>
                </div>
              </div>
            </div>

            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 lg:col-span-2">
              <h3 class="font-bold text-slate-900 mb-4">Area-wise Complaint Volume</h3>
              <div class="space-y-4">
                <div v-for="area in ['Downtown', 'North Zone', 'East Ward', 'South Suburbs']" :key="area" class="flex items-center gap-4">
                  <span class="text-sm font-medium text-slate-600 w-24 truncate">{{ area }}</span>
                  <div class="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-[#2563EB] rounded-full" :style="`width: ${Math.floor(Math.random() * 60) + 20}%`"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </main>

    <!-- Side Drawer: Complaint Details -->
    <div v-if="activeDrawer" class="fixed inset-0 z-40 bg-slate-900/20 backdrop-blur-sm flex justify-end" @click="activeDrawer = false">
      <div class="w-full max-w-md bg-white h-full shadow-2xl flex flex-col animate-slide-in" @click.stop>
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div>
            <h2 class="text-lg font-bold text-slate-900">Complaint Details</h2>
            <p class="text-sm text-slate-500 font-mono">{{ activeComplaint.id }}</p>
          </div>
          <button @click="activeDrawer = false" class="p-2 text-slate-400 hover:bg-slate-200 rounded-lg transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 space-y-8">
          
          <div class="flex gap-3">
            <span :class="`px-3 py-1 rounded-full text-xs font-bold ${statusColor(activeComplaint.status)}`">{{ activeComplaint.status }}</span>
            <span :class="`px-3 py-1 rounded text-xs font-bold ${priorityColor(activeComplaint.priority)}`">{{ activeComplaint.priority }} Priority</span>
          </div>

          <div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">{{ activeComplaint.title }}</h3>
            <p class="text-sm text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-lg border border-slate-100">
              Citizen reports a massive garbage accumulation near the central park entrance. The waste has not been collected for 4 days, causing hygiene issues and foul odor in the residential area.
            </p>
          </div>

          <div class="grid grid-cols-2 gap-y-4 text-sm">
            <div>
              <p class="text-slate-500 mb-1">Citizen</p>
              <p class="font-bold text-slate-900">{{ activeComplaint.citizen }}</p>
            </div>
            <div>
              <p class="text-slate-500 mb-1">Category</p>
              <p class="font-bold text-slate-900">{{ activeComplaint.category }}</p>
            </div>
            <div>
              <p class="text-slate-500 mb-1">Location</p>
              <p class="font-bold text-slate-900 flex items-center gap-1"><MapPin class="w-3 h-3 text-slate-400" /> {{ activeComplaint.area }}</p>
            </div>
            <div>
              <p class="text-slate-500 mb-1">Submitted</p>
              <p class="font-bold text-slate-900">{{ activeComplaint.date }}</p>
            </div>
          </div>

          <div>
            <p class="font-bold text-slate-900 mb-3">Evidence Attached</p>
            <div class="w-full h-40 bg-slate-100 rounded-lg border border-slate-200 overflow-hidden relative group">
              <img src="https://images.unsplash.com/photo-1528323273322-d81458248d40?auto=format&fit=crop&q=80&w=400" alt="Evidence" class="w-full h-full object-cover" />
            </div>
          </div>

          <!-- Vertical Timeline -->
          <div>
            <p class="font-bold text-slate-900 mb-4">Activity Timeline</p>
            <div class="relative pl-4 border-l-2 border-slate-200 space-y-6">
              <div class="relative">
                <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#2563EB] rounded-full ring-4 ring-white"></div>
                <p class="text-sm font-bold text-slate-900">Submitted by Citizen</p>
                <p class="text-xs text-slate-500">{{ activeComplaint.date }}</p>
              </div>
              <div class="relative" :class="{'opacity-50': activeComplaint.status === 'Submitted'}">
                <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#F59E0B] rounded-full ring-4 ring-white"></div>
                <p class="text-sm font-bold text-slate-900">Verified by Officer</p>
                <p class="text-xs text-slate-500" v-if="activeComplaint.status !== 'Submitted'">July 10, 2026</p>
              </div>
              <div class="relative opacity-50">
                <div class="absolute -left-[21px] w-2.5 h-2.5 bg-slate-300 rounded-full ring-4 ring-white"></div>
                <p class="text-sm font-bold text-slate-900">Assigned to Worker</p>
              </div>
            </div>
          </div>

        </div>
        
        <div class="p-6 border-t border-slate-100 bg-white grid grid-cols-2 gap-3">
          <button @click="openModal('priority', activeComplaint)" class="py-2.5 border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors">Change Priority</button>
          <button @click="openModal('assign', activeComplaint)" class="py-2.5 bg-[#2563EB] text-white font-medium rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm">Assign Worker</button>
        </div>
      </div>
    </div>

    <!-- Teleport Modals to Body for correct z-indexing -->
    <Teleport to="body">
      <!-- Verify Modal -->
      <div v-if="activeModal === 'verify'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl overflow-hidden">
          <div class="p-6 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Verify Complaint</h3>
            <button @click="activeModal = null" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4">
            <p class="text-sm text-slate-600">Review the details and approve the complaint for assignment, or reject it if invalid.</p>
            <textarea rows="3" placeholder="Add verification remarks (optional)..." class="w-full p-3 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"></textarea>
          </div>
          <div class="p-6 bg-slate-50 border-t border-slate-100 flex gap-3 justify-end">
            <button @click="activeModal = null" class="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg">Reject</button>
            <button @click="activeModal = null" class="px-4 py-2 text-sm font-medium text-white bg-[#22C55E] hover:bg-green-600 shadow-sm rounded-lg">Approve & Verify</button>
          </div>
        </div>
      </div>

      <!-- Assign Worker Modal -->
      <div v-if="activeModal === 'assign'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
          <div class="p-6 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Assign Field Worker</h3>
            <button @click="activeModal = null" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 bg-slate-50 border-b border-slate-100">
            <div class="relative">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input type="text" placeholder="Search available workers..." class="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
            </div>
          </div>
          <div class="max-h-64 overflow-y-auto p-2">
            <div v-for="worker in dummyWorkers" :key="worker.name" class="p-3 hover:bg-slate-50 rounded-lg flex items-center justify-between cursor-pointer border border-transparent hover:border-slate-200 transition-colors">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center font-bold text-slate-500">{{ worker.name.charAt(0) }}</div>
                <div>
                  <p class="font-bold text-slate-900 text-sm">{{ worker.name }}</p>
                  <p class="text-xs text-slate-500">{{ worker.dept }} • {{ worker.workload }} Active Tasks</p>
                </div>
              </div>
              <button class="px-3 py-1.5 bg-blue-50 text-[#2563EB] hover:bg-[#2563EB] hover:text-white text-xs font-bold rounded transition-colors">Assign</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  BarChart, Search, AlertTriangle, CheckCircle, 
  Eye, Users, MapPin, Clock, Building, User, X, Settings
} from 'lucide-vue-next'

// Core Layout State
const isSidebarOpen = ref(false)

// Data State
const searchQuery = ref('')
const selectedComplaints = ref([])
const activeDrawer = ref(false)
const activeModal = ref(null)
const activeComplaint = ref({})

const filters = reactive({
  status: 'All',
  priority: 'All',
  category: 'All'
})

// Mock Data
const summaryStats = [
  { label: 'Total Complaints', value: '1,248', trend: '+12%', trendColor: 'text-green-600', icon: BarChart, bg: 'bg-blue-50', color: 'text-[#2563EB]' },
  { label: 'Pending Verification', value: '42', trend: '+5', trendColor: 'text-amber-600', icon: Clock, bg: 'bg-amber-50', color: 'text-amber-500' },
  { label: 'Assigned', value: '156', trend: '-2', trendColor: 'text-slate-400', icon: Users, bg: 'bg-purple-50', color: 'text-purple-500' },
  { label: 'In Progress', value: '89', trend: '+14', trendColor: 'text-green-600', icon: Settings, bg: 'bg-blue-50', color: 'text-blue-500' },
  { label: 'Resolved', value: '840', trend: '+28', trendColor: 'text-green-600', icon: CheckCircle, bg: 'bg-green-50', color: 'text-[#22C55E]' },
  { label: 'Emergency', value: '12', trend: '+3', trendColor: 'text-red-600', icon: AlertTriangle, bg: 'bg-red-50', color: 'text-red-500' },
  { label: 'Avg. Resol. Time', value: '2.4d', trend: '-0.2d', trendColor: 'text-green-600', icon: Clock, bg: 'bg-slate-100', color: 'text-slate-600' }
]

const dummyWorkers = [
  { name: 'Rajesh Kumar', dept: 'Sanitation', workload: 2 },
  { name: 'Amit Singh', dept: 'Roads & Infra', workload: 5 },
  { name: 'Suresh Patil', dept: 'Electrical', workload: 1 },
  { name: 'Vijay Sharma', dept: 'Water Board', workload: 3 },
]

const complaints = ref([
  { id: 'CMP-2026-001', title: 'Overflowing Garbage Bin', citizen: 'Rahul Verma', category: 'Garbage', area: 'Downtown Sector 4', priority: 'High', status: 'Submitted', date: 'Jul 09, 2026', worker: null },
  { id: 'CMP-2026-002', title: 'Deep Pothole on Main Road', citizen: 'Priya Sharma', category: 'Pothole', area: 'MG Road', priority: 'Emergency', status: 'In Progress', date: 'Jul 08, 2026', worker: 'Amit Singh' },
  { id: 'CMP-2026-003', title: 'Broken Streetlight', citizen: 'Anil Kapoor', category: 'Streetlight', area: 'East Ward', priority: 'Low', status: 'Verified', date: 'Jul 07, 2026', worker: null },
  { id: 'CMP-2026-004', title: 'Blocked Drainage Tube', citizen: 'Sneha Patel', category: 'Drainage', area: 'North Zone', priority: 'Medium', status: 'Assigned', date: 'Jul 06, 2026', worker: 'Rajesh Kumar' },
  { id: 'CMP-2026-005', title: 'Public Park Bench Broken', citizen: 'Vikram Singh', category: 'Infrastructure', area: 'South Suburbs', priority: 'Low', status: 'Resolved', date: 'Jul 05, 2026', worker: 'Suresh Patil' },
])

// Computed Properties
const filteredComplaints = computed(() => {
  return complaints.value.filter(c => {
    const searchMatch = !searchQuery.value || 
      c.id.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
      c.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
      c.citizen.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const statusMatch = filters.status === 'All' || c.status === filters.status
    const priorityMatch = filters.priority === 'All' || c.priority === filters.priority
    const categoryMatch = filters.category === 'All' || c.category === filters.category

    return searchMatch && statusMatch && priorityMatch && categoryMatch
  })
})

const isAllSelected = computed(() => {
  return filteredComplaints.value.length > 0 && selectedComplaints.value.length === filteredComplaints.value.length
})

// Methods
const toggleAll = (e) => {
  if (e.target.checked) {
    selectedComplaints.value = filteredComplaints.value.map(c => c.id)
  } else {
    selectedComplaints.value = []
  }
}

const statusColor = (status) => {
  const map = {
    'Submitted': 'bg-slate-100 text-slate-700',
    'Verified': 'bg-blue-100 text-blue-700',
    'Assigned': 'bg-purple-100 text-purple-700',
    'In Progress': 'bg-amber-100 text-amber-700',
    'Resolved': 'bg-green-100 text-green-700'
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

const openDrawer = (complaint) => {
  activeComplaint.value = complaint
  activeDrawer.value = true
}

const openModal = (type, complaint) => {
  activeComplaint.value = complaint
  activeModal.value = type
  activeDrawer.value = false
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

.animate-slide-in {
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

/* Custom Scrollbar for Drawer & Main Area */
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