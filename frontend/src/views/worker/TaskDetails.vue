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
                <span class="text-slate-900 font-semibold">{{ task.id }}</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Task Details</h1>
              <p class="text-slate-500 mt-1">Review task information and complete assigned work.</p>
            </div>
            <div class="flex gap-2">
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
                <Phone class="w-4 h-4 text-slate-400" /> Call Officer
              </button>
            </div>
          </div>

          <!-- Main Layout Grid -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <!-- Left Column: Task Workspace (8 cols) -->
            <div class="xl:col-span-8 flex flex-col gap-6">
              
              <!-- Task Overview Card -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 md:p-6">
                  <div class="flex flex-wrap items-start justify-between gap-4 mb-6">
                    <div>
                      <div class="flex items-center gap-2 mb-2">
                        <span class="px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider bg-slate-100 text-slate-600 font-mono">{{ task.id }}</span>
                        <span :class="`px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider ${priorityBadge(task.priority)}`">{{ task.priority }} Priority</span>
                        <span :class="`px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider ${statusBadge(task.status)}`">{{ task.status }}</span>
                      </div>
                      <h2 class="text-xl md:text-2xl font-bold text-slate-900">{{ task.title }}</h2>
                    </div>
                    <div class="flex gap-2">
                      <button class="px-4 py-2 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center gap-2">
                        <PlayCircle class="w-4 h-4" /> Start Work
                      </button>
                    </div>
                  </div>

                  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 py-4 border-y border-slate-100 mb-6">
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Category</p>
                      <p class="font-medium text-slate-900 mt-1 flex items-center gap-1.5"><ClipboardList class="w-3.5 h-3.5 text-slate-400"/> {{ task.category }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Location</p>
                      <p class="font-medium text-slate-900 mt-1 flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-slate-400"/> {{ task.ward }}, {{ task.area }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Deadline</p>
                      <p class="font-medium text-slate-900 mt-1 flex items-center gap-1.5"><Clock class="w-3.5 h-3.5 text-slate-400"/> {{ task.deadline }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Officer</p>
                      <p class="font-medium text-slate-900 mt-1 flex items-center gap-1.5"><User class="w-3.5 h-3.5 text-slate-400"/> {{ task.officer }}</p>
                    </div>
                  </div>

                  <!-- Visual Progress Tracker -->
                  <div class="w-full relative">
                    <div class="overflow-x-auto pb-4 no-scrollbar">
                      <div class="flex items-center min-w-[600px] justify-between relative">
                        <div class="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-slate-100 rounded-full z-0"></div>
                        <div class="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-[#2563EB] rounded-full z-0 transition-all duration-500" :style="`width: ${progressPercentage}%`"></div>
                        
                        <div v-for="(stage, idx) in progressStages" :key="stage" class="relative z-10 flex flex-col items-center gap-2">
                          <div :class="`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm border-2 transition-colors duration-300 ${currentStageIndex >= idx ? 'bg-[#2563EB] border-[#2563EB] text-white' : 'bg-white border-slate-200 text-slate-400'}`">
                            <CheckCircle v-if="currentStageIndex > idx" class="w-4 h-4" />
                            <span v-else>{{ idx + 1 }}</span>
                          </div>
                          <span :class="`text-[10px] font-bold uppercase tracking-wide ${currentStageIndex >= idx ? 'text-slate-900' : 'text-slate-400'}`">{{ stage }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Officer Instructions & Safety -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-blue-50 border border-blue-100 rounded-[14px] p-5 shadow-sm">
                  <h3 class="font-bold text-[#1E40AF] flex items-center gap-2 mb-3"><FileText class="w-5 h-5" /> Officer Instructions</h3>
                  <div class="space-y-2 text-sm text-[#1E40AF]">
                    <p v-for="(inst, idx) in task.instructions" :key="idx" class="flex items-start gap-2">
                      <span class="font-bold mt-0.5">•</span> {{ inst }}
                    </p>
                  </div>
                </div>

                <div class="bg-amber-50 border border-amber-100 rounded-[14px] p-5 shadow-sm">
                  <h3 class="font-bold text-amber-700 flex items-center gap-2 mb-3"><AlertTriangle class="w-5 h-5" /> Safety Guidelines</h3>
                  <div class="space-y-2">
                    <label v-for="(safety, idx) in task.safetyChecklist" :key="idx" class="flex items-start gap-3 cursor-pointer group">
                      <input type="checkbox" v-model="safety.checked" class="mt-0.5 w-4 h-4 rounded border-amber-300 text-amber-600 focus:ring-amber-500 bg-white" />
                      <span class="text-sm font-medium text-amber-800 group-hover:text-amber-900 transition-colors">{{ safety.text }}</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Complaint Description & Images -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 md:p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><FileText class="w-5 h-5 text-slate-400" /> Complaint Details</h3>
                <p class="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100 mb-4">
                  {{ task.description }}
                </p>
                
                <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-3 mt-6">Complaint Photos</h4>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <div v-for="(img, idx) in task.images" :key="idx" @click="openImagePreview(img)" class="aspect-square rounded-xl overflow-hidden cursor-pointer group relative border border-slate-200">
                    <img :src="img" class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110" />
                    <div class="absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/30 transition-colors flex items-center justify-center">
                      <ImageIcon class="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </div>
                </div>
              </div>

              <!-- Location Details -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-0 overflow-hidden flex flex-col sm:flex-row">
                <div class="w-full sm:w-1/3 bg-slate-100 min-h-[200px] relative border-b sm:border-b-0 sm:border-r border-slate-200 flex items-center justify-center">
                  <span class="text-slate-400 font-bold flex flex-col items-center gap-2"><MapPin class="w-8 h-8"/> Map View Placeholder</span>
                </div>
                <div class="w-full sm:w-2/3 p-5 md:p-6 flex flex-col justify-center">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><MapPin class="w-5 h-5 text-slate-400" /> Location Information</h3>
                  <div class="grid grid-cols-2 gap-y-4 gap-x-2 text-sm">
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Address</p>
                      <p class="font-medium text-slate-900 mt-0.5">{{ task.location.address }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Landmark</p>
                      <p class="font-medium text-slate-900 mt-0.5">{{ task.location.landmark }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Coordinates</p>
                      <p class="font-mono text-slate-700 mt-0.5 text-xs">{{ task.location.lat }}, {{ task.location.lng }}</p>
                    </div>
                  </div>
                  <div class="mt-5">
                    <button class="px-4 py-2 w-full sm:w-auto bg-slate-100 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-200 transition-colors flex items-center justify-center gap-2">
                      <MapPin class="w-4 h-4" /> Get Directions
                    </button>
                  </div>
                </div>
              </div>

              <!-- Work Execution Workspace -->
              <div class="bg-white rounded-[14px] shadow-sm border border-[#2563EB]/20 overflow-hidden">
                <div class="bg-[#2563EB]/5 p-5 border-b border-[#2563EB]/10">
                  <h3 class="font-bold text-[#1E40AF] flex items-center gap-2"><Hammer class="w-5 h-5" /> Work Execution & Evidence</h3>
                </div>
                <div class="p-5 md:p-6 space-y-8">
                  
                  <!-- Progress Slider -->
                  <div>
                    <div class="flex justify-between items-center mb-2">
                      <label class="text-sm font-bold text-slate-900">Current Work Progress</label>
                      <span class="text-xl font-extrabold text-[#2563EB]">{{ workProgress }}%</span>
                    </div>
                    <input type="range" min="0" max="100" step="5" v-model="workProgress" class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#2563EB]" />
                  </div>

                  <div class="h-px bg-slate-100 w-full"></div>

                  <!-- Image Uploads -->
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <p class="text-sm font-bold text-slate-900 mb-3">Before Work Evidence</p>
                      <div class="grid grid-cols-3 gap-2 mb-3">
                        <div v-for="(img, index) in beforeImages" :key="index" class="aspect-square bg-slate-100 rounded-lg relative overflow-hidden group border border-slate-200">
                          <img :src="img" class="w-full h-full object-cover" />
                          <button @click="removeImage('before', index)" class="absolute top-1 right-1 bg-red-500 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"><X class="w-3 h-3"/></button>
                        </div>
                        <label v-if="beforeImages.length < 5" class="aspect-square bg-slate-50 border-2 border-dashed border-slate-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:bg-slate-100 transition-colors group">
                          <Upload class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB] mb-1 transition-colors" />
                          <span class="text-[10px] font-bold text-slate-500">Upload</span>
                          <input type="file" accept="image/*" class="hidden" @change="(e) => handleUpload(e, 'before')" />
                        </label>
                      </div>
                    </div>
                    <div>
                      <p class="text-sm font-bold text-slate-900 mb-3">After Work Evidence</p>
                      <div class="grid grid-cols-3 gap-2 mb-3">
                        <div v-for="(img, index) in afterImages" :key="index" class="aspect-square bg-slate-100 rounded-lg relative overflow-hidden group border border-slate-200">
                          <img :src="img" class="w-full h-full object-cover" />
                          <button @click="removeImage('after', index)" class="absolute top-1 right-1 bg-red-500 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"><X class="w-3 h-3"/></button>
                        </div>
                        <label v-if="afterImages.length < 5" class="aspect-square bg-slate-50 border-2 border-dashed border-slate-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:bg-slate-100 transition-colors group">
                          <Camera class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB] mb-1 transition-colors" />
                          <span class="text-[10px] font-bold text-slate-500">Upload</span>
                          <input type="file" accept="image/*" class="hidden" @change="(e) => handleUpload(e, 'after')" />
                        </label>
                      </div>
                    </div>
                  </div>

                  <div class="h-px bg-slate-100 w-full"></div>

                  <!-- Work Notes & Materials -->
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label class="block text-sm font-bold text-slate-900 mb-3">Materials Used</label>
                      <div class="space-y-2">
                        <label v-for="mat in task.materials" :key="mat.name" class="flex items-center gap-3 p-2.5 bg-slate-50 border border-slate-200 rounded-lg cursor-pointer">
                          <input type="checkbox" v-model="mat.used" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                          <span class="text-sm font-medium text-slate-700 flex-1">{{ mat.name }}</span>
                          <span class="text-xs font-bold bg-white px-2 py-0.5 rounded border border-slate-200">{{ mat.qty }}</span>
                        </label>
                      </div>
                    </div>
                    <div>
                      <div class="flex justify-between items-center mb-3">
                        <label class="text-sm font-bold text-slate-900">Work Notes</label>
                        <span class="text-xs font-medium text-slate-400">{{ workNotes.length }}/500</span>
                      </div>
                      <textarea v-model="workNotes" rows="5" maxlength="500" placeholder="Describe the work completed, challenges faced, or additional context..." class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none resize-none transition-all"></textarea>
                    </div>
                  </div>

                  <!-- Completion Checklist -->
                  <div class="bg-slate-50 rounded-xl p-4 border border-slate-200">
                    <p class="text-sm font-bold text-slate-900 mb-3">Completion Checklist</p>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <label v-for="(checked, label) in completionChecklist" :key="label" class="flex items-center gap-3 cursor-pointer">
                        <input type="checkbox" v-model="completionChecklist[label]" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                        <span class="text-sm font-medium text-slate-700">{{ label }}</span>
                      </label>
                    </div>
                  </div>

                  <!-- Actions -->
                  <div class="flex flex-col sm:flex-row items-center justify-end gap-3 pt-4">
                    <button class="w-full sm:w-auto px-6 py-2.5 bg-white border border-slate-300 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-50 transition-colors">Save Progress</button>
                    <button class="w-full sm:w-auto px-6 py-2.5 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2">
                      <CheckCircle class="w-4 h-4" /> Submit for Verification
                    </button>
                  </div>

                </div>
              </div>

            </div>

            <!-- Right Column: Context & Metadata (4 cols) -->
            <div class="xl:col-span-4 space-y-6">
              
              <!-- Time Tracking -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Clock class="w-5 h-5 text-slate-400" /> Time Tracking</h3>
                <div class="space-y-3">
                  <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                    <span class="text-sm font-medium text-slate-600">Task Started</span>
                    <span class="text-sm font-bold text-slate-900">09:15 AM</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-blue-50 border border-blue-100">
                    <span class="text-sm font-medium text-blue-700">Time Elapsed</span>
                    <span class="text-lg font-bold text-blue-700">2h 45m</span>
                  </div>
                  <div class="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                    <span class="text-sm font-medium text-slate-600">Est. Time Remaining</span>
                    <span class="text-sm font-bold text-slate-900">1h 15m</span>
                  </div>
                </div>
              </div>

              <!-- Citizen Details -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><Users class="w-5 h-5 text-slate-400" /> Citizen Details</h3>
                <div class="space-y-3 text-sm">
                  <div>
                    <p class="text-xs text-slate-500 font-medium">Name</p>
                    <p class="font-bold text-slate-900">{{ task.citizen.name }}</p>
                  </div>
                  <div class="pt-3 border-t border-slate-100">
                    <p class="text-xs text-slate-500 font-medium mb-1">Citizen Notes</p>
                    <p class="text-slate-700 italic bg-slate-50 p-2 rounded border border-slate-100">"{{ task.citizen.notes }}"</p>
                  </div>
                </div>
              </div>

              <!-- Recent Activity Timeline -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Activity class="w-5 h-5 text-slate-400" /> Task Timeline</h3>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="(event, idx) in task.timeline" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 rounded-full ring-4 ring-white border-2" :class="idx === 0 ? 'bg-[#2563EB] border-[#2563EB]' : 'bg-slate-300 border-slate-300'"></div>
                    <p class="text-sm font-bold text-slate-900">{{ event.action }}</p>
                    <p class="text-[10px] font-medium text-slate-500 mt-0.5">{{ event.date }} • {{ event.time }}</p>
                    <p v-if="event.user" class="text-xs text-slate-600 mt-1">By: {{ event.user }}</p>
                  </div>
                  <!-- Future Steps -->
                  <div class="relative opacity-40">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-slate-200 rounded-full ring-4 ring-white border-2 border-slate-300"></div>
                    <p class="text-sm font-bold text-slate-900">Task Completed</p>
                  </div>
                </div>
              </div>

              <!-- Quick Navigation -->
              <div class="grid grid-cols-2 gap-3">
                <router-link to="/worker/dashboard" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <LayoutDashboard class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Dashboard</span>
                </router-link>
                <button class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <Building class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">My Tasks</span>
                </button>
              </div>

            </div>
          </div>
        </div>
      </main>

    <!-- Image Preview Modal -->
    <Teleport to="body">
      <div v-if="previewImage" class="fixed inset-0 z-50 bg-slate-900/90 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in" @click="previewImage = null">
        <button class="absolute top-6 right-6 text-white hover:text-slate-300 p-2"><X class="w-8 h-8" /></button>
        <img :src="previewImage" class="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl" @click.stop />
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  ClipboardList, CheckCircle, Clock, MapPin, AlertTriangle, Wrench, 
  UserCheck, Building, Activity, PlayCircle, Image as ImageIcon, FileText, 
  Search, LayoutGrid, List, Phone, Upload, Camera, X, User, LayoutDashboard
} from 'lucide-vue-next'

// --- State ---
const isSidebarOpen = ref(false)
const viewMode = ref('grid') // 'grid' | 'list'
const expandedTask = ref('CMP-8902') // Automatically expand the active task
const previewImage = ref(null)

const workProgress = ref(65)
const workNotes = ref('')
const beforeImages = ref(['https://images.unsplash.com/photo-1544257121-654dbbc305e7?w=400&fit=crop'])
const afterImages = ref([])

const filters = reactive({
  search: '',
  status: 'All',
  priority: 'All',
  sort: 'Priority'
})

const completionChecklist = reactive({
  'Work completed securely': false,
  'Area cleaned & debris removed': false,
  'After-work photos uploaded': false,
  'Materials usage recorded': false,
  'Safety protocol followed': true
})

// --- Mock Data: Active Task Focus ---
const task = reactive({
  id: 'CMP-8902',
  title: 'Fallen Live Wire near Pedestrian Walkway',
  category: 'Electrical Maintenance',
  priority: 'Emergency',
  status: 'In Progress',
  area: 'Downtown Sector 4',
  ward: 'Ward 14',
  deadline: 'Today, 02:00 PM',
  officer: 'Rahul Sharma',
  description: 'A heavy branch fell during the storm, snapping a live electrical wire which is currently on the pedestrian walkway. Immediate isolation and repair required to prevent fatal accidents.',
  images: [
    'https://images.unsplash.com/photo-1544257121-654dbbc305e7?w=400&fit=crop',
    'https://images.unsplash.com/photo-1584985614946-bdeeb2bc4db1?w=400&fit=crop'
  ],
  location: { address: 'Near Central Park Gate 2, Main Road', landmark: 'Opposite State Bank', lat: '18.5204', lng: '73.8567' },
  instructions: [
    'Ensure full Class 2 safety gear is worn.',
    'Wait for grid shutdown confirmation from control room before touching wires.',
    'Isolate the area with warning cones to keep pedestrians away.',
    'Splice and secure the connection, upload testing evidence.'
  ],
  materials: [
    { name: 'Insulation Tape (HV)', qty: '2 Rolls', used: true },
    { name: 'Wire Splice Kit', qty: '1 Kit', used: false },
    { name: 'Warning Cones', qty: '4 Units', used: true }
  ],
  safetyChecklist: [
    { text: 'Wear electrical safety gloves and helmet.', checked: true },
    { text: 'Verify grid power is disconnected using tester.', checked: true },
    { text: 'Place warning cones 10m away from site.', checked: true }
  ],
  citizen: { name: 'Priya Sharma', notes: 'Sparks were flying from the wire. I have warned people to stay away but please come fast.' },
  timeline: [
    { action: 'Work Progress Updated to 65%', date: 'Today', time: '11:30 AM', user: 'You' },
    { action: 'Work Started', date: 'Today', time: '09:15 AM', user: 'You' },
    { action: 'Task Accepted', date: 'Today', time: '08:45 AM', user: 'You' },
    { action: 'Task Assigned', date: 'Today', time: '08:30 AM', user: 'Officer Rahul Sharma' }
  ]
})

const summaryStats = [
  { title: 'Total Assigned', value: '8', icon: ClipboardList, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Pending', value: '2', icon: Clock, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'In Progress', value: '2', icon: Activity, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { title: 'Completed Today', value: '3', trend: 1, icon: CheckCircle, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'Overdue', value: '0', icon: AlertTriangle, iconBg: 'bg-slate-100', iconColor: 'text-slate-400' }
]

// Array of background tasks for list/grid view
const tasksList = [task] // Reduced to 1 for this focused detailed view example

// --- Computed & Methods ---
const progressStages = ['Assigned', 'Accepted', 'Travelling', 'Reached Site', 'In Progress', 'Completed']
const currentStageIndex = computed(() => {
  const map = { 'Assigned': 0, 'Accepted': 1, 'Travelling': 2, 'Reached Site': 3, 'In Progress': 4, 'Completed': 5 }
  return map[task.status] || 0
})
const progressPercentage = computed(() => (currentStageIndex.value / (progressStages.length - 1)) * 100)

const filteredTasks = computed(() => tasksList)

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700 border border-red-200', 'High': 'bg-orange-100 text-orange-700 border border-orange-200', 'Medium': 'bg-blue-100 text-blue-700 border border-blue-200', 'Low': 'bg-slate-100 text-slate-600 border border-slate-200' }
  return map[priority]
}

const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Completed': 'bg-green-100 text-green-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const actionButtonTheme = (status) => status === 'Assigned' ? 'bg-[#2563EB] hover:bg-[#1E40AF]' : 'bg-[#F59E0B] hover:bg-amber-600'
const actionButtonText = (status) => status === 'Assigned' ? 'Accept Task' : 'Update Status'
const actionButtonIcon = (status) => status === 'Assigned' ? CheckCircle : PlayCircle

const getProgress = (status) => status === 'In Progress' ? workProgress.value : (status === 'Completed' ? 100 : 0)
const isOverdue = (deadline) => deadline.toLowerCase().includes('today')

const toggleExpand = (id) => expandedTask.value = expandedTask.value === id ? null : id
const openImagePreview = (img) => previewImage.value = img

const handleUpload = (e, type) => {
  const file = e.target.files[0]
  if (file) {
    const url = URL.createObjectURL(file)
    if (type === 'before') beforeImages.value.push(url)
    else afterImages.value.push(url)
  }
}

const removeImage = (type, index) => {
  if (type === 'before') beforeImages.value.splice(index, 1)
  else afterImages.value.splice(index, 1)
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