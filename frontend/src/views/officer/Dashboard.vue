<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Header Section -->
          <div class="flex flex-col lg:flex-row justify-between lg:items-end gap-4">
            <div>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">{{ greeting }}, {{ officerName }}</h1>
              <p class="text-slate-500 mt-1">Here's what's happening in your department today.</p>
            </div>
            
            <div class="flex flex-wrap items-center gap-4">
              <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <MapPin class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">{{ officerDepartment || 'No department assigned' }}</span>
              </div>
              <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <Calendar class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">{{ todayLabel }}</span>
              </div>
            </div>
          </div>

          <!-- Top KPI Cards -->
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
            <div v-for="(kpi, idx) in kpiCards" :key="idx" class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 group relative overflow-hidden">
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

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Main Column (8 cols) -->
            <div class="lg:col-span-8 space-y-6">
              
              <!-- Today's Overview Banner -->
              <div class="bg-gradient-to-r from-[#1E40AF] to-[#2563EB] rounded-2xl p-6 text-white shadow-md relative overflow-hidden">
                <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
                <h2 class="text-lg font-bold mb-4 flex items-center gap-2"><Activity class="w-5 h-5" /> Today's Overview</h2>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Total Assigned</p>
                    <p class="text-xl font-bold">{{ kpiRaw.total }}</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Resolved</p>
                    <p class="text-xl font-bold">{{ kpiRaw.resolved }}</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Active Workers</p>
                    <p class="text-xl font-bold">{{ kpiRaw.activeWorkers }}/{{ kpiRaw.totalDeptWorkers }}</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Assigned</p>
                    <p class="text-xl font-bold">{{ kpiRaw.assigned }}</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10 border-red-400/50">
                    <p class="text-xs text-red-100 font-medium mb-1">Emergencies</p>
                    <p class="text-xl font-bold text-red-200">{{ kpiRaw.emergency }}</p>
                  </div>
                  <div class="bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10">
                    <p class="text-xs text-blue-100 font-medium mb-1">Feedback Rx</p>
                    <p class="text-xl font-bold">{{ kpiRaw.feedbackTotal }}</p>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <router-link v-for="action in quickActions" :key="action.title" :to="action.to" class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all group text-left flex flex-col items-start">
                  <div class="w-10 h-10 rounded-xl bg-slate-50 group-hover:bg-blue-50 text-slate-500 group-hover:text-[#2563EB] flex items-center justify-center mb-3 transition-colors">
                    <component :is="action.icon" class="w-5 h-5" />
                  </div>
                  <h3 class="font-bold text-slate-900 text-sm mb-1">{{ action.title }}</h3>
                  <p class="text-xs text-slate-500">{{ action.desc }}</p>
                </router-link>
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
                  <router-link to="/officer/complaints" class="text-xs font-bold text-red-600 hover:underline">View All</router-link>
                </div>
                <div class="divide-y divide-slate-100">
                  <div v-for="em in emergencyComplaints" :key="em.id" class="p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50 transition-colors">
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
                        <p class="text-xs text-slate-500 font-medium">Submitted</p>
                        <p class="text-sm font-bold text-slate-900">{{ em.date }}</p>
                      </div>
                      <router-link :to="em.worker ? `/officer/complaintdetails/${em.rawId}` : `/officer/assign/${em.rawId}`" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg shadow-sm transition-colors w-full md:w-auto text-center">Open Case</router-link>
                    </div>
                  </div>
                  <div v-if="emergencyComplaints.length === 0" class="p-6 text-center text-sm text-slate-400">No active emergencies. Good work.</div>
                </div>
              </div>

              <!-- Recent Complaints Table -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center justify-between">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><ClipboardList class="w-5 h-5 text-[#2563EB]" /> Recent Complaints</h3>
                  <router-link to="/officer/complaints" class="text-sm font-medium text-[#2563EB] hover:underline">View Pipeline</router-link>
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
                            <router-link :to="`/officer/complaintdetails/${cmp.rawId}`" class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded transition-colors"><Eye class="w-4 h-4" /></router-link>
                            <router-link v-if="cmp.status === 'Assigned'" :to="`/officer/assign/${cmp.rawId}`" class="text-[11px] font-bold bg-[#2563EB] text-white px-2.5 py-1.5 rounded hover:bg-[#1E40AF] transition-colors">Assign</router-link>
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
                    <div v-for="worker in workerAvailability" :key="worker.id" class="flex items-center justify-between p-3 border border-slate-100 rounded-xl hover:shadow-sm transition-shadow">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center font-bold text-slate-500 text-sm shrink-0">{{ initials(worker.name) }}</div>
                        <div>
                          <p class="text-sm font-bold text-slate-900">{{ worker.name }}</p>
                        </div>
                      </div>
                      <div class="text-right">
                        <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${worker.status === 'Available' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`">{{ worker.status }}</span>
                        <p class="text-xs text-slate-500 font-medium mt-1">{{ worker.activeTasks }} Active Tasks</p>
                      </div>
                    </div>
                    <div v-if="workerAvailability.length === 0" class="text-center text-sm text-slate-400 py-4">No workers in your department yet.</div>
                  </div>
                </div>

                <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col">
                  <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><Award class="w-5 h-5 text-amber-500" /> Top Performers</h3>
                  </div>
                  <div class="p-5 space-y-4 flex-1">
                    <div v-for="(leader, idx) in topWorkers" :key="leader.id" class="flex items-center gap-3 p-3 border border-slate-100 rounded-xl bg-gradient-to-r from-white to-slate-50">
                      <div class="w-6 font-bold text-slate-400 text-sm text-center">#{{ idx + 1 }}</div>
                      <div class="w-10 h-10 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center font-bold text-slate-500 text-sm shrink-0">{{ initials(leader.name) }}</div>
                      <div class="flex-1">
                        <p class="text-sm font-bold text-slate-900">{{ leader.name }}</p>
                        <p class="text-[10px] text-slate-500 font-medium">{{ leader.completedTasks }} Resolved</p>
                      </div>
                    </div>
                    <div v-if="topWorkers.length === 0" class="text-center text-sm text-slate-400 py-4">No completed tasks yet.</div>
                  </div>
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
                  <div v-if="kpiRaw.emergency > 0" class="flex items-start gap-3 p-3 bg-red-50/50 rounded-xl border border-red-100">
                    <AlertTriangle class="w-4 h-4 mt-0.5 shrink-0 text-red-500" />
                    <p class="text-sm text-slate-700 leading-tight"><span class="font-bold">{{ kpiRaw.emergency }}</span> emergency complaint{{ kpiRaw.emergency === 1 ? '' : 's' }} still need attention.</p>
                  </div>
                  <div v-if="kpiRaw.assigned > 0" class="flex items-start gap-3 p-3 bg-amber-50/50 rounded-xl border border-amber-100">
                    <Clock class="w-4 h-4 mt-0.5 shrink-0 text-amber-500" />
                    <p class="text-sm text-slate-700 leading-tight"><span class="font-bold">{{ kpiRaw.assigned }}</span> complaint{{ kpiRaw.assigned === 1 ? '' : 's' }} awaiting a worker assignment.</p>
                  </div>
                  <div v-if="kpiRaw.avgRating != null" class="flex items-start gap-3 p-3 bg-green-50/50 rounded-xl border border-green-100">
                    <CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-green-500" />
                    <p class="text-sm text-slate-700 leading-tight">Citizens are rating your resolved complaints <span class="font-bold">{{ kpiRaw.avgRating }}/5</span> on average.</p>
                  </div>
                  <div v-if="!kpiRaw.emergency && !kpiRaw.assigned && kpiRaw.avgRating == null" class="text-sm text-slate-400 text-center py-2">Nothing needs your attention right now.</div>
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
                <template v-if="kpiRaw.avgRating != null">
                  <div class="flex items-center justify-center gap-2 mb-1">
                    <span class="text-4xl font-extrabold text-slate-900">{{ kpiRaw.avgRating }}</span>
                    <span class="text-lg text-slate-400 font-bold">/ 5</span>
                  </div>
                  <div class="flex gap-1 mb-4">
                    <Star v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= Math.round(kpiRaw.avgRating) ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                  </div>
                  <div class="w-full flex gap-2">
                    <div class="flex-1 bg-green-50 p-2 rounded-lg border border-green-100">
                      <p class="text-xs text-green-700 font-bold">Positive</p>
                      <p class="text-lg font-extrabold text-green-600">{{ kpiRaw.feedbackPositivePct }}%</p>
                    </div>
                    <div class="flex-1 bg-red-50 p-2 rounded-lg border border-red-100">
                      <p class="text-xs text-red-700 font-bold">Negative</p>
                      <p class="text-lg font-extrabold text-red-500">{{ kpiRaw.feedbackNegativePct }}%</p>
                    </div>
                  </div>
                  <div v-if="kpiRaw.recentFeedbackComment" class="w-full mt-4 text-left border-t border-slate-100 pt-4">
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-2">Recent Comment</p>
                    <p class="text-sm text-slate-700 italic bg-slate-50 p-3 rounded-lg border border-slate-100">"{{ kpiRaw.recentFeedbackComment }}"</p>
                  </div>
                </template>
                <p v-else class="text-sm text-slate-400 py-4">No feedback received yet.</p>
              </div>

              <!-- Recent Notifications -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col h-[400px]">
                <div class="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><Bell class="w-4 h-4 text-slate-500" /> Recent Alerts</h3>
                  <router-link to="/officer/notifications" class="text-xs font-bold text-[#2563EB] hover:underline">View All</router-link>
                </div>
                <div class="flex-1 overflow-y-auto p-4 space-y-4">
                  <div v-for="notif in recentNotifications" :key="notif.id" class="flex gap-3">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 bg-blue-100 text-blue-600">
                      <Bell class="w-4 h-4" />
                    </div>
                    <div>
                      <p class="text-sm font-bold text-slate-900 leading-tight">{{ notif.title }}</p>
                      <p class="text-xs text-slate-500 mt-0.5">{{ notif.time }}</p>
                    </div>
                  </div>
                  <div v-if="recentNotifications.length === 0" class="text-center text-sm text-slate-400 py-4">No notifications yet.</div>
                </div>
              </div>

            </div>
          </div>

        </div>
      </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  MapPin, Calendar, TrendingUp, TrendingDown, Activity, ClipboardList, Users, 
  UserCheck, Clock, ShieldCheck, Building, CheckCircle, AlertTriangle, Search, 
  BarChart3, PieChart, Star, FileText, Bell, Award, Flag, Edit, Settings, Eye
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
const isSidebarOpen = ref(false)
const router = useRouter()

const officerName = ref('Officer')
const officerDepartment = ref('')
const kpiRaw = reactive({
  total: 0, assigned: 0, inProgress: 0, resolved: 0, emergency: 0,
  activeWorkers: 0, totalDeptWorkers: 0, avgResolutionHours: null, avgRating: null,
  feedbackTotal: 0, feedbackPositivePct: null, feedbackNegativePct: null, recentFeedbackComment: null
})
const statusBreakdown = reactive({ Assigned: 0, 'In Progress': 0, Resolved: 0, Closed: 0 })
const weeklyTrend = ref([])
const emergencyComplaints = ref([])
const recentComplaints = ref([])
const workerAvailability = ref([])
const topWorkers = ref([])
const recentNotifications = ref([])

const greeting = computed(() => {
  const h = new Date().getHours()
  return h < 12 ? 'Good Morning' : h < 17 ? 'Good Afternoon' : 'Good Evening'
})
const todayLabel = computed(() => new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: '2-digit', year: 'numeric' }))

const initials = (name) => {
  if (!name) return '?'
  return name.trim().split(/\s+/).slice(0, 2).map(n => n[0]?.toUpperCase()).join('')
}

const kpiCards = computed(() => [
  { title: 'Total Assigned', value: String(kpiRaw.total), icon: ClipboardList, bg: 'bg-blue-50', color: 'text-blue-600' },
  { title: 'Assigned', value: String(kpiRaw.assigned), icon: ShieldCheck, bg: 'bg-amber-50', color: 'text-amber-500' },
  { title: 'In Progress', value: String(kpiRaw.inProgress), icon: Settings, bg: 'bg-purple-50', color: 'text-purple-500' },
  { title: 'Resolved', value: String(kpiRaw.resolved), icon: CheckCircle, bg: 'bg-green-50', color: 'text-green-500' },
  { title: 'Emergencies', value: String(kpiRaw.emergency), icon: AlertTriangle, bg: 'bg-red-50', color: 'text-red-500' },
  { title: 'Active Workers', value: `${kpiRaw.activeWorkers}/${kpiRaw.totalDeptWorkers}`, icon: Users, bg: 'bg-teal-50', color: 'text-teal-500' },
  { title: 'Avg Resol. Time', value: kpiRaw.avgResolutionHours != null ? `${kpiRaw.avgResolutionHours}h` : '—', icon: Clock, bg: 'bg-slate-100', color: 'text-slate-600' },
])

const quickActions = [
  { title: 'Assign Worker', desc: 'Pick an assigned complaint', icon: UserCheck, to: '/officer/complaints' },
  { title: 'Manage Complaints', desc: 'View your full queue', icon: ClipboardList, to: '/officer/complaints' },
  { title: 'Analytics', desc: 'Department performance', icon: BarChart3, to: '/officer/analytics' },
  { title: 'Generate Report', desc: 'Export complaint data', icon: FileText, to: '/officer/analytics' },
]

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-50 text-red-700 border-red-200', 'High': 'bg-orange-50 text-orange-700 border-orange-200', 'Medium': 'bg-blue-50 text-blue-700 border-blue-200', 'Low': 'bg-slate-50 text-slate-600 border-slate-200' }
  return map[priority]
}
const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-purple-100 text-purple-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Resolved': 'bg-green-100 text-green-700', 'Closed': 'bg-slate-200 text-slate-600' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const trendChartRef = ref(null)
const statusChartRef = ref(null)
let trendChart, statusChart

const renderCharts = () => {
  if (trendChart) trendChart.destroy()
  if (statusChart) statusChart.destroy()

  if (trendChartRef.value) {
    trendChart = new Chart(trendChartRef.value, {
      type: 'line',
      data: {
        labels: weeklyTrend.value.map(d => d.day),
        datasets: [{
          label: 'Complaints',
          data: weeklyTrend.value.map(d => d.count),
          borderColor: '#2563EB',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
          fill: true,
          tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } } } }
    })
  }

  if (statusChartRef.value) {
    statusChart = new Chart(statusChartRef.value, {
      type: 'doughnut',
      data: {
        labels: Object.keys(statusBreakdown),
        datasets: [{
          data: Object.values(statusBreakdown),
          backgroundColor: ['#8B5CF6', '#F59E0B', '#22C55E', '#94A3B8'],
          borderWidth: 0
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '75%', plugins: { legend: { position: 'right', labels: { boxWidth: 10 } } } }
    })
  }
}

const timeAgo = (iso) => {
  if (!iso) return ''
  const diffMs = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diffMs / 60000)
  if (mins < 1) return 'Just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: '2-digit' })
}

const fetchDashboard = async () => {
  try {
    const { data } = await axios.get(`${API_BASE}/dashboard`, authHeaders())

    officerName.value = data.officer.name
    officerDepartment.value = data.officer.department
    Object.assign(kpiRaw, data.kpi)
    Object.assign(statusBreakdown, data.statusBreakdown)
    weeklyTrend.value = data.weeklyTrend

    emergencyComplaints.value = data.emergencyComplaints
    recentComplaints.value = data.recentComplaints.map(c => ({ ...c, date: c.date }))
    workerAvailability.value = data.workerAvailability
    topWorkers.value = data.topWorkers

    recentNotifications.value = data.recentNotifications.map(n => ({
      id: n.id, title: n.title, time: timeAgo(n.createdAt)
    }))

    renderCharts()
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
  }
}

onMounted(fetchDashboard)

onUnmounted(() => {
  if (trendChart) trendChart.destroy()
  if (statusChart) statusChart.destroy()
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