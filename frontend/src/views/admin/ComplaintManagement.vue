<template>
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">

      <!-- Scrollable Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">

        <!-- Header & Breadcrumbs -->
        <header class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">Complaint Management</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Complaint Management</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Review every complaint platform-wide and assign it to the right Civic Officer.
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
          <button @click="fetchComplaints" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="text-center text-gray-400 py-10">Loading complaints…</div>

        <template v-else>
        <!-- Summary Cards -->
        <section class="mb-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="card in summaryCards" :key="card.key"
               class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 flex items-center gap-3 hover:border-gray-200 hover:shadow-md transition-all">
            <div :class="['p-2.5 rounded-xl', card.iconBg]">
              <component :is="card.icon" class="w-5 h-5" :class="card.iconColor" />
            </div>
            <div>
              <p class="text-xl font-bold text-gray-900">{{ card.count }}</p>
              <p class="text-xs font-medium text-gray-500">{{ card.label }}</p>
            </div>
          </div>
        </section>

        <!-- Search & Filter Panel -->
        <section class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col xl:flex-row gap-4 items-center justify-between">
          <div class="w-full xl:w-1/3 relative">
            <Search class="w-5 h-5 text-gray-400 absolute left-3 top-3" />
            <input
              v-model="filters.search"
              type="text"
              placeholder="Search title, category, ID, citizen..."
              class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
            />
          </div>
          <div class="w-full xl:w-2/3 flex flex-wrap xl:flex-nowrap gap-3 justify-end">
            <select v-model="filters.status" @change="fetchComplaints" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="All">All Status</option>
              <option value="Unassigned">Unassigned</option>
              <option value="Pending">Pending</option>
              <option value="Under Review">Under Review</option>
              <option value="Assigned">Assigned</option>
              <option value="In Progress">In Progress</option>
              <option value="Resolved">Resolved</option>
              <option value="Closed">Closed</option>
            </select>
            <select v-model="filters.department" @change="fetchComplaints" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="All">All Departments</option>
              <option v-for="d in departments" :key="d" :value="d">{{ d }}</option>
            </select>
            <select v-model="filters.priority" @change="fetchComplaints" class="bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none w-full sm:w-auto">
              <option value="All">All Priorities</option>
              <option value="Emergency">Emergency</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
        </section>

        <!-- Complaints Table (Desktop) -->
        <section class="hidden lg:block bg-white rounded-[14px] shadow-sm border border-gray-50 overflow-hidden mb-6">
          <div class="overflow-x-auto no-scrollbar">
            <table class="w-full text-left border-collapse min-w-[900px]">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-[10px] uppercase tracking-wider font-bold">
                  <th class="p-4 whitespace-nowrap">Complaint</th>
                  <th class="p-4 whitespace-nowrap">Citizen</th>
                  <th class="p-4 whitespace-nowrap">Department</th>
                  <th class="p-4 whitespace-nowrap text-center">Priority</th>
                  <th class="p-4 whitespace-nowrap text-center">Status</th>
                  <th class="p-4 whitespace-nowrap">Assigned Officer</th>
                  <th class="p-4 whitespace-nowrap text-right">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm">
                <tr v-for="c in filteredComplaints" :key="c.raw_id" class="hover:bg-gray-50 transition-colors cursor-pointer" @click="openDrawer(c)">
                  <td class="p-4">
                    <p class="font-bold text-[#2563EB] text-xs font-mono">{{ c.id }}</p>
                    <p class="font-semibold text-gray-900 mt-0.5 truncate max-w-[220px]">{{ c.title }}</p>
                    <p class="text-xs text-gray-500 mt-0.5">{{ c.category }}</p>
                  </td>
                  <td class="p-4 text-gray-700">{{ c.citizen?.name || 'Unknown' }}</td>
                  <td class="p-4 text-gray-700">{{ c.department }}</td>
                  <td class="p-4 text-center">
                    <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase', getPriorityBadge(c.priority)]">{{ c.priority }}</span>
                  </td>
                  <td class="p-4 text-center">
                    <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase', getStatusBadge(c.status)]">{{ c.status }}</span>
                  </td>
                  <td class="p-4 text-gray-700">
                    <span v-if="c.officer" class="font-medium">{{ c.officer.name }}</span>
                    <span v-else class="text-gray-400 italic">Unassigned</span>
                  </td>
                  <td class="p-4 text-right" @click.stop>
                    <button @click="openDrawer(c)"
                            class="px-3 py-1.5 text-xs font-bold rounded-lg border transition-colors"
                            :class="c.officer ? 'border-gray-200 text-gray-600 hover:bg-gray-50' : 'border-[#2563EB] text-[#2563EB] hover:bg-blue-50'">
                      {{ c.officer ? 'Reassign' : 'Assign' }}
                    </button>
                  </td>
                </tr>
                <tr v-if="filteredComplaints.length === 0">
                  <td colspan="7" class="p-10 text-center text-gray-500">No complaints found matching the current filters.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Complaints Cards (Mobile) -->
        <section class="lg:hidden space-y-3 mb-6">
          <div v-for="c in filteredComplaints" :key="c.raw_id"
               class="bg-white p-4 rounded-[14px] shadow-sm border border-gray-50" @click="openDrawer(c)">
            <div class="flex justify-between items-start mb-2">
              <div class="min-w-0">
                <p class="font-mono text-[10px] text-[#2563EB] font-bold">{{ c.id }}</p>
                <h3 class="font-bold text-gray-900 text-sm truncate">{{ c.title }}</h3>
              </div>
              <span :class="['px-2 py-0.5 rounded-full text-[9px] font-bold uppercase shrink-0', getStatusBadge(c.status)]">{{ c.status }}</span>
            </div>
            <p class="text-xs text-gray-500">{{ c.department }} • {{ c.citizen?.name || 'Unknown' }}</p>
            <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-50">
              <span v-if="c.officer" class="text-xs font-medium text-gray-700">{{ c.officer.name }}</span>
              <span v-else class="text-xs text-gray-400 italic">Unassigned</span>
              <button class="text-[#2563EB] text-xs font-semibold hover:underline">{{ c.officer ? 'Reassign' : 'Assign' }}</button>
            </div>
          </div>
          <div v-if="filteredComplaints.length === 0" class="text-center py-10 bg-white rounded-[14px] border border-gray-50 text-gray-500">No complaints found matching the current filters.</div>
        </section>
        </template>
      </main>

      <!-- Detail / Assign Drawer -->
      <div v-if="isDrawerOpen" class="fixed inset-0 z-50 flex justify-end">
        <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm" @click="closeDrawer"></div>
        <div class="relative w-full max-w-lg bg-white h-full shadow-2xl p-6 overflow-y-auto animate-slide-in">
          <div v-if="detailLoading" class="text-center text-gray-400 py-20">Loading details…</div>
          <div v-else-if="selectedComplaint" class="flex flex-col h-full">
            <div class="flex items-start justify-between mb-4">
              <div>
                <p class="font-mono text-xs text-[#2563EB] font-bold">{{ selectedComplaint.id }}</p>
                <h3 class="text-xl font-bold text-gray-900 mt-1">{{ selectedComplaint.title }}</h3>
              </div>
              <button @click="closeDrawer" class="p-2 text-gray-400 hover:bg-gray-100 rounded-full transition-colors">
                <X class="w-5 h-5" />
              </button>
            </div>

            <div class="flex flex-wrap gap-2 mb-5">
              <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase', getStatusBadge(selectedComplaint.status)]">{{ selectedComplaint.status }}</span>
              <span :class="['px-2.5 py-1 rounded-full text-[10px] font-bold uppercase', getPriorityBadge(selectedComplaint.priority)]">{{ selectedComplaint.priority }}</span>
              <span v-if="selectedComplaint.is_escalated" class="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase bg-red-600 text-white">Escalated</span>
            </div>

            <div class="space-y-4 mb-6">
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-100">
                <p class="text-[10px] font-bold text-gray-500 uppercase mb-1">Description</p>
                <p class="text-sm text-gray-700 leading-relaxed">{{ selectedComplaint.description }}</p>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
                  <p class="text-[10px] font-bold text-gray-500 uppercase mb-1">Citizen</p>
                  <p class="text-sm font-semibold text-gray-900">{{ selectedComplaint.citizen?.name }}</p>
                  <p class="text-xs text-gray-500">{{ selectedComplaint.citizen?.email }}</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
                  <p class="text-[10px] font-bold text-gray-500 uppercase mb-1">Department</p>
                  <p class="text-sm font-semibold text-gray-900">{{ selectedComplaint.department }}</p>
                </div>
              </div>
              <div class="bg-gray-50 rounded-xl p-4 border border-gray-100">
                <p class="text-[10px] font-bold text-gray-500 uppercase mb-1">Location</p>
                <p class="text-sm text-gray-700">{{ selectedComplaint.location }}</p>
              </div>
              <div v-if="selectedComplaint.images?.length" class="grid grid-cols-3 gap-2">
                <img v-for="(img, i) in selectedComplaint.images" :key="i" :src="`http://127.0.0.1:5000${img}`"
                     class="w-full h-20 object-cover rounded-lg border border-gray-100" />
              </div>
            </div>

            <!-- Assign / Reassign Officer -->
            <div class="border-t border-gray-100 pt-5">
              <p class="text-sm font-bold text-gray-900 mb-3">
                {{ selectedComplaint.officer ? `Currently assigned to ${selectedComplaint.officer.name}` : 'Assign an Officer' }}
              </p>

              <div v-if="selectedComplaint.eligible_officers.length === 0" class="text-sm text-gray-500 bg-yellow-50 border border-yellow-100 rounded-xl p-3">
                No active officers found in the "{{ selectedComplaint.department }}" department yet.
              </div>
              <div v-else class="flex flex-col sm:flex-row gap-3">
                <select v-model="selectedOfficerId" class="flex-1 bg-gray-50 border border-gray-200 text-gray-700 text-sm rounded-xl px-3 py-2.5 focus:ring-2 focus:ring-[#2563EB]/20 focus:outline-none">
                  <option value="" disabled>Select an officer…</option>
                  <option v-for="o in selectedComplaint.eligible_officers" :key="o.id" :value="o.id">{{ o.name }} ({{ o.empId }})</option>
                </select>
                <button @click="assignOfficer" :disabled="!selectedOfficerId || isAssigning"
                        class="bg-[#2563EB] hover:bg-[#1E40AF] text-white font-semibold px-5 py-2.5 rounded-xl transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed shrink-0">
                  {{ isAssigning ? 'Assigning…' : (selectedComplaint.officer ? 'Reassign' : 'Assign') }}
                </button>
              </div>
              <p v-if="assignError" class="text-red-600 text-xs mt-2">{{ assignError }}</p>
            </div>

            <!-- Status History -->
            <div v-if="selectedComplaint.status_logs?.length" class="border-t border-gray-100 mt-6 pt-5">
              <p class="text-sm font-bold text-gray-900 mb-3">Status History</p>
              <div class="space-y-3">
                <div v-for="(log, i) in selectedComplaint.status_logs" :key="i" class="flex gap-3 text-sm">
                  <div class="w-2 h-2 rounded-full bg-[#2563EB] mt-1.5 shrink-0"></div>
                  <div>
                    <p class="text-gray-800 font-medium">{{ log.old_status || 'Created' }} → {{ log.new_status }}</p>
                    <p class="text-xs text-gray-500">{{ log.remark }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import {
  Calendar, Search, X, ClipboardList, UserX, Loader2, CheckCircle2
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const router = useRouter();
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

const isLoading = ref(true);
const errorMessage = ref('');
const complaints = ref([]);
const departments = ref([]);
const summary = ref({ total: 0, unassigned: 0, in_progress: 0, resolved: 0 });
const filters = ref({ search: '', status: 'All', department: 'All', priority: 'All' });

const isDrawerOpen = ref(false);
const detailLoading = ref(false);
const selectedComplaint = ref(null);
const selectedOfficerId = ref('');
const isAssigning = ref(false);
const assignError = ref('');

const summaryCards = computed(() => [
  { key: 'total',      label: 'Total Complaints', count: summary.value.total,       icon: ClipboardList, iconBg: 'bg-blue-50',   iconColor: 'text-[#2563EB]' },
  { key: 'unassigned', label: 'Unassigned',       count: summary.value.unassigned,  icon: UserX,         iconBg: 'bg-red-50',    iconColor: 'text-red-600' },
  { key: 'in_progress',label: 'In Progress',      count: summary.value.in_progress, icon: Loader2,       iconBg: 'bg-yellow-50', iconColor: 'text-yellow-600' },
  { key: 'resolved',   label: 'Resolved/Closed',  count: summary.value.resolved,    icon: CheckCircle2,  iconBg: 'bg-green-50',  iconColor: 'text-green-600' },
]);

const filteredComplaints = computed(() => {
  if (!filters.value.search.trim()) return complaints.value;
  const q = filters.value.search.trim().toLowerCase();
  return complaints.value.filter(c =>
    c.title.toLowerCase().includes(q) ||
    c.category.toLowerCase().includes(q) ||
    c.id.toLowerCase().includes(q) ||
    (c.citizen?.name || '').toLowerCase().includes(q)
  );
});

const getStatusBadge = (status) => {
  switch (status) {
    case 'Pending': return 'bg-gray-100 text-gray-700';
    case 'Under Review': return 'bg-yellow-100 text-yellow-700';
    case 'Assigned': return 'bg-blue-100 text-blue-700';
    case 'In Progress': return 'bg-indigo-100 text-indigo-700';
    case 'Resolved': return 'bg-green-100 text-green-700';
    case 'Closed': return 'bg-gray-200 text-gray-600';
    default: return 'bg-gray-100 text-gray-700';
  }
};

const getPriorityBadge = (priority) => {
  switch (priority) {
    case 'Emergency': return 'bg-red-600 text-white';
    case 'High': return 'bg-red-100 text-red-700';
    case 'Medium': return 'bg-yellow-100 text-yellow-700';
    case 'Low': return 'bg-green-100 text-green-700';
    default: return 'bg-gray-100 text-gray-700';
  }
};

const fetchComplaints = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/complaints`, {
      params: {
        status: filters.value.status,
        department: filters.value.department,
        priority: filters.value.priority,
      },
      ...authHeaders()
    });
    complaints.value = data.complaints;
    summary.value = data.summary;
    departments.value = data.departments;
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    else errorMessage.value = err.response?.data?.message || 'Failed to load complaints.';
  } finally {
    isLoading.value = false;
  }
};

const openDrawer = async (c) => {
  isDrawerOpen.value = true;
  detailLoading.value = true;
  selectedComplaint.value = null;
  selectedOfficerId.value = '';
  assignError.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/complaints/${c.raw_id}`, authHeaders());
    selectedComplaint.value = data.complaint;
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to load complaint details.';
    isDrawerOpen.value = false;
  } finally {
    detailLoading.value = false;
  }
};

const closeDrawer = () => {
  isDrawerOpen.value = false;
  setTimeout(() => { selectedComplaint.value = null; }, 200);
};

const assignOfficer = async () => {
  if (!selectedOfficerId.value || !selectedComplaint.value) return;
  isAssigning.value = true;
  assignError.value = '';
  try {
    await axios.patch(
      `${API_BASE}/complaints/${selectedComplaint.value.raw_id}/assign`,
      { officer_id: selectedOfficerId.value },
      authHeaders()
    );
    closeDrawer();
    await fetchComplaints();
  } catch (err) {
    assignError.value = err.response?.data?.message || 'Failed to assign officer.';
  } finally {
    isAssigning.value = false;
  }
};

onMounted(fetchComplaints);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

.no-scrollbar { scrollbar-width: none; -ms-overflow-style: none; }
.no-scrollbar::-webkit-scrollbar { display: none; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }

@keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
.animate-slide-in { animation: slideIn 0.25s ease-out forwards; }
</style>
