<template>
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">
      
      
      <!-- Scrollable Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">
        
        <!-- Header & Breadcrumbs -->
        <header class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">Activity Logs</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Activity Logs</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Monitor platform activities, user actions, and administrative events across CivicDesk.
            </p>
          </div>
          <div class="bg-white px-4 py-2 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-2 shrink-0">
            <Clock class="w-4 h-4 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Error banner -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center justify-between">
          <span>{{ errorMessage }}</span>
          <button @click="fetchLogs" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="text-center text-gray-400 py-10">Loading activity logs…</div>

        <template v-else>

        <!-- Top Statistics Grid -->
        <section class="mb-6 grid grid-cols-2 md:grid-cols-4 xl:grid-cols-8 gap-3">
          <div v-for="(stat, index) in topStats" :key="index" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50 flex flex-col group hover:shadow-md transition-all">
            <div class="flex justify-between items-start mb-2">
              <div :class="`p-2 rounded-lg bg-opacity-10 ${stat.colorClass} bg-current group-hover:scale-110 transition-transform`">
                <component :is="stat.icon" class="w-4 h-4" :class="stat.textClass" />
              </div>
            </div>
            <h3 class="text-xl font-bold text-gray-900 leading-tight mb-1">{{ stat.value }}</h3>
            <span class="text-[10px] text-gray-500 font-bold uppercase tracking-wider truncate">{{ stat.label }}</span>
          </div>
        </section>

        <!-- Quick Actions & Log Statistics -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div class="lg:col-span-2 bg-white p-5 rounded-[14px] shadow-sm border border-gray-50">
             <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Monitor class="w-4 h-4 text-[#F59E0B]" /> Quick Actions
             </h2>
             <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
               <button @click="openExportModal" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors group">
                 <Download class="w-5 h-5 mb-2 text-gray-400 group-hover:text-[#2563EB]" />
                 <span class="text-xs font-semibold text-center leading-tight">Export<br>Logs</span>
               </button>
               <button @click="exportCSV" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#22C55E] hover:bg-green-50 text-gray-700 hover:text-[#22C55E] transition-colors group">
                 <FileText class="w-5 h-5 mb-2 text-gray-400 group-hover:text-[#22C55E]" />
                 <span class="text-xs font-semibold text-center leading-tight">Download<br>CSV</span>
               </button>
               <button @click="openExportModal" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#EF4444] hover:bg-red-50 text-gray-700 hover:text-[#EF4444] transition-colors group">
                 <FileText class="w-5 h-5 mb-2 text-gray-400 group-hover:text-[#EF4444]" />
                 <span class="text-xs font-semibold text-center leading-tight">Download<br>PDF</span>
               </button>
               <button @click="scrollTo('filter')" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#F59E0B] hover:bg-yellow-50 text-gray-700 hover:text-[#F59E0B] transition-colors group">
                 <Filter class="w-5 h-5 mb-2 text-gray-400 group-hover:text-[#F59E0B]" />
                 <span class="text-xs font-semibold text-center leading-tight">Filter<br>Events</span>
               </button>
               <button @click="scrollTo('security')" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#EF4444] hover:bg-red-50 text-gray-700 hover:text-[#EF4444] transition-colors group">
                 <ShieldAlert class="w-5 h-5 mb-2 text-gray-400 group-hover:text-[#EF4444]" />
                 <span class="text-xs font-semibold text-center leading-tight">Security<br>Events</span>
               </button>
               <button @click="fetchLogs" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors group">
                 <RefreshCw class="w-5 h-5 mb-2 text-gray-400 group-hover:text-[#2563EB]" />
                 <span class="text-xs font-semibold text-center leading-tight">Refresh<br>Logs</span>
               </button>
             </div>
          </div>
          <div class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 flex flex-col justify-between">
             <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <BarChart3 class="w-4 h-4 text-[#2563EB]" /> Log Statistics
             </h2>
             <div class="grid grid-cols-2 gap-3 flex-1">
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Most Active Module</p><p class="text-sm font-bold text-[#2563EB]">{{ logStats.most_active_module }}</p></div>
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Peak Login</p><p class="text-sm font-bold text-gray-900">{{ logStats.peak_login_hour }}</p></div>
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Busiest Day</p><p class="text-sm font-bold text-gray-900">{{ logStats.busiest_day }}</p></div>
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Avg Daily Events</p><p class="text-sm font-bold text-green-600">{{ logStats.avg_daily_events }}</p></div>
             </div>
          </div>
        </section>

        <!-- Advanced Search & Filter Panel -->
        <section id="filter" class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col gap-4">
          <div class="flex flex-col md:flex-row gap-4 w-full">
            <div class="w-full md:w-1/3 relative">
              <Search class="w-5 h-5 text-gray-400 absolute left-3 top-2.5" />
              <input 
                v-model="filters.search" 
                type="text" 
                placeholder="Search User, Email, Log ID, IP..." 
                class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
            <div class="w-full md:w-2/3 grid grid-cols-2 md:grid-cols-4 gap-3">
              <select v-model="filters.role" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 w-full">
                <option value="All">All Roles</option><option value="Admin">Admin</option><option value="Officer">Officer</option><option value="Worker">Worker</option><option value="Citizen">Citizen</option>
              </select>
              <select v-model="filters.module" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 w-full">
                <option value="All">All Modules</option><option value="Authentication">Authentication</option><option value="Profile">Profile</option><option value="Complaint">Complaint</option><option value="Officer">Officer</option><option value="Department">Department</option>
              </select>
              <select v-model="filters.status" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 w-full">
                <option value="All">All Status</option><option value="Success">Success</option><option value="Warning">Warning</option><option value="Critical">Critical</option>
              </select>
              <select v-model="filters.date" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 w-full">
                <option value="All Time">All Time</option><option value="Today">Today</option><option value="Yesterday">Yesterday</option><option value="Last 7 Days">Last 7 Days</option><option value="Last 30 Days">Last 30 Days</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end gap-3 border-t border-gray-100 pt-4">
            <button @click="resetFilters" class="px-5 py-2 bg-gray-50 text-gray-600 text-sm font-semibold border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Reset Filters</button>
          </div>
        </section>

        <!-- Activity Logs Table (Desktop) -->
        <section class="hidden lg:block bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden mb-6">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse min-w-[1000px]">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-[10px] uppercase tracking-wider font-bold">
                  <th class="p-4 whitespace-nowrap">Log ID / Time</th>
                  <th class="p-4 whitespace-nowrap">User & Role</th>
                  <th class="p-4 whitespace-nowrap">Module</th>
                  <th class="p-4 whitespace-nowrap">Action & Description</th>
                  <th class="p-4 whitespace-nowrap text-center">Status</th>
                  <th class="p-4 whitespace-nowrap">IP Address</th>
                  <th class="p-4 whitespace-nowrap text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm">
                <tr v-for="log in filteredLogs" :key="log.id" class="hover:bg-gray-50 transition-colors group cursor-pointer" @click="openDrawer(log)">
                  <td class="p-4">
                    <p class="font-bold text-[#2563EB] text-xs font-mono">{{ log.id }}</p>
                    <p class="text-xs text-gray-500 mt-0.5">{{ log.date }} {{ log.time }}</p>
                  </td>
                  <td class="p-4">
                    <p class="font-bold text-gray-900">{{ log.user }}</p>
                    <span :class="['mt-0.5 px-2 py-0.5 text-[9px] font-bold uppercase rounded-md', getRoleBadge(log.role)]">{{ log.role }}</span>
                  </td>
                  <td class="p-4 text-gray-700 font-medium">{{ log.module }}</td>
                  <td class="p-4">
                    <p class="font-bold text-gray-900">{{ log.action }}</p>
                    <p class="text-xs text-gray-500 truncate max-w-[200px] mt-0.5">{{ log.desc }}</p>
                  </td>
                  <td class="p-4 text-center">
                    <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide flex items-center justify-center gap-1.5 w-max mx-auto', getStatusBadge(log.status)]">
                      <span class="w-1.5 h-1.5 rounded-full bg-current"></span> {{ log.status }}
                    </span>
                  </td>
                  <td class="p-4 text-xs text-gray-500">
                    <p class="font-mono text-gray-700">{{ log.ip }}</p>
                  </td>
                  <td class="p-4 text-right" @click.stop>
                    <div class="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click="openDrawer(log)" class="p-1.5 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg" title="View Details"><Eye class="w-4 h-4" /></button>
                      <button @click="copyText(log.id)" class="p-1.5 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg" title="Copy Log ID"><Copy class="w-4 h-4" /></button>
                      <button @click="downloadBlob(JSON.stringify(log, null, 2), `${log.id}.json`, 'application/json')" class="p-1.5 text-gray-400 hover:text-[#22C55E] hover:bg-green-50 rounded-lg" title="Export Entry"><Download class="w-4 h-4" /></button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredLogs.length === 0">
                  <td colspan="7" class="p-10 text-center text-gray-500">No activity logs found matching the current filters.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Result count -->
          <div class="p-4 border-t border-gray-100 flex items-center justify-between text-sm text-gray-500 bg-gray-50/50">
            <span>Showing {{ filteredLogs.length }} of {{ logs.length }} most recent logs</span>
          </div>
        </section>

        <!-- Mobile Activity Cards -->
        <section class="lg:hidden space-y-4 mb-6">
          <div v-for="log in filteredLogs" :key="log.id" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50" @click="openDrawer(log)">
            <div class="flex justify-between items-start mb-2">
              <div>
                <h3 class="font-bold text-gray-900 text-sm">{{ log.user }}</h3>
                <p class="text-[10px] text-gray-500 font-mono mt-0.5">{{ log.id }} • {{ log.time }}</p>
              </div>
              <span :class="['px-2 py-0.5 rounded-md text-[9px] font-bold uppercase', getRoleBadge(log.role)]">{{ log.role }}</span>
            </div>
            <div class="mb-3">
              <p class="font-bold text-gray-800 text-sm">{{ log.action }}</p>
              <p class="text-xs text-gray-500 truncate mt-0.5">{{ log.desc }}</p>
            </div>
            <div class="flex justify-between items-center mt-3 pt-3 border-t border-gray-50">
              <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', getStatusBadge(log.status)]">{{ log.status }}</span>
              <button class="text-[#2563EB] text-xs font-semibold hover:underline">Details</button>
            </div>
          </div>
        </section>

        <!-- Charts Row -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <BarChart3 class="w-4 h-4 text-[#2563EB]"/> Most Frequent Activities
            </h2>
            <div class="relative h-64 w-full">
              <canvas ref="horizontalBarChartRef"></canvas>
            </div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <PieChart class="w-4 h-4 text-[#2563EB]"/> Role Distribution
            </h2>
            <div class="relative h-64 w-full flex justify-center">
              <canvas ref="pieChartRef"></canvas>
            </div>
          </div>
        </section>

        <!-- Activity Heatmap -->
        <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 mb-6 overflow-hidden">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
              <Activity class="w-4 h-4 text-[#2563EB]"/> Platform Activity by Day & Hour
            </h2>
            <div class="flex items-center gap-2 text-[10px] text-gray-500 font-semibold uppercase">
              <span>Less</span>
              <div class="flex gap-1">
                <div class="w-3 h-3 rounded-sm bg-gray-100"></div>
                <div class="w-3 h-3 rounded-sm bg-blue-200"></div>
                <div class="w-3 h-3 rounded-sm bg-blue-400"></div>
                <div class="w-3 h-3 rounded-sm bg-blue-600"></div>
                <div class="w-3 h-3 rounded-sm bg-blue-800"></div>
              </div>
              <span>More</span>
            </div>
          </div>
          
          <div class="w-full overflow-x-auto pb-2 custom-scrollbar">
            <div class="min-w-[700px]">
              <!-- Hours Header -->
              <div class="flex pl-10 mb-2 text-[10px] text-gray-400 font-medium">
                <div class="flex-1 text-center" v-for="h in [0, 4, 8, 12, 16, 20]" :key="h">{{h}}:00</div>
              </div>
              <!-- Grid -->
              <div class="flex flex-col gap-1">
                <div v-for="(day, dIndex) in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']" :key="dIndex" class="flex gap-1 items-center">
                  <span class="w-8 text-[10px] text-gray-500 font-medium shrink-0">{{ day }}</span>
                  <div class="flex flex-1 gap-1">
                    <div 
                      v-for="(hour, hIndex) in 24" :key="hIndex" 
                      class="flex-1 aspect-square rounded-sm border border-black/5 hover:border-black/20 transition-all cursor-pointer"
                      :style="`background-color: ${getHeatmapColor(dIndex, hIndex)}`"
                      :title="`${day} ${hIndex}:00 - Activity Level`"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Security, Timelines & Active Users -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          
          <!-- Security Events -->
          <div id="security" class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[400px]">
            <h2 class="text-sm font-bold text-red-600 uppercase tracking-wider mb-5 flex items-center gap-2">
              <ShieldAlert class="w-4 h-4" /> Security Events
            </h2>
            <div class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
              <div v-for="sec in securityEvents" :key="sec.id" class="p-3 border border-gray-100 rounded-xl bg-gray-50 hover:bg-white hover:border-gray-200 transition-colors group">
                <div class="flex justify-between items-start mb-1">
                  <h4 class="font-bold text-gray-900 text-sm group-hover:text-[#2563EB] transition-colors">{{ sec.event }}</h4>
                  <span :class="['px-2 py-0.5 rounded text-[9px] font-bold uppercase', sec.severity === 'High' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700']">{{ sec.severity }}</span>
                </div>
                <div class="flex justify-end items-end mt-2">
                  <span class="text-2xl font-bold text-gray-800">{{ sec.count }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Critical Events Timeline -->
          <div class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[400px]">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <AlertTriangle class="w-4 h-4 text-[#F59E0B]" /> Critical Events
            </h2>
            <div class="flex-1 overflow-y-auto custom-scrollbar">
              <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
                <div v-for="act in criticalEvents" :key="act.id" class="relative pl-5">
                  <span :class="`absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 ${act.color}`"></span>
                  <div class="flex justify-between items-baseline mb-0.5">
                    <h4 class="text-xs font-bold text-gray-900">{{ act.action }}</h4>
                    <span class="text-[9px] text-gray-400 font-medium shrink-0 ml-2">{{ act.time }}</span>
                  </div>
                  <p class="text-[11px] text-gray-500">{{ act.desc }}</p>
                  <p class="text-[10px] text-[#2563EB] font-semibold mt-0.5">{{ act.user }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Most Active Users -->
          <div class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[400px]">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <Users class="w-4 h-4 text-[#2563EB]" /> Most Active Users
            </h2>
            <div class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
              <div v-for="user in activeUsers" :key="user.name" class="flex justify-between items-center p-3 bg-gray-50 border border-gray-100 rounded-xl">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-blue-100 text-[#2563EB] flex items-center justify-center font-bold shrink-0">{{ user.name.charAt(0) }}</div>
                  <div>
                    <p class="font-bold text-gray-900 text-sm">{{ user.name }}</p>
                    <span :class="['mt-0.5 px-2 py-0.5 text-[9px] font-bold uppercase rounded', getRoleBadge(user.role)]">{{ user.role }}</span>
                  </div>
                </div>
                <div class="text-right">
                  <p class="font-bold text-gray-900 text-sm">{{ user.count }} <span class="text-[10px] font-normal text-gray-500">Logs</span></p>
                </div>
              </div>
            </div>
          </div>
        </section>
        </template>

      </main>
    </div>

    <!-- Activity Details Drawer -->
    <div v-if="isDrawerOpen && selectedLog" class="fixed inset-0 z-50 overflow-hidden" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
      <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity" @click="closeDrawer"></div>
      <div class="fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-2xl flex flex-col transform transition-transform duration-300 ease-in-out border-l border-gray-100">
        
        <div class="p-6 border-b border-gray-100 bg-gray-50/50 flex justify-between items-start">
          <div>
             <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase mb-2 inline-block', getStatusBadge(selectedLog.status)]">{{ selectedLog.status }}</span>
             <h2 class="text-xl font-bold text-gray-900 leading-tight font-mono">{{ selectedLog.id }}</h2>
             <p class="text-xs text-gray-500 mt-1">{{ selectedLog.date }} • {{ selectedLog.time }}</p>
          </div>
          <button @click="closeDrawer" class="p-2 text-gray-400 hover:bg-gray-200 rounded-full transition-colors shrink-0"><X class="w-5 h-5"/></button>
        </div>

        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-6">
          <!-- Actor Info -->
          <div>
            <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Actor Information</h3>
            <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-2">
              <div class="flex justify-between"><span class="text-xs text-gray-500">User</span><span class="text-sm font-bold text-gray-900">{{ selectedLog.user }}</span></div>
              <div class="flex justify-between"><span class="text-xs text-gray-500">Role</span><span :class="['px-2 py-0.5 text-[10px] font-bold uppercase rounded', getRoleBadge(selectedLog.role)]">{{ selectedLog.role }}</span></div>
              <div class="flex justify-between"><span class="text-xs text-gray-500">Department</span><span class="text-sm font-medium text-gray-900">{{ selectedLog.department || 'N/A' }}</span></div>
            </div>
          </div>

          <!-- Event Details -->
          <div>
            <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Event Details</h3>
            <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-3">
              <div><span class="text-xs text-gray-500 block mb-0.5">Module</span><span class="text-sm font-medium text-gray-900">{{ selectedLog.module }}</span></div>
              <div><span class="text-xs text-gray-500 block mb-0.5">Action</span><span class="text-sm font-bold text-[#2563EB]">{{ selectedLog.action }}</span></div>
              <div><span class="text-xs text-gray-500 block mb-0.5">Description</span><span class="text-sm text-gray-700 leading-snug block">{{ selectedLog.desc }}</span></div>
            </div>
          </div>

          <!-- Client Details -->
          <div>
            <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Client Information</h3>
            <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-2 text-xs">
              <div class="flex justify-between"><span class="text-gray-500">IP Address</span><span class="font-mono text-gray-900">{{ selectedLog.ip }}</span></div>
            </div>
          </div>
        </div>

        <div class="p-4 border-t border-gray-100 bg-white grid grid-cols-2 gap-3">
          <button @click="copyText(JSON.stringify(selectedLog, null, 2))" class="py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 flex items-center justify-center gap-2">
            <Copy class="w-4 h-4"/> Copy JSON
          </button>
          <button @click="downloadBlob(JSON.stringify(selectedLog, null, 2), `${selectedLog.id}.json`, 'application/json')" class="py-2.5 bg-[#2563EB] text-white text-sm font-semibold rounded-xl hover:bg-[#1E40AF] shadow-sm flex items-center justify-center gap-2">
            <Download class="w-4 h-4"/> Export Log
          </button>
        </div>
      </div>
    </div>

    <!-- Export Modal -->
    <div v-if="exportModalOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="closeExportModal"></div>
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-md p-6 transform transition-all">
        <h2 class="text-xl font-bold text-gray-900 mb-1">Export Activity Logs</h2>
        <p class="text-sm text-gray-500 mb-5">Exports whatever's currently filtered on the page.</p>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Export Format</label>
            <div class="grid grid-cols-2 gap-2">
              <button @click="exportFormat = 'csv'" :class="exportFormat === 'csv' ? 'border-[#2563EB] bg-blue-50 text-[#2563EB]' : 'border-gray-200 text-gray-700 hover:bg-gray-50'" class="p-3 border font-bold text-sm rounded-xl transition-colors">CSV</button>
              <button @click="exportFormat = 'json'" :class="exportFormat === 'json' ? 'border-[#2563EB] bg-blue-50 text-[#2563EB]' : 'border-gray-200 text-gray-700 hover:bg-gray-50'" class="p-3 border font-bold text-sm rounded-xl transition-colors">JSON</button>
              <button disabled title="Not available yet" class="p-3 border border-gray-100 text-gray-300 font-bold text-sm rounded-xl cursor-not-allowed">PDF</button>
              <button disabled title="Not available yet" class="p-3 border border-gray-100 text-gray-300 font-bold text-sm rounded-xl cursor-not-allowed">Excel</button>
            </div>
          </div>
          <p class="text-xs text-gray-500">Will export <span class="font-bold text-gray-900">{{ filteredLogs.length }}</span> log{{ filteredLogs.length === 1 ? '' : 's' }} matching the current filters.</p>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
            <button @click="closeExportModal" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl">Cancel</button>
            <button @click="runExport" class="px-5 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl shadow-sm flex items-center gap-2"><Download class="w-4 h-4"/> Export</button>
          </div>
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
  Activity, Clock, Shield, ShieldAlert, FileText, ClipboardList, Users, 
  UserCog, Bell, Search, Filter, Eye, Download, Copy, RefreshCw, 
  Monitor, Globe, Laptop, Smartphone, MapPin, AlertTriangle, 
  CheckCircle, XCircle, BarChart3, PieChart, TrendingUp, TrendingDown, X
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const router = useRouter();
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

// View State
const sidebarOpen = ref(false);
const isDrawerOpen = ref(false);
const exportModalOpen = ref(false);
const selectedLog = ref(null);
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
const isLoading = ref(true);
const errorMessage = ref('');
const exportFormat = ref('csv');

// --- Live data — populated from GET /api/admin/activity-logs ---
const STAT_META = {
  total_events:    { label: 'Total Events',    icon: Activity,    colorClass: 'text-blue-600 bg-blue-100',   textClass: 'text-blue-600' },
  today:           { label: 'Today',           icon: Clock,       colorClass: 'text-indigo-600 bg-indigo-100', textClass: 'text-indigo-600' },
  admin_actions:   { label: 'Admin Actions',   icon: UserCog,     colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  officer_actions: { label: 'Officer Actions', icon: Shield,      colorClass: 'text-teal-600 bg-teal-100',   textClass: 'text-teal-600' },
  worker_actions:  { label: 'Worker Actions',  icon: ClipboardList, colorClass: 'text-yellow-600 bg-yellow-100', textClass: 'text-yellow-600' },
  citizen_actions: { label: 'Citizen Actions', icon: Users,       colorClass: 'text-green-600 bg-green-100', textClass: 'text-green-600' },
  security_events: { label: 'Security Events', icon: ShieldAlert, colorClass: 'text-red-600 bg-red-100',     textClass: 'text-red-600' },
  system_events:   { label: 'System Events',   icon: Monitor,     colorClass: 'text-gray-600 bg-gray-100',   textClass: 'text-gray-600' },
};
const STAT_ORDER = ['total_events', 'today', 'admin_actions', 'officer_actions', 'worker_actions', 'citizen_actions', 'security_events', 'system_events'];

const topStats = ref([]);
const logStats = ref({ most_active_module: 'N/A', peak_login_hour: 'N/A', busiest_day: 'N/A', avg_daily_events: 0 });
const securityEvents = ref([]);
const activeUsers = ref([]);
const criticalEvents = ref([]);
const logs = ref([]);
const heatmap = ref(Array.from({ length: 7 }, () => Array(24).fill(0)));
const mostFrequentActivities = ref([]);
const roleDistribution = ref({ Admin: 0, Officer: 0, Worker: 0, Citizen: 0 });

const fetchLogs = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/activity-logs`, authHeaders());

    topStats.value = STAT_ORDER.map(key => ({ ...STAT_META[key], value: data.top_stats[key] }));
    logStats.value = data.log_stats;
    securityEvents.value = data.security_events;
    activeUsers.value = data.active_users;
    criticalEvents.value = data.critical_events;
    logs.value = data.logs;
    heatmap.value = data.heatmap;
    mostFrequentActivities.value = data.most_frequent_activities;
    roleDistribution.value = data.role_distribution;

    renderCharts();
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    else errorMessage.value = err.response?.data?.message || 'Failed to load activity logs.';
  } finally {
    isLoading.value = false;
  }
};

// --- Filters & Search Logic ---
const filters = reactive({ search: '', role: 'All', module: 'All', status: 'All', date: 'All Time' });

const filteredLogs = computed(() => {
  let result = logs.value;
  if (filters.search) {
    const q = filters.search.toLowerCase();
    result = result.filter(l => l.user.toLowerCase().includes(q) || l.id.toLowerCase().includes(q) || l.ip.includes(q) || l.desc.toLowerCase().includes(q));
  }
  if (filters.role !== 'All') result = result.filter(l => l.role === filters.role);
  if (filters.module !== 'All') result = result.filter(l => l.module === filters.module);
  if (filters.status !== 'All') result = result.filter(l => l.status === filters.status);
  if (filters.date !== 'All Time') {
    const now = new Date();
    const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    result = result.filter(l => {
      const t = new Date(l.created_at);
      switch (filters.date) {
        case 'Today': return t >= startOfToday;
        case 'Yesterday': {
          const startOfYesterday = new Date(startOfToday); startOfYesterday.setDate(startOfYesterday.getDate() - 1);
          return t >= startOfYesterday && t < startOfToday;
        }
        case 'Last 7 Days': return t >= new Date(startOfToday.getTime() - 7 * 86400000);
        case 'Last 30 Days': return t >= new Date(startOfToday.getTime() - 30 * 86400000);
        default: return true;
      }
    });
  }
  return result;
});

const resetFilters = () => { filters.search = ''; filters.role = 'All'; filters.module = 'All'; filters.status = 'All'; filters.date = 'All Time'; };

// --- UI Helpers ---
const getRoleBadge = (role) => {
  switch(role) {
    case 'Admin': return 'bg-purple-100 text-purple-700';
    case 'Officer': return 'bg-blue-100 text-blue-700';
    case 'Worker': return 'bg-yellow-100 text-yellow-700';
    default: return 'bg-teal-100 text-teal-700'; // Citizen
  }
};
const getStatusBadge = (status) => {
  switch(status) {
    case 'Success': return 'bg-green-100 text-green-700';
    case 'Warning': return 'bg-yellow-100 text-yellow-700';
    case 'Critical': return 'bg-red-600 text-white shadow-sm border border-red-700';
    default: return 'bg-gray-100 text-gray-700';
  }
};

// Heatmap — real day x hour counts from the backend, color-scaled by the matrix's own max.
const heatmapMax = computed(() => Math.max(1, ...heatmap.value.flat()));
const getHeatmapColor = (dayIndex, hourIndex) => {
  const val = heatmap.value[dayIndex]?.[hourIndex] || 0;
  if (val === 0) return 'rgba(37, 99, 235, 0.05)';
  const intensity = val / heatmapMax.value;
  return `rgba(37, 99, 235, ${0.15 + intensity * 0.75})`;
};

const scrollTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });

// Modal / Drawer interactions
const openDrawer = (log) => { selectedLog.value = log; isDrawerOpen.value = true; };
const closeDrawer = () => { isDrawerOpen.value = false; setTimeout(() => { selectedLog.value = null; }, 300); };
const openExportModal = () => { exportModalOpen.value = true; };
const closeExportModal = () => { exportModalOpen.value = false; };

const copyText = (text) => navigator.clipboard.writeText(text);

const downloadBlob = (content, filename, type) => {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

const exportCSV = () => {
  const cols = ['id', 'date', 'time', 'user', 'role', 'department', 'action', 'desc', 'module', 'status', 'ip'];
  const header = cols.join(',');
  const rows = filteredLogs.value.map(l => cols.map(c => `"${String(l[c] ?? '').replace(/"/g, '""')}"`).join(','));
  downloadBlob([header, ...rows].join('\n'), `activity-logs-${Date.now()}.csv`, 'text/csv');
  closeExportModal();
};

const exportJSON = () => {
  downloadBlob(JSON.stringify(filteredLogs.value, null, 2), `activity-logs-${Date.now()}.json`, 'application/json');
  closeExportModal();
};

const runExport = () => {
  if (exportFormat.value === 'csv') exportCSV();
  else if (exportFormat.value === 'json') exportJSON();
};

// --- Charts Logic ---
const horizontalBarChartRef = ref(null);
const pieChartRef = ref(null);
let barChart = null;
let pieChart = null;
const ROLE_COLORS = { Admin: '#9333EA', Officer: '#2563EB', Worker: '#F59E0B', Citizen: '#14B8A6' };

const renderCharts = () => {
  if (!horizontalBarChartRef.value || !pieChartRef.value) return;
  Chart.defaults.font.family = 'Inter, sans-serif';
  Chart.defaults.color = '#64748b';

  barChart?.destroy();
  barChart = new Chart(horizontalBarChartRef.value, {
    type: 'bar',
    data: {
      labels: mostFrequentActivities.value.map(a => a.label),
      datasets: [{ label: 'Event Count', data: mostFrequentActivities.value.map(a => a.count), backgroundColor: '#2563EB', borderRadius: 4 }]
    },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#F3F4F6' } }, y: { grid: { display: false } } } }
  });

  const roleLabels = Object.keys(roleDistribution.value);
  pieChart?.destroy();
  pieChart = new Chart(pieChartRef.value, {
    type: 'pie',
    data: {
      labels: roleLabels,
      datasets: [{ data: roleLabels.map(r => roleDistribution.value[r]), backgroundColor: roleLabels.map(r => ROLE_COLORS[r] || '#94A3B8'), borderWidth: 0 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } }
  });
};

onMounted(fetchLogs);
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

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>