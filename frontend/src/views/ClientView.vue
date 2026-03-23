<template>
  <div id="background" class="min-h-screen bg-gray-200 font-montserrat">
    <section id="client">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
        <!-- Header -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 md:mb-8 gap-4">
          <div class="flex items-center gap-2 md:gap-4">
            <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
              <Users class="text-white w-6 h-6 md:w-8 md:h-8" />
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">GERENCIAR CLIENTES
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
              NOVO CLIENTE
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isFetching" class="flex justify-center items-center h-64">
          <LoaderCircle class="animate-spin text-neutral-700 w-8 h-8 md:w-12 md:h-12" />
        </div>

        <!-- Empty State (No Records) -->
        <div v-else-if="clients.length === 0 && !filters.name"
          class="flex flex-col items-center justify-center h-64 text-gray-500">
          <Users class="mb-4 text-gray-400 w-12 h-12 md:w-16 md:h-16" />
          <p class="text-lg md:text-xl font-semibold">Nenhum cliente cadastrado</p>
          <p class="text-xs md:text-sm mt-2">Clique em "+ NOVO CLIENTE" para adicionar o primeiro cliente</p>
        </div>

        <!-- Empty State (No Matches) -->
        <div v-else-if="clients.length === 0" class="flex flex-col items-center justify-center h-64 text-gray-500">
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
              class="bg-neutral-700 text-white grid grid-cols-[70px_4fr_2fr_1.2fr_1.2fr_70px] gap-4 px-6 py-4 font-bold text-sm uppercase rounded-t-2xl items-center">
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
              <div>Nome</div>
              <div>Telefone</div>
              <div class="text-center">Compras</div>
              <div class="text-center">Total</div>
              <div class="text-center">Mais</div>
            </div>

            <!-- Scrollable Table Body -->
            <div
              class="max-h-[640px] overflow-y-auto relative scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200 rounded-b-2xl bg-white custom-scrollbar"
              ref="tableBody">
              <div v-for="client in clients" :key="client.id"
                class="bg-white grid grid-cols-[70px_4fr_2fr_1.2fr_1.2fr_70px] gap-4 px-6 py-4 border-b border-gray-200 hover:bg-red-50 transition relative last:border-b-0 items-center">
                <div class="font-bold text-neutral-800">#{{ client.id }}</div>
                <div class="text-neutral-800">{{ client.nome }}</div>
                <div class="text-neutral-600">{{ client.telefone || 'Não Informado' }}</div>
                <div class="text-neutral-800 text-center">{{ client.total_compras || 0 }}</div>
                <!-- Sales Detail Dropdown -->
                <div>
                  <SalesDetailSelect :total="client.total_caixas || 0" :sales="client.sales || []" />
                </div>
                <div class="relative text-center">
                  <button @mouseenter="openOptions(client.id)" @mouseleave="scheduleClose(client.id)"
                    :data-client-id="client.id"
                    class="text-neutral-600 hover:text-neutral-800 transition hover:bg-red-100 rounded-full p-1">
                    <MoreHorizontal size="20" />
                  </button>

                  <!-- Options Bubble -->
                  <Teleport to="body">
                    <transition name="bubble">
                      <div v-if="activeOptionsId === client.id"
                        class="fixed bg-white rounded-lg shadow-xl p-4 z-50 w-48 border border-gray-100 font-montserrat"
                        :style="getBubblePosition(client.id)" @mouseenter="cancelClose"
                        @mouseleave="scheduleClose(client.id)">
                        <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                          <p>CRIADO EM: {{ formatDate(client.created_at) }}</p>
                          <p>CRIADO AS: {{ formatTime(client.created_at) }}</p>
                        </div>
                        <div class="flex flex-col gap-2">
                          <button @click="openEditModal(client)"
                            class="bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-1 px-4 rounded text-xs transition">ALTERAR</button>
                          <button @click="openDeleteModal(client)"
                            class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed"
                            :disabled="client.total_compras > 0">
                            DELETAR
                          </button>
                          <div v-if="client.total_compras > 0"
                            class="text-[10px] text-red-500 text-center leading-tight mt-1 font-semibold">
                            Cliente com vendas vinculadas não pode ser excluído.
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
              <span class="text-sm text-gray-600">{{ clients.length }} {{ clients.length === 1 ? 'cliente' : 'clientes'
              }}</span>
              <button @click="toggleSort"
                class="flex items-center gap-2 bg-white px-3 py-2 rounded-lg shadow active:scale-95 transition">
                <span class="text-sm font-semibold">Ordenar</span>
                <ArrowUpWideNarrow v-if="sortOrder === 'desc'" class="w-4 h-4 text-red-600" />
                <ArrowUpNarrowWide v-else class="w-4 h-4 text-red-600" />
              </button>
            </div>

            <div class="space-y-4 animate-fade-in">
              <div v-for="client in clients" :key="client.id"
                class="bg-white rounded-2xl shadow-lg p-4 border border-gray-200 relative">
                <!-- Header com ícone, ID, Nome e menu (⋮) -->
                <div class="flex items-start justify-between mb-3 pb-3 border-b border-gray-100">
                  <div class="flex items-center gap-3 flex-1 min-w-0">
                    <div
                      class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                      <Users :size="20" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="font-bold text-neutral-800 text-lg">#{{ client.id }}</div>
                      <div class="text-sm text-neutral-600 truncate font-semibold">{{ client.nome }}</div>
                    </div>
                  </div>

                  <!-- Menu de 3 pontos -->
                  <div class="relative flex-shrink-0">
                    <button @click="toggleCardMenu(client.id)" :data-card-menu="client.id"
                      class="p-2 hover:bg-gray-100 rounded-lg transition">
                      <MoreVertical class="w-5 h-5 text-gray-600" />
                    </button>
                    <!-- Dropdown menu -->
                    <Teleport to="body">
                      <transition name="bubble">
                        <div v-if="activeCardMenu === client.id" @click.stop
                          class="fixed bg-white rounded-lg shadow-xl border border-gray-100 p-4 w-56 z-[60]"
                          :style="getCardMenuPosition(client.id)">
                          <div class="text-[10px] text-gray-500 mb-3 leading-tight">
                            <p>CRIADO EM: {{ formatDate(client.created_at) }}</p>
                            <p>CRIADO AS: {{ formatTime(client.created_at) }}</p>
                          </div>
                          <div class="flex flex-col gap-2">
                            <button @click="openEditModal(client); activeCardMenu = null"
                              class="bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-1 px-4 rounded text-xs transition">
                              ALTERAR
                            </button>
                            <button @click="openDeleteModal(client); activeCardMenu = null"
                              class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed"
                              :disabled="client.total_compras > 0">
                              DELETAR
                            </button>
                            <div v-if="client.total_compras > 0"
                              class="text-[10px] text-red-500 text-center leading-tight mt-1 font-semibold">
                              Cliente com vendas vinculadas não pode ser excluído.
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
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Telefone:</span>
                    <span class="text-neutral-700">{{ client.telefone || 'Não Informado' }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Compras:</span>
                    <span class="text-neutral-700">{{ client.total_compras || 0 }}</span>
                  </div>
                  <div class="flex items-center gap-2 w-full">
                    <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Total:</span>
                    <div class="flex-1">
                      <SalesDetailSelect :total="client.total_caixas || 0" :sales="client.sales || []" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <ClientFormModal :isOpen="isFormModalOpen" :client="selectedClient" :loading="isLoading" @close="closeFormModal"
      @save="handleSaveClient" />

    <ClientDeleteModal :isOpen="isDeleteModalOpen" :itemName="selectedClient?.nome" :loading="isLoading"
      @close="closeDeleteModal" @confirm="handleDeleteClient" />

    <ClientFilterModal :isOpen="isFilterModalOpen" :currentFilters="filters" @close="closeFilterModal"
      @apply="handleApplyFilters" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, nextTick } from 'vue'
import { MoreHorizontal, MoreVertical, LoaderCircle, Users, Filter, Plus, AlertTriangle, ArrowUpWideNarrow, ArrowUpNarrowWide } from 'lucide-vue-next'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import ClientFormModal from '../components/clients/ClientFormModal.vue'
import ClientDeleteModal from '../components/clients/ClientDeleteModal.vue'
import ClientFilterModal from '../components/clients/ClientFilterModal.vue'
import SalesDetailSelect from '../components/clients/SalesDetailSelect.vue'
import { useToastStore } from '../stores/toast'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()

userStore.ensureValidSession(router)

const clients = ref([])
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
const selectedClient = ref(null)
const isLoading = ref(false)
const isFetching = ref(false)

const sortOrder = ref('asc') // asc = oldest first, desc = newest first

const filters = ref({
  name: '',
  sort_by: '',
  order: 'asc'
})

const fetchClients = async () => {
  isFetching.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.name) params.append('name', filters.value.name)
    if (filters.value.sort_by) params.append('sort_by', filters.value.sort_by)
    if (filters.value.order) params.append('order', filters.value.order)
    params.append('created_order', sortOrder.value)

    const response = await fetch(`/api/clients?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    if (response.ok) {
      clients.value = await response.json()
      await nextTick()
    } else {
      console.error('Failed to fetch clients')
    }
  } catch (error) {
    console.error('Error fetching clients:', error)
  } finally {
    isFetching.value = false
  }
}



const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  fetchClients()
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  // If simple date YYYY-MM-DD, keep existing behavior (Local Date assumption)
  if (dateString.length === 10) {
    const [year, month, day] = dateString.split('-').map(Number)
    return new Date(year, month - 1, day).toLocaleDateString('pt-BR')
  }
  // If datetime, parse as UTC so it converts to local time
  const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
  return new Date(utcDateString).toLocaleDateString('pt-BR')
}

const formatTime = (dateString) => {
  if (!dateString) return ''
  // Treat as UTC to convert to local time
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

const getBubblePosition = (id) => {
  const button = document.querySelector(`[data-client-id="${id}"]`)
  if (!button) return {}

  const rect = button.getBoundingClientRect()
  return {
    top: `${rect.bottom + 8}px`,
    left: `${rect.right - 200}px`
  }
}

// Create/Edit Logic
const openCreateModal = () => {
  selectedClient.value = null
  isFormModalOpen.value = true
}

const openEditModal = (client) => {
  selectedClient.value = { ...client }
  isFormModalOpen.value = true
  activeOptionsId.value = null
}

const closeFormModal = () => {
  isFormModalOpen.value = false
  selectedClient.value = null
}

const handleSaveClient = async (formData) => {
  isLoading.value = true
  const isEdit = !!selectedClient.value?.id
  const url = isEdit
    ? `/api/clients/${selectedClient.value.id}`
    : '/api/clients'
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
      await fetchClients()
      closeFormModal()
      toastStore.add({
        title: isEdit ? 'Cliente Atualizado' : 'Cliente Criado',
        message: `Cliente '${formData.nome}' ${isEdit ? 'atualizado' : 'cadastrado'} com sucesso.`,
        type: 'success'
      })
    } else {
      const errorData = await response.json()
      console.error('Failed to save client', errorData)
      toastStore.add({
        title: 'Erro ao Salvar',
        message: errorData.error || 'Não foi possível salvar os dados do cliente.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error saving client:', error)
  } finally {
    isLoading.value = false
  }
}

// Delete Logic
const openDeleteModal = (client) => {
  selectedClient.value = client
  isDeleteModalOpen.value = true
  activeOptionsId.value = null
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  selectedClient.value = null
}

const handleDeleteClient = async () => {
  if (!selectedClient.value) return
  isLoading.value = true

  try {
    const clientName = selectedClient.value.nome
    const response = await fetch(`/api/clients/${selectedClient.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })

    if (response.ok) {
      await fetchClients()
      closeDeleteModal()
      toastStore.add({
        title: 'Cliente Removido',
        message: `Cliente '${clientName}' removido com sucesso.`,
        type: 'success'
      })
    } else {
      const errorData = await response.json()
      console.error('Failed to delete client', errorData)
      toastStore.add({
        title: 'Erro ao Deletar',
        message: errorData.error || 'Não foi possível remover o cliente.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error deleting client:', error)
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
  fetchClients()
  closeFilterModal()
}

onMounted(() => {
  document.addEventListener('click', cardMenuClickHandler)
  window.addEventListener('scroll', handleScroll, true)
  fetchClients()
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
