<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Completed Tasks</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Completed Tasks Archive</h1>
              <p class="text-slate-500 mt-1">Review completed work, verification status, and performance history.</p>
            </div>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
            <div v-for="stat in summaryStats" :key="stat.title" class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow group">
              <div class="flex justify-between items-start mb-2">
                <div :class="`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor}`">
                  <component :is="stat.icon" class="w-4 h-4" />
                </div>
                <span v-if="stat.trend" :class="`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${stat.trend > 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`">
                  {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
                </span>
              </div>
              <p class="text-2xl font-extrabold text-slate-900">{{ stat.value }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5 leading-tight">{{ stat.title }}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <!-- Left Column: Archive & List (8 cols) -->
            <div class="xl:col-span-8 flex flex-col gap-6">
              
              <!-- Toolbar -->
              <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 justify-between items-center z-10">
                <div class="relative w-full lg:w-72 shrink-0">
                  <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input 
                    v-model="filters.search"
                    type="text" 
                    placeholder="Search ID, title, or area..." 
                    class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none transition-all"
                  />
                </div>
                
                <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
                  <select v-model="filters.verification" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                    <option value="All">All Statuses</option>
                    <option value="Verified">Verified</option>
                    <option value="Pending">Pending Verification</option>
                    <option value="Rejected">Rejected</option>
                  </select>

                  <select v-model="filters.category" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none">
                    <option value="All">All Categories</option>
                    <option value="Garbage">Garbage</option>
                    <option value="Streetlight">Streetlight</option>
                    <option value="Road Damage">Road Damage</option>
                    <option value="Drainage">Drainage</option>
                  </select>

                  <select v-model="filters.sort" class="bg-white border border-slate-300 text-slate-900 font-medium text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 outline-none shadow-sm">
                    <option value="Newest">Newest First</option>
                    <option value="Rating">Highest Rating</option>
                    <option value="Fastest">Fastest Completion</option>
                  </select>

                  <div class="flex bg-slate-100 p-1 rounded-lg border border-slate-200 ml-auto lg:ml-2">
                    <button @click="viewMode = 'grid'" :class="`p-1.5 rounded-md transition-colors ${viewMode === 'grid' ? 'bg-white shadow-sm text-[#2563EB]' : 'text-slate-500 hover:text-slate-700'}`">
                      <LayoutGrid class="w-4 h-4" />
                    </button>
                    <button @click="viewMode = 'table'" :class="`p-1.5 rounded-md transition-colors ${viewMode === 'table' ? 'bg-white shadow-sm text-[#2563EB]' : 'text-slate-500 hover:text-slate-700'}`">
                      <List class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

              <!-- Task List -->
              <div v-if="filteredTasks.length > 0">
                
                <!-- GRID VIEW -->
                <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="task in filteredTasks" :key="task.id" class="bg-white rounded-2xl shadow-sm border border-slate-100 flex flex-col overflow-hidden transition-all duration-300 group hover:shadow-md">
                    <div class="p-4 md:p-5 flex-1">
                      <div class="flex justify-between items-start mb-4 gap-2">
                        <div>
                          <div class="flex items-center gap-2 mb-1">
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-600 font-mono">{{ task.id }}</span>
                            <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${verifyBadge(task.verification)}`">{{ task.verification }}</span>
                          </div>
                          <h3 class="font-bold text-slate-900 leading-tight group-hover:text-[#2563EB] transition-colors">{{ task.title }}</h3>
                        </div>
                        <img :src="task.thumbnail" class="w-14 h-14 rounded-lg object-cover border border-slate-200 shrink-0" />
                      </div>
                      
                      <div class="grid grid-cols-2 gap-y-2.5 text-xs text-slate-500 mb-4">
                        <span class="flex items-center gap-1.5"><ClipboardCheck class="w-3.5 h-3.5 text-slate-400"/> <span class="truncate">{{ task.category }}</span></span>
                        <span class="flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-slate-400"/> <span class="truncate">{{ task.area }}</span></span>
                        <span class="flex items-center gap-1.5"><Calendar class="w-3.5 h-3.5 text-slate-400"/> {{ task.completedOn }}</span>
                        <span class="flex items-center gap-1.5"><Clock class="w-3.5 h-3.5 text-slate-400"/> {{ task.timeTaken }}</span>
                      </div>

                      <div class="flex items-center justify-between pt-3 border-t border-slate-100 mt-auto">
                        <div class="flex items-center gap-1">
                          <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= task.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                        </div>
                        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Officer: {{ task.officer }}</span>
                      </div>
                    </div>

                    <div class="bg-slate-50 border-t border-slate-100 p-3 flex gap-2">
                      <button @click="openTaskDetails(task)" class="px-3 py-2 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors flex-1 flex justify-center items-center gap-1.5 shadow-sm">
                        <Eye class="w-3.5 h-3.5" /> View Details
                      </button>
                      <button class="px-3 py-2 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors flex-1 flex justify-center items-center gap-1.5 shadow-sm">
                        <Download class="w-3.5 h-3.5" /> Report
                      </button>
                    </div>
                  </div>
                </div>

                <!-- TABLE VIEW -->
                <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                  <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm whitespace-nowrap">
                      <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide border-b border-slate-100">
                        <tr>
                          <th class="px-5 py-4">Task Info</th>
                          <th class="px-5 py-4">Status & Time</th>
                          <th class="px-5 py-4">Verification</th>
                          <th class="px-5 py-4 text-center">Rating</th>
                          <th class="px-5 py-4 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-slate-100">
                        <tr v-for="task in filteredTasks" :key="task.id" class="hover:bg-slate-50 transition-colors group">
                          <td class="px-5 py-4">
                            <p class="font-bold text-slate-900 mb-0.5 font-mono">{{ task.id }}</p>
                            <p class="text-xs text-slate-500 flex items-center gap-1"><MapPin class="w-3 h-3"/> {{ task.area }}</p>
                          </td>
                          <td class="px-5 py-4">
                            <p class="text-xs text-slate-900 font-medium mb-1">{{ task.completedOn }}</p>
                            <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wide flex items-center gap-1"><Clock class="w-3 h-3" /> {{ task.timeTaken }}</p>
                          </td>
                          <td class="px-5 py-4">
                            <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${verifyBadge(task.verification)}`">{{ task.verification }}</span>
                          </td>
                          <td class="px-5 py-4">
                            <div class="flex items-center justify-center gap-0.5">
                              <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= task.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                            </div>
                          </td>
                          <td class="px-5 py-4 text-right">
                            <button @click="openTaskDetails(task)" class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded transition-colors" title="View Details"><Eye class="w-4 h-4" /></button>
                            <button class="p-1.5 text-slate-400 hover:text-[#2563EB] hover:bg-blue-50 rounded transition-colors" title="Download Report"><Download class="w-4 h-4" /></button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else class="bg-white p-12 rounded-2xl border border-slate-100 text-center shadow-sm">
                <CheckCircle class="w-12 h-12 text-slate-300 mx-auto mb-4" />
                <h3 class="text-lg font-bold text-slate-900 mb-1">No completed tasks found</h3>
                <p class="text-slate-500 text-sm">Try adjusting your filters or search query.</p>
              </div>
            </div>

            <!-- Right Column: Analytics & Achievements (4 cols) -->
            <div class="xl:col-span-4 space-y-6">
              
              <!-- Analytics Chart 1 -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Activity class="w-4 h-4 text-[#2563EB]" /> Monthly Completion Trend</h3>
                <div class="h-[200px] w-full relative">
                  <canvas ref="completionChartRef"></canvas>
                </div>
              </div>

              <!-- Analytics Chart 2 -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Star class="w-4 h-4 text-amber-500 fill-amber-500" /> Citizen Rating Trend</h3>
                <div class="h-[180px] w-full relative">
                  <canvas ref="ratingChartRef"></canvas>
                </div>
              </div>

              <!-- Achievements -->
              <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Award class="w-5 h-5 text-purple-500" /> My Achievements</h3>
                <div class="space-y-3">
                  <div class="flex items-center gap-4 p-3 bg-gradient-to-r from-amber-50 to-white border border-amber-100 rounded-xl">
                    <div class="w-10 h-10 rounded-full bg-amber-100 flex items-center justify-center text-xl">🏆</div>
                    <div>
                      <p class="font-bold text-slate-900 text-sm">100 Tasks Completed</p>
                      <p class="text-xs text-slate-500">Milestone reached on Jun 15, 2026</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-4 p-3 bg-gradient-to-r from-blue-50 to-white border border-blue-100 rounded-xl">
                    <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-xl">⚡</div>
                    <div>
                      <p class="font-bold text-slate-900 text-sm">Fast Responder</p>
                      <p class="text-xs text-slate-500">Top 10% fastest resolution time</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="grid grid-cols-2 gap-3">
                <router-link to="/worker/tasks" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <ClipboardCheck class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Active Tasks</span>
                </router-link>
                <router-link to="/worker/dashboard" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <Building class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Dashboard</span>
                </router-link>
              </div>

            </div>
          </div>
        </div>
      </main>
    <!-- Task Details Drawer -->
    <Teleport to="body">
      <div v-if="drawerOpen && activeTask" class="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex justify-end animate-fade-in" @click="closeDrawer">
        <div class="w-full max-w-2xl bg-white h-full shadow-2xl flex flex-col transform transition-transform animate-slide-in" @click.stop>
          
          <!-- Drawer Header -->
          <div class="p-5 md:p-6 border-b border-slate-100 bg-slate-50 flex justify-between items-start shrink-0">
            <div>
              <div class="flex items-center gap-2 mb-2">
                <span class="px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-white border border-slate-200 text-slate-600 font-mono">{{ activeTask.id }}</span>
                <span :class="`px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider ${verifyBadge(activeTask.verification)}`">{{ activeTask.verification }}</span>
              </div>
              <h2 class="text-xl font-bold text-slate-900 leading-tight">{{ activeTask.title }}</h2>
              <p class="text-xs text-slate-500 mt-1">Completed on {{ activeTask.completedOn }}</p>
            </div>
            <button @click="closeDrawer" class="p-2 bg-white rounded-lg border border-slate-200 text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"><X class="w-5 h-5"/></button>
          </div>
          
          <!-- Drawer Body -->
          <div class="flex-1 overflow-y-auto p-5 md:p-6 space-y-6">
            
            <!-- Metadata Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Time Taken</p>
                <p class="font-bold text-slate-900">{{ activeTask.timeTaken }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Area</p>
                <p class="font-bold text-slate-900 truncate">{{ activeTask.area }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Officer</p>
                <p class="font-bold text-slate-900 truncate">{{ activeTask.officer }}</p>
              </div>
              <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Citizen Rating</p>
                <div class="flex items-center gap-0.5 mt-0.5">
                  <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= activeTask.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                </div>
              </div>
            </div>

            <!-- Work Details -->
            <div>
              <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider mb-3">Work Performed</h3>
              <p class="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100">
                {{ activeTask.workNotes }}
              </p>
            </div>

            <!-- Material Used -->
            <div>
              <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider mb-3">Materials Used</h3>
              <div class="flex flex-wrap gap-2">
                <span v-for="mat in activeTask.materials" :key="mat" class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded-lg flex items-center gap-1.5">
                  <CheckCircle class="w-3.5 h-3.5 text-green-500" /> {{ mat }}
                </span>
              </div>
            </div>

            <div class="w-full h-px bg-slate-100"></div>

            <!-- Officer Verification Card -->
            <div>
              <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider mb-3">Officer Verification</h3>
              <div :class="`p-4 rounded-xl border ${activeTask.verification === 'Verified' ? 'bg-green-50 border-green-100' : (activeTask.verification === 'Rejected' ? 'bg-red-50 border-red-100' : 'bg-amber-50 border-amber-100')}`">
                <div class="flex items-start justify-between gap-4 mb-2">
                  <div class="flex items-center gap-2">
                    <ShieldCheck :class="`w-5 h-5 ${activeTask.verification === 'Verified' ? 'text-green-600' : (activeTask.verification === 'Rejected' ? 'text-red-600' : 'text-amber-600')}`" />
                    <span class="font-bold text-slate-900">{{ activeTask.verification }} by {{ activeTask.officer }}</span>
                  </div>
                  <span class="text-xs font-medium text-slate-500">{{ activeTask.verifyDate }}</span>
                </div>
                <p class="text-sm text-slate-700 italic">"{{ activeTask.officerComments }}"</p>
              </div>
            </div>

            <!-- Citizen Feedback Card -->
            <div v-if="activeTask.rating > 0">
              <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider mb-3">Citizen Feedback</h3>
              <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-start justify-between gap-4 mb-2">
                  <p class="font-bold text-slate-900">{{ activeTask.citizenName }}</p>
                  <div class="flex items-center gap-0.5">
                    <Star v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= activeTask.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                  </div>
                </div>
                <p class="text-sm text-slate-600 leading-relaxed mb-3">"{{ activeTask.citizenFeedback }}"</p>
                <div class="flex items-center gap-1.5 text-xs font-bold text-green-600">
                  <CheckCircle class="w-3.5 h-3.5" /> Highly Recommended
                </div>
              </div>
            </div>

            <div class="w-full h-px bg-slate-100"></div>

            <!-- Evidence Gallery -->
            <div>
              <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider mb-4">Completion Evidence</h3>
              <div class="grid grid-cols-3 gap-3">
                <div v-for="(img, idx) in activeTask.images" :key="idx" @click="openImagePreview(img)" class="aspect-square bg-slate-100 rounded-xl overflow-hidden cursor-pointer group relative border border-slate-200">
                  <img :src="img.url" class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110" />
                  <div class="absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/30 transition-colors flex items-center justify-center">
                    <Eye class="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <div class="absolute bottom-0 left-0 w-full bg-slate-900/60 text-white text-[9px] font-bold uppercase tracking-wider px-2 py-1 text-center backdrop-blur-sm">
                    {{ img.label }}
                  </div>
                </div>
              </div>
            </div>

          </div>
          
          <!-- Drawer Footer -->
          <div class="p-5 md:p-6 border-t border-slate-100 bg-slate-50 shrink-0">
            <button class="w-full py-3 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2">
              <Download class="w-4 h-4" /> Download Full Report
            </button>
          </div>

        </div>
      </div>
    </Teleport>

    <!-- Image Preview Modal -->
    <Teleport to="body">
      <div v-if="previewImage" class="fixed inset-0 z-[60] bg-slate-900/90 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in" @click="previewImage = null">
        <button class="absolute top-6 right-6 text-white hover:text-slate-300 p-2 transition-colors"><X class="w-8 h-8" /></button>
        <img :src="previewImage" class="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl" @click.stop />
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  CheckCircle, ClipboardCheck, Star, Clock, Calendar, Award, 
  Download, Eye, UserCheck, Building, Activity, FileText, 
  ShieldCheck, Search, LayoutGrid, List, MapPin, X
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const viewMode = ref('grid') // 'grid' | 'table'
const drawerOpen = ref(false)
const activeTask = ref(null)
const previewImage = ref(null)

const completionChartRef = ref(null)
const ratingChartRef = ref(null)
let completionChart, ratingChart

const filters = reactive({
  search: '',
  verification: 'All',
  category: 'All',
  sort: 'Newest'
})

// --- Mock Data ---
const summaryStats = [
  { title: 'Total Completed', value: '142', icon: CheckCircle, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'This Week', value: '14', trend: 12, icon: Calendar, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'This Month', value: '45', icon: Calendar, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { title: 'Avg Completion', value: '4.2h', trend: -5, icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Officer Verified', value: '138', icon: ShieldCheck, iconBg: 'bg-teal-50', iconColor: 'text-teal-500' },
  { title: 'Avg Rating', value: '4.8', trend: 2, icon: Star, iconBg: 'bg-yellow-50', iconColor: 'text-yellow-500' },
  { title: 'Perf. Score', value: '96', icon: Activity, iconBg: 'bg-indigo-50', iconColor: 'text-indigo-500' }
]

const tasks = [
  { 
    id: 'CMP-8875', title: 'Deep Pothole Repair', category: 'Road Damage', area: 'MG Road', ward: 'Ward 12',
    officer: 'Rahul Sharma', completedOn: 'Jul 08, 2026', timeTaken: '3h 45m', verification: 'Verified', rating: 5,
    verifyDate: 'Jul 08, 2026', officerComments: 'Excellent quality of work. Proper cold mix asphalt used and compacted well.',
    citizenName: 'Anil Kumar', citizenFeedback: 'The pothole was fixed surprisingly fast. Thank you for making the road safe again.',
    thumbnail: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=150&h=150&fit=crop',
    workNotes: 'Cleared debris from pothole, applied bonding layer, filled with cold mix asphalt, and compacted using heavy roller. Restored traffic flow safely.',
    materials: ['Cold Mix Asphalt (4 Bags)', 'Primer', 'Warning Cones'],
    images: [
      { label: 'Before', url: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=400&fit=crop' },
      { label: 'Progress', url: 'https://images.unsplash.com/photo-1584985614946-bdeeb2bc4db1?w=400&fit=crop' },
      { label: 'After', url: 'https://images.unsplash.com/photo-1544257121-654dbbc305e7?w=400&fit=crop' }
    ]
  },
  { 
    id: 'CMP-8850', title: 'Blocked Drainage Clearance', category: 'Drainage', area: 'North Zone', ward: 'Ward 8',
    officer: 'Priya Sharma', completedOn: 'Jul 07, 2026', timeTaken: '2h 15m', verification: 'Verified', rating: 4,
    verifyDate: 'Jul 07, 2026', officerComments: 'Drain cleared effectively. Ensure silt is disposed of properly next time.',
    citizenName: 'Sneha Patel', citizenFeedback: 'Water logging is gone. Good job by the team.',
    thumbnail: 'https://images.unsplash.com/photo-1584985614946-bdeeb2bc4db1?w=150&h=150&fit=crop',
    workNotes: 'Used jetting machine to remove plastic blockage. Cleared 10kg of silt from the main chamber. Applied sanitation powder.',
    materials: ['Jetting Machine Usage', 'Sanitation Powder'],
    images: [
      { label: 'Before', url: 'https://images.unsplash.com/photo-1584985614946-bdeeb2bc4db1?w=400&fit=crop' },
      { label: 'After', url: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=400&fit=crop' }
    ]
  },
  { 
    id: 'CMP-8812', title: 'Streetlight Replacement', category: 'Streetlight', area: 'South Suburbs', ward: 'Ward 2',
    officer: 'Rahul Sharma', completedOn: 'Jul 05, 2026', timeTaken: '1h 20m', verification: 'Pending', rating: 0,
    verifyDate: 'Pending Verification', officerComments: 'Awaiting field inspection.',
    citizenName: 'N/A', citizenFeedback: 'Awaiting feedback',
    thumbnail: 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=150&h=150&fit=crop',
    workNotes: 'Replaced faulty 40W LED bulb and checked electrical wiring connections. Tested successfully.',
    materials: ['40W LED Bulb (1)', 'Electrical Tape'],
    images: [
      { label: 'After', url: 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=400&fit=crop' }
    ]
  }
]

// --- Computed & Methods ---
const filteredTasks = computed(() => {
  let result = tasks

  if (filters.search) {
    const q = filters.search.toLowerCase()
    result = result.filter(t => t.id.toLowerCase().includes(q) || t.title.toLowerCase().includes(q) || t.area.toLowerCase().includes(q))
  }
  
  if (filters.verification !== 'All') result = result.filter(t => t.verification === filters.verification)
  if (filters.category !== 'All') result = result.filter(t => t.category === filters.category)

  if (filters.sort === 'Rating') {
    result.sort((a, b) => b.rating - a.rating)
  } else if (filters.sort === 'Fastest') {
    result.sort((a, b) => a.timeTaken.localeCompare(b.timeTaken)) // Naive sort for dummy data
  } else {
    result.sort((a, b) => a.id < b.id ? 1 : -1) // Newest by ID
  }

  return result
})

const verifyBadge = (status) => {
  const map = { 'Verified': 'bg-green-100 text-green-700 border border-green-200', 'Pending': 'bg-amber-100 text-amber-700 border border-amber-200', 'Rejected': 'bg-red-100 text-red-700 border border-red-200' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const openTaskDetails = (task) => {
  activeTask.value = task
  drawerOpen.value = true
}

const closeDrawer = () => {
  drawerOpen.value = false
  setTimeout(() => activeTask.value = null, 300)
}

const openImagePreview = (imgUrl) => previewImage.value = imgUrl

// --- Chart Setup ---
onMounted(() => {
  if (completionChartRef.value) {
    completionChart = new Chart(completionChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Completed Tasks',
          data: [18, 22, 25, 20, 32, 25],
          backgroundColor: '#2563EB',
          borderRadius: 4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }
    })
  }

  if (ratingChartRef.value) {
    ratingChart = new Chart(ratingChartRef.value, {
      type: 'line',
      data: {
        labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Avg Rating',
          data: [4.2, 4.4, 4.3, 4.6, 4.7, 4.8],
          borderColor: '#F59E0B',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          fill: true,
          tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { min: 3, max: 5, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }
    })
  }
})

onUnmounted(() => {
  if (completionChart) completionChart.destroy()
  if (ratingChart) ratingChart.destroy()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
.animate-slide-in { animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>