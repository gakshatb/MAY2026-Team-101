<template>
  <div class="min-h-screen bg-[#F8FAFC] font-sans text-slate-800 font-inter">

    <!-- Reusable Navbar -->
    <Navbar />

    <main>
      <!-- Hero Section -->
      <section id="home" class="pt-32 pb-20 lg:pt-48 lg:pb-32 px-6 overflow-hidden">
        <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-16">
          <div class="flex-1 text-center lg:text-left z-10">
            <h1
              class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-slate-900 leading-tight mb-6 animate-slide-up">
              Report Civic Issues.<br />
              <span class="text-[#2563EB]">Track Every Complaint.</span><br />
              Build Better Communities.
            </h1>
            <p class="text-lg md:text-xl text-slate-600 mb-10 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
              CivicDesk makes it easy for citizens to report civic issues, monitor complaint progress, and stay
              connected with local authorities through one secure and transparent platform.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 mb-12">
              <router-link to="/register"
                class="w-full sm:w-auto text-center bg-[#2563EB] hover:bg-[#1E40AF] text-white font-semibold px-8 py-3.5 rounded-xl shadow-md hover:shadow-lg transition-all text-lg">
                Report a Complaint
              </router-link>
              <a href="#how-it-works"
                class="w-full sm:w-auto text-center bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-semibold px-8 py-3.5 rounded-xl transition-all text-lg">
                Learn More
              </a>
            </div>

            <div
              class="flex flex-wrap items-center justify-center lg:justify-start gap-4 md:gap-8 text-sm font-medium text-slate-600">
              <div v-for="badge in trustBadges" :key="badge" class="flex items-center gap-2">
                <CheckCircle2 class="w-5 h-5 text-[#22C55E]" />
                <span>{{ badge }}</span>
              </div>
            </div>
          </div>

          <div class="flex-1 w-full max-w-lg lg:max-w-none relative">
            <div class="absolute inset-0 bg-blue-100/50 rounded-full blur-3xl transform -translate-x-10 translate-y-10">
            </div>
            <!-- Illustration Placeholder -->
            <!-- Hero Image -->
            <div
              class="relative w-full aspect-square bg-white rounded-3xl border border-slate-100 shadow-xl flex items-center justify-center overflow-hidden">
              <img 
                src="../../assets/home.jpg" 
                alt="CivicDesk Illustration" 
                class="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      <!-- Why CivicDesk Section -->
      <section id="about" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Why CivicDesk?</h2>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto">A modern approach to solving community problems
              effectively and transparently.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div v-for="feature in features" :key="feature.title"
              class="bg-[#F8FAFC] p-8 rounded-2xl hover:-translate-y-1 transition-transform duration-300">
              <div class="w-12 h-12 bg-blue-100 text-[#2563EB] rounded-xl flex items-center justify-center mb-6">
                <component :is="feature.icon" class="w-6 h-6" />
              </div>
              <h3 class="text-xl font-bold text-slate-900 mb-3">{{ feature.title }}</h3>
              <p class="text-slate-600 leading-relaxed">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Civic Problems We Solve -->
      <section id="services" class="py-20">
        <div class="max-w-7xl mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Common Civic Problems</h2>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto">Report exactly what needs fixing. We route it to the
              right department.</p>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <div v-for="problem in problems" :key="problem.title"
              class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md hover:border-blue-100 transition-all cursor-pointer group">
              <div
                class="w-10 h-10 rounded-full bg-slate-50 group-hover:bg-blue-50 flex items-center justify-center mb-4 transition-colors">
                <component :is="problem.icon" class="w-5 h-5 text-slate-600 group-hover:text-[#2563EB]" />
              </div>
              <h3 class="font-bold text-slate-900 mb-2">{{ problem.title }}</h3>
              <p class="text-sm text-slate-500">{{ problem.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- How It Works Section -->
      <section id="how-it-works" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-6">
          <div class="text-center mb-20">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">How CivicDesk Works</h2>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto">A seamless process from reporting an issue to its final
              resolution.</p>
          </div>

          <div class="relative">
            <!-- Connecting Line -->
            <div class="hidden lg:block absolute top-1/2 left-0 w-full h-0.5 bg-slate-100 -translate-y-1/2"></div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
              <div v-for="(step, index) in steps" :key="step.title"
                class="relative z-10 flex flex-col items-center text-center group">
                <div
                  class="w-16 h-16 bg-white border-2 border-slate-200 group-hover:border-[#2563EB] rounded-2xl flex items-center justify-center mb-6 transition-colors shadow-sm">
                  <component :is="step.icon" class="w-7 h-7 text-[#2563EB]" />
                </div>
                <div
                  class="bg-[#2563EB] text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center mb-3">
                  {{ index + 1 }}
                </div>
                <h3 class="font-bold text-slate-900 text-sm mb-2">{{ step.title }}</h3>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Statistics Section -->
      <section class="py-20 bg-[#2563EB] text-white relative overflow-hidden" ref="statsSection">
        <div
          class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIvPjwvc3ZnPg==')] opacity-30">
        </div>
        <div class="max-w-7xl mx-auto px-6 relative z-10">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 text-center">
            <div v-for="(stat, index) in stats" :key="stat.label">
              <div class="text-4xl lg:text-5xl font-extrabold mb-2">{{ animatedStats[index] }}{{ stat.suffix }}</div>
              <div class="text-blue-200 font-medium">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Benefits Section -->
      <section class="py-20">
        <div class="max-w-7xl mx-auto px-6 flex flex-col lg:flex-row items-center gap-16">
          <div class="flex-1 w-full">
            <div
              class="w-full aspect-[4/3] bg-white rounded-3xl border border-slate-200 shadow-lg flex items-center justify-center overflow-hidden">
              <img 
                src="../../assets/home1.jpg" 
                alt="CivicDesk Benefits" 
                class="w-full h-full object-cover"
              />
            </div>
          </div>
          <div class="flex-1">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-6">Empowering Citizens. Enabling Authorities.
            </h2>
            <p class="text-lg text-slate-600 mb-8">CivicDesk bridges the gap between the public and the government,
              creating a collaborative environment for urban maintenance.</p>
            <ul class="space-y-4">
              <li v-for="benefit in benefits" :key="benefit" class="flex items-center gap-3">
                <div class="bg-[#22C55E]/10 p-1.5 rounded-full">
                  <Check class="w-5 h-5 text-[#22C55E]" />
                </div>
                <span class="text-slate-700 font-medium text-lg">{{ benefit }}</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Testimonials -->
      <section class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Trusted by the Community</h2>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto">Hear what citizens are saying about their experience
              with CivicDesk.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="review in testimonials" :key="review.name"
              class="bg-[#F8FAFC] p-8 rounded-2xl border border-slate-100">
              <div class="flex gap-1 text-yellow-400 mb-4">
                <Star v-for="i in 5" :key="i" class="w-5 h-5 fill-current" />
              </div>
              <p class="text-slate-700 mb-8 leading-relaxed">"{{ review.text }}"</p>
              <div class="flex items-center gap-4">
                <div
                  class="w-12 h-12 bg-slate-200 rounded-full flex items-center justify-center text-slate-500 font-bold text-xl">
                  {{ review.name.charAt(0) }}
                </div>
                <div>
                  <h4 class="font-bold text-slate-900">{{ review.name }}</h4>
                  <p class="text-sm text-slate-500">{{ review.role }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ Section -->
      <section id="faqs" class="py-20">
        <div class="max-w-3xl mx-auto px-6">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Frequently Asked Questions</h2>
            <p class="text-lg text-slate-600">Everything you need to know about using the platform.</p>
          </div>
          <div class="space-y-4">
            <div v-for="(faq, index) in faqs" :key="index"
              class="bg-white border border-slate-200 rounded-xl overflow-hidden">
              <button @click="toggleFaq(index)"
                class="w-full flex items-center justify-between p-6 text-left focus:outline-none"
                :aria-expanded="activeFaq === index">
                <span class="font-bold text-slate-900">{{ faq.question }}</span>
                <ChevronDown
                  :class="['w-5 h-5 text-slate-400 transition-transform duration-300', activeFaq === index ? 'rotate-180' : '']" />
              </button>
              <div v-show="activeFaq === index" class="px-6 pb-6 text-slate-600 animate-fade-in">
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Banner -->
      <section class="py-24 bg-slate-900 text-center px-6">
        <div class="max-w-3xl mx-auto">
          <h2 class="text-3xl md:text-5xl font-bold text-white mb-6">Help Make Your City Better.</h2>
          <p class="text-xl text-slate-400 mb-10">Join CivicDesk today and report civic issues with confidence.
            Together, we can build a stronger community.</p>
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <router-link to="/register"
              class="w-full sm:w-auto bg-[#2563EB] hover:bg-blue-500 text-white font-semibold px-8 py-4 rounded-xl transition-colors text-lg">
              Register Now
            </router-link>
            <router-link to="/login"
              class="w-full sm:w-auto bg-transparent border border-slate-600 hover:bg-slate-800 text-white font-semibold px-8 py-4 rounded-xl transition-colors text-lg">
              Login to Account
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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Navbar from '../../components/Navbar.vue'
import Footer from '../../components/Footer.vue'
import {
  CheckCircle2, FileText, Crosshair,
  Bell, Zap, Trash2, Map, LightbulbOff, Droplet,
  Waves, AlertTriangle, Building2, UserPlus, FileEdit,
  UserCheck, HardHat, CheckSquare, MessageSquare,
  Check, Star, ChevronDown, PieChart, MonitorSmartphone
} from 'lucide-vue-next'

// --- State ---
const activeFaq = ref(0)
const statsSection = ref(null)
const statsAnimated = ref(false)

// --- Data ---
const trustBadges = [
  'Easy Complaint Reporting',
  'Transparent Tracking',
  'Faster Resolution',
  'Secure Platform'
]

const features = [
  { title: 'Complaint Submission', description: 'Report civic issues in just a few simple steps with photo evidence.', icon: FileText },
  { title: 'Complaint Tracking', description: 'Track every complaint from initial submission to final completion.', icon: Crosshair },
  { title: 'Real-time Notifications', description: 'Receive updates via SMS/Email whenever your complaint status changes.', icon: Bell },
  { title: 'Faster Resolution', description: 'Improve direct communication between citizens and civic authorities.', icon: Zap },
]

const problems = [
  { title: 'Garbage Collection', desc: 'Missed collections or dumps.', icon: Trash2 },
  { title: 'Road Potholes', desc: 'Damaged or dangerous roads.', icon: Map },
  { title: 'Streetlight Failure', desc: 'Broken or non-functioning lights.', icon: LightbulbOff },
  { title: 'Water Leakage', desc: 'Burst pipes and public leaks.', icon: Droplet },
  { title: 'Blocked Drainage', desc: 'Clogged drains and flooding.', icon: Waves },
  { title: 'Illegal Dumping', desc: 'Unauthorized waste disposal.', icon: AlertTriangle },
  { title: 'Property Damage', desc: 'Vandalism to public assets.', icon: Building2 },
  { title: 'Overflowing Dustbins', desc: 'Public bins requiring clearance.', icon: Trash2 },
]

const steps = [
  { title: 'Register', icon: UserPlus },
  { title: 'Submit Complaint', icon: FileEdit },
  { title: 'Officer Reviews', icon: UserCheck },
  { title: 'Worker Assigned', icon: HardHat },
  { title: 'Issue Resolved', icon: CheckSquare },
  { title: 'Citizen Updates', icon: MessageSquare },
]

const stats = ref([
  { label: 'Total Complaints', target: 0, suffix: '+' },
  { label: 'Resolved Complaints', target: 0, suffix: '+' },
  { label: 'Active Citizens', target: 0, suffix: '+' },
  { label: 'Avg Resolution Time', target: 0, suffix: 'h' },
])
const animatedStats = ref([0, 0, 0, 0])

const fetchStats = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/public-stats')
    if (response.data.success) {
      const s = response.data.stats
      stats.value[0].target = s.total_complaints
      stats.value[1].target = s.resolved_complaints
      stats.value[2].target = s.active_citizens
      stats.value[3].target = s.avg_resolution_hours
    }
  } catch (err) {
    // Backend unreachable — leave targets at 0 rather than guessing.
  }
}

const benefits = [
  'Faster Complaint Reporting directly from your phone',
  'Transparent Complaint Tracking with audit trails',
  'Improved Communication with municipal workers',
  'Better Accountability for government departments',
  'Safer Communities through rapid hazard fixes',
  'Cleaner Environment via proper waste management reporting'
]

const testimonials = [
  { name: 'Sarah Jenkins', role: 'Citizen', text: 'I reported a severe pothole in my neighborhood, and it was filled within 48 hours. The status tracking kept me informed the whole time.' },
  { name: 'Michael Chen', role: 'Working Professional', text: 'CivicDesk is exactly what our city needed. No more calling government offices and waiting on hold. The UI is incredibly intuitive.' },
  { name: 'Priya Sharma', role: 'Shop Owner', text: 'The overflowing dustbins near my shop were affecting business. After using CivicDesk, the waste management team responds consistently.' },
]

const faqs = [
  { question: 'How do I report a complaint?', answer: 'Simply create an account, log in, and click the "Report Issue" button. Fill out the form with the category, location, and a description of the problem.' },
  { question: 'How can I track my complaint?', answer: 'Your dashboard contains a "My Complaints" section where you can see the real-time status (Pending, Assigned, In Progress, Resolved) of every issue you submit.' },
  { question: 'How long does resolution take?', answer: 'Resolution times vary by the severity and type of complaint. Minor issues like garbage collection often resolve in 24-48 hours, while infrastructural repairs may take longer.' },
  { question: 'Who handles my complaint?', answer: 'Your complaint is automatically routed to the relevant Civic Officer for your zone, who then assigns it to a specialized Field Worker for action.' },
  { question: 'Can I upload images?', answer: 'Yes! We strongly encourage uploading images when submitting a complaint, as visual evidence helps authorities assess and resolve the issue faster.' },
]

// --- Logic & Lifecycle ---
const toggleFaq = (index) => {
  activeFaq.value = activeFaq.value === index ? -1 : index
}

const animateCounters = () => {
  if (statsAnimated.value) return
  statsAnimated.value = true

  stats.value.forEach((stat, index) => {
    const duration = 2000 // 2 seconds
    const steps = 60
    const increment = stat.target / steps
    let current = 0

    const timer = setInterval(() => {
      current += increment
      if (current >= stat.target) {
        animatedStats.value[index] = stat.target
        clearInterval(timer)
      } else {
        animatedStats.value[index] = Math.floor(current)
      }
    }, duration / steps)
  })
}

onMounted(async () => {
  
  await fetchStats()

  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      animateCounters()
      observer.disconnect()
    }
  }, { threshold: 0.5 })

  if (statsSection.value) {
    observer.observe(statsSection.value)
  }
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-inter { font-family: 'Inter', sans-serif; }
html { scroll-behavior: smooth; }
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
.animate-slide-up { animation: slideUp 0.6s ease-out forwards; }
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>