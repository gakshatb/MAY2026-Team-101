<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    <Sidebar :userRole="userRole" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      <DashboardNavbar :userRole="userRole" pageTitle="Complaint Feedback" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-7xl mx-auto space-y-6">
          
          <!-- Breadcrumb & Header -->
          <div>
            <nav class="flex text-sm text-slate-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer">Dashboard</span>
              <span class="mx-2">›</span>
              <span class="hover:text-[#2563EB] cursor-pointer">My Complaints</span>
              <span class="mx-2">›</span>
              <span class="hover:text-[#2563EB] cursor-pointer">Complaint Details</span>
              <span class="mx-2">›</span>
              <span class="text-slate-900">Feedback</span>
            </nav>
            <h1 class="text-2xl font-bold text-slate-900">Complaint Feedback</h1>
            <p class="text-slate-500 mt-1">Share your experience to help us improve civic services.</p>
          </div>

          <!-- Main Layout Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <!-- Left Column: Form Area -->
            <div class="lg:col-span-8 space-y-6">
              
              <!-- Complaint Summary Card -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6 flex flex-col sm:flex-row gap-6 items-start">
                <div class="w-full sm:w-32 h-24 rounded-lg overflow-hidden shrink-0 border border-slate-200">
                  <img src="https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&q=80&w=400" alt="Complaint Thumbnail" class="w-full h-full object-cover" />
                </div>
                <div class="flex-1">
                  <div class="flex flex-wrap items-start justify-between gap-3 mb-2">
                    <div>
                      <div class="flex items-center gap-3 mb-1">
                        <span class="text-xs font-bold text-slate-500 bg-slate-100 px-2 py-1 rounded tracking-wide uppercase">CMP-2026-00125</span>
                        <span class="text-xs font-bold text-green-700 bg-green-100 px-2 py-1 rounded flex items-center gap-1">
                          <CheckCircle class="w-3 h-3" /> Resolved
                        </span>
                      </div>
                      <h3 class="text-lg font-bold text-slate-900">Deep Pothole on Main Street</h3>
                    </div>
                    <button class="text-sm font-medium text-[#2563EB] hover:underline whitespace-nowrap">View Details</button>
                  </div>
                  
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-y-2 gap-x-6 text-sm mt-4">
                    <div class="flex items-center gap-2 text-slate-600">
                      <MapPin class="w-4 h-4 text-slate-400 shrink-0" />
                      <span class="truncate">MG Road, Near Central Plaza</span>
                    </div>
                    <div class="flex items-center gap-2 text-slate-600">
                      <Clock class="w-4 h-4 text-slate-400 shrink-0" />
                      <span>Resolved: Jul 08, 2026</span>
                    </div>
                    <div class="flex items-center gap-2 text-slate-600">
                      <Building class="w-4 h-4 text-slate-400 shrink-0" />
                      <span>Roads & Infrastructure</span>
                    </div>
                    <div class="flex items-center gap-2 text-slate-600">
                      <User class="w-4 h-4 text-slate-400 shrink-0" />
                      <span>Worker: Rajesh K.</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Feedback Form -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6 sm:p-8">
                <div class="mb-8">
                  <h2 class="text-xl font-bold text-slate-900">Rate Your Experience</h2>
                  <p class="text-slate-500 mt-1 text-sm">Your feedback helps us improve the quality of civic services.</p>
                </div>

                <form @submit.prevent="submitFeedback" class="space-y-10">
                  
                  <!-- Overall Rating -->
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-3">Overall Rating <span class="text-red-500">*</span></label>
                    <div class="flex items-center gap-4">
                      <div class="flex gap-1.5">
                        <button 
                          v-for="i in 5" :key="i" 
                          type="button"
                          @mouseover="hoverOverall = i" 
                          @mouseleave="hoverOverall = 0"
                          @click="form.overallRating = i"
                          class="focus:outline-none transition-transform hover:scale-110"
                        >
                          <Star 
                            :class="['w-10 h-10 transition-colors duration-200', i <= (hoverOverall || form.overallRating) ? 'text-amber-400 fill-amber-400' : 'text-slate-200']" 
                          />
                        </button>
                      </div>
                      <span class="text-sm font-bold text-slate-600 w-24">{{ ratingText }}</span>
                    </div>
                    <p v-if="errors.overallRating" class="text-red-500 text-xs mt-2">{{ errors.overallRating }}</p>
                  </div>

                  <!-- Detailed Service Ratings -->
                  <div class="bg-slate-50 p-6 rounded-xl border border-slate-100 space-y-4">
                    <div v-for="(metric, index) in serviceRatings" :key="metric.id" class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <span class="text-sm font-medium text-slate-700">{{ metric.label }}</span>
                      <div class="flex gap-1">
                        <button 
                          v-for="i in 5" :key="`sr-${index}-${i}`" 
                          type="button"
                          @mouseover="metric.hover = i" 
                          @mouseleave="metric.hover = 0"
                          @click="metric.rating = i"
                          class="focus:outline-none"
                        >
                          <Star 
                            :class="['w-6 h-6 transition-colors', i <= (metric.hover || metric.rating) ? 'text-amber-400 fill-amber-400' : 'text-slate-300']" 
                          />
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Categories Checkboxes -->
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-3">What went well? (Select all that apply)</label>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <label v-for="cat in feedbackCategories" :key="cat" class="flex items-center gap-3 cursor-pointer group">
                        <div class="relative flex items-center justify-center">
                          <input type="checkbox" :value="cat" v-model="form.categories" class="peer sr-only" />
                          <div class="w-5 h-5 border-2 border-slate-300 rounded peer-checked:bg-[#2563EB] peer-checked:border-[#2563EB] transition-colors"></div>
                          <Check class="w-3.5 h-3.5 text-white absolute opacity-0 peer-checked:opacity-100 transition-opacity" />
                        </div>
                        <span class="text-sm text-slate-600 group-hover:text-slate-900 transition-colors">{{ cat }}</span>
                      </label>
                    </div>
                  </div>

                  <!-- Comment Textarea -->
                  <div>
                    <div class="flex justify-between mb-1.5">
                      <label class="block text-sm font-medium text-slate-700">Tell us about your experience <span class="text-red-500">*</span></label>
                      <span :class="['text-xs', form.comment.length > 1000 ? 'text-red-500' : 'text-slate-400']">{{ form.comment.length }}/1000</span>
                    </div>
                    <textarea 
                      v-model="form.comment" 
                      rows="4" 
                      placeholder="Describe how the issue was resolved..."
                      :class="['w-full px-4 py-3 rounded-lg border text-sm transition-all focus:outline-none focus:ring-2', errors.comment ? 'border-red-500 bg-red-50/50 focus:ring-red-200' : 'border-slate-300 focus:border-[#2563EB] focus:ring-[#2563EB]/20']"
                    ></textarea>
                    <p v-if="errors.comment" class="text-red-500 text-xs mt-1">{{ errors.comment }}</p>
                  </div>

                  <!-- Improvement Textarea -->
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1.5">What could be improved? <span class="text-slate-400 font-normal">(Optional)</span></label>
                    <textarea 
                      v-model="form.improvement" 
                      rows="2" 
                      placeholder="Any suggestions for our team?"
                      class="w-full px-4 py-3 rounded-lg border border-slate-300 text-sm transition-all focus:outline-none focus:ring-2 focus:border-[#2563EB] focus:ring-[#2563EB]/20"
                    ></textarea>
                  </div>

                  <!-- Recommendation Radio -->
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-3">Would you recommend CivicDesk to others?</label>
                    <div class="flex gap-6">
                      <label v-for="opt in ['Yes', 'No', 'Maybe']" :key="opt" class="flex items-center gap-2 cursor-pointer">
                        <input type="radio" :value="opt" v-model="form.recommend" class="w-4 h-4 text-[#2563EB] border-slate-300 focus:ring-[#2563EB]" />
                        <span class="text-sm text-slate-700">{{ opt }}</span>
                      </label>
                    </div>
                  </div>

                  <!-- Optional Photo Upload -->
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1.5">Upload Photo of Completed Work <span class="text-slate-400 font-normal">(Optional)</span></label>
                    
                    <div v-if="!form.photoPreview" class="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:bg-slate-50 transition-colors relative cursor-pointer group">
                      <input type="file" accept=".jpg, .jpeg, .png" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" @change="handleFileUpload" />
                      <div class="w-12 h-12 bg-blue-50 text-[#2563EB] rounded-full flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform">
                        <Camera class="w-6 h-6" />
                      </div>
                      <p class="text-sm font-medium text-slate-700">Click to upload or drag and drop</p>
                      <p class="text-xs text-slate-500 mt-1">SVG, PNG, JPG or GIF (MAX. 5MB)</p>
                    </div>
                    
                    <div v-else class="relative w-40 h-40 rounded-xl border border-slate-200 overflow-hidden group">
                      <img :src="form.photoPreview" alt="Preview" class="w-full h-full object-cover" />
                      <div class="absolute inset-0 bg-slate-900/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <button type="button" @click="form.photoPreview = null" class="bg-red-500 text-white p-2 rounded-lg hover:bg-red-600 transition-colors">
                          <Trash2 class="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Footer Checks -->
                  <div class="space-y-4 pt-6 border-t border-slate-100">
                    <label class="flex items-center gap-3 cursor-pointer">
                      <input type="checkbox" v-model="form.anonymous" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <span class="text-sm text-slate-700">Submit feedback anonymously</span>
                    </label>
                    <label class="flex items-start gap-3 cursor-pointer">
                      <input type="checkbox" v-model="form.agreed" class="w-4 h-4 mt-0.5 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <div class="flex flex-col">
                        <span class="text-sm text-slate-700">I confirm that this feedback is based on my actual experience. <span class="text-red-500">*</span></span>
                        <span v-if="errors.agreed" class="text-red-500 text-xs mt-1">{{ errors.agreed }}</span>
                      </div>
                    </label>
                  </div>

                  <!-- Actions -->
                  <div class="flex items-center justify-end gap-4 pt-4">
                    <button type="button" class="px-6 py-3 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors">
                      Cancel
                    </button>
                    <button 
                      type="submit" 
                      :disabled="isSubmitting"
                      class="px-8 py-3 text-sm font-medium text-white bg-[#2563EB] rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center gap-2 disabled:opacity-70"
                    >
                      <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                      Submit Feedback
                    </button>
                  </div>

                </form>
              </div>
            </div>

            <!-- Right Column: Context & History -->
            <div class="lg:col-span-4 space-y-6">
              
              <!-- Quick Tips -->
              <div class="bg-blue-50 rounded-[14px] p-6 border border-blue-100">
                <h3 class="font-bold text-[#1E40AF] flex items-center gap-2 mb-4">
                  <Lightbulb class="w-5 h-5" /> Quick Tips
                </h3>
                <ul class="space-y-3">
                  <li class="flex items-start gap-2 text-sm text-[#1E40AF]/80">
                    <CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-[#2563EB]" /> Be honest and specific about your experience.
                  </li>
                  <li class="flex items-start gap-2 text-sm text-[#1E40AF]/80">
                    <CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-[#2563EB]" /> Mention what went well to encourage workers.
                  </li>
                  <li class="flex items-start gap-2 text-sm text-[#1E40AF]/80">
                    <CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-[#2563EB]" /> Suggest clear improvements if needed.
                  </li>
                  <li class="flex items-start gap-2 text-sm text-[#1E40AF]/80">
                    <CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-[#2563EB]" /> Your feedback directly helps improve public services.
                  </li>
                </ul>
              </div>

              <!-- Previous Feedback -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 mb-4">Your Past Feedback</h3>
                <div class="space-y-4">
                  <div v-for="fb in pastFeedback" :key="fb.id" class="p-4 border border-slate-100 rounded-xl bg-slate-50/50">
                    <div class="flex justify-between items-start mb-2">
                      <div class="flex gap-0.5">
                        <Star v-for="s in 5" :key="s" :class="['w-3.5 h-3.5', s <= fb.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-300']" />
                      </div>
                      <span class="text-xs text-slate-400 font-medium">{{ fb.date }}</span>
                    </div>
                    <p class="text-sm text-slate-600 mb-2 line-clamp-2">"{{ fb.comment }}"</p>
                    <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wide">CMP-2026-{{ fb.id }}</p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div class="bg-white p-8 rounded-2xl max-w-sm w-full text-center shadow-2xl transform scale-100 transition-all">
        <div class="w-20 h-20 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-6">
          <ThumbsUp class="w-10 h-10" />
        </div>
        <h3 class="text-2xl font-bold text-slate-900 mb-2">Thank You!</h3>
        <p class="text-slate-600 mb-4 text-sm leading-relaxed">Your feedback has been submitted successfully and will help us improve CivicDesk.</p>
        <div class="flex justify-center gap-1 mb-8">
          <Star v-for="i in form.overallRating" :key="i" class="w-6 h-6 text-amber-400 fill-amber-400" />
        </div>
        <div class="space-y-3">
          <button @click="showSuccess = false" class="w-full bg-[#2563EB] hover:bg-[#1E40AF] text-white py-3 rounded-lg font-bold transition-colors">Return to Dashboard</button>
          <button @click="showSuccess = false" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-700 py-3 rounded-lg font-bold transition-colors">View My Complaints</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Star, CheckCircle, MapPin, Clock, Building, User, 
  Check, Camera, Trash2, Lightbulb, ThumbsUp
} from 'lucide-vue-next'

const userRole = ref('Citizen')
const isSidebarOpen = ref(false)
const isSubmitting = ref(false)
const showSuccess = ref(false)

// State
const hoverOverall = ref(0)
const form = reactive({
  overallRating: 0,
  categories: [],
  comment: '',
  improvement: '',
  recommend: 'Yes',
  photoPreview: null,
  anonymous: false,
  agreed: false
})
const errors = reactive({})

const serviceRatings = reactive([
  { id: 'quality', label: 'Quality of Work', rating: 0, hover: 0 },
  { id: 'response', label: 'Response Time', rating: 0, hover: 0 },
  { id: 'communication', label: 'Communication', rating: 0, hover: 0 },
  { id: 'resolution', label: 'Complaint Resolution', rating: 0, hover: 0 },
  { id: 'professionalism', label: 'Professional Behaviour', rating: 0, hover: 0 },
])

const feedbackCategories = [
  'Work completed properly', 'Issue resolved permanently', 
  'Good communication', 'Quick response', 
  'Satisfied with service', 'Clean work', 'Workers were professional'
]

const pastFeedback = [
  { id: '00110', rating: 5, date: 'Jun 12, 2026', comment: 'Very quick response. The streetlight was fixed within 24 hours.' },
  { id: '00085', rating: 4, date: 'May 04, 2026', comment: 'Good work, but the workers left some debris behind.' }
]

const ratingText = computed(() => {
  const val = hoverOverall.value || form.overallRating
  const texts = ['Select Rating', 'Very Poor', 'Poor', 'Average', 'Good', 'Excellent']
  return texts[val]
})

// Methods
const handleFileUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.photoPreview = URL.createObjectURL(file)
  }
}

const validate = () => {
  Object.keys(errors).forEach(k => delete errors[k])
  let isValid = true

  if (form.overallRating === 0) {
    errors.overallRating = 'Please provide an overall rating.'
    isValid = false
  }
  if (form.comment.length < 20) {
    errors.comment = 'Please write at least 20 characters.'
    isValid = false
  }
  if (form.comment.length > 1000) {
    errors.comment = 'Comment cannot exceed 1000 characters.'
    isValid = false
  }
  if (!form.agreed) {
    errors.agreed = 'You must confirm your feedback is genuine.'
    isValid = false
  }

  return isValid
}

const submitFeedback = async () => {
  if (!validate()) return

  isSubmitting.value = true
  await new Promise(resolve => setTimeout(resolve, 1500))
  isSubmitting.value = false
  showSuccess.value = true
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>