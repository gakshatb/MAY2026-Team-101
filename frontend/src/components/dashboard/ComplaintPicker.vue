<!--
  ComplaintPicker.vue

  Shown by ComplaintDetails.vue / ComplaintTracking.vue / Feedback.vue whenever
  those pages are opened without a specific complaint id in the URL (e.g. via
  the sidebar links, which no longer carry a hardcoded id). Fetches the
  citizen's own complaints, optionally filters them (status / feedback
  eligibility), and lets them pick one — emitting `select` with the chosen
  complaint's raw numeric id so the parent page can load its full data.
-->
<template>
  <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
    <div class="px-6 py-5 border-b border-slate-100">
      <h2 class="text-lg font-bold text-slate-900">{{ title }}</h2>
      <p v-if="subtitle" class="text-sm text-slate-500 mt-0.5">{{ subtitle }}</p>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="py-16 text-center text-slate-400">
      Loading your complaints...
    </div>

    <!-- Error -->
    <div v-else-if="hasError" class="py-16 text-center">
      <p class="text-slate-500 font-medium">Something went wrong loading your complaints.</p>
      <button @click="fetchComplaints" class="mt-4 px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm font-medium hover:bg-[#1E40AF] transition-colors">
        Try Again
      </button>
    </div>

    <!-- Empty -->
    <div v-else-if="filteredComplaints.length === 0" class="p-16 text-center">
      <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <Inbox class="w-8 h-8 text-slate-400" />
      </div>
      <h3 class="text-lg font-bold text-slate-900">{{ emptyMessage }}</h3>
      <button @click="router.push('/citizen/submit')" class="mt-6 px-6 py-2.5 bg-[#2563EB] text-white rounded-lg text-sm font-medium hover:bg-[#1E40AF] transition-colors">
        Submit a Complaint
      </button>
    </div>

    <!-- List -->
    <template v-else>
      <!-- Desktop Table -->
      <div class="hidden md:block overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-600">
          <thead class="bg-slate-50 text-slate-700 font-bold uppercase text-[11px] tracking-wider">
            <tr>
              <th class="px-6 py-4">Complaint ID</th>
              <th class="px-6 py-4">Title</th>
              <th class="px-6 py-4">Category</th>
              <th class="px-6 py-4">Status</th>
              <th class="px-6 py-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="c in filteredComplaints" :key="c.id" class="hover:bg-slate-50 transition-colors">
              <td class="px-6 py-4 font-medium text-slate-900">{{ c.id }}</td>
              <td class="px-6 py-4 font-semibold text-slate-900">{{ c.title }}</td>
              <td class="px-6 py-4 text-slate-500">{{ c.category }}</td>
              <td class="px-6 py-4">
                <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase', statusColors(c.status)]">{{ c.status }}</span>
              </td>
              <td class="px-6 py-4 text-right">
                <button @click="$emit('select', c.rawId)" class="text-[#2563EB] font-medium hover:underline text-sm">{{ actionLabel }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Mobile Cards -->
      <div class="md:hidden divide-y divide-slate-100">
        <div v-for="c in filteredComplaints" :key="c.id" class="p-4 space-y-3">
          <div class="flex justify-between items-start">
            <p class="font-bold text-slate-900">{{ c.title }}</p>
            <span :class="['px-2 py-0.5 rounded text-[10px] font-bold', statusColors(c.status)]">{{ c.status }}</span>
          </div>
          <p class="text-xs text-slate-500">ID: {{ c.id }} | {{ c.category }}</p>
          <button @click="$emit('select', c.rawId)" class="w-full py-2 bg-slate-50 rounded-lg text-sm font-medium text-slate-700">{{ actionLabel }}</button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Inbox } from 'lucide-vue-next'

const props = defineProps({
  title:        { type: String, default: 'Select a Complaint' },
  subtitle:     { type: String, default: '' },
  actionLabel:  { type: String, default: 'Select' },
  emptyMessage: { type: String, default: 'No complaints available.' },
  // Only show complaints in this status (e.g. 'Resolved' for the Feedback picker).
  statusFilter: { type: String, default: null },
  // Hide complaints that already have feedback submitted (Feedback picker only).
  excludeWithFeedback: { type: Boolean, default: false },
})

defineEmits(['select'])

const router    = useRouter()
const isLoading = ref(true)
const hasError  = ref(false)
const complaints = ref([])

const filteredComplaints = computed(() => complaints.value.filter(c => {
  if (props.statusFilter && c.status !== props.statusFilter) return false
  if (props.excludeWithFeedback && c.has_feedback) return false
  return true
}))

const fetchComplaints = async () => {
  isLoading.value = true
  hasError.value  = false
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://127.0.0.1:5000/api/citizen/complaints', {
      headers: { Authorization: `Bearer ${token}` }
    })
    complaints.value = data.complaints.map(c => ({
      id: c.id, rawId: c.raw_id,
      title: c.title, category: c.category,
      status: c.status, has_feedback: !!c.has_feedback,
    }))
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
    hasError.value = true
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchComplaints)

const statusColors = (status) => {
  switch (status) {
    case 'Resolved':    return 'bg-green-50 text-green-700'
    case 'In Progress': return 'bg-blue-50 text-blue-700'
    case 'Pending':     return 'bg-amber-50 text-amber-700'
    default:            return 'bg-slate-100 text-slate-700'
  }
}
</script>