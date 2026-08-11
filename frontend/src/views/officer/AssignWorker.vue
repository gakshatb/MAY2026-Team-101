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
                <router-link :to="`/officer/complaintdetails/${route.params.id}`" class="hover:text-[#2563EB] transition-colors">{{ complaint.id }}</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Assign Worker</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Assign Worker</h1>
              <p class="text-slate-500 mt-1">Assign the complaint to the most suitable field worker.</p>
            </div>
            
            <div class="flex gap-2">
              <router-link :to="`/officer/complaintdetails/${route.params.id}`" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-2">
                <Eye class="w-4 h-4 text-slate-400" /> View Complaint
              </router-link>
            </div>
          </div>

          <div v-if="loadError" class="bg-red-50 border border-red-100 text-red-600 text-sm rounded-[14px] p-4 flex items-center justify-between">
            {{ loadError }} <button @click="fetchAll" class="font-bold underline shrink-0 ml-4">Retry</button>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-green-50 text-[#22C55E] flex items-center justify-center shrink-0"><UserCheck class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Available</p>
                <p class="text-lg font-bold text-slate-900">{{ (summary.active ?? 0) - (summary.busyNow ?? 0) }}</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-amber-50 text-amber-500 flex items-center justify-center shrink-0"><Briefcase class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Busy Workers</p>
                <p class="text-lg font-bold text-slate-900">{{ summary.busyNow ?? 0 }}</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0"><Users class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Total Workers</p>
                <p class="text-lg font-bold text-slate-900">{{ summary.total ?? 0 }}</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-purple-50 text-purple-500 flex items-center justify-center shrink-0"><Star class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Avg Rating</p>
                <p class="text-lg font-bold text-slate-900">{{ summary.avgRating ?? '—' }}</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-teal-50 text-teal-600 flex items-center justify-center shrink-0"><Clipboard class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Completed Total</p>
                <p class="text-lg font-bold text-slate-900">{{ summary.completedTotal ?? 0 }}</p>
              </div>
            </div>
          </div>

          <div v-if="!isLoading" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 flex flex-col md:flex-row gap-6">
            <div class="w-full md:w-32 h-24 rounded-lg overflow-hidden shrink-0 border border-slate-200 bg-slate-50">
              <img v-if="complaint.images?.length" :src="`http://127.0.0.1:5000${complaint.images[0]}`" alt="Thumbnail" class="w-full h-full object-cover" />
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
                <span class="flex items-center gap-1.5 text-slate-500"><MapPin class="w-4 h-4 text-slate-400" /> {{ complaint.location?.area }}, {{ complaint.location?.ward }}</span>
                <span class="flex items-center gap-1.5 text-slate-500"><Calendar class="w-4 h-4 text-slate-400" /> Target: {{ complaint.targetDate }}</span>
              </div>
            </div>
          </div>
          <div v-else class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-8 text-center text-slate-400">Loading complaint…</div>

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
                  <select v-model="filters.availability" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                    <option value="All">All Statuses</option>
                    <option value="Available">Available</option>
                    <option value="Busy">Busy</option>
                  </select>

                  <select v-model="filters.sort" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2">
                    <option value="Lowest Workload">Lowest Workload</option>
                    <option value="Highest Rating">Highest Rating</option>
                    <option value="Most Completed">Most Completed</option>
                  </select>
                </div>
              </div>

              <div v-if="isLoading" class="text-center text-slate-400 py-16">Loading workers…</div>
              <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div 
                  v-for="worker in filteredWorkers" :key="worker.id" 
                  class="bg-white rounded-[14px] shadow-sm border p-5 transition-all duration-200"
                  :class="selectedWorker?.id === worker.id ? 'border-[#2563EB] ring-1 ring-[#2563EB] bg-blue-50/10' : 'border-slate-100 hover:shadow-md'"
                >
                  <div class="flex justify-between items-start mb-3">
                    <div class="flex items-center gap-3">
                      <img :src="workerAvatar(worker)" class="w-12 h-12 rounded-full object-cover border border-slate-200" />
                      <div>
                        <h4 class="font-bold text-slate-900 text-sm leading-tight">{{ worker.name }}</h4>
                        <p class="text-xs text-slate-500">{{ worker.department }} • Since {{ worker.memberSince || '—' }}</p>
                      </div>
                    </div>
                    <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${availabilityClass(workerAvailability(worker))}`">{{ workerAvailability(worker) }}</span>
                  </div>
                  
                  <div class="grid grid-cols-2 gap-2 text-xs mb-4">
                    <div class="flex items-center gap-1.5 text-slate-600"><Clipboard class="w-3.5 h-3.5 text-slate-400" /> {{ worker.completedTasks }} completed</div>
                    <div class="flex items-center gap-1.5 text-slate-600"><Star class="w-3.5 h-3.5 text-amber-400 fill-amber-400" /> {{ worker.avgRating ?? '—' }} / 5.0</div>
                  </div>

                  <div class="mb-4">
                    <div class="flex justify-between text-xs mb-1">
                      <span class="font-medium text-slate-600">Current Workload</span>
                      <span class="font-bold text-slate-900">{{ worker.activeTasks }} active task{{ worker.activeTasks === 1 ? '' : 's' }}</span>
                    </div>
                    <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-500" :class="workloadColor(worker.activeTasks)" :style="`width: ${Math.min(100, worker.activeTasks * 25)}%`"></div>
                    </div>
                  </div>

                  <div class="flex gap-2">
                    <button @click="openProfile(worker)" class="flex-1 py-2 bg-slate-50 text-slate-700 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors border border-slate-200">View Profile</button>
                    <button @click="selectWorker(worker)" class="flex-1 py-2 text-white text-xs font-bold rounded-lg transition-colors" :class="selectedWorker?.id === worker.id ? 'bg-[#1E40AF]' : 'bg-[#2563EB] hover:bg-[#1E40AF]'">
                      {{ selectedWorker?.id === worker.id ? 'Selected' : 'Select Worker' }}
                    </button>
                  </div>
                </div>
                <div v-if="filteredWorkers.length === 0" class="md:col-span-2 bg-white p-10 rounded-[14px] border border-slate-100 text-center text-slate-400">No workers match these filters.</div>
              </div>

              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h2 class="font-bold text-slate-900 mb-4">Assignment History</h2>
                <div v-if="complaint.history?.length" class="relative pl-4 border-l-2 border-slate-100 space-y-5">
                  <div v-for="entry in complaint.history" :key="entry.date + entry.time" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#F59E0B] rounded-full ring-4 ring-white"></div>
                    <p class="text-sm font-bold text-slate-900">{{ entry.action }}</p>
                    <p class="text-xs text-slate-500">{{ entry.date }} • {{ entry.time }}<span v-if="entry.detail"> — {{ entry.detail }}</span></p>
                  </div>
                </div>
                <p v-else class="text-sm text-slate-400">No history yet for this complaint.</p>
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
              <img :src="workerAvatar(activeProfile)" class="w-16 h-16 rounded-full object-cover border-2 border-white shadow-sm" />
              <div>
                <h2 class="text-xl font-bold text-slate-900">{{ activeProfile.name }}</h2>
                <p class="text-sm text-slate-500">{{ activeProfile.department }}</p>
                <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider mt-1 inline-block ${availabilityClass(workerAvailability(activeProfile))}`">{{ workerAvailability(activeProfile) }}</span>
              </div>
            </div>
            <button @click="profileDrawer = false" class="text-slate-400 hover:text-slate-600"><X class="w-6 h-6"/></button>
          </div>
          
          <div v-if="isProfileLoading" class="flex-1 flex items-center justify-center text-slate-400">Loading profile…</div>
          <div v-else class="flex-1 overflow-y-auto p-6 space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Member Since</p>
                <p class="font-bold text-slate-900">{{ activeProfile.memberSince || '—' }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Rating</p>
                <p class="font-bold text-slate-900 flex items-center gap-1"><Star class="w-4 h-4 text-amber-400 fill-amber-400"/> {{ activeProfile.avgRating ?? '—' }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Current Workload</p>
                <p class="font-bold text-slate-900">{{ activeProfile.activeTasks }} Tasks</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Completed</p>
                <p class="font-bold text-slate-900">{{ activeProfile.completedTasks }}</p>
              </div>
            </div>

            <div>
              <h3 class="font-bold text-slate-900 mb-3">Contact Information</h3>
              <div class="space-y-3 text-sm">
                <div class="flex items-center gap-3 text-slate-600"><Phone class="w-4 h-4 text-slate-400" /> {{ activeProfile.phone || '—' }}</div>
                <div class="flex items-center gap-3 text-slate-600"><Mail class="w-4 h-4 text-slate-400" /> {{ activeProfile.email || '—' }}</div>
              </div>
            </div>

            <div>
              <h3 class="font-bold text-slate-900 mb-3">Current Assignments</h3>
              <div v-if="activeProfile.currentAssignments?.length" class="space-y-2">
                <div v-for="a in activeProfile.currentAssignments" :key="a.id" class="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100 text-sm">
                  <div>
                    <p class="font-mono font-bold text-slate-900">{{ a.id }}</p>
                    <p class="text-xs text-slate-500">{{ a.category }}<span v-if="a.expectedCompletionDate"> • due {{ a.expectedCompletionDate }}</span></p>
                  </div>
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-blue-100 text-blue-700">{{ a.status }}</span>
                </div>
              </div>
              <p v-else class="text-sm text-slate-400">No active assignments right now.</p>
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
          <p v-if="assignError" class="text-red-600 text-xs mb-4">{{ assignError }}</p>
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
            <router-link :to="`/officer/complaintdetails/${route.params.id}`" class="block w-full py-2.5 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors">View Complaint</router-link>
            <router-link to="/officer/dashboard" class="block w-full py-2.5 bg-slate-100 text-slate-700 font-bold rounded-lg hover:bg-slate-200 transition-colors">Dashboard</router-link>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import {
  Eye, Clock, Calendar, MapPin,
  Building, UserCheck, Briefcase, Users, Search, Star,
  Clipboard, Phone, Mail, X, CheckCircle
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
const defaultAvatar = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop'

const route = useRoute()
const router = useRouter()

const isSidebarOpen = ref(false)
const profileDrawer = ref(false)
const showConfirm = ref(false)
const showSuccess = ref(false)
const isSubmitting = ref(false)
const isLoading = ref(true)
const isProfileLoading = ref(false)
const loadError = ref('')
const assignError = ref('')

const activeProfile = ref({})
const selectedWorker = ref(null)
const searchQuery = ref('')

const complaint = ref({})
const workers = ref([])
const summary = ref({})

const filters = reactive({
  availability: 'All',
  sort: 'Lowest Workload'
})

const form = reactive({
  priority: 'High',
  completionDate: '',
  completionTime: '1 Day',
  notes: '',
  remarks: '',
  checks: {
    verified: false,
    materials: false,
    location: false,
    notified: false
  }
})

// Computed
const filteredWorkers = computed(() => {
  let result = workers.value.filter(w => {
    const q = searchQuery.value.toLowerCase()
    const matchSearch = !q || w.name.toLowerCase().includes(q) || w.empId.toLowerCase().includes(q)
    const matchAvail = filters.availability === 'All' || workerAvailability(w) === filters.availability
    return matchSearch && matchAvail
  })

  if (filters.sort === 'Lowest Workload') result = [...result].sort((a, b) => a.activeTasks - b.activeTasks)
  if (filters.sort === 'Highest Rating') result = [...result].sort((a, b) => (b.avgRating || 0) - (a.avgRating || 0))
  if (filters.sort === 'Most Completed') result = [...result].sort((a, b) => b.completedTasks - a.completedTasks)

  return result
})

// Methods
const workerAvatar = (w) => w?.profilePhoto ? `http://127.0.0.1:5000${w.profilePhoto}` : defaultAvatar
const workerAvailability = (w) => (w?.accountStatus === 'active' && w?.activeTasks === 0) ? 'Available' : 'Busy'
const availabilityClass = (status) => status === 'Available' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
const workloadColor = (activeTasks) => activeTasks >= 4 ? 'bg-red-500' : activeTasks >= 2 ? 'bg-amber-400' : 'bg-green-500'

const fetchComplaint = async () => {
  let id = route.params.id
  if (!id) {
    // No complaint id in the URL (e.g. reached via the sidebar's generic
    // "Assign Worker" link) — fall back to the oldest complaint of this
    // officer's that's still waiting on a worker, and put it in the URL
    // so the rest of this page keeps working off route.params.id as before.
    const { data: listData } = await axios.get(`${API_BASE}/complaints`, { ...authHeaders(), params: { status: 'Assigned' } })
    const rows = listData.complaints || []
    const target = rows[rows.length - 1]
    if (!target) {
      throw new Error('NO_COMPLAINTS_TO_ASSIGN')
    }
    id = target.rawId
    await router.replace(`/officer/assign/${id}`)
  }
  const { data } = await axios.get(`${API_BASE}/complaints/${id}`, authHeaders())
  complaint.value = data.complaint
}

const fetchWorkers = async () => {
  const { data } = await axios.get(`${API_BASE}/workers`, authHeaders())
  workers.value = data.workers
  summary.value = data.summary
}

const fetchAll = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    await Promise.all([fetchComplaint(), fetchWorkers()])
  } catch (err) {
    loadError.value = err.message === 'NO_COMPLAINTS_TO_ASSIGN'
      ? 'There are no complaints waiting on a worker right now.'
      : (err.response?.data?.message || 'Failed to load assignment data.')
  } finally {
    isLoading.value = false
  }
}

const openProfile = async (worker) => {
  activeProfile.value = worker
  profileDrawer.value = true
  isProfileLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/workers/${worker.id}`, authHeaders())
    activeProfile.value = data.worker
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load worker profile.'
  } finally {
    isProfileLoading.value = false
  }
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
  form.completionDate = ''
  form.completionTime = '1 Day'
  Object.keys(form.checks).forEach(k => form.checks[k] = false)
}

const confirmAssignment = () => {
  if (selectedWorker.value) showConfirm.value = true
}

const processAssignment = async () => {
  if (!selectedWorker.value) return
  isSubmitting.value = true
  assignError.value = ''
  try {
    await axios.patch(`${API_BASE}/complaints/${route.params.id}/assign-worker`, {
      worker_id: selectedWorker.value.id,
      priority: form.priority,
      notes: form.notes,
      remarks: form.remarks,
      expectedCompletionDate: form.completionDate || undefined,
      expectedDuration: form.completionTime,
      checks: { ...form.checks },
    }, authHeaders())
    showConfirm.value = false
    showSuccess.value = true
  } catch (err) {
    assignError.value = err.response?.data?.message || 'Failed to assign worker.'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(fetchAll)
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