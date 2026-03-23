<template>
    <div>
        <!-- Blur Layer -->
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
                            :class="order.separado ? 'bg-yellow-100 text-yellow-600' : 'bg-blue-100 text-blue-600'">
                            <Clock v-if="order.separado" class="w-6 h-6" />
                            <PackageCheck v-else class="w-6 h-6" />
                        </div>
                        <h3 class="text-xl font-bold text-neutral-800 mb-2">Confirmar Alteração</h3>
                        <p v-if="order.separado" class="text-sm text-gray-600 mb-6">
                            Deseja retornar o pedido <strong>#{{ order.id }}</strong> para
                            <strong class="text-yellow-600">Pendente</strong>?
                        </p>
                        <p v-else class="text-sm text-gray-600 mb-6">
                            Deseja marcar o pedido <strong>#{{ order.id }}</strong> como
                            <strong class="text-blue-600">Separado</strong>?
                        </p>

                        <div class="flex flex-col-reverse sm:flex-row gap-3 justify-center">
                            <button @click="$emit('close')"
                                class="w-full sm:w-auto px-5 py-2.5 text-sm font-bold text-gray-600 hover:bg-gray-100 rounded-lg transition active:scale-95">
                                CANCELAR
                            </button>
                            <button @click="$emit('confirm')"
                                class="w-full sm:w-auto px-5 py-2.5 text-sm font-bold text-white rounded-lg transition shadow-md active:scale-95 flex items-center justify-center min-w-[120px]"
                                :class="order.separado ? 'bg-yellow-600 hover:bg-yellow-700' : 'bg-blue-600 hover:bg-blue-700'"
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
import { Clock, PackageCheck, LoaderCircle } from 'lucide-vue-next'

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
