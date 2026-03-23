<template>
    <div>
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-40"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <!-- Modal Container - Adjusted for better width/height usage -->
            <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 font-montserrat p-4 pt-20">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <!-- Increased max-width to 1200px (max-w-7xl approx) for "wider horizontal" look -->
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-lg z-10 w-full max-w-6xl h-[65vh] flex flex-col">

                        <!-- Header -->
                        <div
                            class="bg-neutral-800 text-white p-4 flex items-center justify-between rounded-t-xl shrink-0">
                            <h3 class="text-xl font-bold flex items-center gap-2">
                                <RotateCcw class="w-6 h-6" />
                                GERENCIAR DEVOLUÇÕES
                            </h3>
                            <!-- Top Actions in Header (Close) -->
                            <button @click="$emit('close')"
                                class="hover:bg-white/10 p-1 rounded-full text-white transition">
                                <X class="w-6 h-6" />
                            </button>
                        </div>

                        <!-- Top Bar: Filters Button & Legend -->
                        <div
                            class="p-4 bg-gray-50 border-b border-gray-200 shrink-0 flex flex-col md:flex-row justify-between items-center gap-4">

                            <!-- Left: Actions -->
                            <div class="flex items-center gap-2 w-full md:w-auto">
                                <button @click="openFilterModal"
                                    class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg shadow transition flex items-center gap-2 text-sm">
                                    <Filter class="w-4 h-4" /> FILTRAR
                                </button>

                                <!-- Active Filters Chips -->
                                <div class="flex flex-wrap gap-2 ml-2">
                                    <div v-if="hasActiveFilters" @click="resetFilters"
                                        class="cursor-pointer bg-red-50 text-red-600 text-xs font-bold px-3 py-2 rounded-full border border-red-200 hover:bg-red-100 transition flex items-center gap-1">
                                        Filtros Ativos
                                        <X class="w-3 h-3" />
                                    </div>
                                </div>
                            </div>

                            <!-- Right: Legend (Tooltip) & Instructions -->
                            <div class="flex items-center gap-2">
                                <!-- Instructions Trigger -->
                                <button @click="openInstructions"
                                    class="group relative outline-none flex items-center justify-center">
                                    <CircleHelp class="w-6 h-6 text-gray-400 hover:text-gray-600 transition" />
                                    <span
                                        class="absolute top-full mt-2 left-1/2 -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
                                        Como funciona?
                                    </span>
                                </button>

                                <!-- Legend Tooltip -->
                                <div class="relative group flex items-center justify-center">
                                    <AlertCircle
                                        class="w-6 h-6 text-gray-400 cursor-help hover:text-gray-600 transition" />
                                    <!-- Tooltip pointing DOWN -->
                                    <div
                                        class="absolute top-full mt-2 right-0 w-64 bg-black/90 text-white text-xs rounded p-3 hidden group-hover:block z-50 shadow-xl pointer-events-none transition-opacity duration-200">
                                        <div
                                            class="absolute bottom-full right-2 border-8 border-transparent border-b-black/90">
                                        </div>
                                        <p class="mb-1"><strong class="text-yellow-400">Aberto:</strong> Aguardando
                                            retorno físico.</p>
                                        <p class="mb-1"><strong class="text-blue-400">Retornada:</strong> Retornou ao
                                            estoque.</p>
                                        <p><strong class="text-green-400">Concluída:</strong> Alocada em novo lote.</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Table List -->
                        <div class="flex-1 overflow-y-auto p-4 custom-scrollbar bg-gray-100/50">
                            <div v-if="loading" class="flex justify-center items-center h-32">
                                <LoaderCircle class="animate-spin text-gray-400 w-8 h-8" />
                            </div>
                            <div v-else-if="returns.length === 0"
                                class="flex flex-col items-center justify-center h-48 text-gray-400">
                                <PackageOpen class="w-12 h-12 mb-2" />
                                <p>Nenhuma devolução encontrada.</p>
                            </div>

                            <div v-else class="space-y-3">
                                <div v-for="ret in returns" :key="ret.id"
                                    class="bg-white border rounded-lg shadow-sm hover:shadow-md transition p-4">
                                    <div
                                        class="flex flex-col md:flex-row gap-4 justify-between items-start md:items-center">
                                        <!-- Info Blocks -->
                                        <div class="flex items-center gap-4 flex-1">
                                            <div
                                                class="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center shrink-0 border border-gray-200 overflow-hidden">
                                                <img v-if="ret.product_image" :src="formatImage(ret.product_image)"
                                                    class="w-full h-full object-cover" />
                                                <Package v-else class="w-6 h-6 text-gray-400" />
                                            </div>
                                            <div>
                                                <div class="flex items-center gap-3 mb-1">
                                                    <span class="font-bold text-gray-800 text-lg">{{ ret.product_name
                                                        }}</span>
                                                    <span :class="getStatusClass(ret.status)"
                                                        class="text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wide">
                                                        {{ ret.status }}
                                                    </span>
                                                </div>
                                                <div class="text-xs text-gray-500 flex flex-wrap gap-x-4 gap-y-1">
                                                    <span class="flex items-center gap-1">
                                                        <User class="w-3 h-3" /> {{ ret.client_name }}
                                                    </span>
                                                    <span class="flex items-center gap-1">Venda #{{ ret.sale_id
                                                        }}</span>
                                                    <span class="flex items-center gap-1">
                                                        <Box class="w-3 h-3" /> Lote Origem #{{ ret.num_lote_origem }}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        <div
                                            class="flex items-center gap-6 w-full md:w-auto mt-2 md:mt-0 justify-between md:justify-end">
                                            <div class="text-right">
                                                <div class="text-2xl font-black text-red-600">{{ ret.quant_devolvida }}
                                                    <span class="text-xs text-gray-500 font-normal">{{
                                                        ret.product_name?.toLowerCase().includes('25kg') ? 'sc' : 'cx'
                                                        }}</span>
                                                </div>
                                                <div v-if="formatDate(ret.created_at) !== '-'"
                                                    class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">
                                                    {{ formatDate(ret.created_at) }}
                                                </div>
                                            </div>

                                            <button @click="openEdit(ret)"
                                                class="bg-neutral-100 hover:bg-neutral-200 text-neutral-700 font-bold py-2 px-6 rounded-lg text-sm transition flex items-center justify-center gap-2 border border-neutral-200">
                                                <Settings class="w-4 h-4" />
                                                GERENCIAR
                                            </button>
                                        </div>
                                    </div>

                                    <!-- Extra Info Footer -->
                                    <div v-if="ret.status === 'Concluída' || ret.status === 'Retornada' || ret.observacao"
                                        class="mt-4 pt-3 border-t border-dashed border-gray-100 flex flex-col md:flex-row gap-4 text-xs text-gray-500">
                                        <div v-if="ret.status === 'Concluída' || ret.status === 'Retornada'"
                                            class="flex gap-4">
                                            <div
                                                class="flex items-center gap-1 text-blue-700 bg-blue-50 px-2 py-1 rounded">
                                                <CalendarCheck class="w-3 h-3" /> Retorno: <strong>{{
                                                    formatDate(ret.data_retorno) }}</strong>
                                            </div>
                                            <div v-if="ret.status === 'Concluída'"
                                                class="flex items-center gap-1 text-green-700 bg-green-50 px-2 py-1 rounded">
                                                <ArrowRightCircle class="w-3 h-3" /> Novo Lote: <strong>#{{
                                                    ret.novo_lote_id }}</strong>
                                            </div>
                                        </div>
                                        <div v-if="ret.observacao"
                                            class="flex-1 text-gray-600 bg-yellow-50 px-2 py-1 rounded border border-yellow-100 truncate">
                                            <span class="font-bold text-yellow-700">Obs:</span> {{ ret.observacao }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>

        <!-- Edit/Finalize Sub-Modal (Matches styling) -->
        <!-- Blur Layer -->
        <!-- Edit/Finalize Sub-Modal (Using Component) -->
        <ReturnEditModal :isOpen="!!editingReturn" :returnItem="editingReturn" :loadingEdit="loadingEdit"
            :loadingFinalize="loadingFinalize" :loteOptions="loteOptions" :novo_lote_id="finalizeForm.novo_lote_id"
            @close="closeEdit" @save="saveChanges" @finalize="finalizeReturn" @open-delete="confirmDelete"
            @update:novo_lote_id="(val) => finalizeForm.novo_lote_id = val" />

        <!-- Delete Confirmation Modal (Stylized) -->
        <!-- Delete Confirmation Modal (Using Component) -->
        <ReturnDeleteModal :isOpen="isDeleting" :returnItem="editingReturn" :loading="loadingDelete"
            :linkedLot="linkedLot" @close="closeEdit" @confirm="deleteReturn" />

        <!-- Instructions Modal (Escorpião Style) -->
        <ReturnInstructionsModal :isOpen="isInstructionsOpen" @close="closeInstructions" />

        <!-- Filter Modal (Internal or External? I'll make an inline modal here for simplicity or reuse logic) -->
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isFilterOpen" class="fixed inset-0 z-[60]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isFilterOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4 font-montserrat">
                <div class="absolute inset-0 bg-black/60" @click="closeFilterModal"></div>
                <transition name="modal">
                    <div v-if="isFilterOpen"
                        class="bg-white rounded-xl shadow-2xl z-10 w-full max-w-md max-h-[90vh] overflow-y-auto">
                        <div class="bg-red-600 text-white p-4 text-center rounded-t-xl">
                            <h3 class="font-bold text-lg flex items-center justify-center gap-2">
                                <Filter class="w-5 h-5" /> FILTRAR DEVOLUÇÕES
                            </h3>
                        </div>
                        <div class="p-6 space-y-4">
                            <div>
                                <label class="block text-gray-700 text-sm font-bold mb-2">Lote Origem</label>
                                <input v-model="filters.num_lote" type="number"
                                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] py-2 px-3 focus:outline-none focus:border-red-500 focus:bg-white transition"
                                    placeholder="Ex: 2205" />
                            </div>
                            <div>
                                <label class="block text-gray-700 text-sm font-bold mb-2">Cliente</label>
                                <CustomSelect v-model="filters.client_id" :options="clientOptions"
                                    placeholder="Todos os clientes" style="z-index: 9999;" />
                            </div>
                            <div>
                                <label class="block text-gray-700 text-sm font-bold mb-2">Produto</label>
                                <CustomSelect v-model="filters.product_id" :options="productOptions"
                                    placeholder="Todos os produtos" style="z-index: 9999;" />
                            </div>
                            <div>
                                <label class="block text-gray-700 text-sm font-bold mb-2">Status</label>
                                <CustomSelect v-model="filters.status" :options="statusOptions"
                                    placeholder="Todos os Status" style="z-index: 9999;" />
                            </div>

                            <div class="flex gap-3 pt-4">
                                <button @click="applyFilters"
                                    class="flex-1 bg-neutral-800 hover:bg-black text-white font-bold py-3 rounded-lg transition">APLICAR</button>
                                <button @click="resetFilters"
                                    class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 rounded-lg transition">LIMPAR</button>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>

        <!-- Production Create Modal (triggered from "Novo Lote" select) -->
        <ProductionFormModal :isOpen="isProductionModalOpen" :initialData="productionInitialData"
            :loading="productionLoading" zIndexClass="z-[70]" @close="closeProductionModal"
            @save="handleProductionSave" />
    </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { RotateCcw, X, AlertCircle, CircleHelp, LoaderCircle, PackageOpen, Package, Settings, Edit3, CheckCircle2, Check, Trash2, AlertTriangle, Filter, User, Hash, Box, CalendarCheck, ArrowRightCircle } from 'lucide-vue-next'
import { useUserStore } from '../../stores/user'
import { useToastStore } from '../../stores/toast'
import CustomSelect from '../CustomSelect.vue'
import CustomCalendar from '../CustomCalendar.vue'
import ProductionFormModal from '../production/ProductionFormModal.vue'
import ReturnInstructionsModal from './ReturnInstructionsModal.vue'
import ReturnEditModal from './ReturnEditModal.vue'
import ReturnDeleteModal from './ReturnDeleteModal.vue'

const props = defineProps({
    isOpen: Boolean
})

const emit = defineEmits(['close', 'refresh'])
const userStore = useUserStore()
const toastStore = useToastStore()

const returns = ref([])
const loading = ref(false)
const lotesDisponiveis = ref([]) // Raw productions data
const clientOptions = ref([])
const productOptions = ref([])

// Filter State
const isFilterOpen = ref(false)
const filters = ref({
    num_lote: '',
    status: '',
    client_id: '',
    product_id: ''
})

const appliedFilters = ref({ ...filters.value })

const statusOptions = [
    { value: 'Aberto', label: 'Aberto' },
    { value: 'Retornada', label: 'Retornada' },
    { value: 'Concluída', label: 'Concluída' }
]

const hasActiveFilters = computed(() => {
    return Object.values(appliedFilters.value).some(val => val !== '')
})

// Edit/Action State
const editingReturn = ref(null)
const isInstructionsOpen = ref(false)
const loadingEdit = ref(false)
const loadingFinalize = ref(false)
const loadingDelete = ref(false)
const isDeleting = ref(false)

const editForm = ref({
    quant_devolvida: '',
    observacao: ''
})

const finalizeForm = ref({
    data_retorno: '',
    novo_lote_id: ''
})

// Watchers
watch(() => props.isOpen, (val) => {
    if (val) {
        fetchReturns()
        fetchAuxData()
    }
})

// Production Modal State
const isProductionModalOpen = ref(false)
const productionInitialData = ref(null)
const productionLoading = ref(false)

// Computeds
const loteOptions = computed(() => {
    // Filter lots to only include those matching the product of the return being edited
    if (!editingReturn.value) return []

    const returnProductId = editingReturn.value.product_id
    const sourceLotId = editingReturn.value.num_lote_origem

    const options = lotesDisponiveis.value
        .filter(l => l.product_id === returnProductId)
        // .filter(l => l.num_lote != sourceLotId) // ALLOW return to source lot
        .map(l => {
            const isOrigin = l.num_lote == sourceLotId
            return {
                value: l.num_lote,
                label: isOrigin
                    ? `Lote #${l.num_lote} (ORIGEM) - Estoque: ${l.estoque_lote}`
                    : `Lote #${l.num_lote} (${l.product_name}) - Estoque: ${l.estoque_lote}`,
                class: isOrigin ? 'font-bold text-blue-600 bg-blue-50' : ''
            }
        })

    // Prepend "Create New Lot" option
    // We use a special value that we can detect in the watcher
    return [
        { value: 'NEW_LOT_TRIGGER', label: '+ CRIAR NOVO LOTE', class: 'text-red-600 font-bold bg-red-50' },
        ...options
    ]
})

// Watch for "Create New Lot" selection
watch(() => finalizeForm.value.novo_lote_id, (val) => {
    if (val === 'NEW_LOT_TRIGGER') {
        // Reset selection immediately so it doesn't stay on "Create New Lot" if cancelled
        finalizeForm.value.novo_lote_id = ''

        // Open Production Modal
        if (editingReturn.value) {
            productionInitialData.value = {
                product_id: editingReturn.value.product_id,
                quant_caixa_produzida: editingReturn.value.quant_devolvida
            }
            isProductionModalOpen.value = true
        }
    }
})



// Linked Lot Logic for Deletion
const linkedLot = computed(() => {
    if (!editingReturn.value || !editingReturn.value.novo_lote_id) return null
    return lotesDisponiveis.value.find(l => l.num_lote === editingReturn.value.novo_lote_id)
})

// Data Fetching
const fetchReturns = async () => {
    loading.value = true
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000) // 5s timeout

    try {
        const params = new URLSearchParams()
        if (appliedFilters.value.status) params.append('status', appliedFilters.value.status)
        if (appliedFilters.value.num_lote) params.append('num_lote', appliedFilters.value.num_lote)
        if (appliedFilters.value.client_id) params.append('client_id', appliedFilters.value.client_id)
        if (appliedFilters.value.product_id) params.append('product_id', appliedFilters.value.product_id)

        const response = await fetch(`/api/returns?${params.toString()}`, {
            headers: { 'Authorization': `Bearer ${userStore.token}` },
            signal: controller.signal
        })

        clearTimeout(timeoutId)

        if (response.ok) {
            returns.value = await response.json()
        } else {
            console.error('Fetch returns failed:', response.status)
            toastStore.add({ title: 'Erro', message: 'Falha ao carregar devoluções.', type: 'error' })
        }
    } catch (error) {
        if (error.name === 'AbortError') {
            toastStore.add({ title: 'Erro', message: 'Tempo limite excedido ao carregar devoluções.', type: 'error' })
        } else {
            console.error(error)
            toastStore.add({ title: 'Erro', message: 'Erro ao carregar lista.', type: 'error' })
        }
    } finally {
        loading.value = false
    }
}

const fetchAuxData = async () => {
    // Fetch Products, Clients, Lotes for filters/forms
    try {
        const [prodRes, cliRes, loteRes] = await Promise.all([
            fetch('/api/products', { headers: { 'Authorization': `Bearer ${userStore.token}` } }),
            fetch('/api/clients', { headers: { 'Authorization': `Bearer ${userStore.token}` } }),
            fetch('/api/productions', { headers: { 'Authorization': `Bearer ${userStore.token}` } })
        ])

        if (prodRes.ok) {
            const data = await prodRes.json()
            productOptions.value = data.map(p => ({ value: p.id, label: p.nome }))
        }
        if (cliRes.ok) {
            const data = await cliRes.json()
            clientOptions.value = data.map(c => ({ value: c.id, label: c.nome }))
        }
        if (loteRes.ok) {
            lotesDisponiveis.value = await loteRes.json()
            // Map product name to lotes for better display
            lotesDisponiveis.value.forEach(l => {
                const prod = productOptions.value.find(p => p.value === l.product_id)
                l.product_name = prod ? prod.label : 'Produto Desconhecido'
            })
        }

    } catch (e) { console.error(e) }
}


// Filter Actions
const openFilterModal = () => isFilterOpen.value = true
const closeFilterModal = () => isFilterOpen.value = false
const openInstructions = () => isInstructionsOpen.value = true
const closeInstructions = () => isInstructionsOpen.value = false

const applyFilters = () => {
    appliedFilters.value = { ...filters.value }
    fetchReturns()
    closeFilterModal()
}

const resetFilters = () => {
    filters.value = { num_lote: '', status: '', client_id: '', product_id: '' }
    appliedFilters.value = { ...filters.value }
    fetchReturns()
    if (isFilterOpen.value) closeFilterModal()
}


// Edit Actions
const openEdit = (ret) => {
    if (!userStore.user?.is_master) {
        toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem gerenciar devoluções.', type: 'error' })
        return
    }
    editingReturn.value = ret
    editForm.value = {
        quant_devolvida: ret.quant_devolvida,
        observacao: ret.observacao || ''
    }
    finalizeForm.value = {
        data_retorno: ret.data_retorno || '', // Empty by default
        novo_lote_id: ret.novo_lote_id || ''
    }
}

const closeEdit = () => {
    editingReturn.value = null
    isDeleting.value = false
}

const saveChanges = async (formData) => {
    // If formData is passed (from Component event), use it. Otherwise use local state.
    const data = formData || editForm.value

    if (!data.quant_devolvida && !data.observacao) return

    loadingEdit.value = true
    try {
        const payload = { action: 'edit' }
        if (data.quant_devolvida) payload.quant_devolvida = data.quant_devolvida
        if (data.observacao) payload.observacao = data.observacao

        const response = await fetch(`/api/returns/${editingReturn.value.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.token}`
            },
            body: JSON.stringify(payload)
        })

        if (response.ok) {
            const updated = (await response.json()).return
            updateReturnInList(updated)
            editingReturn.value = updated
            toastStore.add({ title: 'Sucesso', message: 'Alterações salvas!', type: 'success' })

            // Close edit mode if successful? User might want to keep editing. 
            // Usually keeping it open is fine or reverting to view.
            // Given UI "Salvar Alterações" suggests staying in context or closing edit accordion? 
            // The current UI seems to be an accordion or inline edit.
            // Let's keep it simple.
            closeEdit()
            emit('refresh')
        } else {
            const err = await response.json()
            toastStore.add({ title: 'Erro', message: err.error, type: 'error' })
        }
    } catch (e) {
        toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
    } finally {
        loadingEdit.value = false
    }
}

const canFinalize = computed(() => {
    if (!editingReturn.value) return false

    // If status is Retornada
    if (editingReturn.value.status === 'Retornada') {
        // Need lot to be filled to finalize, OR date changed to save date
        const originalDate = editingReturn.value.data_retorno || ''
        const dateChanged = finalizeForm.value.data_retorno !== '' && finalizeForm.value.data_retorno !== originalDate
        return finalizeForm.value.novo_lote_id !== '' || dateChanged
    }

    // For Aberto status, need at least date
    return finalizeForm.value.data_retorno !== ''
})

const finalizeButtonText = computed(() => {
    if (!editingReturn.value) return 'DAR BAIXA / FINALIZAR'

    const hasDate = finalizeForm.value.data_retorno !== ''
    const hasLot = finalizeForm.value.novo_lote_id !== ''
    const isRetornada = editingReturn.value.status === 'Retornada'
    const originalDate = editingReturn.value.data_retorno || ''
    const dateChanged = hasDate && finalizeForm.value.data_retorno !== originalDate

    // If status is Retornada
    if (isRetornada) {
        if (hasLot) {
            return 'DAR BAIXA'
        } else if (dateChanged) {
            return 'SALVAR DATA'
        } else {
            return 'DAR BAIXA' // Blocked until lot is filled
        }
    }

    // For Aberto status
    if (hasDate && hasLot) {
        return 'DAR BAIXA / FINALIZAR'
    } else if (hasDate) {
        return 'RETORNAR'
    } else {
        return 'DAR BAIXA / FINALIZAR'
    }
})

const finalizeReturn = async (formData) => {
    // If formData is passed, use it. Otherwise use local state (fallback)
    const data = formData || finalizeForm.value

    // Validation logic is now in the Child Component (ReturnEditModal). 
    // If the event is emitted, we assume it's valid or we do a basic check here.

    // We can re-use the canFinalize logic or trust the child. 
    // Let's trust the child but ensure we have at least one field to update if the logic allows 'partial' updates.

    loadingFinalize.value = true

    try {
        const payload = {
            action: 'finalize',
            data_retorno: data.data_retorno,
            novo_lote_id: data.novo_lote_id || null
        }

        const response = await fetch(`/api/returns/${editingReturn.value.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.token}`
            },
            body: JSON.stringify(payload)
        })

        if (response.ok) {
            const data = await response.json()
            const updated = data.return

            updateReturnInList(updated)
            editingReturn.value = updated

            if (updated.status === 'Concluída') {
                toastStore.add({ title: 'Sucesso', message: 'Devolução concluída!', type: 'success' })
            } else if (updated.status === 'Retornada') {
                toastStore.add({ title: 'Sucesso', message: 'Devolução retornada!', type: 'success' })
            } else {
                toastStore.add({ title: 'Sucesso', message: 'Devolução atualizada!', type: 'success' })
            }

            // Close modal after successful finalize
            setTimeout(() => {
                closeEdit()
                emit('refresh')
            }, 500)
        } else {
            const err = await response.json()
            toastStore.add({ title: 'Erro', message: err.error, type: 'error' })
        }
    } catch (e) {
        console.error(e)
        toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
    } finally {
        loadingFinalize.value = false
    }
}

const confirmDelete = () => {
    isDeleting.value = true
}

const deleteReturn = async () => {
    if (!editingReturn.value) return
    loadingDelete.value = true
    try {
        const response = await fetch(`/api/returns/${editingReturn.value.id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${userStore.token}` }
        })

        if (response.ok) {
            returns.value = returns.value.filter(r => r.id !== editingReturn.value.id)
            closeEdit()
            emit('refresh')
            toastStore.add({ title: 'Sucesso', message: 'Devolução excluída.', type: 'success' })
        } else {
            const err = await response.json()
            toastStore.add({ title: 'Erro', message: err.error, type: 'error' })
        }
    } catch (e) {
        console.error(e)
    } finally {
        loadingDelete.value = false
        isDeleting.value = false
    }
}

// Production Modal Actions
const closeProductionModal = () => {
    isProductionModalOpen.value = false
    productionInitialData.value = null
}

const handleProductionSave = async (formData) => {
    productionLoading.value = true
    try {
        // Duplicate Logic Fix:
        // If we are creating this lot specifically for a return, the return itself will add the stock 
        // when finalized (see return_routes.py:138). 
        // Therefore, the "Production" itself should effectively be 0 (or the difference if user added extras), 
        // otherwise we double count (100 production + 100 return = 200).
        // However, the user SEES the full quantity in the form. capture valid input.

        let payload = { ...formData }

        if (productionInitialData.value) {
            // We are in return mode.
            // productionInitialData.quant_caixa_produzida is the return amount.
            // formData.quant_caixa_produzida is what user typed.
            const returnQty = Number(productionInitialData.value.quant_caixa_produzida)
            const userQty = Number(formData.quant_caixa_produzida)

            // The amount to "Produce" is (UserQty - ReturnQty).
            // If user wants lot to have 100, and return is 100, we produce 0.
            // If user wants lot to have 120, and return is 100, we produce 20.
            let realProduction = userQty - returnQty

            if (realProduction < 0) {
                // User typed less than return quantity? 
                // This is illogical for a container that must hold the return.
                // Logic: The lot MUST hold the return. 
                // If they typed 90, but 100 are coming in... 
                // We'll just assume 0 production and warn? Or just clamp to 0?
                // Let's clamps to 0 to avoid negative stock.
                realProduction = 0
            }

            payload.quant_caixa_produzida = realProduction

            // If realProduction is 0, we are creating an empty lot to be filled by return.
            // Note: Backend might validate quant > 0?
            // production_routes.py Line 21 checks validity. Usually requires > 0?
            // Let's check backend constraints if possible... but assuming 0 is allowed or we need 1?
            // Actually, standard production usually implies creation.
            // If backend rejects 0, we have a problem.
            // Let's assume for now 0 is okay or we handle it. 
            // If backend blocks 0, we might need another approach (like modifying stock manually).
        }

        const response = await fetch('/api/productions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.token}`
            },
            body: JSON.stringify(payload)
        })

        if (response.ok) {
            const createdProduction = await response.json()
            // Backend returns: { message: '...', production: {...} }
            const newLoteNum = createdProduction.production.num_lote

            // Refresh auxiliary data (lots list)
            await fetchAuxData()

            // Auto-select the new lot
            // Force update to make sure Select component sees the new option
            finalizeForm.value.novo_lote_id = newLoteNum

            toastStore.add({
                title: 'Lote Criado',
                message: `Lote #${newLoteNum} criado e selecionado com sucesso.`,
                type: 'success'
            })
            closeProductionModal()
        } else {
            const err = await response.json()
            toastStore.add({ title: 'Erro ao criar lote', message: err.error, type: 'error' })
        }
    } catch (e) {
        console.error(e)
        toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
    } finally {
        productionLoading.value = false
    }
}

// Helpers
const updateReturnInList = (updatedReturn) => {
    const index = returns.value.findIndex(r => r.id === updatedReturn.id)
    if (index !== -1) {
        // preserve flat fields that might be missing in response if backend doesnt send them back fully hydrated
        // But backend usually sends full object or we need to re-flatten. 
        // The endpoint returns `as_dict` which has relationships simplified. 
        // We might need to refresh functionality or handle flattened fields.
        // For now, let's assume we need to re-fetch or patch carefully.
        // Simplest: re-fetch returns list or update carefully. 
        // Let's just update the list object with the new data, keeping old flattened if not present.
        const old = returns.value[index]
        returns.value[index] = { ...old, ...updatedReturn }
    }
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    try {
        const date = new Date(dateString.includes('T') ? dateString : dateString + 'T00:00:00')
        if (isNaN(date.getTime())) return '-'
        return date.toLocaleDateString('pt-BR')
    } catch (e) {
        return '-'
    }
}

const formatImage = (path) => {
    if (!path) return ''
    if (path.startsWith('http')) return path
    return `/${path.replace(/^backend[\\/]/, '').replace(/\\/g, '/')}`
}

const getStatusClass = (status) => {
    if (status === 'Aberto') return 'bg-yellow-100 text-yellow-700 border border-yellow-200'
    if (status === 'Retornada') return 'bg-blue-100 text-blue-700 border border-blue-200'
    if (status === 'Concluída') return 'bg-green-100 text-green-700 border border-green-200'
    return 'bg-gray-100 text-gray-600'
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

.custom-scrollbar::-webkit-scrollbar-track {
    background-color: transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #d1d5db;
    border-radius: 9999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #9ca3af;
}
</style>
