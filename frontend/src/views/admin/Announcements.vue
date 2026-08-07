<template>
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">
      
      
      <!-- Scrollable Dashboard Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">
        
        <!-- Header & Breadcrumbs -->
        <header class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">Announcements</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Announcements</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Create, publish, schedule, and manage platform announcements for all users.
            </p>
          </div>
          <div class="bg-white px-5 py-2.5 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-3 shrink-0">
            <Calendar class="w-5 h-5 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Error banner -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center justify-between">
          <span>{{ errorMessage }}</span>
          <button @click="fetchAnnouncements" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="text-center text-gray-400 py-10">Loading announcements…</div>

        <template v-else>
        <!-- Top Statistics Grid -->
        <section class="mb-6 grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
          <div v-for="(stat, index) in topStats" :key="index" class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 flex flex-col group hover:border-[#2563EB] hover:shadow-md transition-all">
            <div class="flex items-center justify-between mb-3">
              <div :class="`p-2.5 rounded-xl bg-opacity-10 ${stat.colorClass} bg-current group-hover:scale-110 transition-transform duration-300`">
                <component :is="stat.icon" class="w-5 h-5" :class="stat.textClass" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-0.5">{{ stat.value }}</h3>
            <span class="text-xs text-gray-500 font-semibold uppercase tracking-wide">{{ stat.label }}</span>
          </div>
        </section>

        <!-- Quick Actions -->
        <section class="mb-6 grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
          <button @click="openModal('create')" class="flex items-center gap-3 p-3.5 bg-[#2563EB] text-white rounded-[14px] hover:bg-[#1E40AF] transition-colors shadow-sm font-medium">
            <Megaphone class="w-5 h-5 shrink-0" />
            <span class="text-sm">Create New</span>
          </button>
          <button @click="openModal('create')" class="flex items-center gap-3 p-3.5 bg-white border border-gray-100 text-gray-700 rounded-[14px] hover:border-[#2563EB] hover:bg-blue-50 hover:text-[#2563EB] transition-colors font-medium">
            <Clock class="w-5 h-5 shrink-0 text-gray-400" />
            <span class="text-sm">Schedule</span>
          </button>
          <button @click="filters.status = 'Draft'; scrollTo('table')" class="flex items-center gap-3 p-3.5 bg-white border border-gray-100 text-gray-700 rounded-[14px] hover:border-gray-300 hover:bg-gray-50 transition-colors font-medium">
            <FileText class="w-5 h-5 shrink-0 text-gray-400" />
            <span class="text-sm">Drafts</span>
          </button>
          <button @click="filters.status = 'Archived'; scrollTo('table')" class="flex items-center gap-3 p-3.5 bg-white border border-gray-100 text-gray-700 rounded-[14px] hover:border-gray-300 hover:bg-gray-50 transition-colors font-medium">
            <Archive class="w-5 h-5 shrink-0 text-gray-400" />
            <span class="text-sm">Archived</span>
          </button>
          <button @click="scrollTo('analytics')" class="flex items-center gap-3 p-3.5 bg-white border border-gray-100 text-gray-700 rounded-[14px] hover:border-[#2563EB] hover:bg-blue-50 hover:text-[#2563EB] transition-colors font-medium">
            <BarChart3 class="w-5 h-5 shrink-0 text-gray-400" />
            <span class="text-sm">Analytics</span>
          </button>
          <button @click="scrollTo('templates')" class="flex items-center gap-3 p-3.5 bg-white border border-gray-100 text-gray-700 rounded-[14px] hover:border-[#2563EB] hover:bg-blue-50 hover:text-[#2563EB] transition-colors font-medium">
            <Copy class="w-5 h-5 shrink-0 text-gray-400" />
            <span class="text-sm">Templates</span>
          </button>
        </section>

        <!-- Insights & Pinned Split -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <TrendingUp class="w-4 h-4 text-[#F59E0B]" /> Quick Insights
            </h2>
            <div class="grid grid-cols-2 gap-4">
              <div v-for="(insight, index) in quickInsights" :key="index" class="p-3 bg-gray-50 rounded-xl border border-gray-100">
                <p class="text-[10px] font-bold text-gray-500 uppercase tracking-wide mb-1">{{ insight.label }}</p>
                <p class="font-bold text-gray-900 text-sm leading-snug">{{ insight.value }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex flex-col">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <AlertTriangle class="w-4 h-4 text-[#EF4444]" /> Pinned & Critical
            </h2>
            <div class="flex-1 space-y-3">
              <p v-if="pinnedAnnouncements.length === 0" class="text-sm text-gray-400">Nothing pinned right now — pin an announcement from its details view.</p>
              <div v-for="pin in pinnedAnnouncements" :key="pin.id" class="p-3 bg-red-50 border border-red-100 rounded-xl flex items-center justify-between group">
                <div class="flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
                  <div>
                    <h4 class="font-bold text-red-900 text-sm">{{ pin.title }}</h4>
                    <p class="text-xs text-red-700 font-medium">{{ pin.audience }} • {{ pin.views }} views</p>
                  </div>
                </div>
                <button @click="openDrawerById(pin.id)" class="px-3 py-1.5 bg-white border border-red-200 text-red-600 text-xs font-bold rounded-lg hover:bg-red-600 hover:text-white transition-colors shadow-sm">
                  Manage
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Search & Filter Panel -->
        <section class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col xl:flex-row gap-4 items-center justify-between">
          <div class="w-full xl:w-[25%] relative">
            <Search class="w-5 h-5 text-gray-400 absolute left-3 top-3" />
            <input 
              v-model="filters.search" 
              type="text" 
              placeholder="Search title, category, author..." 
              class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
            />
          </div>
          <div class="w-full xl:w-[75%] flex flex-wrap xl:flex-nowrap gap-3 justify-end">
            <select v-model="filters.status" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="All">All Status</option>
              <option value="Published">Published</option>
              <option value="Scheduled">Scheduled</option>
              <option value="Draft">Draft</option>
              <option value="Archived">Archived</option>
            </select>
            <select v-model="filters.audience" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="All">All Audiences</option>
              <option value="All Users">All Users</option>
              <option value="Citizens">Citizens</option>
              <option value="Officers">Officers</option>
              <option value="Workers">Workers</option>
            </select>
            <select v-model="filters.priority" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="All">All Priorities</option>
              <option value="Emergency">Emergency</option>
              <option value="Critical">Critical</option>
              <option value="Important">Important</option>
              <option value="Normal">Normal</option>
            </select>
            <select v-model="filters.category" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="All">All Categories</option>
              <option value="Maintenance">Maintenance</option>
              <option value="Policy">Policy</option>
              <option value="Alert">Alert</option>
              <option value="Holiday">Holiday</option>
              <option value="General">General</option>
            </select>
            <select v-model="filters.sort" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="Newest">Newest First</option>
              <option value="Oldest">Oldest First</option>
              <option value="Views">Most Viewed</option>
            </select>
            <button @click="resetFilters" class="px-4 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors shrink-0 border border-transparent">
              Reset
            </button>
          </div>
        </section>

        <!-- Announcements Data Table (Desktop) -->
        <section id="table" class="hidden lg:block bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden mb-8">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-[11px] uppercase tracking-wider font-bold">
                  <th class="p-4 whitespace-nowrap">ID & Title</th>
                  <th class="p-4 whitespace-nowrap">Category</th>
                  <th class="p-4 whitespace-nowrap">Audience</th>
                  <th class="p-4 whitespace-nowrap text-center">Priority</th>
                  <th class="p-4 whitespace-nowrap text-center">Status</th>
                  <th class="p-4 whitespace-nowrap">Dates (Pub / Exp)</th>
                  <th class="p-4 whitespace-nowrap text-center">Views</th>
                  <th class="p-4 whitespace-nowrap text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm">
                <tr v-for="ann in filteredAnnouncements" :key="ann.id" class="hover:bg-gray-50 transition-colors group">
                  <td class="p-4">
                    <p class="font-bold text-gray-900">{{ ann.title }}</p>
                    <p class="text-xs text-gray-500">{{ ann.id }} • By {{ ann.author }}</p>
                  </td>
                  <td class="p-4 font-medium text-gray-700">{{ ann.category }}</td>
                  <td class="p-4">
                    <span :class="['px-2.5 py-1 rounded-md text-xs font-semibold', getAudienceBadge(ann.audience)]">
                      {{ ann.audience }}
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', getPriorityBadge(ann.priority)]">
                      {{ ann.priority }}
                    </span>
                  </td>
                  <td class="p-4 text-center">
                    <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide flex items-center justify-center gap-1.5 w-max mx-auto', getStatusBadge(ann.status)]">
                      <span class="w-1.5 h-1.5 rounded-full bg-current"></span> {{ ann.status }}
                    </span>
                  </td>
                  <td class="p-4 text-gray-600 text-xs whitespace-nowrap">
                    <p>{{ ann.publishDate }}</p>
                    <p class="text-gray-400">{{ ann.expiryDate }}</p>
                  </td>
                  <td class="p-4 text-center font-semibold text-gray-900">{{ ann.views }}</td>
                  <td class="p-4 text-right">
                    <div class="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click="openDrawer(ann)" class="p-1.5 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg" title="View"><Eye class="w-4 h-4" /></button>
                      <button @click="openModal('edit', ann)" class="p-1.5 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-lg" title="Edit"><Pencil class="w-4 h-4" /></button>
                      <button v-if="ann.status !== 'Published'" @click="quickPublish(ann)" class="p-1.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg" title="Publish"><Send class="w-4 h-4" /></button>
                      <button v-if="ann.status !== 'Archived'" @click="openModal('archive', ann)" class="p-1.5 text-gray-400 hover:text-yellow-600 hover:bg-yellow-50 rounded-lg" title="Archive"><Archive class="w-4 h-4" /></button>
                      <button @click="openModal('delete', ann)" class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg" title="Delete"><Trash2 class="w-4 h-4" /></button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredAnnouncements.length === 0">
                  <td colspan="8" class="p-8 text-center text-gray-500">No announcements match your filters.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Pagination Placeholder -->
          <div class="p-4 border-t border-gray-100 flex items-center justify-between text-sm text-gray-500 bg-gray-50/50">
            <span>Showing 1 to {{ filteredAnnouncements.length }} of {{ announcements.length }}</span>
            <div class="flex gap-1">
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50">Prev</button>
              <button class="px-3 py-1 border border-gray-200 bg-[#2563EB] text-white rounded-md">1</button>
              <button class="px-3 py-1 border border-gray-200 bg-white rounded-md hover:bg-gray-50">Next</button>
            </div>
          </div>
        </section>

        <!-- Mobile Announcement Cards -->
        <section class="lg:hidden space-y-4 mb-8">
          <div v-for="ann in filteredAnnouncements" :key="ann.id" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50">
            <div class="flex justify-between items-start mb-2">
              <h3 class="font-bold text-gray-900 leading-tight pr-2">{{ ann.title }}</h3>
              <span :class="['px-2 py-0.5 rounded-full text-[10px] font-bold uppercase shrink-0', getStatusBadge(ann.status)]">{{ ann.status }}</span>
            </div>
            <div class="flex flex-wrap gap-2 mb-3">
              <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', getPriorityBadge(ann.priority)]">{{ ann.priority }}</span>
              <span :class="['px-2 py-0.5 rounded text-[10px] font-semibold', getAudienceBadge(ann.audience)]">{{ ann.audience }}</span>
              <span class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-[10px] font-semibold">{{ ann.category }}</span>
            </div>
            <div class="text-xs text-gray-500 flex justify-between items-center mb-4">
              <span>Pub: {{ ann.publishDate }}</span>
              <span class="font-bold text-gray-900 flex items-center gap-1"><Eye class="w-3 h-3"/> {{ ann.views }}</span>
            </div>
            <div class="grid grid-cols-2 gap-2">
              <button @click="openDrawer(ann)" class="w-full py-2 bg-blue-50 text-[#2563EB] rounded-lg text-sm font-semibold hover:bg-blue-100 transition-colors">View</button>
              <button @click="openModal('edit', ann)" class="w-full py-2 bg-gray-50 text-gray-700 border border-gray-200 rounded-lg text-sm font-semibold hover:bg-gray-100 transition-colors">Edit</button>
            </div>
          </div>
        </section>

        <!-- Analytics Charts Grid -->
        <section id="analytics" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
             <h3 class="text-xs font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2"><LineChart class="w-4 h-4 text-[#2563EB]"/> Created by Month</h3>
             <div class="relative h-48 w-full"><canvas ref="viewsChartRef"></canvas></div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
             <h3 class="text-xs font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2"><PieChart class="w-4 h-4 text-[#2563EB]"/> Categories</h3>
             <div class="relative h-48 w-full flex justify-center"><canvas ref="categoryChartRef"></canvas></div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
             <h3 class="text-xs font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2"><BarChart3 class="w-4 h-4 text-[#2563EB]"/> Audience Spl.</h3>
             <div class="relative h-48 w-full"><canvas ref="audienceChartRef"></canvas></div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
             <h3 class="text-xs font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2"><PieChart class="w-4 h-4 text-[#2563EB]"/> Priority Dist.</h3>
             <div class="relative h-48 w-full flex justify-center"><canvas ref="priorityChartRef"></canvas></div>
          </div>
        </section>

        <!-- Bottom Grid: Activity, Templates -->
        <section class="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
          
          <!-- Recent Activity -->
          <div class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[400px]">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <Activity class="w-4 h-4 text-[#2563EB]" /> Recent Activity
            </h3>
            <div class="flex-1 overflow-y-auto custom-scrollbar">
              <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
                <p v-if="recentActivity.length === 0" class="text-sm text-gray-400 pl-5">No activity yet.</p>
                <div v-for="act in recentActivity" :key="act.id" class="relative pl-5">
                  <span :class="`absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 ${act.color}`"></span>
                  <div class="flex justify-between items-baseline mb-0.5">
                    <h4 class="text-xs font-bold text-gray-900">{{ act.action }}</h4>
                    <span class="text-[10px] text-gray-400 font-medium">{{ act.time }}</span>
                  </div>
                  <p class="text-[11px] text-gray-500">{{ act.desc }}</p>
                  <p class="text-[10px] text-[#2563EB] font-semibold mt-0.5">Admin: {{ act.admin }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Templates -->
          <div id="templates" class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[400px]">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <Copy class="w-4 h-4 text-[#2563EB]" /> Templates
            </h3>
            <div class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
              <div v-for="tpl in templates" :key="tpl.name" class="p-3 border border-gray-100 rounded-xl hover:border-[#2563EB] transition-colors group flex justify-between items-center">
                <div>
                  <h4 class="font-bold text-gray-900 text-sm group-hover:text-[#2563EB] transition-colors">{{ tpl.name }}</h4>
                  <p class="text-xs text-gray-500">{{ tpl.category }}</p>
                </div>
                <button @click="useTemplate(tpl)" class="px-3 py-1.5 bg-gray-50 border border-gray-200 text-gray-700 text-xs font-bold rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors">
                  Use
                </button>
              </div>
            </div>
          </div>

        </section>
        </template>
      </main>
    </div>

    <!-- Announcement Details Drawer -->
    <div v-if="isDrawerOpen && selectedAnn" class="fixed inset-0 z-50 overflow-hidden" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
      <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity" @click="closeDrawer"></div>
      <div class="fixed inset-y-0 right-0 max-w-lg w-full bg-white shadow-2xl flex flex-col transform transition-transform duration-300 ease-in-out border-l border-gray-100">
        
        <div class="p-6 border-b border-gray-100 bg-gray-50/50 flex justify-between items-start">
          <div class="pr-4">
             <div class="flex gap-2 mb-2">
               <span :class="['px-2 py-0.5 rounded-full text-[10px] font-bold uppercase', getStatusBadge(selectedAnn.status)]">{{ selectedAnn.status }}</span>
               <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', getPriorityBadge(selectedAnn.priority)]">{{ selectedAnn.priority }}</span>
             </div>
             <h2 class="text-xl font-bold text-gray-900 leading-tight">{{ selectedAnn.title }}</h2>
             <p class="text-xs text-gray-500 mt-1">{{ selectedAnn.id }} • Created by {{ selectedAnn.author }}</p>
          </div>
          <button @click="closeDrawer" class="p-2 text-gray-400 hover:bg-gray-200 rounded-full transition-colors shrink-0"><X class="w-5 h-5"/></button>
        </div>

        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-6">
          <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 grid grid-cols-2 gap-4 text-sm">
            <div><p class="text-xs text-gray-500 mb-0.5">Audience</p><p class="font-bold text-gray-900">{{ selectedAnn.audience }}</p></div>
            <div><p class="text-xs text-gray-500 mb-0.5">Category</p><p class="font-bold text-gray-900">{{ selectedAnn.category }}</p></div>
            <div><p class="text-xs text-gray-500 mb-0.5">Publish Date</p><p class="font-bold text-gray-900">{{ selectedAnn.publishDate }}</p></div>
            <div><p class="text-xs text-gray-500 mb-0.5">Expiry Date</p><p class="font-bold text-gray-900">{{ selectedAnn.expiryDate }}</p></div>
            <div class="col-span-2"><p class="text-xs text-gray-500 mb-0.5">Total Views</p><p class="font-bold text-[#2563EB] flex items-center gap-1"><Eye class="w-4 h-4"/> {{ selectedAnn.views }} Views</p></div>
          </div>

          <div v-if="selectedAnn.summary">
            <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Summary</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{{ selectedAnn.summary }}</p>
          </div>

          <div>
            <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Full Content</h3>
            <div class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">{{ selectedAnn.content }}</div>
          </div>
        </div>

        <div class="p-4 border-t border-gray-100 bg-white grid grid-cols-2 gap-3">
          <button @click="openModal('edit', selectedAnn)" class="py-2.5 bg-gray-50 border border-gray-200 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-100 flex items-center justify-center gap-2"><Pencil class="w-4 h-4"/> Edit</button>
          <button @click="togglePin(selectedAnn)" class="py-2.5 bg-purple-50 border border-purple-200 text-purple-700 text-sm font-semibold rounded-xl hover:bg-purple-100">{{ selectedAnn.isPinned ? 'Unpin' : 'Pin' }}</button>
          <button v-if="selectedAnn.status !== 'Published'" @click="quickPublish(selectedAnn)" class="py-2.5 bg-[#2563EB] text-white text-sm font-semibold rounded-xl hover:bg-[#1E40AF] shadow-sm">Publish</button>
          <button v-if="selectedAnn.status !== 'Archived'" @click="openModal('archive', selectedAnn)" class="py-2.5 bg-yellow-50 text-yellow-700 border border-yellow-200 text-sm font-semibold rounded-xl hover:bg-yellow-100">Archive</button>
          <button @click="openModal('delete', selectedAnn)" class="py-2.5 bg-red-50 text-red-600 border border-red-200 text-sm font-semibold rounded-xl hover:bg-red-100 col-span-2">Delete Permanently</button>
        </div>
      </div>
    </div>

    <!-- Modals Container -->
    <div v-if="activeModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
      
      <!-- 1. Create / Edit Modal -->
      <div v-if="activeModal === 'create' || activeModal === 'edit'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-2xl p-6 lg:p-8 transform transition-all max-h-[90vh] overflow-y-auto custom-scrollbar">
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ activeModal === 'create' ? 'Create Announcement' : 'Edit Announcement' }}</h2>
            <p class="text-sm text-gray-500 mt-1">Broadcast information to users across the platform.</p>
          </div>
          <button @click="closeModal" class="p-2 bg-gray-50 text-gray-500 rounded-full hover:bg-gray-100 transition-colors"><X class="w-5 h-5"/></button>
        </div>
        
        <form @submit.prevent="submitPublishOrSave" class="space-y-5">
          <div v-if="formError" class="p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">{{ formError }}</div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Announcement Title</label>
            <input v-model="form.title" type="text" required minlength="3" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none" placeholder="e.g. Scheduled Maintenance for Sector 4" />
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Category</label>
              <select v-model="form.category" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none">
                <option>Maintenance</option><option>Policy</option><option>Alert</option><option>Holiday</option><option>General</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Target Audience</label>
              <select v-model="form.audience" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none">
                <option>All Users</option><option>Citizens</option><option>Officers</option><option>Workers</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Priority</label>
              <select v-model="form.priority" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none">
                <option>Normal</option><option>Important</option><option>Critical</option><option>Emergency</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Short Summary <span class="text-gray-400 font-normal">(optional)</span></label>
            <textarea v-model="form.summary" rows="2" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none resize-none custom-scrollbar" placeholder="Brief summary visible on cards..."></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Full Description</label>
            <textarea v-model="form.content" required minlength="10" rows="5" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none resize-none custom-scrollbar" placeholder="Detailed content..."></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
             <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                Publish Date <span v-if="activeModal === 'edit'" class="text-gray-400 font-normal">(set via Publish button)</span>
                <span v-else class="text-gray-400 font-normal">(leave blank to publish immediately)</span>
              </label>
              <input v-model="form.publishAt" :disabled="activeModal === 'edit'" type="datetime-local" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none disabled:bg-gray-50 disabled:text-gray-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Expiry Date (Optional)</label>
              <input v-model="form.expiryAt" type="datetime-local" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none" />
            </div>
          </div>
          
          <div class="pt-6 flex justify-end gap-3 mt-4 border-t border-gray-100">
            <button type="button" @click="closeModal" class="px-6 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl transition-colors">Cancel</button>
            <button v-if="activeModal === 'create'" type="button" :disabled="isSubmitting" @click="submitDraft" class="px-6 py-2.5 text-sm font-bold text-[#2563EB] bg-blue-50 hover:bg-blue-100 border border-blue-100 rounded-xl transition-colors disabled:opacity-60">Save Draft</button>
            <button type="submit" :disabled="isSubmitting" class="px-6 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl transition-colors shadow-sm disabled:opacity-60">
              {{ activeModal === 'create' ? 'Publish / Schedule' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 2. Archive Confirm -->
      <div v-if="activeModal === 'archive'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center transform transition-all">
        <div class="w-16 h-16 bg-yellow-100 text-yellow-600 rounded-full flex items-center justify-center mx-auto mb-4"><Archive class="w-8 h-8"/></div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Archive Announcement?</h2>
        <p class="text-sm text-gray-500 mb-6">Archived announcements will no longer be visible to users but remain in the system records.</p>
        <div class="flex justify-center gap-3">
          <button @click="closeModal" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl">Cancel</button>
          <button @click="submitArchive" :disabled="isSubmitting" class="px-5 py-2.5 text-sm font-bold text-white bg-yellow-500 hover:bg-yellow-600 rounded-xl shadow-sm disabled:opacity-60">Archive</button>
        </div>
      </div>

      <!-- 3. Delete Confirm -->
      <div v-if="activeModal === 'delete'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center transform transition-all">
        <div class="w-16 h-16 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4"><Trash2 class="w-8 h-8"/></div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Delete Permanently?</h2>
        <p class="text-sm text-gray-500 mb-6">This announcement will be permanently removed. This action cannot be undone.</p>
        <div class="flex justify-center gap-3">
          <button @click="closeModal" class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-200 rounded-xl">Cancel</button>
          <button @click="submitDelete" :disabled="isSubmitting" class="px-5 py-2.5 text-sm font-bold text-white bg-red-600 hover:bg-red-700 rounded-xl shadow-sm disabled:opacity-60">Delete</button>
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
  Megaphone, Bell, MessageSquare, Newspaper, ClipboardList, Activity,
  Calendar, Clock, Users, ShieldAlert, AlertTriangle, FileText, 
  Search, Eye, Pencil, Trash2, Archive, Copy, Send, BarChart3, 
  PieChart, LineChart, TrendingUp, X, Download
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const router = useRouter();
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

// View State
const sidebarOpen = ref(false);
const isDrawerOpen = ref(false);
const activeModal = ref(null);
const selectedAnn = ref(null);
const targetAnn = ref(null);
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
const isLoading = ref(true);
const errorMessage = ref('');
const isSubmitting = ref(false);

// --- Live data — populated from GET /api/admin/announcements ---
const STAT_META = {
  total:       { label: 'Total Announcements', icon: Newspaper, colorClass: 'text-[#2563EB] bg-blue-100', textClass: 'text-[#2563EB]' },
  published:   { label: 'Published',   icon: Send,    colorClass: 'text-[#22C55E] bg-green-100',  textClass: 'text-[#22C55E]' },
  scheduled:   { label: 'Scheduled',   icon: Clock,   colorClass: 'text-[#F59E0B] bg-yellow-100', textClass: 'text-[#F59E0B]' },
  drafts:      { label: 'Drafts',      icon: FileText, colorClass: 'text-gray-600 bg-gray-100',   textClass: 'text-gray-600' },
  archived:    { label: 'Archived',    icon: Archive, colorClass: 'text-red-600 bg-red-100',      textClass: 'text-red-600' },
  total_views: { label: 'Total Views', icon: Eye,     colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
};
const STAT_ORDER = ['total', 'published', 'scheduled', 'drafts', 'archived', 'total_views'];

const topStats = ref([]);
const quickInsights = ref([]);
const pinnedAnnouncements = ref([]);
const announcements = ref([]);
const recentActivity = ref([]);
const categoryDist = ref({});
const audienceDist = ref({});
const priorityDist = ref({});
const monthlyCreated = ref([]);

// Quick-start presets — pre-fill the create form. These aren't stored
// anywhere (no template-storage model exists); they're just convenient
// starting points, not saved data.
const templates = ref([
  { name: 'Routine Maintenance Notice', category: 'Maintenance', priority: 'Normal', audience: 'All Users' },
  { name: 'Emergency Weather Alert', category: 'Alert', priority: 'Emergency', audience: 'All Users' },
  { name: 'Public Holiday Declaration', category: 'Holiday', priority: 'Normal', audience: 'All Users' },
  { name: 'Internal Policy Update', category: 'Policy', priority: 'Important', audience: 'Officers' },
]);

const fetchAnnouncements = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/announcements`, authHeaders());

    topStats.value = STAT_ORDER.map(key => ({ ...STAT_META[key], value: data.top_stats[key] }));
    quickInsights.value = data.quick_insights;
    pinnedAnnouncements.value = data.pinned;
    announcements.value = data.announcements;
    recentActivity.value = data.recent_activity.map(a => ({ ...a, color: 'border-[#2563EB]' }));
    categoryDist.value = data.category_distribution;
    audienceDist.value = data.audience_distribution;
    priorityDist.value = data.priority_distribution;
    monthlyCreated.value = data.monthly_created;

    renderCharts();
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    else errorMessage.value = err.response?.data?.message || 'Failed to load announcements.';
  } finally {
    isLoading.value = false;
  }
};

// --- Filters & Sorting ---
const filters = reactive({
  search: '', status: 'All', audience: 'All', priority: 'All', category: 'All', sort: 'Newest'
});

const filteredAnnouncements = computed(() => {
  let result = announcements.value;

  if (filters.search) {
    const q = filters.search.toLowerCase();
    result = result.filter(a => a.title.toLowerCase().includes(q) || a.category.toLowerCase().includes(q) || a.author.toLowerCase().includes(q));
  }
  if (filters.status !== 'All') result = result.filter(a => a.status === filters.status);
  if (filters.audience !== 'All') result = result.filter(a => a.audience === filters.audience);
  if (filters.priority !== 'All') result = result.filter(a => a.priority === filters.priority);
  if (filters.category !== 'All') result = result.filter(a => a.category === filters.category);

  result.sort((a, b) => {
    if (filters.sort === 'Views') return b.views - a.views;
    if (filters.sort === 'Oldest') return new Date(a.createdAt) - new Date(b.createdAt);
    return new Date(b.createdAt) - new Date(a.createdAt); // Newest
  });

  return result;
});

const resetFilters = () => {
  filters.search = ''; filters.status = 'All'; filters.audience = 'All'; 
  filters.priority = 'All'; filters.category = 'All'; filters.sort = 'Newest';
};

// --- UI Logic Helpers ---
const getStatusBadge = (status) => {
  switch(status) {
    case 'Published': return 'bg-green-100 text-green-700';
    case 'Scheduled': return 'bg-blue-100 text-blue-700';
    case 'Archived': return 'bg-yellow-100 text-yellow-700';
    default: return 'bg-gray-100 text-gray-600'; // Draft
  }
};
const getPriorityBadge = (priority) => {
  switch(priority) {
    case 'Emergency': return 'bg-red-100 text-red-700 border border-red-200';
    case 'Critical': return 'bg-red-50 text-red-600 border border-red-100';
    case 'Important': return 'bg-orange-50 text-orange-600 border border-orange-100';
    default: return 'bg-blue-50 text-blue-600 border border-blue-100';
  }
};
const getAudienceBadge = (audience) => {
  switch(audience) {
    case 'All Users': return 'bg-blue-100 text-blue-700';
    case 'Citizens': return 'bg-teal-100 text-teal-700';
    case 'Officers': return 'bg-purple-100 text-purple-700';
    case 'Workers': return 'bg-yellow-100 text-yellow-700';
    default: return 'bg-gray-100 text-gray-600';
  }
};

const scrollTo = (id) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });

// Modal / Drawer interactions
const openDrawer = (ann) => { selectedAnn.value = ann; isDrawerOpen.value = true; };
const closeDrawer = () => { isDrawerOpen.value = false; setTimeout(() => { selectedAnn.value = null; }, 300); };
const openDrawerById = (annId) => {
  const ann = announcements.value.find(a => a.id === annId);
  if (ann) openDrawer(ann);
};

const blankForm = () => ({ title: '', summary: '', content: '', category: 'General', priority: 'Normal', audience: 'All Users', publishAt: '', expiryAt: '' });
const form = reactive(blankForm());
const formError = ref('');

const resetForm = () => Object.assign(form, blankForm());

const openModal = (type, ann = null) => {
  activeModal.value = type;
  formError.value = '';
  if (ann) targetAnn.value = ann;
  if (type === 'edit' && ann) {
    Object.assign(form, {
      title: ann.title, summary: ann.summary || '', content: ann.content,
      category: ann.category, priority: ann.priority, audience: ann.audience,
      publishAt: '', expiryAt: ann.expiryAt ? toDatetimeLocal(ann.expiryAt) : '',
    });
  } else if (type === 'create') {
    resetForm();
  }
};
const closeModal = () => { activeModal.value = null; targetAnn.value = null; formError.value = ''; };
const handleActionClose = () => { closeModal(); closeDrawer(); };

const toDatetimeLocal = (dateStr) => {
  // dateStr here is the display-formatted date (e.g. 'Aug 06, 2026') — good enough
  // for a starting point in the expiry field; admin can adjust freely.
  const d = new Date(dateStr);
  if (isNaN(d)) return '';
  return d.toISOString().slice(0, 16);
};

const useTemplate = (tpl) => {
  resetForm();
  form.title = tpl.name;
  form.category = tpl.category;
  form.priority = tpl.priority;
  form.audience = tpl.audience;
  activeModal.value = 'create';
  formError.value = '';
};

// --- Backend-wired actions ---
const submitDraft = async () => {
  if (form.title.trim().length < 3) { formError.value = 'Title must be at least 3 characters.'; return; }
  if (form.content.trim().length < 10) { formError.value = 'Content must be at least 10 characters.'; return; }
  isSubmitting.value = true;
  try {
    await axios.post(`${API_BASE}/announcements`, { ...form, action: 'draft' }, authHeaders());
    closeModal();
    await fetchAnnouncements();
  } catch (err) {
    formError.value = err.response?.data?.message || 'Failed to save draft.';
  } finally {
    isSubmitting.value = false;
  }
};

const submitPublishOrSave = async () => {
  if (form.title.trim().length < 3) { formError.value = 'Title must be at least 3 characters.'; return; }
  if (form.content.trim().length < 10) { formError.value = 'Content must be at least 10 characters.'; return; }
  isSubmitting.value = true;
  try {
    if (activeModal.value === 'create') {
      await axios.post(`${API_BASE}/announcements`, { ...form, action: 'publish' }, authHeaders());
    } else {
      await axios.put(`${API_BASE}/announcements/${targetAnn.value.rawId}`, form, authHeaders());
    }
    closeModal();
    await fetchAnnouncements();
  } catch (err) {
    formError.value = err.response?.data?.message || 'Failed to save announcement.';
  } finally {
    isSubmitting.value = false;
  }
};

const quickPublish = async (ann) => {
  try {
    await axios.patch(`${API_BASE}/announcements/${ann.rawId}/publish`, {}, authHeaders());
    await fetchAnnouncements();
    if (selectedAnn.value?.rawId === ann.rawId) closeDrawer();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to publish.';
  }
};

const submitArchive = async () => {
  if (!targetAnn.value) return;
  isSubmitting.value = true;
  try {
    await axios.patch(`${API_BASE}/announcements/${targetAnn.value.rawId}/archive`, {}, authHeaders());
    handleActionClose();
    await fetchAnnouncements();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to archive.';
  } finally {
    isSubmitting.value = false;
  }
};

const submitDelete = async () => {
  if (!targetAnn.value) return;
  isSubmitting.value = true;
  try {
    await axios.delete(`${API_BASE}/announcements/${targetAnn.value.rawId}`, authHeaders());
    handleActionClose();
    await fetchAnnouncements();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to delete.';
  } finally {
    isSubmitting.value = false;
  }
};

const togglePin = async (ann) => {
  try {
    const { data } = await axios.patch(`${API_BASE}/announcements/${ann.rawId}/pin`, {}, authHeaders());
    if (selectedAnn.value?.rawId === ann.rawId) selectedAnn.value.isPinned = data.announcement.isPinned;
    await fetchAnnouncements();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to update pin.';
  }
};

// --- Charts Logic ---
const viewsChartRef = ref(null);
const categoryChartRef = ref(null);
const audienceChartRef = ref(null);
const priorityChartRef = ref(null);
let createdChart = null, categoryChart = null, audienceChart = null, priorityChart = null;

const renderCharts = () => {
  if (!viewsChartRef.value || !categoryChartRef.value || !audienceChartRef.value || !priorityChartRef.value) return;
  Chart.defaults.font.family = 'Inter, sans-serif';
  Chart.defaults.color = '#64748b';

  // 1. Line Chart — announcements created per month (real; there's no
  // recipient-facing view tracking yet to chart views by month instead)
  createdChart?.destroy();
  createdChart = new Chart(viewsChartRef.value, {
    type: 'line',
    data: {
      labels: monthlyCreated.value.map(m => m.month),
      datasets: [{ label: 'Announcements Created', data: monthlyCreated.value.map(m => m.count), borderColor: '#2563EB', backgroundColor: 'rgba(37, 99, 235, 0.1)', tension: 0.4, fill: true }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#F3F4F6' } }, x: { grid: { display: false } } } }
  });

  // 2. Pie Chart (Category)
  const catLabels = Object.keys(categoryDist.value);
  categoryChart?.destroy();
  categoryChart = new Chart(categoryChartRef.value, {
    type: 'pie',
    data: { labels: catLabels, datasets: [{ data: catLabels.map(l => categoryDist.value[l]), backgroundColor: ['#2563EB', '#1E40AF', '#EF4444', '#F59E0B', '#94A3B8'], borderWidth: 0 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } }
  });

  // 3. Bar Chart (Audience)
  const audLabels = Object.keys(audienceDist.value);
  audienceChart?.destroy();
  audienceChart = new Chart(audienceChartRef.value, {
    type: 'bar',
    data: { labels: audLabels, datasets: [{ label: 'Announcements', data: audLabels.map(l => audienceDist.value[l]), backgroundColor: '#3B82F6', borderRadius: 4 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#F3F4F6' } }, x: { grid: { display: false } } } }
  });

  // 4. Doughnut Chart (Priority)
  const prioLabels = Object.keys(priorityDist.value);
  priorityChart?.destroy();
  priorityChart = new Chart(priorityChartRef.value, {
    type: 'doughnut',
    data: { labels: prioLabels, datasets: [{ data: prioLabels.map(l => priorityDist.value[l]), backgroundColor: ['#EF4444', '#DC2626', '#F59E0B', '#3B82F6'], borderWidth: 0 }] },
    options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } }
  });
};

onMounted(fetchAnnouncements);
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
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>