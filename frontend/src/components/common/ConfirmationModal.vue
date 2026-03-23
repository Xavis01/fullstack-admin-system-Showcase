<template>
    <div>
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[60]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-[70] font-montserrat p-4">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-lg p-6 z-10 w-full max-w-[400px] text-center border-2"
                        :class="borderColorClass">

                        <div class="flex justify-center mb-4">
                            <component :is="iconComponent" class="w-12 h-12" :class="textColorClass" />
                        </div>

                        <h3 class="text-lg font-bold mb-2 text-gray-800">{{ title }}</h3>
                        <p v-if="message" class="text-gray-600 mb-6 text-sm">{{ message }}</p>

                        <div class="flex flex-col sm:flex-row justify-center gap-3">
                            <button @click="$emit('confirm')"
                                class="w-full sm:flex-1 text-white font-bold py-2 px-6 rounded-lg transition duration-200 flex items-center justify-center min-w-[80px] shadow-md hover:shadow-lg active:scale-95"
                                :class="confirmButtonClass" :disabled="loading">
                                <span v-if="!loading">{{ confirmText }}</span>
                                <LoaderCircle v-else class="animate-spin w-5 h-5" />
                            </button>

                            <button @click="$emit('close')"
                                class="w-full sm:flex-1 bg-gray-200 hover:bg-gray-300 active:scale-95 text-gray-700 font-bold py-2 px-6 rounded-lg transition duration-200"
                                :disabled="loading">
                                {{ cancelText }}
                            </button>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { LoaderCircle, AlertTriangle, CheckCircle2, Info } from 'lucide-vue-next';

const props = defineProps({
    isOpen: Boolean,
    title: String,
    message: String,
    loading: Boolean,
    confirmText: {
        type: String,
        default: 'SIM'
    },
    cancelText: {
        type: String,
        default: 'NÃO'
    },
    type: {
        type: String,
        default: 'danger', // danger, success, info
        validator: (value) => ['danger', 'success', 'info'].includes(value)
    }
});

defineEmits(['close', 'confirm']);

const iconComponent = computed(() => {
    switch (props.type) {
        case 'success': return CheckCircle2;
        case 'info': return Info;
        default: return AlertTriangle;
    }
});

const textColorClass = computed(() => {
    switch (props.type) {
        case 'success': return 'text-green-600';
        case 'info': return 'text-blue-600';
        default: return 'text-red-600';
    }
});

const borderColorClass = computed(() => {
    switch (props.type) {
        case 'success': return 'border-green-100';
        case 'info': return 'border-blue-100';
        default: return 'border-red-100';
    }
});

const confirmButtonClass = computed(() => {
    switch (props.type) {
        case 'success': return 'bg-green-600 hover:bg-green-700';
        case 'info': return 'bg-blue-600 hover:bg-blue-700';
        default: return 'bg-red-600 hover:bg-red-700';
    }
});
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
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
    transform: scale(0.9) translateY(10px);
}
</style>
