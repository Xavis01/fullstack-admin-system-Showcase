<template>
  <div>
    <!-- Blur Layer with synchronized transition -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 z-40"
        style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
      </div>
    </transition>

    <!-- Animated Overlay & Modal -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 font-montserrat p-4 md:pt-20">
        <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
        <transition name="modal">
          <div v-if="isOpen"
            class="bg-white rounded-xl shadow-lg z-10 w-full max-w-[600px] max-h-[90vh] overflow-y-auto">
            <!-- Header -->
            <div
              class="bg-neutral-700 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3">
              <Users class="w-5 h-5 md:w-6 md:h-6" />
              <h3 class="text-lg md:text-xl font-bold">{{ client ? 'EDITAR CLIENTE' : 'CADASTRO DE CLIENTE' }}</h3>
            </div>
            <!-- Body content omitted for brevity -->
            <div class="p-4 sm:p-6 md:p-8">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-6">
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Nome (Razão Social)</label>
                  <input v-model="formData.nome" type="text" placeholder="Digite o nome..."
                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-4 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200" />
                </div>
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Número de Telefone</label>
                  <input v-model="formData.telefone" type="text" placeholder="(00) 00000-0000"
                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-4 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200"
                    @input="handlePhoneInput" />
                </div>
              </div>

              <div class="flex justify-center">
                <button @click="save"
                  class="bg-red-600 hover:bg-red-700 active:scale-95 text-white font-bold py-3 px-12 rounded-lg transition duration-200 w-full flex justify-center items-center"
                  :disabled="loading">
                  <span v-if="!loading">CONFIRMAR</span>
                  <LoaderCircle v-else class="animate-spin w-5 h-5 md:w-6 md:h-6" />
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
import { LoaderCircle, Users } from 'lucide-vue-next'
import { useToastStore } from '../../stores/toast'

const toastStore = useToastStore()

const props = defineProps({
  isOpen: Boolean,
  client: Object,
  loading: Boolean
})

const emit = defineEmits(['close', 'save'])

const formData = ref({
  nome: '',
  telefone: ''
})

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    if (props.client) {
      formData.value = { ...props.client }
    } else {
      formData.value = { nome: '', telefone: '' }
    }
  }
})

const handlePhoneInput = (event) => {
  // Remove non-numeric characters
  formData.value.telefone = event.target.value.replace(/\D/g, '')
}

const save = () => {
  if (!formData.value.nome || !formData.value.nome.trim()) {
    toastStore.add({
      title: 'Campos Obrigatórios ou Inválidos',
      message: 'Verifique: Nome (Razão Social)',
      type: 'warning'
    })
    return
  }
  emit('save', formData.value)
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
