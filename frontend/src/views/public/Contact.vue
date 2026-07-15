<template>
  <div class="min-h-screen bg-[#F8FAFC] font-sans text-slate-800">
    <Navbar />

    <main class="pt-20">
      <!-- Hero Section -->
      <section class="py-20 px-6 bg-white border-b border-slate-100">
        <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-12">
          <div class="flex-1 text-center lg:text-left">
            <h1 class="text-4xl lg:text-5xl font-extrabold text-slate-900 leading-tight mb-6">Contact CivicDesk</h1>
            <p class="text-lg text-slate-600 mb-8 max-w-xl lg:mx-0 mx-auto leading-relaxed">
              We're here to help. Whether you have a question, feedback, or need technical assistance, feel free to reach out to us.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <a href="#contact-form" class="bg-[#2563EB] hover:bg-[#1E40AF] text-white px-8 py-3.5 rounded-lg font-semibold transition-all shadow-md">Send Message</a>
              <router-link to="/faq" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-8 py-3.5 rounded-lg font-semibold transition-all">View FAQs</router-link>
            </div>
          </div>
          <div class="flex-1 w-full h-80 bg-slate-50 rounded-2xl flex items-center justify-center border-2 border-dashed border-slate-200">
            <span class="text-slate-400 font-medium">[ Hero Illustration: Support & Help ]</span>
          </div>
        </div>
      </section>

      <!-- Contact Info Cards -->
      <section class="py-20 px-6 max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="info in contactInfo" :key="info.title" class="bg-white p-6 rounded-[14px] border border-slate-100 shadow-sm hover:shadow-md transition-all">
            <div class="w-12 h-12 bg-blue-50 text-[#2563EB] rounded-xl flex items-center justify-center mb-4">
              <component :is="info.icon" class="w-6 h-6" />
            </div>
            <h3 class="font-bold text-slate-900 mb-1">{{ info.title }}</h3>
            <p class="text-sm font-semibold text-[#2563EB] mb-2">{{ info.value }}</p>
            <p class="text-xs text-slate-500">{{ info.desc }}</p>
          </div>
        </div>
      </section>

      <!-- Form Section -->
      <section id="contact-form" class="py-20 px-6 bg-white">
        <div class="max-w-4xl mx-auto">
          <div class="bg-[#F8FAFC] p-8 md:p-12 rounded-[14px] border border-slate-100">
            <h2 class="text-2xl font-bold text-slate-900 mb-2">Send Us a Message</h2>
            <p class="text-slate-600 mb-8">We'll get back to you as soon as possible.</p>
            
            <!-- Global API error banner -->
            <div v-if="globalError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {{ globalError }}
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-1.5">Full Name <span class="text-red-500">*</span></label>
                  <input v-model="form.name" type="text" :class="inputClasses(errors.name)" placeholder="John Doe" />
                  <p v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-1.5">Email Address <span class="text-red-500">*</span></label>
                  <input v-model="form.email" type="email" :class="inputClasses(errors.email)" placeholder="john@example.com" />
                  <p v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</p>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1.5">Subject</label>
                <select v-model="form.subject" :class="inputClasses(false)">
                  <option>General Inquiry</option>
                  <option>Technical Support</option>
                  <option>Feedback</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1.5">Message <span class="text-red-500">*</span></label>
                <textarea v-model="form.message" rows="5" :class="inputClasses(errors.message)" placeholder="Describe your message..."></textarea>
                <p v-if="errors.message" class="text-red-500 text-xs mt-1">{{ errors.message }}</p>
              </div>

              <div class="flex items-center gap-2">
                <input v-model="form.agreed" type="checkbox" id="terms" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                <label for="terms" class="text-sm text-slate-600">I agree that my information may be used to respond to my inquiry. <span class="text-red-500">*</span></label>
              </div>
              <p v-if="errors.agreed" class="text-red-500 text-xs mt-1">{{ errors.agreed }}</p>

              <button type="submit" :disabled="isSubmitting" class="w-full bg-[#2563EB] text-white py-3 rounded-lg font-bold hover:bg-[#1E40AF] transition-all disabled:opacity-50">
                {{ isSubmitting ? 'Sending...' : 'Send Message' }}
              </button>
            </form>
          </div>
        </div>
      </section>

      <!-- Team Section -->
      <section class="py-20 px-6 max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-slate-900 text-center mb-12">Meet The Core Team</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
          <div v-for="member in team" :key="member.name" class="bg-white p-6 rounded-[14px] border border-slate-100 text-center hover:shadow-md transition-all">
            <div class="w-20 h-20 bg-slate-100 rounded-full mx-auto mb-4 border-2 border-slate-50"></div>
            <h4 class="font-bold text-slate-900">{{ member.name }}</h4>
            <p class="text-sm text-[#2563EB] font-medium">{{ member.role }}</p>
          </div>
        </div>
      </section>
    </main>

    <!-- Success Modal -->
    <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-slate-900/40 backdrop-blur-sm">
      <div class="bg-white p-8 rounded-[14px] max-w-sm w-full text-center">
        <div class="w-16 h-16 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle class="w-8 h-8" />
        </div>
        <h3 class="text-xl font-bold text-slate-900 mb-2">Thank you!</h3>
        <p class="text-slate-600 mb-6">We have received your message and will respond soon.</p>
        <button @click="showSuccess = false" class="w-full bg-[#2563EB] text-white py-2 rounded-lg font-bold">Return Home</button>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { Mail, Phone, MapPin, Clock, CheckCircle } from 'lucide-vue-next'
import axios from 'axios'

const isSubmitting = ref(false)
const showSuccess = ref(false)
const globalError = ref('')
const form = reactive({ name: '', email: '', subject: 'General Inquiry', message: '', agreed: false })
const errors = reactive({})

const contactInfo = [
  { title: 'Email', value: 'support@civicdesk.in', desc: 'For technical support', icon: Mail },
  { title: 'Phone', value: '+91 98765 43210', desc: 'Mon - Fri, 9am - 6pm', icon: Phone },
  { title: 'Office', value: 'Bhiwandi, Maharashtra', desc: 'CivicDesk Project Office', icon: MapPin },
  { title: 'Working Hours', value: 'Mon - Fri', desc: '9:00 AM - 6:00 PM', icon: Clock }
]

const team = [
  { name: 'Student A', role: 'Project Manager' },
  { name: 'Student B', role: 'Frontend Dev' },
  { name: 'Student C', role: 'Backend Dev' },
  { name: 'Student D', role: 'Database' },
  { name: 'Student E', role: 'QA & Testing' }
]

const inputClasses = (hasError) => [
  'w-full px-4 py-3 rounded-lg border transition-all',
  hasError ? 'border-red-500 bg-red-50/50' : 'border-slate-300 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB]'
]

const handleSubmit = async () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  globalError.value = ''

  // Client-side validation (mirrors backend rules)
  if (form.name.length < 3)     errors.name    = 'Minimum 3 characters required'
  if (!form.email.includes('@')) errors.email   = 'Valid email required'
  if (form.message.length < 20)  errors.message = 'Minimum 20 characters required'
  if (!form.agreed)              errors.agreed  = 'You must agree to the terms'

  if (Object.keys(errors).length > 0) return

  isSubmitting.value = true

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/contact', {
      name:    form.name.trim(),
      email:   form.email.trim().toLowerCase(),
      subject: form.subject.trim(),
      message: form.message.trim()
    })

    if (response.data.success) {
      showSuccess.value = true
      Object.assign(form, { name: '', email: '', subject: 'General Inquiry', message: '', agreed: false })
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      globalError.value = err.response.data.message
    } else {
      globalError.value = 'Something went wrong. Please try again later.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>