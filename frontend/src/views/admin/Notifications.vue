<template>
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col relative overflow-hidden w-full">

      <!-- Scrollable Dashboard Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in custom-scrollbar">

        <!-- Header & Breadcrumbs -->
        <header class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <nav class="flex text-sm text-gray-500 mb-2 font-medium">
              <span class="hover:text-[#2563EB] cursor-pointer transition-colors">Dashboard</span>
              <span class="mx-2">/</span>
              <span class="text-gray-900">Notifications</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Notifications</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              System-wide feed of approvals, suspensions, department changes, and escalations.
            </p>
          </div>
          <div class="bg-white px-5 py-2.5 rounded-[14px] shadow-sm border border-gray-100 flex items-center gap-3">
            <Calendar class="w-5 h-5 text-[#2563EB]" />
            <span class="text-sm font-semibold text-gray-700">{{ currentDate }}</span>
          </div>
        </header>

        <!-- Error banner -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center justify-between">
          <span>{{ errorMessage }}</span>
          <button @click="fetchNotifications" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="text-center text-gray-400 py-10">Loading notifications…</div>

        <template v-else>
        <!-- Summary Cards -->
        <section class="mb-6 grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 gap-4">
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

        <!-- Filter Bar -->
        <div class="bg-white p-3 rounded-[14px] shadow-sm border border-gray-50 flex flex-wrap gap-2 mb-6">
          <button v-for="filter in filters" :key="filter.key" @click="activeFilter = filter.key"
                  :class="['px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                            activeFilter === filter.key ? 'bg-[#2563EB] text-white' : 'text-gray-600 hover:bg-gray-50']">
            {{ filter.label }}
          </button>
        </div>

        <!-- Feed -->
        <div v-if="filteredNotifications.length > 0" class="space-y-3">
          <div v-for="note in filteredNotifications" :key="note.id"
               class="bg-white p-5 rounded-[14px] border border-gray-50 shadow-sm flex gap-4 hover:shadow-md transition-all">
            <div :class="['p-2 rounded-full h-10 w-10 flex items-center justify-center shrink-0', CATEGORY_META[note.category].iconBg]">
              <component :is="CATEGORY_META[note.category].icon" class="w-5 h-5" :class="CATEGORY_META[note.category].iconColor" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-start gap-4">
                <div class="min-w-0">
                  <h4 class="font-bold text-gray-900">{{ note.title }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ note.message }}</p>
                </div>
                <span class="text-xs text-gray-400 font-medium whitespace-nowrap shrink-0">{{ timeAgo(note.created_at) }}</span>
              </div>
              <div class="flex items-center gap-3 mt-3">
                <span :class="['text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded', CATEGORY_META[note.category].badgeClass]">
                  {{ CATEGORY_META[note.category].label }}
                </span>
                <span v-if="note.admin" class="text-[10px] text-gray-400">by {{ note.admin }}</span>
                <span v-if="note.complaint_id" class="text-[10px] font-bold text-gray-500 bg-gray-100 px-2 py-1 rounded">{{ note.complaint_id }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-20 bg-white rounded-[14px] border border-gray-50">
          <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
            <Bell class="w-8 h-8 text-gray-300" />
          </div>
          <h3 class="text-lg font-bold text-gray-900">No Notifications</h3>
          <p class="text-gray-500 mt-2">Nothing in this category yet.</p>
        </div>
        </template>
      </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import {
  Bell, Calendar, UserCheck, UserX, Building2, AlertTriangle,
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const router = useRouter();
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
const isLoading = ref(true);
const errorMessage = ref('');
const activeFilter = ref('all');
const notifications = ref([]);
const summary = ref({ total: 0, approvals: 0, suspensions: 0, departments: 0, escalations: 0 });

// This feed is read-only and derived (see the backend comment on
// GET /api/admin/notifications) — there's no persisted read/unread state,
// so unlike the citizen Notifications page, there's no "Mark All Read"
// here and no per-item read styling. It's a live system feed, not an inbox.
const CATEGORY_META = {
  approvals:   { label: 'Approval',    icon: UserCheck,     iconBg: 'bg-green-100',  iconColor: 'text-green-600',  badgeClass: 'bg-green-100 text-green-700' },
  suspensions: { label: 'Suspension',  icon: UserX,         iconBg: 'bg-red-100',    iconColor: 'text-red-600',    badgeClass: 'bg-red-100 text-red-700' },
  departments: { label: 'Department',  icon: Building2,     iconBg: 'bg-blue-100',   iconColor: 'text-[#2563EB]',  badgeClass: 'bg-blue-100 text-blue-700' },
  escalations: { label: 'Escalation',  icon: AlertTriangle, iconBg: 'bg-yellow-100', iconColor: 'text-yellow-600', badgeClass: 'bg-yellow-100 text-yellow-700' },
};

const summaryCards = computed(() => [
  { key: 'total',       label: 'Total',       count: summary.value.total,       icon: Bell,         iconBg: 'bg-blue-50',   iconColor: 'text-[#2563EB]' },
  { key: 'approvals',   label: 'Approvals',   count: summary.value.approvals,   icon: UserCheck,     iconBg: 'bg-green-50',  iconColor: 'text-green-600' },
  { key: 'suspensions', label: 'Suspensions', count: summary.value.suspensions, icon: UserX,         iconBg: 'bg-red-50',    iconColor: 'text-red-600' },
  { key: 'departments', label: 'Departments', count: summary.value.departments, icon: Building2,     iconBg: 'bg-blue-50',   iconColor: 'text-[#2563EB]' },
  { key: 'escalations', label: 'Escalations', count: summary.value.escalations, icon: AlertTriangle, iconBg: 'bg-yellow-50', iconColor: 'text-yellow-600' },
]);

const filters = [
  { key: 'all', label: 'All' },
  { key: 'approvals', label: 'Approvals' },
  { key: 'suspensions', label: 'Suspensions' },
  { key: 'departments', label: 'Departments' },
  { key: 'escalations', label: 'Escalations' },
];

const filteredNotifications = computed(() => {
  if (activeFilter.value === 'all') return notifications.value;
  return notifications.value.filter(n => n.category === activeFilter.value);
});

const timeAgo = (iso) => {
  const diffMs = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins} min ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs} hr${hrs !== 1 ? 's' : ''} ago`;
  const days = Math.floor(hrs / 24);
  if (days < 7) return days === 1 ? 'Yesterday' : `${days} days ago`;
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const fetchNotifications = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/notifications`, authHeaders());
    notifications.value = data.notifications;
    summary.value = data.summary;
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    else errorMessage.value = err.response?.data?.message || 'Failed to load notifications.';
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchNotifications);
</script>
