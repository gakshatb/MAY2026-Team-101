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
                <span class="text-slate-900 font-semibold">{{ task.id || '...' }}</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Task Details</h1>
              <p class="text-slate-500 mt-1">Review task information and complete assigned work.</p>
            </div>
            <div v-if="task.officer_phone" class="flex gap-2">
              <a :href="`tel:${task.officer_phone}`" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
                <Phone class="w-4 h-4 text-slate-400" /> Call Officer
              </a>
            </div>
          </div>

          <!-- No task selected: pick one -->
          <ComplaintPicker
            v-if="!route.params.id"
            title="Select a Task"
            subtitle="Choose one of your tasks to view its full details"
            actionLabel="View Details"
            empty-message="You have no assigned tasks yet."
            fetch-url="/worker/tasks?status=all"
            data-key="tasks"
            :show-submit-cta="false"
            @select="goToTask"
          />

          <template v-else>
            <div v-if="loading" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-10 text-center text-slate-500">Loading task…</div>
            <div v-else-if="loadError" class="bg-white rounded-[14px] shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>

            <!-- Main Layout Grid -->
            <div v-else class="grid grid-cols-1 xl:grid-cols-12 gap-6">

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
                    <div class="flex gap-2" v-if="!['Resolved', 'Closed'].includes(task.status)">
                      <router-link :to="`/worker/update/${task.raw_id}`" class="px-4 py-2 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center gap-2">
                        <PlayCircle class="w-4 h-4" /> Update Task
                      </router-link>
                    </div>
                  </div>

                  <div class="grid grid-cols-2 md:grid-cols-3 gap-4 py-4 border-y border-slate-100 mb-6">
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Category</p>
                      <p class="font-medium text-slate-900 mt-1 flex items-center gap-1.5"><ClipboardList class="w-3.5 h-3.5 text-slate-400"/> {{ task.category }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Location</p>
                      <p class="font-medium text-slate-900 mt-1 flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-slate-400"/> {{ [task.ward, task.area].filter(Boolean).join(', ') || '—' }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Officer</p>
                      <p class="font-medium text-slate-900 mt-1 flex items-center gap-1.5"><User class="w-3.5 h-3.5 text-slate-400"/> {{ task.officer || 'Unassigned' }}</p>
                    </div>
                  </div>

                  <!-- Visual Progress Tracker -->
                  <div class="w-full relative">
                    <div class="overflow-x-auto pb-4 no-scrollbar">
                      <div class="flex items-center min-w-[500px] justify-between relative">
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

              <!-- Complaint Description & Images -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 md:p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><FileText class="w-5 h-5 text-slate-400" /> Complaint Details</h3>
                <p class="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-100 mb-4">
                  {{ task.description || 'No description provided.' }}
                </p>

                <template v-if="task.images?.length">
                  <h4 class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-3 mt-6">Complaint Photos</h4>
                  <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div v-for="(img, idx) in task.images" :key="idx" @click="openImagePreview(imgSrc(img))" class="aspect-square rounded-xl overflow-hidden cursor-pointer group relative border border-slate-200">
                      <img :src="imgSrc(img)" class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110" />
                      <div class="absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/30 transition-colors flex items-center justify-center">
                        <ImageIcon class="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    </div>
                  </div>
                </template>
              </div>

              <!-- Location Details -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 md:p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><MapPin class="w-5 h-5 text-slate-400" /> Location Information</h3>
                <div class="grid grid-cols-2 gap-y-4 gap-x-2 text-sm">
                  <div>
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Street</p>
                    <p class="font-medium text-slate-900 mt-0.5">{{ task.street || '—' }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Landmark</p>
                    <p class="font-medium text-slate-900 mt-0.5">{{ task.landmark || '—' }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">City</p>
                    <p class="font-medium text-slate-900 mt-0.5">{{ task.city || '—' }}</p>
                  </div>
                  <div>
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wide">Ward</p>
                    <p class="font-medium text-slate-900 mt-0.5">{{ task.ward || '—' }}</p>
                  </div>
                </div>
              </div>

            </div>

            <!-- Right Column: Context & Metadata (4 cols) -->
            <div class="xl:col-span-4 space-y-6">

              <!-- Rating (only for resolved/closed tasks) -->
              <div v-if="['Resolved', 'Closed'].includes(task.status)" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-3"><Star class="w-5 h-5 text-amber-400" /> Citizen Rating</h3>
                <div v-if="task.rating" class="flex items-center gap-1">
                  <Star v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= task.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                </div>
                <p v-else class="text-sm text-slate-500">No feedback submitted yet.</p>
              </div>

              <!-- Task Timeline -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Activity class="w-5 h-5 text-slate-400" /> Task Timeline</h3>
                <div v-if="!task.history?.length" class="text-sm text-slate-500">No status changes recorded yet.</div>
                <div v-else class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="(event, idx) in task.history" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 rounded-full ring-4 ring-white border-2" :class="idx === 0 ? 'bg-[#2563EB] border-[#2563EB]' : 'bg-slate-300 border-slate-300'"></div>
                    <p class="text-sm font-bold text-slate-900">{{ event.old_status ? `${event.old_status} → ${event.new_status}` : event.new_status }}</p>
                    <p class="text-[10px] font-medium text-slate-500 mt-0.5">{{ formatDate(event.changed_at) }}</p>
                    <p v-if="event.remark" class="text-xs text-slate-600 mt-1 italic">"{{ event.remark }}"</p>
                  </div>
                </div>
              </div>

              <!-- Quick Navigation -->
              <div class="grid grid-cols-2 gap-3">
                <router-link to="/worker/dashboard" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <LayoutDashboard class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">Dashboard</span>
                </router-link>
                <router-link to="/worker/tasks" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
                  <Building class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-xs font-bold text-slate-600 group-hover:text-[#2563EB]">My Tasks</span>
                </router-link>
              </div>

            </div>
          </div>
          </template>
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
import { ref, reactive, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import ComplaintPicker from '@/components/dashboard/ComplaintPicker.vue'
import {
  ClipboardList, CheckCircle, MapPin, Building, Activity, PlayCircle,
  Image as ImageIcon, FileText, Phone, X, User, LayoutDashboard, Star
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const loadError = ref('')
const previewImage = ref(null)

const task = reactive({})

const progressStages = ['Assigned', 'In Progress', 'Resolved', 'Closed']
const currentStageIndex = computed(() => {
  const map = { 'Assigned': 0, 'In Progress': 1, 'Resolved': 2, 'Closed': 3 }
  return map[task.status] ?? 0
})
const progressPercentage = computed(() => (currentStageIndex.value / (progressStages.length - 1)) * 100)

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700 border border-red-200', 'High': 'bg-orange-100 text-orange-700 border border-orange-200', 'Medium': 'bg-blue-100 text-blue-700 border border-blue-200', 'Low': 'bg-slate-100 text-slate-600 border border-slate-200' }
  return map[priority] || 'bg-slate-100 text-slate-600 border border-slate-200'
}

const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Resolved': 'bg-green-100 text-green-700', 'Closed': 'bg-slate-200 text-slate-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const imgSrc = (path) => (path?.startsWith('http') ? path : `${API_BASE}/uploads/${path}`)
const openImagePreview = (img) => previewImage.value = img

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function loadTask() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/worker/tasks/${route.params.id}`, { headers: authHeaders() })
    Object.assign(task, data.task)
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load this task.'
  } finally {
    loading.value = false
  }
}

const goToTask = (rawId) => router.push(`/worker/task/${rawId}`)

watch(() => route.params.id, (id) => {
  if (id) loadTask()
}, { immediate: true })
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