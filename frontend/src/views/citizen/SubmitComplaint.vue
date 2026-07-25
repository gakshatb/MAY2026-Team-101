<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <!-- Reusable Sidebar -->
    <Sidebar :userRole="userRole" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
      <!-- Reusable Dashboard Navbar -->
      <DashboardNavbar 
        :userRole="userRole" 
        :user="currentUser"
        pageTitle="Submit Complaint"
        breadcrumb="Submit Complaint"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
      />

      <!-- Main Scrollable Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto space-y-6">
          
          <!-- Page Header -->
          <div class="mb-8">
            <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight mb-2">Submit Complaint</h1>
            <p class="text-slate-500 max-w-2xl leading-relaxed">
              Report civic issues in your locality. Provide accurate details so the concerned department can resolve the issue quickly.
            </p>
          </div>

          <!-- Main Layout Grid -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
            
            <!-- Left Column: Form -->
            <div class="xl:col-span-8">
              <form @submit.prevent="handleSubmit" novalidate class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                
                <!-- Section 1: Complaint Information -->
                <div class="p-6 sm:p-8 border-b border-slate-100">
                  <h2 class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                    <ClipboardList class="w-5 h-5 text-slate-400" />
                    Complaint Information
                  </h2>
                  
                  <div class="space-y-6">
                    <div>
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Complaint Title <span class="text-red-500">*</span></label>
                      <input 
                        v-model="form.title" 
                        type="text" 
                        maxlength="100"
                        :class="inputClasses(errors.title)"
                        placeholder="Enter a short title (e.g., Deep pothole on Main Street)"
                      />
                      <span v-if="errors.title" class="text-red-500 text-xs mt-1.5 block">{{ errors.title }}</span>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                      <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1.5">Category <span class="text-red-500">*</span></label>
                        <select v-model="form.category" :class="[inputClasses(errors.category), 'appearance-none cursor-pointer']">
                          <option value="" disabled>Select a category</option>
                          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
                        </select>
                        <span v-if="errors.category" class="text-red-500 text-xs mt-1.5 block">{{ errors.category }}</span>
                      </div>

                      <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1.5">Priority Level</label>
                        <div class="flex items-center gap-3">
                          <button 
                            v-for="p in priorities" 
                            :key="p.value"
                            type="button"
                            @click="form.priority = p.value"
                            :class="[
                              'flex-1 py-2.5 px-3 rounded-lg text-sm font-medium transition-all border',
                              form.priority === p.value 
                                ? `${p.activeClass} border-transparent shadow-sm` 
                                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                            ]"
                          >
                            {{ p.label }}
                          </button>
                        </div>
                      </div>
                    </div>

                    <div>
                      <label class="flex justify-between items-end mb-1.5">
                        <span class="text-sm font-medium text-slate-700">Description <span class="text-red-500">*</span></span>
                        <span :class="['text-xs font-medium', descriptionLength < 30 ? 'text-amber-500' : 'text-slate-400']">
                          {{ descriptionLength }}/500
                        </span>
                      </label>
                      <textarea 
                        v-model="form.description" 
                        rows="4"
                        maxlength="500"
                        :class="[inputClasses(errors.description), 'resize-none py-3']"
                        placeholder="Describe the issue in detail. Minimum 30 characters required."
                      ></textarea>
                      <span v-if="errors.description" class="text-red-500 text-xs mt-1.5 block">{{ errors.description }}</span>
                    </div>
                  </div>
                </div>

                <!-- Section 2: Location Details -->
                <div class="p-6 sm:p-8 border-b border-slate-100">
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                    <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                      <MapPin class="w-5 h-5 text-slate-400" />
                      Location Details
                    </h2>
                    <button 
                      type="button" 
                      @click="useMyLocation"
                      class="text-sm font-medium text-[#2563EB] bg-blue-50 hover:bg-blue-100 px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
                    >
                      <Navigation class="w-4 h-4" />
                      {{ isLocating ? 'Locating...' : 'Use My Location' }}
                    </button>
                  </div>

                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div>
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">City <span class="text-red-500">*</span></label>
                      <div class="relative">
                        <Building class="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
                        <input v-model="form.city" type="text" :class="[inputClasses(false), 'pl-9']" />
                      </div>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Ward Number <span class="text-red-500">*</span></label>
                      <input v-model="form.ward" type="text" :class="inputClasses(errors.ward)" placeholder="e.g., Ward 4" />
                      <span v-if="errors.ward" class="text-red-500 text-xs mt-1.5 block">{{ errors.ward }}</span>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Area / Locality <span class="text-red-500">*</span></label>
                      <input v-model="form.area" type="text" :class="inputClasses(errors.area)" placeholder="Locality name" />
                      <span v-if="errors.area" class="text-red-500 text-xs mt-1.5 block">{{ errors.area }}</span>
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Street Name <span class="text-red-500">*</span></label>
                      <input v-model="form.street" type="text" :class="inputClasses(errors.street)" placeholder="Street or road name" />
                      <span v-if="errors.street" class="text-red-500 text-xs mt-1.5 block">{{ errors.street }}</span>
                    </div>
                    <div class="sm:col-span-2">
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Nearby Landmark (Optional)</label>
                      <input v-model="form.landmark" type="text" :class="inputClasses(false)" placeholder="Hospital, school, famous shop, etc." />
                    </div>
                  </div>
                </div>

                <!-- Section 3: Upload Evidence -->
                <div class="p-6 sm:p-8 border-b border-slate-100">
                  <h2 class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                    <Camera class="w-5 h-5 text-slate-400" />
                    Upload Evidence
                  </h2>
                  
                  <div 
                    @dragover.prevent="isDragging = true"
                    @dragleave.prevent="isDragging = false"
                    @drop.prevent="handleDrop"
                    :class="[
                      'w-full border-2 border-dashed rounded-xl p-8 transition-colors text-center cursor-pointer',
                      isDragging ? 'border-[#2563EB] bg-blue-50' : 'border-slate-300 bg-slate-50 hover:bg-slate-100',
                      form.image ? 'border-solid border-slate-200 bg-white' : ''
                    ]"
                  >
                    <input type="file" id="fileUpload" class="hidden" accept="image/png, image/jpeg, image/jpg" @change="handleFileSelect" />
                    
                    <div v-if="!form.image" @click="triggerFileInput" class="flex flex-col items-center gap-3">
                      <div class="w-12 h-12 rounded-full bg-white shadow-sm flex items-center justify-center border border-slate-100 mb-2">
                        <Upload class="w-5 h-5 text-[#2563EB]" />
                      </div>
                      <div>
                        <p class="text-sm font-bold text-slate-700">Click to upload or drag and drop</p>
                        <p class="text-xs text-slate-500 mt-1">PNG, JPG or JPEG (Max 5MB)</p>
                      </div>
                    </div>

                    <div v-else class="flex flex-col sm:flex-row items-center justify-between gap-4">
                      <div class="flex items-center gap-4 text-left">
                        <div class="w-16 h-16 rounded-lg bg-slate-100 overflow-hidden shrink-0 border border-slate-200">
                          <img v-if="imagePreview" :src="imagePreview" class="w-full h-full object-cover" alt="Preview" />
                          <Image class="w-6 h-6 text-slate-400 m-auto mt-5" v-else />
                        </div>
                        <div class="min-w-0">
                          <p class="text-sm font-bold text-slate-900 truncate">{{ form.image.name }}</p>
                          <p class="text-xs text-[#22C55E] mt-1 flex items-center gap-1">
                            <CheckCircle2 class="w-3.5 h-3.5" /> Ready to upload
                          </p>
                        </div>
                      </div>
                      <button type="button" @click.stop="removeImage" class="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                        <Trash class="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                  <p class="text-xs text-slate-500 mt-3 flex items-center gap-1.5">
                    <Info class="w-4 h-4 text-slate-400" />
                    Uploading clear images helps authorities verify complaints faster.
                  </p>
                </div>

                <!-- Section 4: Additional Information -->
                <div class="p-6 sm:p-8 border-b border-slate-100">
                  <h2 class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                    <Calendar class="w-5 h-5 text-slate-400" />
                    Additional Details
                  </h2>
                  
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
                    <div>
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Incident Date (Optional)</label>
                      <input v-model="form.incidentDate" type="date" :class="inputClasses(false)" />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Best Time to Visit (Optional)</label>
                      <select v-model="form.visitTime" :class="[inputClasses(false), 'appearance-none']">
                        <option value="">Any time</option>
                        <option value="Morning">Morning (8 AM - 12 PM)</option>
                        <option value="Afternoon">Afternoon (12 PM - 4 PM)</option>
                        <option value="Evening">Evening (4 PM - 8 PM)</option>
                      </select>
                    </div>
                    <div class="sm:col-span-2">
                      <label class="block text-sm font-medium text-slate-700 mb-1.5">Urgency Note (Optional)</label>
                      <input v-model="form.urgencyNote" type="text" :class="inputClasses(false)" placeholder="Briefly explain if this is an immediate safety hazard." />
                    </div>
                  </div>

                  <label class="flex items-start gap-3 cursor-pointer group mt-4">
                    <div class="flex items-center h-5">
                      <input v-model="form.terms" type="checkbox" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB] transition-colors" />
                    </div>
                    <div>
                      <span class="text-sm text-slate-700 group-hover:text-slate-900 transition-colors">I confirm that the information provided is accurate to the best of my knowledge. <span class="text-red-500">*</span></span>
                      <span v-if="errors.terms" class="text-red-500 text-xs mt-1 block">{{ errors.terms }}</span>
                    </div>
                  </label>
                </div>

                <!-- Action Buttons -->
                <div class="p-6 sm:p-8 bg-slate-50 flex flex-col-reverse sm:flex-row items-center justify-end gap-3">
                  <button 
                    type="button" 
                    @click="clearForm" 
                    class="w-full sm:w-auto px-6 py-2.5 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-100 transition-colors"
                  >
                    Clear Form
                  </button>
                  <button 
                    type="submit" 
                    :disabled="isSubmitting"
                    class="w-full sm:w-auto px-8 py-2.5 text-sm font-medium text-white bg-[#2563EB] rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
                  >
                    <Loader2 v-if="isSubmitting" class="w-4 h-4 animate-spin" />
                    <span>{{ isSubmitting ? 'Submitting...' : 'Submit Complaint' }}</span>
                  </button>
                </div>
              </form>
            </div>

            <!-- Right Column: Sidebar Cards -->
            <div class="xl:col-span-4 space-y-6 hidden xl:block">
              <!-- Quick Tips Card -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Lightbulb class="w-5 h-5 text-amber-500" />
                  Quick Tips
                </h3>
                <ul class="space-y-4">
                  <li v-for="tip in tips" :key="tip" class="flex items-start gap-3">
                    <CheckCircle2 class="w-5 h-5 text-[#22C55E] shrink-0" />
                    <span class="text-sm text-slate-600 leading-tight pt-0.5">{{ tip }}</span>
                  </li>
                </ul>
              </div>

              <!-- Recent Complaints Card -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Clock class="w-5 h-5 text-slate-400" />
                  Recent Complaints
                </h3>
                <div class="space-y-4">
                  <div class="p-3 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-between">
                    <div>
                      <p class="text-sm font-bold text-slate-900">Streetlight Failure</p>
                      <p class="text-xs text-slate-500 mt-0.5">Ward 4, MG Road</p>
                    </div>
                    <span class="px-2.5 py-1 rounded-md bg-[#22C55E]/10 text-[#22C55E] text-xs font-semibold uppercase">Resolved</span>
                  </div>
                  <div class="p-3 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-between">
                    <div>
                      <p class="text-sm font-bold text-slate-900">Garbage Accumulation</p>
                      <p class="text-xs text-slate-500 mt-0.5">Area 51, West End</p>
                    </div>
                    <span class="px-2.5 py-1 rounded-md bg-amber-100 text-amber-700 text-xs font-semibold uppercase">Pending</span>
                  </div>
                  <div class="p-3 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-between">
                    <div>
                      <p class="text-sm font-bold text-slate-900">Blocked Drainage</p>
                      <p class="text-xs text-slate-500 mt-0.5">Sector 9, Market</p>
                    </div>
                    <span class="px-2.5 py-1 rounded-md bg-[#2563EB]/10 text-[#2563EB] text-xs font-semibold uppercase">In Progress</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>

    <!-- Success Modal Overlay -->
    <transition name="fade">
      <div v-if="showSuccessModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
        <div class="bg-white rounded-[16px] shadow-2xl max-w-md w-full p-8 text-center transform transition-all" @click.stop>
          <div class="w-20 h-20 bg-[#22C55E]/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 class="w-10 h-10 text-[#22C55E]" />
          </div>
          <h2 class="text-2xl font-bold text-slate-900 mb-2">Complaint Submitted!</h2>
          <p class="text-slate-600 mb-6 leading-relaxed">
            Your complaint has been submitted successfully. The concerned authorities will review it shortly.
          </p>
          <div class="bg-slate-50 rounded-lg p-4 mb-8 border border-slate-100">
            <p class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Complaint ID</p>
            <p class="text-xl font-bold text-slate-900 font-mono tracking-tight">{{ generatedId }}</p>
          </div>
          <div class="flex flex-col gap-3">
            <router-link to="/citizen/complaints" class="w-full px-6 py-3 text-sm font-medium text-white bg-[#2563EB] rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm">
              View Complaint Status
            </router-link>
            <button @click="showSuccessModal = false; clearForm()" class="w-full px-6 py-3 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors">
              Submit Another Issue
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../../components/dashboard/Sidebar.vue'
import DashboardNavbar from '../../components/dashboard/DashboardNavbar.vue'
import { 
  ClipboardList, MapPin, Building, Camera, 
  Calendar, Upload, Image, Trash, Navigation, 
  CheckCircle2, Loader2, Info, Lightbulb, Clock
} from 'lucide-vue-next'

// State
const userRole = ref('Citizen')
const isSidebarOpen = ref(false)
const currentUser = computed(() => {
  const stored = localStorage.getItem('user')
  return stored ? JSON.parse(stored) : null
})
const isSubmitting = ref(false)
const isLocating = ref(false)
const isDragging = ref(false)
const showSuccessModal = ref(false)
const imagePreview = ref(null)
const generatedId = ref('')

const categories = [
  'Garbage Collection',
  'Overflowing Dustbin',
  'Potholes',
  'Road Damage',
  'Broken Streetlight',
  'Water Leakage',
  'Blocked Drainage',
  'Illegal Waste Dumping',
  'Public Property Damage',
  'Other'
]

const priorities = [
  { label: 'Low', value: 'Low', activeClass: 'bg-slate-800 text-white' },
  { label: 'Medium', value: 'Medium', activeClass: 'bg-[#2563EB] text-white' },
  { label: 'High', value: 'High', activeClass: 'bg-amber-500 text-white' },
  { label: 'Emergency', value: 'Emergency', activeClass: 'bg-red-500 text-white' }
]

const tips = [
  'Report one issue per complaint.',
  'Upload a clear image if available.',
  'Mention the exact location.',
  'Write a detailed description.',
  'Avoid duplicate complaints.'
]

const form = reactive({
  title: '',
  category: '',
  priority: 'Medium',
  description: '',
  city: 'Bhiwandi',
  ward: '',
  area: '',
  street: '',
  landmark: '',
  incidentDate: '',
  visitTime: '',
  urgencyNote: '',
  terms: false,
  image: null
})

const errors = reactive({})

// Computed
const descriptionLength = computed(() => form.description.length)

// Helpers
const inputClasses = (hasError) => {
  return [
    'w-full px-4 py-2.5 border rounded-lg text-sm transition-all focus:outline-none focus:ring-2 bg-white',
    hasError 
      ? 'bg-red-50/50 border-red-500 focus:border-red-500 focus:ring-red-200 text-slate-900' 
      : 'border-slate-300 focus:border-[#2563EB] focus:ring-[#2563EB]/20 text-slate-900'
  ]
}

// File Upload Logic
const triggerFileInput = () => {
  document.getElementById('fileUpload').click()
}

const processFile = (file) => {
  if (!file) return
  const validTypes = ['image/jpeg', 'image/jpg', 'image/png']
  if (!validTypes.includes(file.type)) {
    alert('Please upload a valid image file (PNG, JPG, JPEG).')
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    alert('File size exceeds 5MB limit.')
    return
  }
  form.image = file
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleFileSelect = (e) => {
  processFile(e.target.files[0])
}

const handleDrop = (e) => {
  isDragging.value = false
  processFile(e.dataTransfer.files[0])
}

const removeImage = () => {
  form.image = null
  imagePreview.value = null
  document.getElementById('fileUpload').value = ''
}

// Location Logic
const useMyLocation = async () => {
  isLocating.value = true
  await new Promise(resolve => setTimeout(resolve, 800)) // Simulate GPS delay
  form.ward = 'Ward 12'
  form.area = 'Kalyan Naka'
  form.street = 'Agra Road'
  isLocating.value = false
}

// Form Submission
const validateForm = () => {
  Object.keys(errors).forEach(key => delete errors[key])
  let isValid = true

  if (!form.title.trim()) { errors.title = 'Title is required'; isValid = false }
  if (!form.category) { errors.category = 'Category is required'; isValid = false }
  if (descriptionLength.value < 30) { errors.description = 'Please provide at least 30 characters'; isValid = false }
  if (!form.ward.trim()) { errors.ward = 'Ward number is required'; isValid = false }
  if (!form.area.trim()) { errors.area = 'Area/Locality is required'; isValid = false }
  if (!form.street.trim()) { errors.street = 'Street name is required'; isValid = false }
  if (!form.terms) { errors.terms = 'You must confirm the information is accurate'; isValid = false }

  // Scroll to first error (simplified for demo)
  if (!isValid) window.scrollTo({ top: 0, behavior: 'smooth' })

  return isValid
}

const router = useRouter()

const handleSubmit = async () => {
  if (!validateForm()) return
  isSubmitting.value = true
  try {
    const token = localStorage.getItem('token')

    // Use FormData to support image upload
    const payload = new FormData()
    payload.append('title',        form.title)
    payload.append('category',     form.category)
    payload.append('priority',     form.priority)
    payload.append('description',  form.description)
    payload.append('city',         form.city)
    payload.append('ward',         form.ward)
    payload.append('area',         form.area)
    payload.append('street',       form.street)
    payload.append('landmark',     form.landmark || '')
    payload.append('incidentDate', form.incidentDate || '')
    payload.append('visitTime',    form.visitTime || '')
    payload.append('urgencyNote',  form.urgencyNote || '')
    if (form.image) payload.append('image', form.image)

    const { data } = await axios.post(
      'http://127.0.0.1:5000/api/citizen/complaints',
      payload,
      { headers: { Authorization: `Bearer ${token}` } }
    )

    generatedId.value = data.complaint.id
    showSuccessModal.value = true

  } catch (err) {
    if (err.response?.status === 401) router.push('/login')
    const msg = err.response?.data?.message || 'Submission failed. Please try again.'
    errors.submit = msg
  } finally {
    isSubmitting.value = false
  }
}

const clearForm = () => {
  Object.assign(form, {
    title: '', category: '', priority: 'Medium', description: '',
    city: 'Bhiwandi', ward: '', area: '', street: '', landmark: '',
    incidentDate: '', visitTime: '', urgencyNote: '', terms: false
  })
  removeImage()
  Object.keys(errors).forEach(key => delete errors[key])
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

/* Base fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Modal pop animation */
.fade-enter-active .transform {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.fade-leave-active .transform {
  transition: all 0.2s ease-in;
}
.fade-enter-from .transform {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}
.fade-leave-to .transform {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

/* Custom scrollbar for form view */
main::-webkit-scrollbar {
  width: 6px;
}
main::-webkit-scrollbar-track {
  background: transparent;
}
main::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 20px;
}
</style>