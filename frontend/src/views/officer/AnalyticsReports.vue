<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1600px] mx-auto space-y-6">
          
          <!-- Header -->
          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Analytics & Reports</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Analytics & Reports</h1>
              <p class="text-slate-500 mt-1">Trends and performance across the complaints assigned to you.</p>
            </div>
          </div>

          <div v-if="loadError" class="bg-red-50 border border-red-100 text-red-600 text-sm rounded-[14px] p-4 flex items-center justify-between">
            {{ loadError }} <button @click="fetchAnalytics" class="font-bold underline shrink-0 ml-4">Retry</button>
          </div>

          <!-- Global Filters -->
          <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 items-center z-10">
            <div class="flex items-center gap-2 text-slate-700 font-bold shrink-0">
              <Filter class="w-5 h-5 text-[#2563EB]" /> Filters
            </div>
            <div class="w-px h-8 bg-slate-200 hidden lg:block mx-2"></div>
            <div class="flex flex-wrap items-center gap-3 w-full">
              <select v-model="filters.date" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="quarter">Last 3 Months</option>
                <option value="year">This Year</option>
              </select>
              <select v-model="filters.category" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                <option value="all">All Categories</option>
                <option v-for="c in categoryOptions" :key="c" :value="c">{{ c }}</option>
              </select>
              <select v-model="filters.ward" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                <option value="all">All Wards</option>
                <option v-for="w in wardOptions" :key="w" :value="w">{{ w }}</option>
              </select>
            </div>
            <div class="flex gap-2 shrink-0 w-full lg:w-auto mt-2 lg:mt-0">
              <button @click="resetFilters" class="flex-1 lg:flex-none px-4 py-2 bg-slate-100 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-200 transition-colors">Reset</button>
            </div>
          </div>

          <div v-if="isLoading" class="text-center text-slate-400 py-16">Loading analytics…</div>

          <template v-else>
          <!-- Executive KPIs -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="kpi in kpiCards" :key="kpi.title" class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
              <div :class="`w-10 h-10 rounded-xl flex items-center justify-center mb-4 ${kpi.iconBg} ${kpi.iconColor} group-hover:scale-110 transition-transform`">
                <component :is="kpi.icon" class="w-5 h-5" />
              </div>
              <p class="text-3xl font-extrabold text-slate-900">{{ kpi.value }}</p>
              <p class="text-sm font-semibold text-slate-500 mt-1">{{ kpi.title }}</p>
              <p class="text-[11px] text-slate-400 mt-1">{{ kpi.desc }}</p>
            </div>
          </div>

          <!-- Charts Grid 1: Trends & Categories -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
              <div class="mb-6">
                <h3 class="font-bold text-slate-900">Complaint Volume Trend</h3>
                <p class="text-xs text-slate-500">Received vs. resolved, day by day, over the selected period</p>
              </div>
              <div class="h-[300px] w-full relative">
                <canvas v-if="trend.length" ref="trendChartRef"></canvas>
                <p v-else class="text-sm text-slate-400 text-center pt-24">No complaints in this period.</p>
              </div>
            </div>

            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
              <div class="mb-6">
                <h3 class="font-bold text-slate-900">Complaint Categories</h3>
                <p class="text-xs text-slate-500">Distribution within this period</p>
              </div>
              <div class="flex-1 relative min-h-[250px]">
                <canvas v-if="categoryBreakdown.length" ref="categoryChartRef"></canvas>
                <p v-else class="text-sm text-slate-400 text-center pt-16">No data yet.</p>
              </div>
            </div>
          </div>

          <!-- Charts Grid 2: Category performance & Ward status -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
              <div class="mb-6">
                <h3 class="font-bold text-slate-900">Resolution Rate by Category</h3>
                <p class="text-xs text-slate-500">% of complaints resolved, per category</p>
              </div>
              <div class="h-[280px] w-full relative">
                <canvas v-if="categoryPerformance.length" ref="categoryPerfChartRef"></canvas>
                <p v-else class="text-sm text-slate-400 text-center pt-16">No data yet.</p>
              </div>
            </div>

            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
              <div class="mb-6">
                <h3 class="font-bold text-slate-900">Complaint Status by Ward</h3>
                <p class="text-xs text-slate-500">Current lifecycle stage, grouped by ward</p>
              </div>
              <div class="h-[280px] w-full relative">
                <canvas v-if="wardStatus.length" ref="wardChartRef"></canvas>
                <p v-else class="text-sm text-slate-400 text-center pt-16">No ward data yet.</p>
              </div>
            </div>
          </div>

          <!-- Operational Insights & Aging -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <div class="lg:col-span-8 space-y-6">
              <!-- Emergency Monitor -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center justify-between bg-red-50/30">
                  <div class="flex items-center gap-2">
                    <AlertTriangle class="w-5 h-5 text-red-500" />
                    <h3 class="font-bold text-slate-900">Emergency Complaint Monitor</h3>
                  </div>
                  <span class="px-2.5 py-1 bg-red-100 text-red-700 text-xs font-bold rounded-full">{{ emergencyComplaints.length }} Active</span>
                </div>
                <div class="overflow-x-auto">
                  <table class="w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-slate-50 text-slate-500 font-medium">
                      <tr>
                        <th class="px-5 py-3">ID</th>
                        <th class="px-5 py-3">Category</th>
                        <th class="px-5 py-3">Area</th>
                        <th class="px-5 py-3">Assigned Worker</th>
                        <th class="px-5 py-3">Time Pending</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="emp in emergencyComplaints" :key="emp.id" class="hover:bg-slate-50">
                        <td class="px-5 py-3 font-mono font-medium text-slate-900">{{ emp.id }}</td>
                        <td class="px-5 py-3 font-medium text-slate-700">{{ emp.category }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ emp.area }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ emp.worker || 'Unassigned' }}</td>
                        <td class="px-5 py-3"><span class="text-red-600 font-bold">{{ emp.hoursPending }}h</span></td>
                      </tr>
                      <tr v-if="emergencyComplaints.length === 0">
                        <td colspan="5" class="px-5 py-6 text-center text-slate-500">No active emergencies right now.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Worker Leaderboard -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><Award class="w-5 h-5 text-amber-500" /> Worker Leaderboard</h3>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-5">
                  <div v-for="(worker, idx) in topWorkers" :key="worker.id" class="flex items-center gap-4 p-3 border border-slate-100 rounded-xl hover:bg-slate-50 transition-colors">
                    <div class="w-8 h-8 rounded-full bg-slate-100 text-slate-500 font-bold flex items-center justify-center text-sm shrink-0">#{{ idx + 1 }}</div>
                    <img :src="workerAvatar(worker)" class="w-12 h-12 rounded-full object-cover border border-slate-200 shrink-0" />
                    <div class="flex-1 min-w-0">
                      <p class="font-bold text-slate-900 text-sm truncate">{{ worker.name }}</p>
                      <p class="text-xs text-slate-500 truncate">{{ worker.avgRating ? worker.avgRating + ' ★ avg rating' : 'No ratings yet' }}</p>
                    </div>
                    <div class="text-right shrink-0">
                      <p class="font-bold text-[#22C55E] text-sm">{{ worker.completedTasks }}</p>
                      <p class="text-[10px] text-slate-400 font-medium">Tasks</p>
                    </div>
                  </div>
                  <p v-if="topWorkers.length === 0" class="text-sm text-slate-400 col-span-2 text-center py-4">No workers in your department yet.</p>
                </div>
              </div>
            </div>

            <div class="lg:col-span-4 space-y-6">
              
              <!-- Complaint Aging -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 mb-4">Open Complaint Aging</h3>
                <p class="text-xs text-slate-500 -mt-3 mb-4">Snapshot of currently open complaints, right now</p>
                <div class="space-y-3">
                  <div class="flex items-center justify-between p-3 rounded-lg bg-green-50 border border-green-100">
                    <span class="text-sm font-bold text-green-700">0 - 2 Days</span>
                    <span class="text-sm font-bold text-green-700">{{ aging['0-2'] ?? 0 }}</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-yellow-50 border border-yellow-100">
                    <span class="text-sm font-bold text-yellow-700">3 - 5 Days</span>
                    <span class="text-sm font-bold text-yellow-700">{{ aging['3-5'] ?? 0 }}</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-orange-50 border border-orange-100">
                    <span class="text-sm font-bold text-orange-700">6 - 10 Days</span>
                    <span class="text-sm font-bold text-orange-700">{{ aging['6-10'] ?? 0 }}</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-red-50 border border-red-100">
                    <span class="text-sm font-bold text-red-700">10+ Days (Overdue)</span>
                    <span class="text-sm font-bold text-red-700">{{ aging['10+'] ?? 0 }}</span>
                  </div>
                </div>
              </div>

              <!-- Citizen Satisfaction -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 flex flex-col items-center justify-center text-center">
                <h3 class="font-bold text-slate-900 mb-2 w-full text-left">Citizen Satisfaction</h3>
                <template v-if="ratingDistribution.total > 0">
                  <div class="my-4">
                    <span class="text-5xl font-extrabold text-slate-900">{{ kpis.citizenSatisfaction ?? '—' }}</span><span class="text-xl text-slate-400 font-bold">/5</span>
                  </div>
                  <p class="text-sm text-slate-500 font-medium mb-4">Based on {{ ratingDistribution.total }} review{{ ratingDistribution.total === 1 ? '' : 's' }}</p>
                  <div class="w-full space-y-2">
                    <div v-for="star in [5,4,3,2,1]" :key="star" class="flex items-center gap-3 text-xs">
                      <span class="w-8 text-right font-medium text-slate-600">{{ star }} <Star class="w-3 h-3 inline text-slate-400 fill-slate-400"/></span>
                      <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                        <div class="bg-[#22C55E] h-full" :style="`width: ${ratingPct(star)}%`"></div>
                      </div>
                      <span class="w-8 text-left text-slate-500">{{ ratingPct(star) }}%</span>
                    </div>
                  </div>
                </template>
                <p v-else class="text-sm text-slate-400 py-8">No feedback submitted yet this period.</p>
              </div>

            </div>
          </div>
          </template>

        </div>
      </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import axios from 'axios'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  Filter, AlertTriangle, Award, Star, CheckCircle, Clock, Users,
  BarChart3, Layers
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
const defaultAvatar = 'https://images.unsplash.com/photo-1607746882042-944635dfe10e?w=200&h=200&fit=crop'
const workerAvatar = (w) => w?.profilePhoto ? `http://127.0.0.1:5000${w.profilePhoto}` : defaultAvatar

const isSidebarOpen = ref(false)
const isLoading = ref(true)
const loadError = ref('')

const filters = reactive({ date: 'month', category: 'all', ward: 'all' })

const kpis = ref({})
const categoryOptions = ref([])
const wardOptions = ref([])
const trend = ref([])
const categoryBreakdown = ref([])
const categoryPerformance = ref([])
const wardStatus = ref([])
const emergencyComplaints = ref([])
const topWorkers = ref([])
const aging = ref({})
const ratingDistribution = ref({ counts: {}, total: 0 })

const ratingPct = (star) => {
  if (!ratingDistribution.value.total) return 0
  return Math.round(((ratingDistribution.value.counts[star] || 0) / ratingDistribution.value.total) * 100)
}

const kpiCards = computed(() => [
  { title: 'Total Complaints', value: kpis.value.totalComplaints ?? '—', icon: Layers, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]', desc: 'In selected period' },
  { title: 'Active Workers', value: kpis.value.activeWorkers ?? '—', icon: Users, iconBg: 'bg-indigo-50', iconColor: 'text-indigo-500', desc: 'Currently deployed' },
  { title: 'Resolution Rate', value: kpis.value.resolutionRate != null ? kpis.value.resolutionRate + '%' : '—', icon: CheckCircle, iconBg: 'bg-teal-50', iconColor: 'text-teal-500', desc: 'Resolved / total' },
  { title: 'Citizen Satisfaction', value: kpis.value.citizenSatisfaction != null ? kpis.value.citizenSatisfaction + '/5' : '—', icon: Star, iconBg: 'bg-yellow-50', iconColor: 'text-yellow-500', desc: 'Based on feedback' },
])

const resetFilters = () => {
  filters.date = 'month'
  filters.category = 'all'
  filters.ward = 'all'
}

const trendChartRef = ref(null)
const categoryChartRef = ref(null)
const categoryPerfChartRef = ref(null)
const wardChartRef = ref(null)
let trendChart, categoryChart, categoryPerfChart, wardChart

const destroyCharts = () => {
  [trendChart, categoryChart, categoryPerfChart, wardChart].forEach(c => c?.destroy())
}

const renderCharts = () => {
  destroyCharts()

  if (trendChartRef.value && trend.value.length) {
    trendChart = new Chart(trendChartRef.value, {
      type: 'line',
      data: {
        labels: trend.value.map(t => t.date.slice(5)),
        datasets: [
          { label: 'Received', data: trend.value.map(t => t.received), borderColor: '#2563EB', backgroundColor: 'rgba(37,99,235,0.1)', borderWidth: 2, fill: true, tension: 0.4 },
          { label: 'Resolved', data: trend.value.map(t => t.resolved), borderColor: '#22C55E', backgroundColor: 'transparent', borderWidth: 2, borderDash: [5, 5], tension: 0.4 },
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } },
        scales: { y: { beginAtZero: true, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } }
      }
    })
  }

  if (categoryChartRef.value && categoryBreakdown.value.length) {
    categoryChart = new Chart(categoryChartRef.value, {
      type: 'doughnut',
      data: {
        labels: categoryBreakdown.value.map(c => c.category),
        datasets: [{ data: categoryBreakdown.value.map(c => c.count), backgroundColor: ['#2563EB','#F59E0B','#22C55E','#8B5CF6','#EC4899','#06B6D4','#cbd5e1'], borderWidth: 0 }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom', labels: { boxWidth: 12 } } } }
    })
  }

  if (categoryPerfChartRef.value && categoryPerformance.value.length) {
    categoryPerfChart = new Chart(categoryPerfChartRef.value, {
      type: 'bar',
      data: {
        labels: categoryPerformance.value.map(c => c.category),
        datasets: [{ label: 'Resolution Rate (%)', data: categoryPerformance.value.map(c => c.resolutionRate), backgroundColor: '#2563EB', borderRadius: 4 }]
      },
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { max: 100, grid: { color: '#f1f5f9' } }, y: { grid: { display: false } } }
      }
    })
  }

  if (wardChartRef.value && wardStatus.value.length) {
    wardChart = new Chart(wardChartRef.value, {
      type: 'bar',
      data: {
        labels: wardStatus.value.map(w => w.ward),
        datasets: [
          { label: 'Resolved', data: wardStatus.value.map(w => w.Resolved), backgroundColor: '#22C55E' },
          { label: 'In Progress', data: wardStatus.value.map(w => w['In Progress']), backgroundColor: '#F59E0B' },
          { label: 'Pending', data: wardStatus.value.map(w => w.Pending), backgroundColor: '#EF4444' },
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } },
        scales: { x: { stacked: true, grid: { display: false } }, y: { stacked: true, grid: { color: '#f1f5f9' }, beginAtZero: true } }
      }
    })
  }
}

const fetchAnalytics = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/analytics`, {
      ...authHeaders(),
      params: { date: filters.date, category: filters.category, ward: filters.ward }
    })
    kpis.value = data.kpis
    categoryOptions.value = data.categoryOptions
    wardOptions.value = data.wardOptions
    trend.value = data.trend
    categoryBreakdown.value = data.categoryBreakdown
    categoryPerformance.value = data.categoryPerformance
    wardStatus.value = data.wardStatus
    emergencyComplaints.value = data.emergencyComplaints
    topWorkers.value = data.topWorkers
    aging.value = data.aging
    ratingDistribution.value = data.ratingDistribution

    await nextTick()
    renderCharts()
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load analytics.'
  } finally {
    isLoading.value = false
  }
}

watch(() => [filters.date, filters.category, filters.ward], fetchAnalytics)

onMounted(fetchAnalytics)
onUnmounted(destroyCharts)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>