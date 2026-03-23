<template>
    <div class="flex flex-col gap-6">
        <!-- Main Chart: Sales vs Production -->
        <div class="w-full p-6 rounded-2xl bg-white border border-gray-100 shadow-lg">
            <div class="flex items-center justify-between mb-6">
                <div>
                    <h3 class="text-xl font-extrabold text-neutral-800 uppercase tracking-wide">{{ chartTitle }}</h3>
                    <p v-if="!hasDateFilter && chartSubtitle" class="text-xs text-gray-400 font-semibold mt-1">{{
                        chartSubtitle }}</p>
                </div>
                <div class="flex gap-4 text-xs font-bold uppercase tracking-wider">
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-red-600"></span>
                        <span class="text-gray-500">Vendas</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-neutral-800"></span>
                        <span class="text-gray-500">Produção</span>
                    </div>
                </div>
            </div>
            <div class="h-[350px] w-full">
                <Bar :data="barChartData" :options="barChartOptions" />
            </div>
        </div>

        <!-- Secondary Charts Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

            <!-- Sales Distribution -->
            <div class="p-6 rounded-2xl bg-white border border-gray-100 shadow-lg flex flex-col">
                <h3 class="text-xl font-extrabold text-neutral-800 uppercase tracking-wide mb-6">Vendas por Produto</h3>
                <div class="flex-1 flex items-center justify-center relative min-h-[300px]">
                    <Doughnut :data="salesDoughnutData" :options="doughnutOptions" />
                </div>
            </div>

            <!-- Production Distribution -->
            <div class="p-6 rounded-2xl bg-white border border-gray-100 shadow-lg flex flex-col">
                <h3 class="text-xl font-extrabold text-neutral-800 uppercase tracking-wide mb-6">Produção por Produto
                </h3>
                <div class="flex-1 flex items-center justify-center relative min-h-[300px]">
                    <Doughnut :data="productionDoughnutData" :options="doughnutOptions" />
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import { Bar, Doughnut } from 'vue-chartjs';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const props = defineProps({
    overTimeData: { type: Array, default: () => [] },
    salesByProduct: { type: Array, default: () => [] },
    productionByProduct: { type: Array, default: () => [] },
    chartTitle: { type: String, default: 'Desempenho Anual' },
    hasDateFilter: { type: Boolean, default: false },
    granularity: { type: String, default: 'month' }
});

const chartSubtitle = computed(() => {
    if (props.hasDateFilter) return '';
    return props.granularity === 'day' ? 'últimos 30 dias' : 'últimos 12 meses';
});

// --- Bar Chart Configuration ---
const barChartData = computed(() => {
    const labels = props.overTimeData.map(item => {
        if (!item.date) return '';
        const parts = item.date.split('-');
        if (parts.length === 3) {
            const [y, m, d] = parts;
            return `${d}/${m}/${y}`;
        } else if (parts.length === 2) {
            const [y, m] = parts;
            return `${m}/${y}`;
        }
        return item.date;
    });

    return {
        labels: labels,
        datasets: [
            {
                label: 'Vendas',
                backgroundColor: '#dc2626', // Red-600
                data: props.overTimeData.map(item => item.sales),
                borderRadius: 4,
                barPercentage: 0.6,
                categoryPercentage: 0.8
            },
            {
                label: 'Produção',
                backgroundColor: '#262626', // Neutral-800
                data: props.overTimeData.map(item => item.production),
                borderRadius: 4,
                barPercentage: 0.6,
                categoryPercentage: 0.8
            }
        ]
    };
});

const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        tooltip: {
            backgroundColor: '#ffffff',
            titleColor: '#171717',
            bodyColor: '#52525b',
            padding: 12,
            borderColor: '#e5e7eb',
            borderWidth: 1,
            displayColors: true,
            usePointStyle: true,
            callbacks: {
                labelTextColor: () => '#52525b',
                label: (context) => {
                    const label = context.dataset.label || '';
                    const value = context.parsed.y;
                    return ` ${label}: ${value}`;
                }
            }
        }
    },
    scales: {
        x: {
            grid: { display: false, drawBorder: false },
            ticks: { color: '#71717a', font: { size: 11, weight: '600' } }
        },
        y: {
            grid: { color: '#f4f4f5', borderDash: [4, 4], drawBorder: false },
            ticks: { color: '#71717a', font: { size: 11, weight: '600' }, padding: 10 }
        }
    }
};


// --- Doughnut Charts Configuration ---
// Escorpião brand colors: Red, Black, Gray, then additional colors
const doughnutColors = ['#dc2626', '#262626', '#737373', '#3b82f6', '#f59e0b', '#10b981', '#8b5cf6'];

const salesDoughnutData = computed(() => ({
    labels: props.salesByProduct.map(p => p.product),
    datasets: [{
        backgroundColor: doughnutColors,
        borderColor: '#ffffff',
        borderWidth: 2,
        data: props.salesByProduct.map(p => p.total),
    }]
}));

const productionDoughnutData = computed(() => ({
    labels: props.productionByProduct.map(p => p.product),
    datasets: [{
        backgroundColor: doughnutColors,
        borderColor: '#ffffff',
        borderWidth: 2,
        data: props.productionByProduct.map(p => p.total),
    }]
}));

const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
        animateRotate: true,
        animateScale: true,
        duration: 800,
        easing: 'easeInOutQuart'
    },
    interaction: {
        mode: 'point',
        intersect: true
    },
    plugins: {
        legend: {
            position: 'bottom',
            onClick: (e, legendItem, legend) => {
                const index = legendItem.index;
                const chart = legend.chart;
                const meta = chart.getDatasetMeta(0);

                // Toggle visibility
                meta.data[index].hidden = !meta.data[index].hidden;
                chart.update();
            },
            onHover: (e, legendItem, legend) => {
                e.native.target.style.cursor = 'pointer';

                // Highlight corresponding segment
                const index = legendItem.index;
                const chart = legend.chart;
                const meta = chart.getDatasetMeta(0);

                // Reset all segments
                meta.data.forEach((segment, i) => {
                    if (i === index && !segment.hidden) {
                        segment.options.hoverOffset = 15;
                        segment.options.borderWidth = 3;
                    } else {
                        segment.options.hoverOffset = 0;
                        segment.options.borderWidth = 2;
                    }
                });
                chart.update('none');
            },
            onLeave: (e, legendItem, legend) => {
                e.native.target.style.cursor = 'default';

                // Reset all segments
                const chart = legend.chart;
                const meta = chart.getDatasetMeta(0);
                meta.data.forEach(segment => {
                    segment.options.hoverOffset = 0;
                    segment.options.borderWidth = 2;
                });
                chart.update('none');
            },
            labels: {
                color: '#52525b',
                usePointStyle: true,
                padding: 20,
                font: { size: 12, weight: '600' },
                generateLabels: (chart) => {
                    const data = chart.data;
                    if (data.labels.length && data.datasets.length) {
                        const dataset = data.datasets[0];
                        const total = dataset.data.reduce((acc, val) => acc + val, 0);
                        const meta = chart.getDatasetMeta(0);

                        return data.labels.map((label, i) => {
                            const value = dataset.data[i];
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            const hidden = meta.data[i].hidden;

                            return {
                                text: `${label} (${percentage}%)`,
                                fillStyle: hidden ? '#d1d5db' : dataset.backgroundColor[i],
                                fontColor: hidden ? '#9ca3af' : '#52525b',
                                hidden: false,
                                index: i,
                                strokeStyle: hidden ? '#d1d5db' : dataset.backgroundColor[i]
                            };
                        });
                    }
                    return [];
                }
            }
        },
        tooltip: {
            backgroundColor: '#ffffff',
            titleColor: '#171717',
            bodyColor: '#52525b',
            padding: 16,
            borderColor: '#e5e7eb',
            borderWidth: 2,
            cornerRadius: 8,
            displayColors: true,
            boxPadding: 6,
            usePointStyle: true,
            callbacks: {
                label: (context) => {
                    const label = context.label || '';
                    const value = context.parsed;
                    const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                    const unit = label.toLowerCase().includes('25kg') ? 'sacos' : 'caixas';
                    return ` ${label}: ${value} ${unit} (${percentage}%)`;
                },
                title: () => ''
            }
        }
    },
    elements: {
        arc: {
            borderWidth: 2,
            hoverBorderWidth: 3,
            hoverOffset: 12,
            borderColor: '#ffffff'
        }
    },
    cutout: '70%',
    layout: { padding: 20 }
};
</script>
