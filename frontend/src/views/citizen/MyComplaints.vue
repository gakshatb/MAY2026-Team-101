<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Reusable Sidebar -->
    <Sidebar userRole="Citizen" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
      <!-- Reusable Dashboard Navbar -->
      <DashboardNavbar 
        userRole="Citizen" 
        :user="currentUser"
        pageTitle="My Complaints"
        breadcrumb="My Complaints"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
      />

      <!-- Main Scrollable Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto space-y-8">
          
          <!-- Statistics Section -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div v-for="stat in stats" :key="stat.title" class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4 transition-all hover:shadow-md">
              <div :class="['p-3 rounded-xl', stat.bgClass]">
                <component :is="stat.icon" :class="['w-6 h-6', stat.textClass]" />
              </div>
              <div>
                <p class="text-sm font-medium text-slate-500">{{ stat.title }}</p>
                <p class="text-2xl font-bold text-slate-900">{{ stat.count }}</p>
              </div>
            </div>
          </div>

          <!-- Filters Section -->
          <div class="flex flex-col lg:flex-row gap-4 justify-between items-start lg:items-center bg-white p-4 rounded-[14px] shadow-sm border border-slate-100">
            <div class="relative w-full lg:w-96">
              <Search class="w-5 h-5 text-slate-400 absolute left-3 top-3" />
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Search complaints..." 
                class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"
              />
            </div>
            <div class="flex flex-wrap gap-3 w-full lg:w-auto">
              <select v-model="filterStatus" class="px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none">
                <option value="All">All Statuses</option>
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
              </select>
              <button @click="$router.push('/citizen/submit')" class="flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] text-white text-sm font-medium rounded-lg hover:bg-[#1E40AF] transition-colors">
                <Plus class="w-4 h-4" /> Submit Complaint
              </button>
            </div>
          </div>

          <!-- Complaints Table / List -->
          <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
            
            <!-- Desktop Table -->
            <div class="hidden md:block overflow-x-auto">
              <table class="w-full text-left text-sm text-slate-600">
                <thead class="bg-slate-50 text-slate-700 font-bold uppercase text-[11px] tracking-wider">
                  <tr>
                    <th class="px-6 py-4">Complaint ID</th>
                    <th class="px-6 py-4">Title</th>
                    <th class="px-6 py-4">Category</th>
                    <th class="px-6 py-4">Priority</th>
                    <th class="px-6 py-4">Status</th>
                    <th class="px-6 py-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="c in filteredComplaints" :key="c.id" class="hover:bg-slate-50 transition-colors">
                    <td class="px-6 py-4 font-medium text-slate-900">{{ c.id }}</td>
                    <td class="px-6 py-4 font-semibold text-slate-900">{{ c.title }}</td>
                    <td class="px-6 py-4 text-slate-500">{{ c.category }}</td>
                    <td class="px-6 py-4">
                      <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase', priorityColors(c.priority)]">
                        {{ c.priority }}
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase', statusColors(c.status)]">
                        {{ c.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 text-right">
                      <button @click="$router.push(`/citizen/complaintdetails/${c.rawId}`)" class="text-[#2563EB] font-medium hover:underline text-sm">View Details</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Mobile Cards -->
            <div class="md:hidden divide-y divide-slate-100">
              <div v-for="c in filteredComplaints" :key="c.id" class="p-4 space-y-3">
                <div class="flex justify-between items-start">
                  <p class="font-bold text-slate-900">{{ c.title }}</p>
                  <span :class="['px-2 py-0.5 rounded text-[10px] font-bold', statusColors(c.status)]">{{ c.status }}</span>
                </div>
                <p class="text-xs text-slate-500">ID: {{ c.id }} | {{ c.category }}</p>
                <button @click="$router.push(`/citizen/complaintdetails/${c.rawId}`)" class="w-full py-2 bg-slate-50 rounded-lg text-sm font-medium text-slate-700">View Details</button>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredComplaints.length === 0" class="p-16 text-center">
              <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Inbox class="w-8 h-8 text-slate-400" />
              </div>
              <h3 class="text-lg font-bold text-slate-900">No complaints submitted</h3>
              <p class="text-slate-500 mb-6 mt-1">Get started by reporting your first civic issue.</p>
              <button @click="$router.push('/citizen/submit')" class="px-6 py-2.5 bg-[#2563EB] text-white rounded-lg text-sm font-medium hover:bg-[#1E40AF]">
                Submit Complaint
              </button>
            </div>
          </div>

          <!-- Pagination -->
          <div class="flex items-center justify-between text-sm text-slate-500">
            <p>Showing 1-{{ filteredComplaints.length }} of {{ complaints.length }} results</p>
            <div class="flex gap-2">
              <button class="px-4 py-2 border border-slate-200 rounded-lg bg-white disabled:opacity-50">Prev</button>
              <button class="px-4 py-2 border border-slate-200 rounded-lg bg-white">Next</button>
            </div>
          </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../../components/dashboard/Sidebar.vue'
import DashboardNavbar from '../../components/dashboard/DashboardNavbar.vue'
import { 
  ClipboardList, Search, Bell, AlertTriangle, 
  CheckCircle, Clock, Plus, Inbox 
} from 'lucide-vue-next'

const router      = useRouter()
const isSidebarOpen = ref(false)
const currentUser = computed(() => {
  const stored = localStorage.getItem('user')
  return stored ? JSON.parse(stored) : null
})
const isLoading   = ref(true)
const searchQuery = ref('')
const filterStatus = ref('All')

const complaints = ref([])
const stats = ref([
  { title: 'Total',       count: 0, icon: ClipboardList, bgClass: 'bg-blue-50',  textClass: 'text-[#2563EB]' },
  { title: 'Pending',     count: 0, icon: Clock,         bgClass: 'bg-amber-50', textClass: 'text-amber-600' },
  { title: 'In Progress', count: 0, icon: AlertTriangle, bgClass: 'bg-blue-50',  textClass: 'text-[#2563EB]' },
  { title: 'Resolved',    count: 0, icon: CheckCircle,   bgClass: 'bg-green-50', textClass: 'text-[#22C55E]' },
])

const filteredComplaints = computed(() => complaints.value)

const fetchComplaints = async () => {
  isLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const params = {}
    if (filterStatus.value !== 'All')  params.status = filterStatus.value
    if (searchQuery.value.trim())      params.search = searchQuery.value.trim()

    const [{ data }, { data: summaryData }] = await Promise.all([
      axios.get('http://127.0.0.1:5000/api/citizen/complaints', {
        headers: { Authorization: `Bearer ${token}` }, params
      }),
      axios.get('http://127.0.0.1:5000/api/citizen/complaints/summary', {
        headers: { Authorization: `Bearer ${token}` }
      })
    ])
    complaints.value = data.complaints.map(c => ({
      id: c.id, rawId: c.raw_id,
      title: c.title, category: c.category,
      status: c.status, priority: c.priority,
    }))
    stats.value[0].count = summaryData.summary.total
    stats.value[1].count = summaryData.summary.pending
    stats.value[2].count = summaryData.summary.in_progress
    stats.value[3].count = summaryData.summary.resolved
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
  } finally { isLoading.value = false }
}

let searchTimer = null
watch(searchQuery, () => { clearTimeout(searchTimer); searchTimer = setTimeout(fetchComplaints, 400) })
watch(filterStatus, fetchComplaints)
onMounted(fetchComplaints)

const statusColors = (status) => {
  switch(status) {
    case 'Resolved': return 'bg-green-50 text-green-700'
    case 'In Progress': return 'bg-blue-50 text-blue-700'
    case 'Pending': return 'bg-amber-50 text-amber-700'
    default: return 'bg-slate-100 text-slate-700'
  }
}

const priorityColors = (priority) => {
  switch(priority) {
    case 'Emergency': return 'bg-red-50 text-red-700'
    case 'High': return 'bg-orange-50 text-orange-700'
    case 'Medium': return 'bg-blue-50 text-blue-700'
    default: return 'bg-slate-100 text-slate-700'
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>