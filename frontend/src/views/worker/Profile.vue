<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1400px] mx-auto space-y-6 animate-fade-in">

          <!-- Breadcrumb & Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Profile</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Worker Profile</h1>
              <p class="text-slate-500 mt-1">Manage your personal information and view your work performance.</p>
            </div>
          </div>

          <div v-if="loading" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-10 text-center text-slate-500">
            Loading profile…
          </div>
          <div v-else-if="loadError" class="bg-white rounded-[14px] shadow-sm border border-red-100 p-10 text-center text-red-600">
            {{ loadError }}
          </div>

          <!-- Main Two-Column Layout -->
          <div v-else class="grid grid-cols-1 xl:grid-cols-12 gap-6">

            <!-- LEFT COLUMN: Profile & Details (4 cols) -->
            <div class="xl:col-span-4 space-y-6">

              <!-- Profile Overview Card -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6 flex flex-col items-center text-center relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-24 bg-gradient-to-r from-[#1E40AF] to-[#2563EB]"></div>
                <div class="relative mt-8 mb-4">
                  <img :src="photoSrc" class="w-28 h-28 rounded-full object-cover border-4 border-white shadow-md bg-white" />
                </div>
                <h2 class="text-xl font-bold text-slate-900 flex items-center justify-center gap-2">
                  {{ profile.name }} <BadgeCheck class="w-5 h-5 text-[#2563EB]" title="Verified Worker" />
                </h2>
                <p class="text-sm font-bold text-[#2563EB] mt-1">{{ profile.designation || 'Field Worker' }} • {{ profile.department || 'Unassigned' }}</p>
                <p class="text-xs text-slate-500 font-mono mt-1">ID: {{ profile.empId }}</p>

                <div class="flex flex-wrap justify-center gap-3 mt-4 text-sm text-slate-600">
                  <span v-if="profile.city" class="flex items-center gap-1.5"><MapPin class="w-4 h-4 text-slate-400"/> {{ profile.city }}<span v-if="profile.state">, {{ profile.state }}</span></span>
                  <span v-if="profile.phone" class="flex items-center gap-1.5"><Phone class="w-4 h-4 text-slate-400"/> {{ profile.phone }}</span>
                </div>

                <div class="flex w-full gap-3 mt-6">
                  <button @click="openEditModal" class="flex-1 py-2.5 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm">Edit Profile</button>
                  <button @click="openPasswordModal" class="flex-1 py-2.5 bg-white border border-slate-200 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-50 transition-colors shadow-sm">Password</button>
                </div>
              </div>

              <!-- Professional Information -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Briefcase class="w-5 h-5 text-slate-400" /> Professional Info</h3>
                <div class="space-y-4">
                  <div v-for="(val, label) in professionalInfo" :key="label" class="flex justify-between items-center border-b border-slate-50 pb-3 last:border-0 last:pb-0">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">{{ label }}</span>
                    <span class="text-sm font-semibold text-slate-900 text-right">{{ val || '—' }}</span>
                  </div>
                </div>
              </div>

              <!-- Personal Information -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><User class="w-5 h-5 text-slate-400" /> Personal Info</h3>
                <div class="space-y-4">
                  <div v-for="(val, label) in personalInfo" :key="label" class="flex justify-between items-center border-b border-slate-50 pb-3 last:border-0 last:pb-0">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">{{ label }}</span>
                    <span class="text-sm font-semibold text-slate-900 text-right">{{ val || '—' }}</span>
                  </div>
                </div>
              </div>

            </div>

            <!-- RIGHT COLUMN: Performance & History (8 cols) -->
            <div class="xl:col-span-8 space-y-6">

              <!-- Quick Actions Top Bar -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <router-link to="/worker/tasks" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <ClipboardCheck class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Assigned Tasks</span>
                </router-link>
                <router-link to="/worker/completed" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <CheckCircle class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Completed</span>
                </router-link>
                <router-link to="/worker/notifications" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <Bell class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Notifications</span>
                </router-link>
                <router-link to="/worker/dashboard" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <Activity class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Dashboard</span>
                </router-link>
              </div>

              <!-- Performance Summary (KPIs) -->
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-center">
                  <div class="flex items-center gap-2 mb-2">
                    <CheckCircle class="w-4 h-4 text-green-500" />
                    <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wide">Completed Tasks</span>
                  </div>
                  <p class="text-2xl font-extrabold text-slate-900">{{ profile.completedCount ?? 0 }}</p>
                </div>
                <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-center">
                  <div class="flex items-center gap-2 mb-2">
                    <Clock class="w-4 h-4 text-blue-500" />
                    <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wide">Avg Completion</span>
                  </div>
                  <p class="text-2xl font-extrabold text-slate-900">{{ profile.avgCompletionHours != null ? profile.avgCompletionHours + 'h' : '—' }}</p>
                </div>
                <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-center">
                  <div class="flex items-center gap-2 mb-2">
                    <Star class="w-4 h-4 text-amber-500" />
                    <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wide">Citizen Rating</span>
                  </div>
                  <p class="text-2xl font-extrabold text-slate-900">{{ profile.avgRating != null ? profile.avgRating : '—' }}</p>
                </div>
              </div>

              <!-- Work History -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 bg-slate-50/50">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2"><ClipboardCheck class="w-5 h-5 text-slate-400" /> Recent Work History</h3>
                </div>
                <div v-if="workHistory.length === 0" class="p-8 text-center text-sm text-slate-500">No completed tasks yet.</div>
                <div v-else class="overflow-x-auto">
                  <table class="w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide border-b border-slate-100">
                      <tr>
                        <th class="px-5 py-4">Complaint ID</th>
                        <th class="px-5 py-4">Category</th>
                        <th class="px-5 py-4">Completed On</th>
                        <th class="px-5 py-4">Rating</th>
                        <th class="px-5 py-4 text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="work in workHistory" :key="work.id" class="hover:bg-slate-50 transition-colors">
                        <td class="px-5 py-3 font-mono font-bold text-slate-900">{{ work.id }}</td>
                        <td class="px-5 py-3 text-slate-600 font-medium">{{ work.category }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ work.date }}</td>
                        <td class="px-5 py-3">
                          <div v-if="work.rating" class="flex items-center gap-0.5">
                            <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= work.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                          </div>
                          <span v-else class="text-xs text-slate-400">No feedback yet</span>
                        </td>
                        <td class="px-5 py-3 text-right">
                          <router-link :to="`/worker/task/${work.raw_id}`" class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-100 transition-colors">Details</router-link>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Security -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Lock class="w-5 h-5 text-slate-400" /> Security Settings</h3>
                <div class="space-y-4">
                  <button @click="openPasswordModal" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between hover:bg-slate-100 transition-colors group">
                    <span class="text-sm font-medium text-slate-700 flex items-center gap-2"><Key class="w-4 h-4 text-slate-400 group-hover:text-slate-600"/> Change Password</span>
                    <ChevronRight class="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
                  </button>
                  <div v-if="profile.lastLogin" class="p-3 border border-slate-100 rounded-xl">
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Last Login</p>
                    <p class="text-sm text-slate-900 font-medium">{{ profile.lastLogin }}</p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>

    <!-- Edit Profile Modal -->
    <Teleport to="body">
      <div v-if="isEditModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <h3 class="font-bold text-lg text-slate-900">Edit Profile</h3>
            <button @click="isEditModalOpen = false" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
            <div v-if="editError" class="p-3 bg-red-50 border border-red-100 text-red-600 text-sm rounded-lg">{{ editError }}</div>

            <div class="flex items-center gap-4 mb-4">
              <img :src="photoSrc" class="w-16 h-16 rounded-full object-cover border border-slate-200" />
              <div class="flex flex-col gap-1">
                <label class="px-3 py-1.5 bg-slate-100 border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-200 transition-colors flex items-center gap-2 cursor-pointer w-fit">
                  <Upload class="w-3.5 h-3.5"/> {{ photoUploading ? 'Uploading…' : 'Upload New Photo' }}
                  <input type="file" accept="image/*" class="hidden" @change="handlePhotoUpload" :disabled="photoUploading" />
                </label>
                <button v-if="profile.profile_photo" @click="handlePhotoRemove" type="button" class="text-xs font-bold text-red-500 hover:text-red-600 w-fit">Remove photo</button>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Full Name</label>
                <input type="text" v-model="editForm.name" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Phone Number</label>
                <input type="text" v-model="editForm.phone" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Gender</label>
                <select v-model="editForm.gender" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none">
                  <option value="">—</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Date of Birth</label>
                <input type="date" v-model="editForm.dob" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Emergency Contact</label>
                <input type="text" v-model="editForm.emergencyContact" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">City</label>
                <input type="text" v-model="editForm.city" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">State</label>
                <input type="text" v-model="editForm.state" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Pincode</label>
                <input type="text" v-model="editForm.pincode" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div class="col-span-2">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Residential Address</label>
                <textarea rows="2" v-model="editForm.address" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none resize-none"></textarea>
              </div>
            </div>
          </div>
          <div class="p-5 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
            <button @click="isEditModalOpen = false" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-100 transition-colors text-sm">Cancel</button>
            <button @click="saveProfile" :disabled="savingProfile" class="px-4 py-2 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm text-sm disabled:opacity-60">{{ savingProfile ? 'Saving…' : 'Save Changes' }}</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Change Password Modal -->
    <Teleport to="body">
      <div v-if="isPasswordModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <h3 class="font-bold text-lg text-slate-900">Change Password</h3>
            <button @click="isPasswordModalOpen = false" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4">
            <div v-if="passwordError" class="p-3 bg-red-50 border border-red-100 text-red-600 text-sm rounded-lg">{{ passwordError }}</div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Current Password</label>
              <input type="password" v-model="passwordForm.current" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">New Password</label>
              <input type="password" v-model="passwordForm.next" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Confirm New Password</label>
              <input type="password" v-model="passwordForm.confirm" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
            </div>
          </div>
          <div class="p-5 border-t border-slate-100 bg-slate-50 flex flex-col gap-2">
            <button @click="submitPasswordChange" :disabled="changingPassword" class="w-full py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm text-sm disabled:opacity-60">{{ changingPassword ? 'Updating…' : 'Update Password' }}</button>
            <button @click="isPasswordModalOpen = false" class="w-full py-2.5 bg-white border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-100 transition-colors text-sm">Cancel</button>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import {
  BadgeCheck, MapPin, Phone, Briefcase, User, ClipboardCheck, CheckCircle, Clock,
  Bell, Activity, Star, Lock, Key, ChevronRight, X, Upload
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

// --- State ---
const loading = ref(true)
const loadError = ref('')
const profile = reactive({})
const workHistory = ref([])

const isEditModalOpen = ref(false)
const isPasswordModalOpen = ref(false)
const savingProfile = ref(false)
const editError = ref('')
const photoUploading = ref(false)

const editForm = reactive({
  name: '', phone: '', gender: '', dob: '', emergencyContact: '',
  city: '', state: '', pincode: '', address: ''
})

const passwordForm = reactive({ current: '', next: '', confirm: '' })
const passwordError = ref('')
const changingPassword = ref(false)

const photoSrc = computed(() =>
  profile.profile_photo
    ? (profile.profile_photo.startsWith('http') ? profile.profile_photo : `${API_BASE}/uploads/${profile.profile_photo}`)
    : `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.name || 'Worker')}&background=2563EB&color=fff`
)

const professionalInfo = computed(() => ({
  'Employee ID': profile.empId,
  'Department': profile.department,
  'Designation': profile.designation,
  'Member Since': profile.memberSince,
}))

const personalInfo = computed(() => ({
  'Full Name': profile.name,
  'Date of Birth': profile.dob,
  'Gender': profile.gender,
  'Email Address': profile.email,
  'Nationality': profile.nationality,
  'Emergency Contact': profile.emergencyContact,
}))

// Keeps the persistent DashboardLayout (sidebar/navbar) in sync — it reads
// its `user` from localStorage once and only refreshes on this event.
function syncStoredUser(patch) {
  let stored = {}
  try {
    stored = JSON.parse(localStorage.getItem('user') || '{}') || {}
  } catch (err) {
    stored = {}
  }
  localStorage.setItem('user', JSON.stringify({ ...stored, ...patch }))
  window.dispatchEvent(new Event('user-updated'))
}

// --- Data loading ---
async function loadProfile() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/worker/profile`, { headers: authHeaders() })
    Object.assign(profile, data.profile)
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load profile.'
  } finally {
    loading.value = false
  }
}

async function loadWorkHistory() {
  try {
    const { data } = await axios.get(`${API_BASE}/worker/tasks`, {
      headers: authHeaders(),
      params: { status: 'completed' }
    })
    workHistory.value = (data.tasks || []).map(t => ({
      id: t.id,
      raw_id: t.raw_id,
      category: t.category,
      rating: t.rating,
      date: t.updated_at ? new Date(t.updated_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
    }))
  } catch (err) {
    // Non-fatal — the profile summary cards still work without this table.
  }
}

onMounted(() => {
  loadProfile()
  loadWorkHistory()
})

// --- Edit profile ---
function openEditModal() {
  editForm.name = profile.name || ''
  editForm.phone = profile.phone || ''
  editForm.gender = profile.gender || ''
  editForm.dob = profile.dob || ''
  editForm.emergencyContact = profile.emergencyContact || ''
  editForm.city = profile.city || ''
  editForm.state = profile.state || ''
  editForm.pincode = profile.pincode || ''
  editForm.address = profile.address || ''
  editError.value = ''
  isEditModalOpen.value = true
}

async function saveProfile() {
  editError.value = ''
  if (!editForm.name.trim()) {
    editError.value = 'Name cannot be empty.'
    return
  }
  savingProfile.value = true
  try {
    const { data } = await axios.put(`${API_BASE}/worker/profile`, editForm, { headers: authHeaders() })
    Object.assign(profile, data.profile)
    syncStoredUser({ name: data.profile.name })
    isEditModalOpen.value = false
  } catch (err) {
    editError.value = err.response?.data?.message || 'Failed to update profile.'
  } finally {
    savingProfile.value = false
  }
}

async function handlePhotoUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return
  photoUploading.value = true
  try {
    const formData = new FormData()
    formData.append('photo', file)
    const { data } = await axios.post(`${API_BASE}/worker/profile/photo`, formData, { headers: authHeaders() })
    profile.profile_photo = data.profilePhoto
    syncStoredUser({ profilePhoto: data.profilePhoto })
  } catch (err) {
    editError.value = err.response?.data?.message || 'Failed to upload photo.'
  } finally {
    photoUploading.value = false
    event.target.value = ''
  }
}

async function handlePhotoRemove() {
  try {
    await axios.delete(`${API_BASE}/worker/profile/photo`, { headers: authHeaders() })
    profile.profile_photo = null
    syncStoredUser({ profilePhoto: null })
  } catch (err) {
    editError.value = err.response?.data?.message || 'Failed to remove photo.'
  }
}

// --- Change password ---
function openPasswordModal() {
  passwordForm.current = ''
  passwordForm.next = ''
  passwordForm.confirm = ''
  passwordError.value = ''
  isPasswordModalOpen.value = true
}

async function submitPasswordChange() {
  passwordError.value = ''
  if (!passwordForm.current || !passwordForm.next) {
    passwordError.value = 'Both current and new password are required.'
    return
  }
  if (passwordForm.next.length < 8) {
    passwordError.value = 'New password must be at least 8 characters.'
    return
  }
  if (passwordForm.next !== passwordForm.confirm) {
    passwordError.value = 'New password and confirmation do not match.'
    return
  }
  changingPassword.value = true
  try {
    await axios.post(`${API_BASE}/change-password`, {
      currentPassword: passwordForm.current,
      newPassword: passwordForm.next
    }, { headers: authHeaders() })
    isPasswordModalOpen.value = false
  } catch (err) {
    passwordError.value = err.response?.data?.message || 'Failed to change password.'
  } finally {
    changingPassword.value = false
  }
}
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