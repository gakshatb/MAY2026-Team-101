<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1400px] mx-auto space-y-6">
          
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <router-link to="/officer/complaints" class="hover:text-[#2563EB] transition-colors">Complaint Management</router-link>
                <span class="mx-2">›</span>
                <router-link to="/officer/details/CMP-2026-0892" class="hover:text-[#2563EB] transition-colors">CMP-2026-0892</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Assign Worker</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Assign Worker</h1>
              <p class="text-slate-500 mt-1">Assign the complaint to the most suitable field worker.</p>
            </div>
            
            <div class="flex gap-2">
              <button class="p-2.5 bg-white border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50 transition-colors tooltip-trigger">
                <Printer class="w-4 h-4" />
              </button>
              <button class="p-2.5 bg-white border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50 transition-colors tooltip-trigger">
                <Download class="w-4 h-4" />
              </button>
              <button class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-2">
                <Eye class="w-4 h-4 text-slate-400" /> View Complaint
              </button>
            </div>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-green-50 text-[#22C55E] flex items-center justify-center shrink-0"><UserCheck class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Available</p>
                <p class="text-lg font-bold text-slate-900">18</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-amber-50 text-amber-500 flex items-center justify-center shrink-0"><Briefcase class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Busy Workers</p>
                <p class="text-lg font-bold text-slate-900">42</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0"><Users class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Total Workers</p>
                <p class="text-lg font-bold text-slate-900">64</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-red-50 text-red-500 flex items-center justify-center shrink-0"><AlertTriangle class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Emergency Tasks</p>
                <p class="text-lg font-bold text-slate-900">3</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-purple-50 text-purple-500 flex items-center justify-center shrink-0"><Clock class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Avg Response</p>
                <p class="text-lg font-bold text-slate-900">1.2 Hrs</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 flex flex-col md:flex-row gap-6">
            <div class="w-full md:w-32 h-24 rounded-lg overflow-hidden shrink-0 border border-slate-200">
              <img :src="complaint.image" alt="Thumbnail" class="w-full h-full object-cover" />
            </div>
            <div class="flex-1">
              <div class="flex flex-wrap items-start justify-between gap-3 mb-2">
                <div class="flex items-center gap-3">
                  <h3 class="text-lg font-bold text-slate-900">{{ complaint.title }}</h3>
                  <span class="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded bg-slate-100 text-slate-600">{{ complaint.id }}</span>
                  <span class="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded bg-orange-100 text-orange-700">{{ complaint.priority }} Priority</span>
                  <span class="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded bg-blue-100 text-blue-700">{{ complaint.status }}</span>
                </div>
              </div>
              <p class="text-sm text-slate-600 line-clamp-2 mb-3">{{ complaint.description }}</p>
              <div class="flex flex-wrap gap-x-6 gap-y-2 text-sm">
                <span class="flex items-center gap-1.5 text-slate-500"><Building class="w-4 h-4 text-slate-400" /> {{ complaint.category }}</span>
                <span class="flex items-center gap-1.5 text-slate-500"><MapPin class="w-4 h-4 text-slate-400" /> {{ complaint.area }}, {{ complaint.ward }}</span>
                <span class="flex items-center gap-1.5 text-slate-500"><Calendar class="w-4 h-4 text-slate-400" /> Target: {{ complaint.targetDate }}</span>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            
            <div class="xl:col-span-8 flex flex-col gap-6">
              
              <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-4 justify-between items-center z-10">
                <div class="relative w-full lg:w-80">
                  <Search class="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input 
                    v-model="searchQuery"
                    type="text" 
                    placeholder="Search name, ID, or area..." 
                    class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]"
                  />
                </div>
                
                <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
                  <select v-model="filters.department" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                    <option value="All">All Departments</option>
                    <option value="Road Maintenance">Road Maintenance</option>
                    <option value="Electrical">Electrical</option>
                    <option value="Sanitation">Sanitation</option>
                    <option value="Water Supply">Water Supply</option>
                  </select>

                  <select v-model="filters.availability" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                    <option value="All">All Statuses</option>
                    <option value="Available">Available</option>
                    <option value="Busy">Busy</option>
                  </select>

                  <select v-model="filters.sort" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                    <option value="Lowest Workload">Lowest Workload</option>
                    <option value="Highest Rating">Highest Rating</option>
                    <option value="Experience">Experience</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div 
                  v-for="worker in filteredWorkers" :key="worker.id" 
                  class="bg-white rounded-[14px] shadow-sm border p-5 transition-all duration-200"
                  :class="selectedWorker?.id === worker.id ? 'border-[#2563EB] ring-1 ring-[#2563EB] bg-blue-50/10' : 'border-slate-100 hover:shadow-md'"
                >
                  <div class="flex justify-between items-start mb-3">
                    <div class="flex items-center gap-3">
                      <img :src="worker.avatar" class="w-12 h-12 rounded-full object-cover border border-slate-200" />
                      <div>
                        <h4 class="font-bold text-slate-900 text-sm leading-tight">{{ worker.name }}</h4>
                        <p class="text-xs text-slate-500">{{ worker.department }} • {{ worker.experience }} Yrs</p>
                      </div>
                    </div>
                    <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${availabilityClass(worker.status)}`">{{ worker.status }}</span>
                  </div>
                  
                  <div class="grid grid-cols-2 gap-2 text-xs mb-4">
                    <div class="flex items-center gap-1.5 text-slate-600"><MapPin class="w-3.5 h-3.5 text-slate-400" /> {{ worker.area }}</div>
                    <div class="flex items-center gap-1.5 text-slate-600"><Star class="w-3.5 h-3.5 text-amber-400 fill-amber-400" /> {{ worker.rating }} / 5.0</div>
                  </div>

                  <div class="mb-4">
                    <div class="flex justify-between text-xs mb-1">
                      <span class="font-medium text-slate-600">Current Workload</span>
                      <span class="font-bold text-slate-900">{{ worker.tasks }} / {{ worker.maxTasks }} Tasks</span>
                    </div>
                    <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-500" :class="workloadColor(worker.tasks, worker.maxTasks)" :style="`width: ${(worker.tasks / worker.maxTasks) * 100}%`"></div>
                    </div>
                  </div>

                  <div class="flex gap-2">
                    <button @click="openProfile(worker)" class="flex-1 py-2 bg-slate-50 text-slate-700 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors border border-slate-200">View Profile</button>
                    <button @click="selectWorker(worker)" class="flex-1 py-2 text-white text-xs font-bold rounded-lg transition-colors" :class="selectedWorker?.id === worker.id ? 'bg-[#1E40AF]' : 'bg-[#2563EB] hover:bg-[#1E40AF]'">
                      {{ selectedWorker?.id === worker.id ? 'Selected' : 'Select Worker' }}
                    </button>
                  </div>
                </div>
              </div>

              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <Clipboard class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Recent Assignments</h2>
                </div>
                <div class="overflow-x-auto">
                  <table class="w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-slate-50 text-slate-500 font-medium">
                      <tr>
                        <th class="px-5 py-3">ID</th>
                        <th class="px-5 py-3">Worker</th>
                        <th class="px-5 py-3">Category</th>
                        <th class="px-5 py-3">Assigned Date</th>
                        <th class="px-5 py-3">Status</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="assign in recentAssignments" :key="assign.id" class="hover:bg-slate-50">
                        <td class="px-5 py-3 font-mono font-medium text-slate-900">{{ assign.id }}</td>
                        <td class="px-5 py-3 font-medium text-slate-700">{{ assign.worker }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ assign.category }}</td>
                        <td class="px-5 py-3 text-slate-500">{{ assign.date }}</td>
                        <td class="px-5 py-3"><span :class="`px-2 py-0.5 rounded text-[10px] font-bold ${statusBadge(assign.status)}`">{{ assign.status }}</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <div class="xl:col-span-4 flex flex-col gap-6">
              
              <div class="bg-white rounded-[14px] shadow-sm border border-[#2563EB]/20 overflow-hidden sticky top-6">
                <div class="p-5 bg-[#2563EB]/5 border-b border-[#2563EB]/10">
                  <h2 class="font-bold text-[#1E40AF]">Assignment Details</h2>
                </div>
                <div class="p-5 space-y-5">
                  
                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Selected Worker</label>
                    <div v-if="selectedWorker" class="flex items-center gap-3 p-3 bg-blue-50 border border-blue-100 rounded-lg">
                      <img :src="selectedWorker.avatar" class="w-8 h-8 rounded-full object-cover" />
                      <div class="flex-1">
                        <p class="font-bold text-slate-900 text-sm leading-tight">{{ selectedWorker.name }}</p>
                        <p class="text-xs text-slate-600">{{ selectedWorker.department }}</p>
                      </div>
                      <button @click="selectedWorker = null" class="text-slate-400 hover:text-red-500"><X class="w-4 h-4" /></button>
                    </div>
                    <div v-else class="p-4 border-2 border-dashed border-slate-200 rounded-lg text-center bg-slate-50">
                      <p class="text-sm text-slate-500 font-medium">Please select a worker from the list.</p>
                    </div>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Complaint Priority</label>
                    <select v-model="form.priority" class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                      <option value="Low">Low</option>
                      <option value="Medium">Medium</option>
                      <option value="High">High</option>
                      <option value="Emergency">Emergency</option>
                    </select>
                  </div>

                  <div class="grid grid-cols-2 gap-3">
                    <div>
                      <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Expected Date</label>
                      <input type="date" v-model="form.completionDate" class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5" />
                    </div>
                    <div>
                      <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Est. Time</label>
                      <select v-model="form.completionTime" class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                        <option>Same Day</option>
                        <option>1 Day</option>
                        <option>2 Days</option>
                        <option>3 Days</option>
                        <option>1 Week</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Assignment Notes</label>
                    <textarea v-model="form.notes" rows="2" placeholder="Add instructions for the assigned worker..." class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"></textarea>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Internal Remarks</label>
                    <textarea v-model="form.remarks" rows="2" placeholder="Officer-only notes..." class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"></textarea>
                  </div>

                  <div class="bg-slate-50 p-4 rounded-lg border border-slate-100 space-y-3">
                    <p class="text-xs font-bold text-slate-700 uppercase tracking-wide mb-2">Assignment Checklist</p>
                    <label class="flex items-center gap-3 cursor-pointer">
                      <input type="checkbox" v-model="form.checks.verified" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <span class="text-sm text-slate-700">Complaint verified</span>
                    </label>
                    <label class="flex items-center gap-3 cursor-pointer">
                      <input type="checkbox" v-model="form.checks.materials" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <span class="text-sm text-slate-700">Required materials available</span>
                    </label>
                    <label class="flex items-center gap-3 cursor-pointer">
                      <input type="checkbox" v-model="form.checks.location" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <span class="text-sm text-slate-700">Location confirmed</span>
                    </label>
                    <label class="flex items-center gap-3 cursor-pointer">
                      <input type="checkbox" v-model="form.checks.notified" class="w-4 h-4 rounded border-slate-300 text-[#2563EB] focus:ring-[#2563EB]" />
                      <span class="text-sm text-slate-700">Worker notified</span>
                    </label>
                  </div>
                </div>
                <div class="p-5 bg-slate-50 border-t border-slate-100 flex flex-col gap-2">
                  <button @click="confirmAssignment" :disabled="!selectedWorker" class="w-full py-3 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed">
                    Assign Complaint
                  </button>
                  <button @click="resetForm" class="w-full py-2.5 text-sm font-bold text-slate-600 bg-white border border-slate-300 hover:bg-slate-100 rounded-lg transition-colors">
                    Reset Form
                  </button>
                </div>
              </div>

              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h2 class="font-bold text-slate-900 mb-4">Assignment History</h2>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-5">
                  <div class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#F59E0B] rounded-full ring-4 ring-white"></div>
                    <p class="text-sm font-bold text-slate-900">Complaint Verified</p>
                    <p class="text-xs text-slate-500">Jul 08, 2026 • 10:15 AM</p>
                  </div>
                  <div class="relative opacity-40">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-slate-300 rounded-full ring-4 ring-white"></div>
                    <p class="text-sm font-bold text-slate-900">Assigned to Worker</p>
                  </div>
                  <div class="relative opacity-40">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-slate-300 rounded-full ring-4 ring-white"></div>
                    <p class="text-sm font-bold text-slate-900">Work Started</p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </main>

    <!-- Worker Profile Drawer -->
    <Teleport to="body">
      <div v-if="profileDrawer" class="fixed inset-0 z-50 bg-slate-900/20 backdrop-blur-sm flex justify-end animate-fade-in" @click="profileDrawer = false">
        <div class="w-full max-w-md bg-white h-full shadow-2xl flex flex-col transform transition-transform animate-slide-in" @click.stop>
          <div class="p-6 border-b border-slate-100 flex justify-between items-start bg-slate-50">
            <div class="flex items-center gap-4">
              <img :src="activeProfile.avatar" class="w-16 h-16 rounded-full object-cover border-2 border-white shadow-sm" />
              <div>
                <h2 class="text-xl font-bold text-slate-900">{{ activeProfile.name }}</h2>
                <p class="text-sm text-slate-500">{{ activeProfile.department }}</p>
                <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider mt-1 inline-block ${availabilityClass(activeProfile.status)}`">{{ activeProfile.status }}</span>
              </div>
            </div>
            <button @click="profileDrawer = false" class="text-slate-400 hover:text-slate-600"><X class="w-6 h-6"/></button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6 space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Experience</p>
                <p class="font-bold text-slate-900">{{ activeProfile.experience }} Years</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Rating</p>
                <p class="font-bold text-slate-900 flex items-center gap-1"><Star class="w-4 h-4 text-amber-400 fill-amber-400"/> {{ activeProfile.rating }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Current Workload</p>
                <p class="font-bold text-slate-900">{{ activeProfile.tasks }} Tasks</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Completed</p>
                <p class="font-bold text-slate-900">{{ activeProfile.completedTasks }}</p>
              </div>
            </div>

            <div>
              <h3 class="font-bold text-slate-900 mb-3">Contact Information</h3>
              <div class="space-y-3 text-sm">
                <div class="flex items-center gap-3 text-slate-600"><Phone class="w-4 h-4 text-slate-400" /> {{ activeProfile.phone }}</div>
                <div class="flex items-center gap-3 text-slate-600"><Mail class="w-4 h-4 text-slate-400" /> {{ activeProfile.email }}</div>
                <div class="flex items-center gap-3 text-slate-600"><MapPin class="w-4 h-4 text-slate-400" /> Current Area: {{ activeProfile.area }}</div>
              </div>
            </div>

            <div>
              <h3 class="font-bold text-slate-900 mb-3">Skills & Expertise</h3>
              <div class="flex flex-wrap gap-2">
                <span v-for="skill in activeProfile.skills" :key="skill" class="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-semibold rounded-full border border-slate-200">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="p-6 border-t border-slate-100 bg-white">
            <button @click="selectWorkerFromDrawer" class="w-full py-3 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm">
              Assign to this Worker
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Confirmation Modal -->
    <Teleport to="body">
      <div v-if="showConfirm" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white p-6 rounded-2xl max-w-sm w-full shadow-2xl">
          <h3 class="text-lg font-bold text-slate-900 mb-2">Confirm Assignment</h3>
          <p class="text-sm text-slate-600 mb-4">You are about to assign <strong>{{ complaint.id }}</strong> to <strong>{{ selectedWorker?.name }}</strong>.</p>
          <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 text-sm space-y-2 mb-6">
            <div class="flex justify-between"><span class="text-slate-500">Priority:</span> <span class="font-bold text-slate-900">{{ form.priority }}</span></div>
            <div class="flex justify-between"><span class="text-slate-500">Expected:</span> <span class="font-bold text-slate-900">{{ form.completionDate || 'Not set' }}</span></div>
          </div>
          <div class="flex gap-3">
            <button @click="showConfirm = false" class="flex-1 py-2.5 bg-slate-100 text-slate-700 font-bold rounded-lg hover:bg-slate-200 transition-colors">Cancel</button>
            <button @click="processAssignment" class="flex-1 py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex justify-center items-center gap-2">
              <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              Confirm
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Success Modal -->
    <Teleport to="body">
      <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white p-8 rounded-2xl max-w-sm w-full text-center shadow-2xl">
          <div class="w-16 h-16 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle class="w-8 h-8" />
          </div>
          <h3 class="text-xl font-bold text-slate-900 mb-2">Assigned Successfully</h3>
          <p class="text-sm text-slate-600 mb-6">The complaint has been assigned to {{ selectedWorker?.name }}. They have been notified.</p>
          <div class="space-y-3">
            <router-link to="/officer/details/CMP-2026-0892" class="block w-full py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors">View Complaint</router-link>
            <router-link to="/officer/dashboard" class="block w-full py-2.5 bg-slate-100 text-slate-700 font-bold rounded-lg hover:bg-slate-200 transition-colors">Dashboard</router-link>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Printer, Download, Eye, Clock, Calendar, AlertCircle, Flag, MapPin, 
  Building, UserCheck, Briefcase, Users, AlertTriangle, Search, Star, 
  Clipboard, Phone, Mail, X, CheckCircle
} from 'lucide-vue-next'

const isSidebarOpen = ref(false)
const profileDrawer = ref(false)
const showConfirm = ref(false)
const showSuccess = ref(false)
const isSubmitting = ref(false)

const activeProfile = ref({})
const selectedWorker = ref(null)
const searchQuery = ref('')

const filters = reactive({
  department: 'All',
  availability: 'All',
  sort: 'Lowest Workload'
})

const form = reactive({
  priority: 'High',
  completionDate: '2026-07-12',
  completionTime: '1 Day',
  notes: '',
  remarks: '',
  checks: {
    verified: true,
    materials: false,
    location: true,
    notified: false
  }
})

// Dummy Complaint
const complaint = reactive({
  id: 'CMP-2026-0892',
  title: 'Deep Pothole causing traffic disruption',
  category: 'Road Maintenance',
  priority: 'High',
  status: 'Verified',
  description: 'Massive pothole formed after the recent rains. Causing severe traffic slowdowns and dangerous for two-wheelers.',
  targetDate: 'Jul 12, 2026',
  area: 'Downtown',
  ward: 'Ward 14',
  image: 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&q=80&w=400'
})

// Dummy Workers
const workers = reactive([
  { id: 'W001', name: 'Amit Singh', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200', department: 'Road Maintenance', experience: 5, status: 'Available', tasks: 2, maxTasks: 5, rating: 4.8, area: 'Downtown', phone: '+91 98765 11111', email: 'amit.s@civicdesk.in', completedTasks: 142, skills: ['Asphalt Laying', 'Heavy Machinery', 'Traffic Mgmt'] },
  { id: 'W002', name: 'Suresh Patil', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=200', department: 'Road Maintenance', experience: 8, status: 'Busy', tasks: 5, maxTasks: 5, rating: 4.9, area: 'North Zone', phone: '+91 98765 22222', email: 'suresh.p@civicdesk.in', completedTasks: 310, skills: ['Surveying', 'Concrete Repair'] },
  { id: 'W003', name: 'Vijay Sharma', avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&q=80&w=200', department: 'Sanitation', experience: 3, status: 'Available', tasks: 1, maxTasks: 6, rating: 4.5, area: 'Downtown', phone: '+91 98765 33333', email: 'vijay.s@civicdesk.in', completedTasks: 89, skills: ['Waste Management', 'Driving'] },
  { id: 'W004', name: 'Rahul Verma', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=200', department: 'Electrical', experience: 2, status: 'Available', tasks: 3, maxTasks: 4, rating: 4.2, area: 'East Ward', phone: '+91 98765 44444', email: 'rahul.v@civicdesk.in', completedTasks: 45, skills: ['Wiring', 'Streetlight Repair'] }
])

const recentAssignments = [
  { id: 'CMP-0891', worker: 'Suresh Patil', category: 'Road Maintenance', date: 'Jul 09, 2026', status: 'In Progress' },
  { id: 'CMP-0870', worker: 'Rahul Verma', category: 'Electrical', date: 'Jul 08, 2026', status: 'Completed' },
]

// Computed
const filteredWorkers = computed(() => {
  let result = workers.filter(w => {
    const matchSearch = !searchQuery.value || w.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || w.area.toLowerCase().includes(searchQuery.value.toLowerCase()) || w.id.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchDept = filters.department === 'All' || w.department === filters.department
    const matchAvail = filters.availability === 'All' || w.status === filters.availability
    return matchSearch && matchDept && matchAvail
  })

  if (filters.sort === 'Lowest Workload') result.sort((a, b) => (a.tasks / a.maxTasks) - (b.tasks / b.maxTasks))
  if (filters.sort === 'Highest Rating') result.sort((a, b) => b.rating - a.rating)
  if (filters.sort === 'Experience') result.sort((a, b) => b.experience - a.experience)

  return result
})

// Methods
const availabilityClass = (status) => status === 'Available' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
const workloadColor = (tasks, max) => (tasks / max) > 0.8 ? 'bg-red-500' : (tasks / max) > 0.5 ? 'bg-amber-400' : 'bg-green-500'
const statusBadge = (status) => status === 'Completed' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'

const openProfile = (worker) => {
  activeProfile.value = worker
  profileDrawer.value = true
}

const selectWorker = (worker) => {
  selectedWorker.value = worker
}

const selectWorkerFromDrawer = () => {
  selectWorker(activeProfile.value)
  profileDrawer.value = false
}

const resetForm = () => {
  selectedWorker.value = null
  form.notes = ''
  form.remarks = ''
  form.priority = 'High'
  Object.keys(form.checks).forEach(k => form.checks[k] = false)
}

const confirmAssignment = () => {
  if (selectedWorker.value) showConfirm.value = true
}

const processAssignment = async () => {
  isSubmitting.value = true
  await new Promise(resolve => setTimeout(resolve, 1500)) // Fake API call
  isSubmitting.value = false
  showConfirm.value = false
  showSuccess.value = true
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}
.animate-slide-in {
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

/* Tooltip implementation for quick action buttons */
.tooltip-trigger {
  position: relative;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>