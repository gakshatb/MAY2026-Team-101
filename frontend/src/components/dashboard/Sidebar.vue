<template>
  <!-- Mobile backdrop: only rendered when the sidebar is open on small screens -->
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-slate-900/50 z-30 lg:hidden"
    @click="$emit('close-sidebar')"
  ></div>

  <aside
    class="w-64 bg-[#0F172A] text-white flex flex-col h-screen overflow-y-auto border-r border-slate-800 fixed inset-y-0 left-0 z-40 transform transition-transform duration-300 lg:static lg:translate-x-0"
    :class="isOpen ? 'translate-x-0' : '-translate-x-full'"
  >
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
    <nav class="flex-1 px-4 py-4 space-y-1.5 custom-scrollbar overflow-y-auto">
      <router-link 
        v-for="item in menuItems" 
        :key="item.name" 
        :to="item.route"
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
        :class="[
          $route.path.includes(item.route) 
            ? 'bg-[#2563EB] text-white shadow-md' 
            : 'text-slate-300 hover:bg-slate-800 hover:text-white'
        ]"
        @click="$emit('close-sidebar')"
      >
        <component :is="item.icon" class="w-5 h-5" />
        {{ item.name }}
      </router-link>
    </nav>

    <!-- Bottom Actions (Profile & Logout Only - Settings Removed) -->
    <div class="p-4 border-t border-slate-800 space-y-1.5 mt-auto bg-[#0F172A]">
      <router-link 
        :to="`/${rolePrefix}/profile`" 
        class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
        :class="[$route.path.includes('/profile') ? 'bg-[#2563EB] text-white shadow-md' : 'text-slate-300 hover:bg-slate-800 hover:text-white']"
        @click="$emit('close-sidebar')"
      >
        <User class="w-5 h-5" /> Profile
      </router-link>
      
      <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-slate-300 hover:bg-red-500/10 hover:text-red-400 transition-all duration-200 mt-2">
        <LogOut class="w-5 h-5" /> Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { 
  LayoutDashboard, PlusCircle, FolderOpen, 
  MapPin, Bell, MessageSquare, User, 
  LogOut, Shield, Building2, 
  Users, UserSearch, BarChart3, Megaphone, 
  Activity, ClipboardList, FileText, UserPlus, 
  HardHat, Briefcase, ListTodo, Wrench, 
  CheckSquare, PieChart
} from 'lucide-vue-next'

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },

  userRole: {
    type: String,
    default: ''
  }
})

defineEmits(['close-sidebar'])

const router = useRouter()
const route = useRoute()

// SMART DETECTION: Automatically determine the role based on the current URL path
const currentRole = computed(() => {
  const path = route.path.toLowerCase();
  if (path.startsWith('/admin')) return 'Administrator';
  if (path.startsWith('/officer')) return 'Officer';
  if (path.startsWith('/worker')) return 'Worker';
  return 'Citizen'; // Default fallback
})

// Utility to get the URL prefix for Profile routing
const rolePrefix = computed(() => {
  switch (currentRole.value) {
    case 'Administrator': return 'admin';
    case 'Officer': return 'officer';
    case 'Worker': return 'worker';
    default: return 'citizen';
  }
})

// Centralized routing logic based on the auto-detected role
const menuItems = computed(() => {
  switch (currentRole.value) {
    case 'Administrator':
      return [
        { name: 'Dashboard', icon: LayoutDashboard, route: '/admin/dashboard' },
        { name: 'Department Management', icon: Building2, route: '/admin/departmentmanagement' },
        { name: 'Officer Management', icon: Users, route: '/admin/officermanagement' },
        { name: 'Officer Details', icon: UserSearch, route: '/admin/officerdetails' },
        { name: 'System Analytics', icon: BarChart3, route: '/admin/systemanalytics' },
        { name: 'Announcements', icon: Megaphone, route: '/admin/announcements' },
        { name: 'Activity Logs', icon: Activity, route: '/admin/activitylogs' },
      ]
      
    case 'Officer':
      return [
        { name: 'Dashboard', icon: LayoutDashboard, route: '/officer/dashboard' },
        { name: 'Department Complaints', icon: ClipboardList, route: '/officer/complaints' },
        { name: 'Complaint Details', icon: FileText, route: '/officer/complaintdetails/CMP-000' },
        { name: 'Assign Worker', icon: UserPlus, route: '/officer/assign/CMP-000' },
        { name: 'Worker Management', icon: HardHat, route: '/officer/workers' },
        { name: 'Analytics & Reports', icon: PieChart, route: '/officer/analytics' },
        { name: 'Notifications', icon: Bell, route: '/officer/notifications' }
      ]

    case 'Worker':
      return [
        { name: 'Dashboard', icon: LayoutDashboard, route: '/worker/dashboard' },
        { name: 'Department Applications', icon: Briefcase, route: '/worker/departmentapplications' },
        { name: 'Assigned Tasks', icon: ListTodo, route: '/worker/tasks' },
        { name: 'Task Details', icon: FileText, route: '/worker/task/CMP-000' },
        { name: 'Update Complaint', icon: Wrench, route: '/worker/update/CMP-000' },
        { name: 'Completed Tasks', icon: CheckSquare, route: '/worker/completed' },
        { name: 'Notifications', icon: Bell, route: '/worker/notifications' }
      ]

    case 'Citizen':
    default:
      return [
        { name: 'Dashboard', icon: LayoutDashboard, route: '/citizen/dashboard' },
        { name: 'Submit Complaint', icon: PlusCircle, route: '/citizen/submit' },
        { name: 'My Complaints', icon: FolderOpen, route: '/citizen/complaints' },
        { name: 'Complaint Details', icon: FileText, route: '/citizen/complaintdetails' },
        { name: 'Complaint Tracking', icon: MapPin, route: '/citizen/track' }, 
        { name: 'Notifications', icon: Bell, route: '/citizen/notifications' },
        { name: 'Feedback', icon: MessageSquare, route: '/citizen/feedback' },
        { name: 'Activity', icon: Activity, route: '/citizen/activity' }
      ]
  }
})

const handleLogout = async () => {
  const token = localStorage.getItem('token')

  if (token) {
    try {
      await axios.post(
        'http://127.0.0.1:5000/api/logout',
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
    } catch (err) {
      // Ignore — clear local state regardless so the user isn't stuck.
    }
  }

  localStorage.removeItem('token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb {background: #334155; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #475569; }
</style>