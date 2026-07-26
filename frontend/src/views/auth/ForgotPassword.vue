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
              Recover Your Account
            </h2>
            <p class="text-slate-600 leading-relaxed text-base">
              If you've forgotten your password, don't worry. Enter your registered email address and we'll help you
              reset your password securely.
            </p>
          </div>

          <!-- Feature Cards -->
          <div class="space-y-4 mb-10">
            <div class="flex items-center gap-3 text-slate-700">
              <div class="bg-[#2563EB]/10 p-1.5 rounded-full shrink-0">
                <Check class="w-4 h-4 text-[#2563EB]" />
              </div>
              <span class="font-medium text-sm">Secure Password Recovery</span>
            </div>
            <div class="flex items-center gap-3 text-slate-700">
              <div class="bg-[#2563EB]/10 p-1.5 rounded-full shrink-0">
                <Check class="w-4 h-4 text-[#2563EB]" />
              </div>
              <span class="font-medium text-sm">Protected User Accounts</span>
            </div>
            <div class="flex items-center gap-3 text-slate-700">
              <div class="bg-[#2563EB]/10 p-1.5 rounded-full shrink-0">
                <Check class="w-4 h-4 text-[#2563EB]" />
              </div>
              <span class="font-medium text-sm">Fast Recovery Process</span>
            </div>
            <div class="flex items-center gap-3 text-slate-700">
              <div class="bg-[#2563EB]/10 p-1.5 rounded-full shrink-0">
                <Check class="w-4 h-4 text-[#2563EB]" />
              </div>
              <span class="font-medium text-sm">Trusted Public Service Platform</span>
            </div>
          </div>

          <!-- Illustration Placeholder -->
          <div
            class="w-full h-56 bg-slate-200 rounded-[14px] border-2 border-dashed border-slate-300 flex flex-col items-center justify-center text-slate-500 gap-3">
            <LockKeyhole class="w-8 h-8 text-slate-400" />
            <span class="text-sm font-medium">[ Secure Account Recovery Illustration ]</span>
          </div>
        </div>
      </section>

      <!-- Right Side (Recovery Form / Success State) -->
      <section class="w-full lg:w-7/12 flex items-center justify-center p-4 sm:p-8">
        <div
          class="w-full max-w-md bg-white rounded-[14px] shadow-[0_4px_24px_rgb(0,0,0,0.04)] border border-slate-100 p-8 sm:p-10 transition-shadow duration-300 hover:shadow-[0_8px_30px_rgb(0,0,0,0.06)] relative overflow-hidden">

          <!-- Recovery Form -->
          <div v-if="!isSuccess" class="animate-fade-in">
            <div class="mb-8">
              <h3 class="text-2xl font-bold text-slate-900 mb-2">Forgot Password</h3>
              <p class="text-slate-500 text-sm leading-relaxed">
                Enter your registered email address to receive a one-time password (OTP).
              </p>
            </div>

            <!-- Global error -->
            <div v-if="globalError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {{ globalError }}
            </div>

            <form @submit.prevent="handleSubmit" novalidate class="space-y-6">
              <div>
                <label for="email" class="block text-sm font-medium text-slate-700 mb-1.5">Registered Email
                  Address</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail class="w-5 h-5 text-slate-400" />
                  </div>
                  <input id="email" v-model="email" type="email" :disabled="isLoading" :class="[
                    'w-full pl-10 pr-4 py-2.5 bg-slate-50 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-all',
                    emailError ? 'border-red-500 focus:ring-red-200 bg-red-50/50' : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white',
                    isLoading ? 'opacity-70 cursor-not-allowed' : ''
                  ]" placeholder="name@example.com" />
                </div>
                <span v-if="emailError" class="text-red-500 text-xs mt-1.5 block">{{ emailError }}</span>
              </div>

              <div class="space-y-4 pt-2">
                <button type="submit" :disabled="isLoading"
                  class="w-full bg-[#2563EB] hover:bg-[#1E40AF] text-white font-medium py-2.5 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed shadow-sm hover:shadow">
                  <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
                  <span>{{ isLoading ? 'Sending...' : 'Send OTP' }}</span>
                </button>

                <a href="/login"
                  class="w-full flex items-center justify-center gap-2 bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 hover:text-slate-900 font-medium py-2.5 rounded-lg transition-all duration-200">
                  <ArrowLeft class="w-4 h-4" />
                  <span>Back to Login</span>
                </a>
              </div>
            </form>
          </div>

          <!-- Step 2: OTP + New Password -->
          <div v-else class="animate-fade-in">

            <!-- Final success state -->
            <div v-if="resetSuccess" class="text-center py-6 flex flex-col items-center">
              <div class="w-16 h-16 bg-[#22C55E]/10 rounded-full flex items-center justify-center mb-6">
                <CheckCircle2 class="w-8 h-8 text-[#22C55E]" />
              </div>
              <h3 class="text-2xl font-bold text-slate-900 mb-3">Password Reset!</h3>
              <p class="text-slate-600 text-sm leading-relaxed mb-4">
                Your password has been updated. Redirecting to login...
              </p>
            </div>

            <!-- OTP + reset form -->
            <div v-else>
              <div class="mb-6">
                <h3 class="text-2xl font-bold text-slate-900 mb-2">Enter OTP</h3>
                <p class="text-slate-500 text-sm leading-relaxed">
                  An OTP was sent to <strong>{{ email }}</strong>. Enter it below along with your new password.
                </p>
              </div>

              <form @submit.prevent="handleReset" class="space-y-5" novalidate>

                <!-- OTP field -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-1.5">OTP</label>
                  <input v-model="otp" type="text" maxlength="6" placeholder="6-digit OTP" :class="[
                    'w-full px-4 py-2.5 bg-slate-50 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-all tracking-widest text-center font-mono',
                    otpError ? 'border-red-500 focus:ring-red-200 bg-red-50/50' : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white'
                  ]" />
                  <span v-if="otpError" class="text-red-500 text-xs mt-1.5 block">{{ otpError }}</span>
                </div>

                <!-- New password -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-1.5">New Password</label>
                  <input v-model="newPassword" type="password" placeholder="Min. 8 characters" :class="[
                    'w-full px-4 py-2.5 bg-slate-50 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-all',
                    passwordError ? 'border-red-500 focus:ring-red-200 bg-red-50/50' : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white'
                  ]" />
                </div>

                <!-- Confirm password -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-1.5">Confirm New Password</label>
                  <input v-model="confirmPassword" type="password" placeholder="Repeat new password" :class="[
                    'w-full px-4 py-2.5 bg-slate-50 border rounded-lg text-sm focus:outline-none focus:ring-2 transition-all',
                    passwordError ? 'border-red-500 focus:ring-red-200 bg-red-50/50' : 'border-slate-200 focus:border-[#2563EB] focus:ring-[#2563EB]/20 focus:bg-white'
                  ]" />
                  <span v-if="passwordError" class="text-red-500 text-xs mt-1.5 block">{{ passwordError }}</span>
                </div>

                <div class="space-y-3 pt-1">
                  <button type="submit" :disabled="isResetting"
                    class="w-full bg-[#2563EB] hover:bg-[#1E40AF] text-white font-medium py-2.5 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed shadow-sm">
                    <Loader2 v-if="isResetting" class="w-5 h-5 animate-spin" />
                    <span>{{ isResetting ? 'Resetting...' : 'Reset Password' }}</span>
                  </button>

                  <button type="button" @click="isSuccess = false; globalError = ''"
                    class="w-full flex items-center justify-center gap-2 bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 font-medium py-2.5 rounded-lg transition-all duration-200">
                    <ArrowLeft class="w-4 h-4" />
                    <span>Use different email</span>
                  </button>
                </div>

              </form>
            </div>
          </div>

        </div>
      </section>
    </main>

    <!-- Reusable Footer -->
    <Footer />

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Navbar from '../../components/Navbar.vue' // Adjust path based on your folder structure
import Footer from '../../components/Footer.vue' // Adjust path based on your folder structure
import {
  Check, LockKeyhole, Mail,
  ArrowLeft, Loader2, CheckCircle2
} from 'lucide-vue-next'

// State
const router = useRouter()

// ── Step 1: Email ─────────────────────────────────────────────────────────
const email = ref('')
const emailError = ref('')
const isLoading = ref(false)
const isSuccess = ref(false)   // controls step 1 → step 2 transition
const globalError = ref('')

// ── Step 2: OTP + new password ────────────────────────────────────────────
const otp = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const otpError = ref('')
const passwordError = ref('')
const isResetting = ref(false)
const resetSuccess = ref(false)

// ── Validation helpers ────────────────────────────────────────────────────
const validateEmail = () => {
  emailError.value = ''
  if (!email.value.trim()) {
    emailError.value = 'Email address is required'
    return false
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    emailError.value = 'Please enter a valid email address'
    return false
  }
  return true
}

// ── Step 1: Request OTP ───────────────────────────────────────────────────
const handleSubmit = async () => {
  if (!validateEmail()) return

  isLoading.value = true
  globalError.value = ''

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/forgot-password', {
      email: email.value.trim().toLowerCase()
    })

    if (response.data.success) {
      isSuccess.value = true   // move to step 2

      // Dev only: auto-fill OTP from response so testers don't need email
      if (response.data.dev_otp) {
        otp.value = response.data.dev_otp
      }
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      globalError.value = err.response.data.message
    } else {
      globalError.value = 'Something went wrong. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

// ── Step 2: Verify OTP and reset password ────────────────────────────────
const handleReset = async () => {
  otpError.value = ''
  passwordError.value = ''

  if (!otp.value.trim()) {
    otpError.value = 'OTP is required'
    return
  }
  if (newPassword.value.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = 'Passwords do not match'
    return
  }

  isResetting.value = true

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/reset-password', {
      email: email.value.trim().toLowerCase(),
      otp: otp.value.trim(),
      newPassword: newPassword.value
    })

    if (response.data.success) {
      resetSuccess.value = true
      setTimeout(() => router.push('/login'), 2000)
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      otpError.value = err.response.data.message
    } else {
      otpError.value = 'Something went wrong. Please try again.'
    }
  } finally {
    isResetting.value = false
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
</style>