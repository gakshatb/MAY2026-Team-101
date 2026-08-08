<template>
  <div class="max-w-7xl mx-auto space-y-8 animate-fade-in">

    <!-- Page Header -->
    <div>
      <h1 class="text-3xl font-bold text-slate-900 tracking-tight mb-1">My Profile</h1>
      <p class="text-slate-500">Manage your personal information and account settings.</p>
    </div>

    <!-- Role-based Complaint Summary -->
    <div v-if="userRole === 'Citizen'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Total Complaints</span>
        <span class="text-3xl font-bold text-slate-900">{{ complaintStats.total }}</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Pending</span>
        <span class="text-3xl font-bold text-amber-500">{{ complaintStats.pending }}</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Resolved</span>
        <span class="text-3xl font-bold text-[#22C55E]">{{ complaintStats.resolved }}</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Closed</span>
        <span class="text-3xl font-bold text-slate-400">{{ complaintStats.closed }}</span>
      </div>
    </div>

    <div v-if="userRole === 'Civic Officer'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Complaints Managed</span>
        <span class="text-3xl font-bold text-slate-900">145</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Pending Reviews</span>
        <span class="text-3xl font-bold text-amber-500">12</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Resolved (This Month)</span>
        <span class="text-3xl font-bold text-[#22C55E]">89</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Assigned Workers</span>
        <span class="text-3xl font-bold text-[#2563EB]">24</span>
      </div>
    </div>

    <div v-if="userRole === 'Field Worker'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Assigned Tasks</span>
        <span class="text-3xl font-bold text-slate-900">8</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Completed Tasks</span>
        <span class="text-3xl font-bold text-[#22C55E]">42</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Pending Tasks</span>
        <span class="text-3xl font-bold text-amber-500">5</span>
      </div>
      <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100 flex flex-col">
        <span class="text-sm font-medium text-slate-500 mb-1">Avg. Completion Time</span>
        <span class="text-3xl font-bold text-[#2563EB]">18h</span>
      </div>
    </div>

    <!-- Main Layout Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

      <!-- Left Column: Profile & Account Info -->
      <div class="lg:col-span-4 space-y-8">

        <!-- Profile Card -->
        <div
          class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6 flex flex-col items-center text-center">
          <div class="relative mb-5 group">
            <div
              class="w-32 h-32 rounded-full overflow-hidden border-4 border-white shadow-md bg-slate-100 flex items-center justify-center">
              <img v-if="photoUrl" :src="photoUrl" alt="Profile Picture" class="w-full h-full object-cover" />
              <span v-else class="text-3xl font-bold text-slate-400">{{ initials }}</span>
              <div v-if="isUploadingPhoto"
                class="absolute inset-0 rounded-full bg-white/70 flex items-center justify-center">
                <span class="w-6 h-6 border-2 border-slate-300 border-t-[#2563EB] rounded-full animate-spin"></span>
              </div>
            </div>
            <input ref="photoInput" type="file" accept=".png,.jpg,.jpeg" class="hidden" @change="onPhotoSelected" />
            <button @click="photoInput.click()" :disabled="isUploadingPhoto"
              class="absolute bottom-0 right-0 bg-[#2563EB] hover:bg-[#1E40AF] text-white p-2.5 rounded-full shadow-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#2563EB] disabled:opacity-60">
              <Camera class="w-5 h-5" />
            </button>
          </div>
          <button v-if="photoUrl" @click="removePhoto" :disabled="isUploadingPhoto"
            class="text-xs font-medium text-slate-400 hover:text-red-500 transition-colors -mt-3 mb-3">
            Remove photo
          </button>
          <p v-if="photoError" class="text-xs text-red-500 -mt-2 mb-3">{{ photoError }}</p>
          <h2 class="text-xl font-bold text-slate-900 mb-1">{{ profileForm.fullName }}</h2>
          <p class="text-sm font-medium text-[#2563EB] mb-4">{{ userRole }}</p>
          <div
            class="flex items-center gap-2 px-3 py-1 bg-[#22C55E]/10 text-[#22C55E] rounded-full text-xs font-semibold tracking-wide uppercase">
            <Check class="w-3.5 h-3.5" />
            Verified Account
          </div>
        </div>

        <!-- Account Information Card -->
        <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
          <h3 class="text-lg font-bold text-slate-900 mb-5 flex items-center gap-2">
            <Shield class="w-5 h-5 text-slate-400" />
            Account Information
          </h3>
          <div class="space-y-4">
            <div class="flex justify-between items-center py-2 border-b border-slate-50 last:border-0">
              <span class="text-sm text-slate-500">Account ID</span>
              <span class="text-sm font-medium text-slate-900">{{ profileForm.accountId }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-slate-50 last:border-0">
              <span class="text-sm text-slate-500">Status</span>
              <span class="text-sm font-medium text-[#22C55E]">Active</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-slate-50 last:border-0">
              <span class="text-sm text-slate-500">Registered On</span>
              <span class="text-sm font-medium text-slate-900">{{ profileForm.memberSince }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-slate-50 last:border-0">
              <span class="text-sm text-slate-500">Last Login</span>
              <span class="text-sm font-medium text-slate-900">{{ profileForm.lastLogin || 'N/A' }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Forms & Timeline -->
      <div class="lg:col-span-8 space-y-8">

        <!-- Personal Information Form -->
        <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6 sm:p-8">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <h3 class="text-xl font-bold text-slate-900 flex items-center gap-2">
              <User class="w-5 h-5 text-slate-400" />
              Personal Information
            </h3>
            <button v-if="!isEditingProfile" @click="toggleEdit"
              class="text-sm font-medium text-[#2563EB] bg-blue-50 hover:bg-blue-100 px-4 py-2 rounded-lg transition-colors">
              Edit Profile
            </button>
          </div>

          <form @submit.prevent="saveProfile" novalidate class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-5">
            <!-- Full Name -->
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Full Name</label>
              <input v-model="profileForm.fullName" type="text" :disabled="!isEditingProfile"
                :class="inputClasses(profileErrors.fullName, !isEditingProfile)" />
              <span v-if="profileErrors.fullName" class="text-red-500 text-xs mt-1 block">{{ profileErrors.fullName
                }}</span>
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Email Address</label>
              <div class="relative">
                <Mail class="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
                <input v-model="profileForm.email" type="email" :disabled="!isEditingProfile"
                  :class="[inputClasses(profileErrors.email, !isEditingProfile), 'pl-9']" />
              </div>
              <span v-if="profileErrors.email" class="text-red-500 text-xs mt-1 block">{{ profileErrors.email }}</span>
            </div>

            <!-- Mobile -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Mobile Number</label>
              <div class="relative">
                <Phone class="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
                <input v-model="profileForm.mobile" type="text" maxlength="10" :disabled="!isEditingProfile"
                  :class="[inputClasses(profileErrors.mobile, !isEditingProfile), 'pl-9']" />
              </div>
              <span v-if="profileErrors.mobile" class="text-red-500 text-xs mt-1 block">{{ profileErrors.mobile
                }}</span>
            </div>

            <!-- Address -->
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Residential Address</label>
              <div class="relative">
                <MapPin class="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
                <input v-model="profileForm.address" type="text" :disabled="!isEditingProfile"
                  :class="[inputClasses(profileErrors.address, !isEditingProfile), 'pl-9']" />
              </div>
              <span v-if="profileErrors.address" class="text-red-500 text-xs mt-1 block">{{ profileErrors.address
                }}</span>
            </div>

            <!-- City -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">City</label>
              <div class="relative">
                <Building class="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
                <input v-model="profileForm.city" type="text" :disabled="!isEditingProfile"
                  :class="[inputClasses(profileErrors.city, !isEditingProfile), 'pl-9']" />
              </div>
              <span v-if="profileErrors.city" class="text-red-500 text-xs mt-1 block">{{ profileErrors.city }}</span>
            </div>

            <!-- State -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">State</label>
              <input v-model="profileForm.state" type="text" :disabled="!isEditingProfile"
                :class="inputClasses(profileErrors.state, !isEditingProfile)" />
              <span v-if="profileErrors.state" class="text-red-500 text-xs mt-1 block">{{ profileErrors.state }}</span>
            </div>

            <!-- Pincode -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Pincode</label>
              <input v-model="profileForm.pincode" type="text" maxlength="6" :disabled="!isEditingProfile"
                :class="inputClasses(profileErrors.pincode, !isEditingProfile)" />
              <span v-if="profileErrors.pincode" class="text-red-500 text-xs mt-1 block">{{ profileErrors.pincode
                }}</span>
            </div>

            <!-- Gender -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Gender</label>
              <select v-model="profileForm.gender" :disabled="!isEditingProfile"
                :class="[inputClasses(profileErrors.gender, !isEditingProfile), 'appearance-none']">
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
              <span v-if="profileErrors.gender" class="text-red-500 text-xs mt-1 block">{{ profileErrors.gender }}</span>
            </div>

            <!-- Action Buttons -->
            <div v-if="isEditingProfile"
              class="sm:col-span-2 flex items-center justify-end gap-3 mt-4 pt-4 border-t border-slate-100">
              <button type="button" @click="cancelEdit"
                class="px-5 py-2.5 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors">
                Cancel
              </button>
              <button type="submit" :disabled="isSavingProfile"
                class="px-5 py-2.5 text-sm font-medium text-white bg-[#2563EB] rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center gap-2 disabled:opacity-70">
                <span v-if="isSavingProfile"
                  class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                Save Changes
              </button>
            </div>
          </form>
        </div>

        <!-- Change Password Form -->
        <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6 sm:p-8">
          <h3 class="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
            <Lock class="w-5 h-5 text-slate-400" />
            Security Settings
          </h3>

          <form @submit.prevent="updatePassword" novalidate class="space-y-5">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <!-- Current Password -->
              <div class="sm:col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-1.5">Current Password</label>
                <div class="relative">
                  <input v-model="passwordForm.current" :type="showPasswords.current ? 'text' : 'password'"
                    :class="inputClasses(passwordErrors.current, false)" placeholder="Enter current password" />
                  <button type="button" @click="showPasswords.current = !showPasswords.current"
                    class="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600">
                    <EyeOff v-if="showPasswords.current" class="w-5 h-5" />
                    <Eye v-else class="w-5 h-5" />
                  </button>
                </div>
                <span v-if="passwordErrors.current" class="text-red-500 text-xs mt-1 block">{{ passwordErrors.current
                  }}</span>
              </div>

              <!-- New Password -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1.5">New Password</label>
                <div class="relative">
                  <input v-model="passwordForm.new" :type="showPasswords.new ? 'text' : 'password'"
                    :class="inputClasses(passwordErrors.new, false)" placeholder="Enter new password" />
                  <button type="button" @click="showPasswords.new = !showPasswords.new"
                    class="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600">
                    <EyeOff v-if="showPasswords.new" class="w-5 h-5" />
                    <Eye v-else class="w-5 h-5" />
                  </button>
                </div>
                <span v-if="passwordErrors.new" class="text-red-500 text-xs mt-1 block">{{ passwordErrors.new }}</span>
              </div>

              <!-- Confirm Password -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1.5">Confirm New Password</label>
                <div class="relative">
                  <input v-model="passwordForm.confirm" :type="showPasswords.confirm ? 'text' : 'password'"
                    :class="inputClasses(passwordErrors.confirm, false)" placeholder="Confirm new password" />
                  <button type="button" @click="showPasswords.confirm = !showPasswords.confirm"
                    class="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600">
                    <EyeOff v-if="showPasswords.confirm" class="w-5 h-5" />
                    <Eye v-else class="w-5 h-5" />
                  </button>
                </div>
                <span v-if="passwordErrors.confirm" class="text-red-500 text-xs mt-1 block">{{ passwordErrors.confirm
                  }}</span>
              </div>
            </div>

            <div class="flex items-center gap-3 mt-2">
              <button type="submit" :disabled="isUpdatingPassword"
                class="px-5 py-2.5 text-sm font-medium text-white bg-slate-800 rounded-lg hover:bg-slate-900 transition-colors shadow-sm flex items-center gap-2 disabled:opacity-70">
                <span v-if="isUpdatingPassword"
                  class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                Update Password
              </button>
              <button type="button" @click="resetPasswordForm"
                class="px-5 py-2.5 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
                Reset
              </button>
            </div>
          </form>
        </div>

      </div>
    </div>

    <!-- Dashboard Footer -->
    <div class="max-w-7xl mx-auto mt-12 pt-6 border-t border-slate-200">
      <p class="text-center text-sm text-slate-500">&copy; 2026 CivicDesk. All rights reserved.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import {
  User, Mail, Phone, MapPin, Building,
  Lock, Eye, EyeOff, Shield, Check,
  Camera
} from 'lucide-vue-next'

// --- State ---
const userRole = ref('Citizen') // Options: 'Citizen', 'Civic Officer', 'Field Worker'
const router = useRouter()
const isEditingProfile = ref(false)
const isSavingProfile = ref(false)
const isUpdatingPassword = ref(false)
const profileSuccess = ref('')
const passwordSuccess = ref('')

const currentUser = ref(JSON.parse(localStorage.getItem('user') || 'null'))

const complaintStats = reactive({ total: 0, pending: 0, resolved: 0, closed: 0 })

const fetchComplaintStats = async () => {
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://127.0.0.1:5000/api/citizen/complaints/summary', {
      headers: { Authorization: `Bearer ${token}` }
    })
    Object.assign(complaintStats, {
      total: data.summary.total,
      pending: data.summary.pending,
      resolved: data.summary.resolved,
      closed: data.summary.closed,
    })
  } catch (err) {
    console.error('Complaint stats fetch error:', err)
  }
}

// Original data to revert changes on cancel
let originalProfileData = {}

const profileForm = reactive({
  fullName: '', email: '', mobile: '',
  address: '', city: '', state: '', pincode: '', gender: '',
  accountId: '', memberSince: '', lastLogin: ''
})

const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://127.0.0.1:5000/api/citizen/profile', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const u = data.profile
    Object.assign(profileForm, {
      fullName: u.fullName || '',
      email: u.email || '',
      mobile: u.mobile || '',
      address: u.address || '',
      city: u.city || '',
      state: u.state || '',
      pincode: u.pincode || '',
      gender: u.gender || '',
      accountId: u.accountId || '',
      memberSince: u.memberSince || '',
      lastLogin: u.lastLogin || ''
    })
    // Keep the header avatar (which reads from localStorage) in sync too.
    currentUser.value = { ...currentUser.value, profilePhoto: u.profilePhoto || null }
    localStorage.setItem('user', JSON.stringify(currentUser.value))
    window.dispatchEvent(new Event('user-updated')) // live-refresh navbar avatar/name in DashboardLayout
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
  }
}
onMounted(() => {
  fetchProfile()
  if (userRole.value === 'Citizen') fetchComplaintStats()
})

const photoInput = ref(null)
const isUploadingPhoto = ref(false)
const photoError = ref('')
const photoUrl = computed(() => currentUser.value?.profilePhoto ? `http://127.0.0.1:5000${currentUser.value.profilePhoto}` : '')
const initials = computed(() => {
  const name = profileForm.fullName
  if (!name) return '?'
  return name.trim().split(/\s+/).slice(0, 2).map(n => n[0]?.toUpperCase()).join('')
})

const ALLOWED_PHOTO_TYPES = ['image/png', 'image/jpeg']
const MAX_PHOTO_BYTES = 5 * 1024 * 1024

const onPhotoSelected = async (e) => {
  const file = e.target.files[0]
  e.target.value = '' // allow re-selecting the same file later
  if (!file) return

  photoError.value = ''
  if (!ALLOWED_PHOTO_TYPES.includes(file.type)) {
    photoError.value = 'Only PNG and JPEG images are allowed.'
    return
  }
  if (file.size > MAX_PHOTO_BYTES) {
    photoError.value = 'Image exceeds the 5MB size limit.'
    return
  }

  isUploadingPhoto.value = true
  try {
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('photo', file)
    const { data } = await axios.post('http://127.0.0.1:5000/api/citizen/profile/photo', formData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    })
    currentUser.value = { ...currentUser.value, profilePhoto: data.profilePhoto }
    localStorage.setItem('user', JSON.stringify(currentUser.value))
    window.dispatchEvent(new Event('user-updated')) // live-refresh navbar avatar/name in DashboardLayout
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
    photoError.value = err.response?.data?.message || 'Upload failed. Please try again.'
  } finally {
    isUploadingPhoto.value = false
  }
}

const removePhoto = async () => {
  isUploadingPhoto.value = true
  photoError.value = ''
  try {
    const token = localStorage.getItem('token')
    await axios.delete('http://127.0.0.1:5000/api/citizen/profile/photo', {
      headers: { Authorization: `Bearer ${token}` }
    })
    currentUser.value = { ...currentUser.value, profilePhoto: null }
    localStorage.setItem('user', JSON.stringify(currentUser.value))
    window.dispatchEvent(new Event('user-updated')) // live-refresh navbar avatar/name in DashboardLayout
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
    photoError.value = 'Could not remove photo. Please try again.'
  } finally {
    isUploadingPhoto.value = false
  }
}

const passwordForm = reactive({
  current: '',
  new: '',
  confirm: ''
})

const showPasswords = reactive({
  current: false,
  new: false,
  confirm: false
})

const profileErrors = reactive({})
const passwordErrors = reactive({})

// --- Helpers ---
const inputClasses = (hasError, isDisabled) => {
  return [
    'w-full px-4 py-2.5 border rounded-lg text-sm transition-all focus:outline-none focus:ring-2',
    isDisabled
      ? 'bg-slate-50 border-slate-200 text-slate-500 cursor-not-allowed'
      : hasError
        ? 'bg-red-50/50 border-red-500 focus:border-red-500 focus:ring-red-200 text-slate-900'
        : 'bg-white border-slate-300 focus:border-[#2563EB] focus:ring-[#2563EB]/20 text-slate-900'
  ]
}

// --- Methods ---
const toggleEdit = () => {
  originalProfileData = { ...profileForm }
  isEditingProfile.value = true
  Object.keys(profileErrors).forEach(key => delete profileErrors[key])
}

const cancelEdit = () => {
  Object.assign(profileForm, originalProfileData)
  isEditingProfile.value = false
  Object.keys(profileErrors).forEach(key => delete profileErrors[key])
}

const validateProfile = () => {
  let isValid = true
  Object.keys(profileErrors).forEach(key => delete profileErrors[key])

  if (!profileForm.fullName.trim()) {
    profileErrors.fullName = 'Full Name is required'
    isValid = false
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(profileForm.email)) {
    profileErrors.email = 'Valid email is required'
    isValid = false
  }

  if (!/^\d{10}$/.test(profileForm.mobile)) {
    profileErrors.mobile = 'Enter a valid 10-digit mobile number'
    isValid = false
  }

  if (!profileForm.address.trim()) profileErrors.address = 'Address is required', isValid = false
  if (!profileForm.city.trim()) profileErrors.city = 'City is required', isValid = false
  if (!profileForm.state.trim()) profileErrors.state = 'State is required', isValid = false
  if (!profileForm.gender.trim()) profileErrors.gender = 'Gender is required', isValid = false

  if (!/^\d{6}$/.test(profileForm.pincode)) {
    profileErrors.pincode = 'Enter a valid 6-digit pincode'
    isValid = false
  }

  return isValid
}

const saveProfile = async () => {
  if (!validateProfile()) return
  isSavingProfile.value = true
  profileSuccess.value = ''
  try {
    const token = localStorage.getItem('token')
    await axios.put('http://127.0.0.1:5000/api/citizen/profile', {
      fullName: profileForm.fullName,
      email: profileForm.email,
      mobile: profileForm.mobile,
      address: profileForm.address,
      city: profileForm.city,
      state: profileForm.state,
      pincode: profileForm.pincode,
      gender: profileForm.gender,
    }, { headers: { Authorization: `Bearer ${token}` } })
    isEditingProfile.value = false
    profileSuccess.value = 'Profile updated successfully.'

    currentUser.value = {
      ...currentUser.value,
      name: profileForm.fullName,
      email: profileForm.email,
    }
    localStorage.setItem('user', JSON.stringify(currentUser.value))
    window.dispatchEvent(new Event('user-updated')) // live-refresh navbar avatar/name in DashboardLayout
  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
    profileErrors.submit = err.response?.data?.message || 'Update failed.'
  } finally {
    isSavingProfile.value = false
  }
}

const validatePassword = () => {
  let isValid = true
  Object.keys(passwordErrors).forEach(key => delete passwordErrors[key])

  if (!passwordForm.current) {
    passwordErrors.current = 'Current password is required'
    isValid = false
  }

  const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\W]{8,}$/
  if (!strongPasswordRegex.test(passwordForm.new)) {
    passwordErrors.new = 'Must be at least 8 chars with uppercase, lowercase, and number'
    isValid = false
  }

  if (passwordForm.new !== passwordForm.confirm) {
    passwordErrors.confirm = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const updatePassword = async () => {
  if (!validatePassword()) return
  isUpdatingPassword.value = true
  passwordSuccess.value = ''
  try {
    const token = localStorage.getItem('token')
    await axios.post('http://127.0.0.1:5000/api/change-password', {
      currentPassword: passwordForm.current,
      newPassword: passwordForm.new,
    }, { headers: { Authorization: `Bearer ${token}` } })
    passwordSuccess.value = 'Password updated successfully.'
    resetPasswordForm()
  } catch (err) {
    if (err.response?.status === 400 && err.response?.data?.message?.includes('incorrect')) {
      passwordErrors.current = 'Current password is incorrect.'
    } else {
      passwordErrors.submit = err.response?.data?.message || 'Password update failed.'
    }
  } finally {
    isUpdatingPassword.value = false
  }
}

const resetPasswordForm = () => {
  passwordForm.current = ''
  passwordForm.new = ''
  passwordForm.confirm = ''
  Object.keys(passwordErrors).forEach(key => delete passwordErrors[key])
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
.animate-fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
main::-webkit-scrollbar { width: 6px; }
main::-webkit-scrollbar-track { background: transparent; }
main::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 20px; }
</style>