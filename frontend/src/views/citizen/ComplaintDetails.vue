<template>
  <!-- Loading state -->
  <div v-if="isLoading" class="max-w-7xl mx-auto py-24 text-center text-slate-400">
    Loading complaint details...
  </div>

  <!-- No complaint selected: let the user pick one instead of a dead end -->
  <div v-else-if="!route.params.id" class="max-w-5xl mx-auto">
    <ComplaintPicker title="Select a Complaint" subtitle="Choose one of your complaints to view its full details."
      action-label="View Details" empty-message="No complaints available to view."
      @select="(id) => router.push(`/citizen/complaintdetails/${id}`)" />
  </div>

  <!-- Error / not found state -->
  <div v-else-if="!complaint" class="max-w-7xl mx-auto py-24 text-center">
    <p class="text-slate-500 font-medium">We couldn't load this complaint.</p>
    <p class="text-sm text-slate-400 mt-1">It may not exist, or you may not have access to it.</p>
    <button @click="router.push('/citizen/complaints')"
      class="mt-4 px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm font-medium hover:bg-[#1E40AF] transition-colors">
      Back to My Complaints
    </button>
  </div>

  <div v-else class="max-w-7xl mx-auto space-y-6">

    <!-- Header Actions -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Complaint #{{ complaint.id }}</h1>
        <p class="text-sm text-slate-500 mt-1">{{ complaint.title }}</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="printPage"
          class="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-2">
          <Printer class="w-4 h-4" /> Print
        </button>
        <button @click="downloadPdf"
          class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm font-medium hover:bg-[#1E40AF] transition-colors flex items-center gap-2">
          <Download class="w-4 h-4" /> Download PDF
        </button>
      </div>
    </div>

    <!-- Main Layout Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left Column (Main Content - 2/3 width) -->
      <div class="lg:col-span-2 space-y-6">

        <!-- Complaint Info Card -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h2 class="text-lg font-bold text-slate-900 mb-4">Description</h2>
          <p class="text-slate-600 leading-relaxed">{{ complaint.description }}</p>
        </div>

        <!-- Location Card -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h2 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <MapPin class="w-5 h-5 text-slate-400" /> Location Details
          </h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-6">
            <div v-for="(val, label) in locationDetails" :key="label">
              <p class="text-xs text-slate-500 uppercase font-medium">{{ label }}</p>
              <p class="text-sm font-bold text-slate-900">{{ val }}</p>
            </div>
          </div>
          <!-- Maps Placeholder -->
          <div
            class="w-full h-48 bg-slate-100 rounded-lg border border-slate-200 flex items-center justify-center text-slate-400">
            <span class="flex items-center gap-2">
              <MapPin class="w-4 h-4" /> Google Maps Placeholder
            </span>
          </div>
        </div>

        <!-- Evidence Card -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h2 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Camera class="w-5 h-5 text-slate-400" /> Uploaded Evidence
          </h2>
          <div v-if="images.length" class="grid grid-cols-2 gap-4">
            <div v-for="(img, i) in images" :key="i"
              class="relative group cursor-pointer overflow-hidden rounded-lg h-32 border border-slate-200">
              <img :src="`http://127.0.0.1:5000${img}`" alt="Evidence"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
              <div
                class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                <Maximize2 class="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
          <p v-else class="text-sm text-slate-400">No evidence images were attached to this complaint.</p>
        </div>

      </div>

      <!-- Right Column (Status & Assigned Info - 1/3 width) -->
      <div class="lg:col-span-1 space-y-6">

        <!-- Status Card -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 text-center">
          <p class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-2">Current Status</p>
          <span class="inline-block px-4 py-2 rounded-full text-sm font-bold bg-blue-50 text-[#2563EB] uppercase">{{
            complaint.status }}</span>
        </div>

        <!-- Assigned Personnel Card -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h3 class="text-sm font-bold text-slate-900 mb-4">Assigned Personnel</h3>
          <div class="space-y-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center">
                <User class="w-5 h-5 text-slate-500" />
              </div>
              <div>
                <p class="text-sm font-bold text-slate-900">{{ complaint.officer?.name || 'Not yet assigned' }}</p>
                <p class="text-xs text-slate-500">Civic Officer</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center">
                <HardHat class="w-5 h-5 text-slate-500" />
              </div>
              <div>
                <p class="text-sm font-bold text-slate-900">{{ complaint.worker?.name || 'Not yet assigned' }}</p>
                <p class="text-xs text-slate-500">Field Worker</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Timeline Preview -->
        <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100">
          <h3 class="text-sm font-bold text-slate-900 mb-6">Timeline</h3>
          <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
            <div v-for="step in timeline" :key="step.title" class="relative">
              <div
                :class="['absolute -left-[21px] w-2.5 h-2.5 rounded-full mt-1', step.completed ? 'bg-[#22C55E]' : 'bg-slate-300']">
              </div>
              <p :class="['text-sm font-medium', step.completed ? 'text-slate-900' : 'text-slate-400']">{{ step.title }}
              </p>
              <p class="text-[10px] text-slate-400">{{ step.date }}</p>
            </div>
          </div>
          <button @click="router.push(`/citizen/track/${rawId}`)"
            class="w-full mt-6 text-sm font-medium text-[#2563EB] hover:underline">View Complete Timeline</button>
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
import ComplaintPicker from '@/components/dashboard/ComplaintPicker.vue'
import {
  Printer, Download, MapPin, Camera, Maximize2,
  User, HardHat, ShieldCheck
} from 'lucide-vue-next'

defineProps({ id: { type: String, default: null } })

const route = useRoute()
const router = useRouter()
const isLoading = ref(true)

const complaint = ref(null)
const locationDetails = ref({})
const images = ref([])
const timeline = ref([])
const rawId = ref(null)

const STAGE_ORDER = ['Pending', 'Under Review', 'Assigned', 'In Progress', 'Resolved', 'Closed']
const STAGE_LABELS = { Pending: 'Submitted', 'Under Review': 'Under Review', Assigned: 'Assigned', 'In Progress': 'In Progress', Resolved: 'Resolved', Closed: 'Closed' }

const fetchComplaintDetails = async () => {
  if (!route.params.id) {
    complaint.value = null
    isLoading.value = false
    return
  }
  isLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const id = route.params.id

    // The plain /complaints/:id endpoint has full complaint fields but no
    // activity history — that lives on the separate /tracking endpoint, so
    // fetch both for this page's details + timeline preview.
    const [{ data }, { data: trackingData }] = await Promise.all([
      axios.get(`http://127.0.0.1:5000/api/citizen/complaints/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      }),
      axios.get(`http://127.0.0.1:5000/api/citizen/complaints/${id}/tracking`, {
        headers: { Authorization: `Bearer ${token}` }
      })
    ])
    const c = data.complaint
    rawId.value = c.raw_id
    complaint.value = {
      id: c.id,
      title: c.title,
      category: c.category,
      status: c.status,
      priority: c.priority,
      submittedAt: c.created_at ? new Date(c.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: '2-digit' }) : '',
      description: c.description,
      has_feedback: c.has_feedback,
      officer: c.officer,
      worker: c.worker,
    }
    images.value = c.images || []

    locationDetails.value = Object.fromEntries(
      Object.entries({
        City: c.city, Ward: c.ward, Area: c.area, Street: c.street, Landmark: c.landmark
      }).filter(([, val]) => !!val)
    )

    const currentIndex = STAGE_ORDER.indexOf(c.status)
    timeline.value = STAGE_ORDER.map((stage, index) => {
      const logEntry = trackingData.activity_log.find(l => l.new_status === stage)
      return {
        title: STAGE_LABELS[stage],
        completed: index <= currentIndex,
        date: logEntry?.changed_at
          ? new Date(logEntry.changed_at).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' })
          : ''
      }
    })
  } catch (err) {
    complaint.value = null
    if (err.response?.status === 401) router.push('/login')
    console.error('ComplaintDetails fetch error:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchComplaintDetails)
// Vue Router reuses this component instance when navigating between
// /citizen/complaintdetails and /citizen/complaintdetails/:id (same route,
// different param) — onMounted alone won't re-fire, so re-fetch on id change.
watch(() => route.params.id, fetchComplaintDetails)

const printPage = () => window.print()

const downloadPdf = () => {
  if (!complaint.value) return
  const doc = new jsPDF()
  const marginX = 14
  const pageWidth = doc.internal.pageSize.getWidth()
  let y = 20

  doc.setFontSize(18)
  doc.setFont(undefined, 'bold')
  doc.text('CivicDesk — Complaint Report', marginX, y)
  y += 12

  doc.setFontSize(11)
  doc.setFont(undefined, 'normal')
  const fields = [
    ['Complaint ID', complaint.value.id],
    ['Title', complaint.value.title],
    ['Category', complaint.value.category],
    ['Status', complaint.value.status],
    ['Priority', complaint.value.priority],
    ['Submitted', complaint.value.submittedAt],
  ]
  fields.forEach(([label, value]) => {
    doc.setFont(undefined, 'bold')
    doc.text(`${label}:`, marginX, y)
    doc.setFont(undefined, 'normal')
    doc.text(String(value ?? '—'), marginX + 40, y)
    y += 8
  })

  y += 4
  doc.setFont(undefined, 'bold')
  doc.text('Description', marginX, y)
  y += 7
  doc.setFont(undefined, 'normal')
  const descLines = doc.splitTextToSize(complaint.value.description || 'No description provided.', pageWidth - marginX * 2)
  doc.text(descLines, marginX, y)
  y += descLines.length * 6 + 8

  if (Object.keys(locationDetails.value).length) {
    doc.setFont(undefined, 'bold')
    doc.text('Location', marginX, y)
    y += 7
    doc.setFont(undefined, 'normal')
    Object.entries(locationDetails.value).forEach(([label, value]) => {
      doc.text(`${label}: ${value}`, marginX, y)
      y += 6
    })
    y += 6
  }

  if (timeline.value.length) {
    doc.setFont(undefined, 'bold')
    doc.text('Status Timeline', marginX, y)
    y += 7
    doc.setFont(undefined, 'normal')
    timeline.value.forEach(step => {
      const status = step.completed ? 'Completed' : 'Pending'
      doc.text(`${step.title}: ${status}${step.date ? ' (' + step.date + ')' : ''}`, marginX, y)
      y += 6
    })
  }

  doc.save(`${complaint.value.id}-report.pdf`)
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>