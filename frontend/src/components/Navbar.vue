<template>
  <!-- 
    The header becomes sticky, and its background transitions from transparent 
    to a solid white with a subtle shadow when the user scrolls down.
  -->
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
      isScrolled ? 'bg-white/95 backdrop-blur-md shadow-sm py-3' : 'bg-transparent py-5'
    ]"
  >
    <div class="max-w-7xl mx-auto px-6 flex items-center justify-between h-full">
      
      <!-- Left Side: Logo & Branding -->
      <div class="flex items-center">
        <router-link to="/" class="flex items-center gap-2.5 group focus:outline-none focus:ring-2 focus:ring-[#2563EB] rounded-lg" aria-label="CivicDesk Home">
          <div class="bg-[#2563EB]/10 p-2 rounded-xl group-hover:bg-[#2563EB]/20 transition-colors">
            <ShieldCheck class="w-7 h-7 text-[#2563EB]" />
          </div>
          <span class="text-2xl font-bold tracking-tight text-slate-900">CivicDesk</span>
        </router-link>
        <!-- Tagline hidden on smaller screens to prevent crowding -->
        <span class="hidden lg:block text-xs font-medium text-slate-500 border-l border-slate-300 pl-3 ml-3 mt-1 tracking-wide">
          Civic Complaint Management Platform
        </span>
      </div>

      <!-- Center: Desktop Navigation -->
      <nav class="hidden md:flex items-center gap-8" aria-label="Main Navigation">
        <router-link
          v-for="link in navLinks"
          :key="link.name"
          :to="link.path"
          class="text-sm font-medium text-slate-600 hover:text-[#2563EB] transition-colors focus:outline-none focus:ring-2 focus:ring-[#2563EB] rounded-md px-2 py-1"
          exact-active-class="text-[#2563EB] !font-semibold"
        >
          {{ link.name }}
        </router-link>
      </nav>

      <!-- Right Side: Auth / Profile Actions -->
      <div class="hidden md:flex items-center gap-4">
        
        <!-- Not Logged In State -->
        <template v-if="!isLoggedIn">
          <router-link
            to="/login"
            class="text-sm font-medium text-slate-600 hover:text-[#2563EB] transition-colors px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
          >
            Login
          </router-link>
          <router-link
            to="/register"
            class="text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] px-5 py-2.5 rounded-lg shadow-sm hover:shadow transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#2563EB]"
          >
            Register
          </router-link>
        </template>

        <!-- Logged In State -->
        <template v-else>
          <button @click="router.push(`/${rolePrefix}/notifications`)" class="relative p-2 text-slate-500 hover:text-[#2563EB] hover:bg-blue-50 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-[#2563EB]" aria-label="Notifications">
            <Bell class="w-5 h-5" />
            <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-[#22C55E] rounded-full border border-white"></span>
          </button>

          <!-- Profile Dropdown -->
          <div class="relative">
            <button 
              @click="toggleProfileDropdown"
              class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-100 border border-slate-200 hover:border-[#2563EB] transition-colors focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
              aria-label="User Menu"
              aria-expanded="isProfileDropdownOpen"
            >
              <User class="w-5 h-5 text-slate-600" />
            </button>

            <!-- Dropdown Menu -->
            <transition name="dropdown">
              <div 
                v-if="isProfileDropdownOpen" 
                class="absolute right-0 mt-3 w-56 bg-white border border-slate-100 rounded-xl shadow-lg py-2 flex flex-col z-50"
              >
                <div class="px-4 py-2 border-b border-slate-100 mb-1">
                  <p class="text-sm font-semibold text-slate-900">{{ currentUser?.name || 'User' }}</p>
                  <p class="text-xs text-slate-500">{{ currentUser?.role || 'Citizen' }} Account</p>
                </div>
                
                <router-link :to="`/${rolePrefix}/dashboard`" class="flex items-center gap-3 px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-[#2563EB] transition-colors" @click="isProfileDropdownOpen = false">
                  <LayoutDashboard class="w-4 h-4" /> Dashboard
                </router-link>
                <router-link :to="`/${rolePrefix}/profile`" class="flex items-center gap-3 px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-[#2563EB] transition-colors" @click="isProfileDropdownOpen = false">
                  <User class="w-4 h-4" /> Profile
                </router-link>
                
                <div class="h-px bg-slate-100 my-1"></div>
                
                <button @click="handleLogout" class="flex items-center gap-3 w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                  <LogOut class="w-4 h-4" /> Logout
                </button>
              </div>
            </transition>
          </div>
        </template>
      </div>

      <!-- Mobile Menu Toggle -->
      <button 
        class="md:hidden p-2 text-slate-600 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-[#2563EB]" 
        @click="isMobileMenuOpen = !isMobileMenuOpen"
        :aria-label="isMobileMenuOpen ? 'Close menu' : 'Open menu'"
      >
        <X v-if="isMobileMenuOpen" class="w-6 h-6" />
        <Menu v-else class="w-6 h-6" />
      </button>
    </div>

    <!-- Mobile Slide-Down Menu -->
    <transition name="slide-down">
      <div 
        v-if="isMobileMenuOpen" 
        class="md:hidden absolute top-full left-0 w-full bg-white border-b border-slate-200 shadow-xl overflow-hidden"
      >
        <div class="px-6 py-4 flex flex-col gap-2">
          <router-link
            v-for="link in navLinks"
            :key="link.name"
            :to="link.path"
            class="text-base font-medium text-slate-700 hover:text-[#2563EB] py-2"
            exact-active-class="text-[#2563EB] font-semibold"
            @click="isMobileMenuOpen = false"
          >
            {{ link.name }}
          </router-link>
          
          <div class="h-px bg-slate-100 my-3"></div>
          
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="text-base font-medium text-slate-700 hover:text-[#2563EB] py-2" @click="isMobileMenuOpen = false">
              Login
            </router-link>
            <router-link to="/register" class="mt-2 text-center text-base font-medium text-white bg-[#2563EB] px-5 py-3 rounded-lg w-full" @click="isMobileMenuOpen = false">
              Register
            </router-link>
          </template>
          
          <template v-else>
            <router-link :to="`/${rolePrefix}/dashboard`" class="flex items-center gap-3 text-base font-medium text-slate-700 hover:text-[#2563EB] py-2" @click="isMobileMenuOpen = false">
              <LayoutDashboard class="w-5 h-5 text-slate-400" /> Dashboard
            </router-link>
            <router-link :to="`/${rolePrefix}/profile`" class="flex items-center gap-3 text-base font-medium text-slate-700 hover:text-[#2563EB] py-2" @click="isMobileMenuOpen = false">
              <User class="w-5 h-5 text-slate-400" /> Profile
            </router-link>
            <button @click="handleLogout" class="flex items-center gap-3 text-base font-medium text-red-600 hover:text-red-700 py-2 w-full text-left">
              <LogOut class="w-5 h-5 opacity-80" /> Logout
            </button>
          </template>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { 
  ShieldCheck, Menu, X, Bell, User, 
  LogOut, LayoutDashboard 
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

// State
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)
const isProfileDropdownOpen = ref(false)
const isLoggedIn = ref(false)
const currentUser = ref(null)

// Reads the auth state that Login.vue/Register.vue write to localStorage.
// Re-checked on every route change so the navbar updates right after
// login/logout without needing a full page reload.
const checkAuthState = () => {
  const token = localStorage.getItem('token')
  const storedUser = localStorage.getItem('user')
  isLoggedIn.value = !!token
  currentUser.value = storedUser ? JSON.parse(storedUser) : null
}

// Mirrors the role-prefix logic in Sidebar.vue / DashboardNavbar.vue so
// Dashboard/Profile/Notifications links here land on real routes.
const rolePrefix = computed(() => {
  switch (currentUser.value?.role) {
    case 'Admin':
    case 'Administrator': return 'admin'
    case 'Officer': return 'officer'
    case 'Worker': return 'worker'
    default: return 'citizen'
  }
})

// Navigation configuration
const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'About', path: '/about' },
  { name: 'Services', path: '/services' },
  { name: 'How It Works', path: '/how-it-works' },
  { name: 'FAQs', path: '/faq' },
  { name: 'Contact', path: '/contact' }
]

// Methods
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

const toggleProfileDropdown = () => {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value
}

const handleLogout = async () => {
  const token = localStorage.getItem('token')

  // Best-effort: tell the backend to blacklist this token. Proceed with
  // local cleanup regardless of whether this succeeds (e.g. token already
  // expired) so the user is never stuck unable to log out.
  if (token) {
    try {
      await axios.post(
        'http://127.0.0.1:5000/api/logout',
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
    } catch (err) {
      // Ignore — we clear local state below no matter what.
    }
  }

  localStorage.removeItem('token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')

  isLoggedIn.value = false
  currentUser.value = null
  isProfileDropdownOpen.value = false
  isMobileMenuOpen.value = false

  router.push('/login')
}

// Lifecycle Hooks
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  checkAuthState()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// Re-check auth state on every navigation (e.g. right after Login.vue
// redirects post-login, or after visiting /logout-adjacent pages).
watch(() => route.fullPath, checkAuthState)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

header {
  font-family: 'Inter', sans-serif;
}

/* Slide Down Animation for Mobile Menu */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease-in-out;
  transform-origin: top;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Dropdown Fade Animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>