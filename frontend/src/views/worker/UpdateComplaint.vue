<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1400px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Breadcrumb & Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <router-link to="/worker/tasks" class="hover:text-[#2563EB] transition-colors">Assigned Tasks</router-link>
                <span class="mx-2">›</span>
                <router-link :to="`/worker/task/${complaint.id}`" class="hover:text-[#2563EB] transition-colors">Task Details</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Update Progress</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Update Complaint</h1>
              <p class="text-slate-500 mt-1">Update work progress, record materials, and submit task completion.</p>
            </div>
            <div class="flex gap-2">
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
                <Phone class="w-4 h-4 text-slate-400" /> Contact Officer
              </button>
            </div>
          </div>

          <!-- Summary Card -->
          <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 md:p-6">
            <div class="flex flex-col md:flex-row md:items-start justify-between gap-4">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2 flex-wrap">
                  <span class="px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-slate-100 text-slate-600 font-mono">{{ complaint.id }}</span>
                  <span :class="`px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider ${priorityBadge(complaint.priority)}`">{{ complaint.priority }} Priority</span>
                  <span :class="`px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider ${statusBadge(complaint.status)}`">{{ complaint.status }}</span>
                </div>
                <h2 class="text-xl md:text-2xl font-bold text-slate-900 mb-1">{{ complaint.title }}</h2>
                <div class="flex items-center gap-4 text-sm text-slate-500 font-medium flex-wrap">
                  <span class="flex items-center gap-1"><ClipboardList class="w-4 h-4 text-slate-400" /> {{ complaint.category }}</span>
                  <span class="flex items-center gap-1"><MapPin class="w-4 h-4 text-slate-400" /> {{ complaint.area }}, {{ complaint.ward }}</span>
                  <span class="flex items-center gap-1"><User class="w-4 h-4 text-slate-400" /> Officer: {{ complaint.officer }}</span>
                </div>
              </div>
              <div class="w-full md:w-64 shrink-0 text-right">
                <div class="mb-1 flex justify-between text-sm font-bold text-slate-700">
                  <span>Overall Progress</span>
                  <span>{{ form.progress }}%</span>
                </div>
                <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-500 bg-[#2563EB]" :style="`width: ${form.progress}%`"></div>
                </div>
                <p class="text-xs text-slate-500 font-medium mt-2 flex items-center justify-end gap-1"><Clock class="w-3.5 h-3.5" /> Deadline: {{ complaint.deadline }}</p>
              </div>
            </div>
          </div>

          <!-- Main Layout Grid -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <!-- Left Column: Work Execution Form (8 cols) -->
            <div class="xl:col-span-8 flex flex-col gap-6">
              
              <!-- Status & Progress Controls -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 bg-slate-50/50">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><Activity class="w-5 h-5 text-[#2563EB]" /> Current Status & Progress</h3>
                </div>
                <div class="p-5 space-y-6">
                  
                  <!-- Stage Tracker -->
                  <div class="w-full relative py-2 overflow-x-auto no-scrollbar">
                    <div class="flex items-center min-w-[700px] justify-between relative px-2">
                      <div class="absolute left-4 right-4 top-1/2 -translate-y-1/2 h-1 bg-slate-100 rounded-full z-0"></div>
                      <div class="absolute left-4 top-1/2 -translate-y-1/2 h-1 bg-[#2563EB] rounded-full z-0 transition-all duration-500" :style="`width: ${stagePercentage}%`"></div>
                      
                      <div v-for="(stage, idx) in stages" :key="stage" class="relative z-10 flex flex-col items-center gap-1.5 w-20">
                        <div :class="`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs border-2 transition-colors duration-300 bg-white ${currentStageIndex >= idx ? 'border-[#2563EB] text-[#2563EB]' : 'border-slate-200 text-slate-300'}`">
                          <CheckCircle v-if="currentStageIndex > idx" class="w-3.5 h-3.5" />
                          <div v-else class="w-2 h-2 rounded-full" :class="currentStageIndex === idx ? 'bg-[#2563EB]' : 'bg-transparent'"></div>
                        </div>
                        <span :class="`text-[9px] font-bold uppercase tracking-wider text-center leading-tight ${currentStageIndex >= idx ? 'text-slate-800' : 'text-slate-400'}`">{{ stage }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Update Status</label>
                      <select v-model="form.status" @change="handleStatusChange" class="w-full bg-white border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] p-2.5 outline-none font-medium shadow-sm transition-all">
                        <option v-for="opt in statusOptions" :key="opt" :value="opt">{{ opt }}</option>
                      </select>
                    </div>
                    <div>
                      <div class="flex justify-between items-center mb-1.5">
                        <label class="text-xs font-bold text-slate-500 uppercase tracking-wide">Work Completion</label>
                        <span class="text-sm font-extrabold text-[#2563EB]">{{ form.progress }}%</span>
                      </div>
                      <input type="range" min="0" max="100" step="5" v-model="form.progress" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#2563EB]" />
                      <p class="text-[10px] text-slate-400 font-medium text-right mt-1">Est. Remaining: 45 mins</p>
                    </div>
                  </div>

                </div>
              </div>

              <!-- Checklists (Site & Completion) -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><CheckSquare class="w-4 h-4 text-slate-400" /> Site Checklist</h3>
                  <div class="space-y-3">
                    <label v-for="(val, key) in siteChecklist" :key="key" class="flex items-center gap-3 cursor-pointer group">
                      <input type="checkbox" v-model="siteChecklist[key]" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <span class="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{{ key }}</span>
                    </label>
                  </div>
                </div>

                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><CheckSquare class="w-4 h-4 text-green-500" /> Completion Checklist</h3>
                  <div class="space-y-3">
                    <label v-for="(val, key) in completionChecklist" :key="key" class="flex items-center gap-3 cursor-pointer group">
                      <input type="checkbox" v-model="completionChecklist[key]" class="w-4 h-4 rounded border-slate-300 text-green-600 focus:ring-green-500" />
                      <span class="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{{ key }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Materials Usage -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Tool class="w-5 h-5 text-slate-400" /> Record Materials Used</h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div v-for="(mat, idx) in materials" :key="idx" class="flex items-center justify-between p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
                    <label class="flex items-center gap-3 cursor-pointer flex-1">
                      <input type="checkbox" v-model="mat.used" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <span class="text-sm font-medium text-slate-700">{{ mat.name }}</span>
                    </label>
                    <div v-if="mat.used" class="flex items-center gap-2 w-24">
                      <input type="number" v-model="mat.qty" min="1" class="w-12 p-1 text-xs text-center border border-slate-300 rounded focus:ring-[#2563EB] outline-none" />
                      <span class="text-xs text-slate-500">{{ mat.unit }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Evidence Uploads -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 bg-slate-50/50">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><Camera class="w-5 h-5 text-slate-400" /> Work Evidence Photos</h3>
                </div>
                <div class="p-5 space-y-6">
                  
                  <!-- Upload Section Reusable Structure -->
                  <div v-for="(section, sIdx) in uploadSections" :key="sIdx" class="space-y-2">
                    <div class="flex justify-between items-end mb-2">
                      <div>
                        <p class="text-sm font-bold text-slate-900">{{ section.title }}</p>
                        <p class="text-xs text-slate-500">{{ section.desc }} (Max 5)</p>
                      </div>
                      <span class="text-xs font-bold text-slate-400">{{ section.images.length }}/5 Uploaded</span>
                    </div>
                    
                    <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
                      <div v-for="(img, iIdx) in section.images" :key="iIdx" class="aspect-square rounded-xl bg-slate-100 relative overflow-hidden group border border-slate-200">
                        <img :src="img" class="w-full h-full object-cover" />
                        <button @click="removeImage(section, iIdx)" class="absolute top-1 right-1 bg-red-500/90 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"><X class="w-3 h-3"/></button>
                      </div>
                      <label v-if="section.images.length < 5" class="aspect-square rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 hover:bg-slate-100 transition-colors flex flex-col items-center justify-center cursor-pointer group">
                        <Upload class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB] mb-1 transition-colors" />
                        <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wide">Upload</span>
                        <input type="file" accept="image/jpeg, image/png, image/jpg" class="hidden" @change="(e) => handleImageUpload(e, section)" />
                      </label>
                    </div>
                  </div>

                </div>
              </div>

              <!-- Work Notes -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <div class="flex justify-between items-end mb-3">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><FileText class="w-5 h-5 text-slate-400" /> Work Notes</h3>
                  <span class="text-xs font-medium text-slate-400">{{ form.notes.length }}/500</span>
                </div>
                <textarea 
                  v-model="form.notes" 
                  maxlength="500" 
                  rows="4" 
                  placeholder="Describe the work completed today, challenges faced, or any remaining activities..." 
                  class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none resize-none transition-all"
                ></textarea>
              </div>

              <!-- Issue Reporting Toggle -->
              <div class="bg-white rounded-[14px] shadow-sm border border-red-100 overflow-hidden">
                <button @click="showIssueReporting = !showIssueReporting" class="w-full p-5 flex justify-between items-center bg-red-50/50 hover:bg-red-50 transition-colors">
                  <h3 class="font-bold text-red-700 flex items-center gap-2"><AlertTriangle class="w-5 h-5" /> Report Issue / Blocked Work</h3>
                  <ChevronDown class="w-5 h-5 text-red-700 transition-transform duration-300" :class="showIssueReporting ? 'rotate-180' : ''" />
                </button>
                <div v-if="showIssueReporting" class="p-5 border-t border-red-100 animate-fade-in space-y-4">
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Reason for Blockage</label>
                    <select v-model="issue.reason" class="w-full bg-white border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-2 focus:ring-red-500/20 focus:border-red-500 p-2.5 outline-none">
                      <option disabled value="">Select reason...</option>
                      <option>Material Not Available</option>
                      <option>Weather Conditions</option>
                      <option>Access Restricted</option>
                      <option>Additional Damage Found</option>
                      <option>Other</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Issue Description</label>
                    <textarea v-model="issue.description" rows="3" placeholder="Provide details to the officer..." class="w-full p-3 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-red-500/20 focus:border-red-500 outline-none resize-none"></textarea>
                  </div>
                  <div class="text-right">
                    <button class="px-4 py-2 bg-red-600 text-white text-sm font-bold rounded-lg hover:bg-red-700 transition-colors shadow-sm">Report to Officer</button>
                  </div>
                </div>
              </div>

              <!-- Main Action Buttons -->
              <div class="flex flex-col sm:flex-row items-center justify-end gap-3 pt-2">
                <button class="w-full sm:w-auto px-6 py-3 bg-white border border-slate-300 text-slate-700 text-sm font-bold rounded-xl hover:bg-slate-50 transition-colors">Cancel</button>
                <button class="w-full sm:w-auto px-6 py-3 bg-slate-100 text-slate-700 text-sm font-bold rounded-xl hover:bg-slate-200 transition-colors">Save Draft</button>
                <button @click="openConfirmModal" class="w-full sm:w-auto px-6 py-3 bg-[#2563EB] text-white text-sm font-bold rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2">
                  <CheckCircle class="w-4 h-4" /> Submit Update
                </button>
              </div>

            </div>

            <!-- Right Column: Context & History (4 cols) -->
            <div class="xl:col-span-4 space-y-6">
              
              <!-- Officer Instructions -->
              <div class="bg-blue-50 border border-blue-100 rounded-[14px] p-5 shadow-sm">
                <h3 class="font-bold text-[#1E40AF] flex items-center gap-2 mb-3"><Shield class="w-5 h-5" /> Officer Instructions</h3>
                <p class="text-sm text-[#1E40AF] leading-relaxed italic bg-white/50 p-3 rounded-lg border border-blue-100/50">
                  "{{ complaint.instructions }}"
                </p>
              </div>

              <!-- Today's Summary & Time Tracking -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Clock class="w-5 h-5 text-slate-400" /> Time Tracking</h3>
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Started</p>
                    <p class="text-sm font-bold text-slate-900">09:15 AM</p>
                  </div>
                  <div class="p-3 bg-slate-50 rounded-xl border border-slate-100">
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wide mb-1">Break Time</p>
                    <p class="text-sm font-bold text-slate-900">45 Mins</p>
                  </div>
                </div>
                <div class="flex items-center justify-between p-3 bg-blue-50 border border-blue-100 rounded-xl mb-4">
                  <span class="text-sm font-bold text-blue-800">Total Time Worked</span>
                  <span class="text-xl font-extrabold text-blue-700">3h 20m</span>
                </div>
                <div class="flex items-center justify-between text-xs font-medium text-slate-500 px-1">
                  <span>Est. Completion</span>
                  <span>14:00 PM</span>
                </div>
              </div>

              <!-- Progress Timeline -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><List class="w-5 h-5 text-slate-400" /> Progress Timeline</h3>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="(event, idx) in timeline" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 rounded-full ring-4 ring-white border-2" :class="idx === 0 ? 'bg-[#2563EB] border-[#2563EB]' : 'bg-slate-300 border-slate-300'"></div>
                    <p class="text-sm font-bold text-slate-900">{{ event.action }}</p>
                    <p class="text-[10px] font-medium text-slate-500 mt-0.5">{{ event.date }} • {{ event.time }}</p>
                  </div>
                </div>
              </div>

              <!-- Recent Updates -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><History class="w-5 h-5 text-slate-400" /> Recent Log</h3>
                <div class="space-y-3">
                  <div class="flex gap-3 items-start">
                    <Camera class="w-4 h-4 text-slate-400 mt-0.5" />
                    <div>
                      <p class="text-sm text-slate-700">Uploaded 2 Before Photos</p>
                      <p class="text-[10px] text-slate-400">10 mins ago</p>
                    </div>
                  </div>
                  <div class="flex gap-3 items-start">
                    <Tool class="w-4 h-4 text-slate-400 mt-0.5" />
                    <div>
                      <p class="text-sm text-slate-700">Recorded 1x Replacement Bulb</p>
                      <p class="text-[10px] text-slate-400">15 mins ago</p>
                    </div>
                  </div>
                  <div class="flex gap-3 items-start">
                    <PlayCircle class="w-4 h-4 text-slate-400 mt-0.5" />
                    <div>
                      <p class="text-sm text-slate-700">Status changed to In Progress</p>
                      <p class="text-[10px] text-slate-400">2 hours ago</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="grid grid-cols-2 gap-3">
                <router-link :to="`/worker/task/${complaint.id}`" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <FileText class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Task Details</span>
                </router-link>
                <router-link to="/worker/tasks" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <ClipboardList class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">All Tasks</span>
                </router-link>
              </div>

            </div>
          </div>
        </div>
      </main>
    <!-- Confirmation Modal -->
    <Teleport to="body">
      <div v-if="showConfirmModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white p-6 rounded-2xl max-w-sm w-full shadow-2xl">
          <h3 class="text-lg font-bold text-slate-900 mb-2">Confirm Update</h3>
          <p class="text-sm text-slate-600 mb-4">You are about to update the status to <strong class="text-slate-900">{{ form.status }}</strong> with <strong class="text-slate-900">{{ form.progress }}%</strong> completion.</p>
          <div class="flex gap-3">
            <button @click="showConfirmModal = false" class="flex-1 py-2.5 bg-slate-100 text-slate-700 font-bold rounded-lg hover:bg-slate-200 transition-colors">Cancel</button>
            <button @click="processUpdate" class="flex-1 py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex justify-center items-center gap-2">
              <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              Confirm
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Success Modal -->
    <Teleport to="body">
      <div v-if="showSuccessModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white p-8 rounded-2xl max-w-sm w-full text-center shadow-2xl">
          <div class="w-16 h-16 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle class="w-8 h-8" />
          </div>
          <h3 class="text-xl font-bold text-slate-900 mb-2">Update Successful</h3>
          <p class="text-sm text-slate-600 mb-6">The complaint progress has been updated and recorded in the system.</p>
          <div class="space-y-3">
            <button @click="showSuccessModal = false" class="w-full py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors">Continue Working</button>
            <router-link to="/worker/tasks" class="block w-full py-2.5 bg-slate-100 text-slate-700 font-bold rounded-lg hover:bg-slate-200 transition-colors">View Assigned Tasks</router-link>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  ClipboardList, CheckCircle, Clock, MapPin, AlertTriangle, 
  User, Activity, FileText, Phone, Camera, Upload, X, CheckSquare,
  Wrench, Shield, List, History, ChevronDown, PlayCircle
} from 'lucide-vue-next'

// --- State ---
const isSidebarOpen = ref(false)
const showIssueReporting = ref(false)
const showConfirmModal = ref(false)
const showSuccessModal = ref(false)
const isSubmitting = ref(false)

const form = reactive({
  status: 'In Progress',
  progress: 65,
  notes: ''
})

const issue = reactive({
  reason: '',
  description: ''
})

// --- Mock Data ---
const complaint = reactive({
  id: 'CMP-8902',
  title: 'Fallen Live Wire near Pedestrian Walkway',
  category: 'Electrical',
  priority: 'Emergency',
  status: 'In Progress',
  area: 'Downtown Sector 4',
  ward: 'Ward 14',
  deadline: 'Today, 02:00 PM',
  officer: 'Officer S. Patel',
  instructions: 'Inspect the fallen wire. Ensure grid power is disconnected before repair. Splice connection, reattach to pole securely. Upload testing evidence before leaving site.'
})

const stages = ['Assigned', 'Accepted', 'Travelling', 'Reached Site', 'Work Started', 'In Progress', 'Quality Check', 'Completed']
const statusOptions = ['Accepted', 'Travelling', 'Reached Site', 'Work Started', 'In Progress', 'Waiting for Materials', 'Temporarily Paused', 'Completed']

const siteChecklist = reactive({
  'Reached Location': true,
  'Area Inspected': true,
  'Required Materials Available': true,
  'Repair Started': true,
  'Safety Protocol Followed': true
})

const completionChecklist = reactive({
  'Work Completed': false,
  'Photos Uploaded': false,
  'Notes Added': false,
  'Materials Recorded': true,
  'Final Inspection Done': false
})

const materials = reactive([
  { name: 'Insulation Tape (HV)', qty: 2, unit: 'Rolls', used: true },
  { name: 'Wire Splice Kit', qty: 1, unit: 'Kit', used: false },
  { name: 'Warning Cones', qty: 4, unit: 'Units', used: true },
  { name: 'Replacement Bracket', qty: 1, unit: 'Unit', used: false }
])

const uploadSections = reactive([
  { id: 'before', title: 'Before Work', desc: 'Initial state of the issue', images: ['https://images.unsplash.com/photo-1544257121-654dbbc305e7?w=400&fit=crop'] },
  { id: 'progress', title: 'Work In Progress', desc: 'Repair activities taking place', images: [] },
  { id: 'after', title: 'After Completion', desc: 'Final resolved state', images: [] }
])

const timeline = [
  { action: 'Updated status to In Progress', date: 'Jul 09, 2026', time: '10:30 AM' },
  { action: 'Reached Site & Inspected', date: 'Jul 09, 2026', time: '09:45 AM' },
  { action: 'Travelling to Site', date: 'Jul 09, 2026', time: '09:15 AM' },
  { action: 'Task Accepted', date: 'Jul 09, 2026', time: '08:45 AM' }
]

// --- Computed & Methods ---
const currentStageIndex = computed(() => {
  // Map form status to stages array index
  const index = stages.indexOf(form.status)
  // If status is not exactly in stages (like "Temporarily Paused"), return current approximate stage based on progress
  if (index === -1) {
    if (form.progress === 100) return stages.indexOf('Completed')
    if (form.progress > 0) return stages.indexOf('In Progress')
    return 0
  }
  return index
})

const stagePercentage = computed(() => (currentStageIndex.value / (stages.length - 1)) * 100)

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700 border border-red-200', 'High': 'bg-orange-100 text-orange-700 border border-orange-200', 'Medium': 'bg-blue-100 text-blue-700 border border-blue-200', 'Low': 'bg-slate-100 text-slate-600 border border-slate-200' }
  return map[priority]
}

const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Completed': 'bg-green-100 text-green-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const handleStatusChange = () => {
  if (form.status === 'Completed') form.progress = 100
  if (form.status === 'Work Started' && form.progress === 0) form.progress = 10
}

const handleImageUpload = (e, section) => {
  if (section.images.length >= 5) return
  const file = e.target.files[0]
  if (file) {
    const url = URL.createObjectURL(file)
    section.images.push(url)
  }
}

const removeImage = (section, index) => {
  section.images.splice(index, 1)
}

const openConfirmModal = () => showConfirmModal.value = true

const processUpdate = async () => {
  isSubmitting.value = true
  await new Promise(resolve => setTimeout(resolve, 1500)) // Simulate network request
  isSubmitting.value = false
  showConfirmModal.value = false
  showSuccessModal.value = true
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>