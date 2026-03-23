<template>
    <div>
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[60]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen"
                class="fixed inset-0 flex items-center justify-center z-[60] font-montserrat px-3 md:px-4 pt-36 pb-6">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-2xl z-10 w-full max-w-6xl flex flex-col overflow-hidden max-h-full">

                        <!-- Header -->
                        <div
                            class="bg-neutral-800 text-white px-4 md:px-6 py-4 flex items-center justify-between shrink-0 rounded-t-xl">
                            <div class="flex items-center gap-3">
                                <div class="bg-red-600 p-2 rounded-lg">
                                    <BarChart2 class="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 class="text-base md:text-lg font-bold">ESTATÍSTICAS DE LOTES</h3>
                                    <p class="text-white/60 text-xs font-medium">Previsão e fluxo de vendas</p>
                                </div>
                            </div>
                            <button @click="$emit('close')"
                                class="text-white/50 hover:text-white transition p-1 rounded-full hover:bg-white/10">
                                <X class="w-5 h-5" />
                            </button>
                        </div>

                        <!-- Search and Filter Bar -->
                        <div
                            class="bg-gray-50 border-b border-gray-200 px-4 md:px-6 py-3 flex flex-col sm:flex-row gap-3 items-center justify-between shrink-0">
                            <div class="relative w-full sm:w-72">
                                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Search class="w-4 h-4 text-gray-400" />
                                </div>
                                <input v-model="searchQuery" type="text" placeholder="Buscar por lote..."
                                    class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-red-500 focus:border-red-500 transition shadow-sm" />
                            </div>
                            <div class="flex items-center gap-2 w-full sm:w-auto">
                                <!-- Info Button -->
                                <button @click="$emit('open-info')" title="Entenda as métricas"
                                    class="flex-shrink-0 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 transition rounded-lg">
                                    <Info class="w-5 h-5" />
                                </button>

                                <!-- Custom Select -->
                                <div class="w-full sm:w-48">
                                    <CustomSelect v-model="statusFilter" :options="statusOptions" />
                                </div>
                            </div>
                        </div>

                        <!-- Data Table (Desktop) & Cards (Mobile) -->
                        <div class="flex-1 overflow-y-auto bg-gray-100 p-4 md:p-6 custom-scrollbar">
                            <div v-if="filteredProductions.length === 0"
                                class="flex flex-col items-center justify-center py-16 text-gray-500">
                                <PackageOpen class="w-12 h-12 text-gray-400 mb-2" />
                                <p class="text-lg font-semibold text-gray-600">Nenhum lote encontrado</p>
                            </div>

                            <div v-else class="space-y-4">
                                <!-- Desktop Table -->
                                <div
                                    class="hidden lg:block bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                                    <table class="w-full text-left text-sm">
                                        <thead
                                            class="bg-neutral-100 text-neutral-600 border-b border-gray-200 text-xs uppercase font-bold tracking-wider">
                                            <tr>
                                                <th class="px-5 py-4 w-1/4">Produto & Lote</th>
                                                <th class="px-5 py-4">Data Prod.</th>
                                                <th class="px-5 py-4">Tempo Parado</th>
                                                <th class="px-5 py-4">Status de Vendas</th>
                                                <th class="px-5 py-4 text-center">Desempenho</th>
                                            </tr>
                                        </thead>
                                        <tbody class="divide-y divide-gray-100">
                                            <tr v-for="item in filteredProductions" :key="item.num_lote"
                                                class="hover:bg-blue-50/30 transition">
                                                <td class="px-5 py-4">
                                                    <div class="flex items-center gap-3">
                                                        <div
                                                            class="w-10 h-10 rounded-full bg-gray-100 border border-gray-200 overflow-hidden flex-shrink-0 flex items-center justify-center">
                                                            <img v-if="item.product_image" :src="item.product_image"
                                                                class="w-full h-full object-cover" />
                                                            <Package v-else class="w-5 h-5 text-gray-400" />
                                                        </div>
                                                        <div>
                                                            <div class="font-extrabold text-neutral-800">#{{
                                                                item.num_lote }}</div>
                                                            <div
                                                                class="text-xs text-neutral-500 font-semibold truncate max-w-[150px]">
                                                                {{ item.product_name }}</div>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td class="px-5 py-4 font-semibold text-neutral-700">
                                                    {{ formatDate(item.data_producao) }}
                                                </td>
                                                <td class="px-5 py-4">
                                                    <div class="flex flex-col">
                                                        <span :class="getStoppedDaysCssLine1(item)">{{
                                                            getStoppedDaysString(item) }}</span>
                                                        <span class="text-xs text-gray-500 font-semibold">{{
                                                            getStoppedUntilDate(item) }}</span>
                                                    </div>
                                                </td>
                                                <td class="px-5 py-4">
                                                    <div class="flex flex-col gap-1">
                                                        <div class="flex items-center justify-between text-xs">
                                                            <span class="font-bold text-gray-500">1ª: <span
                                                                    class="text-gray-800">{{
                                                                        formatDate(item.first_sale_date) || '--/--/----'
                                                                    }}</span></span>
                                                        </div>
                                                        <div class="flex items-center justify-between text-xs">
                                                            <span class="font-bold text-gray-500">Última: <span
                                                                    class="text-gray-800">{{
                                                                        formatDate(item.last_sale_date) || '--/--/----'
                                                                    }}</span></span>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td class="px-5 py-4 text-center">
                                                    <div v-if="item.estoque_lote === 0"
                                                        class="inline-flex flex-col items-center justify-center bg-green-50 text-green-700 border border-green-200 px-3 py-1.5 rounded-lg w-full">
                                                        <span
                                                            class="text-[10px] uppercase font-bold tracking-wider leading-none mb-1">Esgotado
                                                            em</span>
                                                        <span class="font-extrabold text-sm leading-none">{{
                                                            getSaleDuration(item) }}</span>
                                                    </div>
                                                    <div v-else
                                                        class="inline-flex flex-col items-center justify-center bg-amber-50 text-amber-700 border border-amber-200 px-3 py-1.5 rounded-lg w-full">
                                                        <span
                                                            class="text-[10px] uppercase font-bold tracking-wider leading-none mb-1">Em
                                                            Estoque</span>
                                                        <span class="font-extrabold text-sm leading-none">{{
                                                            item.estoque_lote }} {{
                                                                item.product_name?.toLowerCase().includes('25kg') ? 'sc' :
                                                                    'cx' }}</span>
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <!-- Mobile Cards -->
                                <div class="block lg:hidden space-y-3">
                                    <div v-for="item in filteredProductions" :key="item.num_lote"
                                        class="bg-white border border-gray-200 rounded-xl p-4 shadow-sm relative">
                                        <!-- Header -->
                                        <div class="flex items-center gap-3 mb-3 pb-3 border-b border-gray-100">
                                            <div
                                                class="w-12 h-12 rounded-full bg-gray-100 border border-gray-200 overflow-hidden flex-shrink-0 flex items-center justify-center">
                                                <img v-if="item.product_image" :src="item.product_image"
                                                    class="w-full h-full object-cover" />
                                                <Package v-else class="w-6 h-6 text-gray-400" />
                                            </div>
                                            <div class="flex-1">
                                                <div class="flex justify-between items-start">
                                                    <div class="font-extrabold text-neutral-800 text-lg leading-tight">
                                                        #{{ item.num_lote }}</div>
                                                    <span v-if="item.estoque_lote === 0"
                                                        class="bg-green-100 text-green-700 text-[10px] uppercase font-bold px-2 py-0.5 rounded-full">Esgotado</span>
                                                    <span v-else
                                                        class="bg-amber-100 text-amber-700 text-[10px] uppercase font-bold px-2 py-0.5 rounded-full">{{
                                                            item.estoque_lote }} {{
                                                            item.product_name?.toLowerCase().includes('25kg') ? 'sc' : 'cx'
                                                        }}</span>
                                                </div>
                                                <div class="text-xs text-neutral-500 font-semibold">{{ item.product_name
                                                    }}</div>
                                            </div>
                                        </div>

                                        <!-- Stats Grid -->
                                        <div class="grid grid-cols-2 gap-3 text-sm">
                                            <div>
                                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide">
                                                    Produzido Em</p>
                                                <p class="font-semibold text-gray-800">{{ formatDate(item.data_producao)
                                                    }}</p>
                                            </div>
                                            <div>
                                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide">
                                                    Tempo Parado</p>
                                                <p :class="getStoppedDaysCssLine1(item, true)">{{
                                                    getStoppedDaysString(item) }}</p>
                                                <p class="text-[10px] text-gray-400 leading-tight">Até {{
                                                    getStoppedUntilDate(item) }}</p>
                                            </div>
                                            <div>
                                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide">
                                                    1ª e Última Venda</p>
                                                <p class="font-semibold text-gray-800 leading-tight">{{
                                                    formatDate(item.first_sale_date) || '--/--/----' }}</p>
                                                <p class="font-semibold text-gray-600 leading-tight text-xs mt-0.5">{{
                                                    formatDate(item.last_sale_date) || '--/--/----' }}</p>
                                            </div>
                                            <div v-if="item.estoque_lote === 0">
                                                <p class="text-[10px] text-green-600 font-bold uppercase tracking-wide">
                                                    Tempo p/ Esgotar</p>
                                                <p class="font-extrabold text-green-700">{{ getSaleDuration(item) }}</p>
                                            </div>
                                            <div v-else>
                                                <p class="text-[10px] text-amber-600 font-bold uppercase tracking-wide">
                                                    Status</p>
                                                <p class="font-extrabold text-amber-700">Ainda vendendo</p>
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
import { ref, computed } from 'vue'
import { X, BarChart2, Package, Search, PackageOpen, Info } from 'lucide-vue-next'
import CustomSelect from '../CustomSelect.vue'

const props = defineProps({
    isOpen: Boolean,
    productions: {
        type: Array,
        default: () => []
    }
})

defineEmits(['close', 'open-info'])

const searchQuery = ref('')
const statusFilter = ref('ALL')

const statusOptions = [
    { value: 'ALL', label: 'Todos os Lotes' },
    { value: 'SOLD_OUT', label: 'Esgotados' },
    { value: 'ACTIVE', label: 'Em Estoque' }
]

// Sort and filter productions
const filteredProductions = computed(() => {
    let sorted = [...props.productions].sort((a, b) => {
        // Sort explicitly by data_producao desc
        return new Date(b.data_producao) - new Date(a.data_producao)
    })

    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        sorted = sorted.filter(p =>
            p.num_lote.toString().toLowerCase().includes(query) ||
            p.product_name.toLowerCase().includes(query)
        )
    }

    if (statusFilter.value === 'SOLD_OUT') {
        sorted = sorted.filter(p => Number(p.estoque_lote) === 0)
    } else if (statusFilter.value === 'ACTIVE') {
        sorted = sorted.filter(p => Number(p.estoque_lote) > 0)
    }

    return sorted
})

// Format helpers
const formatDate = (dateString) => {
    if (!dateString) return ''
    if (dateString.length === 10) {
        const cleanDate = dateString.replace(' ', 'T')
        const [year, month, day] = cleanDate.split('T')[0].split('-').map(Number)
        return new Date(year, month - 1, day).toLocaleDateString('pt-BR')
    }
    const utcDateString = dateString.replace(' ', 'T') + (dateString.includes('Z') ? '' : 'Z')
    return new Date(utcDateString).toLocaleDateString('pt-BR')
}

// Logic for "Tempo Parado"
const getStoppedDays = (item) => {
    const start = new Date(item.data_producao.replace(' ', 'T').substring(0, 10) + 'T00:00:00')
    const endStr = item.first_sale_date ? item.first_sale_date : new Date().toISOString()
    const end = new Date(endStr.replace(' ', 'T').substring(0, 10) + 'T00:00:00')

    const diffMs = end - start
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
    return diffDays >= 0 ? diffDays : 0
}

const getStoppedDaysString = (item) => {
    const days = getStoppedDays(item)
    if (days === 0) return 'Vendido no mesmo dia'
    if (days === 1) return '1 dia parado'
    return `${days} dias parados`
}

const getStoppedDaysCssLine1 = (item, isMobile = false) => {
    const days = getStoppedDays(item)
    const base = isMobile ? 'font-semibold text-gray-800' : 'font-extrabold text-gray-800'
    if (days === 0) return `${base} text-green-600`
    if (days < 5) return `${base} text-blue-600`
    if (days < 15) return `${base} text-amber-600`
    return `${base} text-red-600`
}

const getStoppedUntilDate = (item) => {
    if (item.first_sale_date) {
        return `Até primeira venda (${formatDate(item.first_sale_date)})`
    }
    return `Até hoje (Sem vendas)`
}

// Logic for "Tempo p/ Esgotar" (Only if sold out, duration between first and last sale)
// Wait, the prompt says "quanto tempo demorou pra vender todo o lote"
const getSaleDuration = (item) => {
    if (item.estoque_lote > 0) return '--'
    if (!item.first_sale_date || !item.last_sale_date) return 'N/A'

    const start = new Date(item.first_sale_date.replace(' ', 'T').substring(0, 10) + 'T00:00:00')
    const end = new Date(item.last_sale_date.replace(' ', 'T').substring(0, 10) + 'T00:00:00')
    const diffMs = end - start
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return 'No mesmo dia'
    if (diffDays === 1) return '1 dia'
    return `${diffDays} dias`
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
    background-color: #cbd5e1;
    border-radius: 9999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #94a3b8;
}
</style>
