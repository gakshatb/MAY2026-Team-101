<template>
  <header class="bg-white h-20 px-6 border-b border-slate-200 flex items-center justify-between sticky top-0 z-30">
    <div class="flex items-center gap-4">
      <button @click="$emit('toggle-sidebar')" class="lg:hidden p-2 text-slate-500 hover:bg-slate-100 rounded-lg">
        <Menu class="w-6 h-6" />
      </button>
      <h2 class="text-xl font-bold text-slate-800 hidden sm:block">{{ pageTitle }}</h2>
    </div>

    <div class="flex items-center gap-3 sm:gap-6">
      <!-- Search -->
      <div class="hidden md:flex relative">
        <Search class="w-5 h-5 text-slate-400 absolute left-3 top-2.5" />
        <input 
          type="text" 
          placeholder="Search complaints..." 
          class="pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] w-64 transition-all"
        />
      </div>

      <!-- Notifications -->
      <button @click="router.push('/notifications')" class="relative p-2 text-slate-500 hover:bg-slate-100 rounded-full transition-colors">
        <Bell class="w-6 h-6" />
        <span class="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 border-2 border-white rounded-full"></span>
      </button>

      <div class="w-px h-8 bg-slate-200 hidden sm:block"></div>

      <!-- Profile Dropdown -->
      <button @click="router.push('/profile')" class="flex items-center gap-3 hover:bg-slate-50 p-1.5 rounded-lg transition-colors text-left">
        <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="Avatar" class="w-10 h-10 rounded-full object-cover border border-slate-200" />
        <div class="hidden sm:block">
          <p class="text-sm font-bold text-slate-900 leading-none mb-1">Jane Doe</p>
          <p class="text-xs font-medium text-[#2563EB] leading-none">{{ userRole }}</p>
        </div>
        <ChevronDown class="w-4 h-4 text-slate-400 hidden sm:block" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Menu, Bell, Search, ChevronDown } from 'lucide-vue-next'

const router = useRouter()

defineProps({
  userRole: {
    type: String,
    default: 'Citizen'
  },
  pageTitle: {
    type: String,
    default: 'Dashboard'
  }
})
</script>