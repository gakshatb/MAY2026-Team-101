<template>
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">
      
      
      <!-- Scrollable Dashboard Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">
        
        <!-- Header & Breadcrumbs -->
        <header class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">System Analytics</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Platform Analytics</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Monitor platform performance, complaint trends, department productivity, and overall system health.
            </p>
          </div>
          <div class="flex flex-col items-end gap-1">
            <div class="bg-white px-4 py-2 rounded-xl shadow-sm border border-gray-100 flex items-center gap-2">
              <Calendar class="w-4 h-4 text-[#2563EB]" />
              <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
            </div>
            <span class="text-[10px] text-gray-400 font-medium">Last Updated: Just now</span>
          </div>
        </header>

        <!-- Error banner -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center justify-between">
          <span>{{ errorMessage }}</span>
          <button @click="fetchAnalytics" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="text-center text-gray-400 py-20">Loading analytics…</div>

        <template v-else-if="analytics">
        <!-- Analytics Filter Panel -->
        <section class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6">
          <div class="flex flex-col xl:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-2 text-gray-700 font-bold shrink-0">
              <Filter class="w-5 h-5 text-[#2563EB]" /> Global Filters
            </div>
            <div class="flex-1 grid grid-cols-2 md:grid-cols-4 xl:flex gap-3 w-full">
              <select class="form-select bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2 focus:ring-[#2563EB]/20 outline-none w-full xl:w-auto">
                <option>Last 30 Days</option>
                <option>This Quarter</option>
                <option>Year to Date</option>
              </select>
              <select class="form-select bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2 focus:ring-[#2563EB]/20 outline-none w-full xl:w-auto">
                <option>All Departments</option>
                <option>Garbage Management</option>
                <option>Road Maintenance</option>
              </select>
              <select class="form-select bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2 focus:ring-[#2563EB]/20 outline-none w-full xl:w-auto">
                <option>All Categories</option>
                <option>Infrastructure</option>
                <option>Utilities</option>
              </select>
              <select class="form-select bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2 focus:ring-[#2563EB]/20 outline-none w-full xl:w-auto">
                <option>All Statuses</option>
                <option>Pending</option>
                <option>Resolved</option>
              </select>
            </div>
            <div class="flex gap-2 shrink-0 w-full xl:w-auto">
              <button class="flex-1 xl:flex-none px-4 py-2 bg-[#2563EB] text-white text-sm font-semibold rounded-xl hover:bg-[#1E40AF] transition-colors shadow-sm">Apply</button>
              <button class="flex-1 xl:flex-none px-4 py-2 bg-gray-50 text-gray-600 text-sm font-semibold border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Reset</button>
            </div>
          </div>
        </section>

        <!-- Top KPI Cards -->
        <section class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-8 gap-4 mb-8">
          <div v-for="kpi in kpis" :key="kpi.key" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50 flex flex-col group hover:shadow-md transition-all">
            <div class="flex justify-between items-start mb-2">
              <div :class="`p-2 rounded-lg ${kpi.colorClass} group-hover:scale-110 transition-transform`">
                <component :is="kpi.icon" class="w-4 h-4" :class="kpi.textClass" />
              </div>
              <span v-if="kpi.hasTrend" :class="['text-[10px] font-bold px-1.5 py-0.5 rounded flex items-center gap-0.5', kpi.trend >= 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600']">
                <TrendingUp v-if="kpi.trend >= 0" class="w-3 h-3" />
                <TrendingDown v-else class="w-3 h-3" />
                {{ Math.abs(kpi.trend) }}%
              </span>
            </div>
            <h3 class="text-xl font-bold text-gray-900 leading-tight mb-1">{{ kpi.value }}</h3>
            <span class="text-[10px] text-gray-500 font-semibold uppercase tracking-wide truncate">{{ kpi.label }}</span>
          </div>
        </section>

        <!-- Quick Actions & Insights Split -->
        <div class="grid grid-cols-1 xl:grid-cols-4 gap-6 mb-8">
          
          <!-- Quick Insights -->
          <section class="xl:col-span-1 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex flex-col">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Activity class="w-4 h-4 text-[#F59E0B]" /> Platform Insights
            </h2>
            <div class="flex-1 space-y-3">
              <div v-for="(insight, index) in insights" :key="index" class="p-3 bg-gray-50 rounded-xl border border-gray-100 flex justify-between items-center">
                <div>
                  <p class="text-[10px] font-bold text-gray-500 uppercase tracking-wide">{{ insight.label }}</p>
                  <p class="font-bold text-[#2563EB] text-sm mt-0.5">{{ insight.value }}</p>
                </div>
                <component :is="insight.icon" class="w-5 h-5 text-gray-400" />
              </div>
            </div>
          </section>

          <!-- Emergency Analytics & Announcements -->
          <section class="xl:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
             <div class="bg-red-50 p-6 rounded-[14px] border border-red-100">
                <h2 class="text-sm font-bold text-red-700 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <AlertTriangle class="w-4 h-4" /> Emergency Handling
                </h2>
                <div class="grid grid-cols-2 gap-4 mb-4">
                  <div><p class="text-xs text-red-600 font-semibold">Total Emergencies</p><p class="text-2xl font-bold text-red-700">{{ emergency.total }}</p></div>
                  <div><p class="text-xs text-red-600 font-semibold">Avg Response</p><p class="text-2xl font-bold text-red-700">{{ emergency.avg_response_minutes }}m</p></div>
                  <div><p class="text-xs text-green-700 font-semibold">Resolved</p><p class="text-lg font-bold text-green-700">{{ emergency.resolved }}</p></div>
                  <div><p class="text-xs text-red-600 font-semibold">Pending</p><p class="text-lg font-bold text-red-700">{{ emergency.pending }}</p></div>
                </div>
                <div class="pt-3 border-t border-red-200/50">
                  <p class="text-xs text-red-700 font-medium">Most Impacted:
                    <strong>{{ emergency.most_impacted_ward ? `Ward ${emergency.most_impacted_ward}` : 'None recorded' }}</strong>
                  </p>
                </div>
             </div>

             <div class="bg-[#2563EB] p-6 rounded-[14px] shadow-sm text-white relative overflow-hidden">
                <div class="absolute right-0 top-0 opacity-10">
                  <Bell class="w-32 h-32 transform translate-x-8 -translate-y-8" />
                </div>
                <h2 class="text-sm font-bold text-blue-100 uppercase tracking-wider mb-4 relative z-10 flex items-center gap-2">
                  <Bell class="w-4 h-4" /> Announcements Reach
                </h2>
                <div class="grid grid-cols-2 gap-4 relative z-10">
                  <div><p class="text-xs text-blue-200 font-medium">Published</p><p class="text-2xl font-bold">{{ announcementsReach.published_count }}</p></div>
                  <div><p class="text-xs text-blue-200 font-medium">Total Views</p><p class="text-2xl font-bold">{{ announcementsReach.total_views }}</p></div>
                </div>
             </div>
          </section>

          <!-- Quick Actions Grid -->
          <section class="xl:col-span-1 bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 flex flex-col justify-center gap-3">
             <button class="flex items-center gap-3 p-3 w-full bg-gray-50 border border-gray-100 hover:border-[#2563EB] rounded-xl text-left transition-colors group">
               <Download class="w-5 h-5 text-gray-400 group-hover:text-[#2563EB] shrink-0" />
               <div><p class="text-sm font-bold text-gray-900">Export Master Report</p><p class="text-[10px] text-gray-500">Download complete PDF</p></div>
             </button>
             <button @click="exportDepartmentCsv" class="flex items-center gap-3 p-3 w-full bg-gray-50 border border-gray-100 hover:border-[#22C55E] rounded-xl text-left transition-colors group">
               <FileSpreadsheet class="w-5 h-5 text-gray-400 group-hover:text-[#22C55E] shrink-0" />
               <div><p class="text-sm font-bold text-gray-900">Generate CSV</p><p class="text-[10px] text-gray-500">Department analytics table</p></div>
             </button>
             <button class="flex items-center gap-3 p-3 w-full bg-gray-50 border border-gray-100 hover:border-[#F59E0B] rounded-xl text-left transition-colors group">
               <FileText class="w-5 h-5 text-gray-400 group-hover:text-[#F59E0B] shrink-0" />
               <div><p class="text-sm font-bold text-gray-900">Dept Performance</p><p class="text-[10px] text-gray-500">View standalone reports</p></div>
             </button>
          </section>

        </div>

        <!-- Charts Grid 1: Line & Bar -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <LineChart class="w-4 h-4 text-[#2563EB]" /> Platform Growth Trends
            </h2>
            <div class="relative h-72 w-full">
              <canvas ref="growthChartRef"></canvas>
            </div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <BarChart3 class="w-4 h-4 text-[#2563EB]" /> Complaints by Department
            </h2>
            <div class="relative h-72 w-full">
              <canvas ref="deptBarChartRef"></canvas>
            </div>
          </div>
        </section>

        <!-- Charts Grid 2: Pie, Doughnut, Radar -->
        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex justify-between items-center">
              <span class="flex items-center gap-2"><PieChart class="w-4 h-4 text-[#2563EB]" /> Category</span>
            </h2>
            <div class="relative h-64 w-full flex justify-center">
              <canvas ref="categoryPieChartRef"></canvas>
            </div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex justify-between items-center">
              <span class="flex items-center gap-2"><PieChart class="w-4 h-4 text-[#F59E0B]" /> Status</span>
            </h2>
            <div class="relative h-64 w-full flex justify-center">
              <canvas ref="statusDoughnutChartRef"></canvas>
            </div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex justify-between items-center">
              <span class="flex items-center gap-2"><Activity class="w-4 h-4 text-[#22C55E]" /> Dept Distribution</span>
            </h2>
            <div class="relative h-64 w-full flex justify-center">
              <canvas ref="radarChartRef"></canvas>
            </div>
          </div>
        </section>

        <!-- Department Performance Table -->
        <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden mb-8">
          <div class="p-5 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
              <Building2 class="w-4 h-4 text-[#2563EB]" /> Department Analytics
            </h2>
            <button @click="exportDepartmentCsv" class="text-xs font-bold text-[#2563EB] hover:underline">Export Table</button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse min-w-[800px]">
              <thead>
                <tr class="bg-white text-gray-500 text-[11px] uppercase tracking-wider font-bold border-b border-gray-100">
                  <th class="p-4 whitespace-nowrap">Department</th>
                  <th class="p-4 whitespace-nowrap text-center">Total Managed</th>
                  <th class="p-4 whitespace-nowrap text-center">Resolved / Pend.</th>
                  <th class="p-4 whitespace-nowrap text-center">Avg Time</th>
                  <th class="p-4 whitespace-nowrap text-center">Rating</th>
                  <th class="p-4 whitespace-nowrap text-center">Score</th>
                  <th class="p-4 whitespace-nowrap text-right">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50 text-sm">
                <tr v-for="dept in departmentAnalytics" :key="dept.name" class="hover:bg-gray-50 transition-colors">
                  <td class="p-4 font-bold text-gray-900">{{ dept.name }}</td>
                  <td class="p-4 text-center font-medium">{{ dept.total }}</td>
                  <td class="p-4 text-center">
                    <span class="text-green-600 font-semibold">{{ dept.resolved }}</span> / 
                    <span class="text-red-500 font-semibold">{{ dept.pending }}</span>
                  </td>
                  <td class="p-4 text-center text-gray-600 font-medium">{{ dept.avg_time_hours }}h</td>
                  <td class="p-4 text-center font-bold text-gray-900">{{ dept.rating ?? '—' }}</td>
                  <td class="p-4 text-center">
                    <span :class="['px-2 py-1 rounded-full text-xs font-bold', getScoreBg(dept.score)]">{{ dept.score }}%</span>
                  </td>
                  <td class="p-4 text-right">
                    <button class="text-[#2563EB] font-semibold text-xs hover:underline">View</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Top Performers (Officers & Workers) -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          
          <!-- Officers -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
             <div class="flex justify-between items-center mb-5">
               <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
                <UserCog class="w-4 h-4 text-[#2563EB]" /> Top 5 Officers
               </h2>
             </div>
             <div class="space-y-3">
                <div v-for="officer in topOfficers" :key="officer.name" class="flex items-center justify-between p-3 border border-gray-100 rounded-xl bg-gray-50 hover:bg-white hover:border-gray-200 transition-colors">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-blue-100 text-[#2563EB] flex items-center justify-center font-bold">{{ officer.name.charAt(0) }}</div>
                    <div>
                      <p class="font-bold text-gray-900 text-sm">{{ officer.name }}</p>
                      <p class="text-[10px] text-gray-500 font-medium uppercase">{{ officer.dept }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="font-bold text-[#2563EB] text-sm">{{ officer.score }}%</p>
                    <p class="text-[10px] text-gray-500 font-medium">{{ officer.managed }} Cmp • {{ officer.rating ?? '—' }}/5</p>
                  </div>
                </div>
             </div>
          </div>

          <!-- Workers -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
             <div class="flex justify-between items-center mb-5">
               <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
                <Users class="w-4 h-4 text-[#F59E0B]" /> Top 5 Workers
               </h2>
             </div>
             <div class="space-y-3">
                <div v-for="worker in topWorkers" :key="worker.name" class="flex items-center justify-between p-3 border border-gray-100 rounded-xl bg-gray-50 hover:bg-white hover:border-gray-200 transition-colors">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-yellow-100 text-[#F59E0B] flex items-center justify-center font-bold">{{ worker.name.charAt(0) }}</div>
                    <div>
                      <p class="font-bold text-gray-900 text-sm">{{ worker.name }}</p>
                      <p class="text-[10px] text-gray-500 font-medium uppercase">{{ worker.dept }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="font-bold text-[#22C55E] text-sm">{{ worker.completion_rate }}%</p>
                    <p class="text-[10px] text-gray-500 font-medium">{{ worker.tasks }} Tasks • {{ worker.avg_time_hours }}h Avg</p>
                  </div>
                </div>
             </div>
          </div>
        </section>

        <!-- Miscellaneous Row: Gauge, Horizontal Bar, Heatmap Placeholder -->
        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex flex-col items-center">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider w-full mb-4 flex items-center gap-2">
              <Gauge class="w-4 h-4 text-[#2563EB]" /> Citizen Satisfaction
            </h2>
            <div class="relative w-full h-40">
              <canvas ref="gaugeChartRef"></canvas>
              <div class="absolute inset-0 flex flex-col items-center justify-end pb-4 pointer-events-none">
                <span class="text-3xl font-bold text-gray-900">{{ satisfactionPct }}%</span>
                <span class="text-xs text-gray-500 font-medium">Overall Positive</span>
              </div>
            </div>
            <div class="flex justify-between w-full mt-4 text-xs font-bold text-gray-500 uppercase tracking-wide">
              <span>0%</span>
              <span>Target: 95%</span>
              <span>100%</span>
            </div>
          </div>

          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Clock class="w-4 h-4 text-[#F59E0B]" /> Avg Resolution Time
            </h2>
            <div class="relative h-48 w-full">
              <canvas ref="horizontalBarChartRef"></canvas>
            </div>
          </div>

          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex flex-col">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <MapPinned class="w-4 h-4 text-[#EF4444]" /> Complaint Density Map
            </h2>
            <div class="flex-1 bg-gray-100 rounded-xl border border-gray-200 flex flex-col items-center justify-center relative overflow-hidden">
               <!-- Dummy SVG Map Placeholder -->
               <svg class="w-full h-full text-gray-300 absolute inset-0 opacity-50" fill="currentColor" viewBox="0 0 100 100" preserveAspectRatio="none">
                 <path d="M10,20 Q30,10 50,30 T90,20 L90,80 Q70,90 50,70 T10,80 Z" />
                 <circle cx="30" cy="40" r="15" fill="#EF4444" opacity="0.3"/>
                 <circle cx="30" cy="40" r="5" fill="#EF4444" opacity="0.8"/>
                 <circle cx="70" cy="60" r="20" fill="#F59E0B" opacity="0.2"/>
                 <circle cx="70" cy="60" r="8" fill="#F59E0B" opacity="0.7"/>
               </svg>
               <div class="relative z-10 bg-white/90 backdrop-blur px-3 py-1.5 rounded-lg border border-gray-200 shadow-sm">
                 <span class="text-xs font-bold text-gray-700">Map Integration Pending</span>
               </div>
            </div>
          </div>
        </section>

        <!-- Bottom Grid: Timeline, Export -->
        <!-- System Health & Recent Reports were dropped here — there's no
             infra-monitoring or stored-report data source in this schema
             (see the note on dashboard()'s alerts: no fake infra metrics). -->
        <section class="grid grid-cols-1 xl:grid-cols-3 gap-6">

          <!-- Recent Platform Activity -->
          <div class="xl:col-span-2 bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[350px]">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <Activity class="w-4 h-4 text-[#2563EB]" /> Platform Activity
            </h2>
            <div v-if="!activityTimeline.length" class="flex-1 flex items-center justify-center text-sm text-gray-400">No recent activity.</div>
            <div v-else class="flex-1 overflow-y-auto custom-scrollbar pr-2">
              <div class="relative border-l-2 border-gray-100 ml-3 space-y-5">
                <div v-for="act in activityTimeline" :key="act.id" class="relative pl-5">
                  <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-[#2563EB]"></span>
                  <div class="flex justify-between items-baseline mb-0.5">
                    <h4 class="text-xs font-bold text-gray-900">{{ act.title }}</h4>
                    <span class="text-[10px] text-gray-400 font-medium">{{ timeAgo(act.created_at) }}</span>
                  </div>
                  <p class="text-[11px] text-gray-500">{{ act.description }}</p>
                  <p class="text-[10px] text-[#2563EB] font-semibold mt-0.5">User: {{ act.user }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Export -->
          <div class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 flex flex-col h-[350px] justify-center gap-3">
            <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-2 flex items-center gap-2">
              <FileSpreadsheet class="w-4 h-4 text-[#2563EB]" /> Export
            </h2>
            <button @click="exportDepartmentCsv" class="flex items-center gap-3 p-3 w-full bg-gray-50 border border-gray-100 hover:border-[#22C55E] rounded-xl text-left transition-colors group">
              <FileSpreadsheet class="w-5 h-5 text-gray-400 group-hover:text-[#22C55E] shrink-0" />
              <div><p class="text-sm font-bold text-gray-900">Department Analytics CSV</p><p class="text-[10px] text-gray-500">Generated from the current data on this page</p></div>
            </button>
          </div>

        </section>
        </template>
      </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

// Icons
import {
  BarChart3, PieChart, LineChart, TrendingUp, TrendingDown, Gauge,
  Building2, Users, UserCog, ClipboardList, Database, Server,
  ShieldCheck, Clock, Award, Activity, Bell, Calendar, Download,
  FileSpreadsheet, FileText, MapPinned, Filter, Search, RefreshCw, AlertTriangle
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

// View State
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
const isLoading = ref(true);
const errorMessage = ref('');
const analytics = ref(null);

// --- KPI display config (icons/colors stay client-side; values come from the API) ---
const KPI_META = {
  total_complaints:     { label: 'Total Complaints', icon: ClipboardList, colorClass: 'text-blue-600 bg-blue-100', textClass: 'text-blue-600' },
  open_complaints:      { label: 'Open Complaints', icon: Clock, colorClass: 'text-red-500 bg-red-100', textClass: 'text-red-500' },
  resolved_complaints:  { label: 'Resolved', icon: ShieldCheck, colorClass: 'text-green-600 bg-green-100', textClass: 'text-green-600' },
  total_citizens:       { label: 'Total Citizens', icon: Users, colorClass: 'text-indigo-600 bg-indigo-100', textClass: 'text-indigo-600' },
  total_officers:       { label: 'Total Officers', icon: UserCog, colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  total_workers:        { label: 'Total Workers', icon: Users, colorClass: 'text-yellow-600 bg-yellow-100', textClass: 'text-yellow-600' },
  departments:          { label: 'Departments', icon: Building2, colorClass: 'text-pink-600 bg-pink-100', textClass: 'text-pink-600' },
  avg_resolution_hours: { label: 'Avg Res Time (h)', icon: Clock, colorClass: 'text-teal-600 bg-teal-100', textClass: 'text-teal-600' },
};

const kpis = computed(() => {
  if (!analytics.value) return [];
  return Object.entries(analytics.value.kpis).map(([key, { value, trend_pct }]) => ({
    key, value, trend: trend_pct ?? 0, hasTrend: trend_pct !== null,
    ...KPI_META[key],
  }));
});

const insights = computed(() => {
  if (!analytics.value) return [];
  const i = analytics.value.insights;
  const fmtDept = (d) => d ? `${d.name}${d.rating != null ? ` (${d.rating})` : ''}` : 'Not enough data';
  const fmtFast = (d) => d ? `${d.name} (${d.avg_time_hours}h)` : 'Not enough data';
  return [
    { label: 'Most Active Dept', value: i.most_active_dept || 'Not enough data', icon: Building2 },
    { label: 'Highest Satisfaction', value: fmtDept(i.highest_satisfaction_dept), icon: Award },
    { label: 'Fastest Resolution', value: fmtFast(i.fastest_resolution_dept), icon: Clock },
    { label: 'Top Concern Area', value: i.top_concern_ward ? `Ward ${i.top_concern_ward}` : 'No emergencies logged', icon: AlertTriangle },
  ];
});

const emergency = computed(() => analytics.value?.emergency || { total: 0, resolved: 0, pending: 0, avg_response_minutes: 0, most_impacted_ward: null });
const announcementsReach = computed(() => analytics.value?.announcements_reach || { published_count: 0, total_views: 0 });
const departmentAnalytics = computed(() => analytics.value?.department_analytics || []);
const topOfficers = computed(() => analytics.value?.top_officers || []);
const topWorkers = computed(() => analytics.value?.top_workers || []);
const activityTimeline = computed(() => analytics.value?.activity_timeline || []);

// --- UI Helpers ---
const getScoreBg = (score) => {
  if (score >= 90) return 'bg-green-100 text-green-700';
  if (score >= 80) return 'bg-blue-100 text-blue-700';
  if (score >= 60) return 'bg-yellow-100 text-yellow-700';
  return 'bg-red-100 text-red-700';
};

const timeAgo = (iso) => {
  if (!iso) return '—';
  const diffMs = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins} min ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs} hr${hrs !== 1 ? 's' : ''} ago`;
  const days = Math.floor(hrs / 24);
  return days === 1 ? 'Yesterday' : `${days} days ago`;
};

// --- Export current department table as a real CSV (client-side, on demand) ---
const exportDepartmentCsv = () => {
  const rows = [['Department', 'Total', 'Resolved', 'Pending', 'Avg Time (h)', 'Rating', 'Score']];
  departmentAnalytics.value.forEach(d => {
    rows.push([d.name, d.total, d.resolved, d.pending, d.avg_time_hours, d.rating ?? '—', d.score]);
  });
  const csv = rows.map(r => r.join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `department_analytics_${new Date().toISOString().slice(0, 10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
};

// --- Chart Instances ---
const growthChartRef = ref(null);
const deptBarChartRef = ref(null);
const categoryPieChartRef = ref(null);
const statusDoughnutChartRef = ref(null);
const radarChartRef = ref(null);
const horizontalBarChartRef = ref(null);
const gaugeChartRef = ref(null);
let chartInstances = [];

const destroyCharts = () => {
  chartInstances.forEach(c => c.destroy());
  chartInstances = [];
};

const renderCharts = () => {
  const data = analytics.value;
  if (!data || !growthChartRef.value) return;
  destroyCharts();

  Chart.defaults.font.family = 'Inter, sans-serif';
  Chart.defaults.color = '#64748b';

  // 1. Growth Line Chart
  chartInstances.push(new Chart(growthChartRef.value, {
    type: 'line',
    data: {
      labels: data.growth_trend.labels,
      datasets: [
        { label: 'Complaints', data: data.growth_trend.complaints, borderColor: '#EF4444', tension: 0.4 },
        { label: 'Citizens', data: data.growth_trend.citizens, borderColor: '#2563EB', tension: 0.4 }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { grid: { color: '#F3F4F6' } }, x: { grid: { display: false } } } }
  }));

  // 2. Dept Bar Chart
  chartInstances.push(new Chart(deptBarChartRef.value, {
    type: 'bar',
    data: {
      labels: departmentAnalytics.value.map(d => d.name),
      datasets: [{ label: 'Total Complaints', data: departmentAnalytics.value.map(d => d.total), backgroundColor: '#2563EB', borderRadius: 4 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: '#F3F4F6' } }, x: { grid: { display: false } } } }
  }));

  // 3. Category Pie Chart
  const catLabels = Object.keys(data.category_breakdown);
  chartInstances.push(new Chart(categoryPieChartRef.value, {
    type: 'pie',
    data: {
      labels: catLabels,
      datasets: [{ data: Object.values(data.category_breakdown), backgroundColor: ['#2563EB', '#1E40AF', '#F59E0B', '#22C55E', '#94A3B8', '#EF4444', '#A855F7'], borderWidth: 0 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } }
  }));

  // 4. Status Doughnut Chart
  chartInstances.push(new Chart(statusDoughnutChartRef.value, {
    type: 'doughnut',
    data: {
      labels: Object.keys(data.status_breakdown),
      datasets: [{ data: Object.values(data.status_breakdown), backgroundColor: ['#22C55E', '#3B82F6', '#F59E0B', '#EF4444', '#64748b'], borderWidth: 0 }]
    },
    options: { responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } } } }
  }));

  // 5. Radar Chart
  chartInstances.push(new Chart(radarChartRef.value, {
    type: 'radar',
    data: {
      labels: departmentAnalytics.value.map(d => d.name),
      datasets: [
        { label: 'Total Handled', data: departmentAnalytics.value.map(d => d.total), backgroundColor: 'rgba(37, 99, 235, 0.2)', borderColor: '#2563EB', pointBackgroundColor: '#2563EB' },
        { label: 'Resolution Score', data: departmentAnalytics.value.map(d => d.score), backgroundColor: 'rgba(34, 197, 94, 0.2)', borderColor: '#22C55E', pointBackgroundColor: '#22C55E' }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { r: { ticks: { display: false } } }, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } } }
  }));

  // 6. Horizontal Bar (Resolution Time by Category)
  const resLabels = Object.keys(data.resolution_by_category);
  chartInstances.push(new Chart(horizontalBarChartRef.value, {
    type: 'bar',
    data: {
      labels: resLabels,
      datasets: [{ label: 'Avg Hours', data: Object.values(data.resolution_by_category), backgroundColor: '#F59E0B', borderRadius: 4 }]
    },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: '#F3F4F6' } }, y: { grid: { display: false } } } }
  }));

  // 7. Gauge Chart (Satisfaction) via Half-Doughnut
  const s = data.satisfaction;
  chartInstances.push(new Chart(gaugeChartRef.value, {
    type: 'doughnut',
    data: {
      labels: ['Satisfied', 'Neutral', 'Dissatisfied'],
      datasets: [{ data: [s.satisfied_pct, s.neutral_pct, s.dissatisfied_pct], backgroundColor: ['#22C55E', '#F59E0B', '#EF4444'], borderWidth: 0 }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      circumference: 180, rotation: -90, cutout: '80%',
      plugins: { legend: { display: false }, tooltip: { enabled: true } }
    }
  }));
};

const satisfactionPct = computed(() => analytics.value?.satisfaction?.satisfied_pct ?? 0);

const fetchAnalytics = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/analytics`, authHeaders());
    analytics.value = data;
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to load analytics.';
  } finally {
    isLoading.value = false;
  }

  // Wait for isLoading=false to actually flip the DOM to the v-else-if
  // block that holds the <canvas> elements — only then can Chart.js
  // acquire a real 2D context. Rendering charts from inside the try
  // block (before `finally`) was the bug: the canvases didn't exist
  // yet, Chart.js threw, and that throw was swallowed by the catch
  // above — showing "Failed to load analytics" even on a successful fetch.
  if (analytics.value) {
    await nextTick();
    renderCharts();
  }
};

onMounted(fetchAnalytics);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

/* Custom Scrollbars */
.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* Global Focus Override */
.form-select:focus { box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2); }

/* Entry Animation */
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
</style>