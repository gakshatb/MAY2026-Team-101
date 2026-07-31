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
            <button class="flex items-center justify-center gap-2 px-4 py-2.5 bg-[#2563EB] hover:bg-[#1E40AF] text-white rounded-xl text-sm font-semibold transition-colors shadow-sm">
              <RefreshCw class="w-4 h-4" /> Transfer
            </button>
            <button class="flex items-center justify-center gap-2 px-4 py-2.5 bg-red-50 hover:bg-red-100 text-red-600 border border-red-100 rounded-xl text-sm font-semibold transition-colors">
              <UserX class="w-4 h-4" /> Suspend
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
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Gender / DOB</span><span class="font-medium text-gray-900">{{ personal.gender }} • {{ personal.dob }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Blood Group</span><span class="font-medium text-red-500">{{ personal.bloodGroup }}</span></li>
              <li class="flex flex-col border-b border-gray-50 pb-2">
                <span class="text-gray-500 mb-1">Address</span>
                <span class="font-medium text-gray-900">{{ personal.address }}, {{ personal.city }}, {{ personal.state }} - {{ personal.pin }}</span>
              </li>
              <li class="flex justify-between pt-1"><span class="text-gray-500">Emergency</span><span class="font-bold text-gray-900">{{ personal.emergency }}</span></li>
            </ul>
          </div>

          <!-- Department Information -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Building2 class="w-4 h-4 text-[#2563EB]" /> Department Details
            </h3>
            <ul class="space-y-3 text-sm mb-5">
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Current Dept</span><span class="font-bold text-[#2563EB]">{{ dept.name }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Dept Head</span><span class="font-medium text-gray-900">{{ dept.head }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Code & Since</span><span class="font-medium text-gray-900">{{ dept.code }} • {{ dept.since }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">HQ Location</span><span class="font-medium text-gray-900">{{ dept.location }}</span></li>
              <li class="flex justify-between pt-1"><span class="text-gray-500">Contact</span><span class="font-medium text-gray-900">{{ dept.contact }}</span></li>
            </ul>
            <button class="w-full py-2 bg-blue-50 text-[#2563EB] hover:bg-blue-100 rounded-lg text-sm font-semibold transition-colors">
              View Department Dashboard
            </button>
          </div>

          <!-- Security Information -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <ShieldCheck class="w-4 h-4 text-[#2563EB]" /> Security & Access
            </h3>
            <ul class="space-y-3 text-sm">
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Last Login</span><span class="font-medium text-gray-900">{{ security.lastLogin }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Last Pwd Change</span><span class="font-medium text-gray-900">{{ security.lastPwd }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">2FA Status</span><span :class="security.mfa ? 'text-green-600 font-bold' : 'text-red-500 font-bold'">{{ security.mfa ? 'Enabled' : 'Disabled' }}</span></li>
              <li class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Failed Logins</span><span class="font-medium text-gray-900">{{ security.failedLogins }}</span></li>
              <li class="flex justify-between pt-1"><span class="text-gray-500">Session Status</span><span class="font-bold text-green-600">Active</span></li>
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
                  <p class="text-lg font-bold text-yellow-700">{{ workerSummary.pendingApps }}</p>
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
                  <p class="font-bold text-[#2563EB] text-sm">March 2026</p>
                </div>
                <div class="p-3 bg-blue-50/50 rounded-xl">
                  <p class="text-xs text-gray-500 mb-0.5">Fastest Res.</p>
                  <p class="font-bold text-[#2563EB] text-sm">4h 12m (Pothole)</p>
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
                    <td class="p-4 text-gray-600">{{ comp.worker }}</td>
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

        <!-- Final Row: Feedback, Documents, Notifications -->
        <section class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
          
          <!-- Citizen Feedback -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <MessageSquare class="w-4 h-4 text-[#2563EB]" /> Citizen Feedback
            </h3>
            <div class="flex items-center gap-4 mb-5 p-4 bg-gray-50 rounded-xl border border-gray-100">
              <div class="text-3xl font-bold text-[#2563EB]">{{ feedbackSummary.rating }}</div>
              <div>
                <div class="flex text-yellow-400"><Star class="w-4 h-4 fill-current" v-for="i in 4" :key="i"/><StarHalf class="w-4 h-4 fill-current"/></div>
                <p class="text-xs text-gray-500 mt-1">Based on {{ feedbackSummary.totalReviews }} reviews</p>
              </div>
            </div>
            <div class="space-y-3">
              <div v-for="fb in recentFeedbacks" :key="fb.id" class="p-3 border border-gray-100 rounded-xl">
                <div class="flex justify-between items-start mb-1">
                  <p class="text-sm font-bold text-gray-900">{{ fb.name }}</p>
                  <span class="text-[10px] text-gray-400">{{ fb.date }}</span>
                </div>
                <p class="text-xs text-gray-600 line-clamp-2">"{{ fb.comment }}"</p>
              </div>
            </div>
          </div>

          <!-- Documents -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <FileText class="w-4 h-4 text-[#2563EB]" /> Official Documents
            </h3>
            <div class="space-y-3">
              <div v-for="doc in documents" :key="doc.id" class="flex items-center justify-between p-3 border border-gray-100 rounded-xl hover:border-[#2563EB] transition-colors group">
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-blue-50 text-[#2563EB] rounded-lg"><FileText class="w-4 h-4"/></div>
                  <div>
                    <p class="text-sm font-semibold text-gray-900">{{ doc.name }}</p>
                    <p class="text-[10px] text-gray-500">Uploaded: {{ doc.date }}</p>
                  </div>
                </div>
                <button class="p-2 text-gray-400 hover:text-[#2563EB] transition-colors"><Download class="w-4 h-4"/></button>
              </div>
            </div>
          </div>

          <!-- Notifications/Alerts -->
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Bell class="w-4 h-4 text-[#2563EB]" /> Recent Notifications
            </h3>
            <div class="space-y-3">
              <div v-for="noti in notifications" :key="noti.id" class="flex items-start gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                <div :class="`mt-0.5 w-2 h-2 rounded-full shrink-0 ${noti.color}`"></div>
                <div>
                  <p class="text-sm font-medium text-gray-900 leading-tight">{{ noti.title }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ noti.time }}</p>
                </div>
              </div>
            </div>
            <button class="w-full mt-4 py-2 text-[#2563EB] text-sm font-semibold hover:bg-blue-50 rounded-lg transition-colors">
              View All Alerts
            </button>
          </div>

        </section>
      </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';

// Icons
import { 
  BadgeCheck, Calendar, Mail, Phone, Pencil, RefreshCw, UserX, Key, 
  ClipboardList, CheckCircle, Clock, Users, Building2, User, 
  ShieldCheck, TrendingUp, Eye, Activity, FileText, Download, 
  Bell, MessageSquare, Star, StarHalf, Lightbulb
} from 'lucide-vue-next';

// View State
const sidebarOpen = ref(false);
const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

// --- Dummy Data ---
const officer = ref({
  name: 'Anita Patel',
  empId: 'OFC-1045',
  designation: 'Senior Civic Officer',
  department: 'Road Maintenance',
  email: 'anita.p@civicdesk.gov',
  phone: '+91 98765 11111',
  joinedDate: 'Jan 15, 2022',
  experience: '4+ Years',
  status: 'Active',
  avatar: 'https://i.pravatar.cc/150?img=5'
});

const topStats = ref([
  { label: 'Total Managed', value: '3,450', icon: ClipboardList, colorClass: 'text-[#2563EB] bg-blue-100', textClass: 'text-[#2563EB]' },
  { label: 'Resolved', value: '3,210', icon: CheckCircle, colorClass: 'text-[#22C55E] bg-green-100', textClass: 'text-[#22C55E]' },
  { label: 'Pending', value: '45', icon: Clock, colorClass: 'text-[#F59E0B] bg-yellow-100', textClass: 'text-[#F59E0B]' },
  { label: 'Avg Time', value: '24h', icon: Activity, colorClass: 'text-purple-600 bg-purple-100', textClass: 'text-purple-600' },
  { label: 'Satisfaction', value: '4.8/5', icon: Star, colorClass: 'text-yellow-500 bg-yellow-100', textClass: 'text-yellow-600' },
  { label: 'Workers', value: '42', icon: Users, colorClass: 'text-[#1E40AF] bg-indigo-100', textClass: 'text-[#1E40AF]' },
  { label: 'Dept Rank', value: '#2', icon: Building2, colorClass: 'text-pink-600 bg-pink-100', textClass: 'text-pink-600' },
  { label: 'Score', value: '95%', icon: TrendingUp, colorClass: 'text-[#22C55E] bg-green-100', textClass: 'text-[#22C55E]' }
]);

const personal = ref({
  name: 'Anita Suresh Patel', gender: 'Female', dob: '12 Aug 1988', bloodGroup: 'O+',
  address: 'Block A, Municipal Quarters', city: 'Pune', state: 'Maharashtra', pin: '411001',
  emergency: '+91 99887 77665 (Spouse)'
});

const dept = ref({
  name: 'Road Maintenance', head: 'Rajesh Verma (Director)', code: 'DEPT-RM',
  since: 'Oct 2023', location: 'Zone 4 HQ, Ground Floor', email: 'roads.zone4@civicdesk.gov',
  contact: '020-2553-1122'
});

const security = ref({
  lastLogin: 'Today, 09:14 AM (IP: 192.168.1.4)', lastPwd: 'Mar 01, 2026', mfa: true,
  failedLogins: '0 in last 30 days'
});

const workerSummary = ref({ assigned: 42, active: 38, pendingApps: 4, completed: 1845 });

const performanceBars = ref([
  { label: 'Complaint Resolution Rate', value: 95, color: 'bg-green-500' },
  { label: 'Task Assignment Speed', value: 88, color: 'bg-blue-500' },
  { label: 'Citizen Satisfaction', value: 92, color: 'bg-indigo-500' },
  { label: 'Department Contribution', value: 78, color: 'bg-yellow-500' }
]);

const recentComplaints = ref([
  { id: 'CMP-8842', category: 'Pothole Repair', priority: 'High', status: 'In Progress', worker: 'Rahul V.' },
  { id: 'CMP-8841', category: 'Road Cave-in', priority: 'Emergency', status: 'Assigned', worker: 'Amit S.' },
  { id: 'CMP-8830', category: 'Broken Pavement', priority: 'Medium', status: 'Resolved', worker: 'Pooja K.' },
  { id: 'CMP-8825', category: 'Waterlogging (Road)', priority: 'High', status: 'Resolved', worker: 'Rahul V.' }
]);

const adminActivities = ref([
  { id: 1, action: 'Profile Details Updated', date: 'Jun 15, 2026 - 14:30', admin: 'SysAdmin (Jane Doe)' },
  { id: 2, action: 'Transferred to Road Maint.', date: 'Oct 01, 2023 - 09:00', admin: 'SysAdmin (Jane Doe)' },
  { id: 3, action: 'Password Reset Forced', date: 'Jan 10, 2023 - 11:20', admin: 'Security Bot' },
  { id: 4, action: 'Officer Account Created', date: 'Jan 15, 2022 - 10:00', admin: 'SysAdmin (Jane Doe)' }
]);

const feedbackSummary = ref({ rating: '4.8', totalReviews: 842 });
const recentFeedbacks = ref([
  { id: 1, name: 'Suresh Raina', date: '2 days ago', comment: 'The pothole was fixed within 24 hours. Very prompt action by the officer and team.' },
  { id: 2, name: 'Kavita Sharma', date: '1 week ago', comment: 'Good work, but the debris was left on the side of the road for 2 days before clearing.' }
]);

const documents = ref([
  { id: 1, name: 'Employee_ID_Scan.pdf', date: 'Jan 15, 2022' },
  { id: 2, name: 'Appointment_Letter.pdf', date: 'Jan 10, 2022' },
  { id: 3, name: 'Transfer_Order_RM.pdf', date: 'Oct 01, 2023' }
]);

const notifications = ref([
  { id: 1, title: 'Worker application approved for Amit S.', time: '2 hours ago', color: 'bg-green-500' },
  { id: 2, title: 'Emergency complaint CMP-8841 received.', time: '5 hours ago', color: 'bg-red-500' },
  { id: 3, title: 'Monthly performance report generated.', time: 'Jul 01, 2026', color: 'bg-blue-500' }
]);

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

// --- Charts Logic ---
const doughnutChartRef = ref(null);
const lineChartRef = ref(null);

onMounted(() => {
  // Doughnut Chart (Complaint Stats)
  new Chart(doughnutChartRef.value, {
    type: 'doughnut',
    data: {
      labels: ['Resolved', 'In Progress', 'Assigned', 'Pending', 'Rejected'],
      datasets: [{
        data: [3210, 85, 110, 45, 12],
        backgroundColor: ['#22C55E', '#3B82F6', '#F59E0B', '#EF4444', '#94A3B8'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '65%',
      plugins: { legend: { position: 'right', labels: { boxWidth: 12, font: { size: 10 } } } }
    }
  });

  // Line Chart (Monthly Performance)
  new Chart(lineChartRef.value, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [
        {
          label: 'Complaints Managed',
          data: [210, 245, 180, 320, 290, 340],
          borderColor: '#2563EB',
          backgroundColor: 'rgba(37, 99, 235, 0.1)',
          tension: 0.4, fill: true,
        },
        {
          label: 'Resolution Rate (%)',
          data: [92, 94, 90, 95, 96, 95],
          borderColor: '#22C55E',
          borderDash: [5, 5],
          tension: 0.4, fill: false,
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: { 
        y: { beginAtZero: false, grid: { color: '#F3F4F6' } },
        x: { grid: { display: false } }
      }
    }
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