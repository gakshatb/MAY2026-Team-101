<template>
  <div class="min-h-screen bg-[#F8FAFC] font-sans text-slate-800">
    <Navbar />

    <main class="pt-20">
      <!-- Hero Section -->
      <section class="py-20 px-6 bg-white border-b border-slate-100">
        <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-12">
          <div class="flex-1 text-center lg:text-left">
            <h1 class="text-4xl lg:text-6xl font-extrabold text-slate-900 leading-tight mb-6">Frequently Asked Questions</h1>
            <p class="text-lg text-slate-600 mb-8 max-w-xl lg:mx-0 mx-auto leading-relaxed">
              Find answers to the most common questions about CivicDesk and how our platform helps resolve civic issues in your city.
            </p>
            <div class="flex gap-4 justify-center lg:justify-start">
              <router-link to="/citizen/submit" class="bg-[#2563EB] hover:bg-[#1E40AF] text-white px-8 py-3.5 rounded-lg font-semibold transition-all shadow-md">Report Complaint</router-link>
              <button class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-8 py-3.5 rounded-lg font-semibold transition-all">Contact Support</button>
            </div>
          </div>
          <div class="flex-1 w-full h-80 bg-slate-50 rounded-2xl flex items-center justify-center border-2 border-dashed border-slate-200">
            <span class="text-slate-400 font-medium text-center p-4">[ Illustration: Help Center & Support ]</span>
          </div>
        </div>
      </section>

      <!-- Search Section -->
      <section class="py-10 px-6">
        <div class="max-w-3xl mx-auto">
          <div class="relative group">
            <Search class="absolute left-4 top-4 text-slate-400 w-5 h-5" />
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search your question..." 
              class="w-full pl-12 pr-6 py-4 rounded-xl border border-slate-200 shadow-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
            />
          </div>
        </div>
      </section>

      <!-- Category Navigation -->
      <section class="px-6 pb-12">
        <div class="max-w-5xl mx-auto flex flex-wrap gap-3 justify-center">
          <button 
            v-for="cat in categories" :key="cat.id"
            @click="scrollToSection(cat.id)"
            class="px-5 py-2.5 bg-white border border-slate-200 rounded-lg text-sm font-medium hover:border-[#2563EB] hover:text-[#2563EB] transition-colors"
          >
            {{ cat.name }}
          </button>
        </div>
      </section>

      <!-- FAQ Content -->
      <section class="pb-20 px-6">
        <div class="max-w-4xl mx-auto">
          <div v-for="cat in filteredSections" :key="cat.id" :id="cat.id" class="mb-12">
            <h2 class="text-2xl font-bold text-slate-900 mb-6">{{ cat.name }}</h2>
            <div class="space-y-4">
              <div 
                v-for="faq in cat.questions" :key="faq.q"
                class="bg-white border border-slate-200 rounded-xl overflow-hidden transition-all"
              >
                <button 
                  @click="toggleFaq(faq)" 
                  class="w-full p-6 text-left font-bold text-slate-900 flex justify-between items-center hover:bg-slate-50"
                  :aria-expanded="faq.isOpen"
                >
                  {{ faq.q }}
                  <ChevronDown :class="['w-5 h-5 text-slate-400 transition-transform', faq.isOpen ? 'rotate-180' : '']" />
                </button>
                <div v-if="faq.isOpen" class="p-6 pt-0 text-slate-600 leading-relaxed border-t border-slate-50">
                  {{ faq.a }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Statistics -->
      <section class="py-20 bg-white border-t border-slate-100 px-6">
        <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div v-for="stat in stats" :key="stat.label">
            <p class="text-4xl font-bold text-[#2563EB] mb-2">{{ stat.val }}</p>
            <p class="text-slate-500 font-medium">{{ stat.label }}</p>
          </div>
        </div>
      </section>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { Search, ChevronDown } from 'lucide-vue-next'

const searchQuery = ref('')

const categories = ref([
  { id: 'general', name: 'General', questions: [
    { q: 'What is CivicDesk?', a: 'CivicDesk is a digital platform bridging citizens and municipal authorities to resolve civic issues transparently.', isOpen: false },
    { q: 'Is CivicDesk free?', a: 'Yes, CivicDesk is completely free for all citizens to use.', isOpen: false }
  ]},
  { id: 'submission', name: 'Complaint Submission', questions: [
    { q: 'How do I submit a complaint?', a: 'Navigate to the dashboard and click "Report Complaint". Fill out the form and submit.', isOpen: false },
    { q: 'Can I upload photos?', a: 'Yes, uploading images is highly encouraged to help authorities assess the issue.', isOpen: false }
  ]},
  { id: 'tracking', name: 'Tracking', questions: [
    { q: 'How do I track my complaint?', a: 'Visit "My Complaints" in your dashboard to see real-time status updates.', isOpen: false }
  ]}
])

const stats = [
  { label: 'Total Questions', val: '30+' },
  { label: 'Categories', val: '9' },
  { label: 'User Roles', val: '3' },
  { label: 'Features', val: '9+' }
]

const toggleFaq = (faq) => {
  faq.isOpen = !faq.isOpen
}

const scrollToSection = (id) => {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth' })
}

const filteredSections = computed(() => {
  if (!searchQuery.value) return categories.value
  return categories.value.map(cat => ({
    ...cat,
    questions: cat.questions.filter(q => 
      q.q.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
      q.a.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })).filter(cat => cat.questions.length > 0)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>