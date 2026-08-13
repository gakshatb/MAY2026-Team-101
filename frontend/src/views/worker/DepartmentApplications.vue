<template>
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar relative">

        <!-- Header & Breadcrumbs -->
        <header class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2">
              <router-link to="/worker/dashboard" class="hover:text-[#2563EB]">Dashboard</router-link>
              <span class="mx-2">/</span>
              <span class="text-gray-900 font-medium">Department Applications</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Department Applications</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Apply to departments and track your application status.
            </p>
          </div>
        </header>

        <div v-if="loading" class="bg-white rounded-[14px] shadow-sm border border-gray-100 p-10 text-center text-gray-500">Loading departments…</div>
        <div v-else-if="loadError" class="bg-white rounded-[14px] shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>

        <template v-else>
          <!-- Top Statistics Grid -->
          <section class="mb-8 grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
            <div v-for="(stat, index) in topStats" :key="index" class="bg-white p-5 rounded-[14px] shadow-sm hover:shadow-md transition-shadow border border-gray-50 flex flex-col">
              <div class="flex items-center gap-3 mb-3">
                <div :class="`p-2.5 rounded-lg ${stat.bg}`">
                  <component :is="stat.icon" class="w-5 h-5" :class="stat.text" />
                </div>
              </div>
              <h3 class="text-2xl font-bold text-gray-900 mb-1">{{ stat.value }}</h3>
              <span class="text-sm text-gray-500 font-medium">{{ stat.label }}</span>
            </div>
          </section>

          <!-- Search & Filter Section -->
          <section id="browse" class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col xl:flex-row gap-4 items-center justify-between">
            <div class="w-full xl:w-1/3 relative">
              <Search class="w-5 h-5 text-gray-400 absolute left-3 top-3" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search departments or codes..."
                class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
            <div class="w-full xl:w-auto flex flex-wrap gap-3">
              <select v-model="sortBy" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
                <option value="Name">Sort by Name</option>
                <option value="Workers">Most Workers</option>
              </select>
              <button @click="searchQuery = ''; sortBy = 'Name'" class="px-4 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">
                Reset
              </button>
            </div>
          </section>

          <!-- Available Departments Section -->
          <section class="mb-10">
            <div v-if="!canApply" class="mb-5 bg-amber-50 border border-amber-200 rounded-[14px] p-4 flex items-start gap-3">
              <Clock class="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
              <p class="text-sm text-amber-800">
                You have an ongoing task, so new department applications are disabled until it's marked Resolved. You can still track existing applications below.
              </p>
            </div>
            <h2 class="text-lg font-bold text-gray-900 mb-5">Departments</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              <div v-for="dept in filteredDepartments" :key="dept.id" class="bg-white rounded-[14px] border border-gray-100 shadow-sm hover:shadow-md transition-all p-5 flex flex-col relative overflow-hidden">
                <div v-if="dept.applicationStatus !== 'Not Applied'" :class="['absolute top-0 right-0 px-3 py-1 text-[10px] font-bold uppercase tracking-wide rounded-bl-lg', getStatusBgClass(dept.applicationStatus)]">
                  {{ dept.applicationStatus }}
                </div>
                <div class="flex items-start gap-4 mb-4">
                  <div class="w-12 h-12 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0">
                    <Building2 class="w-6 h-6" />
                  </div>
                  <div>
                    <h3 class="font-bold text-gray-900 leading-tight">{{ dept.name }}</h3>
                    <p class="text-xs text-gray-500 mt-1">{{ dept.code || 'No code' }}</p>
                  </div>
                </div>
                <p class="text-sm text-gray-600 mb-4 line-clamp-2 flex-1">{{ dept.description || 'No description available.' }}</p>

                <div class="grid grid-cols-2 gap-2 text-sm mb-5">
                  <div class="bg-gray-50 p-2 rounded-lg text-center">
                    <p class="text-xs text-gray-500 mb-0.5">Head</p>
                    <p class="font-bold text-gray-900 text-xs truncate">{{ dept.head || '—' }}</p>
                  </div>
                  <div class="bg-gray-50 p-2 rounded-lg text-center">
                    <p class="text-xs text-gray-500 mb-0.5">Workers</p>
                    <p class="font-bold text-gray-900">{{ dept.workerCount }}</p>
                  </div>
                </div>

                <div class="flex gap-3">
                  <button
                    v-if="dept.applicationStatus === 'Not Applied' && canApply"
                    @click="openApplyModal(dept)"
                    class="flex-1 py-2 bg-[#2563EB] text-white rounded-xl text-sm font-medium hover:bg-[#1E40AF] transition-colors shadow-sm"
                  >
                    Apply Now
                  </button>
                  <button
                    v-else-if="dept.applicationStatus === 'Not Applied' && !canApply"
                    disabled
                    title="Finish or hand off your current task before applying to a new department."
                    class="flex-1 py-2 bg-gray-100 text-gray-400 rounded-xl text-sm font-medium cursor-not-allowed"
                  >
                    Ongoing Task
                  </button>
                  <button
                    v-else-if="dept.applicationStatus === 'Pending'"
                    @click="openWithdrawModal(dept)"
                    class="flex-1 py-2 bg-yellow-50 text-yellow-700 border border-yellow-200 rounded-xl text-sm font-medium hover:bg-yellow-100 transition-colors"
                  >
                    Withdraw Application
                  </button>
                  <button v-else class="flex-1 py-2 bg-green-50 text-green-700 border border-green-200 rounded-xl text-sm font-medium cursor-default">
                    Current Department
                  </button>
                </div>
              </div>

              <div v-if="filteredDepartments.length === 0" class="col-span-full py-12 text-center bg-white rounded-[14px] border border-gray-100">
                <Search class="w-10 h-10 text-gray-300 mx-auto mb-3" />
                <h3 class="text-lg font-medium text-gray-900">No departments found</h3>
                <p class="text-gray-500 text-sm mt-1">Try adjusting your search.</p>
              </div>
            </div>
          </section>

          <!-- My Applications Table -->
          <section id="applications" class="mb-10">
            <h2 class="text-lg font-bold text-gray-900 mb-5">My Application History</h2>

            <div v-if="applications.length === 0" class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-8 text-center text-gray-500">
              You haven't applied to any departments yet.
            </div>

            <template v-else>
              <!-- Desktop Table -->
              <div class="hidden md:block bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden">
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                      <th class="p-4 font-semibold">Department</th>
                      <th class="p-4 font-semibold">Applied Date</th>
                      <th class="p-4 font-semibold">Status</th>
                      <th class="p-4 font-semibold">Remark</th>
                      <th class="p-4 font-semibold text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100 text-sm">
                    <tr v-for="app in applications" :key="app.id" class="hover:bg-gray-50 transition-colors">
                      <td class="p-4 font-medium text-gray-900">{{ app.departmentName }}</td>
                      <td class="p-4 text-gray-600">{{ formatDate(app.appliedAt) }}</td>
                      <td class="p-4">
                        <span :class="['px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 w-max', getStatusClass(app.status)]">
                          <span class="w-1.5 h-1.5 rounded-full bg-current"></span> {{ app.status }}
                        </span>
                      </td>
                      <td class="p-4 text-gray-500 text-xs max-w-[220px] truncate">{{ app.remark || (app.status === 'Pending' ? 'Awaiting review…' : '—') }}</td>
                      <td class="p-4 text-right">
                        <button v-if="app.status === 'Pending'" @click="openWithdrawModalFromApp(app)" class="text-sm font-medium text-red-600 hover:text-red-800">Withdraw</button>
                        <span v-else class="text-sm text-gray-400">—</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Mobile Cards -->
              <div class="md:hidden space-y-4">
                <div v-for="app in applications" :key="app.id" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50">
                  <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-gray-900">{{ app.departmentName }}</h3>
                    <span :class="['px-2 py-0.5 rounded-full text-[10px] font-semibold', getStatusClass(app.status)]">{{ app.status }}</span>
                  </div>
                  <div class="text-xs text-gray-500 mb-3 space-y-1">
                    <p>Applied: <span class="font-medium text-gray-900">{{ formatDate(app.appliedAt) }}</span></p>
                    <p v-if="app.remark" class="italic mt-2 text-gray-600">"{{ app.remark }}"</p>
                  </div>
                  <button v-if="app.status === 'Pending'" @click="openWithdrawModalFromApp(app)" class="w-full py-2 bg-red-50 text-red-700 rounded-lg text-sm font-medium hover:bg-red-100 transition-colors">Withdraw Application</button>
                </div>
              </div>
            </template>
          </section>

          <!-- Tips -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <section class="bg-[#2563EB] rounded-[14px] shadow-sm border border-[#1E40AF] p-6 text-white relative overflow-hidden lg:col-span-2">
              <div class="absolute right-0 top-0 opacity-10">
                <BadgeCheck class="w-32 h-32 transform translate-x-8 -translate-y-8" />
              </div>
              <h2 class="text-lg font-bold mb-3 flex items-center gap-2 relative z-10">
                <Lightbulb class="w-5 h-5" /> Tips for Success
              </h2>
              <ul class="space-y-2 text-sm text-blue-100 relative z-10">
                <li class="flex items-start gap-2"><CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-blue-300"/> Keep your profile complete and up to date before applying.</li>
                <li class="flex items-start gap-2"><CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-blue-300"/> You can only have one pending application per department at a time.</li>
                <li class="flex items-start gap-2"><CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-blue-300"/> An admin reviews every application — you'll be notified either way.</li>
              </ul>
            </section>
          </div>
        </template>
      </main>

    <!-- Apply Modal -->
    <Teleport to="body">
      <div v-if="showApplyModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" @click="closeModals"></div>
        <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-lg p-6">
          <h2 class="text-xl font-bold text-gray-900 mb-1">Apply to {{ targetDept?.name }}</h2>
          <p class="text-sm text-gray-500 mb-5">Submit a note for the admin reviewing your request.</p>
          <form @submit.prevent="submitApplication" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Note to Admin (optional)</label>
              <textarea v-model="applyMessage" rows="3" maxlength="500" class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none custom-scrollbar" placeholder="Why are you a good fit for this department?"></textarea>
            </div>
            <p v-if="applyError" class="text-sm text-red-600">{{ applyError }}</p>
            <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
              <button type="button" @click="closeModals" class="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
              <button type="submit" :disabled="submitting" class="px-5 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl transition-colors shadow-sm disabled:opacity-60">{{ submitting ? 'Submitting…' : 'Submit Application' }}</button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Withdraw Modal -->
    <Teleport to="body">
      <div v-if="showWithdrawModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" @click="closeModals"></div>
        <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center">
          <div class="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertTriangle class="w-8 h-8" />
          </div>
          <h2 class="text-xl font-bold text-gray-900 mb-2">Withdraw Application?</h2>
          <p class="text-sm text-gray-500 mb-6">
            Are you sure you want to withdraw your pending application for <strong class="text-gray-900">{{ withdrawTarget?.name || withdrawTarget?.departmentName }}</strong>?
          </p>
          <p v-if="withdrawError" class="text-sm text-red-600 mb-3">{{ withdrawError }}</p>
          <div class="flex justify-center gap-3">
            <button @click="closeModals" class="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
            <button @click="confirmWithdraw" :disabled="submitting" class="px-5 py-2 text-sm font-medium text-white bg-[#EF4444] hover:bg-red-700 rounded-xl transition-colors shadow-sm disabled:opacity-60">{{ submitting ? 'Withdrawing…' : 'Withdraw' }}</button>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import {
  Building2, Briefcase, ShieldCheck, Clock, AlertTriangle,
  ClipboardList, Search, Lightbulb, BadgeCheck, CheckCircle
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

const loading = ref(true)
const loadError = ref('')
const departments = ref([])
const canApply = ref(true)
const applications = ref([])

const searchQuery = ref('')
const sortBy = ref('Name')

const showApplyModal = ref(false)
const showWithdrawModal = ref(false)
const targetDept = ref(null)
const withdrawTarget = ref(null)
const applyMessage = ref('')
const applyError = ref('')
const withdrawError = ref('')
const submitting = ref(false)

const topStats = computed(() => {
  const pending = applications.value.filter(a => a.status === 'Pending').length
  const approved = applications.value.filter(a => a.status === 'Approved').length
  const rejected = applications.value.filter(a => a.status === 'Rejected').length
  return [
    { label: 'Available Depts', value: departments.value.length, icon: Building2, bg: 'bg-gray-100', text: 'text-gray-600' },
    { label: 'Applied', value: applications.value.length, icon: Briefcase, bg: 'bg-blue-100', text: 'text-[#2563EB]' },
    { label: 'Approved', value: approved, icon: ShieldCheck, bg: 'bg-green-100', text: 'text-[#22C55E]' },
    { label: 'Pending', value: pending, icon: Clock, bg: 'bg-yellow-100', text: 'text-[#F59E0B]' },
    { label: 'Rejected', value: rejected, icon: AlertTriangle, bg: 'bg-red-100', text: 'text-[#EF4444]' },
    { label: 'Total Apps', value: applications.value.length, icon: ClipboardList, bg: 'bg-purple-100', text: 'text-purple-600' },
  ]
})

const filteredDepartments = computed(() => {
  let result = departments.value
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(d => d.name.toLowerCase().includes(q) || (d.code || '').toLowerCase().includes(q))
  }
  result = [...result]
  if (sortBy.value === 'Workers') {
    result.sort((a, b) => b.workerCount - a.workerCount)
  } else {
    result.sort((a, b) => a.name.localeCompare(b.name))
  }
  return result
})

const getStatusClass = (status) => {
  switch (status) {
    case 'Approved': return 'bg-green-50 text-green-700 border border-green-200'
    case 'Pending': return 'bg-yellow-50 text-yellow-700 border border-yellow-200'
    case 'Rejected': return 'bg-red-50 text-red-700 border border-red-200'
    case 'Withdrawn': return 'bg-gray-100 text-gray-600 border border-gray-200'
    default: return 'bg-gray-100 text-gray-600 border border-gray-200'
  }
}

const getStatusBgClass = (status) => {
  switch (status) {
    case 'Current': return 'bg-green-500 text-white'
    case 'Pending': return 'bg-yellow-500 text-white'
    default: return 'bg-gray-200 text-gray-600'
  }
}

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

function closeModals() {
  showApplyModal.value = false
  showWithdrawModal.value = false
  targetDept.value = null
  withdrawTarget.value = null
  applyMessage.value = ''
  applyError.value = ''
  withdrawError.value = ''
}

function openApplyModal(dept) {
  if (!canApply.value) return
  targetDept.value = dept
  applyMessage.value = ''
  applyError.value = ''
  showApplyModal.value = true
}

function openWithdrawModal(dept) {
  withdrawTarget.value = { ...dept, applicationId: dept.application?.id }
  withdrawError.value = ''
  showWithdrawModal.value = true
}

function openWithdrawModalFromApp(app) {
  withdrawTarget.value = { departmentName: app.departmentName, applicationId: app.id }
  withdrawError.value = ''
  showWithdrawModal.value = true
}

async function loadData() {
  loading.value = true
  loadError.value = ''
  try {
    const [deptRes, appRes] = await Promise.all([
      axios.get(`${API_BASE}/worker/departments`, { headers: authHeaders() }),
      axios.get(`${API_BASE}/worker/department-applications`, { headers: authHeaders() })
    ])
    departments.value = deptRes.data.departments || []
    canApply.value = deptRes.data.canApply !== false
    applications.value = appRes.data.applications || []
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load departments.'
  } finally {
    loading.value = false
  }
}

async function submitApplication() {
  if (!targetDept.value) return
  submitting.value = true
  applyError.value = ''
  try {
    await axios.post(`${API_BASE}/worker/department-applications`, {
      departmentId: targetDept.value.id,
      message: applyMessage.value.trim()
    }, { headers: authHeaders() })
    closeModals()
    await loadData()
  } catch (err) {
    applyError.value = err.response?.data?.message || 'Failed to submit application.'
  } finally {
    submitting.value = false
  }
}

async function confirmWithdraw() {
  if (!withdrawTarget.value?.applicationId) return
  submitting.value = true
  withdrawError.value = ''
  try {
    await axios.delete(`${API_BASE}/worker/department-applications/${withdrawTarget.value.applicationId}`, { headers: authHeaders() })
    closeModals()
    await loadData()
  } catch (err) {
    withdrawError.value = err.response?.data?.message || 'Failed to withdraw application.'
  } finally {
    submitting.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }

.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>