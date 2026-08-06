<template>
  <div class="min-h-screen flex flex-col bg-[#F8FAFC] font-sans text-slate-800 animate-fade-in">

    <!-- Reusable Navbar -->
    <Navbar />

    <!-- Main Content (Added pt-24 to prevent overlap with the fixed Navbar) -->
    <main class="flex-1 flex max-w-7xl w-full mx-auto pt-24 pb-12">
      <!-- Left Side (Illustration & Branding) -->
      <section class="hidden lg:flex lg:w-5/12 flex-col justify-center px-8 py-8 xl:px-12">
        <div class="max-w-md">
          <div class="mb-8">
            <h1 class="text-4xl font-extrabold text-slate-900 mb-3 leading-tight">
              CivicDesk
            </h1>
            <h2 class="text-xl text-[#2563EB] font-semibold mb-4">
              Create Your Account
            </h2>
            <p class="text-slate-600 leading-relaxed">
              Join CivicDesk to report civic issues, monitor complaint progress, receive updates, and help improve your
              community.
            </p>
          </div>

          <!-- Feature Cards -->
          <div class="space-y-3 mb-10">
            <div v-for="feature in features" :key="feature" class="flex items-center gap-3 text-slate-700">
              <div class="bg-[#2563EB]/10 p-1.5 rounded-full shrink-0">
                <Check class="w-4 h-4 text-[#2563EB]" />
              </div>
              <span class="font-medium text-sm">{{ feature }}</span>
            </div>
          </div>

          <!-- Illustration -->
          <div class="w-full h-56 rounded-[14px] overflow-hidden shadow-lg border border-slate-100">
            <img 
              src="../../assets/register.jpg" 
              alt="CivicDesk Registration" 
              class="w-full h-full object-cover"
            />
          </div>
        </div>
      </section>

      <!-- Right Side (Registration Form) -->
      <section class="w-full lg:w-7/12 flex items-center justify-center p-4 sm:p-8">
        <div
          class="w-full max-w-2xl bg-white rounded-[14px] shadow-[0_4px_24px_rgb(0,0,0,0.04)] border border-slate-100 p-6 sm:p-10 transition-shadow duration-300 hover:shadow-[0_8px_30px_rgb(0,0,0,0.06)]">
          <div class="mb-8">
            <h3 class="text-2xl font-bold text-slate-900 mb-1.5">Create Account</h3>
            <p class="text-slate-500 text-sm">Register to access CivicDesk services.</p>
          </div>

          <!-- Global error banner -->
          <div v-if="globalError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {{ globalError }}
          </div>

          <!-- Global success banner -->
          <div v-if="globalSuccess"
            class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
            {{ globalSuccess }}
          </div>

          <form @submit.prevent="handleRegister" class="grid grid-cols-1 sm:grid-cols-2 gap-x-5 gap-y-5" novalidate>

            <!-- Full Name -->
            <div class="sm:col-span-2">
              <label for="fullName" class="block text-sm font-medium text-slate-700 mb-1.5">Full Name</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User class="w-5 h-5 text-slate-400" />
                </div>
                <input id="fullName" v-model="form.fullName" type="text" :class="inputClasses(errors.fullName)"
                  placeholder="John Doe" />
              </div>
              <span v-if="errors.fullName" class="text-red-500 text-xs mt-1.5 block">{{ errors.fullName }}</span>
            </div>

            <!-- Email Address -->
            <div class="sm:col-span-2">
              <label for="email" class="block text-sm font-medium text-slate-700 mb-1.5">Email Address</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail class="w-5 h-5 text-slate-400" />
                </div>
                <input id="email" v-model="form.email" type="email" :class="inputClasses(errors.email)"
                  placeholder="john@example.com" />
              </div>
              <span v-if="errors.email" class="text-red-500 text-xs mt-1.5 block">{{ errors.email }}</span>
            </div>

            <!-- Mobile Number -->
            <div>
              <label for="mobile" class="block text-sm font-medium text-slate-700 mb-1.5">Mobile Number</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Phone class="w-5 h-5 text-slate-400" />
                </div>
                <input id="mobile" v-model="form.mobile" type="tel" maxlength="10" :class="inputClasses(errors.mobile)"
                  placeholder="9876543210" />
              </div>
              <span v-if="errors.mobile" class="text-red-500 text-xs mt-1.5 block">{{ errors.mobile }}</span>
            </div>

            <!-- Account Role (Dropdown) -->
            <div>
              <label for="role" class="block text-sm font-medium text-slate-700 mb-1.5">Account Role</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Shield class="w-5 h-5 text-slate-400" />
                </div>
                <select id="role" v-model="form.role" :class="[
                  'w-full pl-10 pr-10 py-2.5 bg-slate-50 border rounded-lg text-sm appearance-none focus:outline-none focus:ring-2 transition-all cursor-pointer',
                  errors.role ? 'border-red-500 focus:ring-red-200 bg-red-50/50' : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white',
                  !form.role ? 'text-slate-400' : 'text-slate-900'
                ]">
                  <option value="" disabled selected>Select your role</option>
                  <option value="Citizen">Citizen</option>
                  <option value="Officer">Civic Officer</option>
                  <option value="Worker">Field Worker</option>
                </select>
                <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <ChevronDown class="w-5 h-5 text-slate-400" />
                </div>
              </div>
              <span v-if="errors.role" class="text-red-500 text-xs mt-1.5 block">{{ errors.role }}</span>
            </div>

            <!-- Residential Address -->
            <div class="sm:col-span-2">
              <label for="address" class="block text-sm font-medium text-slate-700 mb-1.5">Residential Address</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 pt-3 pointer-events-none">
                  <MapPin class="w-5 h-5 text-slate-400" />
                </div>
                <textarea id="address" v-model="form.address" rows="2"
                  :class="[inputClasses(errors.address), 'pt-2.5 resize-none']"
                  placeholder="Flat/House No., Street Name, Area"></textarea>
              </div>
              <span v-if="errors.address" class="text-red-500 text-xs mt-1.5 block">{{ errors.address }}</span>
            </div>

            <!-- City -->
            <div>
              <label for="city" class="block text-sm font-medium text-slate-700 mb-1.5">City</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Building class="w-5 h-5 text-slate-400" />
                </div>
                <input id="city" v-model="form.city" type="text" :class="inputClasses(errors.city)"
                  placeholder="City Name" />
              </div>
              <span v-if="errors.city" class="text-red-500 text-xs mt-1.5 block">{{ errors.city }}</span>
            </div>

            <!-- Pincode -->
            <div>
              <label for="pincode" class="block text-sm font-medium text-slate-700 mb-1.5">Pincode</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Hash class="w-5 h-5 text-slate-400" />
                </div>
                <input id="pincode" v-model="form.pincode" type="text" maxlength="6"
                  :class="inputClasses(errors.pincode)" placeholder="123456" />
              </div>
              <span v-if="errors.pincode" class="text-red-500 text-xs mt-1.5 block">{{ errors.pincode }}</span>
            </div>

            <!-- Password -->
            <div>
              <label for="password" class="block text-sm font-medium text-slate-700 mb-1.5">Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock class="w-5 h-5 text-slate-400" />
                </div>
                <input id="password" v-model="form.password" :type="showPassword ? 'text' : 'password'"
                  :class="inputClasses(errors.password)" placeholder="Create a password" />
                <button type="button" @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 transition-colors">
                  <EyeOff v-if="showPassword" class="w-4 h-4" />
                  <Eye v-else class="w-4 h-4" />
                </button>
              </div>

              <!-- Password Strength Indicator -->
              <div v-if="form.password" class="mt-2 flex items-center gap-2">
                <div class="flex-1 flex gap-1 h-1">
                  <div class="flex-1 rounded-full transition-colors duration-300"
                    :class="passwordStrengthScore >= 1 ? strengthColors.bg : 'bg-slate-200'"></div>
                  <div class="flex-1 rounded-full transition-colors duration-300"
                    :class="passwordStrengthScore >= 2 ? strengthColors.bg : 'bg-slate-200'"></div>
                  <div class="flex-1 rounded-full transition-colors duration-300"
                    :class="passwordStrengthScore >= 3 ? strengthColors.bg : 'bg-slate-200'"></div>
                </div>
                <span class="text-[10px] font-medium uppercase tracking-wider" :class="strengthColors.text">
                  {{ passwordStrengthLabel }}
                </span>
              </div>
              <span v-if="errors.password" class="text-red-500 text-xs mt-1.5 block">{{ errors.password }}</span>
            </div>

            <!-- Confirm Password -->
            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-slate-700 mb-1.5">Confirm
                Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock class="w-5 h-5 text-slate-400" />
                </div>
                <input id="confirmPassword" v-model="form.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'" :class="inputClasses(errors.confirmPassword)"
                  placeholder="Confirm password" />
                <button type="button" @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 transition-colors">
                  <EyeOff v-if="showConfirmPassword" class="w-4 h-4" />
                  <Eye v-else class="w-4 h-4" />
                </button>
              </div>
              <span v-if="errors.confirmPassword" class="text-red-500 text-xs mt-1.5 block">{{ errors.confirmPassword
                }}</span>
            </div>

            <!-- Terms & Conditions -->
            <div class="sm:col-span-2 mt-2">
              <label class="flex items-start gap-3 cursor-pointer group">
                <div class="flex items-center h-5">
                  <input v-model="form.terms" type="checkbox"
                    class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB] transition-colors" />
                </div>
                <span class="text-sm text-slate-600 group-hover:text-slate-900 transition-colors">
                  I agree to the <a href="#" class="text-[#2563EB] hover:underline">Terms of Service</a> and <a href="#"
                    class="text-[#2563EB] hover:underline">Privacy Policy</a>.
                </span>
              </label>
              <span v-if="errors.terms" class="text-red-500 text-xs mt-1.5 block">{{ errors.terms }}</span>
            </div>

            <!-- Actions -->
            <div class="sm:col-span-2 mt-4 space-y-4">
              <button type="submit" :disabled="isLoading"
                class="w-full bg-[#2563EB] hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed shadow-sm hover:shadow">
                <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
                <span>{{ isLoading ? 'Creating Account...' : 'Create Account' }}</span>
              </button>

              <div class="text-center">
                <router-link to="/login"
                  class="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
                  Already have an account? <span class="text-[#2563EB] hover:underline">Login</span>
                </router-link>
              </div>
            </div>
          </form>
        </div>
      </section>
    </main>

    <!-- Reusable Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../../components/Navbar.vue' // Adjust path based on your folder structure
import Footer from '../../components/Footer.vue' // Adjust path based on your folder structure
import {
  User, Mail, Phone, MapPin, Building, Hash, Lock,
  Eye, EyeOff, Shield, Check, Loader2, ChevronDown
} from 'lucide-vue-next'
import axios from "axios"

// --- State ---
const features = [
  'Report Civic Complaints',
  'Track Complaint Progress',
  'Receive Status Notifications',
  'Faster Communication with Authorities'
]

const form = reactive({
  fullName: '',
  email: '',
  mobile: '',
  address: '',
  city: '',
  pincode: '',
  password: '',
  confirmPassword: '',
  role: '', // Set empty to force selection
  terms: false
})

const errors = reactive({})
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const globalError = ref('')
const globalSuccess = ref('')
const router = useRouter()

// --- Computed & Helpers ---

// Dynamic classes for inputs to handle error state styling
const inputClasses = (hasError) => [
  'w-full pl-10 pr-4 py-2.5 bg-slate-50 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-all',
  hasError
    ? 'border-red-500 focus:ring-red-200 bg-red-50/50'
    : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white'
]

// Password Strength Logic
const passwordStrengthScore = computed(() => {
  const p = form.password
  if (!p) return 0
  let score = 0
  if (p.length >= 8) score += 1
  if (/(?=.*[a-z])(?=.*[A-Z])/.test(p)) score += 1
  if (/(?=.*\d)/.test(p)) score += 1
  return score
})

const passwordStrengthLabel = computed(() => {
  switch (passwordStrengthScore.value) {
    case 1: return 'Weak'
    case 2: return 'Medium'
    case 3: return 'Strong'
    default: return ''
  }
})

const strengthColors = computed(() => {
  switch (passwordStrengthScore.value) {
    case 1: return { bg: 'bg-red-500', text: 'text-red-600' }
    case 2: return { bg: 'bg-yellow-500', text: 'text-yellow-600' }
    case 3: return { bg: 'bg-[#22C55E]', text: 'text-[#22C55E]' } // Green
    default: return { bg: 'bg-slate-200', text: 'text-slate-400' }
  }
})

// --- Validation Logic ---
const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  let isValid = true

  // Name validation (Min 3 chars, alphabets & spaces)
  if (!form.fullName.trim()) {
    errors.fullName = 'Full Name is required'
    isValid = false
  } else if (!/^[A-Za-z\s]{3,}$/.test(form.fullName)) {
    errors.fullName = 'Name must be at least 3 characters and contain only letters'
    isValid = false
  }

  // Email validation
  if (!form.email) {
    errors.email = 'Email address is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  // Mobile validation (10 digits)
  if (!form.mobile) {
    errors.mobile = 'Mobile number is required'
    isValid = false
  } else if (!/^\d{10}$/.test(form.mobile)) {
    errors.mobile = 'Mobile number must be exactly 10 digits'
    isValid = false
  }

  // Role validation
  if (!form.role) {
    errors.role = 'Please select an account role'
    isValid = false
  }

  // Address & City
  if (!form.address.trim()) {
    errors.address = 'Residential address is required'
    isValid = false
  }
  if (!form.city.trim()) {
    errors.city = 'City is required'
    isValid = false
  }

  // Pincode (6 digits)
  if (!form.pincode) {
    errors.pincode = 'Pincode is required'
    isValid = false
  } else if (!/^\d{6}$/.test(form.pincode)) {
    errors.pincode = 'Pincode must be exactly 6 digits'
    isValid = false
  }

  // Password validation (Min 8, 1 uppercase, 1 lowercase, 1 number)
  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\W]{8,}$/.test(form.password)) {
    errors.password = 'Must be at least 8 chars with uppercase, lowercase, and number'
    isValid = false
  }

  // Confirm Password
  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  // Terms
  if (!form.terms) {
    errors.terms = 'You must agree to the Terms of Service'
    isValid = false
  }

  return isValid
}

// --- Submit Handler ---
const handleRegister = async () => {
  if (!validateForm()) return

  isLoading.value = true
  globalError.value = ''
  globalSuccess.value = ''

  try {
    const response = await axios.post(
      'http://127.0.0.1:5000/api/register',
      {
        fullName: form.fullName,
        email: form.email,
        mobile: form.mobile,
        address: form.address,
        city: form.city,
        pincode: form.pincode,
        password: form.password,
        role: form.role,
      }
    )

    if (response.data.success) {
      globalSuccess.value = 'Registration successful! Redirecting to login...'
      setTimeout(() => router.push('/login'), 1500)
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      globalError.value = err.response.data.message
    } else {
      globalError.value = 'An unexpected error occurred. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
.animate-fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
textarea::-webkit-scrollbar { width: 6px; }
textarea::-webkit-scrollbar-track { background: transparent; }
textarea::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 20px; }
</style>