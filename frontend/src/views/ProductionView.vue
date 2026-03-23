<template>
  <div id="background" class="min-h-screen bg-gray-200 font-montserrat">
    <section id="production">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
        <!-- Header -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 md:mb-8 gap-4">
          <div class="flex items-center gap-2 md:gap-4">
            <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
              <Boxes class="text-white w-6 h-6 md:w-8 md:h-8" />
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">GERENCIAR PRODUÇÃO
            </h2>
          </div>
          <div class="flex flex-col sm:flex-row gap-2 md:gap-4 w-full lg:w-auto">
            <button @click="openStatsModal"
              class="w-full sm:w-auto order-3 lg:order-1 bg-white hover:bg-gray-50 active:scale-95 text-red-600 font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2 border border-red-600 hover:border-red-700">
              <BarChart2 class="w-5 h-5" />
              ESTATÍSTICAS
            </button>
            <button @click="openFilterModal"
              class="w-full sm:w-auto order-2 lg:order-2 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Filter class="w-5 h-5" />
              FILTRAR
            </button>
            <button @click="openCreateModal"
              class="w-full sm:w-auto order-1 lg:order-3 bg-neutral-700 hover:bg-neutral-800 active:scale-95 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Plus class="w-5 h-5" />
              NOVO LOTE
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isFetching" class="flex justify-center items-center h-64">
          <LoaderCircle class="animate-spin text-neutral-700 w-8 h-8 md:w-12 md:h-12" />
        </div>

        <!-- Empty State (No Records) -->
        <div v-else-if="totalItems === 0" class="flex flex-col items-center justify-center h-64 text-gray-500">
          <Boxes class="mb-4 text-gray-400 w-12 h-12 md:w-16 md:h-16" />
          <p class="text-lg md:text-xl font-semibold">Nenhum lote cadastrado</p>
          <p class="text-xs md:text-sm mt-2">Clique em "+ NOVO LOTE" para adicionar o primeiro lote</p>
        </div>

        <!-- Empty State (No Matches) -->
        <div v-else-if="productions.length === 0" class="flex flex-col items-center justify-center h-64 text-gray-500">
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
              class="bg-neutral-700 text-white grid grid-cols-[80px_3fr_2fr_2fr_2fr_70px] gap-4 px-6 py-4 font-bold text-sm uppercase rounded-t-2xl items-center">
              <div class="flex items-center gap-2 cursor-pointer group select-none hover:text-white" @click="toggleSort"
                title="Clique para ordenar">
                <span>LOTE</span>
                <div
                  class="flex items-center justify-center w-6 h-6 rounded-full bg-neutral-600 group-hover:bg-neutral-500 transition duration-200">
                  <transition name="rotate" mode="out-in">
                    <ArrowUpWideNarrow v-if="sortOrder === 'desc'" :size="14" class="text-red-500" />
                    <ArrowUpNarrowWide v-else :size="14" class="text-red-500" />
                  </transition>
                </div>
              </div>
              <div>PRODUTO</div>
              <div>PRODUZIDO</div>
              <div>ESTOQUE</div>
              <div>DATA</div>
              <div class="text-center">MAIS</div>
            </div>

            <!-- Scrollable Table Body -->
            <div
              class="max-h-[640px] overflow-y-auto relative scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200 rounded-b-2xl bg-white custom-scrollbar"
              ref="tableBody">
              <div v-for="item in productions" :key="item.num_lote"
                class="bg-white grid grid-cols-[80px_3fr_2fr_2fr_2fr_70px] gap-4 px-6 py-4 border-b border-gray-200 hover:bg-red-50 transition relative last:border-b-0 items-center">
                <div class="font-bold text-neutral-800">#{{ item.num_lote }}</div>
                <div class="flex items-center gap-3">
                  <img v-if="item.product_image" :src="item.product_image"
                    class="w-8 h-8 rounded-full object-cover border border-gray-200" alt="" />
                  <div v-else class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-400">
                    <Package size="16" />
                  </div>
                  <div class="text-neutral-800 font-semibold">{{ item.product_name }}</div>
                </div>
                <div class="text-neutral-800">{{ item.quant_caixa_produzida }} {{
                  item.product_name?.toUpperCase().includes('25KG') ? 'Sacos' : 'Caixas' }}</div>
                <div class="text-neutral-800" :class="{ 'text-red-500 font-bold': item.estoque_lote === 0 }">
                  {{ item.estoque_lote === 0 ? 'Sem Estoque' : item.estoque_lote +
                    (item.product_name?.toUpperCase().includes('25KG') ? ' Sacos' : ' Caixas') }}
                </div>
                <div class="text-neutral-800">{{ formatDate(item.data_producao) }}</div>
                <div class="relative text-center flex items-center justify-center h-8">
                  <button v-if="Number(item.estoque_lote) > 0" @click="goToSale(item.num_lote)"
                    class="absolute right-[calc(50%+16px)] text-neutral-600 hover:text-red-600 hover:scale-110 transition-all duration-200 rounded-full p-1"
                    title="Vender Lote">
                    <ShoppingCart size="20" />
                  </button>
                  <button @mouseenter="openOptions(item.num_lote)" @mouseleave="scheduleClose(item.num_lote)"
                    :data-lote-id="item.num_lote"
                    class="text-neutral-600 hover:text-neutral-800 transition hover:bg-red-100 rounded-full p-1 relative z-10">
                    <MoreHorizontal size="20" />
                  </button>
                  <!-- Options Bubble -->
                  <Teleport to="body">
                    <transition name="bubble">
                      <div v-if="activeOptionsId === item.num_lote"
                        class="fixed bg-white rounded-lg shadow-xl p-4 z-50 w-48 border border-gray-100 font-montserrat"
                        :style="getBubblePosition(item.num_lote)" @mouseenter="cancelClose"
                        @mouseleave="scheduleClose(item.num_lote)">
                        <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                          <p>CRIADO EM: {{ formatDate(item.created_at) }}</p>
                          <p>CRIADO AS: {{ formatTime(item.created_at) }}</p>
                          <p>CRIADO POR: {{ item.created_by_name }}</p>
                        </div>
                        <div class="flex flex-col gap-2">
                          <button @click="openEditModal(item)"
                            class="bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed"
                            :disabled="item.has_sales"
                            :title="item.has_sales ? 'Não é possível alterar um lote com vendas vinculadas' : ''">
                            ALTERAR
                          </button>
                          <button @click="openDeleteModal(item)"
                            class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed"
                            :disabled="item.has_sales">
                            DELETAR
                          </button>
                          <div v-if="item.has_sales"
                            class="text-[10px] text-red-500 text-center leading-tight mt-1 font-semibold">
                            Lote com vendas vinculadas não pode ser alterado ou excluído.
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
              <span class="text-sm text-gray-600">{{ productions.length }} {{ productions.length === 1 ? 'lote' :
                'lotes' }}</span>
              <button @click="toggleSort"
                class="flex items-center gap-2 bg-white px-3 py-2 rounded-lg shadow active:scale-95 transition">
                <span class="text-sm font-semibold">Ordenar</span>
                <ArrowUpWideNarrow v-if="sortOrder === 'desc'" class="w-4 h-4 text-red-600" />
                <ArrowUpNarrowWide v-else class="w-4 h-4 text-red-600" />
              </button>
            </div>

            <div class="space-y-4 animate-fade-in">
              <div v-for="item in productions" :key="item.num_lote"
                class="bg-white rounded-2xl shadow-lg p-4 border border-gray-200 relative">
                <!-- Header com Lote e Menu dropdown -->
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

                  <!-- Menu de 3 pontos -->
                  <div class="relative flex-shrink-0">
                    <button @click="toggleCardMenu(item.num_lote)" :data-card-menu="item.num_lote"
                      class="p-2 hover:bg-gray-100 rounded-lg transition">
                      <MoreVertical class="w-5 h-5 text-gray-600" />
                    </button>
                    <!-- Dropdown menu -->
                    <Teleport to="body">
                      <transition name="bubble">
                        <div v-if="activeCardMenu === item.num_lote" @click.stop
                          class="fixed bg-white rounded-lg shadow-xl border border-gray-100 p-4 w-48 z-[60]"
                          :style="getCardMenuPosition(item.num_lote)">
                          <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                            <p>CRIADO EM: {{ formatDate(item.created_at) }}</p>
                            <p>CRIADO AS: {{ formatTime(item.created_at) }}</p>
                            <p>CRIADO POR: {{ item.created_by_name }}</p>
                          </div>
                          <div class="flex flex-col gap-2">
                            <button @click="openEditModal(item); activeCardMenu = null" :disabled="item.has_sales"
                              class="bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed"
                              :title="item.has_sales ? 'Não é possível alterar um lote com vendas vinculadas' : ''">
                              ALTERAR
                            </button>
                            <button @click="openDeleteModal(item); activeCardMenu = null" :disabled="item.has_sales"
                              class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed">
                              DELETAR
                            </button>
                            <div v-if="item.has_sales"
                              class="text-[10px] text-red-500 text-center leading-tight mt-1 font-semibold">
                              Lote com vendas vinculadas não pode ser alterado ou excluído.
                            </div>
                          </div>
                        </div>
                      </transition>
                    </Teleport>
                  </div>
                </div>

                <!-- Badge de estoque e botão vender -->
                <div class="flex items-center justify-between mb-3">
                  <span :class="item.estoque_lote === 0 ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-700'"
                    class="px-3 py-1 rounded-full text-sm font-semibold">
                    {{ item.estoque_lote === 0 ? 'Sem Estoque' : `${item.estoque_lote}
                    ${item.product_name?.toUpperCase().includes('25KG') ? 'Sacos' : 'Caixas'}` }}
                  </span>
                  <button v-if="item.estoque_lote > 0" @click="goToSale(item.num_lote)"
                    class="flex items-center gap-1 bg-red-600 hover:bg-red-700 active:scale-95 text-white px-3 py-1.5 rounded-lg text-sm font-semibold transition">
                    <ShoppingCart class="w-4 h-4" />
                    Vender
                  </button>
                </div>

                <!-- Detalhes -->
                <div class="space-y-2 text-sm">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Produzido:</span>
                    <span class="text-neutral-700">{{ item.quant_caixa_produzida }} {{
                      item.product_name?.toUpperCase().includes('25KG') ? 'Sacos' : 'Caixas' }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Data:</span>
                    <span class="text-neutral-700">{{ formatDate(item.data_producao) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <ProductionFormModal :isOpen="isFormModalOpen" :production="selectedProduction" :loading="isLoading"
      @close="closeFormModal" @save="handleSaveProduction" />

    <ProductionFilterModal :isOpen="isFilterModalOpen" :currentFilters="filters" @close="closeFilterModal"
      @apply="handleApplyFilters" />

    <ProductionDeleteModal :isOpen="isDeleteModalOpen" :itemName="selectedProduction?.num_lote" :loading="isLoading"
      @close="closeDeleteModal" @confirm="handleDeleteProduction" />

    <ProductionStatsModal :isOpen="isStatsModalOpen" :productions="productions" @close="closeStatsModal"
      @open-info="isStatsInfoModalOpen = true" />
    <ProductionStatsInfoModal :isOpen="isStatsInfoModalOpen" @close="isStatsInfoModalOpen = false" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { MoreHorizontal, MoreVertical, LoaderCircle, Package, Boxes, Filter, Plus, AlertTriangle, ArrowUpWideNarrow, ArrowUpNarrowWide, ShoppingCart, BarChart2 } from 'lucide-vue-next'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import ProductionFormModal from '../components/production/ProductionFormModal.vue'
import ProductionFilterModal from '../components/production/ProductionFilterModal.vue'
import ProductionDeleteModal from '../components/production/ProductionDeleteModal.vue'
import ProductionStatsModal from '../components/production/ProductionStatsModal.vue'
import ProductionStatsInfoModal from '../components/production/ProductionStatsInfoModal.vue'
import { useToastStore } from '../stores/toast'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()

userStore.ensureValidSession(router)

const productions = ref([])
const totalItems = ref(0)
const activeOptionsId = ref(null)
const tableBody = ref(null)

const goToSale = (lote) => {
  router.push({ path: '/sale', query: { new_sale_lote: lote } })
}

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
    // Fallback - calculate based on card position
    return { top: '50px', right: '8px' }
  }

  const rect = button.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const menuWidth = 192 // 48 * 4 = 192px (w-48)

  // Position below and aligned to the right edge of the button
  // Ensure it doesn't go off screen with 8px margin
  const leftPosition = Math.min(
    rect.right - menuWidth, // Align to right edge of button
    viewportWidth - menuWidth - 8 // Don't go past viewport with 8px margin
  )

  return {
    top: `${rect.bottom + 4}px`,
    left: `${Math.max(8, leftPosition)}px` // Also ensure it doesn't go off left edge
  }
}

// Close mobile card menu when clicking outside
const cardMenuClickHandler = (event) => {
  if (activeCardMenu.value !== null) {
    const menu = document.querySelector('.fixed.z-\\[60\\]')
    const button = event.target.closest('button')

    if (!menu?.contains(event.target) && !button) {
      activeCardMenu.value = null
    }
  }
}

// Close menu on scroll
const handleScroll = () => {
  if (activeCardMenu.value !== null) {
    activeCardMenu.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', cardMenuClickHandler)
  window.addEventListener('scroll', handleScroll, true) // true = capture phase to catch all scrolls
})

onBeforeUnmount(() => {
  document.removeEventListener('click', cardMenuClickHandler)
  window.removeEventListener('scroll', handleScroll, true)
})

// Modal states
const isFormModalOpen = ref(false)
const isFilterModalOpen = ref(false)
const isDeleteModalOpen = ref(false)
const isStatsModalOpen = ref(false)
const isStatsInfoModalOpen = ref(false)
const selectedProduction = ref(null)
const isLoading = ref(false)
const isFetching = ref(false)

const sortOrder = ref('desc')

const filters = ref({
  num_lote: '',
  product_id: '',
  start_date: '',
  end_date: '',
  hide_empty_stock: false
})

const fetchProductions = async () => {
  isFetching.value = true
  try {
    const response = await fetch('/api/productions', {
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    if (response.ok) {
      let data = await response.json()

      const productsResponse = await fetch('/api/products', {
        headers: { 'Authorization': `Bearer ${userStore.token}` }
      })
      const products = await productsResponse.json()
      const productMap = {}
      products.forEach(p => {
        let imageUrl = null
        if (p.image_path) {
          if (p.image_path.startsWith('http')) {
            imageUrl = p.image_path
          } else {
            let cleanPath = p.image_path.replace(/^backend[\\/]/, '').replace(/\\/g, '/')
            imageUrl = `/${cleanPath}`
          }
        }
        productMap[p.id] = { name: p.nome, image: imageUrl }
      })

      data = data.map(item => ({
        ...item,
        product_name: productMap[item.product_id]?.name || 'Produto Desconhecido',
        product_image: productMap[item.product_id]?.image,
        has_sales: !!item.has_sales // Ensure boolean
      }))

      totalItems.value = data.length

      // Apply client-side filtering/sorting since backend seems simple
      if (filters.value.num_lote) {
        const searchLote = String(filters.value.num_lote).toLowerCase()
        data = data.filter(item => String(item.num_lote).toLowerCase().includes(searchLote))
      }
      if (filters.value.product_id) {
        data = data.filter(item => item.product_id == filters.value.product_id)
      }
      if (filters.value.start_date) {
        const startDate = new Date(filters.value.start_date)
        data = data.filter(item => new Date(item.data_producao) >= startDate)
      }
      if (filters.value.end_date) {
        const endDate = new Date(filters.value.end_date)
        data = data.filter(item => new Date(item.data_producao) <= endDate)
      }
      if (filters.value.hide_empty_stock) {
        data = data.filter(item => Number(item.estoque_lote) > 0)
      }

      // Sort by num_lote
      data.sort((a, b) => {
        const valA = a.num_lote
        const valB = b.num_lote
        // Use localeCompare with numeric option for correct string number sorting
        return sortOrder.value === 'asc'
          ? valA.localeCompare(valB, undefined, { numeric: true })
          : valB.localeCompare(valA, undefined, { numeric: true })
      })

      productions.value = data
      await nextTick()
    } else {
      console.error('Failed to fetch productions')
    }
  } catch (error) {
    console.error('Error fetching productions:', error)
  } finally {
    isFetching.value = false
  }
}

const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  fetchProductions()
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  // Handle "YYYY-MM-DD" (Local) or "YYYY-MM-DD HH:MM:SS" (UTC)
  if (dateString.length === 10) {
    const cleanDate = dateString.replace(' ', 'T')
    const [year, month, day] = cleanDate.split('T')[0].split('-').map(Number)
    return new Date(year, month - 1, day).toLocaleDateString('pt-BR')
  }
  const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
  return new Date(utcDateString).toLocaleDateString('pt-BR')
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
  const date = new Date(utcDateString)
  return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
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
  }, 150) // 150ms delay to allow moving to bubble
}

const cancelClose = () => {
  if (closeTimeout.value) {
    clearTimeout(closeTimeout.value)
    closeTimeout.value = null
  }
}

const getBubblePosition = (id) => {
  const button = document.querySelector(`[data-lote-id="${id}"]`)
  if (!button) return {}

  const rect = button.getBoundingClientRect()
  return {
    top: `${rect.bottom + 8}px`,
    left: `${rect.right - 200}px`
  }
}

// Create/Edit Logic
const openCreateModal = () => {
  selectedProduction.value = null
  isFormModalOpen.value = true
}

const openEditModal = (production) => {
  if (!userStore.user?.is_master) {
    toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem alterar lotes.', type: 'error' })
    activeOptionsId.value = null
    activeCardMenu.value = null
    return
  }
  selectedProduction.value = { ...production }
  isFormModalOpen.value = true
  activeOptionsId.value = null
}

const closeFormModal = () => {
  isFormModalOpen.value = false
  selectedProduction.value = null
}

const handleSaveProduction = async (formData) => {
  isLoading.value = true
  const isEdit = !!selectedProduction.value?.num_lote
  const url = isEdit
    ? `/api/productions/${selectedProduction.value.num_lote}`
    : '/api/productions'
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
        await fetchProductions()
        closeFormModal()
        toastStore.add({
          title: 'Lote Atualizado',
          message: `Lote #${formData.num_lote} atualizado com sucesso.`,
          type: 'success'
        })
      } else {
        // For production, num_lote is usually in formData, but if backend generates it or we want to be safe
        const createdProduction = await response.json()
        await fetchProductions()
        closeFormModal()
        toastStore.add({
          title: 'Lote Criado',
          message: `Lote #${createdProduction.num_lote || formData.num_lote} registrado com sucesso.`,
          type: 'success'
        })
      }
    } else {
      const error = await response.json()
      toastStore.add({
        title: 'Erro ao Salvar',
        message: error.error || 'Não foi possível salvar o lote.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error saving production:', error)
  } finally {
    isLoading.value = false
  }
}

// Delete Logic
const openDeleteModal = (production) => {
  if (!userStore.user?.is_master) {
    toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem excluir lotes.', type: 'error' })
    activeOptionsId.value = null
    activeCardMenu.value = null
    return
  }
  selectedProduction.value = production
  isDeleteModalOpen.value = true
  activeOptionsId.value = null
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  selectedProduction.value = null
}

const handleDeleteProduction = async () => {
  if (!selectedProduction.value) return
  isLoading.value = true

  try {
    const lote = selectedProduction.value.num_lote
    const response = await fetch(`/api/productions/${lote}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })

    if (response.ok) {
      await fetchProductions()
      closeDeleteModal()
      toastStore.add({
        title: 'Lote Removido',
        message: `Lote #${lote} removido com sucesso.`,
        type: 'success'
      })
    } else {
      toastStore.add({
        title: 'Erro ao Deletar',
        message: 'Não foi possível remover o lote.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error deleting production:', error)
  } finally {
    isLoading.value = false
  }
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
  fetchProductions()
  closeFilterModal()
}

const openStatsModal = () => {
  isStatsModalOpen.value = true
}

const closeStatsModal = () => {
  isStatsModalOpen.value = false
}

onMounted(() => {
  fetchProductions()
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
