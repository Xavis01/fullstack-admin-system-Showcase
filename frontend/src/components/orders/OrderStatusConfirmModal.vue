<template>
    <div>
        <!-- Blur Layer with synchronized transition -->
        <transition name="modal-backdrop">
            <div v-if="isOpen && order" class="fixed inset-0 z-[70]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen && order"
                class="fixed inset-0 flex items-center justify-center z-[70] font-montserrat p-4">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen && order"
                        class="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 relative z-10 text-center">
                        <div class="mx-auto w-12 h-12 rounded-full mb-4 flex items-center justify-center"
                            :class="order.achieved ? 'bg-orange-100 text-orange-600' : 'bg-green-100 text-green-600'">
                            <Clock v-if="order.achieved" class="w-6 h-6" />
                            <CheckCircle2 v-else class="w-6 h-6" />
                        </div>
                        <h3 class="text-xl font-bold text-neutral-800 mb-2">Confirmar Alteração de Status</h3>
                        <p v-if="order.achieved" class="text-sm text-gray-600 mb-6">
                            Este pedido estava como <strong>Concluído</strong>. Deseja marcá-lo como <strong
                                class="text-orange-600">Pendente</strong> novamente?
                        </p>
                        <p v-else class="text-sm text-gray-600 mb-6">
                            Deseja marcar o pedido <strong>#{{ order.id }}</strong> como <strong
                                class="text-green-600">Concluído</strong>?
                        </p>

                        <div class="flex flex-col-reverse sm:flex-row gap-3 justify-center">
                            <button @click="$emit('close')"
                                class="w-full sm:w-auto px-5 py-2.5 text-sm font-bold text-gray-600 hover:bg-gray-100 rounded-lg transition active:scale-95">
                                CANCELAR
                            </button>
                            <button @click="$emit('confirm')"
                                class="w-full sm:w-auto px-5 py-2.5 text-sm font-bold text-white rounded-lg transition shadow-md active:scale-95 flex items-center justify-center min-w-[120px]"
                                :class="order.achieved ? 'bg-orange-600 hover:bg-orange-700' : 'bg-green-600 hover:bg-green-700'"
                                :disabled="isToggling">
                                <LoaderCircle v-if="isToggling" class="w-5 h-5 animate-spin" />
                                <span v-else>CONFIRMAR</span>
                            </button>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { Clock, CheckCircle2, LoaderCircle } from 'lucide-vue-next'

const props = defineProps({
    isOpen: Boolean,
    order: Object,
    isToggling: Boolean
})

const emit = defineEmits(['close', 'confirm'])
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
