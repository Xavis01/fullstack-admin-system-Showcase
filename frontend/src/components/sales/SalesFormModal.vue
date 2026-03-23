<template>
    <div>
        <!-- 1. Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[70]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <!-- 2. Container principal -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[80] flex items-center justify-center pt-36 pb-6 px-3 md:px-4 font-montserrat">
            <!-- 3. Overlay escuro -->
            <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>

            <!-- 4. Modal content -->
            <transition name="modal">
                <div v-if="isOpen"
                    class="bg-white rounded-xl shadow-lg z-10 w-full max-h-full overflow-hidden flex flex-col relative"
                    :class="showOrdersPanel ? 'max-w-5xl' : 'max-w-[600px]'">
                    <!-- Header fixo (shrink-0) -->
                    <div
                        class="bg-neutral-700 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl shrink-0">
                        <h3 class="text-lg md:text-xl font-bold">{{ sale?.id ? 'EDITAR VENDA' : 'NOVA VENDA' }}</h3>
                        <!-- Linked order badge -->
                        <span v-if="linkedOrderProductId"
                            class="bg-green-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                            <Link2 class="w-3 h-3" /> VINCULADA
                        </span>
                    </div>

                    <!-- Body com flex-1 overflow-y-auto -->
                    <div class="flex-1 overflow-y-auto">
                        <div class="flex flex-col md:flex-row h-full">
                            <!-- Left Column: Form -->
                            <div class="flex-1 p-4 sm:p-6 md:p-8"
                                :class="showOrdersPanel ? 'md:border-r md:border-gray-200' : ''">
                                <form @submit.prevent="save">
                                    <!-- Lote Select -->
                                    <div class="mb-4 md:mb-6">
                                        <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Lote
                                        </label>
                                        <div class="relative">
                                            <input v-model="formData.num_lote" type="number"
                                                placeholder="Digite ou selecione o lote..."
                                                class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 leading-tight focus:outline-none focus:border-red-500 focus:bg-white transition duration-200"
                                                :class="{ 'opacity-50 cursor-not-allowed': isLoteLocked, 'hover:border-gray-400': !isLoteLocked && !loteDropdownOpen }"
                                                :disabled="isLoteLocked" @focus="loteDropdownOpen = true"
                                                @blur="closeLoteDropdown" autocomplete="off" />

                                            <!-- Dropdown Icon / Loading -->
                                            <div
                                                class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none flex items-center justify-center">
                                                <div v-if="loadingLotes"
                                                    class="w-5 h-5 flex items-center justify-center opacity-50">
                                                    <LoaderCircle class="animate-spin text-gray-600 w-5 h-5" />
                                                </div>
                                                <svg v-else-if="!isLoteLocked"
                                                    class="fill-current h-5 w-5 text-gray-600 transition-transform duration-200"
                                                    :class="{ 'rotate-180': loteDropdownOpen }"
                                                    xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                                    <path
                                                        d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                                                </svg>
                                            </div>

                                            <!-- Custom Rich Dropdown -->
                                            <transition enter-active-class="transition ease-out duration-200"
                                                enter-from-class="opacity-0 translate-y-1"
                                                enter-to-class="opacity-100 translate-y-0"
                                                leave-active-class="transition ease-in duration-150"
                                                leave-from-class="opacity-100 translate-y-0"
                                                leave-to-class="opacity-0 translate-y-1">
                                                <div v-if="loteDropdownOpen && filteredLoteOptions.length > 0"
                                                    class="absolute z-50 w-full mt-1 bg-white border-2 border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
                                                    <div v-for="option in filteredLoteOptions" :key="option.value"
                                                        @mousedown.prevent="selectLote(option)"
                                                        class="px-3 py-2 cursor-pointer transition duration-150 hover:bg-red-50 hover:text-red-600 first:rounded-t-lg last:rounded-b-lg flex items-center gap-2 text-gray-700">
                                                        <img v-if="option.image" :src="option.image"
                                                            class="w-6 h-6 object-cover rounded-full border border-gray-200" />
                                                        <span>{{ option.label }}</span>
                                                    </div>
                                                </div>
                                            </transition>
                                        </div>
                                    </div>

                                    <!-- Client Select -->
                                    <div class="mb-4 md:mb-6">
                                        <label
                                            class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Cliente</label>
                                        <CustomSelect v-model="formData.client_id" :options="clientOptions"
                                            placeholder="Selecione um cliente" :loading="loadingClients"
                                            :disabled="loadingClients || !!linkedOrderProductId" />
                                    </div>

                                    <div class="mb-4 md:mb-6" v-if="selectedLoteProduct">
                                        <label
                                            class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Produto</label>
                                        <div
                                            class="flex items-center gap-3 p-2 bg-gray-100 rounded-lg border border-gray-200">
                                            <img v-if="selectedLoteProduct.image" :src="selectedLoteProduct.image"
                                                class="w-10 h-10 rounded-full object-cover" />
                                            <span class="font-semibold text-gray-700">{{ selectedLoteProduct.name
                                                }}</span>
                                        </div>
                                    </div>

                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-6">
                                        <div>
                                            <div class="flex justify-between items-end mb-2">
                                                <label
                                                    class="block text-gray-700 text-xs md:text-sm font-bold">Quantidade
                                                    Vendida</label>
                                                <span v-if="maxQuantity !== null"
                                                    class="text-xs text-gray-500 font-medium">
                                                    Máx: {{ maxQuantity }}
                                                </span>
                                            </div>
                                            <div class="relative">
                                                <input v-model="formData.quant_caixa_vendida" type="number" min="1"
                                                    :max="maxQuantity"
                                                    class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200" />
                                                <span
                                                    class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 font-semibold">{{
                                                        selectedLoteProduct?.name?.toLowerCase().includes('25kg') ?
                                                    'Sacos' :
                                                    'Caixas' }}</span>
                                            </div>
                                        </div>
                                        <div>
                                            <label
                                                class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Data da
                                                Venda</label>
                                            <CustomCalendar v-model="formData.data_venda"
                                                placeholder="Selecione a data" />
                                        </div>
                                    </div>

                                    <!-- Unlink button if linked -->
                                    <div v-if="linkedOrderProductId && !prefilledData"
                                        class="mb-4 flex items-center gap-2">
                                        <button type="button" @click="unlinkOrder"
                                            class="text-xs text-orange-600 hover:text-orange-700 font-bold flex items-center gap-1 transition">
                                            <X class="w-3 h-3" /> Desvincular expedição
                                        </button>
                                    </div>

                                    <div class="flex justify-center">
                                        <button type="submit"
                                            class="bg-red-600 hover:bg-red-700 active:scale-95 text-white font-bold h-12 px-12 rounded-lg transition duration-200 flex items-center justify-center w-full"
                                            :disabled="loading || isSaving">
                                            <span v-if="!loading && !isSaving">CONFIRMAR</span>
                                            <LoaderCircle v-else class="animate-spin w-5 h-5 md:w-6 md:h-6" />
                                        </button>
                                    </div>
                                </form>
                            </div>

                            <!-- Right Column: Pending Orders (Method B) - only for new sales without prefilled -->
                            <div v-if="showOrdersPanel"
                                class="w-full md:w-[340px] bg-gray-50 p-4 md:p-5 shrink-0 overflow-y-auto border-t md:border-t-0">
                                <h4
                                    class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                                    <Truck class="w-3.5 h-3.5" /> Vincular a uma Expedição
                                </h4>

                                <div v-if="loadingOrders" class="flex justify-center py-8">
                                    <LoaderCircle class="animate-spin text-gray-400 w-6 h-6" />
                                </div>

                                <div v-else-if="pendingOrders.length === 0"
                                    class="text-center py-8 text-gray-400 text-sm">
                                    Nenhuma expedição pendente
                                </div>

                                <div v-else class="space-y-2.5">
                                    <div v-for="order in pendingOrders" :key="order.id"
                                        class="bg-white rounded-lg border border-gray-200 overflow-hidden">
                                        <!-- Order header -->
                                        <div class="px-3 py-2 bg-gray-100 flex items-center justify-between">
                                            <span class="text-xs font-bold text-neutral-700">#{{ order.id }} - {{
                                                order.client_name }}</span>
                                            <span class="text-[10px] text-gray-400 font-semibold">{{
                                                order.quant_caixa_solicitada }} un.</span>
                                        </div>
                                        <!-- Lotes -->
                                        <div class="p-2 space-y-1">
                                            <div v-for="lote in order.lotes" :key="lote.id"
                                                @click="!lote.sold && selectOrderLote(order, lote)"
                                                :class="[
                                                    'flex items-center gap-2 px-2.5 py-2 rounded-md transition text-sm',
                                                    lote.sold
                                                        ? 'bg-green-50 text-green-600 cursor-default'
                                                        : linkedOrderProductId === lote.id
                                                            ? 'bg-red-50 border-2 border-red-400 cursor-pointer'
                                                            : 'hover:bg-red-50 cursor-pointer border border-transparent hover:border-red-200'
                                                ]">
                                                <img v-if="lote.product_image" :src="lote.product_image"
                                                    class="w-5 h-5 rounded-full object-cover border border-gray-200 shrink-0" />
                                                <div v-else
                                                    class="w-5 h-5 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 shrink-0">
                                                    <Package class="w-2.5 h-2.5" />
                                                </div>
                                                <div class="flex-1 min-w-0">
                                                    <p class="text-xs font-semibold text-neutral-700 truncate">
                                                        #{{ lote.num_lote }} - {{ lote.product_name }}
                                                    </p>
                                                    <p class="text-[10px] text-gray-400">Qtd: {{ lote.quantidade }}
                                                    </p>
                                                </div>
                                                <CheckCircle2 v-if="lote.sold"
                                                    class="w-4 h-4 text-green-500 shrink-0" />
                                                <span v-else-if="linkedOrderProductId === lote.id"
                                                    class="text-[9px] font-bold text-red-600 shrink-0 bg-red-100 px-1.5 py-0.5 rounded">SELECIONADO</span>
                                                <span v-else
                                                    class="text-[9px] font-bold text-gray-400 shrink-0">VINCULAR</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { LoaderCircle, Link2, Truck, Package, CheckCircle2, X } from 'lucide-vue-next'
import CustomSelect from '../CustomSelect.vue'
import CustomCalendar from '../CustomCalendar.vue'
import { useUserStore } from '../../stores/user'
import { useToastStore } from '../../stores/toast'

const toastStore = useToastStore()

const props = defineProps({
    isOpen: Boolean,
    sale: Object,
    loading: Boolean,
    prefilledData: Object  // { num_lote, client_id, quant_caixa_vendida, order_product_id }
})

const emit = defineEmits(['close', 'save'])
const userStore = useUserStore()

const formData = ref({
    num_lote: '',
    client_id: '',
    quant_caixa_vendida: '',
    data_venda: new Date().toISOString().split('T')[0]
})

const loteOptions = ref([])
const clientOptions = ref([])
const productions = ref([])
const productsMap = ref({})

const loadingLotes = ref(false)
const loadingClients = ref(false)
const dataLoaded = ref(false)
const isSaving = ref(false)

// Linked order product ID (Método A from prefilled OR Método B from panel selection)
const linkedOrderProductId = ref(null)

// Pending orders for Method B panel
const pendingOrders = ref([])
const loadingOrders = ref(false)

// Show orders panel: always when creating new sale (not edit)
const showOrdersPanel = computed(() => !props.sale?.id)

// Lote is locked when editing an existing sale
const isLoteLocked = computed(() => !!props.sale?.id || loadingLotes.value)

// Custom Searchable Dropdown Logic
const loteDropdownOpen = ref(false)

const filteredLoteOptions = computed(() => {
    if (!formData.value.num_lote) return loteOptions.value
    const search = String(formData.value.num_lote).toLowerCase()
    return loteOptions.value.filter(opt =>
        String(opt.value).toLowerCase().includes(search) ||
        opt.label.toLowerCase().includes(search)
    )
})

const selectLote = (option) => {
    formData.value.num_lote = option.value
    loteDropdownOpen.value = false
}

const closeLoteDropdown = () => {
    loteDropdownOpen.value = false
}

const fetchData = async () => {
    loadingLotes.value = true

    // Always fetch productions to get fresh stock
    const productionsPromise = fetch('/api/productions?available=true', { headers: { 'Authorization': `Bearer ${userStore.token}` } })

    // Fetch clients and products only if not loaded
    const promises = [productionsPromise]
    if (!dataLoaded.value) {
        loadingClients.value = true
        promises.push(fetch('/api/clients', { headers: { 'Authorization': `Bearer ${userStore.token}` } }))
        promises.push(fetch('/api/products', { headers: { 'Authorization': `Bearer ${userStore.token}` } }))
    }

    try {
        const responses = await Promise.all(promises)
        const productionsRes = responses[0]
        const clientsRes = !dataLoaded.value ? responses[1] : null
        const productsRes = !dataLoaded.value ? responses[2] : null

        if (productsRes && productsRes.ok) {
            const data = await productsRes.json()
            data.forEach(p => {
                let imageUrl = null
                if (p.image_path) {
                    imageUrl = p.image_path.startsWith('http') ? p.image_path : `/${p.image_path.replace(/^backend[\\/]/, '').replace(/\\/g, '/')}`
                }
                productsMap.value[p.id] = { name: p.nome, image: imageUrl }
            })
        }

        if (productionsRes.ok) {
            let data = await productionsRes.json()
            productions.value = data

            // If editing and the lote is not available (0 stock), fetch it specifically
            if (props.sale?.num_lote) {
                const exists = data.find(p => p.num_lote === props.sale.num_lote)
                if (!exists) {
                    const specificResp = await fetch(`/api/productions/${props.sale.num_lote}`, {
                        headers: { 'Authorization': `Bearer ${userStore.token}` }
                    })
                    if (specificResp.ok) {
                        const specificProd = await specificResp.json()
                        productions.value.push(specificProd)
                    }
                }
            }

            // If prefilled, also ensure the specific lot is present
            if (props.prefilledData?.num_lote) {
                const exists = data.find(p => p.num_lote === props.prefilledData.num_lote)
                if (!exists) {
                    const specificResp = await fetch(`/api/productions/${props.prefilledData.num_lote}`, {
                        headers: { 'Authorization': `Bearer ${userStore.token}` }
                    })
                    if (specificResp.ok) {
                        const specificProd = await specificResp.json()
                        productions.value.push(specificProd)
                    }
                }
            }

            updateLoteOptions()
        }

        if (clientsRes && clientsRes.ok) {
            const data = await clientsRes.json()
            clientOptions.value = data.map(c => ({ value: c.id, label: c.nome }))
        }

        dataLoaded.value = true
    } catch (e) {
        console.error(e)
    } finally {
        loadingClients.value = false
        loadingLotes.value = false
    }
}

const fetchPendingOrders = async () => {
    loadingOrders.value = true
    try {
        const response = await fetch('/api/orders?achieved=false', {
            headers: { 'Authorization': `Bearer ${userStore.token}` }
        })
        if (response.ok) {
            pendingOrders.value = await response.json()
        }
    } catch (e) {
        console.error(e)
    } finally {
        loadingOrders.value = false
    }
}

const updateLoteOptions = () => {
    loteOptions.value = productions.value.map(p => {
        const prodData = productsMap.value[p.product_id]
        const prodName = prodData?.name || 'Produto'
        return {
            value: p.num_lote,
            label: `#${p.num_lote} - ${prodName} (Estoque: ${p.estoque_lote})`,
            image: prodData?.image
        }
    })
}

// Method B: Select a lot from an order in the right panel
const selectOrderLote = (order, lote) => {
    // If already selected, deselect
    if (linkedOrderProductId.value === lote.id) {
        unlinkOrder()
        return
    }

    linkedOrderProductId.value = lote.id
    formData.value.num_lote = lote.num_lote
    formData.value.client_id = order.client_id
    formData.value.quant_caixa_vendida = lote.quantidade
}

const unlinkOrder = () => {
    linkedOrderProductId.value = null
    // Don't clear form fields — user might want to keep them
}

watch(() => props.isOpen, (isOpen) => {
    if (isOpen) {
        linkedOrderProductId.value = null

        if (props.sale) {
            // Edit mode
            formData.value = {
                num_lote: props.sale.num_lote,
                client_id: props.sale.client_id,
                quant_caixa_vendida: props.sale.quant_caixa_vendida,
                data_venda: props.sale.data_venda
            }
        } else if (props.prefilledData) {
            // Method A: pre-filled from OrderManagerModal
            formData.value = {
                num_lote: props.prefilledData.num_lote,
                client_id: props.prefilledData.client_id,
                quant_caixa_vendida: props.prefilledData.quant_caixa_vendida,
                data_venda: new Date().toISOString().split('T')[0]
            }
            linkedOrderProductId.value = props.prefilledData.order_product_id
        } else {
            // New sale (normal flow)
            formData.value = {
                num_lote: '',
                client_id: '',
                quant_caixa_vendida: '',
                data_venda: new Date().toISOString().split('T')[0]
            }
        }

        // Defer fetch to allow modal animation
        setTimeout(() => {
            fetchData()
            // Always fetch pending orders for new sales
            if (showOrdersPanel.value) {
                fetchPendingOrders()
            }
        }, 350)
    }
})

const selectedLoteProduct = computed(() => {
    if (!formData.value.num_lote) return null
    const prod = productions.value.find(p => p.num_lote === formData.value.num_lote)
    if (!prod) return null
    return productsMap.value[prod.product_id]
})

const maxQuantity = computed(() => {
    if (!formData.value.num_lote) return null
    const prod = productions.value.find(p => p.num_lote === formData.value.num_lote)
    if (!prod) return null

    if (props.sale && props.sale.num_lote === formData.value.num_lote) {
        return prod.estoque_lote + props.sale.quant_caixa_vendida
    }

    return prod.estoque_lote
})

const save = async () => {
    const errors = []

    if (!formData.value.num_lote) errors.push('Lote')
    if (!formData.value.client_id) errors.push('Cliente')

    if (!formData.value.quant_caixa_vendida || Number(formData.value.quant_caixa_vendida) <= 0) {
        errors.push('Quantidade Vendida (maior que 0)')
    } else if (maxQuantity.value !== null && Number(formData.value.quant_caixa_vendida) > maxQuantity.value) {
        errors.push(`Quantidade Indisponível (Max: ${maxQuantity.value})`)
    }

    if (!formData.value.data_venda) errors.push('Data da Venda')

    if (errors.length > 0) {
        toastStore.add({
            title: 'Campos Obrigatórios ou Inválidos',
            message: 'Verifique: ' + errors.join(', '),
            type: 'warning'
        })
        return
    }

    const prod = productions.value.find(p => p.num_lote === formData.value.num_lote)
    if (!prod) {
        toastStore.add({
            title: 'Lote Inválido',
            message: 'O lote informado não existe ou não está disponível.',
            type: 'error'
        })
        return
    }

    const payload = {
        ...formData.value,
        product_id: prod.product_id
    }

    // Include order_product_id if linked
    if (linkedOrderProductId.value) {
        payload.order_product_id = linkedOrderProductId.value
    }

    // If opened from OrderManagerModal (prefilledData), do POST internally
    if (props.prefilledData) {
        isSaving.value = true
        try {
            const response = await fetch('/api/sales', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${userStore.token}`
                },
                body: JSON.stringify(payload)
            })

            if (response.ok) {
                const result = await response.json()
                toastStore.add({
                    title: 'Venda Criada',
                    message: `Venda #${result.sale.id} registrada e vinculada à expedição.`,
                    type: 'success'
                })
                emit('save') // No payload — just signal success
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
            toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
        } finally {
            isSaving.value = false
        }
    } else {
        // Normal flow: emit payload for parent (SaleView) to handle
        emit('save', payload)
    }
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
}
</style>
