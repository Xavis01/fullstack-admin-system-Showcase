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
            class="bg-white rounded-xl shadow-lg z-10 w-full max-w-[600px] max-h-[90vh] overflow-y-auto">
            <!-- Header -->
            <div
              class="bg-neutral-700 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl">
              <ShieldUser class="w-5 h-5 md:w-6 md:h-6" />
              <h3 class="text-lg md:text-xl font-bold">{{ user ? 'EDITAR USUÁRIO' : 'NOVO USUÁRIO' }}</h3>
            </div>

            <!-- Body -->
            <div class="p-4 sm:p-6 md:p-8">
              <!-- Nome -->
              <div class="mb-4 md:mb-6">
                <label class="block text-gray-700 text-sm font-bold mb-2">Nome Completo</label>
                <input v-model="formData.nome" type="text"
                  class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-4 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200"
                  placeholder="Digite o nome completo" />
              </div>

              <!-- Email -->
              <div class="mb-4 md:mb-6">
                <label class="block text-gray-700 text-sm font-bold mb-2">Email</label>
                <input v-model="formData.email" type="email"
                  class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-4 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200"
                  placeholder="email@escorpiao.com.br" />
              </div>

              <!-- Data de Nascimento e Senha (Grid Responsivo) -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-4 md:mb-6">
                <!-- Data de Nascimento -->
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">Data de Nascimento</label>
                  <CustomCalendar v-model="formData.dt_nascimento" placeholder="Selecione a data" position="top" />
                </div>

                <!-- Senha -->
                <div>
                  <label class="block text-gray-700 text-sm font-bold mb-2">
                    {{ user ? 'Nova Senha (Opcional)' : 'Senha' }}
                  </label>
                  <input v-model="formData.password" type="password"
                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-4 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200"
                    placeholder="******" />
                </div>
              </div>

              <!-- Checkbox Admin -->
              <div class="flex items-center cursor-pointer mb-3 md:mb-4 select-none"
                @click="formData.is_admin = !formData.is_admin">
                <div
                  class="w-5 h-5 border-2 border-gray-300 rounded flex items-center justify-center transition-colors duration-200"
                  :class="formData.is_admin ? 'bg-red-600 border-red-600' : 'bg-white'">
                  <Check v-if="formData.is_admin" class="w-3.5 h-3.5 text-white" stroke-width="3" />
                </div>
                <span class="ml-2 text-xs md:text-sm font-bold text-gray-700">CONCEDER ACESSO ADMINISTRATIVO</span>
              </div>

              <!-- Checkbox Master -->
              <div class="flex items-center cursor-pointer mb-6 md:mb-8 select-none"
                @click="formData.is_master = !formData.is_master">
                <div
                  class="w-5 h-5 border-2 border-gray-300 rounded flex items-center justify-center transition-colors duration-200"
                  :class="formData.is_master ? 'bg-red-600 border-red-600' : 'bg-white'">
                  <Check v-if="formData.is_master" class="w-3.5 h-3.5 text-white" stroke-width="3" />
                </div>
                <span class="ml-2 text-xs md:text-sm font-bold text-gray-700">CONCEDER ACESSO MASTER</span>
              </div>

              <!-- Action Buttons (Responsivo) -->
              <div class="flex flex-col sm:flex-row justify-center gap-3 md:gap-4">
                <button @click="$emit('close')"
                  class="w-full sm:w-auto order-2 sm:order-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-3 px-6 md:px-8 rounded-lg transition duration-200 active:scale-95"
                  type="button">
                  CANCELAR
                </button>
                <button @click="submitForm"
                  class="w-full sm:flex-1 order-1 sm:order-2 bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 md:px-12 rounded-lg transition duration-200 flex items-center justify-center gap-2 active:scale-95"
                  :disabled="loading">
                  <LoaderCircle v-if="loading" class="animate-spin w-5 h-5 md:w-6 md:h-6" />
                  {{ user ? 'SALVAR ALTERAÇÕES' : 'CRIAR USUÁRIO' }}
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
import { ShieldUser, LoaderCircle, Check } from 'lucide-vue-next'
import CustomCalendar from '../CustomCalendar.vue'

const props = defineProps({
  isOpen: Boolean,
  user: Object,
  loading: Boolean
})

const emit = defineEmits(['close', 'save'])

const formData = ref({
  nome: '',
  email: '',
  dt_nascimento: '',
  password: '',
  is_admin: false,
  is_master: false
})

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    if (props.user) {
      formData.value = {
        id: props.user.id,
        nome: props.user.nome || '',
        email: props.user.email || '',
        dt_nascimento: props.user.dt_nascimento || '',
        password: '',
        is_admin: props.user.is_admin || false,
        is_master: props.user.is_master || false
      }
    } else {
      formData.value = {
        nome: '',
        email: '',
        dt_nascimento: '',
        password: '',
        is_admin: false,
        is_master: false
      }
    }
  }
})

const submitForm = () => {
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
