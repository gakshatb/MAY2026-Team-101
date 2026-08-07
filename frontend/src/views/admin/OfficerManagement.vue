<template>
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">
      
      
      <!-- Scrollable Dashboard Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">
        
        <!-- Header & Breadcrumbs -->
        <header class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">Officer Management</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Officer Management</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Manage officer accounts, department assignments, approvals, and overall officer performance.
            </p>
          </div>
          <div class="bg-white px-5 py-2.5 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-3">
            <Calendar class="w-5 h-5 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Error banner -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center justify-between">
          <span>{{ errorMessage }}</span>
          <button @click="fetchOfficers" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="mb-8 text-center text-gray-400 py-10">Loading officers…</div>

        <template v-else>
        <!-- Top Statistics Grid -->
        <section class="mb-8 grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
          <div v-for="(stat, index) in topStats" :key="index" class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 flex flex-col group hover:border-gray-200 hover:shadow-md transition-all">
            <div class="flex items-center gap-3 mb-3">
              <div :class="`p-2.5 rounded-lg bg-opacity-10 ${stat.colorClass} bg-current group-hover:scale-110 transition-transform duration-300`">
                <component :is="stat.icon" class="w-5 h-5" :class="stat.textClass" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-0.5">{{ stat.value }}</h3>
            <span class="text-sm text-gray-500 font-medium">{{ stat.label }}</span>
          </div>
        </section>

        <!-- Quick Actions & Insights Split -->
        <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-8">
          <!-- Quick Actions -->
          <section class="xl:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
              <Zap class="w-5 h-5 text-[#F59E0B]" /> Quick Actions
            </h2>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
              <button @click="openModal('create')" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors group">
                <UserPlus class="w-6 h-6 mb-2 text-gray-400 group-hover:text-[#2563EB]" />
                <span class="text-xs font-semibold text-center leading-tight">Create<br>Officer</span>
              </button>
              <button @click="scrollTo('pending')" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#22C55E] hover:bg-green-50 text-gray-700 hover:text-[#22C55E] transition-colors group">
                <UserCheck class="w-6 h-6 mb-2 text-gray-400 group-hover:text-[#22C55E]" />
                <span class="text-xs font-semibold text-center leading-tight">Pending<br>Approvals</span>
              </button>
              <button class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#F59E0B] hover:bg-yellow-50 text-gray-700 hover:text-[#F59E0B] transition-colors group">
                <RefreshCw class="w-6 h-6 mb-2 text-gray-400 group-hover:text-[#F59E0B]" />
                <span class="text-xs font-semibold text-center leading-tight">Transfer<br>Officer</span>
              </button>
              <button class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#EF4444] hover:bg-red-50 text-gray-700 hover:text-[#EF4444] transition-colors group">
                <Key class="w-6 h-6 mb-2 text-gray-400 group-hover:text-[#EF4444]" />
                <span class="text-xs font-semibold text-center leading-tight">Reset<br>Account</span>
              </button>
              <button class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors group">
                <BarChart3 class="w-6 h-6 mb-2 text-gray-400 group-hover:text-[#2563EB]" />
                <span class="text-xs font-semibold text-center leading-tight">View<br>Analytics</span>
              </button>
              <button class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors group">
                <ClipboardList class="w-6 h-6 mb-2 text-gray-400 group-hover:text-[#2563EB]" />
                <span class="text-xs font-semibold text-center leading-tight">Generate<br>Report</span>
              </button>
            </div>
          </section>

          <!-- Quick Insights -->
          <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex flex-col">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Lightbulb class="w-5 h-5 text-[#2563EB]" /> Quick Insights
            </h2>
            <div class="flex-1 space-y-3">
              <div v-for="(insight, index) in quickInsights" :key="index" class="p-3 bg-gray-50 rounded-xl border border-gray-100 flex justify-between items-center">
                <div>
                  <p class="text-[11px] font-bold text-gray-500 uppercase tracking-wide">{{ insight.label }}</p>
                  <p class="font-semibold text-gray-900 text-sm mt-0.5">{{ insight.value }}</p>
                </div>
                <div class="w-8 h-8 rounded-full bg-blue-100 text-[#2563EB] flex items-center justify-center shrink-0">
                  <component :is="insight.icon" class="w-4 h-4" />
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Search & Filter Section -->
        <section class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col xl:flex-row gap-4 items-center justify-between">
          <div class="w-full xl:w-[30%] relative">
            <Search class="w-5 h-5 text-gray-400 absolute left-3 top-3" />
            <input 
              v-model="filters.search" 
              type="text" 
              placeholder="Search by name, ID, or email..." 
              class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
            />
          </div>
          <div class="w-full xl:w-[70%] flex flex-wrap xl:flex-nowrap gap-3 justify-end">
            <select v-model="filters.status" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none min-w-[130px]">
              <option value="All">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Pending">Pending</option>
              <option value="Suspended">Suspended</option>
            </select>
            <select v-model="filters.department" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none min-w-[160px]">
              <option value="All">All Departments</option>
              <option v-for="dept in departmentList" :key="dept" :value="dept">{{ dept }}</option>
            </select>
            <select v-model="filters.performance" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none min-w-[140px]">
              <option value="All">All Performance</option>
              <option value="Excellent">Excellent</option>
              <option value="Good">Good</option>
              <option value="Average">Average</option>
              <option value="Needs Improvement">Needs Improvement</option>
            </select>
            <select v-model="filters.sort" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none min-w-[140px]">
              <option value="Name">Sort: Name</option>
              <option value="Complaints">Sort: Complaints</option>
              <option value="Score">Sort: Score</option>
            </select>
            <button @click="resetFilters" class="px-4 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors shrink-0 flex items-center gap-2">
              <RefreshCw class="w-4 h-4" /> Reset
            </button>
          </div>
        </section>

        <!-- Officer Table (Desktop) -->
        <section class="hidden md:block bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden mb-8">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-[11px] uppercase tracking-wider font-bold">
                  <th class="p-4 whitespace-nowrap sticky left-0 bg-gray-50 z-10">Officer Details</th>
                  <th class="p-4 whitespace-nowrap">Employee ID</th>
                  <th class="p-4 whitespace-nowrap">Department</th>
                  <th class="p-4 text-center whitespace-nowrap">Complaints (P/R)</th>
                  <th class="p-4 text-center whitespace-nowrap">Score</th>
                  <th class="p-4 whitespace-nowrap">Status</th>
                  <th class="p-4 text-right whitespace-nowrap">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm">
                <tr v-for="officer in filteredOfficers" :key="officer.id" class="hover:bg-gray-50 transition-colors group">
                  <td class="p-4 sticky left-0 bg-white group-hover:bg-gray-50 z-10 transition-colors">
                    <div class="flex items-center gap-3">
                      <img :src="officer.avatar" :alt="officer.name" class="w-10 h-10 rounded-full object-cover border border-gray-200 shrink-0" />
                      <div>
                        <p class="font-bold text-gray-900 leading-tight">{{ officer.name }}</p>
                        <p class="text-xs text-gray-500 mt-0.5">{{ officer.email }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="p-4 font-medium text-gray-700">{{ officer.empId }}</td>
                  <td class="p-4">
                    <p class="font-semibold text-gray-900">{{ officer.department }}</p>
                    <p class="text-xs text-gray-500">{{ officer.designation }}</p>
                  </td>
                  <td class="p-4 text-center">
                    <span class="font-medium text-red-500">{{ officer.pending }}</span> / 
                    <span class="font-medium text-green-600">{{ officer.resolved }}</span>
                  </td>
                  <td class="p-4 text-center">
                    <div class="flex flex-col items-center">
                      <span :class="['font-bold', getScoreColor(officer.score)]">{{ officer.score }}%</span>
                      <div class="w-16 h-1.5 bg-gray-100 rounded-full mt-1 overflow-hidden">
                        <div :class="['h-full rounded-full', getScoreBg(officer.score)]" :style="`width: ${officer.score}%`"></div>
                      </div>
                    </div>
                  </td>
                  <td class="p-4">
                    <span :class="['px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 w-max', getStatusBadge(officer.status)]">
                      <span class="w-1.5 h-1.5 rounded-full bg-current"></span> {{ officer.status }}
                    </span>
                  </td>
                  <td class="p-4 text-right">
                    <div class="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click="openDrawer(officer)" class="p-2 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors" title="View Profile"><Eye class="w-4 h-4" /></button>
                      <button @click="openModal('edit', officer)" class="p-2 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors" title="Edit"><Pencil class="w-4 h-4" /></button>
                      <button @click="openModal('transfer', officer)" class="p-2 text-gray-400 hover:text-[#F59E0B] hover:bg-yellow-50 rounded-lg transition-colors" title="Transfer"><RefreshCw class="w-4 h-4" /></button>
                      <button @click="openModal('suspend', officer)" class="p-2 text-gray-400 hover:text-[#EF4444] hover:bg-red-50 rounded-lg transition-colors" title="Suspend"><UserMinus class="w-4 h-4" /></button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredOfficers.length === 0">
                  <td colspan="7" class="p-12 text-center text-gray-500">
                    <Users class="w-10 h-10 text-gray-300 mx-auto mb-3" />
                    <p class="text-base font-medium text-gray-900">No officers found</p>
                    <p class="text-sm">Try adjusting your filters or search query.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Pagination Placeholder -->
          <div class="p-4 border-t border-gray-100 flex items-center justify-between text-sm text-gray-500 bg-gray-50/50">
            <span>Showing 1 to {{ filteredOfficers.length }} of {{ officers.length }} entries</span>
            <div class="flex gap-1">
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50 disabled:opacity-50">Prev</button>
              <button class="px-3 py-1 border border-gray-200 bg-[#2563EB] text-white rounded-md">1</button>
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50 disabled:opacity-50">Next</button>
            </div>
          </div>
        </section>

        <!-- Officer Cards (Mobile) -->
        <section class="md:hidden space-y-4 mb-8">
          <div v-for="officer in filteredOfficers" :key="officer.id" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50">
            <div class="flex justify-between items-start mb-3">
              <div class="flex items-center gap-3">
                <img :src="officer.avatar" :alt="officer.name" class="w-12 h-12 rounded-full border border-gray-100 object-cover" />
                <div>
                  <h3 class="font-bold text-gray-900">{{ officer.name }}</h3>
                  <p class="text-xs text-gray-500">{{ officer.empId }} • {{ officer.department }}</p>
                </div>
              </div>
              <span :class="['px-2 py-0.5 rounded-full text-[10px] font-semibold flex items-center gap-1', getStatusBadge(officer.status)]">
                {{ officer.status }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm mb-4">
              <div class="bg-gray-50 p-2 rounded-lg">
                <p class="text-xs text-gray-500 mb-0.5">Complaints</p>
                <p class="font-medium text-gray-900"><span class="text-red-500">{{ officer.pending }}</span> P / <span class="text-green-600">{{ officer.resolved }}</span> R</p>
              </div>
              <div class="bg-gray-50 p-2 rounded-lg">
                <p class="text-xs text-gray-500 mb-0.5">Score</p>
                <p :class="['font-bold', getScoreColor(officer.score)]">{{ officer.score }}%</p>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-2">
              <button @click="openDrawer(officer)" class="w-full py-2 bg-blue-50 text-[#2563EB] rounded-lg text-sm font-medium hover:bg-blue-100 transition-colors">View Profile</button>
              <button @click="openModal('edit', officer)" class="w-full py-2 bg-gray-50 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-100 transition-colors border border-gray-200">Manage</button>
            </div>
          </div>
        </section>

        <!-- Charts Section -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4">Complaints Managed (Top 5 Officers)</h2>
            <div class="relative h-64 w-full">
              <canvas ref="barChartRef"></canvas>
            </div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4">Department Distribution</h2>
            <div class="relative h-64 w-full flex justify-center">
              <canvas ref="pieChartRef"></canvas>
            </div>
          </div>
        </section>

        <!-- Pending Registrations & Timeline Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          
          <!-- Pending Registrations -->
          <section id="pending" class="bg-white rounded-[14px] shadow-sm border border-gray-50 flex flex-col h-[450px]">
            <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50 rounded-t-[14px]">
              <h2 class="text-lg font-bold text-gray-900 flex items-center gap-2">
                <UserPlus class="w-5 h-5 text-[#F59E0B]" /> Pending Approvals
              </h2>
              <span class="px-2.5 py-0.5 bg-yellow-100 text-yellow-700 text-xs font-bold rounded-full">{{ pendingRegistrations.length }}</span>
            </div>
            <div class="p-4 flex-1 overflow-y-auto custom-scrollbar space-y-3">
              <div v-for="app in pendingRegistrations" :key="app.id" class="p-4 border border-gray-100 rounded-xl hover:border-gray-200 transition-colors bg-white">
                <div class="flex items-start gap-3 mb-3">
                  <div class="w-10 h-10 rounded-full bg-blue-50 text-[#2563EB] flex items-center justify-center font-bold">{{ app.name.charAt(0) }}</div>
                  <div class="flex-1">
                    <h4 class="font-bold text-gray-900 text-sm">{{ app.name }}</h4>
                    <p class="text-xs text-gray-500">{{ app.requestedDept || 'Unassigned' }}</p>
                  </div>
                  <span class="text-[10px] text-gray-400">{{ app.date }}</span>
                </div>
                <div class="flex gap-2">
                  <button @click="approveRegistration(app)" class="flex-1 py-1.5 bg-[#22C55E] hover:bg-green-600 text-white rounded-lg text-xs font-medium transition-colors shadow-sm">Approve</button>
                  <button @click="rejectRegistration(app)" class="flex-1 py-1.5 bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 rounded-lg text-xs font-medium transition-colors">Reject</button>
                </div>
              </div>
              <div v-if="pendingRegistrations.length === 0" class="h-full flex flex-col items-center justify-center text-gray-500">
                <CheckCircle class="w-8 h-8 text-green-500 mb-2 opacity-50"/>
                <p class="text-sm">No pending registrations.</p>
              </div>
            </div>
          </section>

          <!-- Recent Activities -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 flex flex-col h-[450px]">
            <div class="p-6 border-b border-gray-100 bg-gray-50/50 rounded-t-[14px]">
              <h2 class="text-lg font-bold text-gray-900 flex items-center gap-2">
                <Activity class="w-5 h-5 text-[#2563EB]" /> Recent Activities
              </h2>
            </div>
            <div class="p-6 flex-1 overflow-y-auto custom-scrollbar">
              <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
                <div v-for="activity in recentActivities" :key="activity.id" class="relative pl-6">
                  <span :class="['absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2', activity.color]"></span>
                  <div class="flex justify-between items-baseline mb-0.5">
                    <h4 class="text-sm font-semibold text-gray-900">{{ activity.action }}</h4>
                    <span class="text-[10px] text-gray-400 shrink-0 ml-2">{{ activity.time }}</span>
                  </div>
                  <p class="text-sm text-gray-500">{{ activity.desc }}</p>
                  <p class="text-[11px] font-medium text-[#2563EB] mt-1">Admin: {{ activity.admin }}</p>
                </div>
              </div>
            </div>
          </section>

        </div>
        </template>
      </main>
    </div>

    <!-- Officer Details Drawer -->
    <div v-if="isDrawerOpen && selectedOfficer" class="fixed inset-0 z-50 overflow-hidden" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
      <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity" @click="closeDrawer"></div>
      <div class="fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-2xl flex flex-col transform transition-transform duration-300 ease-in-out border-l border-gray-100">
        
        <!-- Drawer Header -->
        <div class="p-6 border-b border-gray-100 flex justify-between items-start bg-gray-50/50 relative overflow-hidden">
          <div class="absolute top-0 right-0 p-4 opacity-5">
            <Building2 class="w-32 h-32" />
          </div>
          <div class="relative z-10 flex items-center gap-4">
            <img :src="selectedOfficer.avatar" class="w-16 h-16 rounded-full border-2 border-white shadow-sm object-cover" />
            <div>
              <h2 class="text-xl font-bold text-gray-900 leading-tight">{{ selectedOfficer.name }}</h2>
              <p class="text-sm font-medium text-[#2563EB]">{{ selectedOfficer.designation }}</p>
              <span :class="['mt-1.5 inline-flex px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide', getStatusBadge(selectedOfficer.status)]">
                {{ selectedOfficer.status }}
              </span>
            </div>
          </div>
          <button @click="closeDrawer" class="relative z-10 p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-full transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Drawer Content -->
        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-6">
          
          <!-- Identity -->
          <div>
            <h3 class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-3">Identity & Contact</h3>
            <div class="bg-gray-50 rounded-xl p-4 border border-gray-100 space-y-3 text-sm">
              <div class="flex items-center gap-3"><BadgeCheck class="w-4 h-4 text-gray-400"/><span class="text-gray-600 w-20">Emp ID:</span> <span class="font-semibold text-gray-900">{{ selectedOfficer.empId }}</span></div>
              <div class="flex items-center gap-3"><Building2 class="w-4 h-4 text-gray-400"/><span class="text-gray-600 w-20">Dept:</span> <span class="font-semibold text-gray-900">{{ selectedOfficer.department }}</span></div>
              <div class="flex items-center gap-3"><Mail class="w-4 h-4 text-gray-400"/><span class="text-gray-600 w-20">Email:</span> <a href="#" class="font-medium text-[#2563EB] hover:underline">{{ selectedOfficer.email }}</a></div>
              <div class="flex items-center gap-3"><Phone class="w-4 h-4 text-gray-400"/><span class="text-gray-600 w-20">Phone:</span> <span class="font-medium text-gray-900">{{ selectedOfficer.phone }}</span></div>
              <div class="flex items-center gap-3"><Calendar class="w-4 h-4 text-gray-400"/><span class="text-gray-600 w-20">Joined:</span> <span class="font-medium text-gray-900">{{ selectedOfficer.joined }} ({{ selectedOfficer.experience }})</span></div>
            </div>
          </div>

          <!-- Performance -->
          <div>
            <h3 class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-3">Performance Overview</h3>
            <div class="grid grid-cols-2 gap-3 mb-4">
              <div class="p-3 bg-white border border-gray-100 rounded-xl text-center shadow-sm">
                <p class="text-[11px] text-gray-500 uppercase font-bold mb-1">Total Assigned</p>
                <p class="text-xl font-bold text-gray-900">{{ selectedOfficer.resolved + selectedOfficer.pending }}</p>
              </div>
              <div class="p-3 bg-white border border-gray-100 rounded-xl text-center shadow-sm">
                <p class="text-[11px] text-gray-500 uppercase font-bold mb-1">Avg Res. Time</p>
                <p class="text-xl font-bold text-gray-900">{{ selectedOfficer.avgTime }}</p>
              </div>
              <div class="p-3 bg-white border border-gray-100 rounded-xl text-center shadow-sm">
                <p class="text-[11px] text-green-600 uppercase font-bold mb-1">Resolved</p>
                <p class="text-xl font-bold text-green-600">{{ selectedOfficer.resolved }}</p>
              </div>
              <div class="p-3 bg-white border border-gray-100 rounded-xl text-center shadow-sm">
                <p class="text-[11px] text-red-500 uppercase font-bold mb-1">Pending</p>
                <p class="text-xl font-bold text-red-500">{{ selectedOfficer.pending }}</p>
              </div>
            </div>

            <!-- Score Bar -->
            <div class="bg-gray-50 rounded-xl p-4 border border-gray-100">
              <div class="flex justify-between items-end mb-2">
                <span class="text-sm font-semibold text-gray-700">Overall Score</span>
                <span :class="['text-lg font-bold', getScoreColor(selectedOfficer.score)]">{{ selectedOfficer.score }}%</span>
              </div>
              <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                <div :class="['h-full rounded-full', getScoreBg(selectedOfficer.score)]" :style="`width: ${selectedOfficer.score}%`"></div>
              </div>
              <p class="text-xs text-gray-500 mt-2 flex items-center gap-1"><Award class="w-3 h-3 text-yellow-500"/> Citizen Rating: {{ selectedOfficer.citizenRating }}/5.0</p>
            </div>
          </div>
        </div>

        <!-- Drawer Actions -->
        <div class="p-4 border-t border-gray-100 bg-white grid grid-cols-2 gap-3">
          <button @click="router.push(`/admin/officerdetails/${selectedOfficer.id}`)" class="col-span-2 py-2.5 bg-blue-50 text-[#2563EB] font-semibold text-sm rounded-xl hover:bg-blue-100 transition-colors border border-blue-100">
            View Full Details
          </button>
          <button @click="openModal('edit', selectedOfficer)" class="py-2.5 bg-gray-50 border border-gray-200 text-gray-700 font-semibold text-sm rounded-xl hover:bg-gray-100 transition-colors">
            Edit Profile
          </button>
          <button @click="openModal('transfer', selectedOfficer)" class="py-2.5 bg-[#2563EB] text-white font-semibold text-sm rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm">
            Transfer Dept
          </button>
          <button @click="openModal('reset', selectedOfficer)" class="py-2.5 bg-white border border-gray-200 text-gray-700 font-semibold text-sm rounded-xl hover:bg-gray-50 transition-colors">
            Reset Auth
          </button>
          <button v-if="selectedOfficer.status === 'Active'" @click="openModal('suspend', selectedOfficer)" class="py-2.5 bg-red-50 text-red-600 font-semibold text-sm rounded-xl hover:bg-red-100 transition-colors border border-red-100">
            Suspend
          </button>
          <button v-else @click="submitReactivate(selectedOfficer)" :disabled="isSubmitting" class="py-2.5 bg-green-50 text-green-600 font-semibold text-sm rounded-xl hover:bg-green-100 transition-colors border border-green-100 disabled:opacity-60">
            Reactivate
          </button>
        </div>
      </div>
    </div>

    <!-- Modals Container -->
    <div v-if="activeModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
      
      <!-- 1. Create / Edit Officer Modal -->
      <div v-if="activeModal === 'create' || activeModal === 'edit'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-2xl p-6 lg:p-8 transform transition-all max-h-[90vh] overflow-y-auto custom-scrollbar">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ activeModal === 'create' ? 'Create Officer Account' : 'Edit Officer Profile' }}</h2>
            <p class="text-sm text-gray-500 mt-1">Fill in the official details to manage system access.</p>
          </div>
          <button @click="closeModal" class="p-2 bg-gray-50 text-gray-500 rounded-full hover:bg-gray-100 transition-colors"><X class="w-5 h-5"/></button>
        </div>
        
        <form @submit.prevent="handleActionClose" class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Full Name</label>
              <input type="text" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none" placeholder="e.g. Ramesh Kumar" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Employee ID</label>
              <input type="text" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none bg-gray-50" placeholder="e.g. OFC-1045" :disabled="activeModal === 'edit'" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Email Address</label>
              <input type="email" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none" placeholder="name@civicdesk.gov" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Phone Number</label>
              <input type="text" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none" placeholder="+91 98765 43210" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Department Assignment</label>
              <select class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none">
                <option v-for="dept in departmentList" :key="dept">{{ dept }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Designation</label>
              <select class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none">
                <option>Senior Civic Officer</option>
                <option>Field Officer</option>
                <option>Department Head</option>
                <option>Inspector</option>
              </select>
            </div>
            <div v-if="activeModal === 'create'" class="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-5 pt-2 border-t border-gray-100">
               <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Temporary Password</label>
                <input type="password" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none" placeholder="••••••••" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Confirm Password</label>
                <input type="password" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none" placeholder="••••••••" />
              </div>
            </div>
            <div v-if="activeModal === 'edit'">
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Account Status</label>
              <select class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none">
                <option>Active</option>
                <option>Suspended</option>
              </select>
            </div>
          </div>
          
          <div class="pt-6 flex justify-end gap-3 mt-4">
            <button type="button" @click="closeModal" class="px-6 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
            <button type="submit" class="px-6 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl transition-colors shadow-sm">
              {{ activeModal === 'create' ? 'Create Account' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 2. Transfer Officer Modal -->
      <div v-if="activeModal === 'transfer'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-md p-6 transform transition-all">
        <h2 class="text-xl font-bold text-gray-900 mb-1">Transfer Department</h2>
        <p class="text-sm text-gray-500 mb-5">Reassign <strong class="text-gray-800">{{ targetOfficer?.name || 'Officer' }}</strong> to a new department.</p>
        
        <form @submit.prevent="submitTransfer" class="space-y-4">
          <div class="p-3 bg-gray-50 border border-gray-200 rounded-xl text-sm mb-4">
            <span class="text-gray-500 block text-xs uppercase font-bold mb-0.5">Current Department</span>
            <span class="font-semibold text-gray-900">{{ targetOfficer?.department || 'Select from table first' }}</span>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">New Department</label>
            <select v-model="transferForm.departmentId" required class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none">
              <option value="" disabled>Select a department</option>
              <option v-for="dept in departmentOptions" :key="dept.id" :value="dept.id">{{ dept.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Effective Date</label>
            <input type="date" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Reason for Transfer</label>
            <textarea rows="2" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none resize-none"></textarea>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
            <button type="button" @click="closeModal" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl transition-colors">Cancel</button>
            <button type="submit" class="px-5 py-2.5 text-sm font-bold text-white bg-[#F59E0B] hover:bg-yellow-600 rounded-xl transition-colors shadow-sm">Process Transfer</button>
          </div>
        </form>
      </div>

      <!-- 3. Suspend Officer Modal -->
      <div v-if="activeModal === 'suspend'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-md p-6 transform transition-all">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-full bg-red-100 text-red-600 flex items-center justify-center shrink-0"><AlertTriangle class="w-5 h-5"/></div>
          <h2 class="text-xl font-bold text-gray-900">Suspend Account</h2>
        </div>
        <div class="p-3 bg-red-50 border border-red-100 rounded-xl mb-4">
          <p class="text-sm text-red-700 font-medium">Warning: Suspending <strong class="text-red-900">{{targetOfficer?.name}}</strong> will immediately revoke their platform access.</p>
        </div>
        <form @submit.prevent="submitSuspend" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Reason for Suspension</label>
            <select v-model="suspendForm.reason" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-red-500/20 outline-none">
              <option>Policy Violation</option>
              <option>Poor Performance Review</option>
              <option>Administrative Leave</option>
              <option>Other</option>
            </select>
          </div>
          <div class="pt-4 flex justify-end gap-3">
            <button type="button" @click="closeModal" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl">Cancel</button>
            <button type="submit" :disabled="isSubmitting" class="px-5 py-2.5 text-sm font-bold text-white bg-[#EF4444] hover:bg-red-700 rounded-xl shadow-sm disabled:opacity-60">Confirm Suspension</button>
          </div>
        </form>
      </div>

      <!-- 4. Reset Account / Delete Modals (Simplified) -->
      <div v-if="activeModal === 'reset'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center transform transition-all">
        <div class="w-16 h-16 bg-blue-100 text-[#2563EB] rounded-full flex items-center justify-center mx-auto mb-4">
          <Key class="w-8 h-8" />
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-1">Reset Account Credentials</h2>
        <p class="text-sm text-gray-500 mb-6">
          Send a password reset link to <strong class="text-gray-800">{{ targetOfficer?.email }}</strong>.
        </p>
        <div class="flex flex-col gap-3">
          <button @click="handleActionClose" class="w-full py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl shadow-sm">Send Reset Link</button>
          <button @click="closeModal" class="w-full py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl">Cancel</button>
        </div>
      </div>
      
    </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Chart from 'chart.js/auto';

// Icons
import { 
  UserCog, Users, UserPlus, UserCheck, UserMinus, Building2, 
  ClipboardList, BarChart3, TrendingUp, Award, ShieldCheck, 
  Search, Eye, Pencil, RefreshCw, Trash2, Clock, Calendar, 
  Mail, Phone, BadgeCheck, Activity, AlertTriangle, Key, X, Lightbulb, CheckCircle, Zap
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const router = useRouter();
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

// View State
const sidebarOpen = ref(false);
const isDrawerOpen = ref(false);
const activeModal = ref(null);
const selectedOfficer = ref(null);
const targetOfficer = ref(null);
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
const isLoading = ref(true);
const errorMessage = ref('');
const isSubmitting = ref(false);

// --- Live data — populated from the backend ---
const STAT_META = {
  total_officers:    { label: 'Total Officers',    icon: Users,      colorClass: 'text-[#2563EB] bg-blue-100',   textClass: 'text-[#2563EB]' },
  active_officers:   { label: 'Active Officers',   icon: UserCheck,  colorClass: 'text-[#22C55E] bg-green-100',  textClass: 'text-[#22C55E]' },
  pending_approvals: { label: 'Pending Approvals', icon: Clock,      colorClass: 'text-[#F59E0B] bg-yellow-100', textClass: 'text-[#F59E0B]' },
  suspended:         { label: 'Suspended',         icon: UserMinus,  colorClass: 'text-[#EF4444] bg-red-100',    textClass: 'text-[#EF4444]' },
  departments:       { label: 'Departments',       icon: Building2,  colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  avg_rating:        { label: 'Avg Rating',        icon: Award,      colorClass: 'text-indigo-600 bg-indigo-100', textClass: 'text-indigo-600' },
};
const STAT_ORDER = ['total_officers', 'active_officers', 'pending_approvals', 'suspended', 'departments', 'avg_rating'];
const INSIGHT_ICONS = { 'Top Performer': Award, 'Most Active Dept': TrendingUp, 'Highest Workload': Activity };
const ACTIVITY_COLORS = {
  officer_approved: 'border-green-500', officer_rejected: 'border-red-500',
  officer_suspended: 'border-red-500', officer_reactivated: 'border-green-500',
  officer_transferred: 'border-yellow-500', officer_updated: 'border-blue-500',
};

const topStats = ref([]);
const quickInsights = ref([]);
const officers = ref([]);
const pendingRegistrations = ref([]);
const recentActivities = ref([]);
const departmentList = ref([]);        // department names, for filters/legacy selects
const departmentOptions = ref([]);     // [{id, name}], needed for the transfer modal

const timeAgo = (iso) => {
  if (!iso) return '';
  const diffMs = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins} min ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs} hr${hrs !== 1 ? 's' : ''} ago`;
  const days = Math.floor(hrs / 24);
  if (days < 7) return days === 1 ? 'Yesterday' : `${days} days ago`;
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const fetchOfficers = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/officers`, authHeaders());

    topStats.value = STAT_ORDER
      .filter(key => key in data.top_stats)
      .map(key => ({
        ...STAT_META[key],
        value: key === 'avg_rating'
          ? (data.top_stats[key] != null ? `${data.top_stats[key]}/5` : 'N/A')
          : data.top_stats[key],
      }));

    quickInsights.value = data.quick_insights.map(i => ({ ...i, icon: INSIGHT_ICONS[i.label] || Lightbulb }));
    officers.value = data.officers;
    pendingRegistrations.value = data.pending_registrations;
    recentActivities.value = data.recent_activities.map(a => ({
      id: a.id,
      action: a.action,
      desc: a.description,
      time: timeAgo(a.created_at),
      admin: a.admin,
      color: 'border-blue-500',
    }));
    departmentList.value = data.departments;
    renderCharts();
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    errorMessage.value = err.response?.data?.message || 'Failed to load officers.';
  } finally {
    isLoading.value = false;
  }
};

const fetchDepartmentOptions = async () => {
  try {
    const { data } = await axios.get(`${API_BASE}/departments`, authHeaders());
    departmentOptions.value = data.departments.map(d => ({ id: d.id, name: d.name }));
  } catch (err) {
    // Non-fatal — the transfer modal just won't have options if this fails.
  }
};

onMounted(() => {
  fetchOfficers();
  fetchDepartmentOptions();
});

// --- Filters & Sorting ---
const filters = reactive({
  search: '',
  status: 'All',
  department: 'All',
  performance: 'All',
  sort: 'Name'
});

const filteredOfficers = computed(() => {
  let result = officers.value;

  if (filters.search) {
    const q = filters.search.toLowerCase();
    result = result.filter(o => o.name.toLowerCase().includes(q) || o.empId.toLowerCase().includes(q) || o.email.toLowerCase().includes(q));
  }
  if (filters.status !== 'All') result = result.filter(o => o.status === filters.status);
  if (filters.department !== 'All') result = result.filter(o => o.department === filters.department);
  if (filters.performance !== 'All') {
    result = result.filter(o => {
      if(filters.performance === 'Excellent') return o.score >= 90;
      if(filters.performance === 'Good') return o.score >= 80 && o.score < 90;
      if(filters.performance === 'Average') return o.score >= 60 && o.score < 80;
      return o.score < 60;
    });
  }

  result.sort((a, b) => {
    if (filters.sort === 'Name') return a.name.localeCompare(b.name);
    if (filters.sort === 'Complaints') return (b.resolved + b.pending) - (a.resolved + a.pending);
    if (filters.sort === 'Score') return b.score - a.score;
    return 0;
  });

  return result;
});

const resetFilters = () => {
  filters.search = '';
  filters.status = 'All';
  filters.department = 'All';
  filters.performance = 'All';
  filters.sort = 'Name';
};

// --- UI Logic ---
const getStatusBadge = (status) => {
  switch(status) {
    case 'Active': return 'bg-green-50 text-green-700 border border-green-200';
    case 'Suspended': return 'bg-red-50 text-red-700 border border-red-200';
    case 'Pending': return 'bg-yellow-50 text-yellow-700 border border-yellow-200';
    default: return 'bg-gray-100 text-gray-600 border border-gray-200';
  }
};
const getScoreColor = (score) => {
  if(score >= 90) return 'text-green-600';
  if(score >= 80) return 'text-blue-600';
  if(score >= 60) return 'text-yellow-600';
  return 'text-red-600';
};
const getScoreBg = (score) => {
  if(score >= 90) return 'bg-green-500';
  if(score >= 80) return 'bg-blue-500';
  if(score >= 60) return 'bg-yellow-500';
  return 'bg-red-500';
};

const scrollTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });

// Modal / Drawer interactions
const openDrawer = (officer) => { selectedOfficer.value = officer; isDrawerOpen.value = true; };
const closeDrawer = () => { isDrawerOpen.value = false; setTimeout(() => { selectedOfficer.value = null; }, 300); };
const openModal = (type, officer = null) => {
  activeModal.value = type;
  if (officer) targetOfficer.value = officer;
  if (type === 'suspend') suspendForm.reason = 'Policy Violation';
  if (type === 'transfer') transferForm.departmentId = '';
};
const closeModal = () => { activeModal.value = null; targetOfficer.value = null; };
const handleActionClose = () => { closeModal(); closeDrawer(); };

// --- Backend-wired actions ---
const suspendForm = reactive({ reason: 'Policy Violation' });
const transferForm = reactive({ departmentId: '' });

const approveRegistration = async (reg) => {
  try {
    await axios.patch(`${API_BASE}/users/${reg.id}/approve`, {}, authHeaders());
    await fetchOfficers();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to approve registration.';
  }
};

const rejectRegistration = async (reg) => {
  try {
    await axios.patch(`${API_BASE}/users/${reg.id}/reject`, {}, authHeaders());
    await fetchOfficers();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to reject registration.';
  }
};

const submitSuspend = async () => {
  if (!targetOfficer.value) return;
  isSubmitting.value = true;
  try {
    await axios.patch(
      `${API_BASE}/officers/${targetOfficer.value.id}/suspend`,
      { reason: suspendForm.reason },
      authHeaders()
    );
    handleActionClose();
    await fetchOfficers();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to suspend officer.';
  } finally {
    isSubmitting.value = false;
  }
};

const submitReactivate = async (officer) => {
  if (!officer) return;
  isSubmitting.value = true;
  try {
    await axios.patch(`${API_BASE}/officers/${officer.id}/reactivate`, {}, authHeaders());
    handleActionClose();
    await fetchOfficers();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to reactivate officer.';
  } finally {
    isSubmitting.value = false;
  }
};

const submitTransfer = async () => {
  if (!targetOfficer.value || !transferForm.departmentId) return;
  isSubmitting.value = true;
  try {
    await axios.patch(
      `${API_BASE}/officers/${targetOfficer.value.id}/transfer`,
      { departmentId: transferForm.departmentId },
      authHeaders()
    );
    handleActionClose();
    await fetchOfficers();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to transfer officer.';
  } finally {
    isSubmitting.value = false;
  }
};

// --- Charts — driven by the officers list once it loads ---
const barChartRef = ref(null);
const pieChartRef = ref(null);
let barChart = null;
let pieChart = null;
const CHART_COLORS = ['#2563EB', '#1E40AF', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE'];

const renderCharts = () => {
  if (!barChartRef.value || !pieChartRef.value) return;

  const topFive = [...officers.value]
    .sort((a, b) => (b.resolved + b.pending) - (a.resolved + a.pending))
    .slice(0, 5);

  barChart?.destroy();
  barChart = new Chart(barChartRef.value, {
    type: 'bar',
    data: {
      labels: topFive.map(o => o.name.split(' ')[0]),
      datasets: [
        { label: 'Resolved', data: topFive.map(o => o.resolved), backgroundColor: '#22C55E', borderRadius: 4 },
        { label: 'Pending', data: topFive.map(o => o.pending), backgroundColor: '#EF4444', borderRadius: 4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: { x: { stacked: true, grid: { display: false } }, y: { stacked: true, grid: { color: '#F3F4F6' } } }
    }
  });

  const byDept = {};
  officers.value.forEach(o => { const d = o.department || 'Unassigned'; byDept[d] = (byDept[d] || 0) + 1; });
  const deptLabels = Object.keys(byDept);

  pieChart?.destroy();
  pieChart = new Chart(pieChartRef.value, {
    type: 'doughnut',
    data: {
      labels: deptLabels,
      datasets: [{
        data: deptLabels.map(l => byDept[l]),
        backgroundColor: deptLabels.map((_, i) => CHART_COLORS[i % CHART_COLORS.length]),
        borderWidth: 0, hoverOffset: 4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '70%',
      plugins: { legend: { position: 'right' } }
    }
  });
};
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