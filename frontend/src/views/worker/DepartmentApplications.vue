<template>
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar relative">
        
        <!-- Header & Breadcrumbs -->
        <header class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2">
              <span class="hover:text-[#2563EB] cursor-pointer">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900 font-medium">Department Applications</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Department Applications</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Apply to departments, manage active applications, and track your approval status.
            </p>
          </div>
          <div class="bg-white px-5 py-2.5 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-3">
            <Calendar class="w-5 h-5 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Top Statistics Grid -->
        <section class="mb-8 grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
          <div v-for="(stat, index) in topStats" :key="index" class="bg-white p-5 rounded-[14px] shadow-sm hover:shadow-md transition-shadow border border-gray-50 flex flex-col group">
            <div class="flex items-center gap-3 mb-3">
              <div :class="`p-2.5 rounded-lg bg-opacity-10 ${stat.colorClass} bg-current group-hover:scale-110 transition-transform`">
                <component :is="stat.icon" class="w-5 h-5" :class="stat.textClass" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-1">{{ stat.value }}</h3>
            <span class="text-sm text-gray-500 font-medium">{{ stat.label }}</span>
          </div>
        </section>

        <!-- Quick Actions -->
        <section class="mb-8">
          <h2 class="text-lg font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <button v-for="(action, index) in quickActions" :key="index" @click="scrollToSection(action.target)" class="flex items-center gap-3 p-4 bg-white rounded-[14px] border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors group">
              <component :is="action.icon" class="w-5 h-5 text-gray-400 group-hover:text-[#2563EB]" />
              <span class="text-sm font-semibold">{{ action.label }}</span>
            </button>
          </div>
        </section>

        <!-- Search & Filter Section -->
        <section id="browse" class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col xl:flex-row gap-4 items-center justify-between">
          <div class="w-full xl:w-1/3 relative">
            <Search class="w-5 h-5 text-gray-400 absolute left-3 top-3" />
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search departments, codes, or officers..." 
              class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
            />
          </div>
          <div class="w-full xl:w-auto flex flex-wrap gap-3">
            <select v-model="filterStatus" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
              <option value="All">All Statuses</option>
              <option value="Not Applied">Not Applied</option>
              <option value="Pending">Pending</option>
              <option value="Approved">Approved</option>
            </select>
            <select v-model="filterCategory" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
              <option value="All">All Categories</option>
              <option value="Infrastructure">Infrastructure</option>
              <option value="Utilities">Utilities</option>
              <option value="Environment">Environment</option>
            </select>
            <select v-model="sortBy" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
              <option value="Name">Sort by Name</option>
              <option value="Rating">Highest Rating</option>
              <option value="Complaints">Most Complaints</option>
            </select>
            <button @click="resetFilters" class="px-4 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">
              Reset
            </button>
          </div>
        </section>

        <!-- Available Departments Section (Grid) -->
        <section class="mb-10">
          <h2 class="text-lg font-bold text-gray-900 mb-5">Available Departments</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <div v-for="dept in filteredDepartments" :key="dept.id" class="bg-white rounded-[14px] border border-gray-100 shadow-sm hover:shadow-md transition-all p-5 flex flex-col group relative overflow-hidden">
              <div v-if="dept.status !== 'Not Applied'" :class="['absolute top-0 right-0 px-3 py-1 text-[10px] font-bold uppercase tracking-wide rounded-bl-lg', getStatusBgClass(dept.status)]">
                {{ dept.status }}
              </div>
              <div class="flex items-start gap-4 mb-4">
                <div class="w-12 h-12 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0">
                  <component :is="dept.icon" class="w-6 h-6" />
                </div>
                <div>
                  <h3 class="font-bold text-gray-900 leading-tight group-hover:text-[#2563EB] transition-colors">{{ dept.name }}</h3>
                  <p class="text-xs text-gray-500 mt-1">{{ dept.code }} • {{ dept.category }}</p>
                </div>
              </div>
              <p class="text-sm text-gray-600 mb-4 line-clamp-2 flex-1">{{ dept.description }}</p>
              
              <div class="grid grid-cols-2 gap-2 text-sm mb-5">
                <div class="bg-gray-50 p-2 rounded-lg text-center">
                  <p class="text-xs text-gray-500 mb-0.5">Rating</p>
                  <p class="font-bold text-gray-900 flex items-center justify-center gap-1"><Award class="w-3 h-3 text-yellow-500"/> {{ dept.rating }}</p>
                </div>
                <div class="bg-gray-50 p-2 rounded-lg text-center">
                  <p class="text-xs text-gray-500 mb-0.5">Active Tasks</p>
                  <p class="font-bold text-gray-900">{{ dept.activeComplaints }}</p>
                </div>
              </div>

              <div class="flex gap-3">
                <button @click="openDrawer(dept)" class="flex-1 py-2 bg-gray-50 text-gray-700 rounded-xl text-sm font-medium hover:bg-gray-100 transition-colors border border-gray-200">
                  Details
                </button>
                <button 
                  v-if="dept.status === 'Not Applied'" 
                  @click="openModal('apply', dept)" 
                  class="flex-1 py-2 bg-[#2563EB] text-white rounded-xl text-sm font-medium hover:bg-[#1E40AF] transition-colors shadow-sm"
                >
                  Apply Now
                </button>
                <button 
                  v-else-if="dept.status === 'Pending'" 
                  @click="openModal('withdraw', dept)" 
                  class="flex-1 py-2 bg-yellow-50 text-yellow-700 border border-yellow-200 rounded-xl text-sm font-medium hover:bg-yellow-100 transition-colors"
                >
                  Withdraw
                </button>
                <button 
                  v-else-if="dept.status === 'Approved'" 
                  class="flex-1 py-2 bg-green-50 text-green-700 border border-green-200 rounded-xl text-sm font-medium hover:bg-green-100 transition-colors cursor-default"
                >
                  Approved
                </button>
              </div>
            </div>
            
            <!-- Empty State -->
            <div v-if="filteredDepartments.length === 0" class="col-span-full py-12 text-center bg-white rounded-[14px] border border-gray-100">
              <Search class="w-10 h-10 text-gray-300 mx-auto mb-3" />
              <h3 class="text-lg font-medium text-gray-900">No departments found</h3>
              <p class="text-gray-500 text-sm mt-1">Try adjusting your search or filters.</p>
            </div>
          </div>
        </section>

        <!-- My Applications Table (Desktop) & Cards (Mobile) -->
        <section id="applications" class="mb-10">
          <h2 class="text-lg font-bold text-gray-900 mb-5">My Application History</h2>
          
          <!-- Desktop Table -->
          <div class="hidden md:block bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="p-4 font-semibold">App ID</th>
                  <th class="p-4 font-semibold">Department</th>
                  <th class="p-4 font-semibold">Applied Date</th>
                  <th class="p-4 font-semibold">Status</th>
                  <th class="p-4 font-semibold">Officer Remarks</th>
                  <th class="p-4 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm">
                <tr v-for="app in applications" :key="app.id" class="hover:bg-gray-50 transition-colors">
                  <td class="p-4 font-medium text-gray-900">{{ app.id }}</td>
                  <td class="p-4 font-medium text-gray-900">{{ app.deptName }}</td>
                  <td class="p-4 text-gray-600">{{ app.date }}</td>
                  <td class="p-4">
                    <span :class="['px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 w-max', getStatusClass(app.status)]">
                      <span class="w-1.5 h-1.5 rounded-full bg-current"></span> {{ app.status }}
                    </span>
                  </td>
                  <td class="p-4 text-gray-500 text-xs max-w-[200px] truncate">{{ app.remarks || 'Pending review...' }}</td>
                  <td class="p-4 text-right">
                    <button v-if="app.status === 'Pending'" @click="openModal('withdraw', {name: app.deptName})" class="text-sm font-medium text-red-600 hover:text-red-800">Withdraw</button>
                    <button v-else-if="app.status === 'Rejected'" class="text-sm font-medium text-[#2563EB] hover:text-[#1E40AF]">Reapply</button>
                    <span v-else class="text-sm text-gray-400">Assigned</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile Cards -->
          <div class="md:hidden space-y-4">
            <div v-for="app in applications" :key="app.id" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50">
              <div class="flex justify-between items-start mb-2">
                <h3 class="font-bold text-gray-900">{{ app.deptName }}</h3>
                <span :class="['px-2 py-0.5 rounded-full text-[10px] font-semibold flex items-center gap-1', getStatusClass(app.status)]">
                  {{ app.status }}
                </span>
              </div>
              <div class="text-xs text-gray-500 mb-3 space-y-1">
                <p>App ID: <span class="font-medium text-gray-900">{{ app.id }}</span></p>
                <p>Date: <span class="font-medium text-gray-900">{{ app.date }}</span></p>
                <p v-if="app.remarks" class="italic mt-2 text-gray-600">"{{ app.remarks }}"</p>
              </div>
              <button v-if="app.status === 'Pending'" @click="openModal('withdraw', {name: app.deptName})" class="w-full py-2 bg-red-50 text-red-700 rounded-lg text-sm font-medium hover:bg-red-100 transition-colors">Withdraw Application</button>
            </div>
          </div>
        </section>

        <!-- Two Column Grid for Info sections -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          
          <!-- Application Status Timeline -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
              <Clock class="w-5 h-5 text-[#2563EB]" /> Application Timeline (Recent)
            </h2>
            <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
              <div class="relative pl-6">
                <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-green-500"></span>
                <div class="flex justify-between items-baseline mb-0.5">
                  <h4 class="text-sm font-semibold text-gray-900">Approved for Garbage Management</h4>
                  <span class="text-xs text-gray-400">Jul 10, 2026</span>
                </div>
                <p class="text-sm text-gray-500 mt-1">Officer R. Singh has approved your profile. You are now eligible to receive assignments.</p>
              </div>
              <div class="relative pl-6">
                <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-yellow-500"></span>
                <div class="flex justify-between items-baseline mb-0.5">
                  <h4 class="text-sm font-semibold text-gray-900">Under Review - Road Maintenance</h4>
                  <span class="text-xs text-gray-400">Jul 08, 2026</span>
                </div>
                <p class="text-sm text-gray-500 mt-1">Your application is currently being reviewed by Officer A. Patel.</p>
              </div>
              <div class="relative pl-6">
                <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-gray-300"></span>
                <div class="flex justify-between items-baseline mb-0.5">
                  <h4 class="text-sm font-semibold text-gray-900">Application Submitted</h4>
                  <span class="text-xs text-gray-400">Jul 07, 2026</span>
                </div>
                <p class="text-sm text-gray-500 mt-1">You applied to Road Maintenance.</p>
              </div>
            </div>
          </section>

          <!-- Required Skills & Tips -->
          <div class="space-y-6">
            <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6">
              <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Hammer class="w-5 h-5 text-[#F59E0B]" /> Required Skills
              </h2>
              <div class="flex flex-wrap gap-2">
                <span v-for="(skill, index) in requiredSkills" :key="index" class="px-3 py-1.5 bg-gray-50 border border-gray-200 text-gray-700 rounded-lg text-sm font-medium">
                  {{ skill }}
                </span>
              </div>
            </section>
            
            <section class="bg-[#2563EB] rounded-[14px] shadow-sm border border-[#1E40AF] p-6 text-white relative overflow-hidden">
              <div class="absolute right-0 top-0 opacity-10">
                <BadgeCheck class="w-32 h-32 transform translate-x-8 -translate-y-8" />
              </div>
              <h2 class="text-lg font-bold mb-3 flex items-center gap-2 relative z-10">
                <Lightbulb class="w-5 h-5" /> Tips for Success
              </h2>
              <ul class="space-y-2 text-sm text-blue-100 relative z-10">
                <li class="flex items-start gap-2"><CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-blue-300"/> Complete your profile fully before applying.</li>
                <li class="flex items-start gap-2"><CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-blue-300"/> Apply only to departments that match your skill set.</li>
                <li class="flex items-start gap-2"><CheckCircle class="w-4 h-4 mt-0.5 shrink-0 text-blue-300"/> Maintaining a good resolution time leads to better ratings.</li>
              </ul>
            </section>
          </div>

        </div>
      </main>

    <!-- Department Details Drawer -->
    <div v-if="isDrawerOpen && selectedDept" class="fixed inset-0 z-50 overflow-hidden" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
      <div class="absolute inset-0 bg-slate-900/40 transition-opacity" @click="closeDrawer"></div>
      <div class="fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-2xl flex flex-col transform transition-transform duration-300 ease-in-out border-l border-gray-100">
        
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl bg-[#2563EB] text-white flex items-center justify-center">
              <component :is="selectedDept.icon" class="w-6 h-6" />
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-900">{{ selectedDept.name }}</h2>
              <p class="text-sm text-gray-500">{{ selectedDept.code }}</p>
            </div>
          </div>
          <button @click="closeDrawer" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-6">
          <div>
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2">Description</h3>
            <p class="text-sm text-gray-600 leading-relaxed">{{ selectedDept.description }}</p>
          </div>

          <div>
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Department Head</h3>
            <div class="flex items-center gap-3 p-3 rounded-xl border border-gray-100 bg-gray-50">
              <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center"><User class="w-5 h-5 text-gray-500"/></div>
              <div>
                <p class="font-bold text-gray-900 text-sm">{{ selectedDept.head }}</p>
                <p class="text-xs text-gray-500">Officer: {{ selectedDept.officer }}</p>
              </div>
            </div>
          </div>

          <div>
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Metrics & Requirements</h3>
            <ul class="space-y-3 text-sm">
              <li class="flex justify-between border-b border-gray-100 pb-2">
                <span class="text-gray-500">Current Field Workers</span>
                <span class="font-semibold text-gray-900">{{ selectedDept.workers }}</span>
              </li>
              <li class="flex justify-between border-b border-gray-100 pb-2">
                <span class="text-gray-500">Average Resolution Time</span>
                <span class="font-semibold text-gray-900">{{ selectedDept.avgResTime }}</span>
              </li>
              <li class="flex justify-between border-b border-gray-100 pb-2">
                <span class="text-gray-500">Department Rating</span>
                <span class="font-bold text-gray-900 flex items-center gap-1"><Award class="w-4 h-4 text-yellow-500"/> {{ selectedDept.rating }}/5.0</span>
              </li>
            </ul>
          </div>

          <div>
             <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Working Areas</h3>
             <div class="flex flex-wrap gap-2">
               <span class="px-2.5 py-1 bg-blue-50 text-blue-700 border border-blue-100 rounded-md text-xs font-medium">North Zone</span>
               <span class="px-2.5 py-1 bg-blue-50 text-blue-700 border border-blue-100 rounded-md text-xs font-medium">South Zone</span>
               <span class="px-2.5 py-1 bg-blue-50 text-blue-700 border border-blue-100 rounded-md text-xs font-medium">Central Hub</span>
             </div>
          </div>
        </div>

        <div class="p-4 border-t border-gray-100 bg-gray-50">
          <button v-if="selectedDept.status === 'Not Applied'" @click="openModal('apply', selectedDept)" class="w-full py-3 bg-[#2563EB] text-white font-bold rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm">
            Apply to Department
          </button>
          <button v-else-if="selectedDept.status === 'Pending'" class="w-full py-3 bg-gray-300 text-gray-700 font-bold rounded-xl cursor-not-allowed">
            Application Pending
          </button>
          <button v-else-if="selectedDept.status === 'Approved'" class="w-full py-3 bg-green-600 text-white font-bold rounded-xl cursor-not-allowed">
            Already Approved
          </button>
        </div>
      </div>
    </div>

    <!-- Modals Overlay Container -->
    <div v-if="activeModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/50 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
      
      <!-- Application Modal -->
      <div v-if="activeModal === 'apply'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 transform transition-all">
        <h2 class="text-xl font-bold text-gray-900 mb-1">Apply to {{ targetDept?.name }}</h2>
        <p class="text-sm text-gray-500 mb-5">Submit your profile to the officer for review.</p>
        
        <form @submit.prevent="submitApplication" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Years of Experience</label>
            <select class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none">
              <option>Less than 1 year</option>
              <option>1-3 Years</option>
              <option>3-5 Years</option>
              <option>5+ Years</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Relevant Skills</label>
            <input type="text" class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none" placeholder="e.g. Electrical Repair, Welding..." />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Additional Notes for Officer</label>
            <textarea rows="3" class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none custom-scrollbar" placeholder="Highlight why you are a good fit..."></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Supporting Document / Resume</label>
            <div class="border-2 border-dashed border-gray-200 rounded-xl p-4 text-center hover:bg-gray-50 transition-colors cursor-pointer">
              <Upload class="w-6 h-6 text-gray-400 mx-auto mb-2" />
              <span class="text-xs text-gray-500 font-medium">Click to upload PDF or Image</span>
            </div>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
            <button type="button" @click="closeModal" class="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
            <button type="submit" class="px-5 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl transition-colors shadow-sm">Submit Application</button>
          </div>
        </form>
      </div>

      <!-- Withdraw Modal -->
      <div v-if="activeModal === 'withdraw'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center transform transition-all">
        <div class="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <AlertTriangle class="w-8 h-8" />
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Withdraw Application?</h2>
        <p class="text-sm text-gray-500 mb-6">
          Are you sure you want to withdraw your pending application for <strong class="text-gray-900">{{ targetDept?.name }}</strong>? You will need to apply again later.
        </p>
        <div class="flex justify-center gap-3">
          <button @click="closeModal" class="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
          <button @click="withdrawApplication" class="px-5 py-2 text-sm font-medium text-white bg-[#EF4444] hover:bg-red-700 rounded-xl transition-colors shadow-sm">Withdraw</button>
        </div>
      </div>
    </div>

</template>

<script setup>
import { ref, computed } from 'vue';
// Adjust paths as needed for your project structure
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';

// Icons
import { 
  Building2, Building, Users, UserCheck, ClipboardList, Briefcase, 
  FileCheck, CheckCircle, Clock, Calendar, Search, Filter, Eye, 
  ArrowRight, ShieldCheck, Award, MapPin, Hammer, Wrench, BadgeCheck, 
  FileText, Upload, AlertTriangle, Lightbulb, User, X
} from 'lucide-vue-next';

// Layout State
const sidebarOpen = ref(false);
const isDrawerOpen = ref(false);
const activeModal = ref(null);
const selectedDept = ref(null);
const targetDept = ref(null);

const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

// --- Dummy Data ---
const topStats = ref([
  { label: 'Available Depts', value: '12', icon: Building, colorClass: 'text-gray-600 bg-gray-100', textClass: 'text-gray-600' },
  { label: 'Applied', value: '4', icon: Briefcase, colorClass: 'text-[#2563EB] bg-blue-100', textClass: 'text-[#2563EB]' },
  { label: 'Approved', value: '2', icon: ShieldCheck, colorClass: 'text-[#22C55E] bg-green-100', textClass: 'text-[#22C55E]' },
  { label: 'Pending', value: '1', icon: Clock, colorClass: 'text-[#F59E0B] bg-yellow-100', textClass: 'text-[#F59E0B]' },
  { label: 'Rejected', value: '1', icon: AlertTriangle, colorClass: 'text-[#EF4444] bg-red-100', textClass: 'text-[#EF4444]' },
  { label: 'Total Apps', value: '5', icon: ClipboardList, colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' }
]);

const quickActions = ref([
  { label: 'Browse Depts', icon: Search, target: 'browse' },
  { label: 'My Applications', icon: FileText, target: 'applications' },
  { label: 'Update Profile', icon: User, target: null },
  { label: 'History', icon: Clock, target: null }
]);

const departments = ref([
  { id: 1, name: 'Garbage Management', code: 'DEPT-GM', category: 'Environment', description: 'Handles solid waste collection, disposal, and street cleaning across municipal zones.', head: 'Ramesh Singh', officer: 'R. Singh', workers: 145, activeComplaints: 142, avgResTime: '24h', rating: 4.6, status: 'Approved', icon: Wrench },
  { id: 2, name: 'Road Maintenance', code: 'DEPT-RM', category: 'Infrastructure', description: 'Responsible for repairing potholes, maintaining pavements, and infrastructure safety.', head: 'Anita Patel', officer: 'A. Patel', workers: 90, activeComplaints: 305, avgResTime: '72h', rating: 4.2, status: 'Pending', icon: MapPin },
  { id: 3, name: 'Street Lighting', code: 'DEPT-SL', category: 'Utilities', description: 'Manages repair and installation of electrical street lights and poles.', head: 'Vikram Joshi', officer: 'V. Joshi', workers: 45, activeComplaints: 45, avgResTime: '12h', rating: 4.8, status: 'Not Applied', icon: Lightbulb },
  { id: 4, name: 'Water Supply', code: 'DEPT-WS', category: 'Utilities', description: 'Handles pipe leakages, water pressure issues, and reservoir maintenance.', head: 'Priya Desai', officer: 'P. Desai', workers: 85, activeComplaints: 85, avgResTime: '18h', rating: 4.5, status: 'Approved', icon: Wrench },
  { id: 5, name: 'Drainage & Sewer', code: 'DEPT-DS', category: 'Infrastructure', description: 'Maintains underground sewage lines, open drains, and flood prevention systems.', head: 'Sanjay Kumar', officer: 'S. Kumar', workers: 110, activeComplaints: 210, avgResTime: '48h', rating: 3.9, status: 'Rejected', icon: Hammer },
  { id: 6, name: 'Parks & Gardens', code: 'DEPT-PG', category: 'Environment', description: 'Upkeep of public parks, tree pruning, and landscaping.', head: 'Meera Reddy', officer: 'M. Reddy', workers: 30, activeComplaints: 12, avgResTime: '20h', rating: 4.9, status: 'Not Applied', icon: Building2 }
]);


const applications = ref([
  { id: 'APP-1042', deptName: 'Garbage Management', date: 'Jul 10, 2026', status: 'Approved', officer: 'R. Singh', remarks: 'Welcome to the team.' },
  { id: 'APP-1035', deptName: 'Water Supply', date: 'Jun 28, 2026', status: 'Approved', officer: 'P. Desai', remarks: 'Good plumbing experience.' },
  { id: 'APP-1050', deptName: 'Road Maintenance', date: 'Jul 08, 2026', status: 'Pending', officer: 'A. Patel', remarks: '' },
  { id: 'APP-1022', deptName: 'Drainage & Sewer', date: 'May 15, 2026', status: 'Rejected', officer: 'S. Kumar', remarks: 'Requires heavy machinery license.' }
]);

const requiredSkills = ref([
  'Electrical Repair', 'Plumbing', 'Road Surfacing', 'Waste Management', 'Heavy Machinery Operation', 'Carpentry', 'General Maintenance'
]);

// --- Search & Filter Logic ---
const searchQuery = ref('');
const filterStatus = ref('All');
const filterCategory = ref('All');
const sortBy = ref('Name');

const filteredDepartments = computed(() => {
  let result = departments.value;

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(d => d.name.toLowerCase().includes(q) || d.code.toLowerCase().includes(q) || d.officer.toLowerCase().includes(q));
  }
  if (filterStatus.value !== 'All') {
    result = result.filter(d => d.status === filterStatus.value);
  }
  if (filterCategory.value !== 'All') {
    result = result.filter(d => d.category === filterCategory.value);
  }

  result = [...result].sort((a, b) => {
    if (sortBy.value === 'Name') return a.name.localeCompare(b.name);
    if (sortBy.value === 'Rating') return b.rating - a.rating;
    if (sortBy.value === 'Complaints') return b.activeComplaints - a.activeComplaints;
    return 0;
  });

  return result;
});

const resetFilters = () => {
  searchQuery.value = '';
  filterStatus.value = 'All';
  filterCategory.value = 'All';
  sortBy.value = 'Name';
};

// --- UI Helpers ---
const getStatusClass = (status) => {
  switch(status) {
    case 'Approved': return 'bg-green-50 text-green-700 border border-green-200';
    case 'Pending': return 'bg-yellow-50 text-yellow-700 border border-yellow-200';
    case 'Rejected': return 'bg-red-50 text-red-700 border border-red-200';
    default: return 'bg-gray-100 text-gray-600 border border-gray-200';
  }
};

const getStatusBgClass = (status) => {
  switch(status) {
    case 'Approved': return 'bg-green-500 text-white';
    case 'Pending': return 'bg-yellow-500 text-white';
    case 'Rejected': return 'bg-red-500 text-white';
    default: return 'bg-gray-200 text-gray-600';
  }
};

const scrollToSection = (id) => {
  if(!id) return;
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

// --- Interactions ---
const openDrawer = (dept) => {
  selectedDept.value = dept;
  isDrawerOpen.value = true;
};
const closeDrawer = () => {
  isDrawerOpen.value = false;
  setTimeout(() => { selectedDept.value = null; }, 300);
};

const openModal = (type, dept = null) => {
  activeModal.value = type;
  if(dept) targetDept.value = dept;
};
const closeModal = () => {
  activeModal.value = null;
  targetDept.value = null;
};

const submitApplication = () => {
  // In a real app, you would make an axios call here.
  // For UI flow: change status to Pending, close modal, close drawer.
  if(targetDept.value) {
     targetDept.value.status = 'Pending';
  }
  closeModal();
  closeDrawer();
};

const withdrawApplication = () => {
  // Simulate withdrawal
  if(targetDept.value) {
      const dept = departments.value.find(d => d.name === targetDept.value.name);
      if(dept) dept.status = 'Not Applied';
  }
  closeModal();
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

/* Custom Scrollbars */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #CBD5E1;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94A3B8;
}

/* Page Entry Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

/* Line Clamp for long descriptions */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>