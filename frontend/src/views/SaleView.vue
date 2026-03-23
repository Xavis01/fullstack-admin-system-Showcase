<template>
  <div id="background" class="min-h-screen bg-gray-200 font-montserrat">
    <section id="sale">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
        <!--Header -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 md:mb-8 gap-4">
          <div class="flex items-center gap-2 md:gap-4">
            <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
              <ShoppingCart class="text-white w-6 h-6 md:w-8 md:h-8" />
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">GERENCIAR VENDAS
            </h2>
          </div>
          <div class="flex flex-col sm:flex-row gap-2 md:gap-4 w-full lg:w-auto">
            <button @click="openReturnManager"
              class="w-full sm:w-auto order-3 lg:order-1 bg-white hover:bg-gray-50 active:scale-95 text-red-600 font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2 border border-red-600 hover:border-red-700">
              <RotateCcw class="w-5 h-5" />
              DEVOLUÇÕES
            </button>
            <button @click="openOrderManager"
              class="w-full sm:w-auto order-3 lg:order-1 bg-white hover:bg-gray-50 active:scale-95 text-red-600 font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2 border border-red-600 hover:border-red-700">
              <Truck class="w-5 h-5" />
              EXPEDIÇÃO
            </button>
            <button @click="openFilterModal"
              class="w-full sm:w-auto order-2 lg:order-2 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Filter class="w-5 h-5" />
              FILTRAR
            </button>
            <button @click="openCreateModal"
              class="w-full sm:w-auto order-1 lg:order-3 bg-neutral-700 hover:bg-neutral-800 active:scale-95 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Plus class="w-5 h-5" />
              NOVA VENDA
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isFetching" class="flex justify-center items-center h-64">
          <LoaderCircle class="animate-spin text-neutral-700 w-8 h-8 md:w-12 md:h-12" />
        </div>

        <!-- Empty State (No Records - No Filters) -->
        <div v-else-if="sales.length === 0 && !hasActiveFilters"
          class="flex flex-col items-center justify-center h-64 text-gray-500">
          <ShoppingCart class="mb-4 text-gray-400 w-12 h-12 md:w-16 md:h-16" />
          <p class="text-lg md:text-xl font-semibold">Nenhuma venda cadastrada</p>
          <p class="text-xs md:text-sm mt-2">Clique em "+ NOVA VENDA" para adicionar a primeira venda</p>
        </div>

        <!-- Empty State (No Matches - Filtered) -->
        <div v-else-if="sales.length === 0 && hasActiveFilters"
          class="flex flex-col items-center justify-center h-64 text-gray-500">
          <div class="mb-4 text-red-500">
            <AlertTriangle class="w-12 h-12 md:w-16 md:h-16" />
          </div>
          <p class="text-lg md:text-xl font-semibold text-gray-700">Nenhum registro encontrado</p>
          <p class="text-xs md:text-sm mt-2">Tente ajustar os filtros para encontrar o que procura</p>
        </div>

        <!-- Desktop Table + Mobile Cards -->
        <div v-else class="relative">
          <!-- Desktop Table (hidden on mobile) -->
          <div class="hidden lg:block animate-fade-in rounded-2xl shadow-lg">
            <!-- Table Header -->
            <div
              class="bg-neutral-700 text-white grid grid-cols-[80px_100px_3fr_3fr_2fr_2fr_70px] gap-4 px-6 py-4 font-bold text-sm uppercase rounded-t-2xl items-center">
              <div class="flex items-center gap-2 cursor-pointer group select-none hover:text-white" @click="toggleSort"
                title="Clique para ordenar">
                <span>ID</span>
                <div
                  class="flex items-center justify-center w-6 h-6 rounded-full bg-neutral-600 group-hover:bg-neutral-500 transition duration-200">
                  <transition name="rotate" mode="out-in">
                    <ArrowUpWideNarrow v-if="sortOrder === 'desc'" :size="14" class="text-red-500" />
                    <ArrowUpNarrowWide v-else :size="14" class="text-red-500" />
                  </transition>
                </div>
              </div>
              <div>LOTE</div>
              <div>PRODUTO</div>
              <div>CLIENTE</div>
              <div>QUANTIDADE</div>
              <div>DATA</div>
              <div class="text-center">MAIS</div>
            </div>

            <!-- Scrollable Table Body -->
            <div
              class="max-h-[640px] overflow-y-auto relative scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200 rounded-b-2xl bg-white custom-scrollbar"
              ref="tableBody">
              <div v-for="item in sales" :key="item.id"
                class="bg-white grid grid-cols-[80px_100px_3fr_3fr_2fr_2fr_70px] gap-4 px-6 py-4 border-b border-gray-200 hover:bg-red-50 transition relative last:border-b-0 items-center">
                <div class="font-bold text-neutral-800">#{{ item.id }}</div>
                <div class="font-bold text-neutral-800">#{{ item.num_lote }}</div>
                <div class="flex items-center gap-3">
                  <img v-if="item.product_image" :src="item.product_image"
                    class="w-8 h-8 rounded-full object-cover border border-gray-200" alt="" />
                  <div v-else class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-400">
                    <Package size="16" />
                  </div>
                  <div class="text-neutral-800 font-semibold">{{ item.product_name }}</div>
                </div>
                <div class="text-neutral-800">{{ item.client_name }}</div>
                <div class="text-neutral-800">{{ item.quant_caixa_vendida }} {{
                  item.product_name?.toLowerCase().includes('25kg') ? 'Sacos' : 'Caixas' }}</div>
                <div class="text-neutral-800">{{ formatDate(item.data_venda) }}</div>
                <div class="relative text-center">
                  <button @mouseenter="openOptions(item.id)" @mouseleave="scheduleClose(item.id)"
                    :data-sale-id="item.id"
                    class="text-neutral-600 hover:text-neutral-800 transition hover:bg-red-100 rounded-full p-1 relative">
                    <MoreHorizontal size="20" />
                    <!-- Indicator for returns -->
                    <div v-if="item.returns_info?.has_returns" class="absolute -top-1 -right-1 flex h-3 w-3">
                      <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
                        :class="getStatusPingColor(item.returns_info.latest_status)"></span>
                      <span class="relative inline-flex rounded-full h-3 w-3"
                        :class="getStatusDotColor(item.returns_info.latest_status)"></span>
                    </div>
                  </button>

                  <!-- Options Bubble -->
                  <Teleport to="body">
                    <transition name="bubble">
                      <div v-if="activeOptionsId === item.id"
                        class="fixed bg-white rounded-lg shadow-xl p-4 z-50 w-56 border border-gray-100 font-montserrat"
                        :style="getBubblePosition(item.id)" @mouseenter="cancelClose"
                        @mouseleave="scheduleClose(item.id)">
                        <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                          <p>CRIADO EM: {{ formatDate(item.created_at) }}</p>
                          <p>CRIADO AS: {{ formatTime(item.created_at) }}</p>
                          <p>CRIADO POR: {{ item.created_by_name }}</p>
                          <p class="mt-1 font-bold text-neutral-700">ESTOQUE RESTANTE: {{ item.remaining_stock }}</p>
                        </div>
                        <div class="flex flex-col gap-2">
                          <button @click="openEditModal(item)"
                            :disabled="!!item.order_product_id"
                            :title="item.order_product_id ? 'Vendas vinculadas a expedições não podem ser editadas' : 'Alterar venda'"
                            :class="item.order_product_id ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-gray-200 hover:bg-gray-300 text-neutral-800'"
                            class="font-bold py-1 px-4 rounded text-xs transition">ALTERAR</button>
                          <button @click="openReturnModal(item)"
                            class="bg-white hover:bg-gray-50 text-red-600 font-bold py-1 px-4 rounded text-xs transition flex items-center justify-center gap-1 border border-red-600">
                            <CornerDownLeft class="w-3 h-3" /> DEVOLUÇÃO
                          </button>
                          <button @click="openDeleteModal(item)"
                            class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition">DELETAR</button>

                          <!-- Return Status Info inside bubble if exists -->
                          <div v-if="item.returns_info?.has_returns"
                            class="mt-2 pt-2 border-t border-dashed border-gray-200 text-[10px] text-gray-500">
                            <p class="flex items-center gap-1 font-bold"
                              :class="getStatusTextColor(item.returns_info.latest_status)">
                              <Info class="w-3 h-3" /> DEVOLUÇÃO
                            </p>
                            <p>Qtd: {{ item.returns_info.total_returned }} {{
                              item.product_name?.toLowerCase().includes('25kg') ? 'sacos' : 'caixas' }}</p>
                            <p>Status: {{ item.returns_info.latest_status }}</p>
                          </div>
                        </div>
                      </div>
                    </transition>
                  </Teleport>
                </div>
              </div>
            </div>
          </div>

          <!-- Mobile Cards (visible on mobile only) -->
          <div class="block lg:hidden">
            <!-- Sort button -->
            <div class="flex justify-between items-center mb-4">
              <span class="text-sm text-gray-600">{{ sales.length }} {{ sales.length === 1 ? 'venda' : 'vendas'
              }}</span>
              <button @click="toggleSort"
                class="flex items-center gap-2 bg-white px-3 py-2 rounded-lg shadow active:scale-95 transition">
                <span class="text-sm font-semibold">Ordenar</span>
                <ArrowUpWideNarrow v-if="sortOrder === 'desc'" class="w-4 h-4 text-red-600" />
                <ArrowUpNarrowWide v-else class="w-4 h-4 text-red-600" />
              </button>
            </div>

            <div class="space-y-4 animate-fade-in">
              <div v-for="item in sales" :key="item.id"
                class="bg-white rounded-2xl shadow-lg p-4 border border-gray-200 relative">
                <!-- Header com imagem, ID, produto e menu (⋮) -->
                <div class="flex items-start justify-between mb-3 pb-3 border-b border-gray-100">
                  <div class="flex items-center gap-3 flex-1 min-w-0">
                    <img v-if="item.product_image" :src="item.product_image"
                      class="w-12 h-12 rounded-full object-cover border-2 border-gray-200 flex-shrink-0" alt="" />
                    <div v-else
                      class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                      <Package :size="20" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="font-bold text-neutral-800 text-lg">#{{ item.id }}</div>
                      <div class="text-sm text-neutral-600 truncate">{{ item.product_name }}</div>
                    </div>
                  </div>

                  <!-- Menu de 3 pontos -->
                  <div class="relative flex-shrink-0">
                    <button @click="toggleCardMenu(item.id)" :data-card-menu="item.id"
                      class="p-2 hover:bg-gray-100 rounded-lg transition relative">
                      <MoreVertical class="w-5 h-5 text-gray-600" />
                      <div v-if="item.returns_info?.has_returns" class="absolute top-1 right-1 flex h-2 w-2">
                        <span class="relative inline-flex rounded-full h-2 w-2"
                          :class="getStatusDotColor(item.returns_info.latest_status)"></span>
                      </div>
                    </button>
                    <!-- Dropdown menu -->
                    <Teleport to="body">
                      <transition name="bubble">
                        <div v-if="activeCardMenu === item.id" @click.stop
                          class="fixed bg-white rounded-lg shadow-xl border border-gray-100 p-4 w-56 z-[60]"
                          :style="getCardMenuPosition(item.id)">
                          <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                            <p>CRIADO EM: {{ formatDate(item.created_at) }}</p>
                            <p>CRIADO AS: {{ formatTime(item.created_at) }}</p>
                            <p>CRIADO POR: {{ item.created_by_name }}</p>
                            <p class="mt-1 font-bold text-neutral-700">ESTOQUE RESTANTE: {{ item.remaining_stock }}</p>
                          </div>
                          <div class="text-xs font-bold text-gray-800 mb-3">
                            {{ item.quant_caixa_vendida }} {{
                              item.product_name?.toLowerCase().includes('25kg') ? 'Sacos' : 'Caixas'
                            }}
                          </div>
                          <div class="flex flex-col gap-2">
                            <button @click="openEditModal(item); activeCardMenu = null"
                              :disabled="!!item.order_product_id"
                              :title="item.order_product_id ? 'Vendas vinculadas a expedições não podem ser editadas' : 'Alterar venda'"
                              :class="item.order_product_id ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-gray-200 hover:bg-gray-300 text-neutral-800'"
                              class="font-bold py-1 px-4 rounded text-xs transition">
                              ALTERAR
                            </button>
                            <button @click="openReturnModal(item); activeCardMenu = null"
                              class="bg-white hover:bg-gray-50 text-red-600 font-bold py-1 px-4 rounded text-xs transition flex items-center justify-center gap-1 border border-red-600">
                              <CornerDownLeft class="w-3 h-3" /> DEVOLUÇÃO
                            </button>
                            <button @click="openDeleteModal(item); activeCardMenu = null"
                              class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition">
                              DELETAR
                            </button>

                            <div v-if="item.returns_info?.has_returns"
                              class="mt-2 pt-2 border-t border-dashed border-gray-200 text-[10px] text-gray-500">
                              <p class="flex items-center gap-1 font-bold"
                                :class="getStatusTextColor(item.returns_info.latest_status)">
                                <Info class="w-3 h-3" /> DEVOLUÇÃO
                              </p>
                              <p>Qtd: {{ item.returns_info.total_returned }} {{
                                item.product_name?.toLowerCase().includes('25kg') ? 'sacos' : 'caixas' }}</p>
                              <p>Status: {{ item.returns_info.latest_status }}</p>
                            </div>
                          </div>
                        </div>
                      </transition>
                    </Teleport>
                  </div>
                </div>

                <!-- Detalhes -->
                <div class="space-y-2 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Lote:</span>
                    <span class="text-neutral-700 font-bold">#{{ item.num_lote }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Cliente:</span>
                    <span class="text-neutral-700">{{ item.client_name }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Quantidade:</span>
                    <span class="text-neutral-700">{{ item.quant_caixa_vendida }} {{
                      item.product_name?.toLowerCase().includes('25kg') ? 'Sacos' : 'Caixas' }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Data:</span>
                    <span class="text-neutral-700">{{ formatDate(item.data_venda) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <SalesFormModal :isOpen="isFormModalOpen" :sale="selectedSale" :loading="isLoading" @close="closeFormModal"
      @save="handleSaveSale" />

    <SalesFilterModal :isOpen="isFilterModalOpen" :currentFilters="filters" @close="closeFilterModal"
      @apply="handleApplyFilters" />

    <SalesDeleteModal :isOpen="isDeleteModalOpen" :itemName="selectedSale?.id" :loading="isLoading"
      @close="closeDeleteModal" @confirm="handleDeleteSale" />

    <SalesReturnModal :isOpen="isReturnModalOpen" :sale="selectedSale" :loading="isLoading" @close="closeReturnModal"
      @save="handleSaveReturn" />

    <ReturnManagerModal :isOpen="isReturnManagerOpen" @close="isReturnManagerOpen = false" @refresh="fetchSales" />
    <OrderManagerModal :isOpen="isOrderManagerOpen" @close="isOrderManagerOpen = false" @sale-saved="fetchSales" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import { MoreHorizontal, MoreVertical, LoaderCircle, Package, Filter, Plus, AlertTriangle, ArrowUpWideNarrow, ArrowUpNarrowWide, ShoppingCart, RotateCcw, Truck, CornerDownLeft, Info } from 'lucide-vue-next'
import { useUserStore } from '../stores/user'
import { useRouter, useRoute } from 'vue-router'
import SalesFormModal from '../components/sales/SalesFormModal.vue'
import SalesReturnModal from '../components/sales/SalesReturnModal.vue'
import ReturnManagerModal from '../components/returns/ReturnManagerModal.vue'
import OrderManagerModal from '../components/orders/OrderManagerModal.vue'
import SalesFilterModal from '../components/sales/SalesFilterModal.vue'
import SalesDeleteModal from '../components/sales/SalesDeleteModal.vue'
import { useToastStore } from '../stores/toast'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()
const route = useRoute()

userStore.ensureValidSession(router)

const sales = ref([])
const totalItems = ref(0)
const activeOptionsId = ref(null)
const tableBody = ref(null)

// Mobile card menu state
const activeCardMenu = ref(null)

const toggleCardMenu = (id) => {
  if (activeCardMenu.value === id) {
    activeCardMenu.value = null
  } else {
    activeCardMenu.value = id
  }
}

const getCardMenuPosition = (id) => {
  const button = document.querySelector(`button[data-card-menu="${id}"]`)
  if (!button) {
    return { top: '50px', right: '8px' }
  }

  const rect = button.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const menuWidth = 224 // w-56 = 224px

  const leftPosition = Math.min(
    rect.right - menuWidth,
    viewportWidth - menuWidth - 8
  )

  return {
    top: `${rect.bottom + 4}px`,
    left: `${Math.max(8, leftPosition)}px`
  }
}

// Click-outside and scroll handlers
const cardMenuClickHandler = (event) => {
  if (activeCardMenu.value !== null) {
    const menu = document.querySelector('.fixed.z-\\[60\\]')
    const button = event.target.closest('button')

    if (!menu?.contains(event.target) && !button) {
      activeCardMenu.value = null
    }
  }
}

const handleScroll = () => {
  if (activeCardMenu.value !== null) {
    activeCardMenu.value = null
  }
}

// Modal states
const isFormModalOpen = ref(false)
const isFilterModalOpen = ref(false)
const isDeleteModalOpen = ref(false)
const isReturnModalOpen = ref(false)
const isReturnManagerOpen = ref(false)
const isOrderManagerOpen = ref(false)

const selectedSale = ref(null)
const isLoading = ref(false)
const isFetching = ref(false)

const sortOrder = ref('desc')

const filters = ref({
  num_lote: '',
  client_id: '',
  product_id: '',
  start_date: '',
  end_date: ''
})

const hasActiveFilters = computed(() => {
  return !!(
    filters.value.sale_id ||
    filters.value.num_lote ||
    filters.value.client_id ||
    filters.value.product_id ||
    filters.value.start_date ||
    filters.value.end_date
  )
})

const fetchSales = async () => {
  isFetching.value = true
  try {
    // Build query string
    const params = new URLSearchParams()
    if (filters.value.sale_id) params.append('sale_id', filters.value.sale_id)
    if (filters.value.num_lote) params.append('num_lote', filters.value.num_lote)
    if (filters.value.client_id) params.append('client_id', filters.value.client_id)
    if (filters.value.product_id) params.append('product_id', filters.value.product_id)
    if (filters.value.start_date) params.append('start_date', filters.value.start_date)
    if (filters.value.end_date) params.append('end_date', filters.value.end_date)

    const response = await fetch(`/api/sales?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    if (response.ok) {
      const data = await response.json()

      totalItems.value = data.length

      // Sort
      data.sort((a, b) => {
        const valA = a.id
        const valB = b.id
        return sortOrder.value === 'asc' ? valA - valB : valB - valA
      })

      sales.value = data
      await nextTick()


    } else {
      console.error('Failed to fetch sales')
    }
  } catch (error) {
    console.error('Error fetching sales:', error)
  } finally {
    isFetching.value = false
  }
}

const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  fetchSales()
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  if (dateString.length === 10) {
    const cleanDate = dateString.replace(' ', 'T')
    const [year, month, day] = cleanDate.split('T')[0].split('-').map(Number)
    const date = new Date(year, month - 1, day)
    return date.toLocaleDateString('pt-BR')
  }
  const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
  const date = new Date(utcDateString)
  return date.toLocaleDateString('pt-BR')
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
  const date = new Date(utcDateString)
  return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const getStatusDotColor = (status) => {
  switch (status) {
    case 'Retornada': return 'bg-blue-500'
    case 'Concluída': return 'bg-green-500'
    default: return 'bg-yellow-500' // Aberto
  }
}

const getStatusPingColor = (status) => {
  switch (status) {
    case 'Retornada': return 'bg-blue-400'
    case 'Concluída': return 'bg-green-400'
    default: return 'bg-yellow-400'
  }
}

const getStatusTextColor = (status) => {
  switch (status) {
    case 'Retornada': return 'text-blue-600'
    case 'Concluída': return 'text-green-600'
    default: return 'text-yellow-600'
  }
}

const closeTimeout = ref(null)

const openOptions = (id) => {
  if (closeTimeout.value) {
    clearTimeout(closeTimeout.value)
    closeTimeout.value = null
  }
  activeOptionsId.value = id
}

const closeOptions = (id) => {
  if (activeOptionsId.value === id) {
    activeOptionsId.value = null
  }
}

const scheduleClose = (id) => {
  closeTimeout.value = setTimeout(() => {
    closeOptions(id)
  }, 150)
}

const cancelClose = () => {
  if (closeTimeout.value) {
    clearTimeout(closeTimeout.value)
    closeTimeout.value = null
  }
}

const getBubblePosition = (id) => {
  const button = document.querySelector(`[data-sale-id="${id}"]`)
  if (!button) return {}

  const rect = button.getBoundingClientRect()
  return {
    top: `${rect.bottom + 8}px`,
    left: `${rect.right - 230}px` // Adjusted for wider bubble
  }
}

// Create/Edit Logic
const openCreateModal = () => {
  selectedSale.value = null
  isFormModalOpen.value = true
}

const openEditModal = (sale) => {
  if (!userStore.user?.is_master) {
    toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem alterar vendas.', type: 'error' })
    activeOptionsId.value = null
    activeCardMenu.value = null
    return
  }
  if (sale.order_product_id) {
    toastStore.add({ title: 'Ação Bloqueada', message: 'Vendas vinculadas a expedições não podem ser editadas. Exclua e refaça a venda.', type: 'warning' })
    activeOptionsId.value = null
    activeCardMenu.value = null
    return
  }
  selectedSale.value = { ...sale }
  isFormModalOpen.value = true
  activeOptionsId.value = null
}

const closeFormModal = () => {
  isFormModalOpen.value = false
  selectedSale.value = null
}

const handleSaveSale = async (formData) => {
  isLoading.value = true
  const isEdit = !!selectedSale.value?.id
  const url = isEdit
    ? `/api/sales/${selectedSale.value.id}`
    : '/api/sales'
  const method = isEdit ? 'PUT' : 'POST'

  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userStore.token}`
      },
      body: JSON.stringify(formData)
    })

    if (response.ok) {
      if (isEdit) {
        const saleId = selectedSale.value.id
        await fetchSales()
        toastStore.add({
          title: 'Venda Atualizada',
          message: `Venda #${saleId} atualizada com sucesso.`,
          type: 'success'
        })
        closeFormModal()
      } else {
        // Response contains the created sale object wrapped in { message, sale }
        const result = await response.json()
        await fetchSales()
        toastStore.add({
          title: 'Venda Criada',
          message: `Venda #${result.sale.id} registrada com sucesso.`,
          type: 'success'
        })
        closeFormModal()
      }

    } else {
      const error = await response.json()
      toastStore.add({
        title: 'Erro ao Salvar',
        message: error.error || 'Não foi possível salvar a venda.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error saving sale:', error)
  } finally {
    isLoading.value = false
  }
}

// Delete Logic
const openDeleteModal = (sale) => {
  if (!userStore.user?.is_master) {
    toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem excluir vendas.', type: 'error' })
    activeOptionsId.value = null
    activeCardMenu.value = null
    return
  }
  selectedSale.value = sale
  isDeleteModalOpen.value = true
  activeOptionsId.value = null
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  selectedSale.value = null
}

const handleDeleteSale = async () => {
  if (!selectedSale.value) return
  isLoading.value = true

  try {
    const saleId = selectedSale.value.id
    const response = await fetch(`/api/sales/${saleId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })

    if (response.ok) {
      await fetchSales()
      closeDeleteModal()
      toastStore.add({
        title: 'Venda Removida',
        message: `Venda #${saleId} removida com sucesso.`,
        type: 'success'
      })
    } else {
      toastStore.add({
        title: 'Erro ao Deletar',
        message: 'Não foi possível remover a venda.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error deleting sale:', error)
  } finally {
    isLoading.value = false
  }
}

// Return Logic
const openReturnModal = (sale) => {
  if (!userStore.user?.is_master) {
    toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem criar devoluções.', type: 'error' })
    activeOptionsId.value = null
    activeCardMenu.value = null
    return
  }
  selectedSale.value = sale
  isReturnModalOpen.value = true
  activeOptionsId.value = null
  activeCardMenu.value = null
}

const closeReturnModal = () => {
  isReturnModalOpen.value = false
  selectedSale.value = null
}

const handleSaveReturn = async (formData) => {
  isLoading.value = true
  try {
    const response = await fetch('/api/returns', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userStore.token}`
      },
      body: JSON.stringify(formData)
    })

    if (response.ok) {
      await fetchSales()
      closeReturnModal()
      toastStore.add({
        title: 'Devolução Registrada',
        message: 'Devolução realizada com sucesso.',
        type: 'success'
      })
    } else {
      const err = await response.json()
      toastStore.add({
        title: 'Erro',
        message: err.error,
        type: 'error'
      })
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

const openReturnManager = () => {
  isReturnManagerOpen.value = true
}

const openOrderManager = () => {
  isOrderManagerOpen.value = true
}

// Filter Logic
const openFilterModal = () => {
  isFilterModalOpen.value = true
}

const closeFilterModal = () => {
  isFilterModalOpen.value = false
}

const handleApplyFilters = (newFilters) => {
  filters.value = newFilters
  fetchSales()
  closeFilterModal()
}

onMounted(async () => {
  document.addEventListener('click', cardMenuClickHandler)
  window.addEventListener('scroll', handleScroll, true)

  try {
    await fetchSales()

    if (route.query.new_sale_lote) {
      await nextTick()
      const lote = Array.isArray(route.query.new_sale_lote) ? route.query.new_sale_lote[0] : route.query.new_sale_lote
      selectedSale.value = {
        num_lote: lote,
        client_id: '',
        quant_caixa_vendida: '',
        data_venda: new Date().toISOString().split('T')[0]
      }
      isFormModalOpen.value = true

      // Clear query param after a short delay to ensure modal opens
      setTimeout(() => {
        router.replace({ query: {} })
      }, 500)
    }
  } catch (error) {
    console.error('Error in SaleView onMounted:', error)
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', cardMenuClickHandler)
  window.removeEventListener('scroll', handleScroll, true)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar-track {
  border-bottom-right-radius: 1rem;
  background-color: #e5e7eb;
  /* gray-200 */
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #9ca3af;
  /* gray-400 */
  border-radius: 9999px;
}

/* Bubble animations */
.bubble-enter-active,
.bubble-leave-active {
  transition: all 0.2s ease;
}

.bubble-enter-from,
.bubble-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-5px);
}

/* Rotate animation for sort icon */
.rotate-enter-active,
.rotate-leave-active {
  transition: all 0.2s ease;
}

.rotate-enter-from {
  opacity: 0;
  transform: rotate(-90deg);
}

.rotate-leave-to {
  opacity: 0;
  transform: rotate(90deg);
}
</style>
