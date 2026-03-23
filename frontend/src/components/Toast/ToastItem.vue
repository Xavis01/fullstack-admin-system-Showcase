<script setup>
import { onMounted } from 'vue';
import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from 'lucide-vue-next';
import { useToastStore } from '../../stores/toast';

const props = defineProps({
  toast: {
    type: Object,
    required: true,
  },
});

const store = useToastStore();

const icons = {
  success: CheckCircle,
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
};

// Border colors for the left strip
const borderColors = {
  success: 'border-green-500',
  error: 'border-red-600',
  warning: 'border-yellow-500',
  info: 'border-blue-500',
};

// Icon colors
const iconColors = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500'
}

function close() {
  store.remove(props.toast.id);
}
</script>

<template>
  <div
    class="relative flex items-center gap-4 p-4 mb-3 rounded-lg shadow-2xl transition-all duration-300 w-full max-w-sm pointer-events-auto bg-[#1a1a1a] border-l-4 border-gray-700"
    :class="[borderColors[toast.type]]"
  >
    <!-- Icon -->
    <component :is="icons[toast.type]" class="w-6 h-6 shrink-0" :class="iconColors[toast.type]" />

    <!-- Content -->
    <div class="flex-1">
      <h3 v-if="toast.title" class="font-bold text-sm text-white mb-0.5 leading-tight">
        {{ toast.title }}
      </h3>
      <p class="text-xs text-gray-300 leading-relaxed">{{ toast.message }}</p>
    </div>

    <!-- Close Button -->
    <button
      @click="close"
      class="shrink-0 p-1.5 hover:bg-white/10 rounded-md transition-colors text-gray-400 hover:text-white"
    >
      <X class="w-4 h-4" />
    </button>
  </div>
</template>

<style scoped>
</style>
