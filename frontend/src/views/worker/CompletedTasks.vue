<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1600px] mx-auto space-y-6 animate-fade-in">

          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Completed Tasks</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Completed Tasks</h1>
              <p class="text-slate-500 mt-1">Review completed work and citizen feedback.</p>
            </div>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-blue-50 text-[#2563EB]"><CheckCircle class="w-4 h-4" /></div>
              </div>
              <p class="text-2xl font-extrabold text-slate-900">{{ tasks.length }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Total Completed</p>
            </div>
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-amber-50 text-amber-500"><Clock class="w-4 h-4" /></div>
              </div>
              <p class="text-2xl font-extrabold text-slate-900">{{ avgTimeTaken }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Avg Completion Time</p>
            </div>
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-yellow-50 text-yellow-500"><Star class="w-4 h-4" /></div>
              </div>
              <p class="text-2xl font-extrabold text-slate-900">{{ avgRating }}</p>
              <p class="text-xs font-semibold text-slate-500 mt-0.5">Avg Citizen Rating</p>
            </div>
          </div>

          <!-- Toolbar -->
          <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 justify-between items-center">
            <div class="relative w-full lg:w-72 shrink-0">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                v-model="filters.search"
                type="text"
                placeholder="Search ID, title, or area..."
                class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none transition-all"
              />
            </div>
            <select v-model="filters.sort" class="w-full lg:w-48 p-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none">
              <option value="Newest">Newest First</option>
              <option value="Rating">Highest Rated</option>
            </select>
          </div>

          <div v-if="loading" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-10 text-center text-slate-500">Loading completed tasks…</div>
          <div v-else-if="loadError" class="bg-white rounded-2xl shadow-sm border border-red-100 p-10 text-center text-red-600">{{ loadError }}</div>
          <div v-else-if="filteredTasks.length === 0" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-10 text-center text-slate-500">No completed tasks found.</div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            <div v-for="task in filteredTasks" :key="task.id" class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-shadow">
              <div class="p-5">
                <div class="flex items-center justify-between mb-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-600 font-mono uppercase">{{ task.id }}</span>
                  <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${task.status === 'Closed' ? 'bg-slate-200 text-slate-700' : 'bg-green-100 text-green-700'}`">{{ task.status }}</span>
                </div>
                <h3 class="font-bold text-slate-900 mb-1">{{ task.title }}</h3>
                <p class="text-xs text-slate-500 flex items-center gap-1 mb-3"><MapPin class="w-3.5 h-3.5 text-slate-400" /> {{ task.area }}</p>

                <div class="flex items-center justify-between text-xs text-slate-500 mb-3">
                  <span>{{ task.category }}</span>
                  <span>{{ formatDate(task.updated_at) }}</span>
                </div>

                <div class="flex items-center justify-between pt-3 border-t border-slate-100">
                  <div v-if="task.rating" class="flex items-center gap-0.5">
                    <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= task.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                  </div>
                  <span v-else class="text-xs text-slate-400">Feedback is yet to submit</span>
                  <router-link :to="`/worker/task/${task.raw_id}`" class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-100 transition-colors">Details</router-link>
                </div>

                <p v-if="task.rating && task.feedback_comment" class="text-xs text-slate-600 italic mt-2 line-clamp-2">"{{ task.feedback_comment }}"</p>
                <p v-else-if="task.rating" class="text-xs text-slate-400 italic mt-2">No written comments.</p>
              </div>
            </div>
          </div>

        </div>
      </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import { CheckCircle, Star, Clock, MapPin, Search } from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

const loading = ref(true)
const loadError = ref('')
const tasks = ref([])

const filters = reactive({ search: '', sort: 'Newest' })

const filteredTasks = computed(() => {
  let result = tasks.value
  if (filters.search) {
    const q = filters.search.toLowerCase()
    result = result.filter(t =>
      t.id.toLowerCase().includes(q) ||
      t.title.toLowerCase().includes(q) ||
      (t.area || '').toLowerCase().includes(q)
    )
  }
  result = [...result]
  if (filters.sort === 'Rating') {
    result.sort((a, b) => (b.rating || 0) - (a.rating || 0))
  } else {
    result.sort((a, b) => new Date(b.updated_at || 0) - new Date(a.updated_at || 0))
  }
  return result
})

const avgRating = computed(() => {
  const rated = tasks.value.filter(t => t.rating)
  if (!rated.length) return '—'
  return (rated.reduce((sum, t) => sum + t.rating, 0) / rated.length).toFixed(1)
})

const avgTimeTaken = computed(() => {
  const withDuration = tasks.value.filter(t => t.created_at && t.updated_at)
  if (!withDuration.length) return '—'
  const totalHours = withDuration.reduce((sum, t) => {
    return sum + (new Date(t.updated_at) - new Date(t.created_at)) / 3600000
  }, 0)
  return `${(totalHours / withDuration.length).toFixed(1)}h`
})

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function loadCompletedTasks() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/worker/tasks`, {
      headers: authHeaders(),
      params: { status: 'completed' }
    })
    tasks.value = data.tasks || []
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load completed tasks.'
  } finally {
    loading.value = false
  }
}

onMounted(loadCompletedTasks)
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

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>