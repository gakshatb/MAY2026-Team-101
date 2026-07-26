<template>
  <div class="min-h-screen bg-[#F8FAFC] font-sans text-slate-800">
    <Navbar />

    <main>
      <!-- Hero Section -->
      <section class="pt-32 pb-20 px-6 bg-white">
        <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-12">
          <div class="flex-1 text-center lg:text-left">
            <h1 class="text-4xl lg:text-6xl font-extrabold text-slate-900 leading-tight mb-6">How CivicDesk Works</h1>
            <p class="text-lg text-slate-600 mb-8 max-w-xl lg:mx-0 mx-auto leading-relaxed">
              From reporting a civic issue to its successful resolution, CivicDesk keeps every step simple, transparent,
              and easy to track.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <router-link to="/citizen/submit"
                class="bg-[#2563EB] hover:bg-[#1E40AF] text-white px-8 py-3.5 rounded-lg font-semibold transition-all shadow-md hover:shadow-lg">Report
                a Complaint</router-link>
              <button
                class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-8 py-3.5 rounded-lg font-semibold transition-all">Learn
                More</button>
            </div>
          </div>
          <div
            class="flex-1 w-full h-80 bg-slate-50 rounded-2xl flex items-center justify-center border-2 border-dashed border-slate-200">
            <span class="text-slate-400 font-medium">[ Hero Illustration: Smart City Workflow ]</span>
          </div>
        </div>
      </section>

      <!-- Workflow Timeline Section -->
      <section class="py-20 px-6 max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-slate-900 text-center mb-16">Complete Complaint Workflow</h2>

        <!-- Desktop Horizontal Workflow -->
        <div class="hidden lg:grid grid-cols-4 gap-8 relative">
          <div v-for="(step, index) in workflowSteps" :key="index"
            class="relative flex flex-col items-center text-center">
            <div
              class="w-16 h-16 bg-white border-2 border-slate-200 rounded-full flex items-center justify-center mb-6 z-10 shadow-sm text-[#2563EB]">
              <component :is="step.icon" class="w-8 h-8" />
            </div>
            <h3 class="font-bold text-slate-900 mb-2">{{ step.title }}</h3>
            <p class="text-sm text-slate-500">{{ step.desc }}</p>
            <!-- Connector Line -->
            <div v-if="index < workflowSteps.length - 1" class="absolute top-8 left-[60%] w-full h-0.5 bg-slate-200">
            </div>
          </div>
        </div>

        <!-- Mobile/Tablet Vertical Workflow -->
        <div class="lg:hidden space-y-8">
          <div v-for="(step, index) in workflowSteps" :key="index" class="flex gap-4">
            <div class="flex flex-col items-center">
              <div class="w-10 h-10 bg-[#2563EB] text-white rounded-full flex items-center justify-center shrink-0">
                <component :is="step.icon" class="w-5 h-5" />
              </div>
              <div v-if="index < workflowSteps.length - 1" class="w-0.5 h-full bg-slate-200 mt-2"></div>
            </div>
            <div>
              <h3 class="font-bold text-slate-900 mb-1">{{ step.title }}</h3>
              <p class="text-sm text-slate-500">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Role-Based Workflow -->
      <section class="py-20 px-6 bg-white">
        <div class="max-w-7xl mx-auto text-center mb-16">
          <h2 class="text-3xl font-bold text-slate-900 mb-4">Who Does What?</h2>
        </div>
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="role in roles" :key="role.title"
            class="p-8 border border-slate-100 rounded-[14px] shadow-sm hover:shadow-md transition-all">
            <h3 class="text-xl font-bold text-slate-900 mb-6">{{ role.title }}</h3>
            <ul class="space-y-4 text-left">
              <li v-for="item in role.tasks" :key="item" class="flex items-center gap-3 text-slate-600">
                <CheckCircle class="w-5 h-5 text-[#22C55E]" /> {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- FAQ Section -->
      <section class="py-20 px-6 max-w-3xl mx-auto">
        <h2 class="text-3xl font-bold text-slate-900 text-center mb-12">Frequently Asked Questions</h2>
        <div v-for="(faq, index) in faqs" :key="index" class="mb-4 border border-slate-200 rounded-lg overflow-hidden">
          <button @click="toggleFaq(index)"
            class="w-full text-left p-6 font-bold text-slate-900 flex justify-between items-center bg-white">
            {{ faq.q }}
            <ChevronDown class="w-5 h-5 text-slate-400" />
          </button>
          <div v-if="activeFaq === index" class="p-6 pt-0 text-slate-600 bg-white">{{ faq.a }}</div>
        </div>
      </section>

      <!-- CTA -->
      <section class="py-24 px-6 text-center bg-[#0F172A] text-white">
        <h2 class="text-4xl font-bold mb-6">Ready to Improve Your Community?</h2>
        <p class="text-slate-400 mb-10 max-w-lg mx-auto">Join CivicDesk today and help make your city cleaner, safer,
          and more transparent.</p>
        <div class="flex gap-4 justify-center">
          <router-link to="/register"
            class="bg-[#2563EB] text-white px-10 py-4 rounded-lg font-bold hover:bg-[#1E40AF]">Register</router-link>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import {
  User, Clipboard, ShieldCheck, Users, Wrench,
  Bell, CheckCircle, Star, ChevronDown
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const activeFaq = ref(0)

const workflowSteps = [
  { title: 'Registration', desc: 'Create your secure account.', icon: User },
  { title: 'Submit Complaint', desc: 'Fill in details and location.', icon: Clipboard },
  { title: 'Verification', desc: 'Officer reviews complaint validity.', icon: ShieldCheck },
  { title: 'Assignment', desc: 'Task assigned to field worker.', icon: Users },
  { title: 'Work Started', desc: 'Action taken on-site.', icon: Wrench },
  { title: 'Notifications', desc: 'Citizen receives status update.', icon: Bell },
  { title: 'Resolution', desc: 'Issue fixed and verified.', icon: CheckCircle },
  { title: 'Feedback', desc: 'Citizen rates the service.', icon: Star }
]

const roles = [
  { title: 'Citizen', tasks: ['Register', 'Submit Complaint', 'Track Progress', 'Receive Notifications', 'Provide Feedback'] },
  { title: 'Civic Officer', tasks: ['Verify Complaint', 'Assign Task', 'Monitor Performance', 'View Analytics', 'Supervise Work'] },
  { title: 'Field Worker', tasks: ['Receive Job', 'Navigate to site', 'Update Status', 'Upload Evidence', 'Finish Task'] }
]

const faqs = [
  { q: 'How do I report a complaint?', a: 'Sign up, click "Report a Complaint," select your category, and describe the issue.' },
  { q: 'How do I track my complaint?', a: 'Check the "My Complaints" section of your dashboard for live updates.' }
]

const toggleFaq = (i) => activeFaq.value = activeFaq.value === i ? -1 : i
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>