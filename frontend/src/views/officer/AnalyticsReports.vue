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
              <p class="text-slate-500 mt-1">Monitor operations, analyze trends, evaluate performance, and generate reports.</p>
            </div>
            <div class="flex gap-2">
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-2 shadow-sm">
                <Download class="w-4 h-4 text-slate-500" /> Export PDF
              </button>
              <button class="px-4 py-2 bg-[#2563EB] text-white font-medium rounded-lg hover:bg-[#1E40AF] transition-colors flex items-center gap-2 shadow-sm">
                <Printer class="w-4 h-4" /> Print Dashboard
              </button>
            </div>
          </div>

          <!-- Global Filters -->
          <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 items-center z-10">
            <div class="flex items-center gap-2 text-slate-700 font-bold shrink-0">
              <Filter class="w-5 h-5 text-[#2563EB]" /> Global Filters
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
                <option value="garbage">Garbage</option>
                <option value="potholes">Potholes</option>
                <option value="streetlights">Streetlights</option>
              </select>
              <select v-model="filters.department" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                <option value="all">All Departments</option>
                <option value="electrical">Electrical</option>
                <option value="sanitation">Sanitation</option>
                <option value="roads">Road Maintenance</option>
              </select>
              <select v-model="filters.ward" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                <option value="all">All Wards</option>
                <option value="w1">Ward 1</option>
                <option value="w2">Ward 2</option>
                <option value="w3">Ward 3</option>
              </select>
            </div>
            <div class="flex gap-2 shrink-0 w-full lg:w-auto mt-2 lg:mt-0">
              <button @click="resetFilters" class="flex-1 lg:flex-none px-4 py-2 bg-slate-100 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-200 transition-colors">Reset</button>
              <button class="flex-1 lg:flex-none px-4 py-2 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] shadow-sm transition-colors">Apply Filters</button>
            </div>
          </div>

          <!-- Executive KPIs -->
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-4 gap-4">
            <div v-for="kpi in kpis" :key="kpi.title" class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
              <div class="flex justify-between items-start mb-4">
                <div :class="`w-10 h-10 rounded-xl flex items-center justify-center ${kpi.iconBg} ${kpi.iconColor} group-hover:scale-110 transition-transform`">
                  <component :is="kpi.icon" class="w-5 h-5" />
                </div>
                <div :class="`flex items-center gap-1 text-xs font-bold px-2 py-1 rounded-full ${kpi.trend > 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`">
                  <TrendingUp v-if="kpi.trend > 0" class="w-3 h-3" />
                  <TrendingDown v-else class="w-3 h-3" />
                  {{ Math.abs(kpi.trend) }}%
                </div>
              </div>
              <p class="text-3xl font-extrabold text-slate-900">{{ kpi.value }}</p>
              <p class="text-sm font-semibold text-slate-500 mt-1">{{ kpi.title }}</p>
              <p class="text-[11px] text-slate-400 mt-1">{{ kpi.desc }}</p>
            </div>
          </div>

          <!-- Charts Grid 1: Trends & Categories -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
              <div class="flex justify-between items-center mb-6">
                <div>
                  <h3 class="font-bold text-slate-900">Complaint Volume Trends</h3>
                  <p class="text-xs text-slate-500">Daily complaints over the selected period</p>
                </div>
                <select class="bg-slate-50 border border-slate-200 text-slate-700 text-xs rounded focus:ring-[#2563EB] px-2 py-1 outline-none">
                  <option>Daily</option><option>Weekly</option><option>Monthly</option>
                </select>
              </div>
              <div class="h-[300px] w-full relative">
                <canvas ref="trendChartRef"></canvas>
              </div>
            </div>

            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
              <div class="mb-6">
                <h3 class="font-bold text-slate-900">Complaint Categories</h3>
                <p class="text-xs text-slate-500">Distribution of civic issues</p>
              </div>
              <div class="flex-1 relative min-h-[250px]">
                <canvas ref="categoryChartRef"></canvas>
              </div>
            </div>
          </div>

          <!-- Charts Grid 2: Performance & Status -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
              <div class="mb-6">
                <h3 class="font-bold text-slate-900">Department Performance</h3>
                <p class="text-xs text-slate-500">Resolution efficiency across municipal departments</p>
              </div>
              <div class="h-[280px] w-full relative">
                <canvas ref="deptChartRef"></canvas>
              </div>
            </div>

            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
              <div class="mb-6">
                <h3 class="font-bold text-slate-900">Complaint Status Overview</h3>
                <p class="text-xs text-slate-500">Current lifecycle stage of all active complaints</p>
              </div>
              <div class="h-[280px] w-full relative">
                <canvas ref="statusChartRef"></canvas>
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
                        <th class="px-5 py-3">Action</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="emp in emergencyComplaints" :key="emp.id" class="hover:bg-slate-50">
                        <td class="px-5 py-3 font-mono font-medium text-slate-900">{{ emp.id }}</td>
                        <td class="px-5 py-3 font-medium text-slate-700">{{ emp.category }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ emp.area }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ emp.worker || 'Unassigned' }}</td>
                        <td class="px-5 py-3"><span class="text-red-600 font-bold">{{ emp.time }}</span></td>
                        <td class="px-5 py-3"><button class="text-[#2563EB] font-bold text-xs hover:underline">Escalate</button></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Worker Leaderboard -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><Award class="w-5 h-5 text-amber-500" /> Worker Performance Leaderboard</h3>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-5">
                  <div v-for="(worker, idx) in topWorkers" :key="worker.id" class="flex items-center gap-4 p-3 border border-slate-100 rounded-xl hover:bg-slate-50 transition-colors">
                    <div class="w-8 h-8 rounded-full bg-slate-100 text-slate-500 font-bold flex items-center justify-center text-sm shrink-0">#{{ idx + 1 }}</div>
                    <img :src="worker.avatar" class="w-12 h-12 rounded-full object-cover border border-slate-200 shrink-0" />
                    <div class="flex-1 min-w-0">
                      <p class="font-bold text-slate-900 text-sm truncate">{{ worker.name }}</p>
                      <p class="text-xs text-slate-500 truncate">{{ worker.dept }}</p>
                    </div>
                    <div class="text-right shrink-0">
                      <p class="font-bold text-[#22C55E] text-sm">{{ worker.score }}</p>
                      <p class="text-[10px] text-slate-400 font-medium">{{ worker.completed }} Tasks</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="lg:col-span-4 space-y-6">
              
              <!-- Quick Insights -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Activity class="w-5 h-5 text-[#2563EB]" /> Operational Insights</h3>
                <div class="space-y-4">
                  <div v-for="(insight, idx) in insights" :key="idx" class="flex items-start gap-3 p-3 bg-blue-50/50 rounded-lg border border-blue-100">
                    <component :is="insight.icon" class="w-4 h-4 mt-0.5 shrink-0" :class="insight.color" />
                    <p class="text-sm text-slate-700 leading-tight">{{ insight.text }}</p>
                  </div>
                </div>
              </div>

              <!-- Complaint Aging -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 mb-4">Complaint Aging Tracker</h3>
                <div class="space-y-3">
                  <div class="flex items-center justify-between p-3 rounded-lg bg-green-50 border border-green-100">
                    <span class="text-sm font-bold text-green-700">0 - 2 Days</span>
                    <span class="text-sm font-bold text-green-700">425</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-yellow-50 border border-yellow-100">
                    <span class="text-sm font-bold text-yellow-700">3 - 5 Days</span>
                    <span class="text-sm font-bold text-yellow-700">112</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-orange-50 border border-orange-100">
                    <span class="text-sm font-bold text-orange-700">6 - 10 Days</span>
                    <span class="text-sm font-bold text-orange-700">45</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-red-50 border border-red-100">
                    <span class="text-sm font-bold text-red-700">10+ Days (Overdue)</span>
                    <span class="text-sm font-bold text-red-700">18</span>
                  </div>
                </div>
              </div>

              <!-- Citizen Satisfaction -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 flex flex-col items-center justify-center text-center">
                <h3 class="font-bold text-slate-900 mb-2 w-full text-left">Citizen Satisfaction</h3>
                <div class="my-4">
                  <span class="text-5xl font-extrabold text-slate-900">4.6</span><span class="text-xl text-slate-400 font-bold">/5</span>
                </div>
                <div class="flex gap-1 mb-2">
                  <Star v-for="i in 5" :key="i" class="w-6 h-6 text-amber-400 fill-amber-400" />
                </div>
                <p class="text-sm text-slate-500 font-medium mb-4">Based on 1,240 reviews</p>
                <div class="w-full space-y-2">
                  <div class="flex items-center gap-3 text-xs">
                    <span class="w-8 text-right font-medium text-slate-600">5 <Star class="w-3 h-3 inline text-slate-400 fill-slate-400"/></span>
                    <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden"><div class="bg-[#22C55E] h-full" style="width: 70%"></div></div>
                    <span class="w-8 text-left text-slate-500">70%</span>
                  </div>
                  <div class="flex items-center gap-3 text-xs">
                    <span class="w-8 text-right font-medium text-slate-600">4 <Star class="w-3 h-3 inline text-slate-400 fill-slate-400"/></span>
                    <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden"><div class="bg-[#22C55E] h-full" style="width: 20%"></div></div>
                    <span class="w-8 text-left text-slate-500">20%</span>
                  </div>
                  <div class="flex items-center gap-3 text-xs">
                    <span class="w-8 text-right font-medium text-slate-600">3 <Star class="w-3 h-3 inline text-slate-400 fill-slate-400"/></span>
                    <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden"><div class="bg-amber-400 h-full" style="width: 6%"></div></div>
                    <span class="w-8 text-left text-slate-500">6%</span>
                  </div>
                  <div class="flex items-center gap-3 text-xs">
                    <span class="w-8 text-right font-medium text-slate-600">2 <Star class="w-3 h-3 inline text-slate-400 fill-slate-400"/></span>
                    <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden"><div class="bg-orange-400 h-full" style="width: 3%"></div></div>
                    <span class="w-8 text-left text-slate-500">3%</span>
                  </div>
                  <div class="flex items-center gap-3 text-xs">
                    <span class="w-8 text-right font-medium text-slate-600">1 <Star class="w-3 h-3 inline text-slate-400 fill-slate-400"/></span>
                    <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden"><div class="bg-red-500 h-full" style="width: 1%"></div></div>
                    <span class="w-8 text-left text-slate-500">1%</span>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Report Generator Section -->
          <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden mt-6">
            <div class="p-6 border-b border-slate-100 bg-slate-50/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2"><FileText class="w-5 h-5 text-[#2563EB]" /> Report Generator</h2>
                <p class="text-sm text-slate-500 mt-1">Generate official PDF, Excel, or CSV documents.</p>
              </div>
              <div class="flex gap-2">
                <button class="px-4 py-2 text-sm font-bold text-[#2563EB] bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors">Saved Templates</button>
              </div>
            </div>
            
            <div class="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div class="col-span-1 md:col-span-2 lg:col-span-1 space-y-4">
                <div>
                  <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Report Type</label>
                  <select class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                    <option>Complaint Summary Report</option>
                    <option>Department Performance</option>
                    <option>Worker Performance Report</option>
                    <option>Citizen Feedback Report</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Output Format</label>
                  <div class="flex gap-3">
                    <label class="flex-1 border border-slate-200 rounded-lg p-2.5 flex items-center justify-center gap-2 cursor-pointer hover:bg-slate-50 transition-colors">
                      <input type="radio" name="format" value="pdf" checked class="w-4 h-4 text-[#2563EB]" /> <span class="text-sm font-bold">PDF</span>
                    </label>
                    <label class="flex-1 border border-slate-200 rounded-lg p-2.5 flex items-center justify-center gap-2 cursor-pointer hover:bg-slate-50 transition-colors">
                      <input type="radio" name="format" value="excel" class="w-4 h-4 text-[#2563EB]" /> <span class="text-sm font-bold">Excel</span>
                    </label>
                  </div>
                </div>
              </div>
              
              <div class="col-span-1 md:col-span-2 lg:col-span-2 space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Date Range</label>
                    <select class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                      <option>This Month</option><option>Last Month</option><option>Custom Range</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Department</label>
                    <select class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                      <option>All Departments</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Area</label>
                    <select class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                      <option>All Areas</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Status Filter</label>
                    <select class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                      <option>All Statuses</option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="col-span-1 md:col-span-2 lg:col-span-1 flex flex-col justify-end gap-3 border-l border-slate-100 pl-0 lg:pl-6">
                <button class="w-full py-3 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2">
                  <Download class="w-4 h-4" /> Generate Report
                </button>
                <button class="w-full py-3 bg-white border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors flex items-center justify-center gap-2">
                  <Eye class="w-4 h-4" /> Preview
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  Filter, TrendingUp, TrendingDown, Download, Printer, AlertTriangle, 
  Award, Activity, Star, FileText, CheckCircle, Clock, Users,
  BarChart3, BadgeCheck, Eye, Layers
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)

const filters = reactive({
  date: 'month',
  category: 'all',
  department: 'all',
  ward: 'all'
})

const resetFilters = () => {
  filters.date = 'month'
  filters.category = 'all'
  filters.department = 'all'
  filters.ward = 'all'
}

// --- Data ---
const kpis = [
  { title: 'Total Complaints', value: '1,248', trend: 12, icon: Layers, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]', desc: 'Registered this month' },
  { title: 'Pending Complaints', value: '184', trend: -5, icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500', desc: 'Awaiting action' },
  { title: 'Resolved Complaints', value: '942', trend: 18, icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]', desc: 'Successfully closed' },
  { title: 'Avg. Resolution Time', value: '24h', trend: -10, icon: BarChart3, iconBg: 'bg-purple-50', iconColor: 'text-purple-500', desc: 'Across all departments' },
  { title: 'Emergency Reports', value: '14', trend: 2, icon: AlertTriangle, iconBg: 'bg-red-50', iconColor: 'text-red-500', desc: 'Critical priority' },
  { title: 'Active Workers', value: '64', trend: 0, icon: Users, iconBg: 'bg-indigo-50', iconColor: 'text-indigo-500', desc: 'Currently deployed' },
  { title: 'Resolution Rate', value: '88%', trend: 4, icon: BadgeCheck, iconBg: 'bg-teal-50', iconColor: 'text-teal-500', desc: 'Target > 85%' },
  { title: 'Citizen Satisfaction', value: '4.6/5', trend: 2, icon: Star, iconBg: 'bg-yellow-50', iconColor: 'text-yellow-500', desc: 'Based on feedback' },
]

const emergencyComplaints = [
  { id: 'CMP-8902', category: 'Water Leakage', area: 'Downtown Sector 4', worker: null, time: '2 Hrs' },
  { id: 'CMP-8915', category: 'Road Collapse', area: 'East Ward Highway', worker: 'Amit Singh', time: '4 Hrs' },
  { id: 'CMP-8933', category: 'Live Wire Drop', area: 'North Zone Park', worker: 'Rahul Verma', time: '1 Hr' },
]

const topWorkers = [
  { id: 1, name: 'Suresh Patil', dept: 'Sanitation', score: 98, completed: 142, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=100' },
  { id: 2, name: 'Rajesh Kumar', dept: 'Roads', score: 95, completed: 118, avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=100' },
  { id: 3, name: 'Priya Sharma', dept: 'Water Supply', score: 92, completed: 95, avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=100' },
  { id: 4, name: 'Amit Singh', dept: 'Electrical', score: 89, completed: 88, avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&q=80&w=100' },
]

const insights = [
  { text: 'Garbage complaints in East Ward increased by 15% this week.', icon: TrendingUp, color: 'text-amber-500' },
  { text: 'Electrical Department improved average resolution time by 4 hours.', icon: TrendingDown, color: 'text-green-500' },
  { text: 'Ward 5 currently has the highest backlog of pending complaints.', icon: AlertTriangle, color: 'text-red-500' }
]

// --- Charts Setup ---
const trendChartRef = ref(null)
const categoryChartRef = ref(null)
const deptChartRef = ref(null)
const statusChartRef = ref(null)

let trendChart, categoryChart, deptChart, statusChart

onMounted(() => {
  // 1. Trend Line Chart
  if (trendChartRef.value) {
    trendChart = new Chart(trendChartRef.value, {
      type: 'line',
      data: {
        labels: ['1st', '5th', '10th', '15th', '20th', '25th', '30th'],
        datasets: [{
          label: 'Total Complaints',
          data: [65, 80, 55, 110, 95, 130, 115],
          borderColor: '#2563EB',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4
        }, {
          label: 'Resolved',
          data: [45, 60, 40, 90, 85, 110, 105],
          borderColor: '#22C55E',
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } },
        scales: {
          y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
          x: { grid: { display: false } }
        }
      }
    })
  }

  // 2. Category Donut Chart
  if (categoryChartRef.value) {
    categoryChart = new Chart(categoryChartRef.value, {
      type: 'doughnut',
      data: {
        labels: ['Garbage', 'Potholes', 'Lighting', 'Drainage', 'Other'],
        datasets: [{
          data: [35, 25, 20, 15, 5],
          backgroundColor: ['#2563EB', '#F59E0B', '#22C55E', '#8B5CF6', '#cbd5e1'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: { legend: { position: 'bottom', labels: { boxWidth: 12 } } }
      }
    })
  }

  // 3. Department Performance Bar Chart
  if (deptChartRef.value) {
    deptChart = new Chart(deptChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Roads', 'Sanitation', 'Electrical', 'Water', 'Drainage'],
        datasets: [{
          label: 'Resolution Rate (%)',
          data: [82, 95, 88, 76, 85],
          backgroundColor: '#2563EB',
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { max: 100, grid: { color: '#f1f5f9' } },
          y: { grid: { display: false } }
        }
      }
    })
  }

  // 4. Status Stacked Chart
  if (statusChartRef.value) {
    statusChart = new Chart(statusChartRef.value, {
      type: 'bar',
      data: {
        labels: ['W1', 'W2', 'W3', 'W4', 'W5'],
        datasets: [
          { label: 'Resolved', data: [40, 50, 30, 60, 45], backgroundColor: '#22C55E' },
          { label: 'In Progress', data: [15, 20, 10, 25, 15], backgroundColor: '#F59E0B' },
          { label: 'Pending', data: [5, 10, 5, 8, 12], backgroundColor: '#EF4444' }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } },
        scales: {
          x: { stacked: true, grid: { display: false } },
          y: { stacked: true, grid: { color: '#f1f5f9' } }
        }
      }
    })
  }
})

onUnmounted(() => {
  if (trendChart) trendChart.destroy()
  if (categoryChart) categoryChart.destroy()
  if (deptChart) deptChart.destroy()
  if (statusChart) statusChart.destroy()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>