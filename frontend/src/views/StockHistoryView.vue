<template>
  <div id="background" class="min-h-screen bg-gray-200 font-montserrat">
    <section id="stock-history">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
        <!-- Header -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 md:mb-8 gap-4">
          <div class="flex items-center gap-2 md:gap-4">
            <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
              <ScrollText class="text-white w-6 h-6 md:w-8 md:h-8" />
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">MOVIMENTAÇÕES
            </h2>
          </div>
          <div class="flex flex-col sm:flex-row gap-2 md:gap-4 w-full lg:w-auto">
            <button @click="showSnapshotPanel = !showSnapshotPanel; showFilters = false"
              class="w-full sm:w-auto bg-white hover:bg-gray-50 active:scale-95 text-red-600 font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2 border border-red-600">
              <CalendarClock class="w-5 h-5" />
              {{ showSnapshotPanel ? 'OCULTAR POSIÇÃO' : 'POSIÇÃO DE ESTOQUE' }}
            </button>
            <button @click="showFilters = !showFilters; showSnapshotPanel = false"
              class="w-full sm:w-auto bg-red-600 hover:bg-red-700 active:scale-95 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Filter class="w-5 h-5" />
              {{ showFilters ? 'OCULTAR FILTROS' : 'FILTRAR' }}
            </button>
            <button v-if="hasActiveFilters" @click="clearFilters"
              class="w-full sm:w-auto bg-white hover:bg-gray-50 active:scale-95 text-neutral-600 font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2 border border-gray-300">
              <X class="w-5 h-5" />
              LIMPAR
            </button>
          </div>
        </div>

        <!-- Stock Snapshot Panel (New Section) -->
        <transition name="slide">
          <div v-if="showSnapshotPanel"
            class="bg-white rounded-2xl shadow-lg p-4 md:p-6 mb-6 border-2 border-red-100 animate-fade-in relative overflow-hidden">
            <div class="absolute top-0 right-0 p-4 opacity-10">
              <CalendarClock class="w-24 h-24 text-red-600" />
            </div>
            <div class="relative z-10">
              <h3 class="text-lg font-bold text-neutral-800 mb-4 flex items-center gap-2">
                <Box class="text-red-600" />
                POSIÇÃO DE ESTOQUE RETROATIVA
              </h3>
              <p class="text-sm text-neutral-500 mb-6">Consulte a quantidade exata de estoque que o sistema possuía em
                qualquer data/horário passado.</p>

              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 items-end">
                <div>
                  <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Data da Consulta</label>
                  <CustomCalendar v-model="snapshotFilter.date" placeholder="dd/mm/aaaa" />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Horário (Opcional)</label>
                  <CustomTimePicker v-model="snapshotFilter.time" placeholder="HH:mm" />
                </div>
                <div>
                  <button @click="fetchStockSnapshot" :disabled="isFetchingSnapshot"
                    class="w-full h-11 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-semibold rounded-lg shadow transition duration-200 flex items-center justify-center gap-2 disabled:opacity-50">
                    <Search v-if="!isFetchingSnapshot" class="w-5 h-5" />
                    <LoaderCircle v-else class="w-5 h-5 animate-spin" />
                    {{ isFetchingSnapshot ? 'CONSULTANDO...' : 'CONSULTAR AGORA' }}
                  </button>
                </div>
              </div>

              <!-- Results Area -->
              <div v-if="stockSnapshotResult" class="mt-8 animate-fade-in">
                <div class="bg-gray-50 rounded-xl p-4 md:p-6 border border-gray-200">
                  <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
                    <div>
                      <p class="text-xs font-bold text-neutral-400 uppercase tracking-widest">RESULTADO DA POSIÇÃO EM
                      </p>
                      <h4 class="text-xl font-extrabold text-neutral-800">
                        {{ formatDate(stockSnapshotResult.date) }} <span class="text-red-600">{{
                          stockSnapshotResult.time }}</span>
                      </h4>
                    </div>
                    <div class="bg-red-600 text-white px-6 py-3 rounded-xl shadow-lg text-center">
                      <p class="text-[10px] uppercase font-bold opacity-80">Estoque Total Geral</p>
                      <p class="text-2xl font-black">{{ stockSnapshotResult.total_geral }} <span
                          class="text-xs font-normal">UNID.</span></p>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="prod in stockSnapshotResult.stock_by_product" :key="prod.product_id"
                      class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm flex items-center justify-between hover:border-red-200 transition">
                      <div class="flex items-center gap-3">
                        <div class="bg-gray-100 p-2 rounded-lg flex-shrink-0">
                          <img v-if="prod.product_image" :src="prod.product_image" class="w-8 h-8 rounded-full object-cover border border-gray-200" alt="" />
                          <Package v-else class="text-neutral-500 w-5 h-5 mx-1.5 my-1.5" />
                        </div>
                        <div>
                          <p class="text-sm font-bold text-neutral-800 truncate max-w-[150px]">{{ prod.product_name }}
                          </p>
                          <p class="text-[10px] text-neutral-400 uppercase font-bold">{{ prod.lotes_count }} Lotes Ativos
                          </p>
                        </div>
                      </div>
                      <div class="text-right">
                        <p class="text-lg font-black text-red-600">{{ prod.total_stock }}</p>
                        <p class="text-[10px] text-neutral-400 font-bold uppercase">unid.</p>
                      </div>
                    </div>
                  </div>

                  <p v-if="stockSnapshotResult.stock_by_product.length === 0" class="text-center py-8 text-neutral-500 italic">
                    Nenhum estoque encontrado nesta data.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </transition>

        <!-- Filters Panel -->
        <transition name="slide">
          <div v-if="showFilters"
            class="bg-white rounded-2xl shadow-lg p-4 md:p-6 mb-6 border border-gray-200 animate-fade-in">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <!-- Date Start -->
              <div>
                <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Data Inicial</label>
                <CustomCalendar v-model="filters.start_date" placeholder="dd/mm/aaaa" />
              </div>
              <!-- Date End -->
              <div>
                <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Data Final</label>
                <CustomCalendar v-model="filters.end_date" placeholder="dd/mm/aaaa" />
              </div>
              <!-- Time Start -->
              <div>
                <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Horário Inicial</label>
                <CustomTimePicker v-model="filters.start_time" placeholder="HH:mm" />
              </div>
              <!-- Time End -->
              <div>
                <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Horário Final</label>
                <CustomTimePicker v-model="filters.end_time" placeholder="HH:mm" />
              </div>
              <!-- Product Filter -->
              <div>
                <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Produto</label>
                <CustomSelect v-model="filters.product_id" :options="productOptions" placeholder="Todos os Produtos" />
              </div>
              <!-- Type Filter -->
              <div>
                <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Tipo</label>
                <CustomSelect v-model="filters.tipo" :options="typeOptions" placeholder="Todos os Tipos" />
              </div>
              <!-- Lote Filter -->
              <div>
                <label class="block text-xs font-semibold text-neutral-500 uppercase mb-1">Lote</label>
                <input type="text" v-model="filters.num_lote" placeholder="Buscar por nº do lote"
                  class="w-full h-11 px-3 rounded-lg border border-gray-300 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition text-sm" />
              </div>
              <!-- Apply Button -->
              <div class="flex items-end">
                <button @click="fetchMovements"
                  class="w-full h-11 bg-neutral-700 hover:bg-neutral-800 active:scale-95 text-white font-semibold rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
                  <Search class="w-5 h-5" />
                  BUSCAR
                </button>
              </div>
            </div>
          </div>
        </transition>

        <!-- Loading State -->
        <div v-if="isFetching" class="flex justify-center items-center h-64">
          <LoaderCircle class="animate-spin text-neutral-700 w-8 h-8 md:w-12 md:h-12" />
        </div>

        <!-- Empty State -->
        <div v-else-if="movements.length === 0"
          class="flex flex-col items-center justify-center h-64 text-gray-500">
          <ScrollText class="mb-4 text-gray-400 w-12 h-12 md:w-16 md:h-16" />
          <p class="text-lg md:text-xl font-semibold">Nenhuma movimentação encontrada</p>
          <p class="text-xs md:text-sm mt-2">
            {{ hasActiveFilters ? 'Tente ajustar os filtros' : 'As movimentações serão registradas automaticamente' }}
          </p>
        </div>

        <!-- Data -->
        <div v-else class="relative">
          <!-- Count -->
          <div class="flex justify-between items-center mb-4">
            <span class="text-sm text-gray-600">{{ movements.length }} {{ movements.length === 1 ? 'movimentação' :
              'movimentações' }}</span>
          </div>

          <!-- Desktop Table -->
          <div class="hidden lg:block animate-fade-in rounded-2xl shadow-lg">
            <div
              class="bg-neutral-700 text-white grid grid-cols-[160px_2fr_2fr_100px_1fr_120px_2fr] gap-4 px-6 py-4 font-bold text-sm uppercase rounded-t-2xl items-center">
              <div>DATA/HORA</div>
              <div>TIPO</div>
              <div>PRODUTO</div>
              <div>LOTE</div>
              <div>QUANTIDADE</div>
              <div>ESTOQUE APÓS</div>
              <div>RESPONSÁVEL</div>
            </div>

            <div
              class="max-h-[500px] overflow-y-auto relative scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200 rounded-b-2xl bg-white custom-scrollbar">
              <div v-for="item in movements" :key="item.id"
                class="bg-white grid grid-cols-[160px_2fr_2fr_100px_1fr_120px_2fr] gap-4 px-6 py-4 border-b border-gray-200 hover:bg-red-50 transition relative last:border-b-0 items-center">
                <!-- Date/Time -->
                <div class="text-neutral-800 text-sm">
                  <div class="font-semibold">{{ formatDate(item.created_at) }}</div>
                  <div class="text-neutral-500 text-xs">{{ formatTime(item.created_at) }}</div>
                </div>
                <!-- Type -->
                <div>
                  <span :class="getTypeBadgeClass(item.tipo)"
                    class="px-2.5 py-1 rounded-full text-xs font-bold whitespace-nowrap">
                    {{ getTypeLabel(item.tipo) }}
                  </span>
                </div>
                <!-- Product -->
                <div class="flex items-center gap-3">
                  <img v-if="item.product_image" :src="item.product_image"
                    class="w-8 h-8 rounded-full object-cover border border-gray-200" alt="" />
                  <div v-else class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-400">
                    <Package size="16" />
                  </div>
                  <div class="text-neutral-800 font-semibold text-sm truncate">{{ item.product_name }}</div>
                </div>
                <!-- Lote -->
                <div class="font-bold text-neutral-800">#{{ item.num_lote }}</div>
                <!-- Quantity -->
                <div :class="item.quantidade > 0 ? 'text-green-600' : 'text-red-600'" class="font-bold">
                  {{ item.quantidade > 0 ? '+' : '' }}{{ item.quantidade }}
                </div>
                <!-- Stock After -->
                <div class="text-neutral-800 font-semibold">{{ item.estoque_apos }}</div>
                <!-- Responsible -->
                <div class="text-neutral-600 text-sm truncate">{{ item.created_by_name || '—' }}</div>
              </div>
            </div>
          </div>

          <!-- Mobile Cards -->
          <div class="block lg:hidden">
            <div class="space-y-4 animate-fade-in">
              <div v-for="item in movements" :key="item.id"
                class="bg-white rounded-2xl shadow-lg p-4 border border-gray-200">
                <!-- Header -->
                <div class="flex items-start justify-between mb-3 pb-3 border-b border-gray-100">
                  <div class="flex items-center gap-3 flex-1 min-w-0">
                    <img v-if="item.product_image" :src="item.product_image"
                      class="w-12 h-12 rounded-full object-cover border-2 border-gray-200 flex-shrink-0" alt="" />
                    <div v-else
                      class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                      <Package :size="20" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="font-bold text-neutral-800 text-lg">#{{ item.num_lote }}</div>
                      <div class="text-sm text-neutral-600 truncate">{{ item.product_name }}</div>
                    </div>
                  </div>
                  <span :class="getTypeBadgeClass(item.tipo)"
                    class="px-2.5 py-1 rounded-full text-xs font-bold whitespace-nowrap flex-shrink-0 ml-2">
                    {{ getTypeLabel(item.tipo) }}
                  </span>
                </div>

                <!-- Quantity Badge -->
                <div class="flex items-center justify-between mb-3">
                  <span :class="item.quantidade > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
                    class="px-3 py-1 rounded-full text-sm font-bold">
                    {{ item.quantidade > 0 ? '+' : '' }}{{ item.quantidade }} Caixas
                  </span>
                  <span class="text-sm text-neutral-500 font-semibold">
                    Estoque: {{ item.estoque_apos }}
                  </span>
                </div>

                <!-- Details -->
                <div class="space-y-2 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[90px]">Data:</span>
                    <span class="text-neutral-700">{{ formatDate(item.created_at) }} às {{ formatTime(item.created_at)
                      }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[90px]">Responsável:</span>
                    <span class="text-neutral-700">{{ item.created_by_name || '—' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ScrollText, Filter, LoaderCircle, Package, Search, X, CalendarClock, Box } from 'lucide-vue-next'
import CustomCalendar from '../components/CustomCalendar.vue'
import CustomTimePicker from '../components/CustomTimePicker.vue'
import CustomSelect from '../components/CustomSelect.vue'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

userStore.ensureValidSession(router)

const movements = ref([])
const products = ref([])
const isFetching = ref(false)
const showFilters = ref(false)

// Stock Snapshot (Position at date) refs
const showSnapshotPanel = ref(false)
const isFetchingSnapshot = ref(false)
const stockSnapshotResult = ref(null)
const snapshotFilter = ref({
  date: new Date().toISOString().split('T')[0],
  time: '23:59'
})

const filters = ref({
  start_date: '',
  end_date: '',
  start_time: '',
  end_time: '',
  product_id: '',
  tipo: '',
  num_lote: ''
})

const hasActiveFilters = computed(() => {
  return !!(
    filters.value.start_date ||
    filters.value.end_date ||
    filters.value.start_time ||
    filters.value.end_time ||
    filters.value.product_id ||
    filters.value.tipo ||
    filters.value.num_lote
  )
})

const clearFilters = () => {
  filters.value = {
    start_date: '',
    end_date: '',
    start_time: '',
    end_time: '',
    product_id: '',
    tipo: '',
    num_lote: ''
  }
  fetchMovements()
}

const productOptions = computed(() => {
  return [
    { value: '', label: 'Todos os Produtos' },
    ...products.value.map(p => ({
      value: p.id,
      label: p.nome,
      image: p.image_url || null
    }))
  ]
})

const typeOptions = [
  { value: '', label: 'Todos os Tipos' },
  { value: 'initial_snapshot', label: 'Snapshot Inicial' },
  { value: 'production_created', label: 'Produção Criada' },
  { value: 'production_edited', label: 'Produção Editada' },
  { value: 'sale_created', label: 'Venda Criada' },
  { value: 'sale_edited', label: 'Venda Editada' },
  { value: 'sale_edit_rollback', label: 'Venda Editada (Rollback)' },
  { value: 'sale_deleted', label: 'Venda Excluída' },
  { value: 'return_concluded', label: 'Devolução Concluída' },
  { value: 'return_deleted', label: 'Devolução Excluída' }
]

const fetchStockSnapshot = async () => {
  if (!snapshotFilter.value.date) return
  isFetchingSnapshot.value = true
  try {
    const params = new URLSearchParams({
      date: snapshotFilter.value.date
    })
    if (snapshotFilter.value.time) params.append('time', snapshotFilter.value.time)

    const response = await fetch(`/api/stock-at-date?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${userStore.token}` }
    })
    if (response.ok) {
      stockSnapshotResult.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching stock snapshot:', error)
  } finally {
    isFetchingSnapshot.value = false
  }
}

const fetchMovements = async () => {
  isFetching.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.start_date) params.append('start_date', filters.value.start_date)
    if (filters.value.end_date) params.append('end_date', filters.value.end_date)
    if (filters.value.start_time) params.append('start_time', filters.value.start_time)
    if (filters.value.end_time) params.append('end_time', filters.value.end_time)
    if (filters.value.product_id) params.append('product_id', filters.value.product_id)
    if (filters.value.tipo) params.append('tipo', filters.value.tipo)
    if (filters.value.num_lote) params.append('num_lote', filters.value.num_lote)

    const response = await fetch(`/api/stock-movements?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    if (response.ok) {
      movements.value = await response.json()
    } else {
      console.error('Failed to fetch stock movements')
    }
  } catch (error) {
    console.error('Error fetching stock movements:', error)
  } finally {
    isFetching.value = false
  }
}

const fetchProducts = async () => {
  try {
    const response = await fetch('/api/products', {
      headers: { 'Authorization': `Bearer ${userStore.token}` }
    })
    if (response.ok) {
      products.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  if (dateString.length === 10) {
    const [year, month, day] = dateString.split('-').map(Number)
    return new Date(year, month - 1, day).toLocaleDateString('pt-BR')
  }
  const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
  return new Date(utcDateString).toLocaleDateString('pt-BR')
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
  return new Date(utcDateString).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const TYPE_MAP = {
  initial_snapshot: { label: 'Snapshot Inicial', color: 'bg-neutral-200 text-neutral-700' },
  production_created: { label: 'Produção', color: 'bg-green-100 text-green-700' },
  production_edited: { label: 'Produção Editada', color: 'bg-blue-100 text-blue-700' },
  sale_created: { label: 'Venda', color: 'bg-red-100 text-red-600' },
  sale_edited: { label: 'Venda Editada', color: 'bg-orange-100 text-orange-700' },
  sale_edit_rollback: { label: 'Venda Editada (Rollback)', color: 'bg-yellow-100 text-yellow-700' },
  sale_deleted: { label: 'Venda Excluída', color: 'bg-purple-100 text-purple-700' },
  return_concluded: { label: 'Devolução Concluída', color: 'bg-teal-100 text-teal-700' },
  return_deleted: { label: 'Devolução Excluída', color: 'bg-pink-100 text-pink-700' },
  manual_adjustment: { label: 'Ajuste Manual', color: 'bg-gray-100 text-gray-700' }
}

const getTypeLabel = (tipo) => TYPE_MAP[tipo]?.label || tipo
const getTypeBadgeClass = (tipo) => TYPE_MAP[tipo]?.color || 'bg-gray-100 text-gray-700'

onMounted(() => {
  fetchMovements()
  fetchProducts()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar-track {
  border-bottom-right-radius: 1rem;
  background-color: #e5e7eb;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #9ca3af;
  border-radius: 9999px;
}

/* Slide transition for filters */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  margin-bottom: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  max-height: 500px;
}
</style>
