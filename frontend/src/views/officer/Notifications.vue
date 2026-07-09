<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Sidebar Placeholder -->
    <Sidebar userRole="Civic Officer" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      
      <!-- Navbar Placeholder -->
      <DashboardNavbar userRole="Civic Officer" pageTitle="Notification Center" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1600px] mx-auto space-y-6">
          
          <!-- Header & Breadcrumbs -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Notifications</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Notification Center</h1>
              <p class="text-slate-500 mt-1">Stay informed about complaint activities, worker updates, system alerts, and operational events.</p>
            </div>
            <div class="flex gap-2">
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-2 shadow-sm">
                <Settings class="w-4 h-4 text-slate-500" /> Preferences
              </button>
            </div>
          </div>

          <!-- Emergency Alerts Banner -->
          <div v-if="emergencyAlerts.length > 0" class="bg-red-50 border border-red-200 rounded-[14px] p-5 shadow-sm animate-fade-in relative overflow-hidden">
            <div class="absolute top-0 left-0 w-1.5 h-full bg-red-500"></div>
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 class="text-red-700 font-bold flex items-center gap-2 mb-1">
                  <AlertTriangle class="w-5 h-5" /> Emergency Action Required ({{ emergencyAlerts.length }})
                </h3>
                <p class="text-red-600 text-sm">You have unresolved emergency complaints that require immediate assignment or verification.</p>
              </div>
              <button @click="activeTab = 'Emergency'" class="px-4 py-2 bg-red-600 text-white text-sm font-bold rounded-lg hover:bg-red-700 transition-colors shadow-sm whitespace-nowrap">
                Review Emergencies
              </button>
            </div>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div v-for="stat in summaryStats" :key="stat.title" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:shadow-md transition-shadow flex flex-col justify-between">
              <div class="flex justify-between items-start mb-3">
                <div :class="`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor}`">
                  <component :is="stat.icon" class="w-5 h-5" />
                </div>
                <span v-if="stat.trend" :class="`text-[10px] font-bold px-1.5 py-0.5 rounded ${stat.trend > 0 ? 'bg-green-50 text-green-600' : 'bg-slate-100 text-slate-500'}`">
                  {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}
                </span>
              </div>
              <div>
                <p class="text-2xl font-extrabold text-slate-900">{{ stat.value }}</p>
                <p class="text-xs font-semibold text-slate-500 mt-0.5">{{ stat.title }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Column: Search, Filters & Quick Links -->
            <div class="lg:col-span-3 space-y-6">
              
              <!-- Search & Filters -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Search class="w-4 h-4 text-[#2563EB]" /> Search & Filter</h3>
                
                <div class="space-y-4">
                  <div class="relative">
                    <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                    <input 
                      v-model="searchQuery"
                      type="text" 
                      placeholder="Search ID, keyword, name..." 
                      class="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Priority</label>
                    <select v-model="filters.priority" class="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                      <option value="All">All Priorities</option>
                      <option value="Emergency">Emergency</option>
                      <option value="High">High</option>
                      <option value="Medium">Medium</option>
                      <option value="Low">Low</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Timeframe</label>
                    <select v-model="filters.date" class="w-full bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                      <option value="All">All Time</option>
                      <option value="Today">Today</option>
                      <option value="Week">This Week</option>
                      <option value="Month">This Month</option>
                    </select>
                  </div>
                </div>

                <div class="mt-5 pt-4 border-t border-slate-100 flex gap-2">
                  <button @click="resetFilters" class="flex-1 py-2 text-sm font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">Reset</button>
                </div>
              </div>

              <!-- Notification Preferences -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 hidden lg:block">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Settings class="w-4 h-4 text-slate-400" /> Preferences</h3>
                <div class="space-y-3">
                  <label class="flex items-center justify-between cursor-pointer">
                    <span class="text-sm font-medium text-slate-700">Complaint Alerts</span>
                    <div class="relative inline-flex items-center">
                      <input type="checkbox" v-model="prefs.complaint" class="sr-only peer">
                      <div class="w-9 h-5 bg-slate-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#2563EB]"></div>
                    </div>
                  </label>
                  <label class="flex items-center justify-between cursor-pointer">
                    <span class="text-sm font-medium text-slate-700">Worker Updates</span>
                    <div class="relative inline-flex items-center">
                      <input type="checkbox" v-model="prefs.worker" class="sr-only peer">
                      <div class="w-9 h-5 bg-slate-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#2563EB]"></div>
                    </div>
                  </label>
                  <label class="flex items-center justify-between cursor-pointer">
                    <span class="text-sm font-medium text-slate-700">Emergency Push</span>
                    <div class="relative inline-flex items-center">
                      <input type="checkbox" v-model="prefs.emergency" class="sr-only peer">
                      <div class="w-9 h-5 bg-slate-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#2563EB]"></div>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 hidden lg:block">
                <h3 class="font-bold text-slate-900 mb-4">Quick Links</h3>
                <div class="space-y-2">
                  <button class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <Clipboard class="w-4 h-4" /> Complaint Management
                  </button>
                  <button class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <Activity class="w-4 h-4" /> Open Analytics
                  </button>
                  <button class="w-full text-left px-3 py-2 text-sm text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-2">
                    <Users class="w-4 h-4" /> Manage Workers
                  </button>
                </div>
              </div>

            </div>

            <!-- Right Column: Notifications Feed -->
            <div class="lg:col-span-9 flex flex-col h-full bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
              
              <!-- Tabs -->
              <div class="border-b border-slate-100 bg-slate-50/50 flex overflow-x-auto no-scrollbar px-2">
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
              <div v-if="selectedIds.length > 0" class="bg-[#2563EB]/10 border-b border-[#2563EB]/20 px-4 py-2 flex items-center justify-between animate-fade-in">
                <span class="text-sm font-bold text-[#1E40AF]">{{ selectedIds.length }} selected</span>
                <div class="flex gap-2">
                  <button @click="markSelectedRead" class="px-3 py-1.5 bg-white text-xs font-bold text-slate-700 rounded border border-slate-200 hover:bg-slate-50 shadow-sm transition-colors">Mark as Read</button>
                  <button class="px-3 py-1.5 bg-white text-xs font-bold text-slate-700 rounded border border-slate-200 hover:bg-slate-50 shadow-sm transition-colors">Archive</button>
                  <button class="px-3 py-1.5 bg-red-50 text-xs font-bold text-red-600 rounded border border-red-100 hover:bg-red-100 shadow-sm transition-colors">Delete</button>
                </div>
              </div>

              <!-- List Header / Select All -->
              <div class="px-5 py-3 border-b border-slate-100 flex items-center justify-between bg-white shrink-0">
                <label class="flex items-center gap-3 cursor-pointer">
                  <input type="checkbox" :checked="isAllSelected" @change="toggleAll" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-600">Select All</span>
                </label>
                <button @click="markAllRead" class="text-xs font-bold text-[#2563EB] hover:underline">Mark all as read</button>
              </div>

              <!-- Notification List -->
              <div class="flex-1 overflow-y-auto bg-slate-50/30">
                <div class="divide-y divide-slate-100">
                  
                  <div 
                    v-for="notif in filteredNotifications" :key="notif.id" 
                    @click="openDrawer(notif)"
                    class="p-4 sm:p-5 flex items-start gap-4 hover:bg-slate-50 transition-colors cursor-pointer group relative"
                    :class="{'bg-white': notif.read, 'bg-blue-50/30': !notif.read}"
                  >
                    <!-- Unread Indicator -->
                    <div v-if="!notif.read" class="absolute left-0 top-0 bottom-0 w-1 bg-[#2563EB]"></div>

                    <!-- Checkbox -->
                    <div class="mt-1 shrink-0" @click.stop>
                      <input type="checkbox" v-model="selectedIds" :value="notif.id" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                    </div>

                    <!-- Icon -->
                    <div :class="`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${typeColors(notif.type).bg} ${typeColors(notif.type).text}`">
                      <component :is="typeIcon(notif.type)" class="w-5 h-5" />
                    </div>

                    <!-- Content -->
                    <div class="flex-1 min-w-0">
                      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1">
                        <div class="flex items-center gap-2 flex-wrap">
                          <h4 class="text-sm font-bold text-slate-900 group-hover:text-[#2563EB] transition-colors line-clamp-1">{{ notif.title }}</h4>
                          <span v-if="notif.complaintId" class="px-2 py-0.5 rounded bg-slate-100 text-[10px] font-bold text-slate-600 border border-slate-200 font-mono">{{ notif.complaintId }}</span>
                          <span v-if="notif.priority === 'Emergency'" class="px-2 py-0.5 rounded bg-red-100 text-red-700 text-[10px] font-bold border border-red-200 uppercase tracking-wider">Emergency</span>
                        </div>
                        <span class="text-xs font-medium text-slate-400 shrink-0">{{ notif.time }}</span>
                      </div>
                      
                      <p class="text-sm text-slate-600 line-clamp-2 mb-2">{{ notif.description }}</p>
                      
                      <div class="flex items-center gap-3 text-xs text-slate-500 font-medium flex-wrap">
                        <span v-if="notif.category" class="flex items-center gap-1"><FileText class="w-3.5 h-3.5"/> {{ notif.category }}</span>
                        <span v-if="notif.area" class="flex items-center gap-1"><MapPin class="w-3.5 h-3.5"/> {{ notif.area }}</span>
                        <span v-if="notif.worker" class="flex items-center gap-1"><UserCheck class="w-3.5 h-3.5"/> {{ notif.worker }}</span>
                        <span v-if="notif.citizen" class="flex items-center gap-1"><Users class="w-3.5 h-3.5"/> {{ notif.citizen }}</span>
                      </div>
                    </div>

                    <!-- Quick Hover Actions -->
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
                  <div v-if="filteredNotifications.length === 0" class="p-12 text-center text-slate-500 bg-white">
                    <Bell class="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <p class="font-bold text-slate-900">No notifications found</p>
                    <p class="text-sm mt-1">Try adjusting your filters or search query.</p>
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
          
          <div class="p-6 border-b border-slate-100 flex justify-between items-start bg-slate-50">
            <div class="flex items-center gap-3">
              <div :class="`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${typeColors(activeNotif.type).bg} ${typeColors(activeNotif.type).text}`">
                <component :is="typeIcon(activeNotif.type)" class="w-5 h-5" />
              </div>
              <div>
                <h2 class="text-lg font-bold text-slate-900 leading-tight">{{ activeNotif.type }} Notification</h2>
                <p class="text-xs text-slate-500 mt-0.5">{{ activeNotif.date }} at {{ activeNotif.time }}</p>
              </div>
            </div>
            <button @click="closeDrawer" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6 space-y-6">
            
            <div>
              <h3 class="text-xl font-bold text-slate-900 mb-2">{{ activeNotif.title }}</h3>
              <p class="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100">
                {{ activeNotif.description }}
              </p>
            </div>

            <!-- Complaint Meta (If applicable) -->
            <div v-if="activeNotif.complaintId" class="space-y-4">
              <h4 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Related Complaint</h4>
              <div class="grid grid-cols-2 gap-3 text-sm">
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <p class="text-xs text-slate-500 font-bold mb-1">ID</p>
                  <p class="font-mono font-medium text-[#2563EB]">{{ activeNotif.complaintId }}</p>
                </div>
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <p class="text-xs text-slate-500 font-bold mb-1">Priority</p>
                  <p class="font-bold" :class="activeNotif.priority === 'Emergency' ? 'text-red-600' : 'text-slate-700'">{{ activeNotif.priority || 'Medium' }}</p>
                </div>
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <p class="text-xs text-slate-500 font-bold mb-1">Area</p>
                  <p class="font-medium text-slate-900 truncate">{{ activeNotif.area || 'N/A' }}</p>
                </div>
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <p class="text-xs text-slate-500 font-bold mb-1">Category</p>
                  <p class="font-medium text-slate-900 truncate">{{ activeNotif.category || 'N/A' }}</p>
                </div>
              </div>
            </div>

            <!-- Entities Involved -->
            <div v-if="activeNotif.worker || activeNotif.citizen" class="space-y-3 border-t border-slate-100 pt-6">
              <h4 class="font-bold text-slate-900 text-sm uppercase tracking-wider mb-2">People Involved</h4>
              <div v-if="activeNotif.worker" class="flex items-center gap-3 p-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer">
                <div class="w-8 h-8 rounded-full bg-purple-100 text-purple-700 flex items-center justify-center font-bold text-xs"><UserCheck class="w-4 h-4"/></div>
                <div>
                  <p class="text-xs text-slate-500 font-medium">Assigned Worker</p>
                  <p class="text-sm font-bold text-slate-900">{{ activeNotif.worker }}</p>
                </div>
              </div>
              <div v-if="activeNotif.citizen" class="flex items-center gap-3 p-3 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer">
                <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-xs"><Users class="w-4 h-4"/></div>
                <div>
                  <p class="text-xs text-slate-500 font-medium">Citizen</p>
                  <p class="text-sm font-bold text-slate-900">{{ activeNotif.citizen }}</p>
                </div>
              </div>
            </div>

            <!-- Action Timeline (Dummy representation) -->
            <div v-if="activeNotif.type === 'Complaint'" class="border-t border-slate-100 pt-6">
               <h4 class="font-bold text-slate-900 text-sm uppercase tracking-wider mb-4">Recent Activity</h4>
               <div class="relative pl-4 border-l-2 border-slate-100 space-y-4">
                  <div class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#2563EB] rounded-full ring-4 ring-white"></div>
                    <p class="text-sm font-bold text-slate-900">Notification Generated</p>
                    <p class="text-xs text-slate-500">{{ activeNotif.time }}</p>
                  </div>
               </div>
            </div>

          </div>
          
          <!-- Drawer Actions -->
          <div class="p-6 border-t border-slate-100 bg-white grid grid-cols-2 gap-3 shrink-0">
            <button v-if="!activeNotif.read" @click="toggleRead(activeNotif); closeDrawer()" class="py-2.5 border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors flex items-center justify-center gap-2 text-sm">
              <CheckCircle class="w-4 h-4" /> Mark Read
            </button>
            <button v-else @click="closeDrawer" class="py-2.5 border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors text-sm">
              Close
            </button>
            
            <router-link v-if="activeNotif.complaintId" :to="`/officer/details/${activeNotif.complaintId}`" class="py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex items-center justify-center gap-2 text-sm shadow-sm">
              <Eye class="w-4 h-4" /> Open Complaint
            </router-link>
            <button v-else class="py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex items-center justify-center gap-2 text-sm shadow-sm">
              <Activity class="w-4 h-4" /> Take Action
            </button>
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
  Bell, AlertTriangle, Clipboard, CheckCircle, Clock, MessageSquare, 
  Users, UserCheck, MapPin, Search, Filter, Eye, Activity, FileText, 
  Archive, Settings, X
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const drawerOpen = ref(false)
const activeNotif = ref(null)

const activeTab = ref('All')
const searchQuery = ref('')
const selectedIds = ref([])

const filters = reactive({
  priority: 'All',
  date: 'All'
})

const prefs = reactive({
  complaint: true,
  worker: true,
  emergency: true
})

// --- Mock Data ---
const summaryStats = [
  { title: 'Total Notifications', value: '1,248', icon: Bell, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Unread', value: '24', trend: 5, icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'High Priority', value: '12', icon: AlertTriangle, iconBg: 'bg-orange-50', iconColor: 'text-orange-500' },
  { title: 'Emergency', value: '2', icon: AlertTriangle, iconBg: 'bg-red-50', iconColor: 'text-red-600' },
  { title: 'New Assignments', value: '45', trend: 12, icon: Clipboard, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { title: 'Resolved Alerts', value: '180', trend: 20, icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' }
]

const tabs = [
  { name: 'All' },
  { name: 'Unread', count: 24 },
  { name: 'Emergency', count: 2 },
  { name: 'Complaints' },
  { name: 'Assignments' },
  { name: 'Feedback' },
  { name: 'System' }
]

const notifications = ref([
  { id: 'n1', type: 'Emergency', title: 'Live Wire Down - Immediate Action Required', description: 'Citizen reported a live electrical wire fallen on the main road. Severe safety hazard.', complaintId: 'CMP-8902', citizen: 'Priya Sharma', area: 'Ward 4, MG Road', category: 'Electrical', priority: 'Emergency', time: '10 mins ago', date: 'Jul 09, 2026', read: false },
  { id: 'n2', type: 'Assignment', title: 'Worker Accepted Assignment', description: 'Amit Singh has accepted the assignment and started work on the site.', complaintId: 'CMP-8845', worker: 'Amit Singh', area: 'Downtown', category: 'Pothole', priority: 'High', time: '1 hour ago', date: 'Jul 09, 2026', read: false },
  { id: 'n3', type: 'Complaint', title: 'New Complaint Submitted', description: 'Heavy garbage accumulation near the local park entrance. Foul smell affecting residents.', complaintId: 'CMP-8903', citizen: 'Rahul Verma', area: 'Sector 12', category: 'Sanitation', priority: 'Medium', time: '2 hours ago', date: 'Jul 09, 2026', read: false },
  { id: 'n4', type: 'Feedback', title: 'Citizen Submitted Feedback', description: 'Citizen gave a 5-star rating for the quick resolution of the streetlight issue.', complaintId: 'CMP-8710', citizen: 'Anjali Desai', worker: 'Suresh Patil', area: 'North Zone', category: 'Streetlight', priority: 'Low', time: '5 hours ago', date: 'Jul 09, 2026', read: true },
  { id: 'n5', type: 'System', title: 'Platform Maintenance Scheduled', description: 'CivicDesk will undergo routine maintenance tonight from 2:00 AM to 4:00 AM IST. Expect minor disruptions.', priority: 'Medium', time: '1 day ago', date: 'Jul 08, 2026', read: true },
  { id: 'n6', type: 'Assignment', title: 'Task Marked as Completed', description: 'Field worker has completed the drainage clearing task and uploaded evidence.', complaintId: 'CMP-8655', worker: 'Vikram Jadhav', area: 'South Ward', category: 'Drainage', priority: 'High', time: '1 day ago', date: 'Jul 08, 2026', read: true }
])

// --- Computed & Methods ---
const emergencyAlerts = computed(() => notifications.value.filter(n => n.type === 'Emergency' && !n.read))

const filteredNotifications = computed(() => {
  let result = notifications.value

  // Tab Filter
  if (activeTab.value === 'Unread') result = result.filter(n => !n.read)
  else if (activeTab.value === 'Emergency') result = result.filter(n => n.type === 'Emergency')
  else if (activeTab.value === 'Complaints') result = result.filter(n => n.type === 'Complaint')
  else if (activeTab.value === 'Assignments') result = result.filter(n => n.type === 'Assignment')
  else if (activeTab.value === 'Feedback') result = result.filter(n => n.type === 'Feedback')
  else if (activeTab.value === 'System') result = result.filter(n => n.type === 'System')

  // Search Filter
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(n => 
      n.title.toLowerCase().includes(q) || 
      (n.complaintId && n.complaintId.toLowerCase().includes(q)) ||
      (n.citizen && n.citizen.toLowerCase().includes(q)) ||
      (n.worker && n.worker.toLowerCase().includes(q)) ||
      (n.area && n.area.toLowerCase().includes(q))
    )
  }

  // Dropdown Filters
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
  notifications.value.forEach(n => {
    if (selectedIds.value.includes(n.id)) n.read = true
  })
  selectedIds.value = []
}
const markAllRead = () => { notifications.value.forEach(n => n.read = true) }

const resetFilters = () => {
  searchQuery.value = ''
  filters.priority = 'All'
  filters.date = 'All'
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
    'Assignment': Clipboard,
    'Complaint': FileText,
    'Feedback': MessageSquare,
    'System': Activity
  }
  return map[type] || Bell
}

const typeColors = (type) => {
  const map = {
    'Emergency': { bg: 'bg-red-100', text: 'text-red-600' },
    'Assignment': { bg: 'bg-purple-100', text: 'text-purple-600' },
    'Complaint': { bg: 'bg-blue-100', text: 'text-[#2563EB]' },
    'Feedback': { bg: 'bg-green-100', text: 'text-green-600' },
    'System': { bg: 'bg-slate-200', text: 'text-slate-600' }
  }
  return map[type] || { bg: 'bg-slate-100', text: 'text-slate-500' }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}
.animate-slide-in {
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

/* Custom Scrollbar */
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