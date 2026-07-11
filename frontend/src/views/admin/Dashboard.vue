<template>
  <div class="flex h-screen overflow-hidden bg-[#F8FAFC]">
    
    <!-- Mobile Sidebar Backdrop -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 bg-slate-900/50 z-40 lg:hidden transition-opacity" 
      @click="sidebarOpen = false"
      aria-hidden="true"
    ></div>

    <!-- Sidebar Wrapper -->
    <div 
      :class="[
        'fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 lg:relative lg:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <Sidebar userRole="Administrator" />
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">
      
      <!-- Top Navbar -->
      <DashboardNavbar 
        userRole="System Administrator" 
        pageTitle="Admin Dashboard" 
        @toggle-sidebar="sidebarOpen = !sidebarOpen" 
      />
      
      <!-- Scrollable Dashboard Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 font-sans animate-fade-in custom-scrollbar">
        
        <!-- Welcome Header -->
        <header class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight flex items-center gap-2">
              Good Morning, System Administrator
            </h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Monitor platform performance, manage departments, and oversee system operations.
            </p>
          </div>
          <div class="text-right flex flex-col items-start md:items-end bg-white px-5 py-3 rounded-[14px] shadow-sm border border-gray-100">
            <span class="text-sm font-medium text-gray-500 uppercase tracking-wider">{{ currentDate }}</span>
            <span class="text-2xl font-bold text-[#2563EB]">{{ currentTime }}</span>
          </div>
        </header>

        <!-- Top Statistics Grid -->
        <section class="mb-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-4" aria-label="System Statistics">
          <div 
            v-for="(stat, index) in topStats" 
            :key="index"
            class="bg-white p-5 rounded-[14px] shadow-sm hover:shadow-md transition-all duration-300 border border-gray-50 group flex flex-col"
          >
            <div class="flex justify-between items-start mb-4">
              <div :class="`p-3 rounded-xl bg-opacity-10 ${stat.colorClass} bg-current group-hover:scale-110 transition-transform duration-300`">
                <component :is="stat.icon" class="w-6 h-6" :class="stat.textClass" />
              </div>
              <span :class="['text-xs font-semibold px-2 py-1 rounded-full', stat.trendUp ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
                {{ stat.trend }}
              </span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 mb-1">{{ stat.value }}</h3>
            <p class="text-sm text-gray-500 font-medium">{{ stat.label }}</p>
          </div>
        </section>

        <!-- System Health & Quick Actions -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          
          <!-- System Health -->
          <section class="lg:col-span-2 bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
              <Activity class="w-5 h-5 text-[#2563EB]" /> System Health
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div v-for="(health, index) in systemHealth" :key="index" class="p-4 rounded-xl border border-gray-100 flex items-center gap-4">
                <div :class="['w-3 h-3 rounded-full shadow-sm', health.statusColor]"></div>
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider">{{ health.label }}</p>
                  <p class="font-semibold text-gray-900">{{ health.value }}</p>
                </div>
              </div>
            </div>
          </section>

          <!-- Quick Actions -->
          <section class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
              <Zap class="w-5 h-5 text-[#F59E0B]" /> Quick Actions
            </h2>
            <div class="grid grid-cols-2 gap-3">
              <button 
                v-for="(action, index) in quickActions" 
                :key="index"
                class="flex flex-col items-center justify-center p-4 rounded-xl border border-gray-100 hover:border-[#2563EB] hover:bg-blue-50 text-gray-700 hover:text-[#2563EB] transition-colors duration-200"
              >
                <component :is="action.icon" class="w-6 h-6 mb-2" />
                <span class="text-xs font-semibold text-center">{{ action.label }}</span>
              </button>
            </div>
          </section>
        </div>

        <!-- Charts Overview -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4">Monthly User Growth</h2>
            <div class="relative h-64 w-full">
              <canvas ref="growthChartRef"></canvas>
            </div>
          </div>
          <div class="bg-white p-6 rounded-[14px] shadow-sm border border-gray-50">
            <h2 class="text-lg font-bold text-gray-900 mb-4">Complaint Category Distribution</h2>
            <div class="relative h-64 w-full flex justify-center">
              <canvas ref="categoryChartRef"></canvas>
            </div>
          </div>
        </section>

        <!-- Complex Data Tables Section -->
        <div class="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-8">
          
          <!-- Department Performance -->
          <section class="xl:col-span-2 bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden">
            <div class="p-6 border-b border-gray-100 flex justify-between items-center">
              <h2 class="text-lg font-bold text-gray-900">Department Performance</h2>
              <button class="text-sm text-[#2563EB] font-medium hover:underline">View All</button>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse min-w-[600px]">
                <thead>
                  <tr class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
                    <th class="p-4 font-semibold whitespace-nowrap">Department</th>
                    <th class="p-4 font-semibold text-center whitespace-nowrap">Complaints (Total/Pending)</th>
                    <th class="p-4 font-semibold text-center whitespace-nowrap">Avg. Resolution</th>
                    <th class="p-4 font-semibold text-center whitespace-nowrap">Score</th>
                    <th class="p-4 font-semibold text-right whitespace-nowrap">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 text-sm">
                  <tr v-for="dept in departmentPerformance" :key="dept.id" class="hover:bg-gray-50 transition-colors">
                    <td class="p-4 font-medium text-gray-900 flex items-center gap-3 whitespace-nowrap">
                      <div class="w-8 h-8 rounded bg-blue-100 text-blue-600 flex items-center justify-center shrink-0">
                        <Building2 class="w-4 h-4" />
                      </div>
                      {{ dept.name }}
                    </td>
                    <td class="p-4 text-center whitespace-nowrap">
                      <span class="text-gray-900 font-semibold">{{ dept.total }}</span> / 
                      <span class="text-red-500">{{ dept.pending }}</span>
                    </td>
                    <td class="p-4 text-center text-gray-600 whitespace-nowrap">{{ dept.avgTime }}</td>
                    <td class="p-4 text-center whitespace-nowrap">
                      <span :class="['px-2 py-1 rounded-full text-xs font-semibold', dept.score >= 90 ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700']">
                        {{ dept.score }}%
                      </span>
                    </td>
                    <td class="p-4 text-right whitespace-nowrap">
                      <button class="text-[#2563EB] hover:text-[#1E40AF] font-medium text-sm mr-3">Manage</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- System Alerts -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50 flex flex-col">
            <div class="p-6 border-b border-gray-100">
              <h2 class="text-lg font-bold text-gray-900 flex items-center gap-2">
                <AlertTriangle class="w-5 h-5 text-[#EF4444]" /> System Alerts
              </h2>
            </div>
            <div class="p-6 flex-1 overflow-y-auto space-y-4 max-h-[400px] custom-scrollbar">
              <div v-for="alert in systemAlerts" :key="alert.id" :class="`p-4 rounded-xl border-l-4 ${alert.borderClass} ${alert.bgClass}`">
                <div class="flex justify-between items-start">
                  <h4 :class="`font-semibold text-sm ${alert.textClass}`">{{ alert.title }}</h4>
                  <span class="text-xs text-gray-500 shrink-0 ml-2">{{ alert.time }}</span>
                </div>
                <p class="text-sm mt-1 text-gray-600">{{ alert.message }}</p>
              </div>
            </div>
          </section>
        </div>

        <!-- Approvals & Activity Log -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          
          <!-- Pending Approvals -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50">
            <div class="p-6 border-b border-gray-100">
              <h2 class="text-lg font-bold text-gray-900">Pending Approvals</h2>
            </div>
            <div class="divide-y divide-gray-100">
              <div v-for="approval in pendingApprovals" :key="approval.id" class="p-5 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors gap-4">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 shrink-0">
                    <UserCog v-if="approval.type === 'Officer'" class="w-5 h-5" />
                    <FolderKanban v-else class="w-5 h-5" />
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900 text-sm">{{ approval.name }}</p>
                    <p class="text-xs text-gray-500">{{ approval.role }} • {{ approval.department }}</p>
                  </div>
                </div>
                <div class="flex gap-2 self-end sm:self-auto">
                  <button class="px-3 py-1.5 text-sm bg-green-50 text-green-700 hover:bg-green-100 rounded-lg transition-colors font-medium flex items-center gap-1">
                    <CheckCircle class="w-4 h-4" /> Approve
                  </button>
                  <button class="px-3 py-1.5 text-sm bg-red-50 text-red-700 hover:bg-red-100 rounded-lg transition-colors font-medium flex items-center gap-1">
                    <XCircle class="w-4 h-4" /> Reject
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- Platform Activity Timeline -->
          <section class="bg-white rounded-[14px] shadow-sm border border-gray-50">
            <div class="p-6 border-b border-gray-100">
              <h2 class="text-lg font-bold text-gray-900">Recent Platform Activity</h2>
            </div>
            <div class="p-6">
              <div class="relative border-l-2 border-gray-100 ml-3 space-y-6">
                <div v-for="activity in platformActivity" :key="activity.id" class="relative pl-6">
                  <span class="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-[#2563EB]"></span>
                  <div class="flex flex-col sm:flex-row sm:justify-between sm:items-baseline mb-1">
                    <h4 class="text-sm font-semibold text-gray-900">{{ activity.action }}</h4>
                    <span class="text-xs text-gray-400">{{ activity.time }}</span>
                  </div>
                  <p class="text-sm text-gray-500">{{ activity.description }}</p>
                </div>
              </div>
            </div>
          </section>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';

// Import Your Existing Layout Components (Adjust paths if necessary)
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';

// Icons
import { 
  Users, UserCog, HardHat, Building2, ClipboardList, 
  CheckCircle, Megaphone, Activity, Server, Zap, 
  AlertTriangle, ShieldCheck, XCircle, FolderKanban
} from 'lucide-vue-next';

// Layout State
const sidebarOpen = ref(false);

// Clock Logic
const currentTime = ref('');
const currentDate = ref('');
let timerInterval = null;

const updateClock = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  currentDate.value = now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
};

// Dummy Data
const topStats = ref([
  { label: 'Total Citizens', value: '45,231', icon: Users, colorClass: 'text-[#2563EB]', textClass: 'text-[#2563EB]', trend: '+12%', trendUp: true },
  { label: 'Total Officers', value: '128', icon: UserCog, colorClass: 'text-[#1E40AF]', textClass: 'text-[#1E40AF]', trend: '+2%', trendUp: true },
  { label: 'Total Workers', value: '845', icon: HardHat, colorClass: 'text-[#F59E0B]', textClass: 'text-[#F59E0B]', trend: '+5%', trendUp: true },
  { label: 'Total Complaints', value: '12,405', icon: ClipboardList, colorClass: 'text-[#EF4444]', textClass: 'text-[#EF4444]', trend: '-3%', trendUp: false },
  { label: 'Resolved Today', value: '342', icon: CheckCircle, colorClass: 'text-[#22C55E]', textClass: 'text-[#22C55E]', trend: '+18%', trendUp: true },
]);

const systemHealth = ref([
  { label: 'Server Status', value: 'Operational', statusColor: 'bg-[#22C55E]' },
  { label: 'Database Status', value: 'Healthy', statusColor: 'bg-[#22C55E]' },
  { label: 'API Uptime', value: '99.98%', statusColor: 'bg-[#22C55E]' },
  { label: 'Storage Usage', value: '68%', statusColor: 'bg-[#F59E0B]' },
  { label: 'Active Sessions', value: '1,204', statusColor: 'bg-[#2563EB]' },
  { label: 'Last Backup', value: '2 hrs ago', statusColor: 'bg-[#22C55E]' },
]);

const quickActions = ref([
  { label: 'Add Department', icon: Building2 },
  { label: 'Approve Officers', icon: ShieldCheck },
  { label: 'Announcement', icon: Megaphone },
  { label: 'System Settings', icon: Server },
]);

const departmentPerformance = ref([
  { id: 1, name: 'Garbage Management', total: 3402, pending: 142, avgTime: '24h 15m', score: 92 },
  { id: 2, name: 'Road Maintenance', total: 2105, pending: 305, avgTime: '72h 40m', score: 78 },
  { id: 3, name: 'Water Supply', total: 1840, pending: 85, avgTime: '18h 20m', score: 95 },
  { id: 4, name: 'Street Lighting', total: 1204, pending: 45, avgTime: '12h 10m', score: 98 },
]);

const systemAlerts = ref([
  { id: 1, title: 'Emergency Complaint Spike', message: 'Unusual volume of drainage complaints in Sector 4.', time: '10 mins ago', borderClass: 'border-[#EF4444]', bgClass: 'bg-red-50', textClass: 'text-[#EF4444]' },
  { id: 2, title: 'Database Backup Required', message: 'Automated backup failed. Manual intervention needed.', time: '1 hr ago', borderClass: 'border-[#F59E0B]', bgClass: 'bg-yellow-50', textClass: 'text-[#F59E0B]' },
  { id: 3, title: 'Inactive Officer', message: 'Officer Rahul Sharma hasn\'t logged in for 7 days.', time: '3 hrs ago', borderClass: 'border-[#2563EB]', bgClass: 'bg-blue-50', textClass: 'text-[#2563EB]' },
]);

const pendingApprovals = ref([
  { id: 1, name: 'Priya Desai', role: 'Officer Request', department: 'Public Health', type: 'Officer' },
  { id: 2, name: 'Amit Kumar', role: 'Worker App', department: 'Road Maintenance', type: 'Worker' },
  { id: 3, name: 'Sanjay Singh', role: 'Officer Request', department: 'Animal Control', type: 'Officer' },
]);

const platformActivity = ref([
  { id: 1, action: 'Department Added', description: 'System Administrator created "Building Maintenance" department.', time: 'Today, 09:45 AM' },
  { id: 2, action: 'Announcement Published', description: 'Monsoon safety guidelines published to all citizens.', time: 'Yesterday, 14:30 PM' },
  { id: 3, action: 'Worker Approved', description: 'Officer approved 15 new workers for Garbage Management.', time: 'Yesterday, 11:15 AM' },
  { id: 4, action: 'System Settings Changed', description: 'Updated complaint auto-escalation timer from 48h to 24h.', time: 'Oct 12, 10:00 AM' },
]);

// Chart Logic
const growthChartRef = ref(null);
const categoryChartRef = ref(null);

const initializeCharts = () => {
  new Chart(growthChartRef.value, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'New Citizens',
        data: [1200, 1900, 2400, 2100, 3200, 4100],
        borderColor: '#2563EB',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        tension: 0.4,
        fill: true,
      },
      {
        label: 'New Workers',
        data: [50, 120, 180, 140, 220, 280],
        borderColor: '#22C55E',
        backgroundColor: 'transparent',
        tension: 0.4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' } },
      scales: { y: { beginAtZero: true, grid: { color: '#F3F4F6' } }, x: { grid: { display: false } } }
    }
  });

  new Chart(categoryChartRef.value, {
    type: 'doughnut',
    data: {
      labels: ['Garbage', 'Roads', 'Street Light', 'Drainage', 'Water', 'Others'],
      datasets: [{
        data: [35, 20, 15, 12, 10, 8],
        backgroundColor: ['#2563EB', '#1E40AF', '#F59E0B', '#EF4444', '#22C55E', '#94A3B8'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: { legend: { position: 'right' } }
    }
  });
};

onMounted(() => {
  updateClock();
  timerInterval = setInterval(updateClock, 1000);
  initializeCharts();
});

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

/* Custom Scrollbars to match your images */
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
</style>