<template>
  <div class="min-h-screen bg-[#F8FAFC] font-sans text-slate-800">
    <Navbar />

    <main class="pt-20">
      <!-- Hero Section -->
      <section class="py-20 px-6 bg-white">
        <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-12">
          <div class="flex-1">
            <h1 class="text-4xl lg:text-5xl font-extrabold text-slate-900 leading-tight mb-6">
              Building Better Communities Through Smart Civic Services
            </h1>
            <p class="text-lg text-slate-600 mb-8 leading-relaxed">
              CivicDesk is a centralized platform that simplifies civic complaint reporting, improves transparency, and
              helps local authorities resolve public issues more efficiently.
            </p>
            <div class="flex gap-4">
              <button
                class="bg-[#2563EB] hover:bg-[#1E40AF] text-white px-8 py-3 rounded-lg font-medium transition-all shadow-md">Learn
                More</button>
              <router-link to="/contact"
                class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-8 py-3 rounded-lg font-medium transition-all">Contact
                Us</router-link>
            </div>
          </div>
          <div
            class="flex-1 w-full h-80 bg-slate-100 rounded-2xl flex items-center justify-center border-2 border-dashed border-slate-300">
            <span class="text-slate-400 font-medium">[ Hero Illustration: Smart City ]</span>
          </div>
        </div>
      </section>

      <!-- Section 1: About -->
      <section class="py-20 px-6 max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-slate-900 mb-8 text-center">About CivicDesk</h2>
        <div class="bg-white p-8 md:p-12 rounded-[14px] shadow-sm border border-slate-100">
          <p class="text-lg text-slate-600 leading-relaxed text-center max-w-4xl mx-auto">
            CivicDesk is a Software Engineering group project designed to bridge the gap between citizens and municipal
            authorities.
            Inspired by real-world interviews with local residents, we identified a critical disconnect in how public
            infrastructure
            complaints were handled. Our platform provides a single source of truth—a centralized dashboard where
            citizens can submit
            issues, track their progress in real-time, and ensure accountability through a transparent, documented
            resolution process.
          </p>
        </div>
      </section>

      <!-- Section 2: Problems -->
      <section class="py-20 px-6 bg-white">
        <div class="max-w-7xl mx-auto">
          <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">The Problem</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div v-for="prob in problems" :key="prob.title"
              class="p-6 bg-[#F8FAFC] rounded-[14px] border border-slate-100 hover:shadow-lg transition-all">
              <component :is="prob.icon" class="w-8 h-8 text-[#2563EB] mb-4" />
              <h3 class="font-bold text-slate-900 mb-2">{{ prob.title }}</h3>
              <p class="text-sm text-slate-500">{{ prob.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 7: Our Users -->
      <section class="py-20 px-6 max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">Who Uses CivicDesk?</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="user in users" :key="user.role"
            class="bg-white p-8 rounded-[14px] border border-slate-100 shadow-sm text-center">
            <div class="w-16 h-16 bg-blue-50 text-[#2563EB] rounded-full flex items-center justify-center mx-auto mb-6">
              <component :is="user.icon" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">{{ user.role }}</h3>
            <p class="text-slate-600">{{ user.desc }}</p>
          </div>
        </div>
      </section>

      <!-- Section 12: Meet The Team -->
      <section class="py-20 px-6 bg-white">
        <div class="max-w-7xl mx-auto">
          <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">Meet The Team</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
            <div v-for="member in team" :key="member.name" class="text-center">
              <img :src="member.image" :alt="member.name"
                class="w-20 h-20 bg-slate-100 rounded-full mx-auto mb-4 border-2 border-slate-50" />
              <h4 class="font-bold text-slate-900">{{ member.name }}</h4>
              <p class="text-sm text-[#2563EB] font-medium">{{ member.role }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="py-20 px-6 bg-[#0F172A] text-white text-center">
        <h2 class="text-3xl font-bold mb-4">Together We Can Build Better Cities.</h2>
        <p class="text-slate-400 mb-8 max-w-xl mx-auto">CivicDesk empowers citizens and authorities to work together for
          cleaner, safer, and smarter communities.</p>
        <div class="flex gap-4 justify-center">
          <router-link to="/register"
            class="bg-[#2563EB] px-8 py-3 rounded-lg font-medium hover:bg-[#1E40AF]">Register</router-link>
          <router-link to="/contact"
            class="bg-transparent border border-slate-600 px-8 py-3 rounded-lg font-medium hover:bg-slate-800">Contact
            Us</router-link>
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
  Building, Shield, Users, ClipboardList,
  Clock, AlertTriangle, User, Search
} from 'lucide-vue-next'

const problems = [
  { title: 'No Reporting Process', desc: 'Citizens are confused about where to file complaints.', icon: Building },
  { title: 'No Transparency', desc: 'Lack of updates leads to mistrust in the system.', icon: Shield },
  { title: 'Delayed Resolution', desc: 'Issues remain unresolved for weeks.', icon: Clock },
  { title: 'Information Gap', desc: 'Departments are siloed, leading to miscommunication.', icon: AlertTriangle }
]

const users = [
  { role: 'Citizen', desc: 'Reports civic issues and tracks complaint status in real-time.', icon: User },
  { role: 'Civic Officer', desc: 'Reviews incoming complaints, verifies issues, and assigns tasks.', icon: Shield },
  { role: 'Field Worker', desc: 'Receives work orders, performs repairs, and marks tasks as complete.', icon: Users }
]

const team = [
  { name: 'Guhan M R', role: 'Project Manager', image: '/Team/guhan.jpg' },
  { name: 'Gupta Shivam Rakesh', role: 'Frontend Dev', image: '/Team/gupta.jpg' },
  { name: 'Akshat B Gupta', role: 'Backend Dev', image: '/Team/akshat.jpg' },
  { name: 'Akash Maurya', role: 'QA & Testing', image: '/Team/akash.jpg' },
  { name: 'Girish M', role: 'Code Reviewer', image: '/Team/girish.jpg' }
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }
</style>