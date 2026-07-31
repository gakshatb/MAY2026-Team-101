<template>
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">
      
      
      <!-- Scrollable Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">
        
        <!-- Header & Breadcrumbs -->
        <header class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2">
              <span class="hover:text-[#2563EB] cursor-pointer">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900 font-medium">Department Management</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Department Management</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Manage civic departments, assign department heads, and monitor departmental performance.
            </p>
          </div>
          <div class="bg-white px-5 py-2.5 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-3">
            <Calendar class="w-5 h-5 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Top Statistics Grid -->
        <section class="mb-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          <div v-for="(stat, index) in topStats" :key="index" class="bg-white p-5 rounded-[14px] shadow-sm hover:shadow-md transition-shadow border border-gray-50 flex flex-col group">
            <div class="flex items-center gap-3 mb-3">
              <div :class="`p-2.5 rounded-lg bg-opacity-10 ${stat.colorClass} bg-current group-hover:scale-110 transition-transform`">
                <component :is="stat.icon" class="w-5 h-5" :class="stat.textClass" />
              </div>
              <span class="text-sm text-gray-500 font-medium">{{ stat.label }}</span>
            </div>
            <h3 class="text-2xl font-bold text-gray-900">{{ stat.value }}</h3>
          </div>
        </section>

        <!-- Quick Actions & Insights -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <!-- Quick Actions -->
          <section class="lg:col-span-1 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Zap class="w-5 h-5 text-[#F59E0B]" /> Quick Actions
            </h2>
            <div class="grid grid-cols-2 gap-3">
              <button @click="openModal('add')" class="flex flex-col items-center justify-center p-4 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors">
                <Plus class="w-6 h-6 mb-2" />
                <span class="text-xs font-semibold text-center">Add Dept</span>
              </button>
              <button @click="openModal('assign')" class="flex flex-col items-center justify-center p-4 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors">
                <UserCog class="w-6 h-6 mb-2" />
                <span class="text-xs font-semibold text-center">Assign Head</span>
              </button>
              <button class="flex flex-col items-center justify-center p-4 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors">
                <BarChart3 class="w-6 h-6 mb-2" />
                <span class="text-xs font-semibold text-center">Analytics</span>
              </button>
              <button class="flex flex-col items-center justify-center p-4 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors">
                <ClipboardList class="w-6 h-6 mb-2" />
                <span class="text-xs font-semibold text-center">Reports</span>
              </button>
            </div>
          </section>

          <!-- Quick Insights -->
          <section class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Lightbulb class="w-5 h-5 text-[#F59E0B]" /> Quick Insights
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div v-for="(insight, index) in quickInsights" :key="index" class="p-4 rounded-xl border border-gray-100 flex justify-between items-center bg-gray-50/50">
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">{{ insight.label }}</p>
                  <p class="font-semibold text-gray-900">{{ insight.department }}</p>
                </div>
                <div class="text-right">
                  <span class="text-lg font-bold text-[#2563EB]">{{ insight.value }}</span>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Charts Section -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4">Complaints by Department</h2>
            <div class="relative h-64 w-full">
              <canvas ref="barChartRef"></canvas>
            </div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4">Performance Metrics</h2>
            <div class="relative h-64 w-full flex justify-center">
              <canvas ref="radarChartRef"></canvas>
            </div>
          </div>
        </section>

        <!-- Search & Filter Section -->
        <section class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div class="w-full md:w-1/3 relative">
            <Search class="w-5 h-5 text-gray-400 absolute left-3 top-3" />
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search departments, heads, IDs..." 
              class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
            />
          </div>
          <div class="w-full md:w-auto flex flex-wrap gap-3">
            <select v-model="filterStatus" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
              <option value="All">All Statuses</option>
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
              <option value="High Workload">High Workload</option>
            </select>
            <select v-model="sortBy" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20">
              <option value="Name">Sort by Name</option>
              <option value="Score">Sort by Performance</option>
              <option value="Complaints">Sort by Complaints</option>
            </select>
            <button @click="resetFilters" class="px-4 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">
              Reset
            </button>
          </div>
        </section>

        <!-- Department Table (Desktop) -->
        <section class="hidden md:block bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden mb-8">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="p-4 font-semibold whitespace-nowrap">ID & Department</th>
                  <th class="p-4 font-semibold whitespace-nowrap">Dept. Head</th>
                  <th class="p-4 font-semibold text-center whitespace-nowrap">Officers</th>
                  <th class="p-4 font-semibold text-center whitespace-nowrap">Complaints (P/R)</th>
                  <th class="p-4 font-semibold text-center whitespace-nowrap">Score</th>
                  <th class="p-4 font-semibold whitespace-nowrap">Status</th>
                  <th class="p-4 font-semibold text-right whitespace-nowrap">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm">
                <tr v-for="dept in sortedAndFilteredDepartments" :key="dept.id" class="hover:bg-gray-50 transition-colors">
                  <td class="p-4 font-medium text-gray-900">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0">
                        <Building2 class="w-5 h-5" />
                      </div>
                      <div>
                        <p class="font-bold">{{ dept.name }}</p>
                        <p class="text-xs text-gray-500">{{ dept.code }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="p-4 text-gray-700">{{ dept.head }}</td>
                  <td class="p-4 text-center text-gray-700">{{ dept.officers }}</td>
                  <td class="p-4 text-center">
                    <span class="text-red-500 font-medium">{{ dept.pending }}</span> / 
                    <span class="text-green-600 font-medium">{{ dept.resolved }}</span>
                  </td>
                  <td class="p-4 text-center">
                    <span :class="['px-2.5 py-1 rounded-full text-xs font-bold', getScoreClass(dept.score)]">
                      {{ dept.score }}%
                    </span>
                  </td>
                  <td class="p-4">
                    <span :class="['px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 w-max', getStatusClass(dept.status)]">
                      <span class="w-1.5 h-1.5 rounded-full bg-current"></span> {{ dept.status }}
                    </span>
                  </td>
                  <td class="p-4 text-right">
                    <div class="flex items-center justify-end gap-2">
                      <button @click="openDrawer(dept)" class="p-1.5 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors" title="View Details">
                        <Eye class="w-4 h-4" />
                      </button>
                      <button @click="openModal('edit', dept)" class="p-1.5 text-gray-400 hover:text-[#F59E0B] hover:bg-yellow-50 rounded-lg transition-colors" title="Edit">
                        <Pencil class="w-4 h-4" />
                      </button>
                      <button @click="openModal('delete', dept)" class="p-1.5 text-gray-400 hover:text-[#EF4444] hover:bg-red-50 rounded-lg transition-colors" title="Delete">
                        <Trash2 class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="sortedAndFilteredDepartments.length === 0">
                  <td colspan="7" class="p-8 text-center text-gray-500">No departments found matching your criteria.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Department Cards (Mobile only) -->
        <section class="md:hidden space-y-4 mb-8">
          <div v-for="dept in sortedAndFilteredDepartments" :key="dept.id" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50">
            <div class="flex justify-between items-start mb-3">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0">
                  <Building2 class="w-5 h-5" />
                </div>
                <div>
                  <h3 class="font-bold text-gray-900">{{ dept.name }}</h3>
                  <p class="text-xs text-gray-500">{{ dept.code }}</p>
                </div>
              </div>
              <span :class="['px-2 py-0.5 rounded-full text-[10px] font-semibold flex items-center gap-1', getStatusClass(dept.status)]">
                {{ dept.status }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm mb-4">
              <div class="bg-gray-50 p-2 rounded-lg">
                <p class="text-xs text-gray-500 mb-0.5">Head</p>
                <p class="font-medium text-gray-900 truncate">{{ dept.head }}</p>
              </div>
              <div class="bg-gray-50 p-2 rounded-lg">
                <p class="text-xs text-gray-500 mb-0.5">Score</p>
                <p :class="['font-bold', getScoreTextClass(dept.score)]">{{ dept.score }}%</p>
              </div>
              <div class="bg-gray-50 p-2 rounded-lg">
                <p class="text-xs text-gray-500 mb-0.5">Officers</p>
                <p class="font-medium text-gray-900">{{ dept.officers }}</p>
              </div>
              <div class="bg-gray-50 p-2 rounded-lg">
                <p class="text-xs text-gray-500 mb-0.5">Complaints</p>
                <p class="font-medium text-gray-900"><span class="text-red-500">{{ dept.pending }}</span> / {{ dept.resolved }}</p>
              </div>
            </div>
            <div class="flex gap-2">
              <button @click="openDrawer(dept)" class="flex-1 py-2 bg-blue-50 text-[#2563EB] rounded-lg text-sm font-medium hover:bg-blue-100 transition-colors">View</button>
              <button @click="openModal('edit', dept)" class="flex-1 py-2 bg-gray-50 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-100 transition-colors">Edit</button>
            </div>
          </div>
        </section>

        <!-- Bottom Grid: Performance Bars & Timeline -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          
          <!-- Department Performance Bars -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-5">Performance Breakdown</h2>
            <div class="space-y-5">
              <div v-for="dept in departments.slice(0, 5)" :key="dept.id">
                <div class="flex justify-between text-sm mb-1.5">
                  <span class="font-medium text-gray-700">{{ dept.name }}</span>
                  <span class="font-bold text-gray-900">{{ dept.score }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-2">
                  <div class="bg-[#2563EB] h-2 rounded-full" :style="{ width: `${dept.score}%` }"></div>
                </div>
              </div>
            </div>
          </section>

          <!-- Recent Activities Timeline -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6">
            <h2 class="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
              <Activity class="w-5 h-5 text-gray-400" /> Recent Activities
            </h2>
            <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
              <div v-for="activity in recentActivities" :key="activity.id" class="relative pl-6">
                <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-[#2563EB]"></span>
                <div class="flex justify-between items-baseline mb-0.5">
                  <h4 class="text-sm font-semibold text-gray-900">{{ activity.action }}</h4>
                  <span class="text-xs text-gray-400 shrink-0">{{ activity.date }}</span>
                </div>
                <p class="text-sm text-gray-500">{{ activity.description }}</p>
                <p class="text-xs text-[#2563EB] mt-1 font-medium">By {{ activity.admin }}</p>
              </div>
            </div>
          </section>
        </div>

      </main>
    </div>

    <!-- Department Details Drawer -->
    <div v-if="isDrawerOpen && selectedDept" class="fixed inset-0 z-50 overflow-hidden" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
      <div class="absolute inset-0 bg-slate-900/40 transition-opacity" @click="closeDrawer"></div>
      <div class="fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-2xl flex flex-col transform transition-transform duration-300 ease-in-out border-l border-gray-100">
        
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl bg-[#2563EB] text-white flex items-center justify-center">
              <Building2 class="w-6 h-6" />
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-900">{{ selectedDept.name }}</h2>
              <p class="text-sm text-gray-500">{{ selectedDept.code }}</p>
            </div>
          </div>
          <button @click="closeDrawer" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-6 custom-scrollbar space-y-6">
          
          <!-- Department Head Section -->
          <div>
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Department Head</h3>
            <div class="flex items-center gap-4 p-4 rounded-xl border border-gray-100 bg-white">
              <img :src="selectedDept.headAvatar" alt="Avatar" class="w-14 h-14 rounded-full object-cover border-2 border-gray-50" />
              <div>
                <p class="font-bold text-gray-900">{{ selectedDept.head }}</p>
                <p class="text-sm text-gray-500 flex items-center gap-1 mt-0.5"><Mail class="w-3 h-3"/> {{ selectedDept.headEmail }}</p>
                <p class="text-sm text-gray-500 flex items-center gap-1 mt-0.5"><Phone class="w-3 h-3"/> {{ selectedDept.headPhone }}</p>
              </div>
            </div>
          </div>

          <!-- Quick Stats -->
          <div>
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Department Metrics</h3>
            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 bg-gray-50 rounded-xl border border-gray-100 text-center">
                <p class="text-xs text-gray-500 mb-1">Assigned Officers</p>
                <p class="text-lg font-bold text-gray-900">{{ selectedDept.officers }}</p>
              </div>
              <div class="p-3 bg-gray-50 rounded-xl border border-gray-100 text-center">
                <p class="text-xs text-gray-500 mb-1">Field Workers</p>
                <p class="text-lg font-bold text-gray-900">{{ selectedDept.workers }}</p>
              </div>
              <div class="p-3 bg-red-50 rounded-xl border border-red-100 text-center">
                <p class="text-xs text-red-600 mb-1">Pending Complaints</p>
                <p class="text-lg font-bold text-red-700">{{ selectedDept.pending }}</p>
              </div>
              <div class="p-3 bg-green-50 rounded-xl border border-green-100 text-center">
                <p class="text-xs text-green-600 mb-1">Resolved (Total)</p>
                <p class="text-lg font-bold text-green-700">{{ selectedDept.resolved }}</p>
              </div>
            </div>
          </div>

          <!-- Additional Info -->
          <div>
             <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-3">Details</h3>
             <ul class="space-y-3 text-sm">
               <li class="flex justify-between border-b border-gray-100 pb-2">
                 <span class="text-gray-500">Status</span>
                 <span :class="['font-semibold', getStatusTextClass(selectedDept.status)]">{{ selectedDept.status }}</span>
               </li>
               <li class="flex justify-between border-b border-gray-100 pb-2">
                 <span class="text-gray-500">Performance Score</span>
                 <span class="font-bold text-gray-900">{{ selectedDept.score }}%</span>
               </li>
               <li class="flex justify-between border-b border-gray-100 pb-2">
                 <span class="text-gray-500">Avg Resolution Time</span>
                 <span class="font-medium text-gray-900">{{ selectedDept.avgTime }}</span>
               </li>
               <li class="flex justify-between border-b border-gray-100 pb-2">
                 <span class="text-gray-500">Created Date</span>
                 <span class="font-medium text-gray-900">{{ selectedDept.created }}</span>
               </li>
             </ul>
          </div>
        </div>

        <div class="p-4 border-t border-gray-100 bg-gray-50 grid grid-cols-2 gap-3">
          <button @click="openModal('edit', selectedDept)" class="py-2.5 bg-white border border-gray-200 text-gray-700 font-medium rounded-xl hover:bg-gray-50 transition-colors">
            Edit Details
          </button>
          <button @click="openModal('assign')" class="py-2.5 bg-[#2563EB] text-white font-medium rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm">
            Reassign Head
          </button>
        </div>
      </div>
    </div>

    <!-- Modals Overlay Container -->
    <div v-if="activeModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/50 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
      
      <!-- 1. Add/Edit Department Modal -->
      <div v-if="activeModal === 'add' || activeModal === 'edit'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 transform transition-all">
        <h2 class="text-xl font-bold text-gray-900 mb-4">{{ activeModal === 'add' ? 'Create New Department' : 'Edit Department' }}</h2>
        <form @submit.prevent="closeModal" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Department Name</label>
            <input type="text" class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none" placeholder="e.g. Garbage Management" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Department Code</label>
              <input type="text" class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none" placeholder="e.g. DEPT-GM" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none">
                <option>Active</option>
                <option>Inactive</option>
                <option>Under Maintenance</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea rows="3" class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] outline-none custom-scrollbar" placeholder="Brief description of responsibilities..."></textarea>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
            <button type="button" @click="closeModal" class="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
            <button type="submit" class="px-5 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl transition-colors shadow-sm">
              {{ activeModal === 'add' ? 'Create Department' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 2. Assign Head Modal -->
      <div v-if="activeModal === 'assign'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-md p-6 transform transition-all">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Assign Department Head</h2>
        <form @submit.prevent="closeModal" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Select Department</label>
            <select class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none">
              <option v-for="dept in departments" :key="dept.id">{{ dept.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Select Officer</label>
            <select class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none">
              <option>Anil Sharma (Current Head: Public Health)</option>
              <option>Priya Desai (Senior Officer)</option>
              <option>Rahul Verma (Officer)</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Effective Date</label>
            <input type="date" class="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#2563EB]/20 outline-none" />
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100">
            <button type="button" @click="closeModal" class="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
            <button type="submit" class="px-5 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-xl transition-colors shadow-sm">Assign Head</button>
          </div>
        </form>
      </div>

      <!-- 3. Delete Confirmation Modal -->
      <div v-if="activeModal === 'delete'" class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 text-center transform transition-all">
        <div class="w-16 h-16 bg-red-100 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <AlertTriangle class="w-8 h-8" />
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Delete Department?</h2>
        <p class="text-sm text-gray-500 mb-6">
          Are you sure you want to delete <strong class="text-gray-900">{{ targetDept?.name }}</strong>? 
          <br/><br/>
          <span class="text-red-500 font-medium bg-red-50 p-2 rounded block text-xs">Warning: Departments with active complaints or assigned officers cannot be deleted.</span>
        </p>
        <div class="flex justify-center gap-3">
          <button @click="closeModal" class="px-5 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-xl transition-colors">Cancel</button>
          <button @click="closeModal" class="px-5 py-2 text-sm font-medium text-white bg-[#EF4444] hover:bg-red-700 rounded-xl transition-colors shadow-sm">Delete</button>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Chart from 'chart.js/auto';

// Icons
import { 
  Building2, Users, UserCog, ClipboardList, BarChart3, 
  Calendar, Zap, Plus, Search, Eye, Pencil, Trash2, 
  X, Mail, Phone, AlertTriangle, Lightbulb, Activity, CheckCircle
} from 'lucide-vue-next';

// Layout State
const sidebarOpen = ref(false);
const isDrawerOpen = ref(false);
const selectedDept = ref(null);
const activeModal = ref(null);
const targetDept = ref(null);

const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

// Dummy Data
const topStats = ref([
  { label: 'Total Departments', value: '12', icon: Building2, colorClass: 'text-[#2563EB] bg-blue-100', textClass: 'text-[#2563EB]' },
  { label: 'Active Depts', value: '11', icon: CheckCircle, colorClass: 'text-[#22C55E] bg-green-100', textClass: 'text-[#22C55E]' },
  { label: 'Depts w/o Officers', value: '0', icon: AlertTriangle, colorClass: 'text-[#F59E0B] bg-yellow-100', textClass: 'text-[#F59E0B]' },
  { label: 'Active Complaints', value: '2,405', icon: ClipboardList, colorClass: 'text-[#EF4444] bg-red-100', textClass: 'text-[#EF4444]' },
  { label: 'Total Officers', value: '128', icon: Users, colorClass: 'text-[#1E40AF] bg-indigo-100', textClass: 'text-[#1E40AF]' },
  { label: 'Avg Resolution', value: '36h', icon: Activity, colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' }
]);

const quickInsights = ref([
  { label: 'Most Active', department: 'Garbage Management', value: '942 Cmp' },
  { label: 'Fastest Resolution', department: 'Street Lighting', value: '12h' },
  { label: 'Highest Rating', department: 'Parks & Gardens', value: '4.8/5' },
  { label: 'High Workload Alert', department: 'Drainage & Sewer', value: '312 Pnd' }
]);

const departments = ref([
  { id: 1, code: 'DEPT-GM', name: 'Garbage Management', head: 'Ramesh Singh', headEmail: 'ramesh.s@civicdesk.gov', headPhone: '+91 98765 43210', headAvatar: 'https://i.pravatar.cc/150?img=11', officers: 24, workers: 145, pending: 142, resolved: 3260, avgTime: '24h 15m', score: 92, status: 'Active', created: 'Jan 12, 2024' },
  { id: 2, code: 'DEPT-RM', name: 'Road Maintenance', head: 'Anita Patel', headEmail: 'anita.p@civicdesk.gov', headPhone: '+91 98765 43211', headAvatar: 'https://i.pravatar.cc/150?img=5', officers: 18, workers: 90, pending: 305, resolved: 1800, avgTime: '72h 40m', score: 78, status: 'High Workload', created: 'Feb 05, 2024' },
  { id: 3, code: 'DEPT-SL', name: 'Street Lighting', head: 'Vikram Joshi', headEmail: 'vikram.j@civicdesk.gov', headPhone: '+91 98765 43212', headAvatar: 'https://i.pravatar.cc/150?img=8', officers: 12, workers: 45, pending: 45, resolved: 1159, avgTime: '12h 10m', score: 98, status: 'Active', created: 'Mar 22, 2024' },
  { id: 4, code: 'DEPT-WS', name: 'Water Supply', head: 'Priya Desai', headEmail: 'priya.d@civicdesk.gov', headPhone: '+91 98765 43213', headAvatar: 'https://i.pravatar.cc/150?img=9', officers: 20, workers: 85, pending: 85, resolved: 1755, avgTime: '18h 20m', score: 95, status: 'Active', created: 'Apr 10, 2024' },
  { id: 5, code: 'DEPT-DS', name: 'Drainage & Sewer', head: 'Sanjay Kumar', headEmail: 'sanjay.k@civicdesk.gov', headPhone: '+91 98765 43214', headAvatar: 'https://i.pravatar.cc/150?img=12', officers: 15, workers: 110, pending: 210, resolved: 980, avgTime: '48h 00m', score: 82, status: 'High Workload', created: 'May 01, 2024' },
  { id: 6, code: 'DEPT-PG', name: 'Parks & Gardens', head: 'Meera Reddy', headEmail: 'meera.r@civicdesk.gov', headPhone: '+91 98765 43215', headAvatar: 'https://i.pravatar.cc/150?img=20', officers: 8, workers: 30, pending: 12, resolved: 420, avgTime: '20h 30m', score: 96, status: 'Active', created: 'Jun 15, 2024' },
  { id: 7, code: 'DEPT-BM', name: 'Building Maintenance', head: 'Unassigned', headEmail: 'N/A', headPhone: 'N/A', headAvatar: 'https://ui-avatars.com/api/?name=BM&background=random', officers: 0, workers: 0, pending: 0, resolved: 0, avgTime: 'N/A', score: 0, status: 'Inactive', created: 'Jul 09, 2026' }
]);

const recentActivities = ref([
  { id: 1, action: 'Department Head Assigned', description: 'Meera Reddy assigned to Parks & Gardens.', date: 'Today, 10:30 AM', admin: 'System Admin' },
  { id: 2, action: 'Department Created', description: 'Building Maintenance department was added to the system.', date: 'Yesterday, 04:15 PM', admin: 'System Admin' },
  { id: 3, action: 'Officer Transferred', description: '2 Officers transferred from Roads to Drainage.', date: 'Jul 08, 2026', admin: 'System Admin' },
  { id: 4, action: 'Status Updated', description: 'Road Maintenance changed to High Workload.', date: 'Jul 05, 2026', admin: 'System Auto' }
]);

// Search & Filter State
const searchQuery = ref('');
const filterStatus = ref('All');
const sortBy = ref('Name');

const sortedAndFilteredDepartments = computed(() => {
  let result = departments.value;

  // Filter by Search
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(d => 
      d.name.toLowerCase().includes(q) || 
      d.head.toLowerCase().includes(q) || 
      d.code.toLowerCase().includes(q)
    );
  }

  // Filter by Status
  if (filterStatus.value !== 'All') {
    result = result.filter(d => d.status === filterStatus.value);
  }

  // Sort
  result = [...result].sort((a, b) => {
    if (sortBy.value === 'Name') return a.name.localeCompare(b.name);
    if (sortBy.value === 'Score') return b.score - a.score;
    if (sortBy.value === 'Complaints') return (b.pending + b.resolved) - (a.pending + a.resolved);
    return 0;
  });

  return result;
});

const resetFilters = () => {
  searchQuery.value = '';
  filterStatus.value = 'All';
  sortBy.value = 'Name';
};

// UI Helpers
const getScoreClass = (score) => {
  if (score >= 90) return 'bg-green-100 text-green-700';
  if (score >= 80) return 'bg-yellow-100 text-yellow-700';
  if (score === 0) return 'bg-gray-100 text-gray-500';
  return 'bg-red-100 text-red-700';
};
const getScoreTextClass = (score) => {
  if (score >= 90) return 'text-green-600';
  if (score >= 80) return 'text-yellow-600';
  if (score === 0) return 'text-gray-400';
  return 'text-red-600';
};
const getStatusClass = (status) => {
  switch(status) {
    case 'Active': return 'bg-green-50 text-green-700 border border-green-200';
    case 'Inactive': return 'bg-gray-100 text-gray-600 border border-gray-300';
    case 'High Workload': return 'bg-red-50 text-red-600 border border-red-200';
    default: return 'bg-blue-50 text-blue-600';
  }
};
const getStatusTextClass = (status) => {
  if(status === 'Active') return 'text-green-600';
  if(status === 'Inactive') return 'text-gray-500';
  return 'text-red-600';
};

// Actions
const openDrawer = (dept) => {
  selectedDept.value = dept;
  isDrawerOpen.value = true;
};
const closeDrawer = () => {
  isDrawerOpen.value = false;
  setTimeout(() => { selectedDept.value = null; }, 300);
};

const openModal = (type, dept = null) => {
  activeModal.value = type;
  if(dept) targetDept.value = dept;
};
const closeModal = () => {
  activeModal.value = null;
  targetDept.value = null;
};

// Charts
const barChartRef = ref(null);
const radarChartRef = ref(null);

onMounted(() => {
  // Bar Chart: Complaints by Dept
  new Chart(barChartRef.value, {
    type: 'bar',
    data: {
      labels: ['Garbage', 'Roads', 'Lighting', 'Water', 'Drainage', 'Parks'],
      datasets: [
        {
          label: 'Resolved',
          data: [3260, 1800, 1159, 1755, 980, 420],
          backgroundColor: '#22C55E',
          borderRadius: 4,
        },
        {
          label: 'Pending',
          data: [142, 305, 45, 85, 210, 12],
          backgroundColor: '#EF4444',
          borderRadius: 4,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: { 
        x: { stacked: true, grid: { display: false } }, 
        y: { stacked: true, grid: { color: '#F3F4F6' } } 
      }
    }
  });

  // Radar Chart: Performance
  new Chart(radarChartRef.value, {
    type: 'radar',
    data: {
      labels: ['Speed', 'Quality', 'Satisfaction', 'Efficiency', 'Response'],
      datasets: [{
        label: 'Platform Average',
        data: [85, 90, 88, 82, 95],
        backgroundColor: 'rgba(37, 99, 235, 0.2)',
        borderColor: '#2563EB',
        pointBackgroundColor: '#2563EB',
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 40,
          max: 100,
          ticks: { display: false }
        }
      },
      plugins: { legend: { display: false } }
    }
  });
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

/* Custom Scrollbars */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #CBD5E1;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94A3B8;
}

/* Page Entry Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
</style>