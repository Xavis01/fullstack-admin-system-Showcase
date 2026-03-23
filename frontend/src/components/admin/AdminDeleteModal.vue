<template>
  <div>
    <!-- Blur Layer with synchronized transition -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 z-40"
        style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
      </div>
    </transition>

    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center flex-col z-50">
        <div class="fixed inset-0 bg-black bg-opacity-50" @click="$emit('close')"></div>
        <transition name="modal">
          <div v-if="isOpen" class="bg-white rounded-xl shadow-lg z-10 w-[400px] overflow-hidden">
            <div class="p-6 text-center">
              <div class="bg-red-100 p-3 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <AlertTriangle class="text-red-600 w-8 h-8" />
              </div>
              <h3 class="text-xl font-bold text-neutral-800 mb-2">Excluir Usuário?</h3>
              <p class="text-gray-600 mb-6">
                Tem certeza que deseja excluir <strong>{{ itemName }}</strong>? Esta ação não pode ser desfeita.
              </p>

              <div class="flex gap-3 justify-center">
                <button @click="$emit('close')"
                  class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-semibold transition">
                  CANCELAR
                </button>
                <button @click="$emit('confirm')" :disabled="loading"
                  class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-bold shadow-lg transition disabled:opacity-50 flex items-center gap-2">
                  <LoaderCircle v-if="loading" class="animate-spin w-6 h-6" />
                  SIM, EXCLUIR
                </button>
              </div>
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
