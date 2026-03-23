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
            class="bg-white rounded-xl shadow-lg z-10 w-full max-w-[500px] max-h-[90vh] overflow-y-auto">
            <!-- Header -->
            <div class="bg-red-600 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3">
              <Filter class="w-5 h-5 md:w-6 md:h-6" />
              <h3 class="text-lg md:text-xl font-bold">FILTRAR PRODUTOS</h3>
            </div>

            <!-- Body -->
            <div class="p-4 sm:p-5 md:p-6">
              <div class="mb-4">
                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Nome do Produto</label>
                <input v-model="filters.name" type="text" placeholder="Digite o nome..."
                  class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] py-2 px-3 leading-tight focus:outline-none focus:border-red-500 focus:bg-white transition duration-200" />
              </div>

              <div class="mb-4">
                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Ordenar Por</label>
                <CustomSelect v-model="filters.sort_by" :options="sortOptions" placeholder="Padrão" />
              </div>

              <div class="mb-6">
                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Ordem</label>
                <CustomSelect v-model="filters.order" :options="orderOptions" />
              </div>

              <div class="flex flex-col sm:flex-row justify-center gap-3 md:gap-4">
                <button @click="apply"
                  class="w-full sm:flex-1 bg-neutral-700 hover:bg-neutral-800 active:scale-95 text-white font-bold py-2 px-6 rounded-lg transition duration-200">
                  APLICAR
                </button>
                <button @click="clear"
                  class="w-full sm:flex-1 bg-gray-300 hover:bg-gray-400 active:scale-95 text-gray-800 font-bold py-2 px-6 rounded-lg transition duration-200">
                  LIMPAR
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
import { ref, watch } from 'vue'
import { Filter, ArrowUpWideNarrow, ArrowDownWideNarrow } from 'lucide-vue-next'
import CustomSelect from '../CustomSelect.vue'

const props = defineProps({
  isOpen: Boolean,
  currentFilters: Object
})

const emit = defineEmits(['close', 'apply'])

const filters = ref({
  name: '',
  sort_by: '',
  order: 'asc'
})

const sortOptions = [
  { value: '', label: 'Padrão' },
  { value: 'nome', label: 'Nome' },
  { value: 'stock', label: 'Estoque Total' }
]

const orderOptions = [
  { value: 'asc', label: 'Crescente', icon: ArrowUpWideNarrow },
  { value: 'desc', label: 'Decrescente', icon: ArrowDownWideNarrow }
]

watch(() => props.isOpen, (isOpen) => {
  if (isOpen && props.currentFilters) {
    filters.value = { ...props.currentFilters }
  }
})

const apply = () => {
  emit('apply', filters.value)
}

const clear = () => {
  filters.value = { name: '', sort_by: '', order: 'asc' }
  emit('apply', filters.value)
}
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
