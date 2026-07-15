<template>
  <div class="min-h-screen flex flex-col bg-[#F8FAFC] font-sans text-slate-800 animate-fade-in">
    
    <!-- Reusable Navbar -->
    <Navbar />

    <!-- Main Content -->
    <main class="flex-1 flex max-w-7xl w-full mx-auto pt-24 pb-12">
      <!-- Left Side (Branding & Features) -->
      <section class="hidden lg:flex lg:w-1/2 flex-col justify-center px-12 py-8">
        <div class="max-w-lg">
          <div class="mb-8">
            <h1 class="text-4xl font-extrabold text-slate-900 mb-4 leading-tight">
              CivicDesk
            </h1>
            <h2 class="text-xl text-[#2563EB] font-semibold mb-4">
              A Civic Complaint Management Platform
            </h2>
            <p class="text-slate-600 leading-relaxed text-lg">
              Report civic issues, track complaint progress, and stay connected with your local authorities through one secure platform.
            </p>
          </div>

          <!-- Feature Cards -->
          <div class="space-y-4 mb-10">
            <div v-for="feature in features" :key="feature" class="flex items-center gap-3 text-slate-700 bg-white px-4 py-3 rounded-xl shadow-sm border border-slate-100">
              <div class="bg-[#22C55E]/10 p-1 rounded-full">
                <Check class="w-4 h-4 text-[#22C55E]" />
              </div>
              <span class="font-medium">{{ feature }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Right Side (Login Form) -->
      <section class="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12">
        <div class="w-full max-w-md bg-white rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 p-8 sm:p-10">
          <div class="mb-8 text-center lg:text-left">
            <h3 class="text-2xl font-bold text-slate-900 mb-2">Welcome Back</h3>
            <p class="text-slate-500 text-sm">Login to continue using CivicDesk.</p>
          </div>

          <!-- Global Error Alert from API -->
          <div v-if="globalError" class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-r-lg">
            <div class="flex items-center">
              <div class="ml-3">
                <p class="text-sm text-red-700 font-medium">{{ globalError }}</p>
              </div>
            </div>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-5" novalidate>
            <!-- Email Field -->
            <div>
              <label for="email" class="block text-sm font-medium text-slate-700 mb-1.5">Email Address</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail class="w-5 h-5 text-slate-400" />
                </div>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  :class="[
                    'w-full pl-10 pr-4 py-2.5 bg-slate-50 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-all',
                    errors.email ? 'border-red-500 focus:ring-red-200 bg-red-50/50' : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white'
                  ]"
                  placeholder="Enter your email"
                  aria-label="Email Address"
                />
              </div>
              <span v-if="errors.email" class="text-red-500 text-xs mt-1.5 block">{{ errors.email }}</span>
            </div>

            <!-- Password Field -->
            <div>
              <label for="password" class="block text-sm font-medium text-slate-700 mb-1.5">Password</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock class="w-5 h-5 text-slate-400" />
                </div>
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  :class="[
                    'w-full pl-10 pr-10 py-2.5 bg-slate-50 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-all',
                    errors.password ? 'border-red-500 focus:ring-red-200 bg-red-50/50' : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white'
                  ]"
                  placeholder="Enter your password"
                  aria-label="Password"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 transition-colors"
                  aria-label="Toggle password visibility"
                >
                  <EyeOff v-if="showPassword" class="w-5 h-5" />
                  <Eye v-else class="w-5 h-5" />
                </button>
              </div>
              <span v-if="errors.password" class="text-red-500 text-xs mt-1.5 block">{{ errors.password }}</span>
            </div>

            <!-- Options Row -->
            <div class="flex items-center justify-between mt-2">
              <label class="flex items-center gap-2 cursor-pointer group">
                <input
                  v-model="form.rememberMe"
                  type="checkbox"
                  class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB] transition-colors"
                />
                <span class="text-sm text-slate-600 group-hover:text-slate-900 transition-colors">Remember me</span>
              </label>
              <router-link to="/forgot-password" class="text-sm font-medium text-[#2563EB] hover:underline">Forgot Password?</router-link>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="isLoading"
              class="w-full bg-[#2563EB] hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed shadow-sm hover:shadow"
            >
              <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
              <span>{{ isLoading ? 'Signing in...' : 'Login' }}</span>
            </button>
          </form>

          <!-- Divider -->
          <div class="mt-8 mb-6 flex items-center">
            <div class="flex-1 border-t border-slate-200"></div>
            <span class="px-4 text-xs font-medium text-slate-400 uppercase tracking-wider">OR</span>
            <div class="flex-1 border-t border-slate-200"></div>
          </div>

          <!-- Register Link -->
          <div class="text-center">
            <p class="text-sm text-slate-600 mb-4">Don't have an account?</p>
            <router-link to="/register" class="w-full flex justify-center bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 hover:text-slate-900 font-medium py-2.5 rounded-lg transition-all duration-200">
              Register
            </router-link>
          </div>
        </div>
      </section>
    </main>

    <!-- Reusable Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Navbar from '../../components/Navbar.vue' // Adjust path based on your folder structure
import Footer from '../../components/Footer.vue' // Adjust path based on your folder structure
import { 
  Mail, Lock, Eye, EyeOff, Loader2, Check
} from 'lucide-vue-next'

const router = useRouter()

const features = [
  'Report Complaints',
  'Track Complaint Status',
  'Real-time Updates',
  'Faster Resolution'
]

const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

const errors = reactive({
  email: '',
  password: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const globalError = ref('')

const validateForm = () => {
  let isValid = true
  
  errors.email = ''
  errors.password = ''
  globalError.value = ''

  if (!form.email) {
    errors.email = 'Email address is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  }

  return isValid
}

const handleLogin = async () => {
  if (!validateForm()) return

  isLoading.value = true
  globalError.value = ''
  
  try {
    // Replace the URL with your Flask API's local development URL
    const response = await axios.post('http://127.0.0.1:5000/api/login', {
      email: form.email,
      password: form.password
    })

    if (response.data.success) {
      const { access_token, refresh_token, user } = response.data

      localStorage.setItem('token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify(user))

      // Direct users to their specific dashboard based on their role
      switch (user.role.toLowerCase()) {
        case 'administrator':
        case 'admin':
          router.push('/admin/dashboard')
          break
        case 'officer':
          router.push('/officer/dashboard')
          break
        case 'worker':
          router.push('/worker/dashboard')
          break
        case 'citizen':
        default:
          router.push('/citizen/dashboard')
          break
      }
    }
  } catch (error) {
    // Catch API errors (400, 401, 403) and display the backend message
    if (error.response && error.response.data && error.response.data.message) {
      globalError.value = error.response.data.message
    } else {
      globalError.value = 'An unexpected error occurred. Please try again later.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>