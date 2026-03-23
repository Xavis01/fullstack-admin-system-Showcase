<template>
    <div>
        <!-- Blur Layer -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[60]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen"
                class="fixed inset-0 z-[60] flex items-center justify-center px-3 md:px-4 pt-36 pb-6 font-montserrat">
                <div class="absolute inset-0 bg-black/60" @click="close"></div>
                <transition name="modal">
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-2xl z-10 w-full max-w-4xl max-h-full overflow-hidden flex flex-col">
                        <!-- Header -->
                        <div
                            class="bg-neutral-800 text-white p-4 rounded-t-xl flex justify-between items-center shrink-0">
                            <h4 class="font-bold flex items-center gap-2">
                                <Edit3 class="w-5 h-5" /> Gerenciar Devolução #{{ returnItem.sale_id }}
                            </h4>
                            <button @click="close">
                                <X class="w-6 h-6" />
                            </button>
                        </div>

                        <!-- Horizontal Layout with Grid -->
                        <div class="p-6 flex-1 overflow-y-auto">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <!-- Left Column: Edit Details -->
                                <div>
                                    <h5
                                        class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4 border-b pb-2">
                                        Detalhes da Devolução</h5>
                                    <div class="space-y-4">
                                        <div>
                                            <label class="block text-gray-700 text-sm font-bold mb-2">Quantidade
                                                Devolvida</label>
                                            <input v-model="editForm.quant_devolvida" type="number"
                                                :disabled="returnItem.status === 'Concluída'"
                                                class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] py-2 px-3 leading-tight focus:outline-none focus:border-red-500 focus:bg-white transition duration-200" />
                                        </div>
                                        <div>
                                            <label class="block text-gray-700 text-sm font-bold mb-2">Observação</label>
                                            <textarea v-model="editForm.observacao" rows="5"
                                                class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg py-2 px-3 leading-tight focus:outline-none focus:border-red-500 focus:bg-white transition duration-200 resize-none"></textarea>
                                        </div>
                                        <button v-if="returnItem.status !== 'Concluída'" @click="saveChanges"
                                            :disabled="loadingEdit"
                                            class="w-full bg-neutral-700 hover:bg-neutral-800 text-white font-bold py-3 rounded-lg transition shadow-md flex items-center justify-center gap-2">
                                            <LoaderCircle v-if="loadingEdit" class="animate-spin w-5 h-5" />
                                            <span>{{ loadingEdit ? 'SALVANDO...' : 'SALVAR ALTERAÇÕES' }}</span>
                                        </button>
                                    </div>
                                </div>

                                <!-- Right Column: Finalize ("Dar Baixa") -->
                                <div>
                                    <div class="bg-red-50 p-5 rounded-xl border border-red-100 h-full">
                                        <h5 class="text-sm font-bold text-red-800 mb-4 flex items-center gap-2">
                                            <CheckCircle2 class="w-5 h-5" /> Dar Baixa / Finalizar
                                        </h5>

                                        <div v-if="returnItem.status === 'Concluída'" class="text-center py-4">
                                            <span
                                                class="text-green-600 font-bold flex items-center justify-center gap-2 text-lg">
                                                <Check class="w-6 h-6" /> Devolução Concluída!
                                            </span>
                                            <p class="text-xs text-gray-500 mt-2">Esta devolução já foi processada e
                                                alocada.</p>
                                        </div>

                                        <div v-else class="space-y-4">
                                            <div>
                                                <label class="block text-red-900 text-xs font-bold mb-2 uppercase">Data
                                                    de Retorno</label>
                                                <CustomCalendar v-model="finalizeForm.data_retorno"
                                                    placeholder="dd/mm/aaaa" />
                                            </div>
                                            <div>
                                                <label class="block text-red-900 text-xs font-bold mb-2 uppercase">Novo
                                                    Lote (Destino)</label>
                                                <CustomSelect v-model="finalizeForm.novo_lote_id" :options="loteOptions"
                                                    placeholder="Selecione um lote..." style="z-index: 9999;" />
                                                <p class="text-[10px] text-red-700 mt-2 font-medium">Selecione o lote
                                                    onde a mercadoria devolvida será inserida.</p>
                                            </div>

                                            <button @click="finalizeReturn" :disabled="!canFinalize || loadingFinalize"
                                                class="w-full bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-lg transition shadow-md mt-2 flex items-center justify-center gap-2">
                                                <LoaderCircle v-if="loadingFinalize" class="animate-spin w-5 h-5" />
                                                <span>{{ loadingFinalize ? 'PROCESSANDO...' : finalizeButtonText
                                                    }}</span>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Delete Button (Full Width Below) -->
                            <div class="col-span-1 md:col-span-2 pt-4 text-center">
                                <button @click="$emit('open-delete')"
                                    class="text-red-500 hover:text-red-700 font-bold text-sm transition flex items-center justify-center gap-1 mx-auto py-2">
                                    <Trash2 class="w-4 h-4" /> EXCLUIR DEVOLUÇÃO
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
import { ref, watch, computed } from 'vue'
import { Edit3, X, LoaderCircle, CheckCircle2, Check, Trash2 } from 'lucide-vue-next'
import CustomCalendar from '../CustomCalendar.vue'
import CustomSelect from '../CustomSelect.vue'

const props = defineProps({
    isOpen: Boolean,
    returnItem: Object,
    loadingEdit: Boolean,
    loadingFinalize: Boolean,
    loteOptions: Array,
    novo_lote_id: [String, Number]
})

const emit = defineEmits(['close', 'save', 'finalize', 'open-delete', 'update:novo_lote_id'])

const editForm = ref({
    quant_devolvida: '',
    observacao: ''
})

const finalizeForm = ref({
    data_retorno: '',
    novo_lote_id: ''
})

watch(() => props.returnItem, (newVal) => {
    if (newVal) {
        editForm.value.quant_devolvida = newVal.quant_devolvida
        editForm.value.observacao = newVal.observacao || ''

        finalizeForm.value.data_retorno = newVal.data_retorno || ''
        finalizeForm.value.novo_lote_id = newVal.novo_lote_id || ''
    }
}, { immediate: true })

// Watch for external updates to novo_lote_id (e.g. from Auto-Select in parent)
watch(() => props.novo_lote_id, (val) => {
    if (val !== undefined && val !== null && val !== finalizeForm.value.novo_lote_id) {
        finalizeForm.value.novo_lote_id = val
    }
})

// Propagate internal form changes to parent or wait for save/finalize?
// For 'novo_lote_id' which triggers 'NEW_LOT_TRIGGER', we need to emit update immediately for the parent watcher to catch it.
watch(() => finalizeForm.value.novo_lote_id, (val) => {
    emit('update:novo_lote_id', val)
})

const canFinalize = computed(() => {
    // If no date, cannot do anything
    if (!finalizeForm.value.data_retorno) return false

    // If status is Aberto, date is enough
    if (props.returnItem?.status === 'Aberto') return true

    // If status is Retornada, need either Lot OR date change to make sense
    if (props.returnItem?.status === 'Retornada') {
        const originalDate = props.returnItem.data_retorno || ''
        const dateChanged = finalizeForm.value.data_retorno !== originalDate
        return finalizeForm.value.novo_lote_id || dateChanged
    }

    return true
})

const finalizeButtonText = computed(() => {
    const hasLot = finalizeForm.value.novo_lote_id
    const status = props.returnItem?.status

    // Logic to mimic original behavior
    if (hasLot) return 'DAR BAIXA / REINTEGRAR'

    if (status === 'Aberto') return 'MARCAR COMO RETORNADA'
    if (status === 'Retornada') return 'SALVAR DATA'

    return 'FINALIZAR'
})

const close = () => {
    emit('close')
}

const saveChanges = () => {
    emit('save', { ...editForm.value })
}

const finalizeReturn = () => {
    emit('finalize', { ...finalizeForm.value })
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
</style>
