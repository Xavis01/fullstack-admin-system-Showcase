<template>
  <div id="background" class="min-h-screen bg-gray-200 font-montserrat">
    <section id="admin">
      <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
        <!-- Header -->
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 md:mb-8 gap-4">
          <div class="flex items-center gap-2 md:gap-4">
            <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
              <ShieldUser class="text-white w-6 h-6 md:w-8 md:h-8" />
            </div>
            <h2 class="text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">GERENCIAR USUÁRIOS
            </h2>
          </div>
          <div class="w-full lg:w-auto flex items-center gap-3">
            <button @click="openCreateModal"
              class="w-full lg:w-auto bg-neutral-700 hover:bg-neutral-800 text-white font-semibold h-11 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
              <Plus class="w-5 h-5" />
              NOVO USUÁRIO
            </button>
            <button @click="openSyncModal"
              class="bg-white hover:bg-gray-100 text-neutral-700 w-11 h-11 rounded-xl shadow-lg flex items-center justify-center transition duration-200 border border-gray-200"
              title="Sincronizar Banco de Dados">
              <DatabaseBackup class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isFetching" class="flex justify-center items-center h-64">
          <LoaderCircle class="animate-spin text-neutral-700 w-8 h-8 md:w-12 md:h-12" />
        </div>

        <!-- Empty State -->
        <div v-else-if="users.length === 0" class="flex flex-col items-center justify-center h-64 text-gray-500">
          <ShieldUser :size="48" class="mb-4 text-gray-400 md:w-16 md:h-16" />
          <p class="text-lg md:text-xl font-semibold">Nenhum usuário encontrado</p>
        </div>

        <!-- User List -->
        <div v-else>
          <!-- Desktop Table (lg+) -->
          <div class="relative hidden lg:block">
            <div class="rounded-2xl shadow-lg">
              <!-- Table Header -->
              <div
                class="bg-neutral-700 text-white grid grid-cols-[80px_2fr_2fr_1.5fr_100px_70px] gap-4 px-6 py-4 font-bold text-sm uppercase rounded-t-2xl items-center">
                <div>ID</div>
                <div>NOME</div>
                <div>EMAIL</div>
                <div>DATA NASC.</div>
                <div class="text-center">ADMIN</div>
                <div class="text-center">AÇÕES</div>
              </div>

              <!-- Table Body -->
              <div class="bg-white rounded-b-2xl overflow-hidden">
                <div v-for="user in users" :key="user.id"
                  class="grid grid-cols-[80px_2fr_2fr_1.5fr_100px_70px] gap-4 px-6 py-4 border-b border-gray-200 hover:bg-red-50 transition relative last:border-b-0 items-center">
                  <div class="font-bold text-neutral-800">#{{ user.id }}</div>
                  <div class="font-semibold text-neutral-700">{{ user.nome }}</div>
                  <div class="text-neutral-600 truncate">{{ user.email }}</div>
                  <div class="text-neutral-600">{{ formatDate(user.dt_nascimento) }}</div>
                  <div class="text-center">
                    <span class="px-2 py-1 rounded text-xs font-bold"
                      :class="user.is_master ? 'bg-red-100 text-red-600' : user.is_admin ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'">
                      {{ user.is_admin ? 'SIM' : 'NÃO' }}
                    </span>
                  </div>

                  <div class="relative text-center">
                    <button @mouseenter="openOptions(user.id)" @mouseleave="scheduleClose(user.id)"
                      :data-user-id="user.id"
                      class="text-neutral-600 hover:text-neutral-800 transition hover:bg-red-100 rounded-full p-1">
                      <MoreHorizontal size="20" />
                    </button>

                    <!-- Options Bubble -->
                    <transition name="bubble">
                      <div v-if="activeOptionsId === user.id"
                        class="fixed bg-white rounded-lg shadow-xl p-4 z-50 w-48 border border-gray-100"
                        :style="getBubblePosition(user.id)" @mouseenter="cancelClose"
                        @mouseleave="scheduleClose(user.id)">
                        <div class="text-[10px] text-gray-500 mb-3 leading-tight text-left">
                          <p>CRIADO EM: {{ formatDate(user.created_at) }}</p>
                          <p>CRIADO AS: {{ formatTime(user.created_at) }}</p>
                        </div>
                        <div class="flex flex-col gap-2">
                          <button @click="openEditModal(user)"
                            class="bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-1 px-4 rounded text-xs transition">ALTERAR</button>
                          <!-- Only allow deleting IF not self (id 1 usually root, or current user) -->
                          <button @click="openDeleteModal(user)"
                            :disabled="user.id === 1 || user.id === userStore.user.id"
                            class="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-1 px-4 rounded text-xs transition disabled:opacity-50 disabled:cursor-not-allowed">
                            DELETAR
                          </button>
                        </div>
                      </div>
                    </transition>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Mobile Cards (< lg) -->
          <div class="block lg:hidden space-y-4">
            <div v-for="user in users" :key="user.id"
              class="bg-white rounded-2xl shadow-lg p-4 border border-gray-200 hover:border-red-300 transition">
              <!-- User Header -->
              <div class="flex items-start justify-between mb-3 pb-3 border-b border-gray-200">
                <div
                  class="bg-red-600 text-white font-bold text-sm w-10 h-10 rounded-lg flex items-center justify-center">
                  #{{ user.id }}
                </div>
                <div>
                  <h3 class="font-bold text-neutral-800 text-base">{{ user.nome }}</h3>
                  <p class="text-xs text-neutral-500 mt-0.5">ID: {{ user.id }}</p>
                </div>
              </div>

              <!-- User Details -->
              <div class="space-y-2.5 mb-4">
                <div class="flex items-start gap-2">
                  <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Email:</span>
                  <span class="text-sm text-neutral-700 break-all">{{ user.email }}</span>
                </div>
                <div class="flex items-start gap-2">
                  <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Nascimento:</span>
                  <span class="text-sm text-neutral-700">{{ formatDate(user.dt_nascimento) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Admin:</span>
                  <span class="px-2 py-0.5 rounded text-xs font-bold"
                    :class="user.is_master ? 'bg-red-100 text-red-600' : user.is_admin ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'">
                    {{ user.is_admin ? 'SIM' : 'NÃO' }}
                  </span>
                </div>
                <div class="flex items-start gap-2">
                  <span class="text-xs font-semibold text-neutral-500 uppercase min-w-[80px]">Criado em:</span>
                  <span class="text-sm text-neutral-700">{{ formatDate(user.created_at) }} às {{
                    formatTime(user.created_at) }}</span>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex gap-2 pt-3 border-t border-gray-200">
                <button @click="openEditModal(user)"
                  class="flex-1 bg-gray-200 hover:bg-gray-300 text-neutral-800 font-bold py-2.5 px-4 rounded-lg text-sm transition active:scale-95">
                  ALTERAR
                </button>
                <button @click="openDeleteModal(user)" :disabled="user.id === 1 || user.id === userStore.user.id"
                  class="flex-1 bg-red-100 hover:bg-red-200 text-red-600 font-bold py-2.5 px-4 rounded-lg text-sm transition active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed">
                  DELETAR
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <AdminFormModal :isOpen="isFormModalOpen" :user="selectedUser" :loading="isLoading" @close="closeFormModal"
      @save="handleSaveUser" />

    <AdminDeleteModal :isOpen="isDeleteModalOpen" :itemName="selectedUser?.nome" :loading="isLoading"
      @close="closeDeleteModal" @confirm="handleDeleteUser" />

    <AdminSyncDbModal :isOpen="isSyncModalOpen" :loading="isSyncLoading" @close="closeSyncModal"
      @confirm="handleSyncDatabase" />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ShieldUser, LoaderCircle, Plus, MoreHorizontal, DatabaseBackup } from 'lucide-vue-next'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { useToastStore } from '../stores/toast'
import AdminFormModal from '../components/admin/AdminFormModal.vue'
import AdminDeleteModal from '../components/admin/AdminDeleteModal.vue'
import AdminSyncDbModal from '../components/admin/AdminSyncDbModal.vue'

const userStore = useUserStore()
const toastStore = useToastStore()
const router = useRouter()

// Ensure valid session and ID 1 check
userStore.ensureValidSession(router)
if (userStore.user?.id !== 1) {
  toastStore.add({ title: 'Acesso Negado', message: 'Você não tem permissão para acessar esta página.', type: 'error' })
  router.push('/')
}

const users = ref([])
const activeOptionsId = ref(null)

// Modal states
const isFormModalOpen = ref(false)
const isDeleteModalOpen = ref(false)
const selectedUser = ref(null)
const isLoading = ref(false)
const isFetching = ref(false)

const fetchUsers = async () => {
  isFetching.value = true
  try {
    const response = await fetch('/api/users', {
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    if (response.ok) {
      users.value = await response.json()
    } else {
      console.error('Failed to fetch users')
    }
  } catch (error) {
    console.error('Error fetching users:', error)
  } finally {
    isFetching.value = false
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
  const button = document.querySelector(`[data-user-id="${id}"]`)
  if (!button) return {}

  const rect = button.getBoundingClientRect()
  return {
    top: `${rect.bottom + 8}px`,
    left: `${rect.right - 200}px`
  }
}

// Create/Edit Logic
const openCreateModal = () => {
  selectedUser.value = null
  isFormModalOpen.value = true
}

const openEditModal = (user) => {
  selectedUser.value = { ...user }
  isFormModalOpen.value = true
  activeOptionsId.value = null
}

const closeFormModal = () => {
  isFormModalOpen.value = false
  selectedUser.value = null
}

const handleSaveUser = async (formData) => {
  isLoading.value = true
  const isEdit = !!selectedUser.value?.id
  const url = isEdit
    ? `/api/users/${selectedUser.value.id}`
    : '/api/users'
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
      await fetchUsers()
      closeFormModal()
      toastStore.add({
        title: isEdit ? 'Usuário Atualizado' : 'Usuário Criado',
        message: `Administrador '${formData.nome}' ${isEdit ? 'atualizado' : 'criado'} com sucesso.`,
        type: 'success'
      })
    } else {
      const errorData = await response.json()
      toastStore.add({
        title: 'Erro ao Salvar',
        message: errorData.error || 'Não foi possível salvar.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error saving user:', error)
  } finally {
    isLoading.value = false
  }
}

// Delete Logic
const openDeleteModal = (user) => {
  selectedUser.value = user
  isDeleteModalOpen.value = true
  activeOptionsId.value = null
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  selectedUser.value = null
}

const handleDeleteUser = async () => {
  if (!selectedUser.value) return
  isLoading.value = true

  try {
    const userName = selectedUser.value.nome
    const response = await fetch(`/api/users/${selectedUser.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })

    if (response.ok) {
      await fetchUsers()
      closeDeleteModal()
      toastStore.add({
        title: 'Usuário Removido',
        message: `Administrador '${userName}' removido com sucesso.`,
        type: 'success'
      })
    } else {
      const errorData = await response.json()
      toastStore.add({
        title: 'Erro ao Deletar',
        message: errorData.error || 'Não foi possível remover.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error deleting user:', error)
  } finally {
    isLoading.value = false
  }
}

// Sync Database Logic
const isSyncModalOpen = ref(false)
const isSyncLoading = ref(false)

const openSyncModal = () => {
  isSyncModalOpen.value = true
}

const closeSyncModal = () => {
  isSyncModalOpen.value = false
}

const handleSyncDatabase = async () => {
  isSyncLoading.value = true
  try {
    const response = await fetch('/api/admin/sync-database', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })

    if (response.ok) {
      closeSyncModal()
      toastStore.add({
        title: 'Banco Sincronizado',
        message: 'O banco de dados foi atualizado com sucesso.',
        type: 'success'
      })
    } else {
      const errorData = await response.json()
      toastStore.add({
        title: 'Erro ao Sincronizar',
        message: errorData.error || 'Não foi possível sincronizar o banco.',
        type: 'error'
      })
    }
  } catch (error) {
    console.error('Error syncing database:', error)
    toastStore.add({
      title: 'Erro de Conexão',
      message: 'Não foi possível conectar ao servidor.',
      type: 'error'
    })
  } finally {
    isSyncLoading.value = false
  }
}

onMounted(() => {
  // Only fetch if has permission
  if (userStore.user?.id === 1) {
    fetchUsers()
  }
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
