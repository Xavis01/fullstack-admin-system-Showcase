<template>
    <div>
        <!-- Delete Confirmation Modal (Stylized) -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[70]"
                style="backdrop-filter: blur(8px); background-color: rgba(0, 0, 0, 0.4); will-change: opacity;">
            </div>
        </transition>

        <transition name="modal">
            <div v-if="isOpen" class="fixed inset-0 z-[70] flex items-center justify-center p-4 font-montserrat">
                <div class="absolute inset-0" @click="close"></div>
                <div
                    class="bg-white rounded-xl shadow-2xl z-20 w-full max-w-md overflow-hidden relative transform transition-all">
                    <!-- Header with Red Gradient -->
                    <div
                        class="bg-gradient-to-r from-red-600 to-red-700 p-6 text-center text-white relative overflow-hidden">
                        <div
                            class="absolute top-0 left-0 w-full h-full opacity-10 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]">
                        </div>
                        <div
                            class="bg-white/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3 backdrop-blur-sm">
                            <Trash2 class="w-8 h-8 text-white" />
                        </div>
                        <h3 class="font-bold text-xl tracking-wide">EXCLUIR DEVOLUÇÃO</h3>
                        <p class="text-red-100 text-sm mt-1">Esta ação não poderá ser desfeita.</p>
                    </div>

                    <div class="p-6 text-center">
                        <!-- Case 1: Linked to Lot AND Insufficient Stock -->
                        <div
                            v-if="returnItem && returnItem.novo_lote_id && linkedLot && linkedLot.estoque_lote < returnItem.quant_devolvida">
                            <div class="bg-red-50 text-red-800 p-4 rounded-lg mb-6 border border-red-200">
                                <AlertTriangle class="w-10 h-10 mx-auto mb-2 text-red-600" />
                                <h4 class="font-bold text-lg mb-2">Ação Bloqueada</h4>
                                <p class="text-sm">
                                    Esta devolução foi vinculada ao lote <strong>#{{ returnItem.novo_lote_id
                                        }}</strong>.
                                </p>
                                <p class="text-sm mt-2 font-bold">
                                    O lote não possui estoque suficiente para reverter esta devolução.
                                </p>
                                <p class="text-xs mt-1">
                                    Estoque Atual: {{ linkedLot.estoque_lote }} | Necessário: {{
                                    returnItem.quant_devolvida }}
                                </p>
                                <p class="text-sm mt-3">
                                    Os itens já foram vendidos. Não é possível excluir.
                                </p>
                            </div>
                            <button @click="close"
                                class="w-full py-3 px-4 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold rounded-lg transition-colors duration-200">
                                ENTENDI
                            </button>
                        </div>

                        <!-- Case 2: Linked to Lot, BUT Sufficient Stock (Warning) -->
                        <div v-else-if="returnItem && returnItem.novo_lote_id">
                            <div class="bg-yellow-50 text-yellow-800 p-4 rounded-lg mb-6 border border-yellow-200">
                                <AlertTriangle class="w-10 h-10 mx-auto mb-2 text-yellow-600" />
                                <h4 class="font-bold text-lg mb-2">Atenção!</h4>
                                <p class="text-sm">
                                    Esta devolução está vinculada ao lote <strong>#{{ returnItem.novo_lote_id
                                        }}</strong>.
                                </p>
                                <p class="text-sm mt-3 font-bold">
                                    Ao excluir:
                                </p>
                                <ul class="text-sm text-left list-disc list-inside mt-2 space-y-1">
                                    <li>{{ returnItem.quant_devolvida }} itens serão <strong>removidos</strong> do lote
                                        #{{ returnItem.novo_lote_id }}.</li>
                                    <li>A quantidade voltará para a <strong>venda original</strong>.</li>
                                </ul>
                            </div>

                            <div class="flex gap-3">
                                <button @click="close" :disabled="loading"
                                    class="flex-1 py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg transition-colors duration-200">
                                    CANCELAR
                                </button>
                                <button @click="confirm" :disabled="loading"
                                    class="flex-1 py-3 px-4 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2">
                                    <LoaderCircle v-if="loading" class="animate-spin w-5 h-5" />
                                    <span>{{ loading ? 'EXCLUINDO...' : 'CONFIRMAR EXCLUSÃO' }}</span>
                                </button>
                            </div>
                        </div>

                        <!-- Case 3: Standard Deletion (Not Linked) -->
                        <div v-else>
                            <p class="text-gray-600 mb-6 leading-relaxed">
                                Ao excluir, a quantidade devolvida será restaurada automaticamente para a
                                <strong class="text-gray-900">Quantidade Vendida</strong> da venda original.
                            </p>

                            <div class="flex gap-3">
                                <button @click="close" :disabled="loading"
                                    class="flex-1 py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg transition-colors duration-200">
                                    CANCELAR
                                </button>
                                <button @click="confirm" :disabled="loading"
                                    class="flex-1 py-3 px-4 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2">
                                    <LoaderCircle v-if="loading" class="animate-spin w-5 h-5" />
                                    <span>{{ loading ? 'EXCLUINDO...' : 'CONFIRMAR' }}</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { Trash2, AlertTriangle, LoaderCircle } from 'lucide-vue-next'

const props = defineProps({
    isOpen: Boolean,
    returnItem: Object,
    loading: Boolean
})

const emit = defineEmits(['close', 'confirm'])

const close = () => {
    emit('close')
}

const confirm = () => {
    emit('confirm')
}
</script>
