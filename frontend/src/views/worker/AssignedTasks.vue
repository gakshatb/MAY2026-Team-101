<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Sidebar Placeholder -->
    <Sidebar userRole="Field Worker" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      
      <!-- Navbar Placeholder -->
      <DashboardNavbar userRole="Field Worker" pageTitle="Assigned Tasks" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

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
            <div class="flex gap-2">
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
                <Clock class="w-4 h-4 text-[#2563EB]" /> Clock In
              </button>
            </div>
          </div>

          <!-- Summary Statistics Cards -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div v-for="stat in summaryStats" :key="stat.title" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
              <div class="flex justify-between items-start mb-2">
                <div :class="`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor}`">
                  <component :is="stat.icon" class="w-4 h-4" />
                </div>
                <span v-if="stat.trend" :class="`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${stat.trend > 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`">
                  {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}
                </span>
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
                    <option value="Travelling">Travelling</option>
                    <option value="Work Started">Work Started</option>
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
                    <option value="Deadline">Sort by: Deadline</option>
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

              <!-- Task List/Grid -->
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
                        <img :src="task.image" class="w-12 h-12 rounded-lg object-cover border border-slate-200 shrink-0" />
                      </div>
                      
                      <p class="text-sm text-slate-600 line-clamp-2 mb-4">{{ task.description }}</p>
                      
                      <div class="grid grid-cols-2 gap-y-2 text-xs text-slate-500 mb-4">
                        <span class="flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-slate-400"/> <span class="truncate">{{ task.area }}</span></span>
                        <span class="flex items-center gap-1.5"><Building class="w-3.5 h-3.5 text-slate-400"/> <span class="truncate">{{ task.category }}</span></span>
                        <span class="flex items-center gap-1.5" :class="isOverdue(task.deadline) ? 'text-red-600 font-bold' : ''"><Clock class="w-3.5 h-3.5 shrink-0"/> Due: {{ task.deadline }}</span>
                        <span class="flex items-center gap-1.5"><UserCheck class="w-3.5 h-3.5 text-slate-400 shrink-0"/> {{ task.officer }}</span>
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

                      <!-- Expandable Details -->
                      <div v-if="expandedTask === task.id" class="mt-4 pt-4 border-t border-slate-100 space-y-4 animate-fade-in">
                        <div class="bg-blue-50 p-3 rounded-lg border border-blue-100">
                          <p class="text-xs font-bold text-[#1E40AF] uppercase tracking-wide flex items-center gap-1.5 mb-1"><FileText class="w-3.5 h-3.5"/> Officer Instructions</p>
                          <p class="text-sm text-[#1E40AF]">{{ task.instructions }}</p>
                        </div>
                        <div>
                          <p class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-2">Required Materials</p>
                          <div class="flex flex-wrap gap-1.5">
                            <span v-for="mat in task.materials" :key="mat" class="px-2 py-1 bg-slate-100 text-slate-600 text-[10px] font-bold rounded flex items-center gap-1 border border-slate-200">
                              <Wrench class="w-3 h-3" /> {{ mat }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Card Actions -->
                    <div class="bg-slate-50 border-t border-slate-100 p-3 flex gap-2">
                      <button @click="toggleExpand(task.id)" class="px-3 py-2 bg-white border border-slate-200 text-slate-600 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors flex-1 flex justify-center items-center">
                        {{ expandedTask === task.id ? 'Hide Details' : 'View Details' }}
                      </button>
                      <button class="px-3 py-2 text-white text-xs font-bold rounded-lg transition-colors flex-1 shadow-sm flex items-center justify-center gap-1.5" :class="actionButtonTheme(task.status)">
                        <component :is="actionButtonIcon(task.status)" class="w-3.5 h-3.5" />
                        {{ actionButtonText(task.status) }}
                      </button>
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
                          <th class="px-5 py-4">Deadline</th>
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
                            <span class="text-slate-600 font-medium text-xs" :class="isOverdue(task.deadline) ? 'text-red-600 font-bold' : ''">{{ task.deadline }}</span>
                          </td>
                          <td class="px-5 py-4 min-w-[120px]">
                            <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                              <div class="h-full rounded-full bg-[#2563EB]" :style="`width: ${getProgress(task.status)}%`"></div>
                            </div>
                            <p class="text-[10px] text-slate-400 mt-1 font-bold">{{ getProgress(task.status) }}%</p>
                          </td>
                          <td class="px-5 py-4 text-right">
                            <div class="flex items-center justify-end gap-2">
                              <button class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-50 transition-colors">Details</button>
                              <button class="px-3 py-1.5 text-white text-xs font-bold rounded transition-colors shadow-sm" :class="actionButtonTheme(task.status)">Update</button>
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
            </div>

            <!-- Right Column: Context & Scheduling (4 cols) -->
            <div class="xl:col-span-4 space-y-6">
              
              <!-- Today's Schedule -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Calendar class="w-5 h-5 text-[#2563EB]" /> Today's Schedule</h3>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="(event, idx) in schedule" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-white rounded-full ring-4 ring-white border-2" :class="event.status === 'past' ? 'border-[#22C55E] bg-[#22C55E]' : event.status === 'current' ? 'border-[#2563EB] bg-[#2563EB] ring-[#2563EB]/20' : 'border-slate-300'"></div>
                    <p class="text-sm font-bold text-slate-900" :class="{'text-slate-400': event.status === 'past'}">{{ event.title }}</p>
                    <p class="text-xs font-medium" :class="event.status === 'past' ? 'text-slate-400' : 'text-[#2563EB]'">{{ event.time }}</p>
                  </div>
                </div>
              </div>

              <!-- Deadline Monitor -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Clock class="w-5 h-5 text-amber-500" /> Deadline Monitor</h3>
                <div class="space-y-3">
                  <div class="flex items-center justify-between p-3 rounded-xl bg-red-50 border border-red-100">
                    <span class="text-sm font-bold text-red-700 flex items-center gap-2"><AlertTriangle class="w-4 h-4"/> Overdue</span>
                    <span class="text-lg font-bold text-red-700">1</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-xl bg-amber-50 border border-amber-100">
                    <span class="text-sm font-bold text-amber-700">Due Today</span>
                    <span class="text-lg font-bold text-amber-700">3</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-xl bg-blue-50 border border-blue-100">
                    <span class="text-sm font-bold text-blue-700">Due Tomorrow</span>
                    <span class="text-lg font-bold text-blue-700">2</span>
                  </div>
                </div>
              </div>

              <!-- Performance Summary -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Activity class="w-5 h-5 text-purple-500" /> Performance Summary</h3>
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p class="text-[10px] font-bold text-slate-500 uppercase mb-1">Completed (Week)</p>
                    <p class="text-xl font-bold text-slate-900">14</p>
                  </div>
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p class="text-[10px] font-bold text-slate-500 uppercase mb-1">Avg Resol. Time</p>
                    <p class="text-xl font-bold text-slate-900">6.5h</p>
                  </div>
                </div>
                <div class="flex items-center justify-between p-3 bg-green-50 rounded-xl border border-green-100">
                  <span class="text-sm font-bold text-green-700">Performance Score</span>
                  <span class="text-lg font-bold text-green-700 flex items-center gap-1">94 <Award class="w-4 h-4"/></span>
                </div>
              </div>

              <!-- Quick Navigation -->
              <div class="grid grid-cols-2 gap-3">
                <button class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <CheckCircle class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Completed Tasks</span>
                </button>
                <button class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <Bell class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Notifications</span>
                </button>
              </div>

            </div>
          </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  ClipboardList, CheckCircle, Clock, Calendar, MapPin, AlertTriangle, 
  Wrench, Truck, Users, UserCheck, Building, Activity, Play, Pause, 
  Flag, Image as ImageIcon, FileText, Search, Filter, LayoutGrid, List,
  Award, Bell, ArrowRight
} from 'lucide-vue-next'

// --- State ---
const isSidebarOpen = ref(false)
const viewMode = ref('grid') // 'grid' | 'list'
const expandedTask = ref(null)

const filters = reactive({
  search: '',
  status: 'All',
  priority: 'All',
  sort: 'Priority'
})

// --- Mock Data ---
const summaryStats = [
  { title: 'Total Assigned', value: '12', icon: ClipboardList, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Pending (To Accept)', value: '2', icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'In Progress', value: '3', icon: Activity, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { title: 'Completed Today', value: '4', trend: 2, icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'High Priority', value: '3', trend: -1, icon: Flag, iconBg: 'bg-orange-50', iconColor: 'text-orange-500' },
  { title: 'Overdue', value: '1', icon: AlertTriangle, iconBg: 'bg-red-50', iconColor: 'text-red-600' }
]

const tasks = [
  { id: 'CMP-8902', title: 'Fallen Live Wire near Park', category: 'Electrical', priority: 'Emergency', status: 'Travelling', area: 'Downtown Sector 4', ward: 'Ward 14', dateAssigned: 'Jul 09, 2026', deadline: 'Today, 12:00 PM', officer: 'Officer S. Patel', description: 'Extremely dangerous live wire fallen on the main pedestrian walkway. Isolate the area immediately.', image: 'https://images.unsplash.com/photo-1544257121-654dbbc305e7?w=150&h=150&fit=crop', instructions: 'Priority 1. Ensure safety gear is worn. Wait for power grid shutdown confirmation before handling.', materials: ['Safety Gloves Class 2', 'Warning Cones', 'Insulation Tape', 'Barricade Tape'] },
  { id: 'CMP-8875', title: 'Deep Pothole causing traffic', category: 'Road Maintenance', priority: 'High', status: 'In Progress', area: 'MG Road', ward: 'Ward 12', dateAssigned: 'Jul 08, 2026', deadline: 'Today, 05:00 PM', officer: 'Officer R. Kumar', description: 'Large pothole developed after recent rains causing severe traffic jams during peak hours.', image: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=150&h=150&fit=crop', instructions: 'Clear debris, apply cold mix asphalt, and compact thoroughly. Ensure traffic flow is managed.', materials: ['Cold Mix Asphalt', 'Compactor', 'Warning Cones'] },
  { id: 'CMP-8850', title: 'Blocked Drainage outside Metro Station', category: 'Drainage', priority: 'Medium', status: 'Assigned', area: 'North Zone', ward: 'Ward 8', dateAssigned: 'Jul 08, 2026', deadline: 'Tomorrow, 10:00 AM', officer: 'Officer P. Sharma', description: 'Water logging reported due to blocked storm water drain. Needs immediate clearing before next rain.', image: 'https://images.unsplash.com/photo-1584985614946-bdeeb2bc4db1?w=150&h=150&fit=crop', instructions: 'Use jetting machine to clear blockages. Remove silt and solid waste from the drain cover.', materials: ['Jetting Machine', 'Gum Boots', 'Silt Shovel'] },
  { id: 'CMP-8812', title: 'Overflowing public dustbin', category: 'Garbage', priority: 'Low', status: 'Work Started', area: 'South Suburbs', ward: 'Ward 2', dateAssigned: 'Jul 07, 2026', deadline: 'Today, 02:00 PM', officer: 'Officer R. Kumar', description: 'Dustbin overflowing and spreading bad odor in the residential area. Needs emptying and sanitization.', image: 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=150&h=150&fit=crop', instructions: 'Empty bin into compactor truck. Spray area with municipal sanitizer powder.', materials: ['Garbage Truck', 'Sanitizer Powder', 'Gloves'] },
]

const schedule = [
  { title: 'Morning Briefing', time: '08:30 AM', status: 'past' },
  { title: 'CMP-8902: Live Wire (Emergency)', time: '09:00 AM', status: 'current' },
  { title: 'CMP-8812: Garbage Clearance', time: '11:30 AM', status: 'upcoming' },
  { title: 'CMP-8875: Pothole Repair', time: '02:00 PM', status: 'upcoming' },
  { title: 'Shift End / Report Submission', time: '05:30 PM', status: 'upcoming' },
]

// --- Computed & Methods ---
const filteredTasks = computed(() => {
  let result = tasks

  // Search
  if (filters.search) {
    const q = filters.search.toLowerCase()
    result = result.filter(t => t.id.toLowerCase().includes(q) || t.title.toLowerCase().includes(q) || t.area.toLowerCase().includes(q))
  }
  
  // Filters
  if (filters.status !== 'All') result = result.filter(t => t.status === filters.status)
  if (filters.priority !== 'All') result = result.filter(t => t.priority === filters.priority)

  // Sort
  if (filters.sort === 'Priority') {
    const pOrder = { 'Emergency': 1, 'High': 2, 'Medium': 3, 'Low': 4 }
    result.sort((a, b) => pOrder[a.priority] - pOrder[b.priority])
  } else if (filters.sort === 'Newest') {
    result.sort((a, b) => a.id < b.id ? 1 : -1)
  }

  // Always bring Emergency to top
  return result.sort((a, b) => (a.priority === 'Emergency' ? -1 : (b.priority === 'Emergency' ? 1 : 0)))
})

const toggleExpand = (id) => { expandedTask.value = expandedTask.value === id ? null : id }

const isOverdue = (deadline) => deadline.toLowerCase().includes('today') // Simplified logic for UI

const getProgress = (status) => {
  const map = { 'Assigned': 10, 'Accepted': 25, 'Travelling': 40, 'Work Started': 60, 'In Progress': 80, 'Waiting for Material': 60, 'Completed': 100 }
  return map[status] || 0
}

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700 border border-red-200', 'High': 'bg-orange-100 text-orange-700 border border-orange-200', 'Medium': 'bg-blue-100 text-blue-700 border border-blue-200', 'Low': 'bg-slate-100 text-slate-600 border border-slate-200' }
  return map[priority]
}

const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'Travelling': 'bg-indigo-100 text-indigo-700', 'Work Started': 'bg-purple-100 text-purple-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Completed': 'bg-green-100 text-green-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

// Action button logic
const actionButtonTheme = (status) => {
  if (status === 'Assigned') return 'bg-[#2563EB] hover:bg-[#1E40AF]'
  if (status === 'Travelling' || status === 'Work Started' || status === 'In Progress') return 'bg-[#F59E0B] hover:bg-amber-600'
  return 'bg-slate-300 text-slate-500 cursor-not-allowed'
}
const actionButtonText = (status) => {
  if (status === 'Assigned') return 'Accept Task'
  if (status === 'Accepted') return 'Start Travel'
  if (status === 'Travelling') return 'Start Work'
  if (status === 'Work Started' || status === 'In Progress') return 'Update Status'
  return 'Completed'
}
const actionButtonIcon = (status) => {
  if (status === 'Assigned') return CheckCircle
  if (status === 'Travelling') return Truck
  if (status === 'Work Started' || status === 'In Progress') return Play
  return CheckCircle
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>