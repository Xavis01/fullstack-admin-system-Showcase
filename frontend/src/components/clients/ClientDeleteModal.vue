<template>
  <div>
    <!-- Blur Layer with synchronized transition -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 z-40"
        style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
      </div>
    </transition>

    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 font-montserrat p-4 md:pt-20">
        <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
        <transition name="modal">
          <div v-if="isOpen"
            class="bg-white rounded-xl shadow-lg p-4 sm:p-5 md:p-6 z-10 w-full max-w-[400px] text-center">
            <div class="flex justify-center mb-3 md:mb-4 text-red-600">
              <AlertTriangle class="w-10 h-10 md:w-12 md:h-12" />
            </div>
            <h3 class="text-base md:text-lg font-bold mb-4">Tem certeza que deseja deletar {{ itemName }}?</h3>
            <div class="flex flex-col sm:flex-row justify-center gap-3 md:gap-4">
              <button @click="$emit('confirm')"
                class="w-full sm:flex-1 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-bold py-2 px-6 rounded-lg transition duration-200 flex items-center justify-center min-w-[80px]"
                :disabled="loading">
                <span v-if="!loading">SIM</span>
                <LoaderCircle v-else class="animate-spin w-5 h-5 md:w-6 md:h-6" />
              </button>
              <button @click="$emit('close')"
                class="w-full sm:flex-1 bg-gray-300 hover:bg-gray-400 active:scale-95 text-gray-800 font-bold py-2 px-6 rounded-lg transition duration-200"
                :disabled="loading">
                NÃO
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { LoaderCircle, AlertTriangle } from 'lucide-vue-next'

defineProps({
  isOpen: Boolean,
  itemName: String,
  loading: Boolean
})

defineEmits(['close', 'confirm'])
</script>

<style scoped>
.modal-backdrop-enter-active,
.modal-backdrop-leave-active {
  transition: opacity 0.3s ease;
}

.modal-backdrop-enter-from,
.modal-backdrop-leave-to {
  opacity: 0;
}

.modal-backdrop-enter-active .modal-backdrop-blur {
  backdrop-filter: blur(0px);
  -webkit-backdrop-filter: blur(0px);
}

.modal-backdrop-leave-to .modal-backdrop-blur {
  backdrop-filter: blur(0px);
  -webkit-backdrop-filter: blur(0px);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(-20px);
}
</style>
