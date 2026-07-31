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
          <div class="flex flex-col items-end gap-1 shrink-0">
            <div class="bg-white px-4 py-2 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-2">
              <Clock class="w-4 h-4 text-[#2563EB]" />
              <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
            </div>
            <span class="text-[10px] text-gray-400 font-medium">Last Updated: Just now</span>
          </div>
        </header>

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
               <button @click="openExportModal" class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#22C55E] hover:bg-green-50 text-gray-700 hover:text-[#22C55E] transition-colors group">
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
               <button class="flex flex-col items-center justify-center p-3 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors group">
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
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Most Active Mod.</p><p class="text-sm font-bold text-[#2563EB]">Complaints</p></div>
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Peak Login</p><p class="text-sm font-bold text-gray-900">09:00 - 10:00 AM</p></div>
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Highest Day</p><p class="text-sm font-bold text-gray-900">Monday (1.2k)</p></div>
               <div class="p-3 bg-gray-50 rounded-xl border border-gray-100"><p class="text-[10px] text-gray-500 font-bold uppercase mb-0.5">Avg Daily Events</p><p class="text-sm font-bold text-green-600">845</p></div>
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
                <option value="All">All Roles</option><option value="Administrator">Administrator</option><option value="Officer">Officer</option><option value="Worker">Worker</option><option value="Citizen">Citizen</option>
              </select>
              <select v-model="filters.module" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 w-full">
                <option value="All">All Modules</option><option value="Authentication">Authentication</option><option value="Complaint">Complaint</option><option value="Department">Department</option><option value="Security">Security</option>
              </select>
              <select v-model="filters.status" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 w-full">
                <option value="All">All Status</option><option value="Success">Success</option><option value="Warning">Warning</option><option value="Error">Error</option><option value="Critical">Critical</option>
              </select>
              <select v-model="filters.date" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 w-full">
                <option value="Today">Today</option><option value="Yesterday">Yesterday</option><option value="Last 7 Days">Last 7 Days</option><option value="Last 30 Days">Last 30 Days</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end gap-3 border-t border-gray-100 pt-4">
            <button @click="resetFilters" class="px-5 py-2 bg-gray-50 text-gray-600 text-sm font-semibold border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Reset</button>
            <button class="px-5 py-2 bg-[#2563EB] text-white text-sm font-semibold rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm">Apply Filters</button>
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
                  <th class="p-4 whitespace-nowrap">IP / Device</th>
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
                    <p>{{ log.device }}</p>
                  </td>
                  <td class="p-4 text-right" @click.stop>
                    <div class="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click="openDrawer(log)" class="p-1.5 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg" title="View Details"><Eye class="w-4 h-4" /></button>
                      <button class="p-1.5 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg" title="Copy Log ID"><Copy class="w-4 h-4" /></button>
                      <button class="p-1.5 text-gray-400 hover:text-[#22C55E] hover:bg-green-50 rounded-lg" title="Export Entry"><Download class="w-4 h-4" /></button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredLogs.length === 0">
                  <td colspan="7" class="p-10 text-center text-gray-500">No activity logs found matching the current filters.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Pagination -->
          <div class="p-4 border-t border-gray-100 flex items-center justify-between text-sm text-gray-500 bg-gray-50/50">
            <span>Showing 1 to {{ filteredLogs.length }} of 8,452 logs</span>
            <div class="flex gap-1">
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50">Prev</button>
              <button class="px-3 py-1 border border-gray-200 bg-[#2563EB] text-white rounded-md">1</button>
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50">2</button>
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50">3</button>
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50">Next</button>
            </div>
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
                <div class="flex justify-between items-end mt-2">
                  <span class="text-2xl font-bold text-gray-800">{{ sec.count }}</span>
                  <span class="text-[10px] text-gray-500">Latest: {{ sec.latest }}</span>
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
                  <button class="text-[10px] text-[#2563EB] font-semibold hover:underline mt-1">Profile</button>
                </div>
              </div>
            </div>
          </div>
        </section>

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
              
              <!-- Value Changes (If applicable) -->
              <div v-if="selectedLog.oldValue" class="mt-4 pt-3 border-t border-gray-200 grid grid-cols-2 gap-3">
                <div><span class="text-[10px] font-bold text-red-500 uppercase block mb-1">Old Value</span><span class="text-xs text-gray-600 font-mono bg-red-50 p-1.5 rounded block line-clamp-2">{{ selectedLog.oldValue }}</span></div>
                <div><span class="text-[10px] font-bold text-green-600 uppercase block mb-1">New Value</span><span class="text-xs text-gray-600 font-mono bg-green-50 p-1.5 rounded block line-clamp-2">{{ selectedLog.newValue }}</span></div>
              </div>
            </div>
          </div>

          <!-- Client Details -->
          <div>
            <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Client Information</h3>
            <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-2 text-xs">
              <div class="flex justify-between"><span class="text-gray-500">IP Address</span><span class="font-mono text-gray-900">{{ selectedLog.ip }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Device</span><span class="font-medium text-gray-900">{{ selectedLog.device }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Browser</span><span class="font-medium text-gray-900">{{ selectedLog.browser }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">OS</span><span class="font-medium text-gray-900">{{ selectedLog.os }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Location</span><span class="font-medium text-gray-900">{{ selectedLog.location }}</span></div>
            </div>
          </div>
        </div>

        <div class="p-4 border-t border-gray-100 bg-white grid grid-cols-2 gap-3">
          <button class="py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 flex items-center justify-center gap-2">
            <Copy class="w-4 h-4"/> Copy JSON
          </button>
          <button class="py-2.5 bg-[#2563EB] text-white text-sm font-semibold rounded-xl hover:bg-[#1E40AF] shadow-sm flex items-center justify-center gap-2">
            <Download class="w-4 h-4"/> Export Log
          </button>
        </div>
      </div>
    </div>

    <!-- Export Modal -->
    <div v-if="exportModalOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="closeExportModal"></div>
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-md p-6 transform transition-all">
        <h2 class="text-xl font-bold text-gray-900 mb-1">Export Audit Logs</h2>
        <p class="text-sm text-gray-500 mb-5">Select format and filters for the exported data.</p>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Export Format</label>
            <div class="grid grid-cols-2 gap-2">
              <button class="p-3 border border-[#2563EB] bg-blue-50 text-[#2563EB] font-bold text-sm rounded-xl">CSV</button>
              <button class="p-3 border border-gray-200 text-gray-700 hover:bg-gray-50 font-bold text-sm rounded-xl">PDF</button>
              <button class="p-3 border border-gray-200 text-gray-700 hover:bg-gray-50 font-bold text-sm rounded-xl">Excel</button>
              <button class="p-3 border border-gray-200 text-gray-700 hover:bg-gray-50 font-bold text-sm rounded-xl">JSON</button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Date Range</label>
            <select class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none text-sm">
              <option>Last 7 Days (Default)</option><option>Last 30 Days</option><option>All Time</option>
            </select>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
            <button @click="closeExportModal" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl">Cancel</button>
            <button @click="closeExportModal" class="px-5 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl shadow-sm flex items-center gap-2"><Download class="w-4 h-4"/> Export</button>
          </div>
        </div>
      </div>
    </div>

</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import Chart from 'chart.js/auto';

// Icons
import { 
  Activity, Clock, Shield, ShieldAlert, FileText, ClipboardList, Users, 
  UserCog, Bell, Search, Filter, Eye, Download, Copy, RefreshCw, 
  Monitor, Globe, Laptop, Smartphone, MapPin, AlertTriangle, 
  CheckCircle, XCircle, BarChart3, PieChart, TrendingUp, TrendingDown, X
} from 'lucide-vue-next';

// View State
const sidebarOpen = ref(false);
const isDrawerOpen = ref(false);
const exportModalOpen = ref(false);
const selectedLog = ref(null);
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });

// --- Dummy Data ---
const topStats = ref([
  { label: 'Total Events', value: '1.2M', trend: 5, icon: Activity, colorClass: 'text-blue-600 bg-blue-100', textClass: 'text-blue-600' },
  { label: 'Today', value: '8,452', trend: 12, icon: Clock, colorClass: 'text-indigo-600 bg-indigo-100', textClass: 'text-indigo-600' },
  { label: 'Admin Actions', value: '142', trend: -2, icon: UserCog, colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  { label: 'Officer Actions', value: '3.4k', trend: 8, icon: Shield, colorClass: 'text-teal-600 bg-teal-100', textClass: 'text-teal-600' },
  { label: 'Worker Actions', value: '2.1k', trend: 15, icon: ClipboardList, colorClass: 'text-yellow-600 bg-yellow-100', textClass: 'text-yellow-600' },
  { label: 'Citizen Actions', value: '2.8k', trend: -4, icon: Users, colorClass: 'text-green-600 bg-green-100', textClass: 'text-green-600' },
  { label: 'Security Events', value: '24', trend: -10, icon: ShieldAlert, colorClass: 'text-red-600 bg-red-100', textClass: 'text-red-600' },
  { label: 'System Events', value: '56', trend: 2, icon: Monitor, colorClass: 'text-gray-600 bg-gray-100', textClass: 'text-gray-600' }
]);

const securityEvents = ref([
  { id: 1, event: 'Failed Login Attempts', severity: 'High', count: 45, latest: '10 mins ago' },
  { id: 2, event: 'Unauthorized Access', severity: 'High', count: 2, latest: 'Yesterday' },
  { id: 3, event: 'Password Resets', severity: 'Medium', count: 124, latest: '1 hr ago' },
  { id: 4, event: 'Account Suspensions', severity: 'Medium', count: 3, latest: '2 days ago' }
]);

const activeUsers = ref([
  { name: 'Anita Patel', role: 'Officer', count: 1420 },
  { name: 'System Admin', role: 'Administrator', count: 850 },
  { name: 'Rahul V.', role: 'Worker', count: 620 },
  { name: 'Jane Doe', role: 'Citizen', count: 45 }
]);

const criticalEvents = ref([
  { id: 1, action: 'Officer Account Suspended', time: '10:30 AM', desc: 'Arjun Verma suspended by Administrator.', user: 'SysAdmin', color: 'border-red-500' },
  { id: 2, action: 'Emergency Complaint', time: '09:15 AM', desc: 'Major Road Cave-in reported in Ward 4.', user: 'Citizen_842', color: 'border-orange-500' },
  { id: 3, action: 'System Settings Updated', time: 'Yesterday', desc: 'Global timeout setting changed to 30 mins.', user: 'SysAdmin', color: 'border-yellow-500' },
  { id: 4, action: 'Department Deleted', time: 'Jul 10', desc: 'Legacy department removed from system.', user: 'SysAdmin', color: 'border-red-500' }
]);

const logs = ref([
  { id: 'LOG-884291', date: 'Jul 12, 2026', time: '12:45:00', user: 'System Admin', role: 'Administrator', department: 'System', action: 'Update System Settings', desc: 'Changed session timeout from 60 to 30 mins.', module: 'Settings', status: 'Success', ip: '192.168.1.10', device: 'Desktop', browser: 'Chrome 115', os: 'Windows 11', location: 'Pune, India', oldValue: '60 mins', newValue: '30 mins' },
  { id: 'LOG-884290', date: 'Jul 12, 2026', time: '12:40:15', user: 'Anita Patel', role: 'Officer', department: 'Road Maintenance', action: 'Assign Complaint', desc: 'Assigned CMP-842 to Worker Rahul V.', module: 'Complaint', status: 'Success', ip: '10.0.0.52', device: 'Desktop', browser: 'Firefox 110', os: 'Windows 10', location: 'Pune, India' },
  { id: 'LOG-884289', date: 'Jul 12, 2026', time: '12:35:10', user: 'Unknown', role: 'Citizen', department: '', action: 'Failed Login', desc: 'Invalid credentials provided.', module: 'Authentication', status: 'Warning', ip: '45.22.11.9', device: 'Mobile', browser: 'Safari Mobile', os: 'iOS 16', location: 'Mumbai, India' },
  { id: 'LOG-884288', date: 'Jul 12, 2026', time: '12:15:00', user: 'Rahul V.', role: 'Worker', department: 'Road Maintenance', action: 'Status Update', desc: 'Marked CMP-840 as Resolved.', module: 'Complaint', status: 'Success', ip: '10.0.1.22', device: 'Mobile', browser: 'Chrome Mobile', os: 'Android 13', location: 'Pune, India', oldValue: 'In Progress', newValue: 'Resolved' },
  { id: 'LOG-884287', date: 'Jul 12, 2026', time: '11:50:00', user: 'System Admin', role: 'Administrator', department: 'System', action: 'Suspend Officer', desc: 'Account suspension for Arjun Verma.', module: 'Officer', status: 'Critical', ip: '192.168.1.10', device: 'Desktop', browser: 'Chrome 115', os: 'Windows 11', location: 'Pune, India', oldValue: 'Active', newValue: 'Suspended' },
  { id: 'LOG-884286', date: 'Jul 12, 2026', time: '11:00:22', user: 'Jane Doe', role: 'Citizen', department: '', action: 'Submit Complaint', desc: 'New complaint CMP-845 (Garbage).', module: 'Complaint', status: 'Success', ip: '112.19.44.2', device: 'Desktop', browser: 'Edge 114', os: 'Windows 11', location: 'Pune, India' },
  { id: 'LOG-884285', date: 'Jul 12, 2026', time: '10:15:05', user: 'DB Service', role: 'System', department: 'Database', action: 'Connection Error', desc: 'Timeout connecting to replica DB.', module: 'Security', status: 'Error', ip: '127.0.0.1', device: 'Server', browser: 'N/A', os: 'Linux', location: 'AWS ap-south-1' }
]);

// --- Filters & Search Logic ---
const filters = reactive({ search: '', role: 'All', module: 'All', status: 'All', date: 'Today' });

const filteredLogs = computed(() => {
  let result = logs.value;
  if (filters.search) {
    const q = filters.search.toLowerCase();
    result = result.filter(l => l.user.toLowerCase().includes(q) || l.id.toLowerCase().includes(q) || l.ip.includes(q) || l.desc.toLowerCase().includes(q));
  }
  if (filters.role !== 'All') result = result.filter(l => l.role === filters.role);
  if (filters.module !== 'All') result = result.filter(l => l.module === filters.module);
  if (filters.status !== 'All') result = result.filter(l => l.status === filters.status);
  return result;
});

const resetFilters = () => { filters.search = ''; filters.role = 'All'; filters.module = 'All'; filters.status = 'All'; filters.date = 'Today'; };

// --- UI Helpers ---
const getRoleBadge = (role) => {
  switch(role) {
    case 'Administrator': return 'bg-purple-100 text-purple-700';
    case 'Officer': return 'bg-blue-100 text-blue-700';
    case 'Worker': return 'bg-yellow-100 text-yellow-700';
    case 'System': return 'bg-gray-200 text-gray-700';
    default: return 'bg-teal-100 text-teal-700'; // Citizen
  }
};
const getStatusBadge = (status) => {
  switch(status) {
    case 'Success': return 'bg-green-100 text-green-700';
    case 'Warning': return 'bg-yellow-100 text-yellow-700';
    case 'Error': return 'bg-red-100 text-red-700';
    case 'Critical': return 'bg-red-600 text-white shadow-sm border border-red-700';
    default: return 'bg-gray-100 text-gray-700';
  }
};

// Heatmap logic
const getHeatmapColor = (dayIndex, hourIndex) => {
  // Generate random looking but deterministic opacity based on indices for dummy data
  const val = (Math.sin(dayIndex * 12 + hourIndex * 3) + 1) / 2; // 0 to 1
  if (hourIndex > 1 && hourIndex < 6) return 'rgba(37, 99, 235, 0.05)'; // Night time low activity
  if (hourIndex > 9 && hourIndex < 18) return `rgba(37, 99, 235, ${0.4 + val * 0.6})`; // Peak hours
  return `rgba(37, 99, 235, ${0.1 + val * 0.3})`;
};

const scrollTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });

// Modal / Drawer interactions
const openDrawer = (log) => { selectedLog.value = log; isDrawerOpen.value = true; };
const closeDrawer = () => { isDrawerOpen.value = false; setTimeout(() => { selectedLog.value = null; }, 300); };
const openExportModal = () => { exportModalOpen.value = true; };
const closeExportModal = () => { exportModalOpen.value = false; };

// --- Charts Logic ---
const horizontalBarChartRef = ref(null);
const pieChartRef = ref(null);

onMounted(() => {
  Chart.defaults.font.family = 'Inter, sans-serif';
  Chart.defaults.color = '#64748b';

  // 1. Horizontal Bar (Most Frequent Activities)
  new Chart(horizontalBarChartRef.value, {
    type: 'bar',
    data: {
      labels: ['Complaint Updates', 'User Logins', 'Worker Assignments', 'Department Changes', 'Profile Updates', 'Announcements'],
      datasets: [{ label: 'Event Count', data: [4500, 3200, 1800, 420, 350, 120], backgroundColor: '#2563EB', borderRadius: 4 }]
    },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#F3F4F6' } }, y: { grid: { display: false } } } }
  });

  // 2. Pie Chart (Role-wise)
  new Chart(pieChartRef.value, {
    type: 'pie',
    data: {
      labels: ['Administrator', 'Officer', 'Worker', 'Citizen', 'System'],
      datasets: [{ data: [15, 30, 25, 25, 5], backgroundColor: ['#9333EA', '#2563EB', '#F59E0B', '#14B8A6', '#94A3B8'], borderWidth: 0 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } }
  });
});
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