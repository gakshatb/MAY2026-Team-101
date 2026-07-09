<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Sidebar Placeholder -->
    <Sidebar userRole="Field Worker" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      
      <!-- Navbar Placeholder -->
      <DashboardNavbar userRole="Field Worker" pageTitle="Dashboard" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Header Section -->
          <div class="flex flex-col lg:flex-row justify-between lg:items-end gap-4">
            <div>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Good Morning, Rahul Verma</h1>
              <p class="text-slate-500 mt-1">Here's your work schedule and assigned tasks for today.</p>
            </div>
            
            <div class="flex flex-wrap items-center gap-3">
              <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <MapPin class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">North Zone, Ward 12</span>
              </div>
              <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-slate-100 flex items-center gap-3">
                <Calendar class="w-4 h-4 text-[#2563EB]" />
                <span class="text-sm font-semibold text-slate-700">{{ currentDate }}</span>
              </div>
            </div>
          </div>

          <!-- Top KPI Summary Cards -->
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
              <div class="absolute bottom-0 left-0 w-full h-8 opacity-10 group-hover:opacity-20 transition-opacity">
                <svg viewBox="0 0 100 20" preserveAspectRatio="none" class="w-full h-full" :class="kpi.color">
                  <path d="M0,20 Q25,5 50,15 T100,0 L100,20 Z" fill="currentColor"></path>
                </svg>
              </div>
            </div>
          </div>

          <!-- Primary Workspace Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Main Column (8 cols) -->
            <div class="lg:col-span-8 flex flex-col gap-6">
              
              <!-- Current Active Task Highlight -->
              <div class="bg-gradient-to-br from-[#1E40AF] to-[#2563EB] rounded-2xl shadow-md overflow-hidden relative text-white">
                <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3"></div>
                <div class="p-6 relative z-10">
                  <div class="flex justify-between items-start mb-4">
                    <div>
                      <div class="flex items-center gap-2 mb-2">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-white/20 backdrop-blur-sm border border-white/20 font-mono">{{ currentTask.id }}</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300 border border-amber-500/30">In Progress</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-red-500/20 text-red-200 border border-red-500/30">{{ currentTask.priority }}</span>
                      </div>
                      <h2 class="text-2xl font-bold mb-1">{{ currentTask.title }}</h2>
                      <div class="flex items-center gap-4 text-sm text-blue-100 font-medium">
                        <span class="flex items-center gap-1"><MapPin class="w-4 h-4" /> {{ currentTask.area }}</span>
                        <span class="flex items-center gap-1"><User class="w-4 h-4" /> Officer: {{ currentTask.officer }}</span>
                      </div>
                    </div>
                    <div class="text-right">
                      <p class="text-xs text-blue-200 font-medium mb-1">Estimated Time</p>
                      <p class="text-xl font-bold flex items-center justify-end gap-1.5"><Clock class="w-5 h-5"/> {{ currentTask.estTime }}</p>
                    </div>
                  </div>
                  
                  <div class="mb-6">
                    <div class="flex justify-between text-xs font-bold text-blue-100 mb-1.5">
                      <span>Task Progress</span>
                      <span>{{ currentTask.progress }}%</span>
                    </div>
                    <div class="w-full h-1.5 bg-black/20 rounded-full overflow-hidden">
                      <div class="h-full bg-white rounded-full" :style="`width: ${currentTask.progress}%`"></div>
                    </div>
                  </div>

                  <div class="flex flex-wrap gap-3">
                    <router-link :to="`/worker/task/${currentTask.id}`" class="px-5 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white text-sm font-bold rounded-lg transition-colors backdrop-blur-sm flex items-center gap-2">
                      <FileText class="w-4 h-4" /> View Details
                    </router-link>
                    <router-link :to="`/worker/update/${currentTask.id}`" class="px-5 py-2.5 bg-white text-[#2563EB] hover:bg-slate-50 text-sm font-bold rounded-lg transition-colors shadow-sm flex items-center gap-2">
                      <PlayCircle class="w-4 h-4" /> Update Complaint
                    </router-link>
                  </div>
                </div>
              </div>

              <!-- Today's Overview Bar -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5 flex flex-wrap justify-between items-center gap-4">
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-blue-50 rounded-lg"><ClipboardList class="w-5 h-5 text-[#2563EB]" /></div>
                  <div><p class="text-xs text-slate-500 font-bold uppercase">Tasks Today</p><p class="text-lg font-extrabold text-slate-900">6</p></div>
                </div>
                <div class="w-px h-10 bg-slate-100 hidden sm:block"></div>
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-green-50 rounded-lg"><CheckCircle class="w-5 h-5 text-green-600" /></div>
                  <div><p class="text-xs text-slate-500 font-bold uppercase">Completed</p><p class="text-lg font-extrabold text-slate-900">2</p></div>
                </div>
                <div class="w-px h-10 bg-slate-100 hidden sm:block"></div>
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-amber-50 rounded-lg"><Clock class="w-5 h-5 text-amber-500" /></div>
                  <div><p class="text-xs text-slate-500 font-bold uppercase">Hours Worked</p><p class="text-lg font-extrabold text-slate-900">3.5h</p></div>
                </div>
                <div class="w-px h-10 bg-slate-100 hidden md:block"></div>
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-purple-50 rounded-lg"><Shield class="w-5 h-5 text-purple-500" /></div>
                  <div><p class="text-xs text-slate-500 font-bold uppercase">Pending Verify</p><p class="text-lg font-extrabold text-slate-900">1</p></div>
                </div>
              </div>

              <!-- Emergency Assignments -->
              <div v-if="emergencies.length > 0" class="bg-white rounded-2xl shadow-sm border border-red-200 overflow-hidden">
                <div class="bg-red-50 px-5 py-3 border-b border-red-100 flex items-center justify-between">
                  <h3 class="font-bold text-red-700 flex items-center gap-2">
                    <div class="relative flex h-3 w-3"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span><span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span></div>
                    Emergency Assignments
                  </h3>
                </div>
                <div class="divide-y divide-slate-100">
                  <div v-for="em in emergencies" :key="em.id" class="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50 transition-colors">
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
                          <span class="flex items-center gap-1"><Clock class="w-3 h-3 text-slate-400"/> Assigned {{ em.timeAssigned }}</span>
                        </p>
                      </div>
                    </div>
                    <button class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg shadow-sm transition-colors whitespace-nowrap">Start Immediately</button>
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
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><ClipboardList class="w-5 h-5 text-[#2563EB]" /> Next Assigned Tasks</h3>
                  <router-link to="/worker/tasks" class="text-sm font-medium text-[#2563EB] hover:underline">View All Tasks</router-link>
                </div>
                <div class="overflow-x-auto">
                  <table class="w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wider border-b border-slate-100">
                      <tr>
                        <th class="px-5 py-3">Task ID & Title</th>
                        <th class="px-5 py-3">Category</th>
                        <th class="px-5 py-3">Status</th>
                        <th class="px-5 py-3">Deadline</th>
                        <th class="px-5 py-3 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="task in assignedTasks" :key="task.id" class="hover:bg-slate-50 transition-colors group">
                        <td class="px-5 py-3">
                          <p class="font-bold text-slate-900 mb-0.5">{{ task.title }}</p>
                          <p class="text-[10px] text-slate-500 font-mono">{{ task.id }} • {{ task.area }}</p>
                        </td>
                        <td class="px-5 py-3 text-slate-600 text-xs font-medium">{{ task.category }}</td>
                        <td class="px-5 py-3">
                          <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${statusBadge(task.status)}`">{{ task.status }}</span>
                        </td>
                        <td class="px-5 py-3 text-slate-600 text-xs font-medium">{{ task.deadline }}</td>
                        <td class="px-5 py-3 text-right">
                          <div class="flex items-center justify-end gap-2">
                            <router-link :to="`/worker/task/${task.id}`" class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-50 transition-colors">Details</router-link>
                            <router-link :to="`/worker/update/${task.id}`" class="px-3 py-1.5 bg-[#2563EB] text-white text-xs font-bold rounded hover:bg-[#1E40AF] transition-colors shadow-sm">Update</router-link>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Charts Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Task Progress Doughnut -->
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex flex-col">
                  <h3 class="font-bold text-slate-900 mb-4">Task Progress Overview</h3>
                  <div class="flex-1 relative min-h-[220px] w-full flex items-center justify-center">
                    <canvas ref="progressChartRef"></canvas>
                  </div>
                </div>
                <!-- Weekly Productivity Line -->
                <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex flex-col">
                  <h3 class="font-bold text-slate-900 mb-4">Weekly Productivity</h3>
                  <div class="flex-1 relative min-h-[220px] w-full">
                    <canvas ref="productivityChartRef"></canvas>
                  </div>
                </div>
              </div>

            </div>

            <!-- Right Context Column (4 cols) -->
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
                    <p class="text-xs text-blue-100 font-medium leading-tight mt-1">Partly Cloudy<br>Wind 12 km/h</p>
                  </div>
                </div>
                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex flex-col justify-between text-center">
                  <h3 class="font-bold text-slate-900 text-sm mb-1">Today</h3>
                  <p class="text-4xl font-extrabold text-[#2563EB]">09</p>
                  <p class="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">Jul 2026</p>
                  <p class="text-[10px] text-slate-400 mt-2 font-medium">Thursday</p>
                </div>
              </div>

              <!-- Today's Schedule -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Calendar class="w-5 h-5 text-[#2563EB]" /> Today's Schedule</h3>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="(event, idx) in schedule" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-white rounded-full ring-4 ring-white border-2" :class="event.status === 'past' ? 'border-[#22C55E] bg-[#22C55E]' : event.status === 'current' ? 'border-[#2563EB] bg-[#2563EB] ring-[#2563EB]/20' : 'border-slate-300'"></div>
                    <p class="text-sm font-bold text-slate-900" :class="{'text-slate-400': event.status === 'past'}">{{ event.title }}</p>
                    <p class="text-[10px] font-bold" :class="event.status === 'past' ? 'text-slate-400' : 'text-[#2563EB]'">{{ event.time }}</p>
                  </div>
                </div>
              </div>

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

              <!-- Required Equipment Checklist -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Tool class="w-5 h-5 text-slate-400" /> Assigned Equipment</h3>
                <div class="space-y-3">
                  <div v-for="eq in equipment" :key="eq.name" class="flex items-center justify-between p-2.5 bg-slate-50 border border-slate-100 rounded-lg">
                    <div class="flex items-center gap-3">
                      <component :is="eq.icon" class="w-4 h-4 text-slate-400" />
                      <span class="text-sm font-medium text-slate-700">{{ eq.name }}</span>
                    </div>
                    <span :class="`px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider ${eq.status === 'Available' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`">{{ eq.status }}</span>
                  </div>
                </div>
              </div>

              <!-- Officer Messages -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col h-[300px]">
                <div class="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><MessageSquare class="w-4 h-4 text-[#2563EB]" /> Officer Messages</h3>
                </div>
                <div class="flex-1 overflow-y-auto p-4 space-y-4">
                  <div v-for="msg in officerMessages" :key="msg.id" class="bg-blue-50 border border-blue-100 rounded-xl p-3 relative">
                    <div class="absolute -left-1.5 top-3 w-3 h-3 bg-blue-50 border-l border-b border-blue-100 transform rotate-45"></div>
                    <p class="text-sm text-[#1E40AF] italic mb-2">"{{ msg.text }}"</p>
                    <div class="flex items-center justify-between">
                      <p class="text-[9px] font-bold text-blue-600 uppercase tracking-wide">— Officer {{ msg.officer }}</p>
                      <p class="text-[9px] text-blue-500 font-medium">{{ msg.time }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Performance Summary -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Award class="w-5 h-5 text-purple-500" /> Performance Summary</h3>
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 text-center">
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Monthly Tasks</p>
                    <p class="text-xl font-bold text-slate-900">42</p>
                  </div>
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100 text-center">
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Citizen Rating</p>
                    <p class="text-xl font-bold text-slate-900 flex items-center justify-center gap-1">4.8 <Star class="w-4 h-4 text-amber-400 fill-amber-400"/></p>
                  </div>
                </div>
                <div class="flex items-center justify-between p-3 bg-green-50 rounded-xl border border-green-100">
                  <span class="text-sm font-bold text-green-800">Performance Score</span>
                  <span class="text-lg font-bold text-green-700 flex items-center gap-1">94/100</span>
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
  MapPin, Calendar, TrendingUp, TrendingDown, ClipboardList, CheckCircle, 
  Clock, Shield, AlertTriangle, FileText, PlayCircle, User, Wrench, Hammer, 
  Truck, ShieldCheck, Activity, MessageSquare, Award, Star, Bell
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const currentDate = 'Thursday, July 09, 2026'

// --- Dummy Data ---
const kpiCards = [
  { title: 'Assigned Tasks', value: '8', trend: 'up', percent: '2', icon: ClipboardList, bg: 'bg-blue-50', color: 'text-blue-600' },
  { title: 'Pending Tasks', value: '3', trend: 'down', percent: '1', icon: Clock, bg: 'bg-amber-50', color: 'text-amber-500' },
  { title: 'In Progress', value: '1', trend: 'up', percent: '1', icon: Activity, bg: 'bg-purple-50', color: 'text-purple-500' },
  { title: 'Completed Today', value: '2', trend: 'up', percent: '2', icon: CheckCircle, bg: 'bg-green-50', color: 'text-green-500' },
  { title: 'Emergency', value: '1', trend: 'down', percent: '1', icon: AlertTriangle, bg: 'bg-red-50', color: 'text-red-500' },
  { title: 'Overdue Tasks', value: '0', trend: 'down', percent: '0', icon: Shield, bg: 'bg-slate-100', color: 'text-slate-600' },
  { title: 'Weekly Score', value: '94', trend: 'up', percent: '5%', icon: Award, bg: 'bg-indigo-50', color: 'text-indigo-500' },
  { title: 'Avg Time', value: '3.5h', trend: 'down', percent: '10%', icon: TrendingDown, bg: 'bg-teal-50', color: 'text-teal-500' },
]

const quickActions = [
  { title: 'My Tasks', desc: 'View assigned list', icon: ClipboardList, link: '/worker/tasks' },
  { title: 'Completed', desc: 'Work history', icon: CheckCircle, link: '/worker/completed' },
  { title: 'Alerts', desc: 'Recent updates', icon: Bell, link: '/worker/notifications' },
  { title: 'Profile', desc: 'Manage account', icon: User, link: '/worker/profile' }
]

const currentTask = {
  id: 'CMP-8875',
  title: 'Deep Pothole Repair on Main Road',
  category: 'Road Damage',
  priority: 'High',
  area: 'MG Road, Ward 12',
  officer: 'S. Patel',
  estTime: '2h 30m',
  progress: 65
}

const emergencies = [
  { id: 'CMP-8902', title: 'Live Wire Fallen on Walkway', area: 'Downtown Sector 4', priority: 'Emergency', timeAssigned: '15 mins ago' }
]

const assignedTasks = [
  { id: 'CMP-8850', title: 'Blocked Drainage clearing', category: 'Drainage', area: 'North Zone', status: 'Assigned', deadline: 'Today, 02:00 PM' },
  { id: 'CMP-8812', title: 'Overflowing dustbin', category: 'Garbage', area: 'South Suburbs', status: 'Travelling', deadline: 'Today, 04:30 PM' },
  { id: 'CMP-8805', title: 'Broken Streetlight', category: 'Electrical', area: 'East Ward', status: 'Accepted', deadline: 'Tomorrow, 10:00 AM' }
]

const schedule = [
  { title: 'Morning Briefing', time: '08:30 AM', status: 'past' },
  { title: 'CMP-8822: Signage Repair', time: '09:00 AM', status: 'past' },
  { title: 'CMP-8875: Pothole Repair', time: '11:00 AM', status: 'current' },
  { title: 'CMP-8902: Live Wire (Emergency)', time: '01:30 PM', status: 'upcoming' },
  { title: 'CMP-8850: Drainage Cleaning', time: '03:30 PM', status: 'upcoming' }
]

const equipment = [
  { name: 'Safety Helmet', status: 'Available', icon: ShieldCheck },
  { name: 'Repair Toolkit', status: 'Available', icon: Hammer },
  { name: 'Reflective Jacket', status: 'Available', icon: User },
  { name: 'Heavy Vehicle', status: 'Unavailable', icon: Truck }
]

const officerMessages = [
  { id: 1, text: 'Please complete Complaint #CMP-8850 before 5 PM due to expected rain.', officer: 'S. Patel', time: '1 hour ago' },
  { id: 2, text: 'Emergency task CMP-8902 assigned. Please pause current work and travel to the site immediately.', officer: 'System', time: '15 mins ago' },
  { id: 3, text: 'Carry additional safety cones for the road repair task today.', officer: 'R. Kumar', time: '3 hours ago' }
]

// --- Visual Helpers ---
const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'Accepted': 'bg-blue-100 text-blue-700', 'Travelling': 'bg-indigo-100 text-indigo-700', 'Work Started': 'bg-purple-100 text-purple-700', 'In Progress': 'bg-amber-100 text-amber-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

// --- Charts Setup ---
const progressChartRef = ref(null)
const productivityChartRef = ref(null)
let progressChart, productivityChart

onMounted(() => {
  // 1. Task Progress Doughnut
  if (progressChartRef.value) {
    progressChart = new Chart(progressChartRef.value, {
      type: 'doughnut',
      data: {
        labels: ['Completed', 'In Progress', 'Assigned', 'Pending Verify'],
        datasets: [{
          data: [12, 1, 3, 1],
          backgroundColor: ['#22C55E', '#F59E0B', '#2563EB', '#8B5CF6'],
          borderWidth: 0
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, cutout: '75%', plugins: { legend: { position: 'right', labels: { boxWidth: 10 } } } }
    })
  }

  // 2. Weekly Productivity Line
  if (productivityChartRef.value) {
    productivityChart = new Chart(productivityChartRef.value, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        datasets: [
          { label: 'Tasks', data: [3, 4, 2, 5, 2], borderColor: '#2563EB', backgroundColor: 'rgba(37,99,235,0.1)', fill: true, tension: 0.4 },
          { label: 'Hours', data: [6, 7, 5, 8, 4], borderColor: '#F59E0B', borderDash: [5, 5], tension: 0.4 }
        ]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } }, scales: { y: { beginAtZero: true, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }
    })
  }
})

onUnmounted(() => {
  if (progressChart) progressChart.destroy()
  if (productivityChart) productivityChart.destroy()
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