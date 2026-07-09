<template>
  <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-800 overflow-hidden">
    
    <Sidebar userRole="Field Worker" :isOpen="isSidebarOpen" @close-sidebar="isSidebarOpen = false" />

    <div class="flex-1 flex flex-col h-screen overflow-hidden">
      
      <DashboardNavbar userRole="Field Worker" pageTitle="Worker Profile" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
        <div class="max-w-[1400px] mx-auto space-y-6 animate-fade-in">
          
          <!-- Breadcrumb & Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/worker/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Profile</span>
              </nav>
              <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">Worker Profile</h1>
              <p class="text-slate-500 mt-1">Manage your personal information, work history, and field performance.</p>
            </div>
          </div>

          <!-- Main Two-Column Layout -->
          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <!-- LEFT COLUMN: Profile & Details (4 cols) -->
            <div class="xl:col-span-4 space-y-6">
              
              <!-- Profile Overview Card -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6 flex flex-col items-center text-center relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-24 bg-gradient-to-r from-[#1E40AF] to-[#2563EB]"></div>
                <div class="relative mt-8 mb-4">
                  <img :src="profile.photo" class="w-28 h-28 rounded-full object-cover border-4 border-white shadow-md bg-white" />
                  <div class="absolute bottom-1 right-1 w-6 h-6 bg-green-500 border-2 border-white rounded-full flex items-center justify-center" title="Available for Work"></div>
                </div>
                <h2 class="text-xl font-bold text-slate-900 flex items-center justify-center gap-2">
                  {{ profile.name }} <BadgeCheck class="w-5 h-5 text-[#2563EB]" title="Verified Worker" />
                </h2>
                <p class="text-sm font-bold text-[#2563EB] mt-1">{{ profile.designation }} • {{ profile.department }}</p>
                <p class="text-xs text-slate-500 font-mono mt-1">ID: {{ profile.id }}</p>
                
                <div class="flex flex-wrap justify-center gap-3 mt-4 text-sm text-slate-600">
                  <span class="flex items-center gap-1.5"><MapPin class="w-4 h-4 text-slate-400"/> {{ profile.ward }}, {{ profile.area }}</span>
                  <span class="flex items-center gap-1.5"><Phone class="w-4 h-4 text-slate-400"/> {{ profile.phone }}</span>
                </div>

                <div class="flex w-full gap-3 mt-6">
                  <button @click="isEditModalOpen = true" class="flex-1 py-2.5 bg-[#2563EB] text-white text-sm font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm">Edit Profile</button>
                  <button @click="isPasswordModalOpen = true" class="flex-1 py-2.5 bg-white border border-slate-200 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-50 transition-colors shadow-sm">Password</button>
                </div>
              </div>

              <!-- Professional Information -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Briefcase class="w-5 h-5 text-slate-400" /> Professional Info</h3>
                <div class="space-y-4">
                  <div v-for="(val, label) in professionalInfo" :key="label" class="flex justify-between items-center border-b border-slate-50 pb-3 last:border-0 last:pb-0">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">{{ label }}</span>
                    <span class="text-sm font-semibold text-slate-900 text-right">{{ val }}</span>
                  </div>
                </div>
              </div>

              <!-- Personal Information -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><User class="w-5 h-5 text-slate-400" /> Personal Info</h3>
                <div class="space-y-4">
                  <div v-for="(val, label) in personalInfo" :key="label" class="flex justify-between items-center border-b border-slate-50 pb-3 last:border-0 last:pb-0">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">{{ label }}</span>
                    <span class="text-sm font-semibold text-slate-900 text-right">{{ val }}</span>
                  </div>
                </div>
              </div>

              <!-- Equipment Assigned -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Tool class="w-5 h-5 text-amber-500" /> Equipment Assigned</h3>
                <div class="space-y-3">
                  <div v-for="eq in equipment" :key="eq.name" class="p-3 bg-slate-50 border border-slate-100 rounded-xl flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center shrink-0">
                        <component :is="eq.icon" class="w-4 h-4" />
                      </div>
                      <div>
                        <p class="text-sm font-bold text-slate-900 leading-tight">{{ eq.name }}</p>
                        <p class="text-[10px] text-slate-500 font-medium mt-0.5">Issued: {{ eq.issued }}</p>
                      </div>
                    </div>
                    <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${eq.condition === 'Good' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'}`">{{ eq.condition }}</span>
                  </div>
                </div>
              </div>

              <!-- Attendance & Leave -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Calendar class="w-5 h-5 text-purple-500" /> Attendance Summary</h3>
                <div class="grid grid-cols-2 gap-3 mb-4">
                  <div class="p-3 bg-green-50 rounded-xl border border-green-100">
                    <p class="text-[10px] font-bold text-green-700 uppercase tracking-wide mb-1">Present Days</p>
                    <p class="text-xl font-extrabold text-green-700">22</p>
                  </div>
                  <div class="p-3 bg-red-50 rounded-xl border border-red-100">
                    <p class="text-[10px] font-bold text-red-700 uppercase tracking-wide mb-1">Leave Days</p>
                    <p class="text-xl font-extrabold text-red-700">2</p>
                  </div>
                </div>
                <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
                  <span class="text-sm font-bold text-slate-700">Current Shift</span>
                  <span class="text-sm font-bold text-[#2563EB]">09:00 AM - 05:00 PM</span>
                </div>
              </div>

              <!-- Documents -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-4"><FileText class="w-5 h-5 text-slate-400" /> Official Documents</h3>
                <div class="space-y-2">
                  <div v-for="doc in documents" :key="doc.name" class="flex justify-between items-center p-3 hover:bg-slate-50 rounded-lg transition-colors border border-transparent hover:border-slate-100 cursor-pointer group">
                    <span class="text-sm font-medium text-slate-700 flex items-center gap-2"><FileText class="w-4 h-4 text-slate-400"/> {{ doc.name }}</span>
                    <Download class="w-4 h-4 text-slate-300 group-hover:text-[#2563EB] transition-colors" />
                  </div>
                </div>
              </div>

            </div>

            <!-- RIGHT COLUMN: Analytics, Work & History (8 cols) -->
            <div class="xl:col-span-8 space-y-6">
              
              <!-- Quick Actions Top Bar -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <router-link to="/worker/tasks" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <ClipboardCheck class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Assigned Tasks</span>
                </router-link>
                <router-link to="/worker/completed" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <CheckCircle class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Completed</span>
                </router-link>
                <router-link to="/worker/notifications" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <Bell class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Notifications</span>
                </router-link>
                <router-link to="/worker/dashboard" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 hover:border-[#2563EB]/30 hover:shadow-md transition-all flex flex-col items-center justify-center text-center gap-2 group">
                  <Activity class="w-6 h-6 text-slate-400 group-hover:text-[#2563EB]" />
                  <span class="text-sm font-bold text-slate-700 group-hover:text-[#2563EB]">Dashboard</span>
                </router-link>
              </div>

              <!-- Performance Summary (KPIs) -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div v-for="stat in performanceStats" :key="stat.title" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-center">
                  <div class="flex items-center gap-2 mb-2">
                    <component :is="stat.icon" class="w-4 h-4" :class="stat.color" />
                    <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wide">{{ stat.title }}</span>
                  </div>
                  <p class="text-2xl font-extrabold text-slate-900">{{ stat.value }}</p>
                </div>
              </div>

              <!-- Charts -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100">
                  <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><TrendingUp class="w-4 h-4 text-[#2563EB]" /> Task Completion Trend</h3>
                  <div class="h-[220px] w-full relative">
                    <canvas ref="completionChartRef"></canvas>
                  </div>
                </div>
                <div class="bg-white p-5 rounded-[14px] shadow-sm border border-slate-100">
                  <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Star class="w-4 h-4 text-amber-500" /> Citizen Rating Trend</h3>
                  <div class="h-[220px] w-full relative">
                    <canvas ref="ratingChartRef"></canvas>
                  </div>
                </div>
              </div>

              <!-- Achievements & Certifications -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                  <div class="p-5 border-b border-slate-100 bg-slate-50/50">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><Award class="w-5 h-5 text-amber-500" /> My Achievements</h3>
                  </div>
                  <div class="p-5 space-y-4">
                    <div v-for="ach in achievements" :key="ach.title" class="flex items-center gap-4 p-3 border border-slate-100 rounded-xl bg-gradient-to-r from-slate-50 to-white">
                      <div class="w-10 h-10 rounded-full bg-amber-50 flex items-center justify-center text-xl shrink-0 border border-amber-100">
                        {{ ach.icon }}
                      </div>
                      <div>
                        <p class="font-bold text-slate-900 text-sm">{{ ach.title }}</p>
                        <p class="text-xs text-slate-500 mt-0.5">{{ ach.desc }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                  <div class="p-5 border-b border-slate-100 bg-slate-50/50">
                    <h3 class="font-bold text-slate-900 flex items-center gap-2"><ShieldCheck class="w-5 h-5 text-green-500" /> Training & Certifications</h3>
                  </div>
                  <div class="p-5 space-y-3">
                    <div v-for="cert in certifications" :key="cert.name" class="p-3 border border-slate-100 rounded-xl hover:bg-slate-50 transition-colors">
                      <p class="font-bold text-slate-900 text-sm">{{ cert.name }}</p>
                      <div class="flex justify-between items-center mt-2 text-xs font-medium text-slate-500">
                        <span class="flex items-center gap-1"><Calendar class="w-3 h-3"/> Completed: {{ cert.date }}</span>
                        <span :class="`px-2 py-0.5 rounded uppercase font-bold text-[9px] ${cert.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`">{{ cert.status }}</span>
                      </div>
                    </div>
                  </div>
                </div>

              </div>

              <!-- Work History / Assigned Areas (Tabs) -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="flex border-b border-slate-100 bg-slate-50/50 px-2">
                  <button @click="historyTab = 'history'" :class="`px-4 py-4 text-sm font-bold border-b-2 transition-colors ${historyTab === 'history' ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-slate-500 hover:text-slate-700'}`">Recent Work History</button>
                  <button @click="historyTab = 'areas'" :class="`px-4 py-4 text-sm font-bold border-b-2 transition-colors ${historyTab === 'areas' ? 'border-[#2563EB] text-[#2563EB]' : 'border-transparent text-slate-500 hover:text-slate-700'}`">Assigned Areas</button>
                </div>
                
                <div class="p-0">
                  <div v-if="historyTab === 'history'" class="overflow-x-auto">
                    <table class="w-full text-left text-sm whitespace-nowrap">
                      <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide border-b border-slate-100">
                        <tr>
                          <th class="px-5 py-4">Complaint ID</th>
                          <th class="px-5 py-4">Category</th>
                          <th class="px-5 py-4">Completed On</th>
                          <th class="px-5 py-4">Rating</th>
                          <th class="px-5 py-4 text-right">Action</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-slate-100">
                        <tr v-for="work in workHistory" :key="work.id" class="hover:bg-slate-50 transition-colors">
                          <td class="px-5 py-3 font-mono font-bold text-slate-900">{{ work.id }}</td>
                          <td class="px-5 py-3 text-slate-600 font-medium">{{ work.category }}</td>
                          <td class="px-5 py-3 text-slate-600">{{ work.date }}</td>
                          <td class="px-5 py-3">
                            <div class="flex items-center gap-0.5">
                              <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= work.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'" />
                            </div>
                          </td>
                          <td class="px-5 py-3 text-right">
                            <button class="px-3 py-1.5 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-100 transition-colors">Details</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                  <div v-if="historyTab === 'areas'" class="p-5 grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div v-for="area in assignedAreas" :key="area.name" class="p-4 bg-slate-50 rounded-xl border border-slate-100 flex flex-col justify-between">
                      <div class="mb-4">
                        <h4 class="font-bold text-slate-900 text-sm flex items-center gap-1.5"><MapPin class="w-4 h-4 text-[#2563EB]"/> {{ area.name }}</h4>
                        <p class="text-xs text-slate-500 mt-1">{{ area.ward }}</p>
                      </div>
                      <div class="grid grid-cols-2 gap-2 text-center">
                        <div class="bg-white p-2 rounded border border-slate-200">
                          <p class="text-[10px] font-bold text-slate-500 uppercase">Assigned</p>
                          <p class="font-bold text-slate-900">{{ area.assigned }}</p>
                        </div>
                        <div class="bg-white p-2 rounded border border-slate-200">
                          <p class="text-[10px] font-bold text-slate-500 uppercase">Completed</p>
                          <p class="font-bold text-[#22C55E]">{{ area.completed }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Settings & Preferences -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Notifications -->
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Bell class="w-5 h-5 text-slate-400" /> Notification Preferences</h3>
                  <div class="space-y-4">
                    <label v-for="(val, key) in notificationPrefs" :key="key" class="flex items-center justify-between cursor-pointer group">
                      <span class="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{{ key }}</span>
                      <div class="relative inline-flex items-center">
                        <input type="checkbox" v-model="notificationPrefs[key]" class="sr-only peer">
                        <div class="w-9 h-5 bg-slate-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#2563EB]"></div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Security -->
                <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-6">
                  <h3 class="font-bold text-slate-900 flex items-center gap-2 mb-5"><Lock class="w-5 h-5 text-slate-400" /> Security Settings</h3>
                  <div class="space-y-4">
                    <button @click="isPasswordModalOpen = true" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between hover:bg-slate-100 transition-colors group">
                      <span class="text-sm font-medium text-slate-700 flex items-center gap-2"><Key class="w-4 h-4 text-slate-400 group-hover:text-slate-600"/> Change Password</span>
                      <ChevronRight class="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
                    </button>
                    <label class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between cursor-pointer group">
                      <span class="text-sm font-medium text-slate-700 flex items-center gap-2"><ShieldCheck class="w-4 h-4 text-slate-400 group-hover:text-slate-600"/> Two-Factor Auth</span>
                      <div class="relative inline-flex items-center">
                        <input type="checkbox" checked class="sr-only peer">
                        <div class="w-9 h-5 bg-slate-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#22C55E]"></div>
                      </div>
                    </label>
                    <div class="p-3 border border-slate-100 rounded-xl">
                      <p class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Last Login</p>
                      <p class="text-sm text-slate-900 font-medium">Jul 09, 2026 - 08:30 AM (Pune)</p>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Edit Profile Modal -->
    <Teleport to="body">
      <div v-if="isEditModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <h3 class="font-bold text-lg text-slate-900">Edit Profile</h3>
            <button @click="isEditModalOpen = false" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4">
            <div class="flex items-center gap-4 mb-4">
              <img :src="profile.photo" class="w-16 h-16 rounded-full object-cover border border-slate-200" />
              <button class="px-3 py-1.5 bg-slate-100 border border-slate-200 text-slate-700 text-xs font-bold rounded hover:bg-slate-200 transition-colors flex items-center gap-2"><Upload class="w-3.5 h-3.5"/> Upload New Photo</button>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Phone Number</label>
                <input type="text" v-model="profile.phone" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Emergency Contact</label>
                <input type="text" value="+91 98765 00000" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
              </div>
              <div class="col-span-2">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Residential Address</label>
                <textarea rows="2" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none resize-none">Apt 4B, Shanti Niwas, Pune</textarea>
              </div>
            </div>
          </div>
          <div class="p-5 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
            <button @click="isEditModalOpen = false" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-100 transition-colors text-sm">Cancel</button>
            <button @click="isEditModalOpen = false" class="px-4 py-2 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm text-sm">Save Changes</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Change Password Modal -->
    <Teleport to="body">
      <div v-if="isPasswordModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-2xl w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
            <h3 class="font-bold text-lg text-slate-900">Change Password</h3>
            <button @click="isPasswordModalOpen = false" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Current Password</label>
              <input type="password" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">New Password</label>
              <input type="password" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Confirm New Password</label>
              <input type="password" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] outline-none" />
            </div>
          </div>
          <div class="p-5 border-t border-slate-100 bg-slate-50 flex flex-col gap-2">
            <button @click="isPasswordModalOpen = false" class="w-full py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm text-sm">Update Password</button>
            <button @click="isPasswordModalOpen = false" class="w-full py-2.5 bg-white border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-100 transition-colors text-sm">Cancel</button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import Chart from 'chart.js/auto'
import { 
  BadgeCheck, MapPin, Phone, Briefcase, User, Wrench, Calendar, FileText, Download,
  ClipboardCheck, CheckCircle, Clock, Bell, Activity, TrendingUp, Star, Award, ShieldCheck,
  Lock, Key, ChevronRight, X, Upload, Hammer, Truck, Construction
} from 'lucide-vue-next'


// --- State ---
const isSidebarOpen = ref(false)
const isEditModalOpen = ref(false)
const isPasswordModalOpen = ref(false)
const historyTab = ref('history')

const completionChartRef = ref(null)
const ratingChartRef = ref(null)
let completionChart, ratingChart

// --- Dummy Data ---
const profile = reactive({
  name: 'Amit Singh',
  photo: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=200&h=200&fit=crop',
  id: 'FW-2026-084',
  designation: 'Senior Field Technician',
  department: 'Road Maintenance',
  ward: 'Ward 12',
  area: 'North Zone',
  phone: '+91 98765 43210',
})

const professionalInfo = {
  'Employee ID': 'FW-2026-084',
  'Department': 'Road Maintenance',
  'Designation': 'Senior Field Technician',
  'Reporting Officer': 'Rajesh Kumar',
  'Experience': '6 Years',
  'Employment Type': 'Full-Time (Permanent)',
  'Skills': 'Asphalt Repair, Heavy Machinery'
}

const personalInfo = {
  'Full Name': 'Amit Singh',
  'Date of Birth': '14 Aug 1992',
  'Gender': 'Male',
  'Email Address': 'amit.singh@civicdesk.in',
  'Blood Group': 'O+',
  'Languages': 'English, Hindi, Marathi'
}

const performanceStats = [
  { title: 'Completed Tasks', value: '342', icon: CheckCircle, color: 'text-green-500' },
  { title: 'Avg Completion', value: '4.5h', icon: Clock, color: 'text-blue-500' },
  { title: 'Citizen Rating', value: '4.8', icon: Star, color: 'text-amber-500' },
  { title: 'Perf. Score', value: '96', icon: Activity, color: 'text-purple-500' }
]

const equipment = [
  { name: 'Safety Helmet Class A', issued: 'Jan 2026', condition: 'Good', icon: ShieldCheck },
  { name: 'Road Repair Tool Kit', issued: 'Mar 2026', condition: 'Good', icon: Wrench },
  { name: 'Reflective Safety Jacket', issued: 'Jan 2026', condition: 'Good', icon: User },
  { name: 'Heavy Compactor (Shared)', issued: 'N/A', condition: 'Maintenance Due', icon: Truck }
]

const achievements = [
  { title: '100 Tasks Completed', desc: 'Milestone achieved in record time.', icon: '🏆' },
  { title: 'Fast Responder', desc: 'Consistently resolves high-priority tasks under 2 hours.', icon: '⚡' },
  { title: 'Top Rated Worker', desc: 'Maintained 4.8+ rating for 6 months.', icon: '⭐' }
]

const certifications = [
  { name: 'Advanced Road Safety Protocol', date: 'Feb 15, 2026', status: 'Active' },
  { name: 'Heavy Machinery Operation Level 2', date: 'Nov 10, 2025', status: 'Active' },
  { name: 'First Aid Emergency Response', date: 'Jan 05, 2024', status: 'Expired' }
]

const workHistory = [
  { id: 'CMP-8875', category: 'Pothole Repair', date: 'Jul 08, 2026', rating: 5 },
  { id: 'CMP-8842', category: 'Road Damage', date: 'Jul 05, 2026', rating: 4 },
  { id: 'CMP-8810', category: 'Pothole Repair', date: 'Jul 02, 2026', rating: 5 },
  { id: 'CMP-8790', category: 'Illegal Dumping', date: 'Jun 28, 2026', rating: 5 }
]

const assignedAreas = [
  { name: 'MG Road Segment 1', ward: 'Ward 12', assigned: 12, completed: 10 },
  { name: 'Downtown North', ward: 'Ward 14', assigned: 8, completed: 8 }
]

const documents = [
  { name: 'Employee ID Card (PDF)' },
  { name: 'Appointment Letter (PDF)' },
  { name: 'Latest Performance Review' }
]

const notificationPrefs = reactive({
  'Task Assignment Alerts': true,
  'Emergency Alerts': true,
  'Deadline Reminders': true,
  'Officer Messages': true,
  'Verification Updates': false,
  'Push Notifications': true
})

// --- Charts Setup ---
onMounted(() => {
  if (completionChartRef.value) {
    completionChart = new Chart(completionChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Completed',
          data: [25, 32, 28, 35, 40, 22],
          backgroundColor: '#2563EB',
          borderRadius: 4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }
    })
  }

  if (ratingChartRef.value) {
    ratingChart = new Chart(ratingChartRef.value, {
      type: 'line',
      data: {
        labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Rating',
          data: [4.5, 4.6, 4.8, 4.7, 4.9, 4.8],
          borderColor: '#F59E0B',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          fill: true,
          tension: 0.4
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { min: 4, max: 5, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }
    })
  }
})

onUnmounted(() => {
  if (completionChart) completionChart.destroy()
  if (ratingChart) ratingChart.destroy()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>