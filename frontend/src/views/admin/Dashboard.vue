<template>
  <div class="font-sans animate-fade-in">

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
                @click="router.push(action.route)"
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
              <button @click="router.push('/admin/departmentmanagement')" class="text-sm text-[#2563EB] font-medium hover:underline">View All</button>
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
                  <tr v-if="!departmentPerformance.length">
                    <td colspan="5" class="p-6 text-center text-gray-400">No complaint activity yet.</td>
                  </tr>
                  <tr v-for="dept in departmentPerformance" :key="dept.name" class="hover:bg-gray-50 transition-colors">
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
                      <button @click="router.push('/admin/departmentmanagement')" class="text-[#2563EB] hover:text-[#1E40AF] font-medium text-sm mr-3">Manage</button>
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
              <div v-if="!systemAlerts.length" class="text-sm text-gray-400 text-center py-6">
                No active alerts. Everything looks normal.
              </div>
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
              <div v-if="!pendingApprovals.length" class="p-6 text-sm text-gray-400 text-center">
                No pending approvals.
              </div>
              <div v-for="approval in pendingApprovals" :key="approval.id" class="p-5 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors gap-4">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 shrink-0">
                    <UserCog v-if="approval.type === 'Officer'" class="w-5 h-5" />
                    <FolderKanban v-else class="w-5 h-5" />
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900 text-sm">{{ approval.name }}</p>
                    <p class="text-xs text-gray-500">{{ approval.role }} • {{ approval.department || 'Not assigned' }}</p>
                  </div>
                </div>
                <div class="flex gap-2 self-end sm:self-auto">
                  <button @click="approveUser(approval.id)" :disabled="approval.busy"
                    class="px-3 py-1.5 text-sm bg-green-50 text-green-700 hover:bg-green-100 rounded-lg transition-colors font-medium flex items-center gap-1 disabled:opacity-50">
                    <CheckCircle class="w-4 h-4" /> Approve
                  </button>
                  <button @click="rejectUser(approval.id)" :disabled="approval.busy"
                    class="px-3 py-1.5 text-sm bg-red-50 text-red-700 hover:bg-red-100 rounded-lg transition-colors font-medium flex items-center gap-1 disabled:opacity-50">
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
                <p v-if="!platformActivity.length" class="text-sm text-gray-400 pl-6">No recent activity.</p>
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

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Chart from 'chart.js/auto';

// Icons
import { 
  Users, UserCog, HardHat, Building2, ClipboardList, 
  CheckCircle, Megaphone, Activity, Server, Zap, 
  AlertTriangle, ShieldCheck, XCircle, FolderKanban
} from 'lucide-vue-next';

const router = useRouter();

// Layout State
const isLoading = ref(true);

// Clock Logic
const currentTime = ref('');
const currentDate = ref('');
let timerInterval = null;

const updateClock = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  currentDate.value = now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
};

// --- Top Stats: labels/icons are static, values come from the API ---
const STAT_META = [
  { key: 'total_citizens',   label: 'Total Citizens',   icon: Users,         colorClass: 'text-[#2563EB]', textClass: 'text-[#2563EB]' },
  { key: 'total_officers',   label: 'Total Officers',   icon: UserCog,       colorClass: 'text-[#1E40AF]', textClass: 'text-[#1E40AF]' },
  { key: 'total_workers',    label: 'Total Workers',    icon: HardHat,       colorClass: 'text-[#F59E0B]', textClass: 'text-[#F59E0B]' },
  { key: 'total_complaints', label: 'Total Complaints', icon: ClipboardList, colorClass: 'text-[#EF4444]', textClass: 'text-[#EF4444]' },
  { key: 'resolved_today',   label: 'Resolved Today',   icon: CheckCircle,   colorClass: 'text-[#22C55E]', textClass: 'text-[#22C55E]' },
];
const topStats = ref(STAT_META.map(m => ({ ...m, value: '0', trend: '—', trendUp: true })));

// System Health has no real backing data source (no server/infra monitoring
// exists in this app) — kept as a static placeholder rather than fabricated.
const systemHealth = ref([
  { label: 'Server Status', value: 'Not monitored', statusColor: 'bg-gray-300' },
  { label: 'Database Status', value: 'Not monitored', statusColor: 'bg-gray-300' },
  { label: 'API Uptime', value: 'Not monitored', statusColor: 'bg-gray-300' },
  { label: 'Storage Usage', value: 'Not monitored', statusColor: 'bg-gray-300' },
  { label: 'Active Sessions', value: 'Not monitored', statusColor: 'bg-gray-300' },
  { label: 'Last Backup', value: 'Not monitored', statusColor: 'bg-gray-300' },
]);

const quickActions = ref([
  { label: 'Add Department', icon: Building2, route: '/admin/departmentmanagement' },
  { label: 'Approve Officers', icon: ShieldCheck, route: '/admin/officermanagement' },
  { label: 'Announcement', icon: Megaphone, route: '/admin/announcements' },
  { label: 'System Settings', icon: Server, route: '/admin/systemanalytics' },
]);

const departmentPerformance = ref([]);
const systemAlerts = ref([]);
const pendingApprovals = ref([]);
const platformActivity = ref([]);

const ALERT_STYLES = {
  critical: { borderClass: 'border-[#EF4444]', bgClass: 'bg-red-50', textClass: 'text-[#EF4444]' },
  warning:  { borderClass: 'border-[#F59E0B]', bgClass: 'bg-yellow-50', textClass: 'text-[#F59E0B]' },
  info:     { borderClass: 'border-[#2563EB]', bgClass: 'bg-blue-50', textClass: 'text-[#2563EB]' },
};

const formatRelativeTime = (isoString) => {
  if (!isoString) return '';
  const diffMs = Date.now() - new Date(isoString).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins} min${mins > 1 ? 's' : ''} ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs} hr${hrs > 1 ? 's' : ''} ago`;
  const days = Math.floor(hrs / 24);
  return `${days} day${days > 1 ? 's' : ''} ago`;
};

// --- Charts ---
const growthChartRef = ref(null);
const categoryChartRef = ref(null);
let growthChart, categoryChart;

const initializeCharts = () => {
  growthChart = new Chart(growthChartRef.value, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        { label: 'New Citizens', data: [], borderColor: '#2563EB', backgroundColor: 'rgba(37, 99, 235, 0.1)', tension: 0.4, fill: true },
        { label: 'New Workers', data: [], borderColor: '#22C55E', backgroundColor: 'transparent', tension: 0.4 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' } },
      scales: { y: { beginAtZero: true, grid: { color: '#F3F4F6' } }, x: { grid: { display: false } } }
    }
  });

  categoryChart = new Chart(categoryChartRef.value, {
    type: 'doughnut',
    data: {
      labels: [],
      datasets: [{
        data: [],
        backgroundColor: ['#2563EB', '#1E40AF', '#F59E0B', '#EF4444', '#22C55E', '#94A3B8', '#A855F7', '#EC4899', '#14B8A6'],
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

const fetchDashboard = async () => {
  isLoading.value = true;
  try {
    const token = localStorage.getItem('token');
    const { data } = await axios.get('http://127.0.0.1:5000/api/admin/dashboard', {
      headers: { Authorization: `Bearer ${token}` }
    });

    topStats.value = STAT_META.map(m => {
      const s = data.top_stats[m.key] || { value: 0, trend_pct: null };
      return {
        ...m,
        value: s.value.toLocaleString(),
        trend: s.trend_pct == null ? '—' : `${s.trend_pct >= 0 ? '+' : ''}${s.trend_pct}%`,
        trendUp: s.trend_pct == null ? true : s.trend_pct >= 0,
      };
    });

    departmentPerformance.value = data.department_performance || [];

    systemAlerts.value = (data.alerts || []).map((a, idx) => ({
      id: idx,
      title: a.title,
      message: a.message,
      time: '',
      ...(ALERT_STYLES[a.severity] || ALERT_STYLES.info),
    }));

    pendingApprovals.value = (data.pending_approvals || []).map(a => ({
      ...a, type: a.role, busy: false,
    }));

    platformActivity.value = (data.platform_activity || []).map(a => ({
      ...a, time: formatRelativeTime(a.created_at),
    }));

    if (growthChart && data.growth_chart) {
      growthChart.data.labels = data.growth_chart.labels;
      growthChart.data.datasets[0].data = data.growth_chart.new_citizens;
      growthChart.data.datasets[1].data = data.growth_chart.new_workers;
      growthChart.update();
    }
    if (categoryChart && data.category_breakdown) {
      categoryChart.data.labels = Object.keys(data.category_breakdown);
      categoryChart.data.datasets[0].data = Object.values(data.category_breakdown);
      categoryChart.update();
    }
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    console.error('Admin dashboard fetch error:', err);
  } finally {
    isLoading.value = false;
  }
};

const approveUser = async (userId) => {
  const target = pendingApprovals.value.find(a => a.id === userId);
  if (target) target.busy = true;
  try {
    const token = localStorage.getItem('token');
    await axios.patch(`http://127.0.0.1:5000/api/admin/users/${userId}/approve`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    pendingApprovals.value = pendingApprovals.value.filter(a => a.id !== userId);
  } catch (err) {
    console.error('Approve failed:', err);
    if (target) target.busy = false;
  }
};

const rejectUser = async (userId) => {
  const target = pendingApprovals.value.find(a => a.id === userId);
  if (target) target.busy = true;
  try {
    const token = localStorage.getItem('token');
    await axios.patch(`http://127.0.0.1:5000/api/admin/users/${userId}/reject`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    pendingApprovals.value = pendingApprovals.value.filter(a => a.id !== userId);
  } catch (err) {
    console.error('Reject failed:', err);
    if (target) target.busy = false;
  }
};

onMounted(() => {
  updateClock();
  timerInterval = setInterval(updateClock, 1000);
  initializeCharts();
  fetchDashboard();
});

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval);
  if (growthChart) growthChart.destroy();
  if (categoryChart) categoryChart.destroy();
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