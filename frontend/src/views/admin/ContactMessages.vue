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
              <span class="text-gray-900">Contact Messages</span>
            </nav>
            <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Contact Messages</h1>
            <p class="text-gray-500 mt-1 text-sm md:text-base">
              Messages submitted by visitors through the public Contact Us form.
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
          <button @click="fetchMessages" class="font-semibold underline shrink-0 ml-4">Retry</button>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="text-center text-gray-400 py-10">Loading messages…</div>

        <template v-else>
        <!-- Summary Cards -->
        <section class="mb-6 grid grid-cols-2 sm:grid-cols-4 gap-4">
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
        <section class="bg-white p-5 rounded-[14px] shadow-sm border border-gray-50 mb-6 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div class="w-full md:w-1/2 relative">
            <Search class="w-5 h-5 text-gray-400 absolute left-3 top-3" />
            <input
              v-model="filters.search"
              type="text"
              placeholder="Search name, email, subject, message..."
              class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
            />
          </div>
          <div class="flex gap-2 shrink-0">
            <button v-for="opt in statusOptions" :key="opt"
                    @click="filters.status = opt; fetchMessages()"
                    :class="['px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                              filters.status === opt ? 'bg-[#2563EB] text-white' : 'text-gray-600 bg-gray-50 hover:bg-gray-100']">
              {{ opt }}
            </button>
          </div>
        </section>

        <!-- Messages List -->
        <div v-if="filteredMessages.length > 0" class="space-y-3">
          <div v-for="msg in filteredMessages" :key="msg.id"
               class="bg-white p-5 rounded-[14px] border shadow-sm flex gap-4 hover:shadow-md transition-all cursor-pointer"
               :class="msg.is_read ? 'border-gray-50' : 'border-blue-200 bg-blue-50/30'"
               @click="openMessage(msg)">
            <div class="p-2.5 rounded-full h-11 w-11 flex items-center justify-center shrink-0"
                 :class="msg.is_read ? 'bg-gray-100' : 'bg-blue-100'">
              <Mail class="w-5 h-5" :class="msg.is_read ? 'text-gray-400' : 'text-[#2563EB]'" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-start gap-4">
                <div class="min-w-0">
                  <div class="flex items-center gap-2">
                    <h4 class="font-bold text-gray-900 truncate">{{ msg.name }}</h4>
                    <span v-if="!msg.is_read" class="w-2 h-2 rounded-full bg-[#2563EB] shrink-0"></span>
                  </div>
                  <p class="text-xs text-gray-500 truncate">{{ msg.email }}</p>
                  <p class="text-sm text-gray-700 mt-1.5 font-medium truncate">{{ msg.subject }}</p>
                  <p class="text-sm text-gray-500 mt-0.5 line-clamp-2">{{ msg.message }}</p>
                </div>
                <span class="text-xs text-gray-400 font-medium whitespace-nowrap shrink-0">{{ timeAgo(msg.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-20 bg-white rounded-[14px] border border-gray-50">
          <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
            <Mail class="w-8 h-8 text-gray-300" />
          </div>
          <h3 class="text-lg font-bold text-gray-900">No Messages</h3>
          <p class="text-gray-500 mt-2">Nothing here matches the current filters.</p>
        </div>
        </template>
      </main>

      <!-- Detail Drawer -->
      <div v-if="isDrawerOpen" class="fixed inset-0 z-50 flex justify-end">
        <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm" @click="closeDrawer"></div>
        <div class="relative w-full max-w-lg bg-white h-full shadow-2xl p-6 overflow-y-auto animate-slide-in">
          <div v-if="selectedMsg" class="flex flex-col h-full">
            <div class="flex items-start justify-between mb-6">
              <div>
                <h3 class="text-xl font-bold text-gray-900">{{ selectedMsg.subject }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ timeAgo(selectedMsg.created_at) }}</p>
              </div>
              <button @click="closeDrawer" class="p-2 text-gray-400 hover:bg-gray-100 rounded-full transition-colors">
                <X class="w-5 h-5" />
              </button>
            </div>

            <div class="bg-gray-50 rounded-xl p-4 mb-6 border border-gray-100">
              <p class="font-bold text-gray-900">{{ selectedMsg.name }}</p>
              <a :href="`mailto:${selectedMsg.email}`" class="text-sm text-[#2563EB] font-medium hover:underline">{{ selectedMsg.email }}</a>
            </div>

            <div class="flex-1">
              <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{{ selectedMsg.message }}</p>
            </div>

            <div class="flex gap-3 pt-6 border-t border-gray-100 mt-6">
              <a :href="`mailto:${selectedMsg.email}?subject=Re: ${selectedMsg.subject}`"
                 class="flex-1 flex items-center justify-center gap-2 bg-[#2563EB] hover:bg-[#1E40AF] text-white font-semibold py-2.5 rounded-lg transition-colors text-sm">
                <Reply class="w-4 h-4" /> Reply by Email
              </a>
              <button @click="toggleRead(selectedMsg)"
                      class="flex items-center justify-center gap-2 bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 font-semibold py-2.5 px-4 rounded-lg transition-colors text-sm">
                <component :is="selectedMsg.is_read ? MailX : MailCheck" class="w-4 h-4" />
                {{ selectedMsg.is_read ? 'Mark Unread' : 'Mark Read' }}
              </button>
              <button @click="removeMessage(selectedMsg)"
                      class="flex items-center justify-center gap-2 bg-white border border-red-200 text-red-600 hover:bg-red-50 font-semibold py-2.5 px-3 rounded-lg transition-colors text-sm">
                <Trash2 class="w-4 h-4" />
              </button>
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
  Mail, MailCheck, MailX, Calendar, Search, X, Reply, Trash2, Inbox, CircleDot
} from 'lucide-vue-next';

const API_BASE = 'http://127.0.0.1:5000/api/admin';
const router = useRouter();
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });

const currentDate = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

const isLoading = ref(true);
const errorMessage = ref('');
const messages = ref([]);
const summary = ref({ total: 0, unread: 0, read: 0, today: 0 });
const filters = ref({ search: '', status: 'All' });
const statusOptions = ['All', 'Unread', 'Read'];

const isDrawerOpen = ref(false);
const selectedMsg = ref(null);

const summaryCards = computed(() => [
  { key: 'total',  label: 'Total Messages', count: summary.value.total,  icon: Inbox,     iconBg: 'bg-blue-50',   iconColor: 'text-[#2563EB]' },
  { key: 'unread', label: 'Unread',         count: summary.value.unread, icon: CircleDot, iconBg: 'bg-red-50',    iconColor: 'text-red-600' },
  { key: 'read',   label: 'Read',           count: summary.value.read,   icon: MailCheck, iconBg: 'bg-green-50',  iconColor: 'text-green-600' },
  { key: 'today',  label: 'Received Today', count: summary.value.today,  icon: Calendar,  iconBg: 'bg-yellow-50', iconColor: 'text-yellow-600' },
]);

const filteredMessages = computed(() => {
  if (!filters.value.search.trim()) return messages.value;
  const q = filters.value.search.trim().toLowerCase();
  return messages.value.filter(m =>
    m.name.toLowerCase().includes(q) ||
    m.email.toLowerCase().includes(q) ||
    m.subject.toLowerCase().includes(q) ||
    m.message.toLowerCase().includes(q)
  );
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
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const fetchMessages = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const { data } = await axios.get(`${API_BASE}/contact-messages`, {
      params: { status: filters.value.status },
      ...authHeaders()
    });
    messages.value = data.messages;
    summary.value = data.summary;
  } catch (err) {
    if (err.response?.status === 401) router.push('/login');
    else errorMessage.value = err.response?.data?.message || 'Failed to load contact messages.';
  } finally {
    isLoading.value = false;
  }
};

const openMessage = async (msg) => {
  selectedMsg.value = msg;
  isDrawerOpen.value = true;
  if (!msg.is_read) {
    await toggleRead(msg, true);
  }
};

const closeDrawer = () => {
  isDrawerOpen.value = false;
  setTimeout(() => { selectedMsg.value = null; }, 200);
};

const toggleRead = async (msg, forceRead = null) => {
  const nextState = forceRead !== null ? forceRead : !msg.is_read;
  try {
    const { data } = await axios.patch(
      `${API_BASE}/contact-messages/${msg.id}/read`,
      { read: nextState },
      authHeaders()
    );
    const updated = data.message_data;
    const idx = messages.value.findIndex(m => m.id === msg.id);
    if (idx !== -1) messages.value[idx] = updated;
    if (selectedMsg.value?.id === msg.id) selectedMsg.value = updated;
    summary.value.unread += updated.is_read ? -1 : 1;
    summary.value.read += updated.is_read ? 1 : -1;
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to update message.';
  }
};

const removeMessage = async (msg) => {
  if (!confirm('Delete this message permanently?')) return;
  try {
    await axios.delete(`${API_BASE}/contact-messages/${msg.id}`, authHeaders());
    closeDrawer();
    await fetchMessages();
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'Failed to delete message.';
  }
};

onMounted(fetchMessages);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.font-sans { font-family: 'Inter', sans-serif; }

.custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }

@keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
.animate-slide-in { animation: slideIn 0.25s ease-out forwards; }

.line-clamp-2 {
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
