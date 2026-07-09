<template>
  <div class="bg-white p-6 rounded-[14px] shadow-sm border border-slate-100 transition-all hover:shadow-md hover:-translate-y-1">
    <div class="flex justify-between items-start mb-4">
      <div :class="['p-2.5 rounded-xl', iconBg]">
        <component :is="icon" class="w-6 h-6" :class="iconColor" />
      </div>
      <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">{{ trend }}</span>
    </div>
    <h3 class="text-3xl font-bold text-slate-900">{{ count }}</h3>
    <p class="text-sm font-medium text-slate-500 mt-1">{{ title }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  count: [String, Number],
  trend: String,
  icon: Object,
  iconBg: String,
  iconColor: String
})
</script>