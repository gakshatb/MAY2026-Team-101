<template>
  <div class="flex h-screen overflow-hidden bg-[#F8FAFC] font-sans">
    

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">
      
      
      <!-- Scrollable Dashboard Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">
        
        <!-- Header & Breadcrumbs -->
        <header class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">Profile</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Administrator Profile</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Manage your account information, security settings, and personal preferences.
            </p>
          </div>
          <div class="bg-white px-5 py-2.5 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-3 shrink-0">
            <Calendar class="w-5 h-5 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Top Section: Banner, Profile Hero & Completion -->
        <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-6">
          
          <!-- Banner & Profile Card -->
          <section class="xl:col-span-2 bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden flex flex-col">
            <!-- Cover Banner -->
            <div class="h-32 md:h-48 w-full relative group">
              <img :src="profile.cover" alt="Cover" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button class="px-4 py-2 bg-white/90 backdrop-blur text-gray-800 text-sm font-bold rounded-xl shadow-sm flex items-center gap-2 hover:bg-white transition-colors">
                  <Camera class="w-4 h-4" /> Change Cover
                </button>
              </div>
            </div>
            <!-- Profile Info -->
            <div class="px-6 pb-6 relative flex-1 flex flex-col">
              <div class="flex flex-col md:flex-row gap-6 items-start md:items-center -mt-12 md:-mt-16 mb-4">
                <div class="relative group">
                  <img :src="profile.avatar" alt="Avatar" class="w-24 h-24 md:w-32 md:h-32 rounded-2xl border-4 border-white object-cover shadow-sm bg-white" />
                  <button class="absolute bottom-2 right-2 p-2 bg-gray-900 text-white rounded-lg shadow-sm opacity-0 group-hover:opacity-100 transition-opacity hover:bg-[#2563EB]">
                    <Upload class="w-4 h-4" />
                  </button>
                </div>
                <div class="flex-1 pt-2 md:pt-16">
                  <div class="flex flex-col md:flex-row md:items-center gap-3 mb-1">
                    <h2 class="text-2xl font-bold text-gray-900">{{ profile.name }}</h2>
                    <div class="flex flex-wrap gap-2">
                      <span class="px-2.5 py-0.5 bg-blue-100 text-blue-700 text-[10px] font-bold uppercase rounded-md flex items-center gap-1"><ShieldCheck class="w-3 h-3"/> System Admin</span>
                      <span class="px-2.5 py-0.5 bg-purple-100 text-purple-700 text-[10px] font-bold uppercase rounded-md">Super Admin</span>
                      <span class="px-2.5 py-0.5 bg-green-100 text-green-700 text-[10px] font-bold uppercase rounded-md flex items-center gap-1"><CheckCircle class="w-3 h-3"/> Active</span>
                    </div>
                  </div>
                  <p class="text-[#2563EB] font-medium">{{ profile.designation }} • {{ profile.department }}</p>
                </div>
                <div class="flex gap-3 w-full md:w-auto md:pt-16">
                  <button class="flex-1 md:flex-none px-5 py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-bold rounded-xl hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
                    <Pencil class="w-4 h-4"/> Edit
                  </button>
                  <button class="flex-1 md:flex-none px-5 py-2.5 bg-[#2563EB] text-white text-sm font-bold rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2">
                    <KeyRound class="w-4 h-4"/> Password
                  </button>
                </div>
              </div>
              <!-- Contact Details Grid -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-auto pt-4 border-t border-gray-50">
                <div><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Admin ID</p><p class="text-sm font-semibold text-gray-900 flex items-center gap-1.5"><BadgeCheck class="w-4 h-4 text-[#2563EB]"/> {{ profile.id }}</p></div>
                <div><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Email</p><p class="text-sm font-semibold text-gray-900 flex items-center gap-1.5 truncate"><Mail class="w-4 h-4 text-gray-400"/> {{ profile.email }}</p></div>
                <div><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Phone</p><p class="text-sm font-semibold text-gray-900 flex items-center gap-1.5"><Phone class="w-4 h-4 text-gray-400"/> {{ profile.phone }}</p></div>
                <div><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Joining Date</p><p class="text-sm font-semibold text-gray-900 flex items-center gap-1.5"><Calendar class="w-4 h-4 text-gray-400"/> {{ profile.joinDate }}</p></div>
              </div>
            </div>
          </section>

          <!-- Profile Completion & Access Summary -->
          <section class="xl:col-span-1 flex flex-col gap-6">
            <!-- Completion Card -->
            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex items-center gap-6">
              <div class="relative w-24 h-24 shrink-0 flex items-center justify-center">
                <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path class="text-gray-100" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  <path class="text-[#22C55E] transition-all duration-1000 ease-out" stroke-width="3" stroke-dasharray="85, 100" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                </svg>
                <div class="absolute flex flex-col items-center justify-center">
                  <span class="text-xl font-bold text-gray-900">85%</span>
                </div>
              </div>
              <div class="flex-1">
                <h3 class="text-sm font-bold text-gray-900 mb-2">Profile Completion</h3>
                <ul class="space-y-1.5 text-xs text-gray-600">
                  <li class="flex items-center gap-2"><CheckCircle class="w-3.5 h-3.5 text-green-500"/> Avatar uploaded</li>
                  <li class="flex items-center gap-2"><CheckCircle class="w-3.5 h-3.5 text-green-500"/> Phone verified</li>
                  <li class="flex items-center gap-2 text-gray-400"><span class="w-3.5 h-3.5 rounded-full border-2 border-gray-300 inline-block"></span> Add emergency contact</li>
                  <li class="flex items-center gap-2 text-gray-400"><span class="w-3.5 h-3.5 rounded-full border-2 border-gray-300 inline-block"></span> Complete address</li>
                </ul>
              </div>
            </div>

            <!-- Access Summary -->
            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex-1">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
                <ShieldCheck class="w-4 h-4 text-[#2563EB]" /> System Access Summary
              </h3>
              <div class="space-y-3">
                <div class="flex justify-between items-center p-3 bg-gray-50 rounded-xl border border-gray-100">
                  <span class="text-xs font-semibold text-gray-600">Permission Level</span>
                  <span class="text-xs font-bold text-purple-700 bg-purple-100 px-2 py-0.5 rounded">Level 5 (Max)</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-gray-50 rounded-xl border border-gray-100">
                  <span class="text-xs font-semibold text-gray-600">Managed Departments</span>
                  <span class="text-xs font-bold text-gray-900">All (12)</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-gray-50 rounded-xl border border-gray-100">
                  <span class="text-xs font-semibold text-gray-600">Managed Officers</span>
                  <span class="text-xs font-bold text-gray-900">128</span>
                </div>
              </div>
            </div>
          </section>

        </div>

        <!-- Profile Statistics Cards -->
        <section class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
          <div v-for="(stat, index) in stats" :key="index" class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 flex flex-col group hover:border-[#2563EB] transition-colors">
            <div class="flex items-center justify-between mb-3">
              <div :class="`p-2.5 rounded-xl bg-opacity-10 ${stat.colorClass} bg-current group-hover:scale-110 transition-transform duration-300`">
                <component :is="stat.icon" class="w-5 h-5" :class="stat.textClass" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-0.5">{{ stat.value }}</h3>
            <span class="text-xs text-gray-500 font-semibold uppercase tracking-wide truncate">{{ stat.label }}</span>
          </div>
        </section>

        <!-- Main Content Layout (Two Columns) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          
          <!-- Left Column (Personal Info, Permissions, Responsibilities) -->
          <div class="lg:col-span-2 space-y-6">
            
            <!-- Personal Information -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <div class="flex justify-between items-center mb-5">
                <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
                  <User class="w-4 h-4 text-[#2563EB]" /> Personal Information
                </h3>
                <button class="text-xs font-bold text-[#2563EB] hover:underline">Edit Info</button>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Full Name</span><span class="text-sm font-semibold text-gray-900">{{ personal.name }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Date of Birth</span><span class="text-sm font-semibold text-gray-900">{{ personal.dob }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Gender</span><span class="text-sm font-semibold text-gray-900">{{ personal.gender }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Nationality</span><span class="text-sm font-semibold text-gray-900">{{ personal.nationality }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2 md:col-span-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Residential Address</span><span class="text-sm font-semibold text-gray-900">{{ personal.address }}, {{ personal.city }}, {{ personal.state }}, {{ personal.country }} - {{ personal.zip }}</span></div>
                <div class="flex flex-col pt-1 md:col-span-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Emergency Contact</span><span class="text-sm font-semibold text-red-600">{{ personal.emergency }}</span></div>
              </div>
            </section>

            <!-- Administrator Permissions -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <BadgeCheck class="w-4 h-4 text-[#2563EB]" /> Administrator Permissions
              </h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div v-for="perm in permissions" :key="perm.name" class="p-4 border border-gray-100 rounded-xl bg-gray-50 hover:bg-white hover:border-[#2563EB] transition-colors group">
                  <div class="flex justify-between items-start mb-2">
                    <h4 class="font-bold text-gray-900 text-sm group-hover:text-[#2563EB] transition-colors">{{ perm.name }}</h4>
                    <span class="px-2 py-0.5 bg-blue-100 text-[#2563EB] text-[9px] font-bold uppercase rounded">{{ perm.level }}</span>
                  </div>
                  <p class="text-xs text-gray-500 leading-snug">{{ perm.desc }}</p>
                </div>
              </div>
            </section>

            <!-- Recent Login History Table -->
            <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden flex flex-col">
              <div class="p-6 border-b border-gray-100 bg-white">
                <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
                  <History class="w-4 h-4 text-[#2563EB]" /> Recent Login History
                </h3>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr class="bg-gray-50 text-gray-500 text-[10px] uppercase tracking-wider font-bold">
                      <th class="p-4 whitespace-nowrap">Date & Time</th>
                      <th class="p-4 whitespace-nowrap">Device / OS</th>
                      <th class="p-4 whitespace-nowrap">Browser</th>
                      <th class="p-4 whitespace-nowrap">IP Address</th>
                      <th class="p-4 whitespace-nowrap text-center">Status</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100 text-sm">
                    <tr v-for="log in loginHistory" :key="log.id" class="hover:bg-gray-50 transition-colors">
                      <td class="p-4"><p class="font-bold text-gray-900">{{ log.date }}</p><p class="text-xs text-gray-500">{{ log.time }}</p></td>
                      <td class="p-4">
                        <p class="font-medium text-gray-900 flex items-center gap-1.5"><Laptop v-if="log.device==='Desktop'" class="w-3.5 h-3.5 text-gray-400"/><Smartphone v-else class="w-3.5 h-3.5 text-gray-400"/> {{ log.device }}</p>
                        <p class="text-xs text-gray-500">{{ log.os }}</p>
                      </td>
                      <td class="p-4 text-gray-600 font-medium">{{ log.browser }}</td>
                      <td class="p-4 text-gray-500 font-mono text-xs">{{ log.ip }}</td>
                      <td class="p-4 text-center">
                        <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', log.status === 'Success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">{{ log.status }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>

          </div>

          <!-- Right Column (Security, Preferences, Timelines) -->
          <div class="lg:col-span-1 space-y-6">
            
            <!-- Quick Actions -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
               <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Quick Actions</h3>
               <div class="grid grid-cols-2 gap-3">
                 <button v-for="action in quickActions" :key="action.name" class="flex flex-col items-center justify-center p-3 bg-gray-50 border border-gray-100 rounded-xl hover:bg-blue-50 hover:border-[#2563EB] hover:text-[#2563EB] transition-colors text-gray-700 group">
                   <component :is="action.icon" class="w-5 h-5 mb-1.5 text-gray-400 group-hover:text-[#2563EB]"/>
                   <span class="text-[11px] font-bold text-center leading-tight">{{ action.name }}</span>
                 </button>
               </div>
            </section>

            <!-- Account Security Section -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <Lock class="w-4 h-4 text-[#2563EB]" /> Account Security
              </h3>
              <ul class="space-y-4 text-sm mb-5">
                <li class="flex flex-col gap-1 border-b border-gray-50 pb-3">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Password Status</span><span class="text-xs text-green-600 font-bold bg-green-50 px-2 py-0.5 rounded">Strong</span></div>
                  <span class="text-xs text-gray-500">Last changed: {{ security.lastPasswordChange }}</span>
                </li>
                <li class="flex flex-col gap-1 border-b border-gray-50 pb-3">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Two-Factor Auth (2FA)</span><span class="text-xs text-[#2563EB] font-bold bg-blue-50 px-2 py-0.5 rounded">Enabled</span></div>
                  <span class="text-xs text-gray-500">Authenticator App configured</span>
                </li>
                <li class="flex flex-col gap-1 border-b border-gray-50 pb-3">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Recovery Email</span></div>
                  <span class="text-xs text-gray-500 truncate">{{ security.recoveryEmail }}</span>
                </li>
                <li class="flex flex-col gap-1 border-b border-gray-50 pb-3">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Active Sessions</span><span class="text-xs text-gray-700 font-bold bg-gray-100 px-2 py-0.5 rounded">{{ security.activeSessions }}</span></div>
                </li>
                <li class="flex flex-col gap-1 pt-1">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Trusted Devices</span><span class="text-xs text-gray-700 font-bold bg-gray-100 px-2 py-0.5 rounded">{{ security.trustedDevices }}</span></div>
                </li>
              </ul>
              <div class="flex flex-col gap-2">
                <button class="w-full py-2 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 transition-colors">Manage Devices</button>
                <button class="w-full py-2 bg-[#2563EB] text-white text-sm font-semibold rounded-xl hover:bg-[#1E40AF] shadow-sm transition-colors">Change Password</button>
              </div>
            </section>

            <!-- Notification Preferences -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <Bell class="w-4 h-4 text-[#2563EB]" /> Notification Preferences
              </h3>
              <div class="space-y-4 mb-6">
                <div v-for="(pref, key) in notificationPrefs" :key="key" class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-700">{{ pref.label }}</span>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="pref.value" class="sr-only peer">
                    <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#2563EB]"></div>
                  </label>
                </div>
              </div>
              <button class="w-full py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
                <Save class="w-4 h-4"/> Save Preferences
              </button>
            </section>

            <!-- Appearance Preferences -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <Palette class="w-4 h-4 text-[#2563EB]" /> Appearance & Localization
              </h3>
              <div class="space-y-4 mb-6">
                <div>
                  <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5">Theme</label>
                  <select class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
                    <option>System Default</option><option>Light Theme</option><option>Dark Theme</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5">Language</label>
                  <select class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
                    <option>English (US)</option><option>Hindi</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-bold text-gray-500 uppercase mb-1.5">Time Zone</label>
                  <select class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
                    <option>(GMT+05:30) India Standard Time</option><option>(GMT+00:00) UTC</option>
                  </select>
                </div>
              </div>
              <button class="w-full py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
                <Save class="w-4 h-4"/> Save Settings
              </button>
            </section>

          </div>
        </div>

        <!-- Bottom Timelines: Account Activity & Recent Notifications -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          
          <!-- Recent Account Activity -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[400px]">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <Activity class="w-4 h-4 text-[#2563EB]" /> Recent Account Activity
            </h3>
            <div class="flex-1 overflow-y-auto custom-scrollbar">
              <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
                <div v-for="act in accountActivities" :key="act.id" class="relative pl-5">
                  <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-[#2563EB]"></span>
                  <div class="flex justify-between items-baseline mb-0.5">
                    <h4 class="text-sm font-bold text-gray-900">{{ act.action }}</h4>
                    <span class="text-[10px] text-gray-400 font-medium shrink-0 ml-2">{{ act.date }} • {{ act.time }}</span>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">{{ act.desc }}</p>
                </div>
              </div>
            </div>
          </section>

          <!-- Recent Notifications -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[400px]">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <Bell class="w-4 h-4 text-[#2563EB]" /> Recent Notifications
            </h3>
            <div class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
              <div v-for="noti in notifications" :key="noti.id" class="flex items-start gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                <div :class="`mt-0.5 p-1.5 rounded-lg text-white shrink-0 ${noti.color}`">
                  <component :is="noti.icon" class="w-3.5 h-3.5" />
                </div>
                <div>
                  <p class="text-sm font-bold text-gray-900 leading-tight">{{ noti.title }}</p>
                  <p class="text-[10px] text-gray-500 mt-1">{{ noti.time }}</p>
                </div>
              </div>
            </div>
            <button class="w-full mt-4 py-2 text-[#2563EB] text-sm font-semibold hover:bg-blue-50 rounded-lg transition-colors border border-transparent">
              View All Notifications
            </button>
          </section>

        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';


// Icons
import { 
  User, UserCog, ShieldCheck, BadgeCheck, Mail, Phone, MapPin, 
  Calendar, Clock, Camera, Lock, KeyRound, Bell, Settings, 
  Palette, Globe, Monitor, Laptop, Smartphone, History, Activity, 
  CheckCircle, AlertTriangle, Users, Building2, FileText, Eye, 
  Pencil, Save, Upload, Megaphone, Check
} from 'lucide-vue-next';

// View State
const sidebarOpen = ref(false);
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

// --- Dummy Data ---
const profile = ref({
  name: 'Jane Doe',
  id: 'ADM-001',
  designation: 'Lead Administrator',
  department: 'CivicDesk HQ',
  email: 'jane.doe@civicdesk.gov',
  phone: '+91 98765 00000',
  joinDate: 'Jan 01, 2020',
  avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
  cover: 'https://images.unsplash.com/photo-1557683316-973673baf926?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'
});

const stats = ref([
  { label: 'Years of Service', value: '6', icon: Award, colorClass: 'text-blue-600 bg-blue-100', textClass: 'text-blue-600' },
  { label: 'Announcements', value: '142', icon: Megaphone, colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  { label: 'Depts Managed', value: '12', icon: Building2, colorClass: 'text-green-600 bg-green-100', textClass: 'text-green-600' },
  { label: 'Officers Managed', value: '128', icon: Users, colorClass: 'text-orange-600 bg-orange-100', textClass: 'text-orange-600' },
  { label: 'System Actions', value: '8.4k', icon: Activity, colorClass: 'text-teal-600 bg-teal-100', textClass: 'text-teal-600' },
  { label: 'Last Login', value: 'Today', icon: Clock, colorClass: 'text-gray-600 bg-gray-100', textClass: 'text-gray-600' }
]);

const personal = ref({
  name: 'Jane Elizabeth Doe',
  dob: '24 Aug 1985',
  gender: 'Female',
  nationality: 'Indian',
  address: '101, Executive Enclave',
  city: 'Pune',
  state: 'Maharashtra',
  country: 'India',
  zip: '411001',
  emergency: '+91 99887 77665 (Spouse)'
});

const permissions = ref([
  { name: 'Manage Departments', desc: 'Create, edit, and delete civic departments.', level: 'Full Access' },
  { name: 'Manage Officers', desc: 'Approve, suspend, and transfer civic officers.', level: 'Full Access' },
  { name: 'Manage Announcements', desc: 'Publish global and targeted notices.', level: 'Full Access' },
  { name: 'System Settings', desc: 'Configure platform-wide variables.', level: 'Full Access' },
  { name: 'View Analytics', desc: 'Access platform business intelligence.', level: 'Read Only' },
  { name: 'Audit Logs', desc: 'Monitor security and activity trails.', level: 'Read Only' }
]);

const security = ref({
  lastPasswordChange: '45 days ago',
  recoveryEmail: 'jane.alt@personal.com',
  activeSessions: 2,
  trustedDevices: 3
});

const notificationPrefs = reactive({
  email: { label: 'Email Notifications', value: true },
  push: { label: 'Push Notifications', value: true },
  alerts: { label: 'System Alerts', value: true },
  security: { label: 'Security Alerts', value: true },
  dept: { label: 'Department Updates', value: false },
  weekly: { label: 'Weekly Reports', value: true }
});

const quickActions = ref([
  { name: 'Edit Profile', icon: Pencil },
  { name: 'Security Settings', icon: ShieldCheck },
  { name: 'Activity Logs', icon: History },
  { name: 'System Settings', icon: Settings }
]);

const loginHistory = ref([
  { id: 1, date: 'Jul 12, 2026', time: '09:00 AM', device: 'Desktop', os: 'Windows 11', browser: 'Chrome', ip: '192.168.1.10', status: 'Success' },
  { id: 2, date: 'Jul 11, 2026', time: '14:30 PM', device: 'Mobile', os: 'iOS 16', browser: 'Safari', ip: '45.22.11.9', status: 'Success' },
  { id: 3, date: 'Jul 10, 2026', time: '08:45 AM', device: 'Desktop', os: 'Windows 11', browser: 'Chrome', ip: '192.168.1.10', status: 'Success' },
  { id: 4, date: 'Jul 09, 2026', time: '23:15 PM', device: 'Unknown', os: 'Linux', browser: 'Firefox', ip: '112.19.44.2', status: 'Failed' }
]);

const accountActivities = ref([
  { id: 1, action: 'Announcement Published', desc: 'Published "System Maintenance Notice".', date: 'Jul 12, 2026', time: '10:30 AM' },
  { id: 2, action: 'Officer Approved', desc: 'Approved registration for Amit Desai.', date: 'Jul 11, 2026', time: '16:45 PM' },
  { id: 3, action: 'Settings Updated', desc: 'Changed global timeout to 30 mins.', date: 'Jul 10, 2026', time: '09:15 AM' },
  { id: 4, action: 'Password Changed', desc: 'Routine 90-day password cycle completed.', date: 'May 28, 2026', time: '11:00 AM' }
]);

const notifications = ref([
  { id: 1, title: 'Security Alert: Failed login attempt detected.', time: '2 hours ago', icon: AlertTriangle, color: 'bg-red-500' },
  { id: 2, title: 'New Officer Registration: Rahul Sharma.', time: '5 hours ago', icon: UserPlus, color: 'bg-blue-500' },
  { id: 3, title: 'System Maintenance scheduled for Sunday.', time: 'Yesterday', icon: Settings, color: 'bg-gray-500' },
  { id: 4, title: 'Department "Building Maintenance" created.', time: 'Jul 10, 2026', icon: Building2, color: 'bg-green-500' }
]);

// Note: Reusing the existing Award icon for fallback in stats array
import { Award, UserPlus } from 'lucide-vue-next';
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

/* Custom Scrollbars */
.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* Entry Animation */
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
</style>