<template>
    <div
        class="bg-white rounded-2xl shadow-lg p-4 md:p-6 border border-gray-100 transition-transform hover:-translate-y-1 duration-300">
        <div class="flex justify-between items-start mb-3 md:mb-4">
            <div class="p-2 md:p-3 rounded-xl bg-red-50">
                <component :is="icon" class="w-5 h-5 md:w-6 md:h-6 text-red-600" />
            </div>
            <div v-if="trend !== undefined"
                class="flex items-center gap-1 text-xs md:text-sm font-bold bg-gray-50 px-2 py-1 rounded-lg"
                :class="trend >= 0 ? 'text-emerald-600' : 'text-red-600'">
                <!-- <TrendingUp v-if="trend >= 0" class="w-4 h-4" /> -->
                <!-- <TrendingDown v-else class="w-4 h-4" /> -->
                <!-- <span>{{ Math.abs(trend) }}%</span> -->
            </div>
        </div>

        <div>
            <h3 class="text-gray-500 text-xs font-bold uppercase tracking-wider mb-1">{{ title }}</h3>
            <p class="text-2xl md:text-3xl font-extrabold text-neutral-800 tracking-tight">{{ formattedValue }}</p>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { TrendingUp, TrendingDown } from 'lucide-vue-next';

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    value: {
        type: [String, Number],
        required: true
    },
    icon: {
        type: Object,
        required: true
    },
    trend: {
        type: Number,
        default: undefined
    }
});

const formattedValue = computed(() => {
    if (props.value === null || props.value === undefined || props.value === '') return props.value;
    
    // Check if it's a valid number before formatting
    const num = Number(props.value);
    if (isNaN(num)) return props.value;
    
    return num.toLocaleString('pt-BR');
});
</script>
