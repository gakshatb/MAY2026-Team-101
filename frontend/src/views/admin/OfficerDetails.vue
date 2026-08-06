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
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Officer Management</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">Officer Details</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Officer Details</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              View complete officer information, department assignments, performance, and administrative history.
            </p>
          </div>
          <div class="bg-white px-5 py-2.5 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-3">
            <Calendar class="w-5 h-5 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Error banner (only for real fetch failures, not the no-id picker state) -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center justify-between">
          <span>{{ errorMessage }}</span>
          <button @click="fetchOfficer" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- No officer selected: pick one from the roster instead of dead-ending -->
        <template v-else-if="!route.params.id">
          <div class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50 mb-6">
            <div class="relative">
              <Search class="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input v-model="pickerSearch" type="text" placeholder="Search officers by name, email, or department…"
                     class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-[#2563EB]/20 outline-none" />
            </div>
          </div>

          <div v-if="isPickerLoading" class="text-center text-gray-400 py-10">Loading officers…</div>

          <div v-else-if="filteredPickerOfficers.length" class="bg-white rounded-[14px] shadow-sm border border-gray-50 divide-y divide-gray-50">
            <button v-for="o in filteredPickerOfficers" :key="o.id" @click="router.push(`/admin/officerdetails/${o.id}`)"
                    class="w-full flex items-center gap-4 p-4 hover:bg-gray-50 transition-colors text-left">
              <img :src="o.avatar" :alt="o.name" class="w-11 h-11 rounded-full object-cover shrink-0" />
              <div class="flex-1 min-w-0">
                <p class="font-bold text-gray-900 truncate">{{ o.name }}</p>
                <p class="text-xs text-gray-500 truncate">{{ o.designation }} · {{ o.department }}</p>
              </div>
              <span :class="['text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded shrink-0',
                              o.status === 'Active' ? 'bg-green-100 text-green-700' : o.status === 'Suspended' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700']">
                {{ o.status }}
              </span>
              <Eye class="w-4 h-4 text-gray-300 shrink-0" />
            </button>
          </div>

          <div v-else class="text-center py-16 bg-white rounded-[14px] border border-gray-50">
            <p class="text-gray-400">No officers match "{{ pickerSearch }}".</p>
          </div>
        </template>

        <!-- Loading state -->
        <div v-else-if="isLoading" class="text-center text-gray-400 py-10">Loading officer details…</div>

        <template v-else-if="officer.id">
        <!-- Officer Profile Card (Hero Section) -->
        <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 p-6 lg:p-8 mb-6 relative overflow-hidden flex flex-col lg:flex-row gap-8 items-start lg:items-center justify-between">
          <div class="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
            <BadgeCheck class="w-48 h-48" />
          </div>
          
          <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6 relative z-10 w-full lg:w-auto text-center sm:text-left">
            <div class="relative">
              <img :src="officer.avatar" :alt="officer.name" class="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl object-cover border-4 border-gray-50 shadow-sm" />
              <div class="absolute -bottom-2 -right-2 w-8 h-8 bg-green-500 border-4 border-white rounded-full" title="Online"></div>
            </div>
            <div class="flex-1 space-y-1">
              <div class="flex flex-col sm:flex-row sm:items-center gap-3">
                <h2 class="text-2xl font-bold text-gray-900">{{ officer.name }}</h2>
                <span :class="['px-3 py-1 text-[11px] font-bold uppercase tracking-wider rounded-full w-max mx-auto sm:mx-0', getStatusBadge(officer.status)]">
                  {{ officer.status }}
                </span>
              </div>
              <p class="text-[#2563EB] font-semibold">{{ officer.designation }} • {{ officer.department }}</p>
              <div class="flex flex-wrap items-center justify-center sm:justify-start gap-y-2 gap-x-4 text-sm text-gray-500 mt-3">
                <span class="flex items-center gap-1.5"><BadgeCheck class="w-4 h-4 text-gray-400"/> {{ officer.empId }}</span>
                <span class="flex items-center gap-1.5"><Mail class="w-4 h-4 text-gray-400"/> {{ officer.email }}</span>
                <span class="flex items-center gap-1.5"><Phone class="w-4 h-4 text-gray-400"/> {{ officer.phone }}</span>
                <span class="flex items-center gap-1.5"><Calendar class="w-4 h-4 text-gray-400"/> Joined {{ officer.joinedDate }} ({{ officer.experience }})</span>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-2 gap-3 w-full lg:w-auto relative z-10 shrink-0">
            <button class="flex items-center justify-center gap-2 px-4 py-2.5 bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 rounded-xl text-sm font-semibold transition-colors">
              <Pencil class="w-4 h-4" /> Edit Profile
            </button>
            <button @click="goToTransfer" class="flex items-center justify-center gap-2 px-4 py-2.5 bg-[#2563EB] hover:bg-[#1E40AF] text-white rounded-xl text-sm font-semibold transition-colors shadow-sm">
              <RefreshCw class="w-4 h-4" /> Transfer
            </button>
            <button @click="toggleSuspension" :disabled="isSubmitting"
                    :class="officer.status === 'Active' ? 'bg-red-50 hover:bg-red-100 text-red-600 border-red-100' : 'bg-green-50 hover:bg-green-100 text-green-600 border-green-100'"
                    class="flex items-center justify-center gap-2 px-4 py-2.5 border rounded-xl text-sm font-semibold transition-colors disabled:opacity-60">
              <component :is="officer.status === 'Active' ? UserX : UserCheck" class="w-4 h-4" />
              {{ officer.status === 'Active' ? 'Suspend' : 'Reactivate' }}
            </button>
            <button class="flex items-center justify-center gap-2 px-4 py-2.5 bg-yellow-50 hover:bg-yellow-100 text-yellow-700 border border-yellow-100 rounded-xl text-sm font-semibold transition-colors">
              <Key class="w-4 h-4" /> Reset Access
            </button>
          </div>
        </section>

        <!-- Top Statistics Grid -->
        <section class="mb-6 grid grid-cols-2 sm:grid-cols-4 xl:grid-cols-8 gap-4">
          <div v-for="(stat, index) in topStats" :key="index" class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50 flex flex-col items-center text-center group hover:border-[#2563EB] transition-colors">
            <div :class="`p-2 rounded-lg bg-opacity-10 ${stat.colorClass} bg-current mb-2 group-hover:scale-110 transition-transform`">
              <component :is="stat.icon" class="w-5 h-5" :class="stat.textClass" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 leading-tight mb-0.5">{{ stat.value }}</h3>
            <span class="text-[11px] text-gray-500 font-medium uppercase tracking-wide">{{ stat.label }}</span>
          </div>
        </section>

        <!-- Charts Section (Doughnut & Line) -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div class="lg:col-span-1 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Complaint Statistics</h3>
            <div class="relative h-60 w-full flex justify-center">
              <canvas ref="doughnutChartRef"></canvas>
            </div>
          </div>
          <div class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Monthly Performance Trends</h3>
            <div class="relative h-60 w-full">
              <canvas ref="lineChartRef"></canvas>
            </div>
          </div>
        </section>

        <!-- 3-Column Split: Information, Department, Security -->
        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <!-- Officer Information -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <User class="w-4 h-4 text-[#2563EB]" /> Personal Details
            </h3>
            <ul class="space-y-3 text-sm">
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Full Name</span><span class="font-medium text-gray-900">{{ personal.name }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Gender</span><span class="font-medium text-gray-900">{{ personal.gender }}</span></li>
              <li class="flex flex-col pt-1">
                <span class="text-gray-500 mb-1">Address</span>
                <span class="font-medium text-gray-900">{{ personal.address }}<template v-if="personal.city">, {{ personal.city }}, {{ personal.state }} - {{ personal.pin }}</template></span>
              </li>
            </ul>
          </div>

          <!-- Department Information -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Building2 class="w-4 h-4 text-[#2563EB]" /> Department Details
            </h3>
            <ul class="space-y-3 text-sm mb-5">
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Current Dept</span><span class="font-bold text-[#2563EB]">{{ dept.name }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Dept Head</span><span class="font-medium text-gray-900">{{ dept.head || 'Unassigned' }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Code & Since</span><span class="font-medium text-gray-900">{{ dept.code }} • {{ dept.since }}</span></li>
              <li class="flex justify-between pt-1"><span class="text-gray-500">Status</span><span class="font-medium text-gray-900">{{ dept.status }}</span></li>
            </ul>
            <button @click="router.push('/admin/departmentmanagement')" class="w-full py-2 bg-blue-50 text-[#2563EB] hover:bg-blue-100 rounded-lg text-sm font-semibold transition-colors">
              View Department Dashboard
            </button>
          </div>

          <!-- Security Information -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <ShieldCheck class="w-4 h-4 text-[#2563EB]" /> Security & Access
            </h3>
            <ul class="space-y-3 text-sm">
              <li class="flex flex-col pt-1">
                <span class="text-gray-500 mb-1">Last Login</span>
                <span class="font-medium text-gray-900" v-if="lastLogin">{{ lastLogin.at }} <span class="text-gray-400 text-xs">(IP: {{ lastLogin.ip }})</span></span>
                <span class="font-medium text-gray-400" v-else>No login recorded yet</span>
              </li>
            </ul>
          </div>
        </section>

        <!-- 2-Column Split: Performance Bars & Worker Summary -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          
          <!-- Officer Performance -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-5 flex items-center gap-2">
              <TrendingUp class="w-4 h-4 text-[#2563EB]" /> Officer Performance
            </h3>
            <div class="space-y-5">
              <div v-for="(bar, index) in performanceBars" :key="index">
                <div class="flex justify-between text-sm mb-1.5">
                  <span class="font-medium text-gray-700">{{ bar.label }}</span>
                  <span class="font-bold text-gray-900">{{ bar.value }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-2">
                  <div :class="`h-2 rounded-full ${bar.color}`" :style="{ width: `${bar.value}%` }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Worker Management & Insights Split -->
          <div class="flex flex-col gap-6">
            
            <!-- Worker Summary -->
            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex-1">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-2">
                  <Users class="w-4 h-4 text-[#2563EB]" /> Worker Management
                </h3>
                <button class="text-[#2563EB] text-xs font-bold hover:underline">View All</button>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div class="p-3 bg-gray-50 border border-gray-100 rounded-xl text-center">
                  <p class="text-xs text-gray-500 mb-1">Assigned</p>
                  <p class="text-lg font-bold text-gray-900">{{ workerSummary.assigned }}</p>
                </div>
                <div class="p-3 bg-gray-50 border border-gray-100 rounded-xl text-center">
                  <p class="text-xs text-gray-500 mb-1">Active Now</p>
                  <p class="text-lg font-bold text-green-600">{{ workerSummary.active }}</p>
                </div>
                <div class="p-3 bg-gray-50 border border-gray-100 rounded-xl text-center">
                  <p class="text-xs text-gray-500 mb-1">Completed</p>
                  <p class="text-lg font-bold text-gray-900">{{ workerSummary.completed }}</p>
                </div>
                <div class="p-3 bg-yellow-50 border border-yellow-100 rounded-xl text-center">
                  <p class="text-xs text-yellow-700 mb-1">Pending App.</p>
                  <p class="text-lg font-bold text-yellow-700">{{ workerSummary.pending }}</p>
                </div>
              </div>
            </div>

            <!-- Quick Insights -->
            <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50 flex-1">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
                <Lightbulb class="w-4 h-4 text-[#2563EB]" /> Quick Insights
              </h3>
              <div class="grid grid-cols-2 gap-3">
                <div class="p-3 bg-blue-50/50 rounded-xl">
                  <p class="text-xs text-gray-500 mb-0.5">Best Month</p>
                  <p class="font-bold text-[#2563EB] text-sm">{{ quickInsights.bestMonth || 'N/A' }}</p>
                </div>
                <div class="p-3 bg-blue-50/50 rounded-xl">
                  <p class="text-xs text-gray-500 mb-0.5">Fastest Res.</p>
                  <p class="font-bold text-[#2563EB] text-sm">{{ quickInsights.fastestResolution || 'N/A' }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Complex Grid: Recent Complaints Table & Timelines -->
        <section class="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-6">
          
          <!-- Recent Complaint Activity (Table) -->
          <div class="xl:col-span-2 bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden flex flex-col">
            <div class="p-5 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider">Recent Complaint Activity</h3>
              <button class="text-sm text-[#2563EB] font-semibold hover:underline">View All</button>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-white text-gray-500 text-xs uppercase tracking-wider border-b border-gray-100">
                    <th class="p-4 font-semibold whitespace-nowrap">ID & Category</th>
                    <th class="p-4 font-semibold whitespace-nowrap">Priority</th>
                    <th class="p-4 font-semibold whitespace-nowrap">Status</th>
                    <th class="p-4 font-semibold whitespace-nowrap">Worker</th>
                    <th class="p-4 font-semibold whitespace-nowrap text-right">Action</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-50 text-sm">
                  <tr v-if="recentComplaints.length === 0"><td colspan="5" class="p-6 text-center text-gray-400">No complaints assigned yet.</td></tr>
                  <tr v-for="comp in recentComplaints" :key="comp.id" class="hover:bg-gray-50 transition-colors">
                    <td class="p-4">
                      <p class="font-bold text-gray-900">{{ comp.id }}</p>
                      <p class="text-xs text-gray-500">{{ comp.category }}</p>
                    </td>
                    <td class="p-4">
                      <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', getPriorityClass(comp.priority)]">
                        {{ comp.priority }}
                      </span>
                    </td>
                    <td class="p-4 text-gray-700 font-medium">{{ comp.status }}</td>
                    <td class="p-4 text-gray-600">{{ comp.worker || 'Unassigned' }}</td>
                    <td class="p-4 text-right">
                      <button class="p-1.5 text-gray-400 hover:text-[#2563EB] hover:bg-blue-50 rounded-lg transition-colors"><Eye class="w-4 h-4"/></button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Administrative Activities Timeline -->
          <div class="bg-white rounded-[14px] shadow-sm border border-gray-50 flex flex-col">
            <div class="p-5 border-b border-gray-100 bg-gray-50/50">
              <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider">Administrative History</h3>
            </div>
            <div class="p-6 flex-1 overflow-y-auto max-h-[400px] custom-scrollbar">
              <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
                <p v-if="adminActivities.length === 0" class="text-sm text-gray-400 pl-6">No administrative actions recorded yet.</p>
                <div v-for="act in adminActivities" :key="act.id" class="relative pl-6">
                  <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-[#2563EB]"></span>
                  <div class="flex justify-between items-baseline mb-0.5">
                    <h4 class="text-sm font-semibold text-gray-900">{{ act.action }}</h4>
                    <span class="text-[10px] text-gray-400 shrink-0">{{ act.date }}</span>
                  </div>
                  <p class="text-xs text-[#2563EB] font-medium mt-1">By: {{ act.admin }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Citizen Feedback -->
        <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <MessageSquare class="w-4 h-4 text-[#2563EB]" /> Citizen Feedback
            </h3>
            <div class="flex items-center gap-4 mb-5 p-4 bg-gray-50 rounded-xl border border-gray-100">
              <div class="text-3xl font-bold text-[#2563EB]">{{ feedbackSummary.rating ?? 'N/A' }}</div>
              <div>
                <div class="flex text-yellow-400"><Star class="w-4 h-4 fill-current" v-for="i in 4" :key="i"/><StarHalf class="w-4 h-4 fill-current"/></div>
                <p class="text-xs text-gray-500 mt-1">Based on {{ feedbackSummary.totalReviews }} reviews</p>
              </div>
            </div>
            <div class="space-y-3">
              <p v-if="recentFeedbacks.length === 0" class="text-sm text-gray-400">No feedback received yet.</p>
              <div v-for="(fb, i) in recentFeedbacks" :key="i" class="p-3 border border-gray-100 rounded-xl">
                <div class="flex justify-between items-start mb-1">
                  <p class="text-sm font-bold text-gray-900">{{ fb.name }}</p>
                  <span class="text-[10px] text-gray-400">{{ fb.date }}</span>
                </div>
                <p class="text-xs text-gray-600 line-clamp-2">"{{ fb.comment }}"</p>
              </div>
            </div>
          </div>
        </section>
        </template>
      </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import Chart from 'chart.js/auto';

// Icons
import { 
  BadgeCheck, Calendar, Mail, Phone, Pencil, RefreshCw, UserX, UserCheck, Key, 
  ClipboardList, CheckCircle, Clock, Users, Building2, User, 
  ShieldCheck, TrendingUp, Eye, Activity, Search,
  MessageSquare, Star, StarHalf, Lightbulb
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const route = useRoute();
const router = useRouter();
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

// View State
const sidebarOpen = ref(false);
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
const isLoading = ref(true);
const errorMessage = ref('');
const isSubmitting = ref(false);

// --- Live data — populated from GET /api/admin/officers/:id ---
const officer = ref({});
const topStats = ref([]);
const personal = ref({});
const dept = ref({});
const lastLogin = ref(null);
const workerSummary = ref({ total: 0, active: 0, completed: 0, pending: 0 });
const performanceBars = ref([]);
const recentComplaints = ref([]);
const adminActivities = ref([]);
const feedbackSummary = ref({ rating: null, totalReviews: 0 });
const recentFeedbacks = ref([]);
const quickInsights = ref({ bestMonth: null, fastestResolution: null });
const statusBreakdown = ref({});
const monthlyTrend = ref([]);

// --- Officer picker — shown when this page is opened with no :id ---
const isPickerLoading = ref(false);
const pickerSearch = ref('');
const pickerOfficers = ref([]);

const fetchPickerOfficers = async () => {
  isPickerLoading.value = true;
  try {
    const { data } = await axios.get(`${API_BASE}/officers`, authHeaders());
    pickerOfficers.value = data.officers;
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    else errorMessage.value = err.response?.data?.message || 'Failed to load officer list.';
  } finally {
    isPickerLoading.value = false;
  }
};

const filteredPickerOfficers = computed(() => {
  const q = pickerSearch.value.trim().toLowerCase();
  if (!q) return pickerOfficers.value;
  return pickerOfficers.value.filter(o =>
    o.name.toLowerCase().includes(q) ||
    o.email.toLowerCase().includes(q) ||
    (o.department || '').toLowerCase().includes(q)
  );
});

const STAT_META = {
  total_managed: { label: 'Total Managed', icon: ClipboardList, colorClass: 'text-[#2563EB] bg-blue-100', textClass: 'text-[#2563EB]' },
  resolved:      { label: 'Resolved',      icon: CheckCircle,   colorClass: 'text-[#22C55E] bg-green-100', textClass: 'text-[#22C55E]' },
  pending:       { label: 'Pending',       icon: Clock,         colorClass: 'text-[#F59E0B] bg-yellow-100', textClass: 'text-[#F59E0B]' },
  avg_time:      { label: 'Avg Time',      icon: Activity,      colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  satisfaction:  { label: 'Satisfaction',  icon: Star,          colorClass: 'text-yellow-500 bg-yellow-100', textClass: 'text-yellow-600' },
  workers:       { label: 'Workers',       icon: Users,         colorClass: 'text-[#1E40AF] bg-indigo-100', textClass: 'text-[#1E40AF]' },
  dept_rank:     { label: 'Dept Rank',     icon: Building2,     colorClass: 'text-pink-600 bg-pink-100', textClass: 'text-pink-600' },
  score:         { label: 'Score',         icon: TrendingUp,    colorClass: 'text-[#22C55E] bg-green-100', textClass: 'text-[#22C55E]' },
};

const fetchOfficer = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/officers/${route.params.id}`, authHeaders());

    officer.value = {
      ...data.officer,
      joinedDate: data.officer.joined,
    };

    topStats.value = [
      { ...STAT_META.total_managed, value: data.top_stats.total_managed },
      { ...STAT_META.resolved,      value: data.top_stats.resolved },
      { ...STAT_META.pending,       value: data.top_stats.pending },
      { ...STAT_META.avg_time,      value: data.top_stats.avg_time || 'N/A' },
      { ...STAT_META.satisfaction,  value: data.top_stats.satisfaction != null ? `${data.top_stats.satisfaction}/5` : 'N/A' },
      { ...STAT_META.workers,       value: data.worker_summary.total },
      { ...STAT_META.dept_rank,     value: data.top_stats.dept_rank ? `#${data.top_stats.dept_rank}` : 'N/A' },
      { ...STAT_META.score,         value: `${data.performance.resolution_rate}%` },
    ];

    personal.value = {
      name: data.officer.name,
      gender: data.officer.gender ? data.officer.gender.charAt(0).toUpperCase() + data.officer.gender.slice(1) : 'Not provided',
      address: data.officer.address || 'Not provided',
      city: data.officer.city || '',
      state: data.officer.state || '',
      pin: data.officer.pincode || '',
    };

    dept.value = data.department;
    lastLogin.value = data.last_login;

    workerSummary.value = {
      total: data.worker_summary.total,
      active: data.worker_summary.active,
      completed: data.worker_summary.completed,
      pending: data.worker_summary.pending,
    };

    performanceBars.value = [
      { label: 'Complaint Resolution Rate', value: data.performance.resolution_rate, color: 'bg-green-500' },
      ...(data.performance.citizen_satisfaction_pct != null
        ? [{ label: 'Citizen Satisfaction', value: data.performance.citizen_satisfaction_pct, color: 'bg-indigo-500' }]
        : []),
    ];

    recentComplaints.value = data.recent_complaints;
    adminActivities.value = data.admin_activities.map(a => ({
      id: a.id, action: a.action, date: a.date, admin: a.admin,
    }));

    feedbackSummary.value = { rating: data.feedback.avg_rating, totalReviews: data.feedback.total_reviews };
    recentFeedbacks.value = data.feedback.recent;

    quickInsights.value = {
      bestMonth: data.quick_insights.best_month,
      fastestResolution: data.quick_insights.fastest_resolution,
    };

    statusBreakdown.value = data.complaint_status_breakdown;
    monthlyTrend.value = data.monthly_trend;

    renderCharts();
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    else if (err.response?.status === 404) errorMessage.value = 'Officer not found.';
    else errorMessage.value = err.response?.data?.message || 'Failed to load officer details.';
  } finally {
    isLoading.value = false;
  }
};

// --- Suspend / Reactivate — same endpoints OfficerManagement.vue uses.
// Transfer is intentionally NOT duplicated here (it needs the full department
// picker built for OfficerManagement.vue); this page links there instead. ---
const toggleSuspension = async () => {
  if (!officer.value.id) return;
  const suspending = officer.value.status === 'Active';
  if (!window.confirm(suspending ? `Suspend ${officer.value.name}?` : `Reactivate ${officer.value.name}?`)) return;

  isSubmitting.value = true;
  try {
    const action = suspending ? 'suspend' : 'reactivate';
    await axios.patch(`${API_BASE}/officers/${officer.value.id}/${action}`, {}, authHeaders());
    await fetchOfficer();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Action failed.';
  } finally {
    isSubmitting.value = false;
  }
};

const goToTransfer = () => router.push('/admin/officermanagement');

// --- UI Helpers ---
const getStatusBadge = (status) => {
  return status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700';
};
const getPriorityClass = (priority) => {
  switch(priority) {
    case 'Emergency': return 'bg-red-100 text-red-700';
    case 'High': return 'bg-orange-100 text-orange-700';
    case 'Medium': return 'bg-yellow-100 text-yellow-700';
    default: return 'bg-blue-100 text-blue-700';
  }
};

// --- Charts — driven by the officer's real complaint data once it loads ---
const doughnutChartRef = ref(null);
const lineChartRef = ref(null);
let doughnutChart = null;
let lineChart = null;
const STATUS_COLORS = {
  'Resolved': '#22C55E', 'Closed': '#16A34A', 'In Progress': '#3B82F6',
  'Assigned': '#8B5CF6', 'Under Review': '#F59E0B', 'Pending': '#EF4444',
};

const renderCharts = () => {
  if (!doughnutChartRef.value || !lineChartRef.value) return;

  const labels = Object.keys(statusBreakdown.value);
  doughnutChart?.destroy();
  if (labels.length) {
    doughnutChart = new Chart(doughnutChartRef.value, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: labels.map(l => statusBreakdown.value[l]),
          backgroundColor: labels.map(l => STATUS_COLORS[l] || '#94A3B8'),
          borderWidth: 0, hoverOffset: 4,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: '65%',
        plugins: { legend: { position: 'right', labels: { boxWidth: 12, font: { size: 10 } } } }
      }
    });
  }

  lineChart?.destroy();
  lineChart = new Chart(lineChartRef.value, {
    type: 'line',
    data: {
      labels: monthlyTrend.value.map(m => m.month),
      datasets: [
        {
          label: 'Complaints Managed',
          data: monthlyTrend.value.map(m => m.managed),
          borderColor: '#2563EB', backgroundColor: 'rgba(37, 99, 235, 0.1)',
          tension: 0.4, fill: true,
        },
        {
          label: 'Resolution Rate (%)',
          data: monthlyTrend.value.map(m => m.resolution_rate),
          borderColor: '#22C55E', borderDash: [5, 5],
          tension: 0.4, fill: false,
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#F3F4F6' } },
        x: { grid: { display: false } }
      }
    }
  });
};

const loadForCurrentRoute = () => {
  errorMessage.value = '';
  if (!route.params.id) {
    isLoading.value = false;
    fetchPickerOfficers();
  } else {
    fetchOfficer();
  }
};

watch(() => route.params.id, loadForCurrentRoute);
onMounted(loadForCurrentRoute);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans { font-family: 'Inter', sans-serif; }

/* Custom Scrollbars */
.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* Line Clamp for Feedback */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animations */
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
</style>