<template>
    <div class="min-h-screen bg-gray-200 font-montserrat text-neutral-900">
        <section id="dashboard">
            <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
                <!-- Header -->
                <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6 md:mb-8">
                    <div class="flex items-center gap-2 md:gap-4">
                        <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
                            <ChartColumn class="text-white w-6 h-6 md:w-8 md:h-8" />
                        </div>
                        <div>
                            <h2 class="text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">
                                Dashboard Geral
                            </h2>
                            <p class="text-gray-500 font-semibold text-xs md:text-sm">Visão consolidada do negócio</p>
                        </div>
                    </div>

                    <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 w-full lg:w-auto">
                        <!-- View Toggle -->
                        <div
                            class="bg-white rounded-lg p-1 sm:mr-2 shadow-sm border border-gray-200 flex order-4 sm:order-1">
                            <button @click="setGranularity('month')"
                                class="flex-1 sm:flex-none px-3 py-2 text-xs font-bold rounded-md transition-colors"
                                :class="filters.granularity === 'month' ? 'bg-neutral-800 text-white shadow' : 'text-gray-500 hover:text-neutral-800'">
                                MÊS
                            </button>
                            <button @click="setGranularity('day')"
                                class="flex-1 sm:flex-none px-3 py-2 text-xs font-bold rounded-md transition-colors"
                                :class="filters.granularity === 'day' ? 'bg-neutral-800 text-white shadow' : 'text-gray-500 hover:text-neutral-800'">
                                DIA
                            </button>
                        </div>

                        <button @click="isReportModalOpen = true"
                            class="w-full sm:w-auto order-3 sm:order-2 bg-neutral-800 hover:bg-black active:scale-95 text-white font-semibold h-11 px-4 rounded-lg shadow-lg transition duration-200 flex items-center justify-center gap-2">
                            <FileText class="w-5 h-5" />
                            RELATÓRIO
                        </button>
                        <button @click="isGoalsModalOpen = true"
                            class="w-full sm:w-auto order-4 sm:order-3 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-semibold h-11 px-4 rounded-lg shadow-lg transition duration-200 flex items-center justify-center gap-2">
                            <Goal class="w-5 h-5" />
                            METAS
                        </button>
                        <button @click="openFilterModal"
                            class="w-full sm:w-auto order-5 sm:order-4 bg-red-600 hover:bg-red-700 active:scale-95 text-white font-semibold h-11 px-4 md:px-6 rounded-lg shadow-lg transition duration-200 flex items-center justify-center gap-2">
                            <Filter class="w-5 h-5" />
                            FILTRAR
                        </button>
                        <button @click="refreshData"
                            class="w-full sm:w-auto order-1 sm:order-5 bg-white hover:bg-gray-50 active:scale-95 text-neutral-700 font-semibold h-11 px-4 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2 border border-blue-100">
                            <RotateCw :class="{ 'animate-spin': loading }" class="w-5 h-5 text-red-600" />
                            <span class="sm:hidden">ATUALIZAR</span>
                        </button>
                    </div>
                </div>

                <!-- Active Filter Indicator -->
                <div v-if="hasActiveFilters" class="mb-6 flex gap-2 flex-wrap">
                    <div v-if="filters.start_date"
                        class="bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-bold border border-red-200 flex items-center gap-1">
                        De: {{ formatDate(filters.start_date) }}
                    </div>
                    <div v-if="filters.end_date"
                        class="bg-red-100 text-red-700 px-3 py-1 rounded-full text-xs font-bold border border-red-200 flex items-center gap-1">
                        Até: {{ formatDate(filters.end_date) }}
                    </div>
                    <div v-if="filters.product_id"
                        class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold border border-blue-200 flex items-center gap-1">
                        Produto Selecionado
                    </div>
                    <div v-if="filters.granularity === 'day'"
                        class="bg-neutral-200 text-neutral-700 px-3 py-1 rounded-full text-xs font-bold border border-neutral-300 flex items-center gap-1">
                        Visão Diária
                    </div>
                    <div v-if="filters.client_id"
                        class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs font-bold border border-purple-200 flex items-center gap-1">
                        Cliente Selecionado
                    </div>
                    <button @click="clearFilters"
                        class="text-xs text-gray-500 hover:text-red-600 font-bold underline">Limpar Filtros</button>
                </div>

                <!-- Warning Alert for Client Filter -->
                <div v-if="filters.client_id"
                    class="mb-6 bg-amber-50 border-l-4 border-amber-500 p-3 md:p-4 rounded-r-lg shadow-sm flex items-start gap-2 md:gap-3">
                    <AlertCircle class="text-amber-500 w-4 h-4 md:w-5 md:h-5 flex-shrink-0 mt-0.5" />
                    <div>
                        <h4 class="font-bold text-amber-800 text-xs md:text-sm uppercase">Atenção</h4>
                        <p class="text-amber-700 text-xs md:text-sm mt-1">
                            O 'filtro por cliente' aplica-se <strong>apenas</strong> aos dados de vendas (Volume de
                            vendas
                            e Gráficos de vendas).
                            Sendo assim, dados de produção e estoque não são afetados pelo 'filtro por cliente', já que
                            não possuem relação.
                        </p>
                    </div>
                </div>

                <div v-if="loading && !stats" class="flex-1 flex items-center justify-center h-64">
                    <LoaderCircle class="animate-spin text-neutral-700 w-8 h-8 md:w-12 md:h-12" />
                </div>

                <template v-else>
                    <!-- KPI Stats Grid -->
                    <div
                        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8 animate-fade-in">
                        <KPICard title="Vendas Totais" :value="stats?.total_sales_volume" :icon="ShoppingBag"
                            :trend="stats?.sales_growth" />
                        <KPICard title="Produção Total" :value="stats?.total_production_volume" :icon="Factory" />
                        <KPICard title="Estoque Atual" :value="stats?.current_stock" :icon="Package" />
                        <KPICard title="Clientes Ativos" :value="stats?.total_clients" :icon="Users" />
                    </div>

                    <!-- Charts Section -->
                    <div class="animate-fade-in animation-delay-200">
                        <DashboardCharts :overTimeData="chartsData?.over_time"
                            :salesByProduct="chartsData?.sales_by_product"
                            :productionByProduct="chartsData?.production_by_product" :chartTitle="chartTitle"
                            :hasDateFilter="hasDateFilter" :granularity="filters.granularity" />
                    </div>
                </template>
            </div>
        </section>

        <DashboardFilterModal :isOpen="isFilterModalOpen" :currentFilters="filters" @close="isFilterModalOpen = false"
            @apply="handleApplyFilters" />

        <GoalsModal :isOpen="isGoalsModalOpen" @close="isGoalsModalOpen = false" />

        <ReportConfigModal :isOpen="isReportModalOpen" @close="isReportModalOpen = false" />
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { ShoppingBag, Factory, Package, Users, RotateCw, ChartColumn, LoaderCircle, Filter, AlertCircle, Goal, FileText } from 'lucide-vue-next';
import KPICard from '../components/dashboard/KPICard.vue';
import DashboardCharts from '../components/dashboard/DashboardCharts.vue';
import DashboardFilterModal from '../components/dashboard/DashboardFilterModal.vue';
import GoalsModal from '../components/dashboard/GoalsModal.vue';
import ReportConfigModal from '../components/dashboard/ReportConfigModal.vue';
import { useUserStore } from '../stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();
const loading = ref(true);
const stats = ref(null);
const chartsData = ref(null);
const isFilterModalOpen = ref(false);
const isGoalsModalOpen = ref(false);
const isReportModalOpen = ref(false);

const filters = ref({
    use_specific_dates: false,
    start_date: '',
    end_date: '',
    selected_months: [],
    selected_years: [],
    selected_years: [],
    product_id: '',
    client_id: '',
    granularity: 'month'
});

const chartTitle = computed(() => filters.value.granularity === 'day' ? 'Desempenho por Dias' : 'Desempenho por Meses');

const hasActiveFilters = computed(() => {
    return !!(filters.value.start_date || filters.value.end_date || filters.value.product_id || filters.value.client_id ||
        filters.value.selected_months.length > 0 || filters.value.selected_years.length > 0);
});

const hasDateFilter = computed(() => {
    return !!(filters.value.start_date || filters.value.end_date ||
        filters.value.selected_months.length > 0 || filters.value.selected_years.length > 0);
});

const formatDate = (d) => {
    if (!d) return '';
    const [y, m, day] = d.split('-');
    return `${day}/${m}/${y}`;
};

const fetchData = async () => {
    loading.value = true;
    userStore.ensureValidSession(router);

    try {
        const headers = { 'Authorization': `Bearer ${userStore.token}` };

        // Build params based on filter mode
        const params = new URLSearchParams();

        if (filters.value.use_specific_dates) {
            // Use specific date range
            if (filters.value.start_date) params.append('start_date', filters.value.start_date);
            if (filters.value.end_date) params.append('end_date', filters.value.end_date);
        } else {
            // Use month/year selection
            if (filters.value.selected_months.length > 0) {
                params.append('months', filters.value.selected_months.join(','));
            }
            if (filters.value.selected_years.length > 0) {
                params.append('years', filters.value.selected_years.join(','));
            }
        }

        if (filters.value.client_id) params.append('client_id', filters.value.client_id);
        if (filters.value.product_id) params.append('product_id', filters.value.product_id);
        params.append('granularity', filters.value.granularity);

        const [summaryRes, chartsRes] = await Promise.all([
            fetch(`/api/dashboard/summary?${params.toString()}`, { headers }),
            fetch(`/api/dashboard/charts?${params.toString()}`, { headers })
        ]);

        if (summaryRes.ok) stats.value = await summaryRes.json();
        if (chartsRes.ok) chartsData.value = await chartsRes.json();

    } catch (error) {
        console.error("Failed to load dashboard data", error);
    } finally {
        loading.value = false;
    }
};

const setGranularity = (gra) => {
    filters.value.granularity = gra;
    fetchData();
};

const refreshData = () => {
    fetchData();
};

const openFilterModal = () => isFilterModalOpen.value = true;

const handleApplyFilters = (newFilters) => {
    // Merge new filters while preserving granularity
    filters.value = { ...filters.value, ...newFilters };
    isFilterModalOpen.value = false;
    fetchData();
};

const clearFilters = () => {
    const gra = filters.value.granularity;
    filters.value = {
        use_specific_dates: false,
        start_date: '',
        end_date: '',
        selected_months: [],
        selected_years: [],
        product_id: '',
        client_id: '',
        granularity: gra
    };
    fetchData();
};

onMounted(() => {
    fetchData();
});
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.5s ease-out forwards;
    opacity: 0;
}

.animation-delay-200 {
    animation-delay: 0.2s;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
