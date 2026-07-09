<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Sidebar Placeholder -->
    <Sidebar userRole="Field Worker" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      
      <!-- Navbar Placeholder -->
      <DashboardNavbar userRole="Field Worker" pageTitle="Notifications" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Header & Breadcrumbs -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Notifications</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Notification Center</h1>
              <p class="text-slate-500 mt-1">Stay updated with task assignments, reminders, verification results, and important announcements.</p>
            </div>
            <div class="flex gap-2">
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
                <Settings class="w-4 h-4 text-slate-500" /> Settings
              </button>
            </div>
          </div>

          <!-- Emergency Alerts Banner -->
          <div v-if="emergencyAlerts.length > 0" class="bg-red-50 border border-red-200 rounded-[14px] p-5 shadow-sm relative overflow-hidden">
            <div class="absolute top-0 left-0 w-1.5 h-full bg-red-500"></div>
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 class="text-red-700 font-bold flex items-center gap-2 mb-1">
                  <AlertTriangle class="w-5 h-5" /> Emergency Task Assigned ({{ emergencyAlerts.length }})
                </h3>
                <p class="text-red-600 text-sm">You have new high-priority emergency tasks that require immediate attention and travel.</p>
              </div>
              <button @click="activeTab = 'Emergency'" class="px-4 py-2 bg-red-600 text-white text-sm font-bold rounded-lg hover:bg-red-700 transition-colors shadow-sm whitespace-nowrap">
                View Emergencies
              </button>
            </div>
          </div>

          <!-- Summary Stats -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div v-for="stat in summaryStats" :key="stat.title" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
              <div class="flex justify-between items-start mb-3">
                <div :class="`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor}`">
                  <component :is="stat.icon" class="w-5 h-5" />
                </div>
              </div>
              <div>
                <p class="text-2xl font-extrabold text-slate-900">{{ stat.value }}</p>
                <p class="text-xs font-semibold text-slate-500 mt-0.5">{{ stat.title }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Column: Search, Filters, Prefs (3 cols) -->
            <div class="lg:col-span-3 space-y-6">
              
              <!-- Search & Filters -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Filter class="w-4 h-4 text-[#2563EB]" /> Search & Filter</h3>
                
                <div class="space-y-4">
                  <div class="relative">
                    <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                    <input 
                      v-model="filters.search"
                      type="text" 
                      placeholder="Search ID, title, or area..." 
                      class="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB] outline-none"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Notification Type</label>
                    <select v-model="filters.type" class="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                      <option value="All">All Types</option>
                      <option value="Assignment">Task Assigned</option>
                      <option value="Reminder">Task Reminder</option>
                      <option value="Message">Officer Message</option>
                      <option value="Verification">Verification Result</option>
                      <option value="System">System Announcement</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Priority</label>
                    <select v-model="filters.priority" class="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                      <option value="All">All Priorities</option>
                      <option value="Emergency">Emergency</option>
                      <option value="High">High</option>
                      <option value="Medium">Medium</option>
                      <option value="Low">Low</option>
                    </select>
                  </div>
                </div>

                <div class="mt-5 pt-4 border-t border-slate-100 flex gap-2">
                  <button @click="resetFilters" class="flex-1 py-2 text-sm font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">Reset</button>
                </div>
              </div>

              <!-- Preferences (UI Only) -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 hidden lg:block">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Settings class="w-4 h-4 text-slate-400" /> Preferences</h3>
                <div class="space-y-3">
                  <label v-for="(val, key) in prefs" :key="key" class="flex items-center justify-between cursor-pointer group">
                    <span class="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{{ formatKey(key) }}</span>
                    <div class="relative inline-flex items-center">
                      <input type="checkbox" v-model="prefs[key]" class="sr-only peer">
                      <div class="w-9 h-5 bg-slate-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#2563EB]"></div>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 hidden lg:block">
                <h3 class="font-bold text-slate-900 mb-4">Quick Links</h3>
                <div class="space-y-2">
                  <router-link to="/worker/tasks" class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <ClipboardList class="w-4 h-4" /> Assigned Tasks
                  </router-link>
                  <router-link to="/worker/completed" class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <CheckCircle class="w-4 h-4" /> Completed Tasks
                  </router-link>
                  <router-link to="/worker/profile" class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <UserCheck class="w-4 h-4" /> My Profile
                  </router-link>
                </div>
              </div>

            </div>

            <!-- Right Column: Notifications Feed (9 cols) -->
            <div class="lg:col-span-9 flex flex-col h-[calc(100vh-140px)] bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
              
              <!-- Tabs -->
              <div class="border-b border-slate-100 bg-slate-50/50 flex overflow-x-auto no-scrollbar px-2 shrink-0">
                <button 
                  v-for="tab in tabs" :key="tab.name" 
                  @click="activeTab = tab.name"
                  class="px-4 py-4 text-sm font-bold whitespace-nowrap border-b-2 transition-colors flex items-center gap-2"
                  :class="activeTab === tab.name ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-slate-500 hover:text-slate-700'"
                >
                  {{ tab.name }}
                  <span v-if="tab.count" :class="`px-1.5 py-0.5 rounded-full text-[10px] ${activeTab === tab.name ? 'bg-[#2563EB] text-white' : 'bg-slate-200 text-slate-600'}`">
                    {{ tab.count }}
                  </span>
                </button>
              </div>

              <!-- Bulk Actions Bar -->
              <div v-if="selectedIds.length > 0" class="bg-[#2563EB]/10 border-b border-[#2563EB]/20 px-4 py-2 flex items-center justify-between animate-fade-in shrink-0">
                <span class="text-sm font-bold text-[#1E40AF]">{{ selectedIds.length }} selected</span>
                <div class="flex gap-2">
                  <button @click="markSelectedRead" class="px-3 py-1.5 bg-white text-xs font-bold text-slate-700 rounded border border-slate-200 hover:bg-slate-50 shadow-sm transition-colors">Mark Read</button>
                  <button class="px-3 py-1.5 bg-white text-xs font-bold text-slate-700 rounded border border-slate-200 hover:bg-slate-50 shadow-sm transition-colors">Archive</button>
                  <button class="px-3 py-1.5 bg-red-50 text-xs font-bold text-red-600 rounded border border-red-100 hover:bg-red-100 shadow-sm transition-colors">Delete</button>
                </div>
              </div>

              <!-- List Header -->
              <div class="px-5 py-3 border-b border-slate-100 flex items-center justify-between bg-white shrink-0">
                <label class="flex items-center gap-3 cursor-pointer">
                  <input type="checkbox" :checked="isAllSelected" @change="toggleAll" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-600">Select All</span>
                </label>
                <button @click="markAllRead" class="text-xs font-bold text-[#2563EB] hover:underline">Mark all as read</button>
              </div>

              <!-- Feed -->
              <div class="flex-1 overflow-y-auto bg-slate-50/30">
                <div class="divide-y divide-slate-100">
                  
                  <div 
                    v-for="notif in filteredNotifications" :key="notif.id" 
                    @click="openDrawer(notif)"
                    class="p-4 sm:p-5 flex items-start gap-4 hover:bg-slate-50 transition-colors cursor-pointer group relative"
                    :class="{'bg-white': notif.read, 'bg-blue-50/30': !notif.read}"
                  >
                    <!-- Unread Bar -->
                    <div v-if="!notif.read" class="absolute left-0 top-0 bottom-0 w-1 bg-[#2563EB]"></div>

                    <!-- Checkbox -->
                    <div class="mt-1 shrink-0" @click.stop>
                      <input type="checkbox" v-model="selectedIds" :value="notif.id" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                    </div>

                    <!-- Icon -->
                    <div :class="`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${typeTheme(notif.type).bg} ${typeTheme(notif.type).text}`">
                      <component :is="typeIcon(notif.type)" class="w-5 h-5" />
                    </div>

                    <!-- Content -->
                    <div class="flex-1 min-w-0">
                      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1">
                        <div class="flex items-center gap-2 flex-wrap">
                          <h4 class="text-sm font-bold text-slate-900 group-hover:text-[#2563EB] transition-colors line-clamp-1">{{ notif.title }}</h4>
                          <span v-if="notif.taskId" class="px-2 py-0.5 rounded bg-white border border-slate-200 text-[10px] font-bold text-slate-600 font-mono">{{ notif.taskId }}</span>
                          <span v-if="notif.priority === 'Emergency'" class="px-2 py-0.5 rounded bg-red-100 text-red-700 text-[10px] font-bold border border-red-200 uppercase tracking-wider">Emergency</span>
                        </div>
                        <span class="text-xs font-medium text-slate-400 shrink-0">{{ notif.time }}</span>
                      </div>
                      
                      <!-- Message Body -->
                      <div v-if="notif.type === 'Message'" class="bg-white border border-slate-200 rounded-lg p-3 my-2 shadow-sm relative">
                        <div class="absolute -left-1.5 top-3 w-3 h-3 bg-white border-l border-b border-slate-200 transform rotate-45"></div>
                        <p class="text-sm text-slate-700 italic">"{{ notif.description }}"</p>
                        <p class="text-[10px] font-bold text-slate-500 mt-2 uppercase tracking-wide">— Officer {{ notif.officer }}</p>
                      </div>
                      <p v-else class="text-sm text-slate-600 line-clamp-2 mb-2">{{ notif.description }}</p>
                      
                      <!-- Meta Tags -->
                      <div class="flex items-center gap-3 text-xs text-slate-500 font-medium flex-wrap">
                        <span v-if="notif.area" class="flex items-center gap-1"><MapPin class="w-3.5 h-3.5"/> {{ notif.area }}</span>
                        <span v-if="notif.category" class="flex items-center gap-1"><FileText class="w-3.5 h-3.5"/> {{ notif.category }}</span>
                        <span v-if="notif.officer && notif.type !== 'Message'" class="flex items-center gap-1"><UserCheck class="w-3.5 h-3.5"/> Officer: {{ notif.officer }}</span>
                      </div>
                    </div>

                    <!-- Quick Actions Hover -->
                    <div class="hidden sm:flex opacity-0 group-hover:opacity-100 transition-opacity gap-2 shrink-0">
                      <button @click.stop="toggleRead(notif)" class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded" :title="notif.read ? 'Mark Unread' : 'Mark Read'">
                        <CheckCircle class="w-4 h-4" />
                      </button>
                      <button @click.stop class="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-200 rounded" title="Archive">
                        <Archive class="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <!-- Empty State -->
                  <div v-if="filteredNotifications.length === 0" class="p-12 text-center text-slate-500 bg-white h-full flex flex-col justify-center items-center">
                    <Bell class="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <p class="font-bold text-slate-900">All caught up!</p>
                    <p class="text-sm mt-1">No notifications match your current filters.</p>
                  </div>

                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>

    <!-- Notification Details Drawer -->
    <Teleport to="body">
      <div v-if="drawerOpen && activeNotif" class="fixed inset-0 z-50 bg-slate-900/30 backdrop-blur-sm flex justify-end animate-fade-in" @click="closeDrawer">
        <div class="w-full max-w-md bg-white h-full shadow-2xl flex flex-col transform transition-transform animate-slide-in" @click.stop>
          
          <div class="p-6 border-b border-slate-100 flex justify-between items-start bg-slate-50 shrink-0">
            <div class="flex items-center gap-3">
              <div :class="`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${typeTheme(activeNotif.type).bg} ${typeTheme(activeNotif.type).text}`">
                <component :is="typeIcon(activeNotif.type)" class="w-5 h-5" />
              </div>
              <div>
                <h2 class="text-lg font-bold text-slate-900 leading-tight">{{ activeNotif.type }}</h2>
                <p class="text-xs text-slate-500 mt-0.5">{{ activeNotif.date }} at {{ activeNotif.time }}</p>
              </div>
            </div>
            <button @click="closeDrawer" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6 space-y-6">
            
            <div>
              <h3 class="text-xl font-bold text-slate-900 mb-2">{{ activeNotif.title }}</h3>
              <div :class="`text-sm text-slate-700 leading-relaxed p-4 rounded-xl border ${activeNotif.type === 'Message' ? 'bg-blue-50 border-blue-100 italic' : 'bg-slate-50 border-slate-100'}`">
                <span v-if="activeNotif.type === 'Message'" class="font-bold text-[#1E40AF] block mb-1">Message from Officer {{ activeNotif.officer }}:</span>
                "{{ activeNotif.description }}"
              </div>
            </div>

            <!-- Task Meta -->
            <div v-if="activeNotif.taskId" class="space-y-4 border-t border-slate-100 pt-6">
              <h4 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Related Task Context</h4>
              <div class="grid grid-cols-2 gap-3 text-sm">
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <p class="text-xs text-slate-500 font-bold mb-1">Task ID</p>
                  <p class="font-mono font-medium text-[#2563EB]">{{ activeNotif.taskId }}</p>
                </div>
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <p class="text-xs text-slate-500 font-bold mb-1">Priority</p>
                  <p class="font-bold" :class="activeNotif.priority === 'Emergency' ? 'text-red-600' : 'text-slate-700'">{{ activeNotif.priority || 'Medium' }}</p>
                </div>
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-100 col-span-2">
                  <p class="text-xs text-slate-500 font-bold mb-1">Location</p>
                  <p class="font-medium text-slate-900">{{ activeNotif.area || 'N/A' }}</p>
                </div>
              </div>
            </div>

            <!-- Contextual Actions depending on type -->
            <div v-if="activeNotif.type === 'Verification'" class="bg-green-50 p-4 rounded-xl border border-green-100">
              <div class="flex items-center gap-2 mb-2">
                <Shield class="w-5 h-5 text-green-600" />
                <h4 class="font-bold text-green-800">Verification Approved</h4>
              </div>
              <p class="text-sm text-green-700">Your submitted work has been reviewed and verified successfully. The task is now closed.</p>
            </div>

          </div>
          
          <div class="p-6 border-t border-slate-100 bg-white grid grid-cols-2 gap-3 shrink-0">
            <button v-if="!activeNotif.read" @click="toggleRead(activeNotif); closeDrawer()" class="py-2.5 border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors flex items-center justify-center gap-2 text-sm">
              <CheckCircle class="w-4 h-4" /> Mark Read
            </button>
            <button v-else @click="closeDrawer" class="py-2.5 border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors text-sm">
              Close
            </button>
            
            <router-link v-if="activeNotif.taskId" :to="`/worker/task/${activeNotif.taskId}`" class="py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex items-center justify-center gap-2 text-sm shadow-sm">
              <ClipboardList class="w-4 h-4" /> Open Task
            </router-link>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Bell, ClipboardList, CheckCircle, AlertTriangle, Clock, Calendar, 
  MessageSquare, Shield, UserCheck, Activity, FileText, Archive, 
  Eye, Search, Filter, Megaphone, Flag, MapPin, X, Settings
} from 'lucide-vue-next'

// --- State ---
const isSidebarOpen = ref(false)
const drawerOpen = ref(false)
const activeNotif = ref(null)
const activeTab = ref('All')
const searchQuery = ref('')
const selectedIds = ref([])

const filters = reactive({
  type: 'All',
  priority: 'All'
})

const prefs = reactive({
  assignments: true,
  emergencies: true,
  reminders: true,
  messages: true,
  verifications: true,
  announcements: false
})
const formatKey = (key) => key.charAt(0).toUpperCase() + key.slice(1) + ' Alerts'

// --- Mock Data ---
const summaryStats = [
  { title: 'Total Notifications', value: '45', icon: Bell, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Unread', value: '5', icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Task Updates', value: '12', icon: Activity, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { title: 'Emergency Alerts', value: '2', icon: AlertTriangle, iconBg: 'bg-red-50', iconColor: 'text-red-600' },
  { title: 'Today', value: '8', icon: Calendar, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'Archived', value: '120', icon: Archive, iconBg: 'bg-slate-100', iconColor: 'text-slate-500' }
]

const tabs = [
  { name: 'All' },
  { name: 'Unread', count: 5 },
  { name: 'Emergency', count: 2 },
  { name: 'Assignments' },
  { name: 'Messages' },
  { name: 'Announcements' }
]

const notifications = ref([
  { id: 'n1', type: 'Emergency', title: 'Emergency Task Assigned', description: 'Live wire fallen on pedestrian walkway. Immediate isolation required. Do not delay.', taskId: 'CMP-8902', area: 'Downtown Sector 4', category: 'Electrical', officer: 'Rahul Sharma', priority: 'Emergency', time: '10 mins ago', date: 'Jul 09, 2026', read: false },
  { id: 'n2', type: 'Assignment', title: 'New Task Assigned: Pothole Repair', description: 'You have been assigned to repair a deep pothole on MG road causing severe traffic.', taskId: 'CMP-8875', area: 'MG Road', category: 'Road Damage', officer: 'Priya Desai', priority: 'High', time: '1 hour ago', date: 'Jul 09, 2026', read: false },
  { id: 'n3', type: 'Message', title: 'New Message from Officer', description: 'Please make sure to bring extra cement for the drainage repair. The damage is worse than reported.', taskId: 'CMP-8850', area: 'North Zone', category: 'Drainage', officer: 'Rahul Sharma', priority: 'Medium', time: '3 hours ago', date: 'Jul 09, 2026', read: false },
  { id: 'n4', type: 'Reminder', title: 'Deadline Approaching', description: 'Task CMP-8812 (Garbage Clearance) is due in 2 hours. Please update status.', taskId: 'CMP-8812', area: 'South Suburbs', category: 'Garbage', officer: 'System', priority: 'Medium', time: '5 hours ago', date: 'Jul 09, 2026', read: true },
  { id: 'n5', type: 'Verification', title: 'Task Verification Approved', description: 'Your submitted work for CMP-8799 has been verified and approved by the officer. Excellent job.', taskId: 'CMP-8799', area: 'Ward 2', category: 'Streetlight', officer: 'Amit Singh', priority: 'Low', time: '1 day ago', date: 'Jul 08, 2026', read: true },
  { id: 'n6', type: 'System', title: 'Platform Maintenance Notice', description: 'CivicDesk will undergo routine maintenance tonight from 2:00 AM to 4:00 AM IST. Offline mode will be available.', officer: 'Admin', priority: 'Low', time: '1 day ago', date: 'Jul 08, 2026', read: true }
])

// --- Computed & Methods ---
const emergencyAlerts = computed(() => notifications.value.filter(n => n.type === 'Emergency' && !n.read))

const filteredNotifications = computed(() => {
  let result = notifications.value

  // Tabs
  if (activeTab.value === 'Unread') result = result.filter(n => !n.read)
  else if (activeTab.value === 'Emergency') result = result.filter(n => n.type === 'Emergency')
  else if (activeTab.value === 'Assignments') result = result.filter(n => n.type === 'Assignment')
  else if (activeTab.value === 'Messages') result = result.filter(n => n.type === 'Message')
  else if (activeTab.value === 'Announcements') result = result.filter(n => n.type === 'System')

  // Search
  if (filters.search) {
    const q = filters.search.toLowerCase()
    result = result.filter(n => 
      n.title.toLowerCase().includes(q) || 
      (n.taskId && n.taskId.toLowerCase().includes(q)) ||
      (n.officer && n.officer.toLowerCase().includes(q)) ||
      (n.area && n.area.toLowerCase().includes(q))
    )
  }

  // Dropdown Filters
  if (filters.type !== 'All') result = result.filter(n => n.type === filters.type)
  if (filters.priority !== 'All') result = result.filter(n => n.priority === filters.priority)

  return result
})

const isAllSelected = computed(() => filteredNotifications.value.length > 0 && selectedIds.value.length === filteredNotifications.value.length)

const toggleAll = (e) => {
  if (e.target.checked) selectedIds.value = filteredNotifications.value.map(n => n.id)
  else selectedIds.value = []
}

const toggleRead = (notif) => { notif.read = !notif.read }
const markSelectedRead = () => {
  notifications.value.forEach(n => { if (selectedIds.value.includes(n.id)) n.read = true })
  selectedIds.value = []
}
const markAllRead = () => { notifications.value.forEach(n => n.read = true) }

const resetFilters = () => {
  filters.search = ''
  filters.type = 'All'
  filters.priority = 'All'
}

const openDrawer = (notif) => {
  activeNotif.value = notif
  drawerOpen.value = true
}

const closeDrawer = () => {
  drawerOpen.value = false
  setTimeout(() => activeNotif.value = null, 300)
}

// Visual Helpers
const typeIcon = (type) => {
  const map = {
    'Emergency': AlertTriangle,
    'Assignment': ClipboardList,
    'Message': MessageSquare,
    'Reminder': Clock,
    'Verification': Shield,
    'System': Megaphone
  }
  return map[type] || Bell
}

const typeTheme = (type) => {
  const map = {
    'Emergency': { bg: 'bg-red-100', text: 'text-red-600' },
    'Assignment': { bg: 'bg-purple-100', text: 'text-purple-600' },
    'Message': { bg: 'bg-blue-100', text: 'text-[#2563EB]' },
    'Reminder': { bg: 'bg-amber-100', text: 'text-amber-600' },
    'Verification': { bg: 'bg-green-100', text: 'text-green-600' },
    'System': { bg: 'bg-slate-200', text: 'text-slate-600' }
  }
  return map[type] || { bg: 'bg-slate-100', text: 'text-slate-500' }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
.animate-slide-in { animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }

.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>