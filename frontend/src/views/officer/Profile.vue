<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1400px] mx-auto space-y-6">
          
          <!-- Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB]">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Profile</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Officer Profile</h1>
              <p class="text-slate-500 mt-1">Manage your professional details and monitor performance.</p>
            </div>
          </div>

          <div v-if="loadError" class="bg-red-50 border border-red-100 text-red-600 text-sm rounded-[14px] p-4">
            {{ loadError }}
          </div>

          <!-- Overview Grid -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <!-- Left: Profile Info -->
            <div class="xl:col-span-4 space-y-6">
              <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 flex flex-col items-center text-center">
                <div class="relative mb-4">
                  <img :src="profile.profilePhoto ? `http://127.0.0.1:5000${profile.profilePhoto}` : defaultAvatar"
                    class="w-24 h-24 rounded-full object-cover border-4 border-slate-50 shadow-sm" />
                  <div class="absolute bottom-1 right-1 w-5 h-5 bg-green-500 border-2 border-white rounded-full"></div>
                </div>
                <h2 class="text-xl font-bold text-slate-900">{{ profile.fullName || 'Loading…' }}</h2>
                <p class="text-sm text-slate-500 mb-4">
                  ID: {{ profile.empId }}<span v-if="profile.department"> | {{ profile.department }}</span>
                </p>
                <div class="flex gap-2">
                  <button @click="openEditModal" class="px-4 py-2 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors">Edit Profile</button>
                </div>
              </div>

              <!-- Performance Stats -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><TrendingUp class="w-4 h-4 text-[#2563EB]" /> Performance Stats</h3>
                <div class="grid grid-cols-2 gap-3">
                  <div class="p-3 bg-slate-50 rounded-lg">
                    <p class="text-[10px] uppercase font-bold text-slate-500">Resolved</p>
                    <p class="text-lg font-bold text-slate-900">{{ profile.resolvedCount ?? '—' }}</p>
                  </div>
                  <div class="p-3 bg-slate-50 rounded-lg">
                    <p class="text-[10px] uppercase font-bold text-slate-500">Rating</p>
                    <p class="text-lg font-bold text-slate-900">
                      {{ profile.avgRating ?? '—' }} <span v-if="profile.avgRating" class="text-xs text-amber-500">★</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right: Detailed Info -->
            <div class="xl:col-span-8 space-y-6">
              
              <!-- Personal/Professional Info -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 mb-6 flex items-center gap-2"><Briefcase class="w-4 h-4 text-slate-400" /> Professional Details</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div v-for="(val, label) in profInfo" :key="label">
                    <p class="text-xs font-medium text-slate-500 uppercase">{{ label }}</p>
                    <p class="text-sm font-bold text-slate-900 mt-1">{{ val || '—' }}</p>
                  </div>
                </div>
              </div>

              <!-- Recent Activities -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Activity class="w-4 h-4 text-slate-400" /> Recent Activities</h3>
                <div v-if="activities.length" class="space-y-6 relative pl-4 border-l border-slate-100">
                  <div v-for="act in activities" :key="act.id" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#2563EB] rounded-full border-2 border-white"></div>
                    <p class="text-sm font-bold text-slate-900">{{ act.description }}</p>
                    <p class="text-xs text-slate-500">{{ act.date }}<span v-if="act.complaintId"> • {{ act.complaintId }}</span></p>
                  </div>
                </div>
                <p v-else class="text-sm text-slate-400">No recent activity yet.</p>
              </div>

            </div>
          </div>
        </div>
      </main>
    <!-- Modals (Teleported) -->
    <Teleport to="body">
      <!-- Edit Profile Modal -->
      <div v-if="activeModal === 'edit'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-lg shadow-2xl p-6">
          <h3 class="font-bold text-lg mb-4">Edit Profile</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Full Name</label>
              <input v-model="editForm.fullName" type="text" class="w-full p-3 border rounded-lg text-sm" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Mobile</label>
              <input v-model="editForm.mobile" type="text" maxlength="10" class="w-full p-3 border rounded-lg text-sm" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Gender</label>
              <select v-model="editForm.gender" class="w-full p-3 border rounded-lg text-sm">
                <option value="">Select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Profile Photo</label>
              <input type="file" accept="image/png,image/jpeg" @change="onPhotoSelected" class="w-full text-sm" />
            </div>
            <p v-if="editError" class="text-red-600 text-xs">{{ editError }}</p>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="activeModal = null" class="px-4 py-2 bg-slate-100 rounded-lg text-sm font-bold">Cancel</button>
            <button @click="saveProfile" :disabled="isSaving" class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm font-bold disabled:opacity-60">
              {{ isSaving ? 'Saving…' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import {
  TrendingUp, Briefcase, Activity
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
const defaultAvatar = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop'

const isSidebarOpen = ref(false)
const activeModal = ref(null)
const loadError = ref('')
const isSaving = ref(false)
const editError = ref('')

const profile = ref({})
const activities = ref([])
const editForm = reactive({ fullName: '', mobile: '', gender: '' })
const selectedPhoto = ref(null)

const profInfo = computed(() => ({
  'Email': profile.value.email,
  'Mobile': profile.value.mobile,
  'Designation': profile.value.designation,
  'Department': profile.value.department,
  'Gender': profile.value.gender,
  'Date of Birth': profile.value.dob,
  'Member Since': profile.value.memberSince,
  'Last Login': profile.value.lastLogin,
}))

const fetchProfile = async () => {
  try {
    const { data } = await axios.get(`${API_BASE}/profile`, authHeaders())
    profile.value = data.profile
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load profile.'
  }
}

const fetchActivity = async () => {
  try {
    const { data } = await axios.get(`${API_BASE}/activity`, { ...authHeaders(), params: { limit: 8 } })
    activities.value = data.activity.map(a => ({
      id: a.id,
      description: a.description,
      complaintId: a.complaintId,
      date: a.createdAt ? new Date(a.createdAt).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : ''
    }))
  } catch (err) {
    console.error(err)
  }
}

const openEditModal = () => {
  editForm.fullName = profile.value.fullName || ''
  editForm.mobile = profile.value.mobile || ''
  editForm.gender = profile.value.gender || ''
  editError.value = ''
  selectedPhoto.value = null
  activeModal.value = 'edit'
}

const onPhotoSelected = (e) => {
  selectedPhoto.value = e.target.files[0] || null
}

const saveProfile = async () => {
  isSaving.value = true
  editError.value = ''
  try {
    await axios.put(`${API_BASE}/profile`, {
      fullName: editForm.fullName,
      mobile: editForm.mobile,
      gender: editForm.gender,
    }, authHeaders())

    if (selectedPhoto.value) {
      const formData = new FormData()
      formData.append('photo', selectedPhoto.value)
      await axios.post(`${API_BASE}/profile/photo`, formData, {
        headers: { ...authHeaders().headers, 'Content-Type': 'multipart/form-data' }
      })
    }

    await fetchProfile()
    activeModal.value = null
  } catch (err) {
    editError.value = err.response?.data?.message || 'Failed to update profile.'
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  fetchProfile()
  fetchActivity()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
.animate-fade-in { animation: fadeIn 0.2s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>