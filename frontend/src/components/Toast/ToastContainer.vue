<script setup>
import { useToastStore } from '../../stores/toast';
import ToastItem from './ToastItem.vue';

const store = useToastStore();
</script>

<template>
  <div
    class="fixed z-[100001] flex flex-col-reverse items-end gap-2 p-4 pointer-events-none sm:bottom-5 sm:right-5 bottom-2 right-2 w-full max-w-sm"
    style="z-index: 100001;"
  >
    <TransitionGroup
      enter-active-class="transform ease-out duration-300 transition-all"
      enter-from-class="translate-y-4 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transform ease-in duration-200 transition-all"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0 scale-95"
      move-class="transition-all duration-300 ease-in-out"
    >
      <ToastItem
        v-for="toast in store.toasts"
        :key="toast.id"
        :toast="toast"
      />
    </TransitionGroup>
  </div>
</template>
