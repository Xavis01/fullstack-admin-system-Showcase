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
            <div
              class="bg-red-600 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl">
              <Filter class="w-5 h-5 md:w-6 md:h-6" />
              <h3 class="text-lg md:text-xl font-bold">FILTRAR VENDAS</h3>
            </div>

            <!-- Body -->
            <div class="p-4 sm:p-5 md:p-6">
              <div class="mb-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">ID da Venda</label>
                  <input v-model="filters.sale_id" type="number" placeholder="Ex: 15"
                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] py-2 px-3 leading-tight focus:outline-none focus:border-red-500 focus:bg-white transition duration-200" />
                </div>

                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Número do Lote</label>
                  <input v-model="filters.num_lote" type="number" placeholder="Ex: 2205"
                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] py-2 px-3 leading-tight focus:outline-none focus:border-red-500 focus:bg-white transition duration-200" />
                </div>
              </div>

              <div class="mb-4">
                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Cliente</label>
                <CustomSelect v-model="filters.client_id" :options="clientOptions" placeholder="Todos os clientes"
                  :loading="loadingClients" />
              </div>

              <div class="mb-4">
                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Produto</label>
                <CustomSelect v-model="filters.product_id" :options="productOptions" placeholder="Todos os produtos"
                  :loading="loadingProducts" />
              </div>

              <div class="mb-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Data Início</label>
                  <CustomCalendar v-model="filters.start_date" placeholder="Início" />
                </div>
                <div>
                  <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Data Fim</label>
                  <CustomCalendar v-model="filters.end_date" placeholder="Fim" />
                </div>
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
import { Filter } from 'lucide-vue-next'
import CustomSelect from '../CustomSelect.vue'
import CustomCalendar from '../CustomCalendar.vue'
import { useUserStore } from '../../stores/user'

const props = defineProps({
  isOpen: Boolean,
  currentFilters: Object
})

const emit = defineEmits(['close', 'apply'])
const userStore = useUserStore()

const filters = ref({
  sale_id: '',
  num_lote: '',
  client_id: '',
  product_id: '',
  start_date: '',
  end_date: ''
})

const clientOptions = ref([])
const productOptions = ref([])
const loadingClients = ref(false)
const loadingProducts = ref(false)

const fetchClients = async () => {
  loadingClients.value = true
  try {
    const response = await fetch('/api/clients', {
      headers: { 'Authorization': `Bearer ${userStore.token}` }
    })
    if (response.ok) {
      const data = await response.json()
      clientOptions.value = data.map(c => ({
        value: c.id,
        label: c.nome
      }))
    }
  } catch (e) {
    console.error(e)
  } finally {
    loadingClients.value = false
  }
}

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
    if (props.currentFilters) {
      filters.value = { ...props.currentFilters }
    }

    // Defer fetch to allow modal animation to complete concurrently
    setTimeout(() => {
      if (clientOptions.value.length === 0) fetchClients()
      if (productOptions.value.length === 0) fetchProducts()
    }, 350)
  }
})

const apply = () => {
  emit('apply', filters.value)
}

const clear = () => {
  filters.value = { sale_id: '', num_lote: '', client_id: '', product_id: '', start_date: '', end_date: '' }
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
