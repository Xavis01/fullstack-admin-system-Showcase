<template>
  <div>
    <!-- Blur Layer with synchronized transition -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 z-40"
        style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
      </div>
    </transition>

    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center font-montserrat p-4 md:pt-20"
        :class="zIndexClass">
        <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
        <transition name="modal">
          <div v-if="isOpen"
            class="bg-white rounded-xl shadow-lg z-10 w-full max-w-[600px] max-h-[90vh] overflow-y-auto">
            <!-- Header -->
            <div
              class="bg-neutral-700 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl">
              <Boxes class="w-5 h-5 md:w-6 md:h-6" />
              <h3 class="text-lg md:text-xl font-bold">{{ production ? 'EDITAR LOTE' : 'NOVO LOTE' }}</h3>
            </div>
            <!-- Body Content Omitted -->
            <div class="p-4 sm:p-6 md:p-8">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-4 md:mb-6">
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Número do Lote</label>
                  <input v-model="formData.num_lote" type="number" placeholder="Ex: 2205"
                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-4 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200"
                    :disabled="!!production" />
                  <!-- Note: num_lote is PK, so maybe disable edit if it's an update? Backend allows update but PK update is tricky. Usually PK is immutable. Let's assume immutable for edit. -->
                </div>
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Produto</label>
                  <CustomSelect v-model="formData.product_id" :options="productOptions"
                    placeholder="Selecione o produto" :loading="loadingProducts" />
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-4 md:mb-6">
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Quantidade Produzida</label>
                  <div class="relative">
                    <input v-model="formData.quant_caixa_produzida" type="number" placeholder="0"
                      class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-4 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200" />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 font-semibold text-sm">{{
                      isSacosProduct ? 'Sacos' : 'Caixas' }}</span>
                  </div>
                </div>
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Data de Produção</label>
                  <CustomCalendar v-model="formData.data_producao" placeholder="Selecione a data" />
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
import { ref, watch, onMounted, computed } from 'vue'
import { LoaderCircle, Boxes } from 'lucide-vue-next'
import CustomSelect from '../CustomSelect.vue'
import CustomCalendar from '../CustomCalendar.vue'
import { useUserStore } from '../../stores/user'
import { useToastStore } from '../../stores/toast'
import { useRoute } from 'vue-router'

const toastStore = useToastStore()

const props = defineProps({
  isOpen: Boolean,
  production: Object,
  initialData: Object,
  loading: Boolean,
  zIndexClass: {
    type: String,
    default: 'z-50'
  }
})

const emit = defineEmits(['close', 'save'])
const userStore = useUserStore()

const formData = ref({
  num_lote: '',
  product_id: '',
  quant_caixa_produzida: '',
  data_producao: ''
})

const productOptions = ref([])
const loadingProducts = ref(false)

const isSacosProduct = computed(() => {
  const selectedProduct = productOptions.value.find(p => p.value === formData.value.product_id)
  return selectedProduct?.label?.toUpperCase().includes('25KG') ?? false
})

const fetchProducts = async () => {
  loadingProducts.value = true
  try {
    const response = await fetch('/api/products', {
      headers: { 'Authorization': `Bearer ${userStore.token}` }
    })
    if (response.ok) {
      const data = await response.json()
      productOptions.value = data.map(p => {
        let imageUrl = null
        if (p.image_path) {
          if (p.image_path.startsWith('http')) {
            imageUrl = p.image_path
          } else {
            let cleanPath = p.image_path.replace(/^backend[\\/]/, '').replace(/\\/g, '/')
            imageUrl = `/${cleanPath}`
          }
        }
        return {
          value: p.id,
          label: p.nome,
          image: imageUrl
        }
      })
    }
  } catch (e) {
    console.error(e)
  } finally {
    loadingProducts.value = false
  }
}

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    if (props.production) {
      formData.value = {
        ...props.production,
        // Ensure date is formatted correctly for calendar (YYYY-MM-DD)
        data_producao: props.production.data_producao ? new Date(props.production.data_producao).toISOString().split('T')[0] : ''
      }
    } else if (props.initialData) {
      // Pre-fill from initialData (e.g. from ReturnManager)
      const today = new Date().toISOString().split('T')[0]
      formData.value = {
        num_lote: '', // Always empty for new lot
        product_id: props.initialData.product_id || '',
        quant_caixa_produzida: props.initialData.quant_caixa_produzida || '',
        data_producao: today
      }
    } else {
      // Default to today
      const today = new Date().toISOString().split('T')[0]
      formData.value = {
        num_lote: '',
        product_id: '',
        quant_caixa_produzida: '',
        data_producao: today
      }
    }

    // Defer fetch to allow modal animation to complete concurrently
    setTimeout(() => {
      fetchProducts() // Ensure products are loaded
    }, 350)
  }
})

const save = () => {
  const errors = []

  if (!formData.value.num_lote || !String(formData.value.num_lote).trim()) {
    errors.push('Número do Lote')
  }
  if (!formData.value.product_id) {
    errors.push('Produto')
  }
  if (!formData.value.quant_caixa_produzida || Number(formData.value.quant_caixa_produzida) <= 0) {
    errors.push('Quantidade Produzida (deve ser maior que 0)')
  }
  if (!formData.value.data_producao) {
    errors.push('Data de Produção')
  }

  if (errors.length > 0) {
    toastStore.add({
      title: 'Campos Obrigatórios ou Inválidos',
      message: 'Verifique: ' + errors.join(', '),
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

/* Hide number input spinners */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}
</style>
