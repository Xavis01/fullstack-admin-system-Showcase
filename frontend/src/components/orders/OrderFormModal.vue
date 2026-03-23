<template>
    <div>
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[70]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen"
                class="fixed inset-0 flex items-start justify-center z-[80] font-montserrat pt-[180px] pb-8 px-3 md:px-4 grayscale-0">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                
                <transition name="modal">
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-2xl z-10 w-full max-w-5xl flex flex-col overflow-hidden max-h-[calc(100vh-220px)]">

                        <!-- Header -->
                        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50 shrink-0">
                            <h3 class="text-lg font-bold text-neutral-800">
                                {{ isEdit ? 'ALTERAR PEDIDO' : 'NOVO PEDIDO' }}
                            </h3>
                            <button @click="$emit('close')"
                                class="text-gray-400 hover:text-neutral-800 transition-colors p-1 rounded-full hover:bg-gray-200">
                                <X class="w-5 h-5" />
                            </button>
                        </div>

                        <!-- Main Content: Grid Layout -->
                        <div class="flex-1 overflow-hidden flex flex-col md:flex-row min-h-0">
                            
                            <!-- Left Column: Form & Selected Items -->
                            <div class="flex-1 flex flex-col border-r border-gray-100 overflow-hidden bg-white">
                                <div class="p-6 space-y-6 overflow-y-auto custom-scrollbar flex-1">
                                    <div class="grid grid-cols-1 gap-6">
                                        <!-- Client Select -->
                                        <div>
                                            <label class="block text-xs font-bold text-gray-700 uppercase mb-2 ml-1 tracking-wide">
                                                CLIENTE *
                                            </label>
                                            <div class="relative z-[70]">
                                                <CustomSelect v-model="formData.client_id" :options="clientOptions"
                                                    placeholder="Selecione ou busque..." searchPlaceholder="Buscar cliente..."
                                                    noOptionsText="Nenhum encontrado" :loading="isLoadingOptions" />
                                            </div>
                                        </div>

                                        <!-- Total Quantity -->
                                        <div>
                                            <label class="block text-xs font-bold text-gray-700 uppercase mb-2 ml-1 tracking-wide">
                                                QUANTIDADE TOTAL SOLICITADA *
                                            </label>
                                            <input type="number" v-model.number="formData.quant_caixa_solicitada" required
                                                min="1"
                                                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-neutral-800 font-semibold focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition shadow-sm placeholder-gray-400"
                                                placeholder="Ex: 50">
                                        </div>

                                        <!-- Observação -->
                                        <div>
                                            <label class="block text-xs font-bold text-gray-700 uppercase mb-2 ml-1 tracking-wide">
                                                OBSERVAÇÃO (OPCIONAL)
                                            </label>
                                            <textarea v-model="formData.observacao" rows="2"
                                                class="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-neutral-800 font-semibold focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 transition shadow-sm placeholder-gray-400 resize-none"
                                                placeholder="Ex: Entregar até sexta-feira, embalar separado..."></textarea>
                                        </div>
                                    </div>

                                    <!-- Selected Lotes Info -->
                                    <div class="space-y-4">
                                        <div class="flex items-center justify-between border-b border-gray-100 pb-2">
                                            <h4 class="text-xs font-bold text-gray-500 uppercase tracking-wider">
                                                Lotes Selecionados ({{ numSelectedLotes }})
                                            </h4>
                                            <span v-if="numSelectedLotes > 0" class="text-[10px] font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded-full">
                                                DISTRIBUIR {{ formData.quant_caixa_solicitada || 0 }} UNIDADES
                                            </span>
                                        </div>

                                        <div v-if="selectedLotesInfo.length === 0" 
                                            class="py-8 border-2 border-dashed border-gray-100 rounded-xl flex flex-col items-center justify-center text-gray-400">
                                            <Package class="w-8 h-8 mb-2 opacity-20" />
                                            <p class="text-sm">Selecione os lotes na lista ao lado</p>
                                        </div>

                                        <div v-else class="space-y-3">
                                            <div v-for="lote in selectedLotesInfo" :key="lote.value"
                                                class="flex items-center gap-3 border rounded-xl px-4 py-3 transition-all"
                                                :class="isLoteSold(lote.value) ? 'bg-green-50/50 border-green-200' : 'bg-gray-50 border-gray-200'">
                                                <img v-if="lote.image" :src="lote.image"
                                                    class="w-8 h-8 rounded-full object-cover border border-gray-200 flex-shrink-0" />
                                                <div v-else
                                                    class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                                                    <Package class="w-4 h-4" />
                                                </div>
                                                
                                                <div class="flex-1 min-w-0">
                                                    <p class="text-sm font-bold text-neutral-800 truncate">{{ lote.productName }}</p>
                                                    <p class="text-[11px] text-gray-500">
                                                        Lote #{{ lote.value }} · 
                                                        <span v-if="isLoteSold(lote.value)" class="font-bold text-green-600">
                                                            Venda #{{ soldLotes[lote.value] }}
                                                        </span>
                                                        <span v-else class="font-bold" :class="lote.disponivel > 0 ? 'text-green-600' : 'text-red-500'">
                                                            {{ lote.disponivel }} disponível
                                                        </span>
                                                    </p>
                                                    <!-- Mini dual progress bar -->
                                                    <div class="mt-1.5 h-1 bg-gray-200 rounded-full overflow-hidden w-24 flex">
                                                        <div v-if="lote.soldPercent > 0" class="h-full bg-red-400 transition-all"
                                                            :style="{ width: Math.min(lote.soldPercent, 100) + '%' }"></div>
                                                        <div v-if="lote.reservedPercent > 0" class="h-full bg-yellow-400 transition-all"
                                                            :style="{ width: Math.min(lote.reservedPercent, 100) + '%' }"></div>
                                                    </div>
                                                </div>

                                                <!-- Quantity Input or Sold Badge -->
                                                <template v-if="isLoteSold(lote.value)">
                                                    <span class="flex items-center gap-1 bg-green-100 text-green-700 text-[10px] font-bold px-2.5 py-1.5 rounded-md shrink-0">
                                                        <CheckCircle2 class="w-3 h-3" />
                                                        {{ selectedLotes[lote.value] }} UN · VENDIDO
                                                    </span>
                                                </template>
                                                <template v-else>
                                                    <div class="flex flex-col items-end gap-1 shrink-0 px-2 border-x border-gray-200">
                                                        <span class="text-[9px] font-black text-gray-400 uppercase">Qtd</span>
                                                        <input type="number" v-model.number="selectedLotes[lote.value]" min="1"
                                                            :max="lote.disponivel"
                                                            class="w-16 px-1.5 py-1 text-sm bg-white border border-gray-300 rounded font-bold text-center text-neutral-800 focus:outline-none focus:ring-2 focus:ring-red-500"
                                                            @input="validateQuantity(lote.value, lote.disponivel)" />
                                                    </div>

                                                    <button type="button" @click="toggleLote(lote.value)"
                                                        class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition shrink-0">
                                                        <X class="w-4 h-4" />
                                                    </button>
                                                </template>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Allocation Alert -->
                                    <div v-if="formData.quant_caixa_solicitada > 0 && numSelectedLotes > 0"
                                        class="p-4 rounded-xl border transition-all"
                                        :class="totalAssignedBoxes === formData.quant_caixa_solicitada ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'">
                                        <div class="flex items-center gap-3">
                                            <div class="p-1.5 rounded-full" :class="totalAssignedBoxes === formData.quant_caixa_solicitada ? 'bg-green-100 text-green-600' : 'bg-yellow-100 text-yellow-600'">
                                                <CheckCircle2 v-if="totalAssignedBoxes === formData.quant_caixa_solicitada" class="w-5 h-5" />
                                                <AlertTriangle v-else class="w-5 h-5" />
                                            </div>
                                            <div class="flex-1">
                                                <span class="text-sm font-bold block" :class="totalAssignedBoxes === formData.quant_caixa_solicitada ? 'text-green-800' : 'text-yellow-800'">
                                                    {{ totalAssignedBoxes }} de {{ formData.quant_caixa_solicitada }} unidades alocadas
                                                </span>
                                                <p v-if="totalAssignedBoxes !== formData.quant_caixa_solicitada" class="text-xs text-yellow-700 mt-0.5 font-medium">
                                                    {{ Math.abs(formData.quant_caixa_solicitada - totalAssignedBoxes) }} 
                                                    {{ totalAssignedBoxes > formData.quant_caixa_solicitada ? 'sobrando' : 'faltando' }}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Footer Actions -->
                                <div class="px-6 py-4 border-t border-gray-100 flex justify-end gap-3 bg-gray-50 shrink-0">
                                    <button type="button" @click="$emit('close')"
                                        class="px-5 py-2.5 text-sm font-bold text-gray-500 hover:bg-gray-200 rounded-lg transition active:scale-95">
                                        CANCELAR
                                    </button>
                                    <button @click="saveOrder"
                                        :disabled="isSaving || totalAssignedBoxes !== formData.quant_caixa_solicitada"
                                        class="px-8 py-2.5 text-sm font-bold text-white bg-red-600 hover:bg-red-700 rounded-lg transition shadow-lg active:scale-95 flex items-center justify-center min-w-[140px]"
                                        :class="(isSaving || totalAssignedBoxes !== formData.quant_caixa_solicitada) ? 'opacity-50 cursor-not-allowed' : ''">
                                        <LoaderCircle v-if="isSaving" class="w-5 h-5 animate-spin mr-2" />
                                        <span v-else>SALVAR PEDIDO</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Right Column: Lote Selection List -->
                            <div class="w-full md:w-[360px] flex flex-col bg-gray-50/50">
                                <!-- Search Header -->
                                <div class="p-4 border-b border-gray-100 bg-white shadow-sm shrink-0">
                                    <h4 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3 px-1">BUSCAR LOTES</h4>
                                    <div class="relative">
                                        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                                        <input v-model="searchQuery" type="text" placeholder="Número do lote ou produto..."
                                            class="w-full bg-gray-50 text-gray-700 border border-gray-200 rounded-xl h-[42px] pl-10 pr-4 text-sm focus:outline-none focus:border-red-400 focus:bg-white focus:ring-4 focus:ring-red-50/50 transition"
                                            autocomplete="off" />
                                    </div>
                                </div>

                                <!-- Lote List -->
                                <div class="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
                                    <div v-if="filteredLoteOptions.length === 0"
                                        class="px-4 py-8 text-sm text-gray-400 text-center flex flex-col items-center opacity-40">
                                        <SearchX class="w-8 h-8 mb-2" />
                                        Nenhum lote disponível
                                    </div>

                                    <div v-for="option in sortedFilteredLoteOptions" :key="option.value"
                                        @click="!option.depleted && toggleLote(option.value)"
                                        class="p-3 rounded-xl transition duration-200 flex items-center gap-3 group relative overflow-hidden"
                                        :class="[
                                            option.depleted ? 'opacity-50 cursor-not-allowed grayscale' : 'cursor-pointer hover:bg-white hover:shadow-md border border-transparent hover:border-gray-100',
                                            isSelected(option.value) && !option.depleted ? 'bg-white border-red-200 shadow-sm ring-1 ring-red-100' : ''
                                        ]">
                                        <!-- Selection Indicator (Left Border) -->
                                        <div v-if="isSelected(option.value) && !option.depleted" 
                                            class="absolute left-0 top-0 bottom-0 w-1 bg-red-600"></div>

                                        <!-- Checkbox -->
                                        <div class="w-[20px] h-[20px] rounded-lg border-2 flex items-center justify-center flex-shrink-0 transition-all duration-300"
                                            :class="option.depleted ? 'border-gray-300 bg-gray-100' : isSelected(option.value) ? 'bg-red-600 border-red-600 scale-105' : 'border-gray-300 group-hover:border-red-400'">
                                            <Check v-if="isSelected(option.value) && !option.depleted" class="w-3.5 h-3.5 text-white" stroke-width="4" />
                                            <X v-if="option.depleted" class="w-3 h-3 text-gray-300" />
                                        </div>

                                        <!-- Product Image -->
                                        <div class="relative flex-shrink-0">
                                            <img v-if="option.image" :src="option.image"
                                                class="w-10 h-10 object-cover rounded-xl border border-gray-100" />
                                            <div v-else
                                                class="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center text-gray-400 border border-gray-100">
                                                <Package class="w-5 h-5" />
                                            </div>
                                        </div>

                                        <!-- Info -->
                                        <div class="flex-1 min-w-0">
                                            <p class="text-[13px] font-bold truncate transition-colors"
                                                :class="isSelected(option.value) ? 'text-red-700' : 'text-neutral-700'">
                                                #{{ option.value }} - {{ option.productName }}
                                            </p>
                                            
                                            <!-- Stats & Bar -->
                                            <div class="mt-1 flex flex-col gap-1.5">
                                                <div class="flex items-center justify-between text-[10px]">
                                                    <span class="font-black" :class="option.depleted ? 'text-red-400' : 'text-green-600'">
                                                        {{ option.depleted ? 'ESGOTADO' : option.disponivel + ' DISPONÍVEIS' }}
                                                    </span>
                                                    <span class="text-gray-400 font-bold uppercase tracking-tighter">Total: {{ option.totalProduzido }}</span>
                                                </div>
                                                <!-- Dual progress bar: red=sold, green/yellow=reserved pending -->
                                                <div class="h-1.5 bg-gray-200 rounded-full overflow-hidden flex">
                                                    <div v-if="option.soldPercent > 0"
                                                        class="h-full bg-red-400 transition-all duration-500"
                                                        :style="{ width: Math.min(option.soldPercent, 100) + '%' }"></div>
                                                    <div v-if="option.reservedPercent > 0"
                                                        class="h-full bg-yellow-400 transition-all duration-500"
                                                        :style="{ width: Math.min(option.reservedPercent, 100) + '%' }"></div>
                                                </div>
                                                <!-- Descriptive text -->
                                                <div class="flex items-center gap-2 text-[9px] font-bold -mt-0.5 flex-wrap">
                                                    <span v-if="option.sold > 0" class="text-red-400 flex items-center gap-0.5">
                                                        <span class="w-1.5 h-1.5 rounded-full bg-red-400 inline-block"></span>
                                                        {{ option.sold }} VENDIDO
                                                    </span>
                                                    <span v-if="option.reserved > 0" class="text-yellow-500 flex items-center gap-0.5">
                                                        <span class="w-1.5 h-1.5 rounded-full bg-yellow-400 inline-block"></span>
                                                        {{ option.reserved }} RESERVADO
                                                    </span>
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
import { ref, watch, computed, nextTick, onMounted } from 'vue'
import { X, Package, CheckCircle2, AlertTriangle, LoaderCircle, Search, Check, SearchX } from 'lucide-vue-next'
import CustomSelect from '../CustomSelect.vue'
import { useUserStore } from '../../stores/user'
import { useToastStore } from '../../stores/toast'

const props = defineProps({
    isOpen: Boolean,
    order: Object, // Pedido para edição
    isEdit: Boolean
})

const emit = defineEmits(['close', 'saved'])
const userStore = useUserStore()
const toastStore = useToastStore()

const isSaving = ref(false)
const isLoadingOptions = ref(false)
const loadingLotes = ref(false)
const searchQuery = ref('')

const formData = ref({
    client_id: '',
    quant_caixa_solicitada: '',
    observacao: '',
})

// Lotes selecionados: { num_lote: quantidade }
const selectedLotes = ref({})
// Lotes vendidos (não podem ser removidos/editados): { num_lote: sale_id }
const soldLotes = ref({})

const loteOptions = ref([])
const clientOptions = ref([])
const productions = ref([])
const productsMap = ref({})

const isSelected = (numLote) => selectedLotes.value.hasOwnProperty(numLote)
const isLoteSold = (numLote) => soldLotes.value.hasOwnProperty(numLote)

const toggleLote = (numLote) => {
    if (isLoteSold(numLote)) {
        toastStore.add({ title: 'Ação Bloqueada', message: 'Este lote já possui uma venda vinculada e não pode ser removido.', type: 'warning' })
        return
    }
    if (isSelected(numLote)) {
        delete selectedLotes.value[numLote]
    } else {
        selectedLotes.value[numLote] = ''
    }
}

const validateQuantity = (numLote, max) => {
    if (selectedLotes.value[numLote] > max) {
        selectedLotes.value[numLote] = max
        const unit = productsMap.value[productions.value.find(p => p.num_lote === numLote)?.product_id]?.name?.toLowerCase().includes('25kg') ? 'sacos' : 'caixas';
        toastStore.add({ title: 'Atenção', message: `O lote #${numLote} só possui ${max} ${unit} em estoque.`, type: 'warning' });
    }
    if (selectedLotes.value[numLote] < 0) {
        selectedLotes.value[numLote] = 0
    }
}

const selectedLotesInfo = computed(() => {
    return loteOptions.value.filter(opt => isSelected(opt.value))
})

const filteredLoteOptions = computed(() => {
    const search = (searchQuery.value || '').toLowerCase()
    if (!search) return loteOptions.value
    return loteOptions.value.filter(opt =>
        String(opt.value).toLowerCase().includes(search) ||
        opt.productName.toLowerCase().includes(search)
    )
})

// Sorted: available first, then by production date (oldest first)
const sortedFilteredLoteOptions = computed(() => {
    return [...filteredLoteOptions.value].sort((a, b) => {
        if (a.depleted && !b.depleted) return 1
        if (!a.depleted && b.depleted) return -1
        
        // Para lotes com o mesmo status de disponibilidade, ordena pelo mais antigo
        return new Date(a.dataProducao) - new Date(b.dataProducao)
    })
})

const numSelectedLotes = computed(() => Object.keys(selectedLotes.value).length)

const totalAssignedBoxes = computed(() => {
    return Object.values(selectedLotes.value).reduce((acc, curr) => acc + (Number(curr) || 0), 0)
})

watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        resetForm()
        fetchData()
    }
})

const resetForm = () => {
    soldLotes.value = {}
    if (props.isEdit && props.order) {
        formData.value = {
            client_id: props.order.client_id,
            quant_caixa_solicitada: props.order.quant_caixa_solicitada,
            observacao: props.order.observacao || '',
        }
        // Map current order lots & track sold ones
        const lotsMap = {}
        props.order.lotes.forEach(l => {
            lotsMap[l.num_lote] = l.quantidade
            if (l.sold) {
                soldLotes.value[l.num_lote] = l.sale_id
            }
        })
        selectedLotes.value = lotsMap
    } else {
        formData.value = {
            client_id: '',
            quant_caixa_solicitada: '',
            observacao: '',
        }
        selectedLotes.value = {}
    }
    searchQuery.value = ''
}

// Fetch helpers
const fetchData = async () => {
    isLoadingOptions.value = true
    loadingLotes.value = true
    try {
        const headers = { 'Authorization': `Bearer ${userStore.token}` }
        // Pass exclude_order_id when editing to not count own reservation
        let productionsUrl = '/api/productions?available=true'
        if (props.order?.id) {
            productionsUrl += `&exclude_order_id=${props.order.id}`
        }
        const [clientsRes, productionsRes, productsRes] = await Promise.all([
            fetch('/api/clients', { headers }),
            fetch(productionsUrl, { headers }),
            fetch('/api/products', { headers })
        ])

        if (clientsRes.ok) {
            const docs = await clientsRes.json()
            clientOptions.value = docs.map(c => ({ value: c.id, label: c.nome }))
        }

        if (productsRes.ok) {
            const docs = await productsRes.json()
            productsMap.value = {}
            docs.forEach(p => {
                let imageUrl = null
                if (p.image_path && p.image_path !== 'null' && p.image_path !== 'None') {
                    imageUrl = p.image_path.startsWith('http') ? p.image_path : `/${p.image_path.replace(/^backend[\\/]/, '').replace(/\\/g, '/')}`
                }
                productsMap.value[p.id] = { name: p.nome, image: imageUrl }
            })
        }

        if (productionsRes.ok) {
            const data = await productionsRes.json()
            productions.value = data
            updateLoteOptions()
        }
    } catch (e) {
        console.error('Error fetching data:', e)
    } finally {
        isLoadingOptions.value = false
        loadingLotes.value = false
    }
}

const updateLoteOptions = () => {
    loteOptions.value = productions.value.map(p => {
        const prodData = productsMap.value[p.product_id]
        const prodName = prodData?.name || 'Produto'
        const totalProduzido = p.quant_caixa_produzida
        const reserved = p.reserved_in_orders || 0
        const sold = p.sold_quantity || 0

        // Disponível = estoque atual - reservas pendentes
        // estoque_lote já desconta vendas, reserved conta pedidos pendentes (achieved=False)
        // Vendas e pedidos são INDEPENDENTES — não se anulam automaticamente
        const disponivel = Math.max(0, p.estoque_lote - reserved)

        // Percentuais para a barra de progresso (baseados no total produzido)
        const soldPercent = totalProduzido > 0 ? (sold / totalProduzido) * 100 : 0
        const reservedPercent = totalProduzido > 0 ? (reserved / totalProduzido) * 100 : 0

        return {
            value: p.num_lote,
            dataProducao: p.data_producao,
            label: `#${p.num_lote} - ${prodName} (Estoque: ${p.estoque_lote})`,
            image: prodData?.image,
            productName: prodName,
            totalProduzido: totalProduzido,
            estoque: p.estoque_lote,
            sold: sold,
            reserved: reserved,
            disponivel: disponivel,
            soldPercent: soldPercent,
            reservedPercent: reservedPercent,
            depleted: disponivel <= 0
        }
    })
}

const saveOrder = async () => {
    if (!formData.value.client_id || !formData.value.quant_caixa_solicitada || numSelectedLotes.value === 0) {
        toastStore.add({ title: 'Atenção', message: 'Preencha os campos obrigatórios e selecione ao menos um lote.', type: 'warning' })
        return
    }

    if (totalAssignedBoxes.value !== formData.value.quant_caixa_solicitada) {
        toastStore.add({ title: 'Atenção', message: 'A soma das quantidades dos lotes deve ser igual ao total solicitado.', type: 'warning' })
        return
    }

    // Validar que todos os lotes não-vendidos possuem quantidade > 0
    const lotesWithoutQty = Object.entries(selectedLotes.value)
        .filter(([numLote, qty]) => !isLoteSold(numLote) && (!qty || Number(qty) <= 0))
    if (lotesWithoutQty.length > 0) {
        toastStore.add({ title: 'Atenção', message: 'Todos os lotes devem ter uma quantidade definida.', type: 'warning' })
        return
    }

    isSaving.value = true
    try {
        const url = props.isEdit ? `/api/orders/${props.order.id}` : '/api/orders'
        const method = props.isEdit ? 'PUT' : 'POST'

        // Format lotes for backend: [{ num_lote, quantidade }]
        const lotesPayload = Object.entries(selectedLotes.value).map(([num_lote, quantidade]) => ({
            num_lote,
            quantidade
        }))

        const payload = {
            ...formData.value,
            lotes: lotesPayload
        }

        const res = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.token}`
            },
            body: JSON.stringify(payload)
        })

        if (res.ok) {
            toastStore.add({ title: 'Sucesso', message: props.isEdit ? 'Pedido atualizado!' : 'Pedido criado com sucesso!', type: 'success' })
            emit('saved')
            emit('close')
        } else {
            const err = await res.json()
            toastStore.add({ title: 'Erro', message: err.error || 'Erro ao salvar pedido.', type: 'danger' })
        }
    } catch (e) {
        console.error(e)
        toastStore.add({ title: 'Erro', message: 'Erro ao conectar com o servidor.', type: 'danger' })
    } finally {
        isSaving.value = false
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

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #e2e8f0;
    border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #cbd5e1;
}
</style>
