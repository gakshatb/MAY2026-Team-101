<template>
  <aside class="w-64 bg-[#0F172A] text-white flex flex-col h-screen overflow-y-auto border-r border-slate-800">
    <!-- Logo -->
    <div class="p-6 flex items-center gap-3">
      <div class="w-8 h-8 bg-[#2563EB] rounded-lg flex items-center justify-center">
        <Shield class="w-5 h-5 text-white" />
      </div>
      <div>
        <h2 class="font-bold text-lg leading-tight tracking-wide">CivicDesk</h2>
        <p class="text-[9px] text-slate-400 tracking-[0.2em] uppercase mt-0.5">Management</p>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 px-4 py-4 space-y-1.5">
      <router-link 
        v-for="item in menuItems" 
        :key="item.name" 
        :to="item.route"
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
        :class="[
          $route.path === item.route 
            ? 'bg-[#2563EB] text-white shadow-md' 
            : 'text-slate-300 hover:bg-slate-800 hover:text-white'
        ]"
      >
        <component :is="item.icon" class="w-5 h-5" />
        {{ item.name }}
      </router-link>
    </nav>

    <!-- Bottom Actions -->
    <div class="p-4 border-t border-slate-800 space-y-1.5 mt-auto">
      <router-link 
        to="/citizen/profile" 
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
        :class="[$route.path === '/citizen/profile' ? 'bg-[#2563EB] text-white shadow-md' : 'text-slate-300 hover:bg-slate-800 hover:text-white']"
      >
        <User class="w-5 h-5" /> Profile
      </router-link>
      
      <button class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition-all duration-200">
        <Settings class="w-5 h-5" /> Settings
      </button>
      
      <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-slate-300 hover:bg-red-500/10 hover:text-red-400 transition-all duration-200 mt-2">
        <LogOut class="w-5 h-5" /> Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  LayoutDashboard, PlusCircle, FolderOpen, 
  MapPin, Bell, MessageSquare, User, 
  Settings, LogOut, Shield
} from 'lucide-vue-next'

const props = defineProps({
  userRole: {
    type: String,
    default: 'Citizen'
  }
})

const router = useRouter()
const route = useRoute()

// Centralized routing logic updated for Citizen prefix
const menuItems = computed(() => {
  if (props.userRole === 'Citizen') {
    return [
      { name: 'Dashboard', icon: LayoutDashboard, route: '/citizen/dashboard' },
      { name: 'Submit Complaint', icon: PlusCircle, route: '/citizen/submit' },
      { name: 'My Complaints', icon: FolderOpen, route: '/citizen/complaints' },
      { name: 'Track Complaint', icon: MapPin, route: '/citizen/track/CMP-000' }, // Placeholder ID for tracking UI
      { name: 'Notifications', icon: Bell, route: '/citizen/notifications' },
      { name: 'Feedback', icon: MessageSquare, route: '/citizen/feedback/CMP-000' } // Placeholder ID for feedback UI
    ]
  }
  
  // Officer/Worker menus (Can be updated later when you build those folders)
  if (props.userRole === 'Civic Officer') {
    return [
      { name: 'Dashboard', icon: LayoutDashboard, route: '/officer/dashboard' }
    ]
  }

  return []
})

const handleLogout = () => {
  // Add logout logic here later (clear tokens, etc)
  router.push('/login')
}
</script>