<template>
    <div>
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-40"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 font-montserrat p-4 md:pt-20">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-lg z-10 w-full max-w-[500px] max-h-[90vh] overflow-y-auto">
                        <!-- Header -->
                        <div
                            class="bg-neutral-700 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl">
                            <h3 class="text-lg md:text-xl font-bold">REGISTRAR DEVOLUÇÃO</h3>
                        </div>

                        <!-- Body -->
                        <div class="p-4 sm:p-6 md:p-8">
                            <div v-if="sale" class="mb-6 bg-red-50 p-4 rounded-lg border border-red-100">
                                <p class="text-sm text-gray-600">Venda: <span class="font-bold text-gray-800">#{{
                                        sale.id }}</span></p>
                                <p class="text-sm text-gray-600">Produto: <span class="font-bold text-gray-800">{{
                                        sale.product_name }}</span></p>
                                <p class="text-sm text-gray-600">Cliente: <span class="font-bold text-gray-800">{{
                                        sale.client_name }}</span></p>
                                <p class="text-sm text-gray-600">Qtd. Vendida: <span class="font-bold text-gray-800">{{
                                        sale.quant_caixa_vendida }}</span></p>
                            </div>

                            <form @submit.prevent="save">
                                <!-- Quantidade Devolvida -->
                                <div class="mb-4 md:mb-6">
                                    <div class="flex justify-between items-end mb-2">
                                        <label class="block text-gray-700 text-xs md:text-sm font-bold">Quantidade
                                            Devolvida</label>
                                        <span class="text-xs text-gray-500 font-medium">
                                            Máx: {{ sale?.quant_caixa_vendida }}
                                        </span>
                                    </div>
                                    <div class="relative">
                                        <input v-model="formData.quant_devolvida" type="number" min="1"
                                            :max="sale?.quant_caixa_vendida"
                                            class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200"
                                            placeholder="Digite a quantidade..." />
                                        <span
                                            class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 font-semibold">{{
                                                sale?.product_name?.toLowerCase().includes('25kg') ? 'Sacos' : 'Caixas'
                                            }}</span>
                                    </div>
                                </div>

                                <!-- Observação -->
                                <div class="mb-6">
                                    <label class="block text-gray-700 text-xs md:text-sm font-bold mb-2">Observação
                                        (Opcional)</label>
                                    <textarea v-model="formData.observacao" rows="3"
                                        class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg p-3 leading-tight hover:border-gray-400 focus:outline-none focus:border-red-500 focus:bg-white transition duration-200 resize-none"
                                        placeholder="Motivo da devolução..."></textarea>
                                </div>

                                <div class="flex justify-center gap-3">
                                    <button type="button" @click="$emit('close')"
                                        class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold h-12 px-6 rounded-lg transition duration-200 flex-1">
                                        CANCELAR
                                    </button>
                                    <button type="submit"
                                        class="bg-red-600 hover:bg-red-700 active:scale-95 text-white font-bold h-12 px-6 rounded-lg transition duration-200 flex items-center justify-center flex-1"
                                        :disabled="loading">
                                        <span v-if="!loading">CONFIRMAR</span>
                                        <LoaderCircle v-else class="animate-spin w-5 h-5 md:w-6 md:h-6" />
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { LoaderCircle } from 'lucide-vue-next'
import { useToastStore } from '../../stores/toast'

const props = defineProps({
    isOpen: Boolean,
    sale: Object,
    loading: Boolean
})

const emit = defineEmits(['close', 'save'])
const toastStore = useToastStore()

const formData = ref({
    quant_devolvida: '',
    observacao: ''
})

watch(() => props.isOpen, (isOpen) => {
    if (isOpen) {
        formData.value = {
            quant_devolvida: '',
            observacao: ''
        }
    }
})

const save = () => {
    const errors = []

    if (!formData.value.quant_devolvida || Number(formData.value.quant_devolvida) <= 0) {
        errors.push('Quantidade Devolvida (maior que 0)')
    }

    if (props.sale && Number(formData.value.quant_devolvida) > props.sale.quant_caixa_vendida) {
        errors.push(`Quantidade não pode exceder a venda (${props.sale.quant_caixa_vendida})`)
    }

    if (errors.length > 0) {
        toastStore.add({
            title: 'Erro de Validação',
            message: errors.join(', '),
            type: 'warning'
        })
        return
    }

    emit('save', {
        sale_id: props.sale.id,
        ...formData.value
    })
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
