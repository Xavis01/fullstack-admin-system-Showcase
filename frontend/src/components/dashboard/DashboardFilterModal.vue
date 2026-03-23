<template>
    <div>
        <!-- Blur Layer with synchronized transition -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-40"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 font-montserrat p-4 md:pt-20">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen" class="bg-white rounded-xl shadow-lg z-10 w-full max-w-[400px]">
                        <!-- Header -->
                        <div
                            class="bg-red-600 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl">
                            <Filter class="w-5 h-5 md:w-6 md:h-6" />
                            <h3 class="text-lg md:text-xl font-bold">FILTRAR DASHBOARD</h3>
                        </div>

                        <!-- Body -->
                        <div class="p-4 sm:p-6">
                            <!-- Specific Date Checkbox -->
                            <div class="mb-4 flex items-center cursor-pointer"
                                @click="filters.use_specific_dates = !filters.use_specific_dates">
                                <div class="w-5 h-5 border-2 border-gray-300 rounded flex items-center justify-center transition-colors duration-200"
                                    :class="{ 'bg-red-600 border-red-600': filters.use_specific_dates, 'bg-white': !filters.use_specific_dates }">
                                    <Check v-if="filters.use_specific_dates" class="w-3.5 h-3.5 text-white"
                                        stroke-width="3" />
                                </div>
                                <label
                                    class="ml-2 text-xs md:text-sm font-bold text-gray-700 cursor-pointer select-none">Data
                                    específica</label>
                            </div>

                            <!-- Specific Date Range (when checkbox is checked) -->
                            <div v-if="filters.use_specific_dates"
                                class="mb-4 grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                                <div>
                                    <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Data
                                        Início</label>
                                    <CustomCalendar v-model="filters.start_date" placeholder="Início" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Data
                                        Fim</label>
                                    <CustomCalendar v-model="filters.end_date" placeholder="Fim" />
                                </div>
                            </div>

                            <!-- Month/Year Selection (when checkbox is unchecked) -->
                            <div v-else class="mb-4 grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                                <div>
                                    <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Mês</label>
                                    <CustomCheckboxSelect v-model="filters.selected_months" :options="monthOptions"
                                        placeholder="Selecione" allOptionLabel="Todos" />
                                </div>
                                <div>
                                    <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Ano</label>
                                    <CustomCheckboxSelect v-model="filters.selected_years" :options="yearOptions"
                                        placeholder="Selecione" allOptionLabel="Todos" :loading="loadingYears" />
                                </div>
                            </div>
                            <!-- Client Selector -->
                            <div class="mb-4">
                                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Cliente</label>
                                <CustomSelect v-model="filters.client_id" :options="clientOptions"
                                    placeholder="Todos os clientes" :loading="loadingClients" />
                            </div>

                            <!-- Product Selector -->
                            <div class="mb-6">
                                <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Produto</label>
                                <CustomSelect v-model="filters.product_id" :options="productOptions"
                                    placeholder="Todos os produtos" :loading="loadingProducts" />
                            </div>

                            <div class="flex flex-col sm:flex-row justify-center gap-3 md:gap-4">
                                <button @click="apply"
                                    class="bg-neutral-700 hover:bg-neutral-800 active:scale-95 text-white font-bold py-2 px-6 rounded-lg transition duration-200 w-full">
                                    APLICAR
                                </button>
                                <button @click="clear"
                                    class="bg-gray-300 hover:bg-gray-400 active:scale-95 text-gray-800 font-bold py-2 px-6 rounded-lg transition duration-200 w-full">
                                    LIMPAR
                                </button>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Filter, Check } from 'lucide-vue-next';
import CustomSelect from '../CustomSelect.vue';
import CustomCalendar from '../CustomCalendar.vue';
import CustomCheckboxSelect from '../CustomCheckboxSelect.vue';
import { useUserStore } from '../../stores/user';

const props = defineProps({
    isOpen: Boolean,
    currentFilters: Object
});

const emit = defineEmits(['close', 'apply']);
const userStore = useUserStore();

const filters = ref({
    use_specific_dates: false,
    start_date: '',
    end_date: '',
    selected_months: [],
    selected_years: [],
    product_id: '',
    client_id: ''
});

const monthOptions = [
    { value: 1, label: 'Janeiro' },
    { value: 2, label: 'Fevereiro' },
    { value: 3, label: 'Março' },
    { value: 4, label: 'Abril' },
    { value: 5, label: 'Maio' },
    { value: 6, label: 'Junho' },
    { value: 7, label: 'Julho' },
    { value: 8, label: 'Agosto' },
    { value: 9, label: 'Setembro' },
    { value: 10, label: 'Outubro' },
    { value: 11, label: 'Novembro' },
    { value: 12, label: 'Dezembro' }
];

const yearOptions = ref([]);
const productOptions = ref([]);
const clientOptions = ref([]);
const loadingProducts = ref(false);
const loadingClients = ref(false);
const loadingYears = ref(false);

const fetchProducts = async () => {
    loadingProducts.value = true;
    try {
        const response = await fetch('/api/products', {
            headers: { 'Authorization': `Bearer ${userStore.token}` }
        });
        if (response.ok) {
            const data = await response.json();
            productOptions.value = data.map(p => {
                let imageUrl = null;
                if (p.image_path) {
                    if (p.image_path.startsWith('http')) {
                        imageUrl = p.image_path;
                    } else {
                        let cleanPath = p.image_path.replace(/^backend[\\/]/, '').replace(/\\/g, '/');
                        imageUrl = `/${cleanPath}`;
                    }
                }
                return {
                    value: p.id,
                    label: p.nome,
                    image: imageUrl
                };
            });
        }
    } catch (e) {
        console.error(e);
    } finally {
        loadingProducts.value = false;
    }
};

const fetchClients = async () => {
    loadingClients.value = true;
    try {
        const response = await fetch('/api/clients', {
            headers: { 'Authorization': `Bearer ${userStore.token}` }
        });
        if (response.ok) {
            const data = await response.json();
            clientOptions.value = data.map(c => ({
                value: c.id,
                label: c.nome
            }));
        }
    } catch (e) {
        console.error(e);
    } finally {
        loadingClients.value = false;
    }
};

const fetchAvailableYears = async () => {
    loadingYears.value = true;
    try {
        const response = await fetch('/api/dashboard/available-years', {
            headers: { 'Authorization': `Bearer ${userStore.token}` }
        });
        if (response.ok) {
            const years = await response.json();
            yearOptions.value = years.map(y => ({ value: y, label: String(y) }));
        }
    } catch (e) {
        console.error(e);
    } finally {
        loadingYears.value = false;
    }
};

watch(() => props.isOpen, (isOpen) => {
    if (isOpen) {
        if (props.currentFilters) {
            filters.value = { ...props.currentFilters };
        }
        // Defer fetch
        setTimeout(() => {
            if (productOptions.value.length === 0) fetchProducts();
            if (clientOptions.value.length === 0) fetchClients();
            if (yearOptions.value.length === 0) fetchAvailableYears();
        }, 350);
    }
});

const apply = () => {
    emit('apply', filters.value);
};

const clear = () => {
    filters.value = {
        use_specific_dates: false,
        start_date: '',
        end_date: '',
        selected_months: [],
        selected_years: [],
        product_id: '',
        client_id: ''
    };
    emit('apply', filters.value);
};
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
</style>
