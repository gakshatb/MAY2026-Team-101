<template>
  <div class="max-w-5xl mx-auto space-y-8">

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div v-for="card in summaryCards" :key="card.title"
        class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4 transition-transform hover:shadow-md">
        <div :class="['p-3 rounded-xl', card.iconBg]">
          <component :is="card.icon" :class="['w-6 h-6', card.iconColor]" />
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500">{{ card.title }}</p>
          <p class="text-2xl font-bold text-slate-900">{{ card.count }}</p>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-wrap gap-2">
      <button v-for="filter in filters" :key="filter.label" @click="activeFilter = filter.label"
        :class="['px-4 py-2 text-sm font-medium rounded-lg transition-colors', activeFilter === filter.label ? 'bg-[#2563EB] text-white' : 'text-slate-600 hover:bg-slate-50']">
        {{ filter.label }}
      </button>
    </div>

    <!-- Activity List -->
    <div v-if="filteredActivity.length > 0" class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
      <div class="relative pl-10 py-6 pr-5">
        <div class="absolute left-[35px] top-6 bottom-6 w-px bg-slate-100"></div>
        <div v-for="(event, idx) in filteredActivity" :key="event.id" class="relative pb-7 last:pb-0">
          <div
            :class="`absolute -left-10 top-0 w-8 h-8 rounded-full flex items-center justify-center ring-4 ring-white ${event.iconBg} ${event.iconColor}`">
            <component :is="event.icon" class="w-4 h-4" />
          </div>
          <p class="text-sm font-bold text-slate-900">{{ event.description }}</p>
          <p class="text-xs text-slate-500 font-medium mt-1">
            {{ event.date }}<span v-if="event.time"> • {{ event.time }}</span>
          </p>
          <button v-if="event.complaintId" @click="goToComplaint(event.complaintId)"
            class="text-xs font-bold text-[#2563EB] hover:underline mt-1.5 inline-flex items-center gap-1">
            {{ event.complaintId }} <ChevronRight class="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-20 bg-white rounded-[14px] border border-slate-100">
      <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
        <Activity class="w-8 h-8 text-slate-300" />
      </div>
      <h3 class="text-lg font-bold text-slate-900">No Activity Yet</h3>
      <p class="text-slate-500 mt-2">Your account activity — logins, complaints, profile changes — will show up here.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  Activity, ClipboardList, Star, User, UserCog, UserPlus,
  LogIn, LogOut, KeyRound, Camera, Mail, Clock, ChevronRight
} from 'lucide-vue-next'

const router = useRouter()
const isLoading = ref(true)
const activeFilter = ref('All')

// Same mapping used on Dashboard.vue — kept in sync with the backend's
// ACTIVITY_TYPES set in api_auth_utils.py.
const ACTIVITY_META = {
  register:                 { icon: UserPlus, bg: 'bg-blue-100',   color: 'text-blue-600',  group: 'Account' },
  login:                    { icon: LogIn,    bg: 'bg-green-100',  color: 'text-green-600', group: 'Account' },
  logout:                   { icon: LogOut,   bg: 'bg-slate-100',  color: 'text-slate-500', group: 'Account' },
  password_changed:         { icon: KeyRound, bg: 'bg-amber-100',  color: 'text-amber-600', group: 'Account' },
  password_reset_requested: { icon: Mail,     bg: 'bg-amber-100',  color: 'text-amber-600', group: 'Account' },
  password_reset_completed: { icon: KeyRound, bg: 'bg-green-100',  color: 'text-green-600', group: 'Account' },
  profile_updated:          { icon: UserCog,  bg: 'bg-purple-100', color: 'text-purple-600',group: 'Profile' },
  profile_photo_updated:    { icon: Camera,   bg: 'bg-purple-100', color: 'text-purple-600',group: 'Profile' },
  profile_photo_removed:    { icon: Camera,   bg: 'bg-slate-100',  color: 'text-slate-500', group: 'Profile' },
  complaint_submitted:      { icon: ClipboardList, bg: 'bg-blue-100', color: 'text-blue-600', group: 'Complaints' },
  feedback_submitted:       { icon: Star,     bg: 'bg-amber-100',  color: 'text-amber-600', group: 'Complaints' },
  default:                  { icon: Clock,    bg: 'bg-slate-100',  color: 'text-slate-500', group: 'Account' },
}

const filters = [
  { label: 'All' },
  { label: 'Complaints' },
  { label: 'Profile' },
  { label: 'Account' },
]

const summaryCards = ref([
  { title: 'All Activity', count: 0, icon: Activity,      iconBg: 'bg-blue-50',   iconColor: 'text-[#2563EB]' },
  { title: 'Complaints',   count: 0, icon: ClipboardList, iconBg: 'bg-green-50',  iconColor: 'text-[#22C55E]' },
  { title: 'Profile',      count: 0, icon: UserCog,       iconBg: 'bg-purple-50', iconColor: 'text-purple-500' },
  { title: 'Account',      count: 0, icon: KeyRound,      iconBg: 'bg-amber-50',  iconColor: 'text-amber-500' },
])

const allActivity = ref([])

// The backend doesn't support server-side group filtering (only a single
// ?type=), so — same approach as Notifications.vue — filtering happens
// client-side across the fetched batch.
const filteredActivity = computed(() => {
  if (activeFilter.value === 'All') return allActivity.value
  return allActivity.value.filter(a => a.group === activeFilter.value)
})

const fetchActivity = async () => {
  isLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://127.0.0.1:5000/api/citizen/activity?limit=100', {
      headers: { Authorization: `Bearer ${token}` }
    })

    allActivity.value = (data.activity || []).map(a => {
      const meta = ACTIVITY_META[a.type] || ACTIVITY_META.default
      const dt = a.created_at ? new Date(a.created_at) : null
      return {
        id: a.id,
        description: a.description,
        complaintId: a.complaint_id,
        date: dt ? dt.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : '',
        time: dt ? dt.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) : '',
        icon: meta.icon,
        iconBg: meta.bg,
        iconColor: meta.color,
        group: meta.group,
      }
    })

    summaryCards.value[0].count = allActivity.value.length
    summaryCards.value[1].count = allActivity.value.filter(a => a.group === 'Complaints').length
    summaryCards.value[2].count = allActivity.value.filter(a => a.group === 'Profile').length
    summaryCards.value[3].count = allActivity.value.filter(a => a.group === 'Account').length
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
    console.error('Activity fetch error:', err)
  } finally {
    isLoading.value = false
  }
}

const goToComplaint = (complaintId) => {
  const rawId = parseInt(complaintId.replace('CMP-', ''), 10)
  router.push(`/citizen/complaintdetails/${rawId}`)
}

onMounted(fetchActivity)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>
