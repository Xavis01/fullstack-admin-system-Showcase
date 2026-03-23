<template>
  <div id="background" class="min-h-screen bg-gray-200 font-montserrat">
    <section id="product">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
        <!-- Header -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 md:mb-8 gap-4">
          <div class="flex items-center gap-2 md:gap-4">
            <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
              <Package class="text-white w-6 h-6 md:w-8 md:h-8" />
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">GERENCIAR PRODUTOS
            </h2>
          </div>
          <div class="flex flex-col sm:flex-row gap-2 md:gap-4 w-full lg:w-auto">
            <button @click="openFilterModal"
              class="w-full sm:w-auto order-2 lg:order-1 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Filter class="w-5 h-5" />
              FILTRAR
            </button>
            <button @click="openCreateModal"
              class="w-full sm:w-auto order-1 lg:order-2 bg-neutral-700 hover:bg-neutral-800 active:scale-95 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Plus class="w-5 h-5" />
              NOVO PRODUTO
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isFetching" class="flex justify-center items-center h-64">
          <LoaderCircle class="animate-spin text-neutral-700 w-8 h-8 md:w-12 md:h-12" />
        </div>

        <!-- Empty State (No Records) -->
        <div v-else-if="products.length === 0 && !filters.name"
          class="flex flex-col items-center justify-center h-64 text-gray-500">
          <Package class="mb-4 text-gray-400 w-12 h-12 md:w-16 md:h-16" />
          <p class="text-lg md:text-xl font-semibold">Nenhum produto cadastrado</p>
          <p class="text-xs md:text-sm mt-2">Clique em "+ NOVO PRODUTO" para adicionar o primeiro produto</p>
        </div>

        <!-- Empty State (No Matches) -->
        <div v-else-if="products.length === 0" class="flex flex-col items-center justify-center h-64 text-gray-500">
          <div class="mb-4 text-red-500">
            <AlertTriangle class="w-12 h-12 md:w-16 md:h-16" />
          </div>
          <p class="text-lg md:text-xl font-semibold text-gray-700">Nenhum registro encontrado</p>
          <p class="text-xs md:text-sm mt-2">Tente ajustar os filtros para encontrar o que procura</p>
        </div>

        <!-- Product Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
          <div v-for="(product, index) in products" :key="product.id"
            class="animate-fade-in bg-neutral-800 rounded-2xl shadow-lg overflow-hidden relative group p-2"
            :style="{ animationDelay: `${index * 100}ms` }">
            <!-- Image Container (White Box) -->
            <div class="bg-white rounded-xl h-64 w-full flex items-center justify-center mb-4 relative overflow-hidden">
              <img v-if="product.image_path" :src="getImageUrl(product.image_path)" alt="Product Image"
                class="max-h-full max-w-full object-contain p-4" />
              <div v-else class="text-gray-300">
                <Package size="64" />
              </div>
            </div>

            <!-- Product Name -->
            <div class="text-white text-center pb-2">
              <h3 class="font-bold text-lg truncate">{{ product.nome }}</h3>
            </div>

            <!-- Divider -->
            <div class="border-t border-gray-600 my-2"></div>

            <!-- Stock Info -->
            <div class="text-white pt-2">
              <div class="flex justify-between text-center divide-x divide-gray-600">
                <div class="w-1/2 px-2">
                  <p class="text-[10px] uppercase text-gray-400 mb-1">ESTOQUE TOTAL</p>
                  <div class="bg-white text-neutral-800 font-bold py-1 px-2 rounded-lg text-sm">
                    {{ product.total_acumulado_caixa || 0 }} {{ product.nome?.toUpperCase().includes('25KG') ? 'SACOS' :
                    'CAIXAS' }}
                  </div>
                </div>
                <div class="w-1/2 px-2">
                  <p class="text-[10px] uppercase text-gray-400 mb-1">ITENS POR CAIXA</p>
                  <div class="bg-white text-neutral-800 font-bold py-1 px-2 rounded-lg text-sm">
                    {{ product.unidades_por_caixa }} UNIDADES
                  </div>
                </div>
              </div>
            </div>


            <!-- Desktop Hover Options Button (hidden on mobile) -->
            <div
              class="hidden md:block absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <button @mouseenter="openOptions(product.id)" @mouseleave="scheduleClose(product.id)"
                class="bg-neutral-200 hover:bg-neutral-300 p-1 rounded-full text-neutral-700">
                <MoreHorizontal size="24" />
              </button>

              <!-- Options Bubble (desktop) -->
              <transition name="bubble">
                <div v-if="activeOptionsId === product.id"
                  class="absolute top-0 right-0 mt-8 mr-[-10px] bg-white rounded-lg shadow-xl p-4 z-20 w-48 border border-gray-100"
                  @mouseenter="cancelClose" @mouseleave="scheduleClose(product.id)">
                  <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                    <p>CRIADO EM: {{ formatDate(product.created_at) }}</p>
                    <p>CRIADO AS: {{ formatTime(product.created_at) }}</p>
                  </div>
                  <div class="flex flex-col gap-2">
                    <button @click="openEditModal(product)"
                      class="bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-1 px-4 rounded text-xs transition">ALTERAR</button>
                    <button @click="openDeleteModal(product)"
                      class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed"
                      :disabled="product.has_dependencies">
                      DELETAR
                    </button>
                    <div v-if="product.has_dependencies"
                      class="text-[10px] text-red-500 text-center leading-tight mt-1 font-semibold">
                      Produto com lotes ou vendas vinculadas não pode ser excluído.
                    </div>
                  </div>
                </div>
              </transition>
            </div>

            <!-- Mobile Menu Button (visible only on mobile) -->
            <div class="md:hidden absolute top-4 right-4">
              <button @click="toggleCardMenu(product.id)" :data-card-menu="product.id"
                class="bg-neutral-200 hover:bg-neutral-300 active:scale-95 p-1.5 rounded-full text-neutral-700">
                <MoreVertical class="w-5 h-5" />
              </button>

              <!-- Mobile Dropdown (Teleport) -->
              <Teleport to="body">
                <transition name="bubble">
                  <div v-if="activeCardMenu === product.id" @click.stop
                    class="fixed bg-white rounded-lg shadow-xl border border-gray-100 p-4 w-56 z-[60]"
                    :style="getCardMenuPosition(product.id)">
                    <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                      <p>CRIADO EM: {{ formatDate(product.created_at) }}</p>
                      <p>CRIADO AS: {{ formatTime(product.created_at) }}</p>
                    </div>
                    <div class="flex flex-col gap-2">
                      <button @click="openEditModal(product); activeCardMenu = null"
                        class="bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-1 px-4 rounded text-xs transition">
                        ALTERAR
                      </button>
                      <button @click="openDeleteModal(product); activeCardMenu = null"
                        class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed"
                        :disabled="product.has_dependencies">
                        DELETAR
                      </button>
                      <div v-if="product.has_dependencies"
                        class="text-[10px] text-red-500 text-center leading-tight mt-1 font-semibold">
                        Produto com lotes ou vendas vinculadas não pode ser excluído.
                      </div>
                    </div>
                  </div>
                </transition>
              </Teleport>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <ProductFormModal :isOpen="isFormModalOpen" :product="selectedProduct" :loading="isLoading" @close="closeFormModal"
      @save="handleSaveProduct" />

    <ProductDeleteModal :isOpen="isDeleteModalOpen" :itemName="selectedProduct?.nome" :loading="isLoading"
      @close="closeDeleteModal" @confirm="handleDeleteProduct" />

    <ProductFilterModal :isOpen="isFilterModalOpen" :currentFilters="filters" @close="closeFilterModal"
      @apply="handleApplyFilters" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { MoreHorizontal, MoreVertical, Package, LoaderCircle, Filter, Plus, AlertTriangle } from 'lucide-vue-next'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import ProductFormModal from '../components/products/ProductFormModal.vue'
import ProductDeleteModal from '../components/products/ProductDeleteModal.vue'
import ProductFilterModal from '../components/products/ProductFilterModal.vue'
import { useToastStore } from '../stores/toast'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()

// Ensure valid session
userStore.ensureValidSession(router)

const products = ref([])
const activeOptionsId = ref(null)

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

// Click-outside and scroll handlers for mobile cards
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
const isDeleteModalOpen = ref(false)
const isFilterModalOpen = ref(false)
const selectedProduct = ref(null)
const isLoading = ref(false)
const isFetching = ref(false)

const filters = ref({
  name: '',
  sort_by: '',
  order: 'asc'
})

const fetchProducts = async () => {
  isFetching.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.name) params.append('name', filters.value.name)
    if (filters.value.sort_by) params.append('sort_by', filters.value.sort_by)
    if (filters.value.order) params.append('order', filters.value.order)

    const response = await fetch(`/api/products?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    if (response.ok) {
      products.value = await response.json()
    } else {
      console.error('Failed to fetch products')
    }
  } catch (error) {
    console.error('Error fetching products:', error)
  } finally {
    isFetching.value = false
  }
}

const getImageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  let cleanPath = path.replace(/^backend[\\/]/, '').replace(/\\/g, '/')
  return `/${cleanPath}`
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
  }, 150)
}

const cancelClose = () => {
  if (closeTimeout.value) {
    clearTimeout(closeTimeout.value)
    closeTimeout.value = null
  }
}

// Create/Edit Logic
const openCreateModal = () => {
  selectedProduct.value = null
  isFormModalOpen.value = true
}

const openEditModal = (product) => {
  selectedProduct.value = { ...product }
  isFormModalOpen.value = true
  activeOptionsId.value = null // Close options
}

const closeFormModal = () => {
  isFormModalOpen.value = false
  selectedProduct.value = null
}

const handleSaveProduct = async (formData) => {
  isLoading.value = true
  const isEdit = !!selectedProduct.value?.id
  const url = isEdit
    ? `/api/products/${selectedProduct.value.id}`
    : '/api/products'
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
      await fetchProducts()
      closeFormModal()
      toastStore.add({
        title: isEdit ? 'Produto Atualizado' : 'Produto Criado',
        message: `Produto '${formData.nome}' ${isEdit ? 'atualizado' : 'criado'} com sucesso.`,
        type: 'success'
      })
    } else {
      const errorData = await response.json()
      console.error('Failed to save product', errorData)
      toastStore.add({
        title: 'Erro ao Salvar',
        message: errorData.error || 'Não foi possível salvar o produto.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error saving product:', error)
  } finally {
    isLoading.value = false
  }
}

// Delete Logic
const openDeleteModal = (product) => {
  selectedProduct.value = product
  isDeleteModalOpen.value = true
  activeOptionsId.value = null // Close options
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  selectedProduct.value = null
}

const handleDeleteProduct = async () => {
  if (!selectedProduct.value) return
  isLoading.value = true

  try {
    const productName = selectedProduct.value.nome
    const response = await fetch(`/api/products/${selectedProduct.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })

    if (response.ok) {
      await fetchProducts()
      closeDeleteModal()
      toastStore.add({
        title: 'Produto Removido',
        message: `Produto '${productName}' removido com sucesso.`,
        type: 'success'
      })
    } else {
      const errorData = await response.json()
      console.error('Failed to delete product', errorData)
      toastStore.add({
        title: 'Erro ao Deletar',
        message: errorData.error || 'Não foi possível remover o produto.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error deleting product:', error)
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
  fetchProducts()
  closeFilterModal()
}

onMounted(() => {
  document.addEventListener('click', cardMenuClickHandler)
  window.addEventListener('scroll', handleScroll, true)
  fetchProducts()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', cardMenuClickHandler)
  window.removeEventListener('scroll', handleScroll, true)
})
</script>

<style scoped>
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
</style>
