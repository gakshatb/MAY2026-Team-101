<template>
  <header class="bg-white h-20 px-6 border-b border-slate-200 flex items-center justify-between sticky top-0 z-30">
    <div class="flex items-center gap-4">
      <button @click="$emit('toggle-sidebar')" class="lg:hidden p-2 text-slate-500 hover:bg-slate-100 rounded-lg">
        <Menu class="w-6 h-6" />
      </button>
      <div class="hidden sm:block">
        <h2 class="text-xl font-bold text-slate-800">{{ pageTitle }}</h2>
        <p v-if="breadcrumb" class="text-xs text-slate-400">{{ breadcrumb }}</p>
      </div>
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
      <button @click="router.push(`/${rolePrefix}/notifications`)" class="relative p-2 text-slate-500 hover:bg-slate-100 rounded-full transition-colors">
        <Bell class="w-6 h-6" />
        <span class="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 border-2 border-white rounded-full"></span>
      </button>

      <div class="w-px h-8 bg-slate-200 hidden sm:block"></div>

      <!-- Profile Dropdown -->
      <button @click="router.push(`/${rolePrefix}/profile`)" class="flex items-center gap-3 hover:bg-slate-50 p-1.5 rounded-lg transition-colors text-left">
        <div class="w-10 h-10 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500 font-semibold text-sm shrink-0 overflow-hidden">
          <img v-if="user?.profilePhoto" :src="photoUrl" alt="" class="w-full h-full object-cover" />
          <span v-else>{{ initials }}</span>
        </div>
        <div class="hidden sm:block">
          <p class="text-sm font-bold text-slate-900 leading-none mb-1">{{ user?.name || 'User' }}</p>
          <p class="text-xs font-medium text-[#2563EB] leading-none">{{ userRole }}</p>
        </div>
        <ChevronDown class="w-4 h-4 text-slate-400 hidden sm:block" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Menu, Bell, Search, ChevronDown } from 'lucide-vue-next'

const router = useRouter()

const props = defineProps({
  userRole: {
    type: String,
    default: 'Citizen'
  },
  user: {
    type: Object,
    default: null
  },
  pageTitle: {
    type: String,
    default: 'Dashboard'
  },
  breadcrumb: {
    type: String,
    default: ''
  }
})

// Mirrors the role-prefix logic in Sidebar.vue so "Profile" and
// "Notifications" here land on the same routes the sidebar links to.
const rolePrefix = computed(() => {
  switch (props.userRole) {
    case 'Administrator':
    case 'Admin': return 'admin'
    case 'Officer': return 'officer'
    case 'Worker': return 'worker'
    default: return 'citizen'
  }
})

const initials = computed(() => {
  const name = props.user?.name
  if (!name) return '?'
  return name.trim().split(/\s+/).slice(0, 2).map(n => n[0]?.toUpperCase()).join('')
})

const photoUrl = computed(() => props.user?.profilePhoto ? `http://127.0.0.1:5000${props.user.profilePhoto}` : '')
</script>