<template>
    <div>
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-40"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen"
                class="fixed inset-0 flex items-center justify-center z-50 font-montserrat px-3 md:px-4 pt-36 pb-6">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen" class="bg-white rounded-xl shadow-lg z-10 w-full max-w-[440px] overflow-visible">

                        <!-- Header -->
                        <div
                            class="bg-red-600 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl">
                            <FileText class="w-5 h-5 md:w-6 md:h-6" />
                            <h3 class="text-lg md:text-xl font-bold">GERAR RELATÓRIO</h3>
                        </div>

                        <!-- Body -->
                        <div class="p-4 sm:p-6 space-y-4">

                            <!-- Product Multi-Select -->
                            <div>
                                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Produtos</label>
                                <CustomCheckboxSelect v-model="selectedProducts" :options="productOptions"
                                    placeholder="Selecione" allOptionLabel="Todos" :loading="loadingProducts" />
                            </div>

                            <!-- Month / Year -->
                            <div class="grid grid-cols-2 gap-3 md:gap-4">
                                <div>
                                    <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Mês</label>
                                    <CustomCheckboxSelect v-model="selectedMonths" :options="monthOptions"
                                        placeholder="Selecione" allOptionLabel="Todos" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Ano</label>
                                    <CustomCheckboxSelect v-model="selectedYears" :options="yearOptions"
                                        placeholder="Selecione" allOptionLabel="Todos" :loading="loadingYears" />
                                </div>
                            </div>

                            <!-- Client Multi-Select -->
                            <div>
                                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Clientes</label>
                                <CustomCheckboxSelect v-model="selectedClients" :options="clientOptions"
                                    placeholder="Selecione" allOptionLabel="Todos" :loading="loadingClients" />
                            </div>

                            <!-- Actions -->
                            <div class="flex flex-col gap-3 pt-2">
                                <button @click="generateReport" :disabled="generating"
                                    class="w-full bg-neutral-800 hover:bg-black active:scale-95 text-white font-bold py-3 rounded-lg transition duration-200 flex items-center justify-center gap-2 shadow-lg">
                                    <LoaderCircle v-if="generating" class="w-5 h-5 animate-spin" />
                                    <template v-else>
                                        <FileText class="w-5 h-5" />
                                        GERAR RELATÓRIO
                                    </template>
                                </button>
                                <button @click="$emit('close')"
                                    class="w-full bg-gray-200 hover:bg-gray-300 active:scale-95 text-gray-700 font-bold py-2.5 rounded-lg transition duration-200">
                                    CANCELAR
                                </button>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>

        <!-- Report View Modal (on top) -->
        <ReportViewModal :isOpen="isReportViewOpen" :reportData="reportData" :periodLabel="periodLabel"
            @close="isReportViewOpen = false" />
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { FileText, LoaderCircle } from 'lucide-vue-next'
import CustomCheckboxSelect from '../CustomCheckboxSelect.vue'
import ReportViewModal from './ReportViewModal.vue'
import { useUserStore } from '../../stores/user'
import { useToastStore } from '../../stores/toast'

const props = defineProps({ isOpen: Boolean })
const emit = defineEmits(['close'])

const userStore = useUserStore()
const toastStore = useToastStore()

const selectedProducts = ref([])
const selectedMonths = ref([])
const selectedYears = ref([])
const selectedClients = ref([])
const generating = ref(false)

const productOptions = ref([])
const clientOptions = ref([])
const yearOptions = ref([])
const loadingProducts = ref(false)
const loadingClients = ref(false)
const loadingYears = ref(false)

const isReportViewOpen = ref(false)
const reportData = ref(null)
const periodLabel = ref('')

const monthOptions = [
    { value: 1, label: 'Janeiro' }, { value: 2, label: 'Fevereiro' },
    { value: 3, label: 'Março' }, { value: 4, label: 'Abril' },
    { value: 5, label: 'Maio' }, { value: 6, label: 'Junho' },
    { value: 7, label: 'Julho' }, { value: 8, label: 'Agosto' },
    { value: 9, label: 'Setembro' }, { value: 10, label: 'Outubro' },
    { value: 11, label: 'Novembro' }, { value: 12, label: 'Dezembro' }
]

const fetchProducts = async () => {
    loadingProducts.value = true
    try {
        const res = await fetch('/api/products', { headers: { 'Authorization': `Bearer ${userStore.token}` } })
        if (res.ok) {
            const data = await res.json()
            productOptions.value = data.map(p => {
                let imageUrl = null
                if (p.image_path && p.image_path !== 'null' && p.image_path !== 'None') {
                    imageUrl = p.image_path.startsWith('http') ? p.image_path : `/${p.image_path.replace(/^backend[\\/]/, '').replace(/\\/g, '/')}`
                }
                return { value: p.id, label: p.nome, image: imageUrl }
            })
        }
    } catch (e) { console.error(e) }
    finally { loadingProducts.value = false }
}

const fetchClients = async () => {
    loadingClients.value = true
    try {
        const res = await fetch('/api/clients', { headers: { 'Authorization': `Bearer ${userStore.token}` } })
        if (res.ok) {
            const data = await res.json()
            clientOptions.value = data.map(c => ({ value: c.id, label: c.nome }))
        }
    } catch (e) { console.error(e) }
    finally { loadingClients.value = false }
}

const fetchYears = async () => {
    loadingYears.value = true
    try {
        const res = await fetch('/api/dashboard/available-years', { headers: { 'Authorization': `Bearer ${userStore.token}` } })
        if (res.ok) {
            const years = await res.json()
            yearOptions.value = years.map(y => ({ value: y, label: String(y) }))
        }
    } catch (e) { console.error(e) }
    finally { loadingYears.value = false }
}

watch(() => props.isOpen, (val) => {
    if (val) {
        selectedProducts.value = []
        selectedMonths.value = []
        selectedYears.value = []
        selectedClients.value = []
        setTimeout(() => {
            if (productOptions.value.length === 0) fetchProducts()
            if (clientOptions.value.length === 0) fetchClients()
            if (yearOptions.value.length === 0) fetchYears()
        }, 300)
    }
})

const generateReport = async () => {
    generating.value = true
    try {
        const params = new URLSearchParams()
        if (selectedProducts.value.length > 0 && selectedProducts.value.length < productOptions.value.length) {
            params.append('product_ids', selectedProducts.value.join(','))
        }
        if (selectedClients.value.length > 0 && selectedClients.value.length < clientOptions.value.length) {
            params.append('client_ids', selectedClients.value.join(','))
        }
        if (selectedMonths.value.length > 0 && selectedMonths.value.length < 12) {
            params.append('months', selectedMonths.value.join(','))
        }
        if (selectedYears.value.length > 0 && selectedYears.value.length < yearOptions.value.length) {
            params.append('years', selectedYears.value.join(','))
        }

        const res = await fetch(`/api/report?${params.toString()}`, {
            headers: { 'Authorization': `Bearer ${userStore.token}` }
        })

        if (res.ok) {
            const data = await res.json()
            reportData.value = data

            // Build period label from frontend selections
            const monthNames = { 1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro' }
            const parts = []

            // Months
            if (selectedMonths.value.length === 0 || selectedMonths.value.length === 12) {
                parts.push('Todos os meses')
            } else {
                parts.push(selectedMonths.value.sort((a, b) => a - b).map(m => monthNames[m]).join(', '))
            }

            // Years
            if (selectedYears.value.length === 0 || selectedYears.value.length === yearOptions.value.length) {
                parts.push('Todos os anos')
            } else {
                parts.push(selectedYears.value.sort((a, b) => a - b).join(', '))
            }

            periodLabel.value = parts.join(' · ')
            isReportViewOpen.value = true
        } else {
            toastStore.add({ title: 'Erro', message: 'Falha ao gerar relatório.', type: 'error' })
        }
    } catch (e) {
        console.error(e)
        toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
    } finally {
        generating.value = false
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

.custom-scrollbar::-webkit-scrollbar-track {
    background-color: transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #d1d5db;
    border-radius: 9999px;
}
</style>
