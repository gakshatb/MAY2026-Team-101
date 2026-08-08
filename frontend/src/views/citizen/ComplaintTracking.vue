<template>
  <!-- Loading State -->
  <div v-if="isLoading" class="h-full flex items-center justify-center text-slate-400">
    Loading tracking details...
  </div>

  <!-- No complaint selected: let the user pick one instead of a dead end -->
  <div v-else-if="!route.params.id" class="max-w-5xl mx-auto py-6">
    <ComplaintPicker title="Select a Complaint to Track"
      subtitle="Choose one of your complaints to see its full tracking timeline." action-label="Track"
      empty-message="No complaints available to track." @select="(id) => router.push(`/citizen/track/${id}`)" />
  </div>

  <!-- Complaint Not Found State -->
  <div v-else-if="!complaint" class="h-full flex items-center justify-center">
    <div class="text-center">
      <div class="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6">
        <SearchX class="w-10 h-10 text-slate-400" />
      </div>
      <h2 class="text-2xl font-bold text-slate-900 mb-2">Complaint Not Found</h2>
      <p class="text-slate-500 mb-6">The Complaint ID you are looking for does not exist.</p>
      <router-link to="/citizen/complaints"
        class="px-6 py-3 bg-[#2563EB] text-white rounded-lg font-medium hover:bg-[#1E40AF]">
        Return to My Complaints
      </router-link>
    </div>
  </div>

  <!-- Complaint Found State -->
  <div v-else class="max-w-7xl mx-auto space-y-8">

    <!-- Header -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-slate-900">Complaint Tracking</h1>
        <div class="flex items-center gap-2 mt-1">
          <span class="text-sm text-slate-500">Complaint ID:</span>
          <span class="text-sm font-mono font-bold bg-slate-200 px-2 py-0.5 rounded">{{ complaint.id }}</span>
        </div>
      </div>
      <div class="flex gap-3">
        <button @click="downloadReport"
          class="px-4 py-2 border border-slate-200 bg-white rounded-lg text-sm font-medium hover:bg-slate-50 flex items-center gap-2">
          <Download class="w-4 h-4" /> Download Report
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

      <!-- Left Column: Progress Tracker -->
      <div class="lg:col-span-2 space-y-6">

        <!-- Progress Tracker -->
        <div class="bg-white p-8 rounded-[14px] shadow-sm border border-slate-100">
          <h3 class="text-lg font-bold text-slate-900 mb-8">Progress Status</h3>
          <div class="space-y-0">
            <div v-for="(step, index) in timelineSteps" :key="step.title" class="relative pl-8 pb-8 last:pb-0">
              <!-- Line Connector -->
              <div v-if="index !== timelineSteps.length - 1"
                class="absolute left-[15px] top-8 w-0.5 h-full bg-slate-100"></div>

              <!-- Icon -->
              <div :class="[
                'absolute left-0 w-8 h-8 rounded-full flex items-center justify-center border-2 z-10 transition-colors',
                step.status === 'completed' ? 'bg-green-100 border-[#22C55E]' :
                  step.status === 'active' ? 'bg-blue-100 border-[#2563EB]' :
                    step.status === 'skipped' ? 'bg-slate-100 border-slate-300' : 'bg-white border-slate-200'
              ]">
                <Check v-if="step.status === 'completed'" class="w-4 h-4 text-[#22C55E]" />
                <div v-else-if="step.status === 'active'" class="w-2.5 h-2.5 bg-[#2563EB] rounded-full animate-pulse">
                </div>
                <SkipForward v-else-if="step.status === 'skipped'" class="w-3.5 h-3.5 text-slate-400" />
                <div v-else class="w-2.5 h-2.5 bg-slate-200 rounded-full"></div>
              </div>

              <div class="pt-0.5">
                <p :class="['font-bold', step.status === 'active' ? 'text-[#2563EB]' : step.status === 'skipped' ? 'text-slate-400' : 'text-slate-900']">{{ step.title
                  }}</p>
                <p class="text-xs text-slate-400 mt-1">{{ step.date || (step.status === 'skipped' ? 'Skipped' : 'Pending') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Activity Timeline Table -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h3 class="text-lg font-bold text-slate-900 mb-4">Activity Log</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead>
                <tr class="text-slate-500 uppercase text-[10px] tracking-wider border-b border-slate-100">
                  <th class="pb-3 font-semibold">Date</th>
                  <th class="pb-3 font-semibold">Status</th>
                  <th class="pb-3 font-semibold">Officer</th>
                  <th class="pb-3 font-semibold">Remarks</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-50">
                <tr v-for="act in activityLog" :key="act.id" class="text-slate-700">
                  <td class="py-4 font-medium">{{ act.date }}</td>
                  <td class="py-4">{{ act.status }}</td>
                  <td class="py-4">{{ act.officer }}</td>
                  <td class="py-4 text-slate-500">{{ act.remarks }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Right Column: Status & Map -->
      <div class="space-y-6">

        <!-- Status Card -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <div class="flex items-center justify-between mb-6">
            <h3 class="font-bold text-slate-900">Current Overview</h3>
            <span class="px-3 py-1 bg-blue-50 text-[#2563EB] text-xs font-bold rounded-full uppercase">{{
              complaint.status }}</span>
          </div>
          <div class="space-y-4">
            <div class="flex justify-between border-b border-slate-50 pb-2">
              <span class="text-sm text-slate-500">Department</span>
              <span class="text-sm font-semibold">{{ complaint.department }}</span>
            </div>
            <div class="flex justify-between border-b border-slate-50 pb-2">
              <span class="text-sm text-slate-500">Assigned To</span>
              <span class="text-sm font-semibold">Not yet assigned</span>
            </div>
            <div class="flex justify-between border-b border-slate-50 pb-2">
              <span class="text-sm text-slate-500">Priority</span>
              <span class="text-sm font-semibold">{{ complaint.priority }}</span>
            </div>
          </div>
        </div>

        <!-- Map Placeholder -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h3 class="font-bold text-slate-900 mb-4">Location</h3>
          <div
            class="h-40 bg-slate-100 rounded-lg border border-slate-200 flex items-center justify-center text-slate-400">
            <MapPin class="w-6 h-6 mr-2" /> Map View
          </div>
        </div>

        <!-- Summary -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h3 class="font-bold text-slate-900 mb-2">{{ complaint.title }}</h3>
          <p class="text-sm text-slate-600">{{ complaint.location }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import jsPDF from 'jspdf'
import ComplaintPicker from '../../components/dashboard/ComplaintPicker.vue'
import {
  Download, MapPin, SearchX, Check, SkipForward
} from 'lucide-vue-next'

defineProps({ id: { type: String, default: null } })

const route = useRoute()
const router = useRouter()
const isLoading = ref(true)

const complaint = ref(null)
const timelineSteps = ref([])
const activityLog = ref([])

const STAGE_ORDER = ['Pending', 'Under Review', 'Assigned', 'In Progress', 'Resolved', 'Closed']
const STAGE_LABELS = { Pending: 'Submitted', 'Under Review': 'Under Review', Assigned: 'Assigned', 'In Progress': 'In Progress', Resolved: 'Resolved', Closed: 'Closed' }

const fetchTracking = async () => {
  if (!route.params.id) {
    complaint.value = null
    isLoading.value = false
    return
  }
  isLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const id = route.params.id
    const { data } = await axios.get(
      `http://127.0.0.1:5000/api/citizen/complaints/${id}/tracking`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    complaint.value = data.complaint

    const currentIndex = STAGE_ORDER.indexOf(complaint.value.status)
    timelineSteps.value = STAGE_ORDER.map((stage, index) => {
      const logEntry = data.activity_log.find(l => l.new_status === stage)
      let status
      if (index === currentIndex) {
        status = 'active'
      } else if (index < currentIndex) {
        status = logEntry ? 'completed' : 'skipped'
      } else {
        status = 'upcoming'
      }
      return {
        title: STAGE_LABELS[stage],
        status,
        date: logEntry?.changed_at
          ? new Date(logEntry.changed_at).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' })
          : null
      }
    })

    activityLog.value = data.activity_log.map((log, index) => ({
      id: index,
      date: log.changed_at ? new Date(log.changed_at).toLocaleString() : '—',
      status: log.new_status,
      officer: '—', // no officer/worker assignment feature yet on the backend
      remarks: log.remark || '—',
    }))
  } catch (err) {
    complaint.value = null
    if (err.response?.status === 401) router.push('/login')
    console.error('Tracking fetch error:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchTracking)
// Vue Router reuses this component instance when navigating between
// /citizen/track and /citizen/track/:id (same route, different param) —
// onMounted alone won't re-fire, so re-fetch whenever the id changes.
watch(() => route.params.id, fetchTracking)

const downloadReport = () => {
  if (!complaint.value) return
  const doc = new jsPDF()
  const marginX = 14
  const pageWidth = doc.internal.pageSize.getWidth()
  let y = 20

  doc.setFontSize(18)
  doc.setFont(undefined, 'bold')
  doc.text('CivicDesk — Complaint Tracking Report', marginX, y)
  y += 12

  doc.setFontSize(11)
  doc.setFont(undefined, 'normal')
  const fields = [
    ['Complaint ID', complaint.value.id],
    ['Title', complaint.value.title],
    ['Category', complaint.value.category],
    ['Department', complaint.value.department],
    ['Status', complaint.value.status],
    ['Priority', complaint.value.priority],
    ['Location', complaint.value.location],
  ]
  fields.forEach(([label, value]) => {
    doc.setFont(undefined, 'bold')
    doc.text(`${label}:`, marginX, y)
    doc.setFont(undefined, 'normal')
    const lines = doc.splitTextToSize(String(value ?? '—'), pageWidth - marginX * 2 - 40)
    doc.text(lines, marginX + 40, y)
    y += 6 * lines.length + 2
  })

  y += 6
  doc.setFont(undefined, 'bold')
  doc.text('Progress Timeline', marginX, y)
  y += 7
  doc.setFont(undefined, 'normal')
  timelineSteps.value.forEach(step => {
    doc.text(`${step.title}: ${step.status}${step.date ? ' (' + step.date + ')' : ''}`, marginX, y)
    y += 6
  })

  y += 6
  doc.setFont(undefined, 'bold')
  doc.text('Activity Log', marginX, y)
  y += 7
  doc.setFont(undefined, 'normal')
  if (activityLog.value.length) {
    activityLog.value.forEach(log => {
      if (y > 270) { doc.addPage(); y = 20 }
      doc.text(`${log.date} — ${log.status}: ${log.remarks}`, marginX, y)
      y += 6
    })
  } else {
    doc.text('No activity recorded yet.', marginX, y)
  }

  doc.save(`${complaint.value.id}-tracking-report.pdf`)
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>