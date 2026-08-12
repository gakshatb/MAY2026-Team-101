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
                <template v-if="route.params.id">
                  <span class="mx-2">›</span>
                  <router-link :to="`/worker/task/${complaint.raw_id}`" class="hover:text-[#2563EB] transition-colors">Task Details</router-link>
                </template>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Update Progress</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Update Complaint</h1>
              <p class="text-slate-500 mt-1">Update task status, upload evidence, and add work notes.</p>
            </div>
            <a v-if="complaint.officer_phone" :href="`tel:${complaint.officer_phone}`" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
              <Phone class="w-4 h-4 text-slate-400" /> Contact Officer
            </a>
          </div>

          <!-- No task selected: pick one -->
          <ComplaintPicker
            v-if="!route.params.id"
            title="Select a Task to Update"
            subtitle="Choose one of your ongoing tasks"
            actionLabel="Update"
            empty-message="You have no ongoing tasks to update right now."
            fetch-url="/worker/tasks"
            data-key="tasks"
            :show-submit-cta="false"
            @select="goToUpdate"
          />

          <template v-else>
            <div v-if="loading" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-10 text-center text-slate-500">Loading task…</div>
            <div v-else-if="loadError" class="bg-white rounded-[14px] shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>

            <template v-else>
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
                    <span class="flex items-center gap-1"><MapPin class="w-4 h-4 text-slate-400" /> {{ complaint.area }}</span>
                    <span class="flex items-center gap-1"><User class="w-4 h-4 text-slate-400" /> Officer: {{ complaint.officer || 'Unassigned' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Already completed notice -->
            <div v-if="isFinal" class="bg-green-50 border border-green-200 rounded-[14px] p-6 text-center">
              <CheckCircle class="w-10 h-10 text-green-500 mx-auto mb-3" />
              <h3 class="font-bold text-green-800 mb-1">This task is already {{ complaint.status }}</h3>
              <p class="text-sm text-green-700 mb-4">No further updates can be made to a completed task.</p>
              <router-link :to="`/worker/task/${complaint.raw_id}`" class="inline-block px-4 py-2 bg-white border border-green-200 text-green-700 text-sm font-bold rounded-lg hover:bg-green-100 transition-colors">View Task Details</router-link>
            </div>

            <!-- Main Layout Grid -->
            <div v-else class="grid grid-cols-1 xl:grid-cols-12 gap-6">

              <!-- Left Column: Work Execution Form (8 cols) -->
              <div class="xl:col-span-8 flex flex-col gap-6">

                <!-- Status Controls -->
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                  <div class="p-5 border-b border-slate-100 bg-slate-50/50">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><Activity class="w-5 h-5 text-[#2563EB]" /> Update Status</h3>
                  </div>
                  <div class="p-5 space-y-6">

                    <!-- Stage Tracker -->
                    <div class="w-full relative py-2">
                      <div class="flex items-center justify-between relative">
                        <div class="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-slate-100 rounded-full z-0"></div>
                        <div class="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-[#2563EB] rounded-full z-0 transition-all duration-500" :style="`width: ${stagePercentage}%`"></div>
                        <div v-for="(stage, idx) in stages" :key="stage" class="relative z-10 flex flex-col items-center gap-1.5">
                          <div :class="`w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs border-2 transition-colors duration-300 bg-white ${currentStageIndex >= idx ? 'border-[#2563EB] text-[#2563EB]' : 'border-slate-200 text-slate-300'}`">
                            <CheckCircle v-if="currentStageIndex > idx" class="w-3.5 h-3.5" />
                            <span v-else>{{ idx + 1 }}</span>
                          </div>
                          <span :class="`text-[9px] font-bold uppercase tracking-wider text-center ${currentStageIndex >= idx ? 'text-slate-800' : 'text-slate-400'}`">{{ stage }}</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Set New Status</label>
                      <select v-model="form.status" class="w-full bg-white border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] p-2.5 outline-none font-medium shadow-sm transition-all">
                        <option v-for="opt in statusOptions" :key="opt" :value="opt">{{ opt }}</option>
                      </select>
                      <p v-if="form.status === 'Resolved'" class="text-xs text-amber-600 font-medium mt-1.5">A resolution note is required to mark this task Resolved.</p>
                    </div>
                  </div>
                </div>

                <!-- Evidence Uploads -->
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                  <div class="p-5 border-b border-slate-100 bg-slate-50/50">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><Camera class="w-5 h-5 text-slate-400" /> Work Evidence Photos</h3>
                  </div>
                  <div class="p-5">
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      <div v-for="(img, idx) in complaint.images" :key="idx" class="aspect-square rounded-xl bg-slate-100 relative overflow-hidden border border-slate-200">
                        <img :src="imgSrc(img)" class="w-full h-full object-cover" />
                      </div>
                      <label class="aspect-square rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 hover:bg-slate-100 transition-colors flex flex-col items-center justify-center cursor-pointer group">
                        <Upload class="w-5 h-5 text-slate-400 group-hover:text-[#2563EB] mb-1 transition-colors" />
                        <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wide">{{ photoUploading ? 'Uploading…' : 'Upload' }}</span>
                        <input type="file" accept="image/jpeg, image/png, image/jpg" class="hidden" @change="handlePhotoUpload" :disabled="photoUploading" />
                      </label>
                    </div>
                    <p v-if="photoError" class="text-xs text-red-600 mt-3">{{ photoError }}</p>
                  </div>
                </div>

                <!-- Work Notes / Resolution Remark -->
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                  <div class="flex justify-between items-end mb-3">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><FileText class="w-5 h-5 text-slate-400" /> Work Notes {{ form.status === 'Resolved' ? '(required)' : '(optional)' }}</h3>
                    <span class="text-xs font-medium text-slate-400">{{ form.notes.length }}/500</span>
                  </div>
                  <textarea
                    v-model="form.notes"
                    maxlength="500"
                    rows="4"
                    placeholder="Describe the work completed, materials used, or remaining activities..."
                    class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none resize-none transition-all"
                  ></textarea>
                </div>

                <!-- Main Action Buttons -->
                <div class="flex flex-col sm:flex-row items-center justify-end gap-3 pt-2">
                  <router-link :to="`/worker/task/${complaint.raw_id}`" class="w-full sm:w-auto px-6 py-3 bg-white border border-slate-300 text-slate-700 text-sm font-bold rounded-xl hover:bg-slate-50 transition-colors text-center">Cancel</router-link>
                  <button @click="openConfirmModal" class="w-full sm:w-auto px-6 py-3 bg-[#2563EB] text-white text-sm font-bold rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2">
                    <CheckCircle class="w-4 h-4" /> Submit Update
                  </button>
                </div>

              </div>

              <!-- Right Column: Context & History (4 cols) -->
              <div class="xl:col-span-4 space-y-6">

                <!-- Progress Timeline -->
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><List class="w-5 h-5 text-slate-400" /> Status History</h3>
                  <div v-if="!complaint.history?.length" class="text-sm text-slate-500">No status changes recorded yet.</div>
                  <div v-else class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                    <div v-for="(event, idx) in complaint.history" :key="idx" class="relative">
                      <div class="absolute -left-[21px] w-2.5 h-2.5 rounded-full ring-4 ring-white border-2" :class="idx === 0 ? 'bg-[#2563EB] border-[#2563EB]' : 'bg-slate-300 border-slate-300'"></div>
                      <p class="text-sm font-bold text-slate-900">{{ event.old_status ? `${event.old_status} → ${event.new_status}` : event.new_status }}</p>
                      <p class="text-[10px] font-medium text-slate-500 mt-0.5">{{ formatDate(event.changed_at) }}</p>
                      <p v-if="event.remark" class="text-xs text-slate-600 mt-1 italic">"{{ event.remark }}"</p>
                    </div>
                  </div>
                </div>

                <!-- Quick Actions -->
                <div class="grid grid-cols-2 gap-3">
                  <router-link :to="`/worker/task/${complaint.raw_id}`" class="p-3 bg-white rounded-xl shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:bg-blue-50 transition-colors flex flex-col items-center justify-center text-center gap-2 group">
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
          </template>
          </template>
        </div>
      </main>

    <!-- Confirmation Modal -->
    <Teleport to="body">
      <div v-if="showConfirmModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white p-6 rounded-2xl max-w-sm w-full shadow-2xl">
          <h3 class="text-lg font-bold text-slate-900 mb-2">Confirm Update</h3>
          <p class="text-sm text-slate-600 mb-2">You are about to update the status to <strong class="text-slate-900">{{ form.status }}</strong>.</p>
          <p v-if="submitError" class="text-sm text-red-600 mb-2">{{ submitError }}</p>
          <div class="flex gap-3 mt-4">
            <button @click="showConfirmModal = false" class="flex-1 py-2.5 bg-slate-100 text-slate-700 font-bold rounded-lg hover:bg-slate-200 transition-colors">Cancel</button>
            <button @click="processUpdate" :disabled="isSubmitting" class="flex-1 py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex justify-center items-center gap-2 disabled:opacity-60">
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
          <p class="text-sm text-slate-600 mb-6">The complaint status has been updated and recorded in the system.</p>
          <div class="space-y-3">
            <router-link :to="`/worker/task/${complaint.raw_id}`" class="block w-full py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors">View Task</router-link>
            <router-link to="/worker/tasks" class="block w-full py-2.5 bg-slate-100 text-slate-700 font-bold rounded-lg hover:bg-slate-200 transition-colors">View Assigned Tasks</router-link>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import ComplaintPicker from '@/components/dashboard/ComplaintPicker.vue'
import {
  ClipboardList, CheckCircle, MapPin,
  User, Activity, FileText, Phone, Camera, Upload, List
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

defineProps({ id: { type: [String, Number], default: null } })

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const loadError = ref('')
const showConfirmModal = ref(false)
const showSuccessModal = ref(false)
const isSubmitting = ref(false)
const submitError = ref('')
const photoUploading = ref(false)
const photoError = ref('')

const form = reactive({ status: 'In Progress', notes: '' })
const complaint = reactive({})

const isFinal = computed(() => ['Resolved', 'Closed'].includes(complaint.status))

const stages = ['Assigned', 'In Progress', 'Resolved', 'Closed']
const statusOptions = computed(() => ['In Progress', 'Resolved'].filter(s => s !== complaint.status))

const currentStageIndex = computed(() => {
  const map = { 'Assigned': 0, 'In Progress': 1, 'Resolved': 2, 'Closed': 3 }
  return map[complaint.status] ?? 0
})
const stagePercentage = computed(() => (currentStageIndex.value / (stages.length - 1)) * 100)

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700 border border-red-200', 'High': 'bg-orange-100 text-orange-700 border border-orange-200', 'Medium': 'bg-blue-100 text-blue-700 border border-blue-200', 'Low': 'bg-slate-100 text-slate-600 border border-slate-200' }
  return map[priority] || 'bg-slate-100 text-slate-600 border border-slate-200'
}

const statusBadge = (status) => {
  const map = { 'Assigned': 'bg-slate-100 text-slate-700', 'In Progress': 'bg-amber-100 text-amber-700', 'Resolved': 'bg-green-100 text-green-700', 'Closed': 'bg-slate-200 text-slate-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const imgSrc = (path) => (path?.startsWith('http') ? path : `${API_BASE}/uploads/${path}`)

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const openConfirmModal = () => {
  submitError.value = ''
  if (form.status === 'Resolved' && !form.notes.trim()) {
    submitError.value = 'A resolution note is required to mark this task Resolved.'
  }
  showConfirmModal.value = true
}

async function processUpdate() {
  if (form.status === 'Resolved' && !form.notes.trim()) {
    submitError.value = 'A resolution note is required to mark this task Resolved.'
    return
  }
  isSubmitting.value = true
  submitError.value = ''
  try {
    const { data } = await axios.patch(
      `${API_BASE}/worker/tasks/${route.params.id}/status`,
      { status: form.status, notes: form.notes },
      { headers: authHeaders() }
    )
    Object.assign(complaint, data.task)
    showConfirmModal.value = false
    showSuccessModal.value = true
  } catch (error) {
    submitError.value = error.response?.data?.message || 'Unable to update this task. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

async function handlePhotoUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return
  photoUploading.value = true
  photoError.value = ''
  try {
    const formData = new FormData()
    formData.append('image', file)
    const { data } = await axios.post(`${API_BASE}/worker/tasks/${route.params.id}/photos`, formData, { headers: authHeaders() })
    complaint.images = [...(complaint.images || []), data.image_url]
  } catch (error) {
    photoError.value = error.response?.data?.message || 'Failed to upload photo.'
  } finally {
    photoUploading.value = false
    event.target.value = ''
  }
}

async function loadTask() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/worker/tasks/${route.params.id}`, { headers: authHeaders() })
    Object.assign(complaint, data.task)
    form.status = data.task.status === 'In Progress' ? 'Resolved' : 'In Progress'
  } catch (error) {
    loadError.value = error.response?.data?.message || 'Unable to load this task.'
  } finally {
    loading.value = false
  }
}

const goToUpdate = (rawId) => router.push(`/worker/update/${rawId}`)

watch(() => route.params.id, (id) => {
  if (id) loadTask()
}, { immediate: true })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>