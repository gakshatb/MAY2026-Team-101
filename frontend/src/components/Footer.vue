<template>
  <footer class="bg-[#0F172A] text-slate-300 rounded-t-[2.5rem] pt-20 pb-8 px-6 font-sans">
    <div class="max-w-7xl mx-auto">
      
      <!-- Top Grid Section -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-x-8 gap-y-12 mb-16">
        
        <!-- Brand & Description (Spans 4 columns on large screens) -->
        <div class="lg:col-span-4 pr-4">
          <div class="flex items-center gap-2 mb-6 text-white">
            <div class="bg-[#2563EB] p-2 rounded-xl">
              <ShieldCheck class="w-7 h-7 text-white" />
            </div>
            <span class="text-2xl font-bold tracking-tight">CivicDesk</span>
          </div>
          <p class="text-slate-400 text-sm leading-relaxed mb-8">
            CivicDesk helps citizens report civic issues, monitor complaint progress, and improve communication with local authorities to build better, safer communities.
          </p>
          
          <!-- Social Icons -->
          <div class="flex items-center gap-4">
            <a v-for="social in socialLinks" :key="social.name" :href="social.url" :aria-label="social.name" class="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-[#2563EB] hover:-translate-y-1 transition-all duration-300">
              <component :is="social.icon" class="w-4 h-4 text-white" />
            </a>
          </div>
        </div>
        
        <!-- Quick Links -->
        <div class="lg:col-span-2">
          <h4 class="text-white font-bold mb-6 uppercase text-sm tracking-wider">Quick Links</h4>
          <ul class="space-y-4 text-sm">
            <li><router-link to="/" class="hover:text-[#2563EB] transition-colors relative group">Home<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
            <li><router-link to="/about" class="hover:text-[#2563EB] transition-colors relative group">About<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
            <li><router-link to="/services" class="hover:text-[#2563EB] transition-colors relative group">Services<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
            <li><router-link to="/faq" class="hover:text-[#2563EB] transition-colors relative group">FAQs<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
            <li><router-link to="/contact" class="hover:text-[#2563EB] transition-colors relative group">Contact<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
          </ul>
        </div>

        <!-- Platform Links -->
        <div class="lg:col-span-2">
          <h4 class="text-white font-bold mb-6 uppercase text-sm tracking-wider">Platform</h4>
          <ul class="space-y-4 text-sm">
            <li><router-link to="/login" class="hover:text-[#2563EB] transition-colors relative group">Login<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
            <li><router-link to="/register" class="hover:text-[#2563EB] transition-colors relative group">Register<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
            <li><router-link to="/report" class="hover:text-[#2563EB] transition-colors relative group">Report Complaint<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
            <li><router-link to="/track" class="hover:text-[#2563EB] transition-colors relative group">Track Complaint<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></router-link></li>
          </ul>
        </div>

        <!-- Support -->
        <div class="lg:col-span-2">
          <h4 class="text-white font-bold mb-6 uppercase text-sm tracking-wider">Support</h4>
          <ul class="space-y-4 text-sm">
            <li><a href="#" class="hover:text-[#2563EB] transition-colors relative group">Help Center<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></a></li>
            <li><a href="#" class="hover:text-[#2563EB] transition-colors relative group">Privacy Policy<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></a></li>
            <li><a href="#" class="hover:text-[#2563EB] transition-colors relative group">Terms & Conditions<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></a></li>
            <li><a href="#" class="hover:text-[#2563EB] transition-colors relative group">Contact Support<span class="absolute -bottom-1 left-0 w-0 h-[1px] bg-[#2563EB] transition-all group-hover:w-full"></span></a></li>
          </ul>
        </div>
        
        <!-- Contact Information -->
        <div class="lg:col-span-2">
          <h4 class="text-white font-bold mb-6 uppercase text-sm tracking-wider">Contact Info</h4>
          <ul class="space-y-5 text-sm">
            <li class="flex items-start gap-3">
              <Mail class="w-5 h-5 text-[#2563EB] shrink-0 mt-0.5" />
              <a href="mailto:support@civicdesk.in" class="hover:text-white transition-colors">support@civicdesk.in</a>
            </li>
            <li class="flex items-start gap-3">
              <Phone class="w-5 h-5 text-[#2563EB] shrink-0 mt-0.5" />
              <a href="tel:+919876543210" class="hover:text-white transition-colors">+91 98765 43210</a>
            </li>
            <li class="flex items-start gap-3">
              <MapPin class="w-5 h-5 text-[#2563EB] shrink-0 mt-0.5" />
              <address class="not-italic text-slate-400">
                Bhiwandi, Maharashtra,<br />
                India
              </address>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Bottom Footer -->
      <div class="pt-8 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500">
        <p>&copy; 2026 CivicDesk. All Rights Reserved.</p>
        <p class="text-center md:text-right">
          Software Engineering Group Project MAY2026-TEAM-101 <br class="md:hidden" />
          <span class="hidden md:inline">|</span> Indian Institute of Technology Madras
        </p>
      </div>
      
    </div>
  </footer>
</template>

<script setup>
import { 
  ShieldCheck, MapPin, Phone, Mail, 
  Github, Linkedin, Twitter, Facebook, Instagram 
} from 'lucide-vue-next'

// Configuration for social links allowing for simple additions/removals
const socialLinks = [
  { name: 'GitHub', url: '#', icon: Github },
  { name: 'LinkedIn', url: '#', icon: Linkedin },
  { name: 'Twitter', url: '#', icon: Twitter },
  { name: 'Facebook', url: '#', icon: Facebook },
  { name: 'Instagram', url: '#', icon: Instagram }
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

footer {
  font-family: 'Inter', sans-serif;
}
</style>