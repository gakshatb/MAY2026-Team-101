<template>
  <div class="min-h-screen bg-[#F8FAFC] font-sans text-slate-800">
    <Navbar />

    <main>
      <!-- Hero Section -->
      <section class="pt-32 pb-20 px-6 bg-white">
        <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-12">
          <div class="flex-1 text-center lg:text-left">
            <h1 class="text-4xl lg:text-6xl font-extrabold text-slate-900 leading-tight mb-6">Our Services</h1>
            <p class="text-lg text-slate-600 mb-8 max-w-2xl lg:mx-0 mx-auto">CivicDesk provides a complete digital
              platform for reporting, managing, tracking, and resolving civic complaints efficiently.</p>
            <div class="flex gap-4 justify-center lg:justify-start">
              <router-link to="/citizen/submit"
                class="bg-[#2563EB] hover:bg-[#1E40AF] text-white px-8 py-3 rounded-lg font-medium transition-all">Report
                Complaint</router-link>
              <router-link to="/contact"
                class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-8 py-3 rounded-lg font-medium transition-all">Contact
                Us</router-link>
            </div>
          </div>
          <div
            class="flex-1 w-full h-80 bg-slate-100 rounded-2xl flex items-center justify-center border-2 border-dashed border-slate-300">
            <span class="text-slate-400 font-medium">[ Hero Illustration: Smart City Maintenance ]</span>
          </div>
        </div>
      </section>

      <!-- Why It Matters -->
      <section class="py-20 px-6">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl font-bold text-slate-900 mb-6">Making Civic Services Easier</h2>
          <p class="text-lg text-slate-600 leading-relaxed">
            Communication between citizens and municipal authorities is often fragmented. CivicDesk removes these
            barriers by digitizing the entire complaint lifecycle.
            We replace confusion with <strong>transparency</strong>, ensuring every report is tracked, assigned, and
            resolved with <strong>efficiency</strong>.
            By providing a single source of truth, we foster a culture of accountability and community care.
          </p>
        </div>
      </section>

      <!-- Core Services -->
      <section class="py-20 px-6 bg-white">
        <div class="max-w-7xl mx-auto">
          <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">Core Services</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="service in coreServices" :key="service.title"
              class="p-8 bg-white border border-slate-100 rounded-[14px] shadow-sm hover:shadow-lg transition-all group">
              <component :is="service.icon" class="w-10 h-10 text-[#2563EB] mb-6" />
              <h3 class="text-xl font-bold text-slate-900 mb-3">{{ service.title }}</h3>
              <p class="text-slate-600 mb-6">{{ service.desc }}</p>
              <button class="text-[#2563EB] font-bold text-sm group-hover:underline">Learn More →</button>
            </div>
          </div>
        </div>
      </section>

      <!-- Role-Based Services -->
      <section class="py-20 px-6 max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">Services for Every User</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="role in roleServices" :key="role.title"
            class="bg-white p-8 rounded-[14px] shadow-sm border border-slate-100">
            <h3 class="text-2xl font-bold text-slate-900 mb-6">{{ role.title }}</h3>
            <ul class="space-y-4">
              <li v-for="item in role.items" :key="item" class="flex items-center gap-3 text-slate-600">
                <CheckCircle class="w-5 h-5 text-[#22C55E]" /> {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Statistics -->
      <section ref="statsSection" class="py-20 px-6 bg-[#2563EB] text-white">
        <div class="max-w-7xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
          <div v-for="(stat, index) in stats" :key="stat.title">
            <p class="text-4xl font-bold mb-2">{{ animatedStats[index] }}+</p>
            <p class="text-blue-100 font-medium">{{ stat.title }}</p>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section class="py-20 px-6 bg-white">
        <div class="max-w-3xl mx-auto">
          <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">Frequently Asked Questions</h2>
          <div v-for="(faq, index) in faqs" :key="index"
            class="mb-4 border border-slate-200 rounded-lg overflow-hidden">
            <button @click="toggleFaq(index)"
              class="w-full text-left p-6 font-bold text-slate-900 flex justify-between items-center">
              {{ faq.q }}
              <ChevronDown class="w-5 h-5 text-slate-400" />
            </button>
            <div v-if="activeFaq === index" class="p-6 pt-0 text-slate-600">{{ faq.a }}</div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="py-24 px-6 text-center">
        <h2 class="text-4xl font-bold text-slate-900 mb-6">Start Reporting Civic Issues Today</h2>
        <p class="text-slate-500 mb-10 max-w-lg mx-auto">Join CivicDesk and help create cleaner, safer, and smarter
          communities.</p>
        <div class="flex gap-4 justify-center">
          <router-link to="/register"
            class="bg-[#2563EB] text-white px-10 py-4 rounded-lg font-bold hover:bg-[#1E40AF]">Register
            Now</router-link>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import {
  ClipboardList, Search, Bell, Shield, Users,
  MapPin, CheckCircle, ChevronDown, Clock, Layers
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const activeFaq = ref(0)
const statsSection = ref(null)
const animatedStats = ref([0, 0, 0, 0])

const coreServices = [
  { title: 'Complaint Submission', desc: 'Report issues in seconds with intuitive forms.', icon: ClipboardList },
  { title: 'Complaint Tracking', desc: 'Real-time updates from submission to resolution.', icon: Search },
  { title: 'Image Evidence', desc: 'Upload high-quality images to verify issues.', icon: Layers },
  { title: 'Real-time Notifications', desc: 'SMS and email updates on status changes.', icon: Bell },
  { title: 'Automated Assignment', desc: 'Smart routing to correct departments.', icon: Shield },
  { title: 'Analytics Dashboard', desc: 'Monitor municipal performance trends.', icon: MapPin }
]

const roleServices = [
  { title: 'Citizen', items: ['Report complaints', 'Track progress', 'View history', 'Give feedback'] },
  { title: 'Civic Officer', items: ['Review complaints', 'Assign tasks', 'View analytics', 'Verify work'] },
  { title: 'Field Worker', items: ['Receive work orders', 'Update status', 'View location', 'Mark resolved'] }
]

const stats = [
  { title: 'User Interviews', target: 5 },
  { title: 'Categories', target: 9 },
  { title: 'Core Services', target: 9 },
  { title: 'Workflow Stages', target: 6 }
]

const faqs = [
  { q: 'How do I report a complaint?', a: 'Log in, click "Submit Complaint," choose a category, and describe the issue.' },
  { q: 'Can I track my status?', a: 'Yes, your dashboard provides live tracking for all your active reports.' }
]

const toggleFaq = (i) => activeFaq.value = activeFaq.value === i ? -1 : i

const animateStats = () => {
  stats.forEach((stat, i) => {
    let current = 0
    const step = Math.max(1, Math.floor(stat.target / 20))
    const interval = setInterval(() => {
      current += step
      if (current >= stat.target) {
        animatedStats.value[i] = stat.target
        clearInterval(interval)
      } else {
        animatedStats.value[i] = current
      }
    }, 50)
  })
}

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) animateStats()
  }, { threshold: 0.5 })
  if (statsSection.value) observer.observe(statsSection.value)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>