<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Sidebar -->
    <Sidebar userRole="Civic Officer" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      
      <!-- Navbar -->
      <DashboardNavbar userRole="Civic Officer" pageTitle="Dashboard" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Header Section -->
          <div class="flex flex-col lg:flex-row justify-between lg:items-end gap-4">
            <div>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Good Morning, Rahul Sharma</h1>
              <p class="text-slate-500 mt-1">Here's what's happening across your assigned departments today.</p>
            </div>
            
            <div class="flex flex-wrap items-center gap-4">
              <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <MapPin class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">Municipal HQ, Block A</span>
              </div>
              <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <Calendar class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">Thursday, July 09, 2026</span>
              </div>
            </div>
          </div>

          <!-- Top KPI Cards -->
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
            <div v-for="(kpi, idx) in kpiCards" :key="idx" class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 group relative overflow-hidden">
              <div class="flex justify-between items-start mb-2 relative z-10">
                <div :class="`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${kpi.bg} ${kpi.color}`">
                  <component :is="kpi.icon" class="w-4 h-4" />
                </div>
                <div :class="`flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${kpi.trend === 'up' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`">
                  <TrendingUp v-if="kpi.trend === 'up'" class="w-3 h-3" />
                  <TrendingDown v-else class="w-3 h-3" />
                  {{ kpi.percent }}
                </div>
              </div>
              <div class="relative z-10">
                <p class="text-xl lg:text-2xl font-extrabold text-slate-900">{{ kpi.value }}</p>
                <p class="text-[11px] font-semibold text-slate-500 mt-0.5 leading-tight">{{ kpi.title }}</p>
              </div>
              <!-- Mini Sparkline visual illusion -->
              <div class="absolute bottom-0 left-0 w-full h-8 opacity-10 group-hover:opacity-20 transition-opacity">
                <svg viewBox="0 0 100 20" preserveAspectRatio="none" class="w-full h-full" :class="kpi.color">
                  <path d="M0,20 Q25,5 50,15 T100,0 L100,20 Z" fill="currentColor"></path>
                </svg>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Main Column (8 cols) -->
            <div class="lg:col-span-8 space-y-6">
              
              <!-- Today's Overview Banner -->
              <div class="bg-gradient-to-r from-[#1E40AF] to-[#2563EB] rounded-2xl p-6 text-white shadow-md relative overflow-hidden">
                <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
                <h2 class="text-lg font-bold mb-4 flex items-center gap-2"><Activity class="w-5 h-5" /> Today's Overview</h2>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Received</p>
                    <p class="text-xl font-bold">142</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Resolved</p>
                    <p class="text-xl font-bold">89</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Active Workers</p>
                    <p class="text-xl font-bold">54</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Pending Assign.</p>
                    <p class="text-xl font-bold">28</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10 border-red-400/50">
                    <p class="text-xs text-red-100 font-medium mb-1">Emergencies</p>
                    <p class="text-xl font-bold text-red-200">3</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Feedback Rx</p>
                    <p class="text-xl font-bold">45</p>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button v-for="action in quickActions" :key="action.title" class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all group text-left flex flex-col items-start">
                  <div class="w-10 h-10 rounded-xl bg-slate-50 group-hover:bg-blue-50 text-slate-500 group-hover:text-[#2563EB] flex items-center justify-center mb-3 transition-colors">
                    <component :is="action.icon" class="w-5 h-5" />
                  </div>
                  <h3 class="font-bold text-slate-900 text-sm mb-1">{{ action.title }}</h3>
                  <p class="text-xs text-slate-500">{{ action.desc }}</p>
                </button>
              </div>

              <!-- Charts: Trend & Status -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex flex-col">
                  <div class="flex justify-between items-center mb-4">
                    <h3 class="font-bold text-slate-900">Complaint Trends</h3>
                    <select class="bg-slate-50 border border-slate-200 text-slate-700 text-xs rounded-lg focus:ring-[#2563EB] px-2 py-1 outline-none">
                      <option>Daily</option><option>Weekly</option><option>Monthly</option>
                    </select>
                  </div>
                  <div class="flex-1 relative min-h-[250px] w-full">
                    <canvas ref="trendChartRef"></canvas>
                  </div>
                </div>
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex flex-col">
                  <h3 class="font-bold text-slate-900 mb-4">Status Overview</h3>
                  <div class="flex-1 relative min-h-[250px] w-full flex items-center justify-center">
                    <canvas ref="statusChartRef"></canvas>
                  </div>
                </div>
              </div>

              <!-- Emergency Complaints -->
              <div class="bg-white rounded-2xl shadow-sm border border-red-200 overflow-hidden">
                <div class="bg-red-50 px-5 py-3 border-b border-red-100 flex items-center justify-between">
                  <h3 class="font-bold text-red-700 flex items-center gap-2">
                    <div class="relative flex h-3 w-3"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span><span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span></div>
                    Emergency Complaints
                  </h3>
                  <button class="text-xs font-bold text-red-600 hover:underline">View All</button>
                </div>
                <div class="divide-y divide-slate-100">
                  <div v-for="em in emergencyCases" :key="em.id" class="p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50 transition-colors">
                    <div class="flex gap-4">
                      <div class="w-12 h-12 rounded-xl bg-red-100 text-red-600 flex items-center justify-center shrink-0">
                        <AlertTriangle class="w-6 h-6" />
                      </div>
                      <div>
                        <div class="flex items-center gap-2">
                          <p class="font-bold text-slate-900">{{ em.category }}</p>
                          <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-700 uppercase tracking-wider">{{ em.id }}</span>
                        </div>
                        <p class="text-sm text-slate-600 mt-1 flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-slate-400"/> {{ em.area }}</p>
                      </div>
                    </div>
                    <div class="flex flex-wrap items-center gap-3">
                      <div class="text-right hidden md:block mr-4">
                        <p class="text-xs text-slate-500 font-medium">Time Received</p>
                        <p class="text-sm font-bold text-slate-900">{{ em.time }}</p>
                      </div>
                      <button class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg shadow-sm transition-colors w-full md:w-auto">Open Case</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Recent Complaints Table -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center justify-between">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><ClipboardList class="w-5 h-5 text-[#2563EB]" /> Recent Complaints</h3>
                  <button class="text-sm font-medium text-[#2563EB] hover:underline">View Pipeline</button>
                </div>
                <div class="overflow-x-auto">
                  <table class="w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wider">
                      <tr>
                        <th class="px-5 py-3">ID</th>
                        <th class="px-5 py-3">Citizen & Area</th>
                        <th class="px-5 py-3">Category</th>
                        <th class="px-5 py-3">Priority</th>
                        <th class="px-5 py-3">Status</th>
                        <th class="px-5 py-3 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="cmp in recentComplaints" :key="cmp.id" class="hover:bg-slate-50 transition-colors">
                        <td class="px-5 py-3 font-mono font-medium text-slate-900">{{ cmp.id }}</td>
                        <td class="px-5 py-3">
                          <p class="font-bold text-slate-900">{{ cmp.citizen }}</p>
                          <p class="text-[11px] text-slate-500">{{ cmp.area }}</p>
                        </td>
                        <td class="px-5 py-3 text-slate-600">{{ cmp.category }}</td>
                        <td class="px-5 py-3"><span :class="`px-2 py-1 rounded text-[10px] font-bold border ${priorityBadge(cmp.priority)}`">{{ cmp.priority }}</span></td>
                        <td class="px-5 py-3"><span :class="`px-2.5 py-1 rounded-full text-[10px] font-bold ${statusBadge(cmp.status)}`">{{ cmp.status }}</span></td>
                        <td class="px-5 py-3 text-right">
                          <div class="flex items-center justify-end gap-2">
                            <button class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded transition-colors"><Eye class="w-4 h-4" /></button>
                            <button v-if="cmp.status === 'Verified'" class="text-[11px] font-bold bg-[#2563EB] text-white px-2.5 py-1.5 rounded hover:bg-[#1E40AF] transition-colors">Assign</button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Worker Availability & Leaderboard -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col">
                  <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><UserCheck class="w-5 h-5 text-green-500" /> Worker Availability</h3>
                  </div>
                  <div class="p-5 space-y-4 flex-1">
                    <div v-for="worker in workers" :key="worker.name" class="flex items-center justify-between p-3 border border-slate-100 rounded-xl hover:shadow-sm transition-shadow">
                      <div class="flex items-center gap-3">
                        <img :src="worker.photo" class="w-10 h-10 rounded-full object-cover border border-slate-200" />
                        <div>
                          <p class="text-sm font-bold text-slate-900">{{ worker.name }}</p>
                          <p class="text-[10px] text-slate-500 font-medium">{{ worker.dept }}</p>
                        </div>
                      </div>
                      <div class="text-right">
                        <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${worker.status === 'Available' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`">{{ worker.status }}</span>
                        <p class="text-xs text-slate-500 font-medium mt-1">{{ worker.tasks }} Active Tasks</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col">
                  <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><Award class="w-5 h-5 text-amber-500" /> Top Performers</h3>
                  </div>
                  <div class="p-5 space-y-4 flex-1">
                    <div v-for="(leader, idx) in leaderboard" :key="leader.name" class="flex items-center gap-3 p-3 border border-slate-100 rounded-xl bg-gradient-to-r from-white to-slate-50">
                      <div class="w-6 font-bold text-slate-400 text-sm text-center">#{{ idx + 1 }}</div>
                      <img :src="leader.photo" class="w-10 h-10 rounded-full object-cover border border-slate-200" />
                      <div class="flex-1">
                        <p class="text-sm font-bold text-slate-900 flex items-center gap-1.5">{{ leader.name }} <span class="px-1.5 py-0.5 bg-blue-100 text-blue-700 text-[9px] rounded uppercase font-bold">{{ leader.badge }}</span></p>
                        <p class="text-[10px] text-slate-500 font-medium">{{ leader.resolved }} Resolved • {{ leader.rating }} <Star class="w-2.5 h-2.5 inline text-amber-400 fill-amber-400" /></p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Department Performance -->
              <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex flex-col">
                <h3 class="font-bold text-slate-900 mb-4">Department Resolution Efficiency</h3>
                <div class="flex-1 relative min-h-[250px] w-full">
                  <canvas ref="deptChartRef"></canvas>
                </div>
              </div>

            </div>

            <!-- Right Sidebar Column (4 cols) -->
            <div class="lg:col-span-4 space-y-6">
              
              <!-- Weather & Calendar Combo -->
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-gradient-to-br from-blue-400 to-[#2563EB] p-4 rounded-2xl text-white shadow-sm flex flex-col justify-between">
                  <div class="flex justify-between items-start">
                    <MapPin class="w-4 h-4 text-blue-100" />
                    <span class="text-2xl">🌤️</span>
                  </div>
                  <div class="mt-4">
                    <p class="text-3xl font-bold">29°C</p>
                    <p class="text-xs text-blue-100 font-medium">Partly Cloudy</p>
                    <p class="text-xs text-blue-200 mt-1">Humidity: 65%</p>
                  </div>
                </div>
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex flex-col justify-between">
                  <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-slate-900 text-sm">Today</h3>
                    <Calendar class="w-4 h-4 text-[#2563EB]" />
                  </div>
                  <div class="space-y-2 mt-2">
                    <div class="border-l-2 border-[#2563EB] pl-2">
                      <p class="text-xs font-bold text-slate-900">11:00 AM</p>
                      <p class="text-[10px] text-slate-500">Dept Review Sync</p>
                    </div>
                    <div class="border-l-2 border-amber-500 pl-2">
                      <p class="text-xs font-bold text-slate-900">02:30 PM</p>
                      <p class="text-[10px] text-slate-500">Site Insp. Ward 4</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Operational Insights -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Activity class="w-4 h-4 text-[#2563EB]" /> Operational Insights</h3>
                <div class="space-y-3">
                  <div class="flex items-start gap-3 p-3 bg-red-50/50 rounded-xl border border-red-100">
                    <TrendingUp class="w-4 h-4 mt-0.5 shrink-0 text-red-500" />
                    <p class="text-sm text-slate-700 leading-tight">Garbage accumulation reports in <span class="font-bold">Ward 3</span> surged by 15% this week.</p>
                  </div>
                  <div class="flex items-start gap-3 p-3 bg-green-50/50 rounded-xl border border-green-100">
                    <CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-green-500" />
                    <p class="text-sm text-slate-700 leading-tight">Electrical Dept. resolved all emergency streetlight issues under 4 hours.</p>
                  </div>
                  <div class="flex items-start gap-3 p-3 bg-amber-50/50 rounded-xl border border-amber-100">
                    <Clock class="w-4 h-4 mt-0.5 shrink-0 text-amber-500" />
                    <p class="text-sm text-slate-700 leading-tight">45 verifications are pending. Assignment delays expected.</p>
                  </div>
                </div>
              </div>

              <!-- Upcoming Tasks -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-4 border-b border-slate-100 bg-slate-50/50">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><CheckCircle class="w-4 h-4 text-slate-500" /> Upcoming Tasks</h3>
                </div>
                <div class="p-2">
                  <label class="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg cursor-pointer">
                    <input type="checkbox" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                    <span class="text-sm text-slate-700">Approve pending worker leaves</span>
                  </label>
                  <label class="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg cursor-pointer">
                    <input type="checkbox" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                    <span class="text-sm text-slate-700">Review Weekly Analytics Report</span>
                  </label>
                  <label class="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg cursor-pointer">
                    <input type="checkbox" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                    <span class="text-sm text-slate-700">Dispatch sanitation team to Sector 12</span>
                  </label>
                </div>
              </div>

              <!-- Citizen Feedback Overview -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5 text-center flex flex-col items-center">
                <h3 class="font-bold text-slate-900 w-full text-left mb-4">Citizen Feedback</h3>
                <div class="flex items-center justify-center gap-2 mb-1">
                  <span class="text-4xl font-extrabold text-slate-900">4.5</span>
                  <span class="text-lg text-slate-400 font-bold">/ 5</span>
                </div>
                <div class="flex gap-1 mb-4">
                  <Star v-for="i in 5" :key="i" class="w-5 h-5 text-amber-400 fill-amber-400" />
                </div>
                <div class="w-full flex gap-2">
                  <div class="flex-1 bg-green-50 p-2 rounded-lg border border-green-100">
                    <p class="text-xs text-green-700 font-bold">Positive</p>
                    <p class="text-lg font-extrabold text-green-600">82%</p>
                  </div>
                  <div class="flex-1 bg-red-50 p-2 rounded-lg border border-red-100">
                    <p class="text-xs text-red-700 font-bold">Negative</p>
                    <p class="text-lg font-extrabold text-red-500">18%</p>
                  </div>
                </div>
                <div class="w-full mt-4 text-left border-t border-slate-100 pt-4">
                  <p class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-2">Recent Comment</p>
                  <p class="text-sm text-slate-700 italic bg-slate-50 p-3 rounded-lg border border-slate-100">"Pothole was filled within 24 hours. Excellent service by the roads department."</p>
                </div>
              </div>

              <!-- Recent Notifications -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col h-[400px]">
                <div class="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><Bell class="w-4 h-4 text-slate-500" /> Recent Alerts</h3>
                  <button class="text-xs font-bold text-[#2563EB] hover:underline">View All</button>
                </div>
                <div class="flex-1 overflow-y-auto p-4 space-y-4">
                  <div v-for="notif in notifications" :key="notif.id" class="flex gap-3">
                    <div :class="`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${notif.bg} ${notif.color}`">
                      <component :is="notif.icon" class="w-4 h-4" />
                    </div>
                    <div>
                      <p class="text-sm font-bold text-slate-900 leading-tight">{{ notif.title }}</p>
                      <p class="text-xs text-slate-500 mt-0.5">{{ notif.time }}</p>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  MapPin, Calendar, TrendingUp, TrendingDown, Activity, ClipboardList, Users, 
  UserCheck, Clock, ShieldCheck, Building, CheckCircle, AlertTriangle, Search, 
  BarChart3, PieChart, Star, FileText, Bell, Award, Flag, Edit, Settings
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)

// --- Dummy Data ---
const kpiCards = [
  { title: 'Total Complaints', value: '3,842', trend: 'up', percent: '12%', icon: ClipboardList, bg: 'bg-blue-50', color: 'text-blue-600' },
  { title: 'Pending Verify', value: '45', trend: 'down', percent: '5%', icon: ShieldCheck, bg: 'bg-amber-50', color: 'text-amber-500' },
  { title: 'Assigned', value: '210', trend: 'up', percent: '8%', icon: UserCheck, bg: 'bg-indigo-50', color: 'text-indigo-500' },
  { title: 'In Progress', value: '185', trend: 'up', percent: '14%', icon: Settings, bg: 'bg-purple-50', color: 'text-purple-500' },
  { title: 'Resolved Today', value: '89', trend: 'up', percent: '22%', icon: CheckCircle, bg: 'bg-green-50', color: 'text-green-500' },
  { title: 'Emergencies', value: '3', trend: 'down', percent: '2%', icon: AlertTriangle, bg: 'bg-red-50', color: 'text-red-500' },
  { title: 'Active Workers', value: '54', trend: 'up', percent: '0%', icon: Users, bg: 'bg-teal-50', color: 'text-teal-500' },
  { title: 'Avg Resol. Time', value: '24h', trend: 'down', percent: '4%', icon: Clock, bg: 'bg-slate-100', color: 'text-slate-600' },
]

const quickActions = [
  { title: 'Assign Worker', icon: UserCheck },
  { title: 'Manage Complaints', icon: ClipboardList },
  { title: 'Analytics', icon: BarChart3 },
  { title: 'Generate Report', icon: FileText }
]

const emergencyComplaints = [
  { id: 'CMP-8902', category: 'Live Wire', area: 'Downtown Sector 4', worker: null, time: '30m ago' },
  { id: 'CMP-8915', category: 'Water Pipe Burst', area: 'MG Road', worker: 'Amit Singh', time: '1h ago' },
]

const recentComplaints = [
  { id: 'CMP-8901', citizen: 'Rahul Verma', category: 'Garbage', area: 'Ward 4', priority: 'Medium', status: 'Verified', date: 'Today, 08:30 AM' },
  { id: 'CMP-8899', citizen: 'Priya Sharma', category: 'Pothole', area: 'North Zone', priority: 'High', status: 'In Progress', date: 'Yesterday' },
  { id: 'CMP-8895', citizen: 'Anil Desai', category: 'Streetlight', area: 'South Suburbs', priority: 'Low', status: 'Assigned', date: 'Yesterday' },
  { id: 'CMP-8890', category: 'Drainage', citizen: 'Sneha Patel', area: 'Downtown', priority: 'High', status: 'Resolved', date: 'Jul 07' },
]

const filteredWorkers = [
  { id: 'W-0042', name: 'Rajesh Kumar', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100', department: 'Roads', status: 'Available', pendingTasks: 1, todayTasks: 4, rating: 4.8, area: 'North Zone' },
  { id: 'W-0089', name: 'Suresh Patil', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100', department: 'Sanitation', status: 'Busy', pendingTasks: 4, todayTasks: 5, rating: 4.9, area: 'Downtown' },
]

const topWorkers = [
  { id: 1, name: 'Suresh Patil', dept: 'Sanitation', score: 98, completed: 142, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100' },
  { id: 2, name: 'Rajesh Kumar', dept: 'Roads', score: 95, completed: 118, avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100' },
]

const notifications = [
  { title: 'New Emergency Complaint', time: '10 mins ago', icon: AlertTriangle, bg: 'bg-red-100', text: 'text-red-600' },
  { title: 'Worker Amit started task CMP-8915', time: '1 hour ago', icon: Clock, bg: 'bg-blue-100', text: 'text-blue-600' },
  { title: 'Citizen feedback received (5 Stars)', time: '2 hours ago', icon: Star, bg: 'bg-amber-100', text: 'text-amber-500' },
  { title: 'Platform update scheduled tonight', time: '5 hours ago', icon: Settings, bg: 'bg-slate-200', text: 'text-slate-600' },
]

// --- Visual Helpers ---
const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-50 text-red-700 border-red-200', 'High': 'bg-orange-50 text-orange-700 border-orange-200', 'Medium': 'bg-blue-50 text-blue-700 border-blue-200', 'Low': 'bg-slate-50 text-slate-600 border-slate-200' }
  return map[priority]
}
const statusBadge = (status) => {
  const map = { 'Verified': 'bg-blue-100 text-blue-700', 'Assigned': 'bg-purple-100 text-purple-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Resolved': 'bg-green-100 text-green-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

// --- Chart Setup ---
const trendChartRef = ref(null)
const statusChartRef = ref(null)
const deptChartRef = ref(null)

let trendChart, statusChart, deptChart

onMounted(() => {
  // 1. Trend Line Chart
  if (trendChartRef.value) {
    trendChart = new Chart(trendChartRef.value, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Complaints',
          data: [65, 80, 55, 110, 95, 130, 142],
          borderColor: '#2563EB',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
          fill: true,
          tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } } } }
    })
  }

  // 2. Status Donut Chart
  if (statusChartRef.value) {
    statusChart = new Chart(statusChartRef.value, {
      type: 'doughnut',
      data: {
        labels: ['In Progress', 'Resolved', 'Assigned', 'Pending'],
        datasets: [{
          data: [185, 89, 210, 45],
          backgroundColor: ['#F59E0B', '#22C55E', '#8B5CF6', '#EF4444'],
          borderWidth: 0
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '75%', plugins: { legend: { position: 'right', labels: { boxWidth: 10 } } } }
    })
  }

  // 3. Dept Performance Horizontal Bar
  if (deptChartRef.value) {
    deptChart = new Chart(deptChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Roads', 'Sanitation', 'Electrical', 'Water', 'Drainage'],
        datasets: [{
          label: 'Efficiency %',
          data: [82, 95, 88, 76, 85],
          backgroundColor: '#2563EB',
          borderRadius: 4
        }]
      },
      options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { max: 100 } } }
    })
  }
})

onUnmounted(() => {
  if (trendChart) trendChart.destroy()
  if (statusChart) statusChart.destroy()
  if (deptChart) deptChart.destroy()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Custom Scrollbar for Main Area */
.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>