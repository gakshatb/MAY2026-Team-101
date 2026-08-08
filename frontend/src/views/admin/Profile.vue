<template>
  <div class="flex h-screen overflow-hidden bg-[#F8FAFC] font-sans">

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">

      <div v-if="isLoading" class="flex-1 flex items-center justify-center text-gray-400">
        Loading profile...
      </div>

      <!-- Scrollable Dashboard Content -->
      <main v-else class="flex-1 overflow-x-hidden overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">

        <!-- Toast -->
        <div v-if="toast" :class="['fixed top-6 right-6 z-50 px-4 py-3 rounded-xl shadow-lg text-sm font-semibold text-white', toast.type === 'error' ? 'bg-red-500' : 'bg-green-500']">
          {{ toast.message }}
        </div>

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
            <!-- Cover Banner (gradient — no stock image dependency) -->
            <div class="h-28 md:h-40 w-full bg-gradient-to-r from-[#1E40AF] via-[#2563EB] to-[#3B82F6]"></div>
            <!-- Profile Info -->
            <div class="px-6 pb-6 relative flex-1 flex flex-col">
              <div class="flex flex-col md:flex-row gap-6 items-start md:items-center -mt-12 md:-mt-16 mb-4">
                <div class="relative group">
                  <img :src="avatarSrc" alt="Avatar" class="w-24 h-24 md:w-32 md:h-32 rounded-2xl border-4 border-white object-cover shadow-sm bg-white" />
                  <button @click="triggerAvatarPick" :disabled="isUploadingPhoto"
                    class="absolute bottom-2 right-2 p-2 bg-gray-900 text-white rounded-lg shadow-sm opacity-0 group-hover:opacity-100 transition-opacity hover:bg-[#2563EB] disabled:opacity-50">
                    <Upload class="w-4 h-4" />
                  </button>
                  <input ref="avatarInput" type="file" accept="image/png,image/jpeg" class="hidden" @change="onAvatarChosen" />
                </div>
                <div class="flex-1 pt-2 md:pt-16">
                  <div class="flex flex-col md:flex-row md:items-center gap-3 mb-1">
                    <h2 class="text-2xl font-bold text-gray-900">{{ profile.name }}</h2>
                    <div class="flex flex-wrap gap-2">
                      <span class="px-2.5 py-0.5 bg-blue-100 text-blue-700 text-[10px] font-bold uppercase rounded-md flex items-center gap-1"><ShieldCheck class="w-3 h-3"/> System Admin</span>
                      <span class="px-2.5 py-0.5 bg-green-100 text-green-700 text-[10px] font-bold uppercase rounded-md flex items-center gap-1"><CheckCircle class="w-3 h-3"/> Active</span>
                    </div>
                  </div>
                  <p class="text-[#2563EB] font-medium">{{ profile.designation }} • {{ profile.department }}</p>
                </div>
                <div class="flex gap-3 w-full md:w-auto md:pt-16">
                  <button @click="isEditing ? cancelEdit() : startEdit()"
                    class="flex-1 md:flex-none px-5 py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-bold rounded-xl hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
                    <component :is="isEditing ? X : Pencil" class="w-4 h-4"/> {{ isEditing ? 'Cancel' : 'Edit' }}
                  </button>
                  <button @click="showPasswordModal = true"
                    class="flex-1 md:flex-none px-5 py-2.5 bg-[#2563EB] text-white text-sm font-bold rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm flex items-center justify-center gap-2">
                    <KeyRound class="w-4 h-4"/> Password
                  </button>
                </div>
              </div>
              <!-- Contact Details Grid -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-auto pt-4 border-t border-gray-50">
                <div><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Admin ID</p><p class="text-sm font-semibold text-gray-900 flex items-center gap-1.5"><BadgeCheck class="w-4 h-4 text-[#2563EB]"/> {{ profile.id }}</p></div>
                <div><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Email</p><p class="text-sm font-semibold text-gray-900 flex items-center gap-1.5 truncate"><Mail class="w-4 h-4 text-gray-400"/> {{ profile.email }}</p></div>
                <div>
                  <p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Phone</p>
                  <p v-if="!isEditing" class="text-sm font-semibold text-gray-900 flex items-center gap-1.5"><Phone class="w-4 h-4 text-gray-400"/> {{ profile.phone }}</p>
                  <input v-else v-model="editForm.phone" placeholder="10-digit phone" class="w-full text-sm px-2 py-1 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                </div>
                <div><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Joining Date</p><p class="text-sm font-semibold text-gray-900 flex items-center gap-1.5"><Calendar class="w-4 h-4 text-gray-400"/> {{ profile.joinDate }}</p></div>
              </div>
              <div v-if="isEditing" class="pt-4 mt-4 border-t border-gray-50 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-[10px] text-gray-500 font-bold uppercase mb-1">Full Name</label>
                  <input v-model="editForm.name" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                </div>
                <div>
                  <label class="block text-[10px] text-gray-500 font-bold uppercase mb-1">Designation</label>
                  <input v-model="editForm.designation" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                </div>
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
                  <path class="text-[#22C55E] transition-all duration-1000 ease-out" stroke-width="3" :stroke-dasharray="`${completionPct}, 100`" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                </svg>
                <div class="absolute flex flex-col items-center justify-center">
                  <span class="text-xl font-bold text-gray-900">{{ completionPct }}%</span>
                </div>
              </div>
              <div class="flex-1">
                <h3 class="text-sm font-bold text-gray-900 mb-2">Profile Completion</h3>
                <ul class="space-y-1.5 text-xs text-gray-600">
                  <li class="flex items-center gap-2" :class="!profile.avatar && 'text-gray-400'">
                    <component :is="profile.avatar ? CheckCircle : EmptyDot" class="w-3.5 h-3.5" :class="profile.avatar ? 'text-green-500' : ''" /> Avatar uploaded
                  </li>
                  <li class="flex items-center gap-2" :class="!personal.emergency && 'text-gray-400'">
                    <component :is="personal.emergency ? CheckCircle : EmptyDot" class="w-3.5 h-3.5" :class="personal.emergency ? 'text-green-500' : ''" /> Emergency contact added
                  </li>
                  <li class="flex items-center gap-2" :class="!personal.address && 'text-gray-400'">
                    <component :is="personal.address ? CheckCircle : EmptyDot" class="w-3.5 h-3.5" :class="personal.address ? 'text-green-500' : ''" /> Address complete
                  </li>
                  <li class="flex items-center gap-2" :class="!personal.dob && 'text-gray-400'">
                    <component :is="personal.dob ? CheckCircle : EmptyDot" class="w-3.5 h-3.5" :class="personal.dob ? 'text-green-500' : ''" /> Date of birth added
                  </li>
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
                  <span class="text-xs font-bold text-purple-700 bg-purple-100 px-2 py-0.5 rounded">Full Access (Admin)</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-gray-50 rounded-xl border border-gray-100">
                  <span class="text-xs font-semibold text-gray-600">Managed Departments</span>
                  <span class="text-xs font-bold text-gray-900">{{ statValue('Depts Managed') }}</span>
                </div>
                <div class="flex justify-between items-center p-3 bg-gray-50 rounded-xl border border-gray-100">
                  <span class="text-xs font-semibold text-gray-600">Managed Officers</span>
                  <span class="text-xs font-bold text-gray-900">{{ statValue('Officers Managed') }}</span>
                </div>
              </div>
            </div>
          </section>

        </div>

        <!-- Profile Statistics Cards -->
        <section class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
          <div v-for="(stat, index) in decoratedStats" :key="index" class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 flex flex-col group hover:border-[#2563EB] transition-colors">
            <div class="flex items-center justify-between mb-3">
              <div :class="`p-2.5 rounded-xl ${stat.colorClass} group-hover:scale-110 transition-transform duration-300`">
                <component :is="stat.icon" class="w-5 h-5" :class="stat.textClass" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-0.5">{{ stat.value }}</h3>
            <span class="text-xs text-gray-500 font-semibold uppercase tracking-wide truncate">{{ stat.label }}</span>
          </div>
        </section>

        <!-- Main Content Layout (Two Columns) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">

          <!-- Left Column (Personal Info, Permissions, Login History) -->
          <div class="lg:col-span-2 space-y-6">

            <!-- Personal Information -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <div class="flex justify-between items-center mb-5">
                <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
                  <User class="w-4 h-4 text-[#2563EB]" /> Personal Information
                </h3>
                <button @click="isEditing ? cancelEdit() : startEdit()" class="text-xs font-bold text-[#2563EB] hover:underline">{{ isEditing ? 'Cancel' : 'Edit Info' }}</button>
              </div>

              <div v-if="!isEditing" class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Full Name</span><span class="text-sm font-semibold text-gray-900">{{ personal.name || '—' }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Date of Birth</span><span class="text-sm font-semibold text-gray-900">{{ personal.dob || 'Not set' }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Gender</span><span class="text-sm font-semibold text-gray-900">{{ personal.gender || 'Not set' }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Nationality</span><span class="text-sm font-semibold text-gray-900">{{ personal.nationality || 'Not set' }}</span></div>
                <div class="flex flex-col border-b border-gray-50 pb-2 md:col-span-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Residential Address</span><span class="text-sm font-semibold text-gray-900">{{ formattedAddress }}</span></div>
                <div class="flex flex-col pt-1 md:col-span-2"><span class="text-[10px] text-gray-400 font-bold uppercase mb-1">Emergency Contact</span><span class="text-sm font-semibold text-red-600">{{ personal.emergency || 'Not set' }}</span></div>
              </div>

              <!-- Edit mode -->
              <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-[10px] text-gray-400 font-bold uppercase mb-1">Date of Birth</label>
                  <input type="date" v-model="editForm.dob" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                </div>
                <div>
                  <label class="block text-[10px] text-gray-400 font-bold uppercase mb-1">Gender</label>
                  <select v-model="editForm.gender" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
                    <option value="">Select</option>
                    <option>Male</option><option>Female</option><option>Other</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[10px] text-gray-400 font-bold uppercase mb-1">Nationality</label>
                  <input v-model="editForm.nationality" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                </div>
                <div>
                  <label class="block text-[10px] text-gray-400 font-bold uppercase mb-1">Recovery Email</label>
                  <input v-model="editForm.recoveryEmail" type="email" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                </div>
                <div class="md:col-span-2">
                  <label class="block text-[10px] text-gray-400 font-bold uppercase mb-1">Address</label>
                  <input v-model="editForm.address" placeholder="Street address" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg mb-2 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                  <div class="grid grid-cols-3 gap-2">
                    <input v-model="editForm.city" placeholder="City" class="text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                    <input v-model="editForm.state" placeholder="State" class="text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                    <input v-model="editForm.zip" placeholder="Pincode" class="text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                  </div>
                </div>
                <div class="md:col-span-2">
                  <label class="block text-[10px] text-gray-400 font-bold uppercase mb-1">Emergency Contact</label>
                  <input v-model="editForm.emergency" placeholder="Name and phone" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
                </div>
                <div class="md:col-span-2 flex gap-3 pt-2">
                  <button @click="saveEdit" :disabled="isSaving" class="px-5 py-2 bg-[#2563EB] text-white text-sm font-bold rounded-xl hover:bg-[#1E40AF] disabled:opacity-50 flex items-center gap-2">
                    <Save class="w-4 h-4" /> {{ isSaving ? 'Saving...' : 'Save Changes' }}
                  </button>
                  <button @click="cancelEdit" class="px-5 py-2 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-bold rounded-xl hover:bg-gray-100">Cancel</button>
                </div>
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
              <div v-if="!loginHistory.length" class="p-6 text-sm text-gray-400 text-center">No login activity recorded yet.</div>
              <div v-else class="overflow-x-auto">
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
                 <button v-for="action in quickActions" :key="action.name" @click="action.handler"
                   class="flex flex-col items-center justify-center p-3 bg-gray-50 border border-gray-100 rounded-xl hover:bg-blue-50 hover:border-[#2563EB] hover:text-[#2563EB] transition-colors text-gray-700 group">
                   <component :is="action.icon" class="w-5 h-5 mb-1.5 text-gray-400 group-hover:text-[#2563EB]"/>
                   <span class="text-[11px] font-bold text-center leading-tight">{{ action.name }}</span>
                 </button>
               </div>
            </section>

            <!-- Account Security Section -->
            <section id="security-section" class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <Lock class="w-4 h-4 text-[#2563EB]" /> Account Security
              </h3>
              <ul class="space-y-4 text-sm mb-5">
                <li class="flex flex-col gap-1 border-b border-gray-50 pb-3">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Password</span></div>
                  <span class="text-xs text-gray-500">Last changed: {{ security.lastPasswordChange }}</span>
                </li>
                <li class="flex flex-col gap-1 border-b border-gray-50 pb-3">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Recovery Email</span></div>
                  <span class="text-xs text-gray-500 truncate">{{ security.recoveryEmail || 'Not set' }}</span>
                </li>
                <li class="flex flex-col gap-1 border-b border-gray-50 pb-3">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Active Sessions</span><span class="text-xs text-gray-700 font-bold bg-gray-100 px-2 py-0.5 rounded">{{ security.activeSessions }}</span></div>
                </li>
                <li class="flex flex-col gap-1 pt-1">
                  <div class="flex justify-between items-center"><span class="font-bold text-gray-900">Trusted Devices</span><span class="text-xs text-gray-700 font-bold bg-gray-100 px-2 py-0.5 rounded">{{ security.trustedDevices }}</span></div>
                </li>
              </ul>

              <!-- Active sessions list, shown when "Manage Devices" is toggled -->
              <div v-if="showSessions" class="space-y-2 mb-4">
                <div v-if="isLoadingSessions" class="text-xs text-gray-400 text-center py-2">Loading sessions...</div>
                <div v-for="s in sessions" :key="s.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-100">
                  <div class="flex items-center gap-2 min-w-0">
                    <component :is="s.device === 'Desktop' ? Laptop : Smartphone" class="w-4 h-4 text-gray-400 shrink-0" />
                    <div class="min-w-0">
                      <p class="text-xs font-bold text-gray-900 truncate">{{ s.device }} • {{ s.os }} • {{ s.browser }}</p>
                      <p class="text-[10px] text-gray-500">{{ s.ip }} · active {{ s.last_active }}</p>
                    </div>
                  </div>
                  <button @click="endSession(s.id)" class="text-[10px] font-bold text-red-600 hover:underline shrink-0 ml-2">End</button>
                </div>
                <div v-if="!isLoadingSessions && !sessions.length" class="text-xs text-gray-400 text-center py-2">No active sessions.</div>
              </div>

              <div class="flex flex-col gap-2">
                <button @click="toggleSessions" class="w-full py-2 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 transition-colors">
                  {{ showSessions ? 'Hide Devices' : 'Manage Devices' }}
                </button>
              </div>
            </section>

            <!-- Notification Preferences -->
            <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
                <Bell class="w-4 h-4 text-[#2563EB]" /> Notification Preferences
              </h3>
              <div class="space-y-4 mb-6">
                <div v-for="pref in notificationPrefList" :key="pref.key" class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-700">{{ pref.label }}</span>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="notificationPrefs[pref.key]" class="sr-only peer">
                    <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#2563EB]"></div>
                  </label>
                </div>
              </div>
              <button @click="savePrefs" :disabled="isSavingPrefs" class="w-full py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 transition-colors flex items-center justify-center gap-2 disabled:opacity-50">
                <Save class="w-4 h-4"/> {{ isSavingPrefs ? 'Saving...' : 'Save Preferences' }}
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
            <div v-if="!accountActivities.length" class="flex-1 flex items-center justify-center text-sm text-gray-400">No activity yet.</div>
            <div v-else class="flex-1 overflow-y-auto custom-scrollbar">
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
            <div v-if="!notifications.length" class="flex-1 flex items-center justify-center text-sm text-gray-400">Nothing new.</div>
            <div v-else class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
              <div v-for="noti in notifications" :key="noti.id" class="flex items-start gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                <div class="mt-0.5 p-1.5 rounded-lg text-white shrink-0 bg-[#2563EB]">
                  <Bell class="w-3.5 h-3.5" />
                </div>
                <div>
                  <p class="text-sm font-bold text-gray-900 leading-tight">{{ noti.title }}</p>
                  <p class="text-[10px] text-gray-500 mt-1">{{ noti.time }}</p>
                </div>
              </div>
            </div>
            <router-link to="/admin/notifications" class="w-full mt-4 py-2 text-[#2563EB] text-sm font-semibold hover:bg-blue-50 rounded-lg transition-colors border border-transparent text-center block">
              View All Notifications
            </router-link>
          </section>

        </div>

      </main>
    </div>

    <!-- Change Password Modal -->
    <div v-if="showPasswordModal" class="fixed inset-0 bg-black/40 z-40 flex items-center justify-center p-4" @click.self="closePasswordModal">
      <div class="bg-white rounded-[14px] shadow-xl w-full max-w-md p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2"><KeyRound class="w-5 h-5 text-[#2563EB]"/> Change Password</h3>
        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Current Password</label>
            <input v-model="pwForm.current" type="password" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">New Password</label>
            <input v-model="pwForm.next" type="password" class="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20" />
          </div>
          <p v-if="pwError" class="text-xs text-red-600">{{ pwError }}</p>
        </div>
        <div class="flex gap-3 mt-5">
          <button @click="submitPasswordChange" :disabled="isChangingPassword" class="flex-1 py-2.5 bg-[#2563EB] text-white text-sm font-bold rounded-xl hover:bg-[#1E40AF] disabled:opacity-50">
            {{ isChangingPassword ? 'Updating...' : 'Update Password' }}
          </button>
          <button @click="closePasswordModal" class="flex-1 py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-bold rounded-xl hover:bg-gray-100">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';

// Icons
import {
  User, ShieldCheck, BadgeCheck, Mail, Phone, MapPin,
  Calendar, Clock, Camera, Lock, KeyRound, Bell, Settings,
  History, Activity,
  CheckCircle, AlertTriangle, Users, Building2, FileText,
  Pencil, Save, Upload, Megaphone, Check, Award, X,
  Laptop, Smartphone, Circle as EmptyDot
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

const isLoading = ref(true);
const toast = ref(null);
const showToast = (message, type = 'success') => {
  toast.value = { message, type };
  setTimeout(() => { toast.value = null; }, 3000);
};

// --- Core state, populated from GET /admin/profile ---
const profile = ref({ name: '', id: '', designation: '', department: '', email: '', phone: '', joinDate: '', avatar: null });
const statsRaw = ref([]);
const personal = ref({});
const permissions = ref([]);
const security = ref({ lastPasswordChange: '—', recoveryEmail: '', activeSessions: 0, trustedDevices: 0 });
const loginHistory = ref([]);
const accountActivities = ref([]);
const notifications = ref([]);
const notificationPrefs = reactive({ email: true, push: true, alerts: true, security: true, dept: false, weekly: true });

const notificationPrefList = [
  { key: 'email',    label: 'Email Notifications' },
  { key: 'push',     label: 'Push Notifications' },
  { key: 'alerts',   label: 'System Alerts' },
  { key: 'security', label: 'Security Alerts' },
  { key: 'dept',     label: 'Department Updates' },
  { key: 'weekly',   label: 'Weekly Reports' },
];

const statIcons = {
  'Years of Service': { icon: Award, colorClass: 'text-blue-600 bg-blue-100', textClass: 'text-blue-600' },
  'Announcements':    { icon: Megaphone, colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  'Depts Managed':    { icon: Building2, colorClass: 'text-green-600 bg-green-100', textClass: 'text-green-600' },
  'Officers Managed': { icon: Users, colorClass: 'text-orange-600 bg-orange-100', textClass: 'text-orange-600' },
  'System Actions':   { icon: Activity, colorClass: 'text-teal-600 bg-teal-100', textClass: 'text-teal-600' },
  'Last Login':       { icon: Clock, colorClass: 'text-gray-600 bg-gray-100', textClass: 'text-gray-600' },
};
const decoratedStats = computed(() => statsRaw.value.map(s => ({ ...s, ...(statIcons[s.label] || {}) })));
const statValue = (label) => statsRaw.value.find(s => s.label === label)?.value ?? '—';

const avatarSrc = computed(() =>
  profile.value.avatar
    ? (profile.value.avatar.startsWith('http') ? profile.value.avatar : `http://127.0.0.1:5000${profile.value.avatar}`)
    : `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.value.name || 'Admin')}&background=2563EB&color=fff`
);

const formattedAddress = computed(() => {
  const p = personal.value;
  const parts = [p.address, p.city, p.state, p.country].filter(Boolean);
  if (!parts.length) return 'Not set';
  return parts.join(', ') + (p.zip ? ` - ${p.zip}` : '');
});

const completionPct = computed(() => {
  const checks = [profile.value.avatar, personal.value.emergency, personal.value.address, personal.value.dob];
  const filled = checks.filter(Boolean).length;
  return Math.round((filled / checks.length) * 100);
});

const quickActions = [
  { name: 'Edit Profile',      icon: Pencil,      handler: () => startEdit() },
  { name: 'Security Settings', icon: ShieldCheck, handler: () => document.getElementById('security-section')?.scrollIntoView({ behavior: 'smooth' }) },
  { name: 'Activity Logs',     icon: History,     handler: () => router.push('/admin/activitylogs') },
  { name: 'Change Password',   icon: KeyRound,    handler: () => { showPasswordModal.value = true; } },
];

import { useRouter } from 'vue-router';
const router = useRouter();

// --- Fetch everything ---
const fetchProfile = async () => {
  isLoading.value = true;
  try {
    const { data } = await axios.get(`${API_BASE}/profile`, authHeaders());
    profile.value = data.profile;
    statsRaw.value = data.stats;
    personal.value = data.personal;
    permissions.value = data.permissions;
    security.value = data.security;
    loginHistory.value = data.loginHistory;
    accountActivities.value = data.accountActivities;
    Object.assign(notificationPrefs, data.notificationPrefs);
  } catch (err) {
    showToast('Failed to load profile.', 'error');
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};

const fetchNotifications = async () => {
  try {
    const { data } = await axios.get(`${API_BASE}/notifications`, authHeaders());
    notifications.value = (data.notifications || []).slice(0, 6).map(n => ({
      id: n.id, title: n.title || n.message, time: new Date(n.created_at).toLocaleString(),
    }));
  } catch (err) {
    console.error('Notifications fetch error:', err);
  }
};

onMounted(() => { fetchProfile(); fetchNotifications(); });

// --- Edit personal/profile info ---
const isEditing = ref(false);
const isSaving = ref(false);
const editForm = reactive({});

const startEdit = () => {
  Object.assign(editForm, {
    name: profile.value.name, phone: profile.value.phone, designation: profile.value.designation,
    dob: personal.value.dob ? new Date(personal.value.dob).toISOString().slice(0, 10) : '',
    gender: personal.value.gender || '', nationality: personal.value.nationality || '',
    address: personal.value.address || '', city: personal.value.city || '',
    state: personal.value.state || '', zip: personal.value.zip || '',
    emergency: personal.value.emergency || '', recoveryEmail: security.value.recoveryEmail || '',
  });
  isEditing.value = true;
};
const cancelEdit = () => { isEditing.value = false; };

const saveEdit = async () => {
  isSaving.value = true;
  try {
    await axios.put(`${API_BASE}/profile`, { ...editForm }, authHeaders());
    await fetchProfile();
    isEditing.value = false;
    showToast('Profile updated successfully.');
  } catch (err) {
    showToast(err.response?.data?.message || 'Failed to update profile.', 'error');
  } finally {
    isSaving.value = false;
  }
};

// --- Avatar upload ---
const avatarInput = ref(null);
const isUploadingPhoto = ref(false);
const triggerAvatarPick = () => avatarInput.value?.click();
const onAvatarChosen = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  isUploadingPhoto.value = true;
  try {
    const formData = new FormData();
    formData.append('photo', file);
    const { data } = await axios.post(`${API_BASE}/profile/photo`, formData, {
      headers: { ...authHeaders().headers, 'Content-Type': 'multipart/form-data' }
    });
    profile.value.avatar = data.profilePhoto;

    const storedUser = JSON.parse(localStorage.getItem('user') || 'null');
    if (storedUser) {
      storedUser.profilePhoto = data.profilePhoto;
      localStorage.setItem('user', JSON.stringify(storedUser));
      window.dispatchEvent(new Event('user-updated'));
    }

    showToast('Photo updated.');
  } catch (err) {
    showToast(err.response?.data?.message || 'Failed to upload photo.', 'error');
  } finally {
    isUploadingPhoto.value = false;
    e.target.value = '';
  }
};

// --- Notification preferences ---
const isSavingPrefs = ref(false);
const savePrefs = async () => {
  isSavingPrefs.value = true;
  try {
    await axios.put(`${API_BASE}/profile/notification-preferences`, { ...notificationPrefs }, authHeaders());
    showToast('Preferences saved.');
  } catch (err) {
    showToast('Failed to save preferences.', 'error');
  } finally {
    isSavingPrefs.value = false;
  }
};

// --- Sessions ---
const showSessions = ref(false);
const isLoadingSessions = ref(false);
const sessions = ref([]);
const toggleSessions = async () => {
  showSessions.value = !showSessions.value;
  if (showSessions.value) {
    isLoadingSessions.value = true;
    try {
      const { data } = await axios.get(`${API_BASE}/profile/sessions`, authHeaders());
      sessions.value = data.sessions;
    } catch (err) {
      showToast('Failed to load sessions.', 'error');
    } finally {
      isLoadingSessions.value = false;
    }
  }
};
const endSession = async (id) => {
  try {
    await axios.delete(`${API_BASE}/profile/sessions/${id}`, authHeaders());
    sessions.value = sessions.value.filter(s => s.id !== id);
    security.value.activeSessions = Math.max(0, security.value.activeSessions - 1);
    showToast('Session ended.');
  } catch (err) {
    showToast(err.response?.data?.message || 'Failed to end session.', 'error');
  }
};

// --- Change password ---
const showPasswordModal = ref(false);
const isChangingPassword = ref(false);
const pwError = ref('');
const pwForm = reactive({ current: '', next: '' });
const closePasswordModal = () => { showPasswordModal.value = false; pwForm.current = ''; pwForm.next = ''; pwError.value = ''; };
const submitPasswordChange = async () => {
  pwError.value = '';
  if (!pwForm.current || !pwForm.next) { pwError.value = 'Both fields are required.'; return; }
  isChangingPassword.value = true;
  try {
    await axios.post('http://127.0.0.1:5000/api/change-password',
      { currentPassword: pwForm.current, newPassword: pwForm.next }, authHeaders());
    showToast('Password changed successfully.');
    closePasswordModal();
    await fetchProfile();
  } catch (err) {
    pwError.value = err.response?.data?.message || 'Failed to change password.';
  } finally {
    isChangingPassword.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

.custom-scrollbar::-webkit-scrollbar { display: none; }
.custom-scrollbar { scrollbar-width: none; -ms-overflow-style: none; }

/* Entry Animation */
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
</style>