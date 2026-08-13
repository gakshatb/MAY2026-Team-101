<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1400px] mx-auto space-y-6 animate-fade-in">

          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/admin/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Department Applications</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Department Applications</h1>
              <p class="text-slate-500 mt-1">Review worker requests to transfer into a department.</p>
            </div>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-amber-50 text-amber-500 mb-2"><Clock class="w-4 h-4" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ counts.pending ?? 0 }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Pending Review</p>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-green-50 text-green-500 mb-2"><CheckCircle class="w-4 h-4" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ counts.approved ?? 0 }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Approved</p>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-red-50 text-red-500 mb-2"><XCircle class="w-4 h-4" /></div>
              <p class="text-2xl font-extrabold text-slate-900">{{ counts.rejected ?? 0 }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Rejected</p>
            </div>
          </div>

          <!-- Filter Tabs -->
          <div class="flex gap-2 bg-white p-2 rounded-2xl shadow-sm border border-slate-100 w-fit">
            <button v-for="tab in tabs" :key="tab" @click="activeTab = tab; loadApplications()" :class="`px-4 py-2 rounded-xl text-sm font-bold transition-colors ${activeTab === tab ? 'bg-[#2563EB] text-white' : 'text-slate-500 hover:bg-slate-50'}`">
              {{ tab }}
            </button>
          </div>

          <div v-if="loading" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-10 text-center text-slate-500">Loading applications…</div>
          <div v-else-if="loadError" class="bg-white rounded-[14px] shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>
          <div v-else-if="applications.length === 0" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-10 text-center text-slate-500">No applications here.</div>

          <div v-else class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm whitespace-nowrap">
                <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide border-b border-slate-100">
                  <tr>
                    <th class="px-5 py-4">Worker</th>
                    <th class="px-5 py-4">Current Dept</th>
                    <th class="px-5 py-4">Applying To</th>
                    <th class="px-5 py-4">Applied</th>
                    <th class="px-5 py-4">Status</th>
                    <th class="px-5 py-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="app in applications" :key="app.id" class="hover:bg-slate-50 transition-colors">
                    <td class="px-5 py-4">
                      <p class="font-bold text-slate-900">{{ app.workerName }}</p>
                      <p class="text-xs text-slate-500">{{ app.workerEmail }}</p>
                    </td>
                    <td class="px-5 py-4 text-slate-600">{{ app.currentDepartment || 'Unassigned' }}</td>
                    <td class="px-5 py-4 font-semibold text-slate-900">{{ app.departmentName }}</td>
                    <td class="px-5 py-4 text-slate-600">{{ formatDate(app.appliedAt) }}</td>
                    <td class="px-5 py-4">
                      <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${statusBadge(app.status)}`">{{ app.status }}</span>
                    </td>
                    <td class="px-5 py-4 text-right">
                      <div v-if="app.status === 'Pending'" class="flex items-center justify-end gap-2">
                        <button @click="openReview(app, 'Approved')" class="px-3 py-1.5 bg-green-600 text-white text-xs font-bold rounded hover:bg-green-700 transition-colors">Approve</button>
                        <button @click="openReview(app, 'Rejected')" class="px-3 py-1.5 bg-red-600 text-white text-xs font-bold rounded hover:bg-red-700 transition-colors">Reject</button>
                      </div>
                      <span v-else class="text-xs text-slate-400">{{ app.remark || '—' }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </main>

    <!-- Review Modal -->
    <Teleport to="body">
      <div v-if="reviewApp" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
        <div class="bg-white rounded-2xl w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 bg-slate-50">
            <h3 class="font-bold text-lg text-slate-900">{{ reviewDecision }} Application</h3>
          </div>
          <div class="p-6 space-y-4">
            <p class="text-sm text-slate-600">
              <strong class="text-slate-900">{{ reviewApp.workerName }}</strong> → <strong class="text-slate-900">{{ reviewApp.departmentName }}</strong>
            </p>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Remark {{ reviewDecision === 'Rejected' ? '(required)' : '(optional)' }}</label>
              <textarea v-model="reviewRemark" rows="3" maxlength="500" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none resize-none"></textarea>
            </div>
            <p v-if="reviewError" class="text-sm text-red-600">{{ reviewError }}</p>
          </div>
          <div class="p-5 border-t border-slate-100 bg-slate-50 flex gap-3">
            <button @click="reviewApp = null" class="flex-1 py-2.5 bg-white border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-100 transition-colors text-sm">Cancel</button>
            <button @click="submitReview" :disabled="submitting" class="flex-1 py-2.5 text-white font-bold rounded-lg transition-colors shadow-sm text-sm disabled:opacity-60" :class="reviewDecision === 'Approved' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'">{{ submitting ? 'Saving…' : `Confirm ${reviewDecision}` }}</button>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Clock, CheckCircle, XCircle } from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

const loading = ref(true)
const loadError = ref('')
const applications = ref([])
const counts = ref({})
const activeTab = ref('Pending')
const tabs = ['Pending', 'Approved', 'Rejected', 'All']

const reviewApp = ref(null)
const reviewDecision = ref('Approved')
const reviewRemark = ref('')
const reviewError = ref('')
const submitting = ref(false)

const statusBadge = (status) => {
  const map = { 'Pending': 'bg-amber-100 text-amber-700', 'Approved': 'bg-green-100 text-green-700', 'Rejected': 'bg-red-100 text-red-700', 'Withdrawn': 'bg-slate-200 text-slate-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function loadApplications() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/admin/department-applications`, {
      headers: authHeaders(),
      params: { status: activeTab.value }
    })
    applications.value = data.applications || []
    counts.value = data.counts || {}
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load applications.'
  } finally {
    loading.value = false
  }
}

function openReview(app, decision) {
  reviewApp.value = app
  reviewDecision.value = decision
  reviewRemark.value = ''
  reviewError.value = ''
}

async function submitReview() {
  reviewError.value = ''
  if (reviewDecision.value === 'Rejected' && !reviewRemark.value.trim()) {
    reviewError.value = 'A remark is required when rejecting an application.'
    return
  }
  submitting.value = true
  try {
    await axios.patch(`${API_BASE}/admin/department-applications/${reviewApp.value.id}`, {
      status: reviewDecision.value,
      remark: reviewRemark.value.trim()
    }, { headers: authHeaders() })
    reviewApp.value = null
    await loadApplications()
  } catch (err) {
    reviewError.value = err.response?.data?.message || 'Failed to submit review.'
  } finally {
    submitting.value = false
  }
}

onMounted(loadApplications)
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
