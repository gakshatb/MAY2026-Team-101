<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1600px] mx-auto space-y-6">
          
          <!-- Header & Breadcrumbs & Quick Actions -->
          <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">Manage Workers</span>
              </nav>
              <h1 class="text-2xl font-bold text-slate-900">Manage Workers</h1>
              <p class="text-slate-500 mt-1">Monitor workforce, track assignments, and manage field operations efficiently.</p>
            </div>
            
            <div class="flex flex-wrap gap-2">
              <button @click="openModal('assign')" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 font-medium rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-2 shadow-sm">
                <Clipboard class="w-4 h-4 text-[#2563EB]" /> Assign Complaint
              </button>
              <button disabled title="Not available yet — workers register themselves." class="px-4 py-2 bg-white border border-slate-200 text-slate-400 font-medium rounded-lg flex items-center gap-2 shadow-sm cursor-not-allowed opacity-60">
                <UserPlus class="w-4 h-4" /> Add Worker
              </button>
              <button disabled title="Not available yet." class="px-4 py-2 bg-white border border-slate-200 text-slate-400 font-medium rounded-lg flex items-center gap-2 shadow-sm cursor-not-allowed opacity-60">
                <Download class="w-4 h-4" /> Export Workers
              </button>
              <button disabled title="Not available yet." class="px-4 py-2 bg-[#2563EB] text-white font-medium rounded-lg flex items-center gap-2 shadow-sm cursor-not-allowed opacity-60">
                <BarChart class="w-4 h-4" /> Generate Report
              </button>
            </div>
          </div>

          <!-- Statistics Cards Grid -->
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
            <div v-for="stat in statistics" :key="stat.title" class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start mb-2">
                <div :class="`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${stat.iconBg} ${stat.iconColor}`">
                  <component :is="stat.icon" class="w-4 h-4" />
                </div>
                <span v-if="stat.trend" :class="`text-[10px] font-bold px-1.5 py-0.5 rounded ${stat.trend > 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}`">
                  {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
                </span>
              </div>
              <div>
                <p class="text-xl font-bold text-slate-900">{{ stat.value }}</p>
                <p class="text-[11px] font-medium text-slate-500 mt-0.5 leading-tight">{{ stat.title }}</p>
              </div>
            </div>
          </div>

          <!-- Search & Filters Toolbar -->
          <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex flex-col xl:flex-row gap-4 justify-between items-center z-10">
            <!-- Search -->
            <div class="relative w-full xl:w-96 shrink-0">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input 
                v-model="filters.search"
                type="text" 
                placeholder="Search by name, ID, dept, or area..." 
                class="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
            
            <!-- Filters -->
            <div class="flex flex-wrap items-center justify-end gap-3 w-full">
              <select v-model="filters.department" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2.5 outline-none">
                <option value="All">All Departments</option>
                <option v-for="dept in departmentOptions" :key="dept" :value="dept">{{ dept }}</option>
              </select>

              <select v-model="filters.availability" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2.5 outline-none">
                <option value="All">All Statuses</option>
                <option value="Available">Available</option>
                <option value="Busy">Busy</option>
                <option value="Offline">Offline</option>
                <option value="On Leave">On Leave</option>
              </select>

              <select v-model="filters.experience" title="Not tracked yet — kept for future use" class="bg-slate-50 border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2.5 outline-none">
                <option value="All">Any Experience</option>
                <option value="0-2">0–2 Years</option>
                <option value="2-5">2–5 Years</option>
                <option value="5-10">5–10 Years</option>
                <option value="10+">10+ Years</option>
              </select>

              <select v-model="filters.sort" class="bg-white border border-slate-300 text-slate-900 font-medium text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2.5 outline-none shadow-sm">
                <option value="Name">Sort by: Name</option>
                <option value="Performance">Sort by: Performance</option>
                <option value="Tasks Completed">Sort by: Tasks Completed</option>
                <option value="Availability">Sort by: Availability</option>
              </select>
            </div>
          </div>

          <!-- Worker Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div v-for="worker in filteredWorkers" :key="worker.id" class="bg-white rounded-[14px] shadow-sm border border-slate-100 hover:shadow-lg transition-all duration-300 flex flex-col overflow-hidden group">
              <div class="p-5 flex-1">
                <!-- Top Row -->
                <div class="flex justify-between items-start mb-4">
                  <div class="flex items-center gap-3">
                    <img :src="avatarUrl(worker.name)" class="w-14 h-14 rounded-full object-cover border-2 border-slate-100" />
                    <div>
                      <h3 class="font-bold text-slate-900 leading-tight">{{ worker.name }}</h3>
                      <p class="text-xs font-mono text-slate-500">{{ worker.id }}</p>
                    </div>
                  </div>
                  <span :class="`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${availabilityBadge(worker.status)}`">{{ worker.status }}</span>
                </div>
                
                <!-- Info Grid -->
                <div class="grid grid-cols-2 gap-y-3 gap-x-2 text-xs mb-4">
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Department</span>
                    <span class="text-slate-700 font-semibold truncate">{{ worker.department }}</span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Area</span>
                    <span class="text-slate-700 font-semibold truncate">{{ worker.area || 'Not tracked' }}</span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Rating</span>
                    <span class="text-amber-500 font-bold flex items-center gap-1"><Star class="w-3 h-3 fill-amber-500"/> {{ worker.rating ?? '—' }}</span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-slate-400 font-medium">Experience</span>
                    <span class="text-slate-700 font-semibold">{{ worker.experience != null ? worker.experience + ' Yrs' : 'Not tracked' }}</span>
                  </div>
                </div>

                <!-- Workload Progress -->
                <div class="mb-2">
                  <div class="flex justify-between text-xs mb-1">
                    <span class="font-medium text-slate-500">Today's Workload</span>
                    <span class="font-bold text-slate-900">{{ worker.pendingTasks }} Pending / {{ worker.todayTasks }} Total</span>
                  </div>
                  <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full rounded-full transition-all duration-500" :class="workloadColor(worker.pendingTasks, worker.todayTasks)" :style="`width: ${(worker.pendingTasks / (worker.todayTasks || 1)) * 100}%`"></div>
                  </div>
                </div>
              </div>

              <!-- Bottom Actions -->
              <div class="bg-slate-50 border-t border-slate-100 p-3 grid grid-cols-4 gap-2">
                <button @click="openDrawer(worker)" class="col-span-2 py-2 bg-white border border-slate-200 text-slate-700 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors flex items-center justify-center gap-1.5 shadow-sm">
                  <Eye class="w-3.5 h-3.5" /> Profile
                </button>
                <button
                  @click="openModal('assign', worker)"
                  :disabled="!worker.isOwnDepartment || worker.accountStatus !== 'active'"
                  :title="!worker.isOwnDepartment ? 'Officers can only manage workers in their own department.' : ''"
                  class="col-span-2 py-2 bg-[#2563EB] text-white text-xs font-bold rounded-lg hover:bg-[#1E40AF] transition-colors flex items-center justify-center gap-1.5 shadow-sm disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <Clipboard class="w-3.5 h-3.5" /> Assign
                </button>
                <button
                  @click="openModal('edit', worker)"
                  :disabled="!worker.isOwnDepartment"
                  :title="!worker.isOwnDepartment ? 'Officers can only manage workers in their own department.' : ''"
                  class="col-span-2 py-2 bg-white border border-slate-200 text-slate-600 text-xs font-bold rounded-lg hover:bg-slate-100 transition-colors flex items-center justify-center gap-1.5 shadow-sm disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <Edit class="w-3.5 h-3.5" /> Edit
                </button>
                <button
                  v-if="worker.accountStatus === 'active'"
                  @click="openModal('deactivate', worker)"
                  :disabled="!worker.isOwnDepartment"
                  :title="!worker.isOwnDepartment ? 'Officers can only manage workers in their own department.' : ''"
                  class="col-span-2 py-2 bg-red-50 text-red-600 text-xs font-bold rounded-lg hover:bg-red-100 transition-colors flex items-center justify-center gap-1.5 shadow-sm border border-red-100 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <UserX class="w-3.5 h-3.5" /> Deactivate
                </button>
                <button
                  v-else
                  @click="openModal('reactivate', worker)"
                  :disabled="!worker.isOwnDepartment"
                  :title="!worker.isOwnDepartment ? 'Officers can only manage workers in their own department.' : ''"
                  class="col-span-2 py-2 bg-green-50 text-green-700 text-xs font-bold rounded-lg hover:bg-green-100 transition-colors flex items-center justify-center gap-1.5 shadow-sm border border-green-100 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <UserCheck class="w-3.5 h-3.5" /> Reactivate
                </button>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredWorkers.length === 0" class="bg-white p-12 rounded-[14px] border border-slate-100 text-center shadow-sm">
            <UserX class="w-12 h-12 text-slate-300 mx-auto mb-4" />
            <h3 class="text-lg font-bold text-slate-900 mb-1">No workers found</h3>
            <p class="text-slate-500 text-sm">Adjust your filters or search query to find workers.</p>
            <button @click="resetFilters" class="mt-4 px-4 py-2 bg-blue-50 text-[#2563EB] text-sm font-bold rounded-lg hover:bg-blue-100 transition-colors">Clear Filters</button>
          </div>

          <!-- Performance Dashboard & Table -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-6">
            <!-- Global Performance Table -->
            <div class="lg:col-span-2 bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
              <div class="p-5 border-b border-slate-100 flex items-center justify-between">
                <h2 class="font-bold text-slate-900 flex items-center gap-2"><BadgeCheck class="w-5 h-5 text-[#2563EB]" /> Top Performers (This Week)</h2>
                <button class="text-sm font-medium text-[#2563EB] hover:underline">View Full Report</button>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-left text-sm whitespace-nowrap">
                  <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide">
                    <tr>
                      <th class="px-5 py-3">Worker</th>
                      <th class="px-5 py-3">Completed</th>
                      <th class="px-5 py-3">Avg Time</th>
                      <th class="px-5 py-3">Score</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100">
                    <tr v-for="perf in performanceData" :key="perf.id" class="hover:bg-slate-50 transition-colors">
                      <td class="px-5 py-3 flex items-center gap-3">
                        <img :src="avatarUrl(perf.name)" class="w-8 h-8 rounded-full object-cover" />
                        <div>
                          <p class="font-bold text-slate-900 leading-none">{{ perf.name }}</p>
                          <p class="text-[10px] text-slate-500 mt-1">{{ perf.department }}</p>
                        </div>
                      </td>
                      <td class="px-5 py-3 text-slate-700 font-medium">{{ perf.completed }} Tasks</td>
                      <td class="px-5 py-3 text-slate-600">{{ perf.avgTime }}</td>
                      <td class="px-5 py-3">
                        <span v-if="perf.score != null" class="px-2 py-1 bg-green-50 text-green-700 font-bold text-xs rounded-full">{{ perf.score }}/100</span>
                        <span v-else class="px-2 py-1 bg-slate-50 text-slate-400 font-bold text-xs rounded-full">No ratings yet</span>
                      </td>
                    </tr>
                    <tr v-if="performanceData.length === 0">
                      <td colspan="4" class="px-5 py-6 text-center text-slate-500 font-medium">No completions in the last 7 days.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Global Charts Placeholder -->
            <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5 flex flex-col">
              <h2 class="font-bold text-slate-900 flex items-center gap-2 mb-6"><PieChart class="w-5 h-5 text-purple-500" /> Overall Task Completion</h2>
              <div class="flex-1 flex flex-col items-center justify-center">
                <div class="relative w-40 h-40 rounded-full flex items-center justify-center mb-6 shadow-inner" :style="`background: conic-gradient(#22C55E 0% ${completionPercent}%, #f1f5f9 ${completionPercent}% 100%);`">
                  <div class="w-32 h-32 bg-white rounded-full flex flex-col items-center justify-center shadow-sm">
                    <span class="text-3xl font-extrabold text-slate-900">{{ completionPercent }}%</span>
                    <span class="text-xs text-slate-500 font-medium">Completion Rate</span>
                  </div>
                </div>
                <div class="w-full space-y-3">
                  <div class="flex justify-between text-sm">
                    <span class="flex items-center gap-2 text-slate-600"><div class="w-3 h-3 rounded bg-[#22C55E]"></div> Completed</span>
                    <span class="font-bold text-slate-900">{{ completionSummary.completed.toLocaleString() }}</span>
                  </div>
                  <div class="flex justify-between text-sm">
                    <span class="flex items-center gap-2 text-slate-600"><div class="w-3 h-3 rounded bg-slate-200"></div> Pending / Dropped</span>
                    <span class="font-bold text-slate-900">{{ completionSummary.pending.toLocaleString() }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </main>

    <!-- Worker Profile Drawer -->
    <Teleport to="body">
      <div v-if="drawerOpen" class="fixed inset-0 z-50 bg-slate-900/30 backdrop-blur-sm flex justify-end animate-fade-in" @click="drawerOpen = false">
        <div class="w-full max-w-2xl bg-white h-full shadow-2xl flex flex-col transform transition-transform animate-slide-in" @click.stop>
          
          <div class="p-6 border-b border-slate-100 flex justify-between items-start bg-slate-50 shrink-0">
            <div class="flex items-center gap-5">
              <img :src="avatarUrl(activeWorker.name)" class="w-20 h-20 rounded-full object-cover border-4 border-white shadow-sm" />
              <div>
                <h2 class="text-2xl font-bold text-slate-900">{{ activeWorker.name }}</h2>
                <p class="text-sm text-slate-600 mb-2">{{ activeWorker.designation }} • {{ activeWorker.department }}</p>
                <div class="flex gap-2">
                  <span :class="`px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wider ${availabilityBadge(activeWorker.status)}`">{{ activeWorker.status }}</span>
                  <span class="px-2.5 py-1 bg-slate-200 text-slate-700 rounded text-xs font-bold font-mono uppercase tracking-wider">{{ activeWorker.id }}</span>
                </div>
              </div>
            </div>
            <button @click="drawerOpen = false" class="p-2 text-slate-400 hover:bg-slate-200 rounded-lg transition-colors"><X class="w-6 h-6"/></button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Total Completed</p>
                <p class="text-xl font-bold text-slate-900">{{ activeWorker.totalCompleted }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Avg Rating</p>
                <p class="text-xl font-bold text-slate-900 flex items-center gap-1.5"><Star class="w-5 h-5 text-amber-400 fill-amber-400"/> {{ activeWorker.rating }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Avg Resol. Time</p>
                <p class="text-xl font-bold text-slate-900">{{ activeWorker.avgResTime }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs font-medium text-slate-500 mb-1">Perf. Score</p>
                <p class="text-xl font-bold text-[#22C55E]">{{ activeWorker.perfScore }}/100</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div>
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><User class="w-4 h-4 text-slate-400" /> Contact & Info</h3>
                <div class="space-y-4 text-sm">
                  <div class="flex items-center gap-3 text-slate-600"><Phone class="w-4 h-4 text-slate-400 shrink-0" /> {{ activeWorker.phone }}</div>
                  <div class="flex items-center gap-3 text-slate-600"><Mail class="w-4 h-4 text-slate-400 shrink-0" /> {{ activeWorker.email }}</div>
                  <div class="flex items-center gap-3 text-slate-600"><MapPin class="w-4 h-4 text-slate-400 shrink-0" /> {{ activeWorker.address || 'Not provided' }}</div>
                  <div class="flex items-center gap-3 text-slate-600"><Calendar class="w-4 h-4 text-slate-400 shrink-0" /> {{ activeWorker.experience }} Years Experience</div>
                </div>
              </div>
              <div>
                <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Briefcase class="w-4 h-4 text-slate-400" /> Skills & Expertise</h3>
                <div class="flex flex-wrap gap-2">
                  <span v-for="skill in activeWorker.skills" :key="skill" class="px-3 py-1.5 bg-blue-50 text-[#2563EB] text-xs font-bold rounded-lg border border-blue-100">
                    {{ skill }}
                  </span>
                  <span v-if="!activeWorker.skills?.length" class="text-sm text-slate-400">Not tracked yet.</span>
                </div>
              </div>
            </div>

            <div class="mb-8">
              <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Clipboard class="w-4 h-4 text-slate-400" /> Current Assignments</h3>
              <div class="overflow-x-auto border border-slate-100 rounded-xl">
                <table class="w-full text-left text-sm whitespace-nowrap">
                  <thead class="bg-slate-50 text-slate-500 font-medium text-xs uppercase tracking-wide">
                    <tr>
                      <th class="px-4 py-3">ID</th>
                      <th class="px-4 py-3">Category</th>
                      <th class="px-4 py-3">Priority</th>
                      <th class="px-4 py-3">Status</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100">
                    <tr v-for="task in activeWorker.currentAssignments" :key="task.id" class="hover:bg-slate-50">
                      <td class="px-4 py-3 font-mono font-medium text-slate-900">{{ task.id }}</td>
                      <td class="px-4 py-3 text-slate-600">{{ task.category }}</td>
                      <td class="px-4 py-3"><span :class="`text-[10px] font-bold px-2 py-0.5 rounded ${priorityBadge(task.priority)}`">{{ task.priority }}</span></td>
                      <td class="px-4 py-3"><span :class="`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${statusBadgeColor(task.status)}`">{{ task.status }}</span></td>
                    </tr>
                    <tr v-if="!activeWorker.currentAssignments?.length">
                      <td colspan="4" class="px-4 py-6 text-center text-slate-500 font-medium">No active assignments</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div>
              <h3 class="font-bold text-slate-900 mb-4 flex items-center gap-2"><Activity class="w-4 h-4 text-slate-400" /> Recent Activity</h3>
              <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                <div v-for="(act, idx) in activeWorker.timeline" :key="idx" class="relative">
                  <div class="absolute -left-[21px] w-2.5 h-2.5 bg-[#2563EB] rounded-full ring-4 ring-white"></div>
                  <p class="text-sm font-bold text-slate-900">{{ act.action }}</p>
                  <p class="text-[11px] text-slate-500 mt-0.5 font-medium">{{ act.date }} • {{ act.id }}</p>
                </div>
                <p v-if="!activeWorker.timeline?.length" class="text-sm text-slate-400">No recent activity recorded.</p>
              </div>
            </div>
          </div>
          
          <div class="p-6 border-t border-slate-100 bg-white grid grid-cols-2 gap-3 shrink-0">
            <button @click="openModal('edit', activeWorker)" class="py-3 border border-slate-200 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition-colors">Edit Details</button>
            <button @click="openModal('assign', activeWorker)" class="py-3 bg-[#2563EB] text-white font-bold rounded-lg hover:bg-[#1E40AF] transition-colors shadow-sm">Assign New Task</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Modals (Teleported) -->
    <Teleport to="body">
      
      <!-- Edit Worker Modal -->
      <div v-if="activeModal === 'edit'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-lg shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center shrink-0">
            <h3 class="font-bold text-lg text-slate-900">Edit Worker Profile</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 overflow-y-auto space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="col-span-2">
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Worker Name</label>
                <input v-model="modalForm.name" type="text" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Department</label>
                <select disabled title="Department changes go through the Department Applications approval flow." v-model="modalForm.department" class="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg text-sm text-slate-400 cursor-not-allowed">
                  <option>{{ modalForm.department }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Experience (Years)</label>
                <input disabled title="Not tracked yet." v-model="modalForm.experience" type="text" placeholder="Not tracked" class="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg text-sm text-slate-400 cursor-not-allowed" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Phone Number</label>
                <input v-model="modalForm.phone" type="text" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Availability</label>
                <select disabled title="Calculated automatically from active tasks and account status." v-model="modalForm.status" class="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg text-sm text-slate-400 cursor-not-allowed">
                  <option>{{ modalForm.status }}</option>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Assigned Area</label>
                <input disabled title="Not tracked yet." v-model="modalForm.area" type="text" placeholder="Not tracked" class="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg text-sm text-slate-400 cursor-not-allowed" />
              </div>
            </div>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3 shrink-0">
            <p v-if="editError" class="text-sm text-red-600 mr-auto self-center">{{ editError }}</p>
            <button @click="closeModal" class="px-5 py-2.5 text-sm font-bold text-slate-600 hover:bg-slate-200 rounded-lg transition-colors">Cancel</button>
            <button @click="submitEdit" :disabled="editSaving" class="px-5 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg shadow-sm transition-colors disabled:opacity-60">{{ editSaving ? 'Saving…' : 'Save Changes' }}</button>
          </div>
        </div>
      </div>

      <!-- Assign Complaint Modal -->
      <div v-if="activeModal === 'assign'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-md shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Direct Assignment</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-6 space-y-4">
            <div v-if="modalContextWorker" class="flex items-center gap-3 p-3 bg-blue-50 border border-blue-100 rounded-lg mb-4">
              <img :src="avatarUrl(modalContextWorker.name)" class="w-10 h-10 rounded-full object-cover" />
              <div>
                <p class="font-bold text-slate-900 text-sm leading-tight">Assigning to: {{ modalContextWorker.name }}</p>
                <p class="text-xs text-slate-600">{{ modalContextWorker.department }}</p>
              </div>
            </div>
            <div v-else>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Worker</label>
              <select v-model="assignForm.workerId" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]">
                <option value="" disabled>Select a worker in your department…</option>
                <option v-for="w in ownDepartmentWorkers" :key="w.rawId" :value="w.rawId">{{ w.name }} ({{ w.status }})</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Complaint ID</label>
              <div class="relative">
                <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input v-model="assignForm.complaintQuery" type="text" placeholder="e.g. CMP-00042 or 42" class="w-full pl-9 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
              </div>
              <p v-if="assignForm.matchedComplaint" class="text-xs text-green-700 mt-1.5">Found: {{ assignForm.matchedComplaint.title }} ({{ assignForm.matchedComplaint.status }})</p>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Deadline</label>
              <input v-model="assignForm.deadline" type="date" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Assignment Notes</label>
              <textarea v-model="assignForm.notes" rows="3" placeholder="Add optional instructions..." class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]"></textarea>
            </div>
            <p v-if="assignError" class="text-sm text-red-600">{{ assignError }}</p>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="closeModal" class="px-5 py-2.5 text-sm font-bold text-slate-600 hover:bg-slate-200 rounded-lg transition-colors">Cancel</button>
            <button @click="submitAssignment" :disabled="assignSubmitting" class="px-5 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg shadow-sm transition-colors disabled:opacity-60">{{ assignSubmitting ? 'Assigning…' : 'Assign Task' }}</button>
          </div>
        </div>
      </div>

      <!-- Deactivate Worker Modal -->
      <div v-if="activeModal === 'deactivate'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-red-50 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertTriangle class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">Deactivate Worker?</h3>
            <p class="text-sm text-slate-600 mb-6">Are you sure you want to deactivate <strong class="text-slate-900">{{ modalContextWorker?.name }}</strong>? They will not be able to receive new assignments.</p>
            
            <div class="text-left mb-6">
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1.5">Reason for Deactivation</label>
              <select v-model="statusReason" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:ring-red-500 focus:border-red-500">
                <option value="">Select a reason...</option>
                <option>Vacation / On Leave</option>
                <option>Inactive</option>
                <option>Transferred</option>
                <option>Other</option>
              </select>
            </div>
            <p v-if="statusError" class="text-sm text-red-600 text-left">{{ statusError }}</p>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex gap-3">
            <button @click="closeModal" class="flex-1 py-2.5 text-sm font-bold text-slate-700 bg-white border border-slate-300 hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
            <button @click="submitStatusChange('suspended')" :disabled="statusSubmitting" class="flex-1 py-2.5 text-sm font-bold text-white bg-red-600 hover:bg-red-700 rounded-lg shadow-sm transition-colors disabled:opacity-60">{{ statusSubmitting ? 'Saving…' : 'Deactivate' }}</button>
          </div>
        </div>
      </div>

      <!-- Reactivate Worker Modal -->
      <div v-if="activeModal === 'reactivate'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <UserCheck class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">Reactivate Worker?</h3>
            <p class="text-sm text-slate-600 mb-6"><strong class="text-slate-900">{{ modalContextWorker?.name }}</strong> will be able to receive new assignments again.</p>
            <p v-if="statusError" class="text-sm text-red-600 text-left">{{ statusError }}</p>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex gap-3">
            <button @click="closeModal" class="flex-1 py-2.5 text-sm font-bold text-slate-700 bg-white border border-slate-300 hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
            <button @click="submitStatusChange('active')" :disabled="statusSubmitting" class="flex-1 py-2.5 text-sm font-bold text-white bg-green-600 hover:bg-green-700 rounded-lg shadow-sm transition-colors disabled:opacity-60">{{ statusSubmitting ? 'Saving…' : 'Reactivate' }}</button>
          </div>
        </div>
      </div>

    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import { 
  Users, UserCheck, UserX, BadgeCheck, Briefcase, Clipboard, 
  Phone, Mail, MapPin, Calendar, Clock, BarChart, PieChart, 
  Star, Edit, Search, Download, UserPlus, Eye, AlertTriangle, X, Activity
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api'
const authHeaders = () => ({ Authorization: `Bearer ${localStorage.getItem('token')}` })

const loading = ref(true)
const loadError = ref('')

const drawerOpen = ref(false)
const drawerLoading = ref(false)
const activeModal = ref(null)
const activeWorker = ref({})
const modalContextWorker = ref(null)
const modalForm = reactive({})

const filters = reactive({
  search: '',
  department: 'All',
  availability: 'All',
  experience: 'All',
  sort: 'Name'
})

// --- Real data (loaded from the API) ---
const workers = ref([])
const performanceData = ref([])
const completionSummary = ref({ completed: 0, pending: 0 })
const ownDepartmentId = ref(null)
const ownDepartmentName = ref(null)

const statistics = ref([
  { title: 'Total Workers', value: 0, icon: Users, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
  { title: 'Available', value: 0, icon: UserCheck, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'Busy', value: 0, icon: Briefcase, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Offline/Leave', value: 0, icon: UserX, iconBg: 'bg-slate-100', iconColor: 'text-slate-500' },
  { title: 'Completed Today', value: 0, icon: BadgeCheck, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
  { title: 'Pending Tasks', value: 0, icon: Clipboard, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
  { title: 'Avg Rating', value: '—', icon: Star, iconBg: 'bg-yellow-50', iconColor: 'text-yellow-500' },
  { title: 'Avg Resol. Time', value: '—', icon: Clock, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' }
])

const departmentOptions = computed(() => {
  const names = new Set(workers.value.map(w => w.department).filter(Boolean))
  return [...names].sort()
})

const ownDepartmentWorkers = computed(() =>
  workers.value.filter(w => w.isOwnDepartment && w.accountStatus === 'active')
)

const completionPercent = computed(() => {
  const total = completionSummary.value.completed + completionSummary.value.pending
  return total ? Math.round((completionSummary.value.completed / total) * 100) : 0
})

const avatarUrl = (name) =>
  `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'Worker')}&background=2563EB&color=fff&size=200`

// --- Load everything from GET /officer/workers ---
async function loadWorkers() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await axios.get(`${API_BASE}/officer/workers`, { headers: authHeaders() })
    workers.value = data.workers || []
    performanceData.value = data.topPerformers || []
    completionSummary.value = data.completionSummary || { completed: 0, pending: 0 }
    ownDepartmentId.value = data.ownDepartmentId ?? null
    ownDepartmentName.value = data.ownDepartmentName ?? null

    const s = data.statistics || {}
    statistics.value = [
      { title: 'Total Workers', value: s.totalWorkers ?? 0, icon: Users, iconBg: 'bg-blue-50', iconColor: 'text-[#2563EB]' },
      { title: 'Available', value: s.available ?? 0, icon: UserCheck, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
      { title: 'Busy', value: s.busy ?? 0, icon: Briefcase, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
      { title: 'Offline/Leave', value: s.offline ?? 0, icon: UserX, iconBg: 'bg-slate-100', iconColor: 'text-slate-500' },
      { title: 'Completed Today', value: s.completedToday ?? 0, icon: BadgeCheck, iconBg: 'bg-green-50', iconColor: 'text-[#22C55E]' },
      { title: 'Pending Tasks', value: s.pendingTasks ?? 0, icon: Clipboard, iconBg: 'bg-amber-50', iconColor: 'text-amber-500' },
      { title: 'Avg Rating', value: s.avgRating ?? '—', icon: Star, iconBg: 'bg-yellow-50', iconColor: 'text-yellow-500' },
      { title: 'Avg Resol. Time', value: s.avgResTimeHours != null ? `${s.avgResTimeHours}h` : '—', icon: Clock, iconBg: 'bg-purple-50', iconColor: 'text-purple-500' }
    ]
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load workers.'
  } finally {
    loading.value = false
  }
}

// --- Computed & Methods ---

const filteredWorkers = computed(() => {
  let result = workers.value.filter(w => {
    const q = filters.search.toLowerCase()
    const matchSearch = !filters.search ||
      w.name.toLowerCase().includes(q) ||
      w.id.toLowerCase().includes(q) ||
      (w.department || '').toLowerCase().includes(q)
    const matchDept = filters.department === 'All' || w.department === filters.department
    const matchAvail = filters.availability === 'All' || w.status === filters.availability
    // Experience isn't tracked yet, so this filter never excludes anyone.
    return matchSearch && matchDept && matchAvail
  })

  if (filters.sort === 'Name') result.sort((a, b) => a.name.localeCompare(b.name))
  if (filters.sort === 'Performance') result.sort((a, b) => (b.perfScore ?? -1) - (a.perfScore ?? -1))
  if (filters.sort === 'Tasks Completed') result.sort((a, b) => b.totalCompleted - a.totalCompleted)
  if (filters.sort === 'Availability') {
    const order = { 'Available': 1, 'Busy': 2, 'Offline': 3, 'On Leave': 4 }
    result.sort((a, b) => order[a.status] - order[b.status])
  }

  return result
})

const resetFilters = () => {
  filters.search = ''
  filters.department = 'All'
  filters.availability = 'All'
  filters.experience = 'All'
}

const availabilityBadge = (status) => {
  if (status === 'Available') return 'bg-green-100 text-green-700'
  if (status === 'Busy') return 'bg-amber-100 text-amber-700'
  if (status === 'Offline') return 'bg-slate-200 text-slate-700'
  return 'bg-red-100 text-red-700'
}

const workloadColor = (pending, total) => {
  if (total === 0) return 'bg-slate-200'
  const ratio = pending / total
  if (ratio > 0.7) return 'bg-red-500'
  if (ratio > 0.3) return 'bg-amber-400'
  return 'bg-green-500'
}

const priorityBadge = (priority) => {
  const map = { 'Emergency': 'bg-red-100 text-red-700', 'High': 'bg-orange-100 text-orange-700', 'Medium': 'bg-blue-100 text-blue-700', 'Low': 'bg-slate-100 text-slate-600' }
  return map[priority]
}

const statusBadgeColor = (status) => {
  const map = { 'Assigned': 'bg-purple-100 text-purple-700', 'In Progress': 'bg-amber-100 text-amber-700' }
  return map[status] || 'bg-slate-100 text-slate-700'
}

// --- Drawer (Profile) ---
async function openDrawer(worker) {
  drawerOpen.value = true
  drawerLoading.value = true
  activeWorker.value = worker
  try {
    const { data } = await axios.get(`${API_BASE}/officer/workers/${worker.rawId}`, { headers: authHeaders() })
    activeWorker.value = data.worker
  } catch (err) {
    // Keep the card-level data showing; drawer still usable, just less detail.
  } finally {
    drawerLoading.value = false
  }
}

// --- Edit modal ---
const editSaving = ref(false)
const editError = ref('')

const openModal = (type, worker = null) => {
  modalContextWorker.value = worker
  activeModal.value = type
  editError.value = ''
  assignError.value = ''
  statusError.value = ''
  statusReason.value = ''
  if (type === 'edit' && worker) {
    Object.assign(modalForm, {
      name: worker.name,
      department: worker.department,
      experience: worker.experience,
      phone: worker.phone,
      status: worker.status,
      area: worker.area
    })
  }
  if (type === 'assign') {
    assignForm.workerId = ''
    assignForm.complaintQuery = ''
    assignForm.matchedComplaint = null
    assignForm.deadline = ''
    assignForm.notes = ''
  }
}

const closeModal = () => {
  activeModal.value = null
  modalContextWorker.value = null
}

async function submitEdit() {
  if (!modalContextWorker.value) return
  editSaving.value = true
  editError.value = ''
  try {
    await axios.patch(`${API_BASE}/officer/workers/${modalContextWorker.value.rawId}`, {
      name: modalForm.name,
      phone: modalForm.phone,
    }, { headers: authHeaders() })
    closeModal()
    await loadWorkers()
  } catch (err) {
    editError.value = err.response?.data?.message || 'Failed to save changes.'
  } finally {
    editSaving.value = false
  }
}

// --- Assign modal ---
const assignForm = reactive({ workerId: '', complaintQuery: '', matchedComplaint: null, deadline: '', notes: '' })
const assignSubmitting = ref(false)
const assignError = ref('')

async function resolveComplaint() {
  const query = assignForm.complaintQuery.trim().replace(/^CMP-?0*/i, '')
  if (!query) return null
  try {
    const { data } = await axios.get(`${API_BASE}/officer/complaints/${query}`, { headers: authHeaders() })
    return data.complaint
  } catch (err) {
    return null
  }
}

async function submitAssignment() {
  assignError.value = ''
  const workerId = modalContextWorker.value?.rawId || assignForm.workerId
  if (!workerId) {
    assignError.value = 'Please select a worker.'
    return
  }
  if (!assignForm.complaintQuery.trim()) {
    assignError.value = 'Please enter a complaint ID.'
    return
  }
  assignSubmitting.value = true
  try {
    const complaint = await resolveComplaint()
    if (!complaint) {
      assignError.value = 'Could not find that complaint, or it is not one of your assigned complaints.'
      return
    }
    await axios.patch(`${API_BASE}/officer/complaints/${complaint.rawId || complaint.id}/assign-worker`, {
      worker_id: workerId,
      expectedCompletionDate: assignForm.deadline || undefined,
      notes: assignForm.notes || undefined,
    }, { headers: authHeaders() })
    closeModal()
    await loadWorkers()
  } catch (err) {
    assignError.value = err.response?.data?.message || 'Failed to assign this task.'
  } finally {
    assignSubmitting.value = false
  }
}

// --- Deactivate / Reactivate ---
const statusSubmitting = ref(false)
const statusError = ref('')
const statusReason = ref('')

async function submitStatusChange(targetStatus) {
  if (!modalContextWorker.value) return
  statusSubmitting.value = true
  statusError.value = ''
  try {
    await axios.patch(`${API_BASE}/officer/workers/${modalContextWorker.value.rawId}/status`, {
      status: targetStatus,
      reason: statusReason.value,
    }, { headers: authHeaders() })
    closeModal()
    await loadWorkers()
  } catch (err) {
    statusError.value = err.response?.data?.message || 'Failed to update this worker.'
  } finally {
    statusSubmitting.value = false
  }
}

onMounted(loadWorkers)
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

/* Custom Scrollbar */
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