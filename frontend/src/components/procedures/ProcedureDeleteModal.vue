<template>
  <div>
    <!-- Blur Backdrop -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 z-40"
        style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
      </div>
    </transition>

    <!-- Overlay & Modal -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 font-montserrat p-4">
        <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
        <transition name="modal">
          <div v-if="isOpen" class="bg-white rounded-3xl shadow-2xl w-full max-w-sm p-6 md:p-8 z-10 text-center">

            <div class="flex justify-center mb-4 text-red-600">
              <AlertTriangle class="w-12 h-12" />
            </div>

            <h3 class="text-lg font-bold text-neutral-800 mb-2">Excluir Procedimento</h3>
            <p class="text-neutral-600 text-sm mb-1">Tem certeza que deseja excluir:</p>
            <p class="font-bold text-neutral-800 mb-3">{{ procedure?.nome }}</p>
            <p class="text-xs text-neutral-400 mb-6">O arquivo será permanentemente removido do sistema.</p>

            <div class="flex gap-3">
              <button @click="$emit('close')" :disabled="loading"
                class="flex-1 py-2.5 rounded-xl bg-gray-300 hover:bg-gray-400 active:scale-95 text-gray-800 font-bold transition text-sm">
                NÃO
              </button>
              <button @click="$emit('confirm')" :disabled="loading"
                class="flex-1 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 active:scale-95 text-white font-bold transition text-sm disabled:opacity-50 flex items-center justify-center gap-2">
                <LoaderCircle v-if="loading" class="animate-spin w-4 h-4" />
                <span v-else>SIM</span>
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { AlertTriangle, LoaderCircle } from 'lucide-vue-next'

defineProps({
  isOpen: Boolean,
  procedure: Object,
  loading: Boolean
})

defineEmits(['close', 'confirm'])
</script>

<style scoped>
.modal-backdrop-enter-active,
.modal-backdrop-leave-active { transition: opacity 0.3s ease; }
.modal-backdrop-enter-from,
.modal-backdrop-leave-to { opacity: 0; }

.modal-enter-active,
.modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from,
.modal-leave-to { opacity: 0; transform: scale(0.9) translateY(-20px); }
</style>
