<template>
    <transition name="modal-backdrop">
        <div v-if="isOpen" class="fixed inset-0 z-[70]"
            style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
        </div>
    </transition>

    <transition name="modal-backdrop">
        <div v-if="isOpen"
            class="fixed inset-0 flex items-center justify-center z-[70] font-montserrat px-3 md:px-4 pt-36 pb-6">
            <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
            <transition name="modal">
                <div v-if="isOpen"
                    class="bg-white rounded-xl shadow-2xl z-10 w-full max-w-2xl flex flex-col overflow-hidden max-h-full">

                    <!-- Header -->
                    <div class="bg-red-600 text-white px-4 md:px-6 py-4 flex items-center justify-between shrink-0">
                        <div class="flex items-center gap-3">
                            <div class="bg-white/20 p-2 rounded-lg">
                                <Info class="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <h3 class="text-base md:text-lg font-bold">ENTENDENDO AS ESTATÍSTICAS</h3>
                                <p class="text-red-100 text-xs font-medium">Guia de métricas e indicadores</p>
                            </div>
                        </div>
                        <button @click="$emit('close')"
                            class="text-white/70 hover:text-white transition p-1 rounded-full hover:bg-white/10">
                            <X class="w-5 h-5" />
                        </button>
                    </div>

                    <!-- Body -->
                    <div class="flex-1 overflow-y-auto bg-gray-50 p-4 md:p-6 custom-scrollbar">
                        <div class="space-y-6">

                            <!-- Tempo Parado -->
                            <div
                                class="bg-white p-4 md:p-5 rounded-xl border border-gray-200 shadow-sm relative overflow-hidden group hover:border-red-300 transition">
                                <div
                                    class="absolute top-0 right-0 w-16 h-16 bg-red-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110">
                                </div>
                                <div class="flex items-start gap-4">
                                    <div class="bg-red-100 p-3 rounded-lg text-red-600 mt-1">
                                        <Clock class="w-6 h-6" />
                                    </div>
                                    <div class="flex-1">
                                        <h4 class="text-lg font-bold text-gray-800 mb-1">Tempo Parado</h4>
                                        <p class="text-sm text-gray-600 leading-relaxed mb-2">
                                            Calcula quantos dias o lote ficou no estoque desde a <strong>sua produção
                                                até a primeira venda</strong>.
                                        </p>
                                        <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside ml-1">
                                            <li>Se não houver vendas, conta até o dia de hoje.</li>
                                            <li>Ajuda a identificar lotes que estão demorando a sair.</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            <!-- Status de Vendas -->
                            <div
                                class="bg-white p-4 md:p-5 rounded-xl border border-gray-200 shadow-sm relative overflow-hidden group hover:border-red-300 transition">
                                <div
                                    class="absolute top-0 right-0 w-16 h-16 bg-red-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110">
                                </div>
                                <div class="flex items-start gap-4">
                                    <div class="bg-red-100 p-3 rounded-lg text-red-600 mt-1">
                                        <CalendarDays class="w-6 h-6" />
                                    </div>
                                    <div class="flex-1">
                                        <h4 class="text-lg font-bold text-gray-800 mb-1">Status de Vendas (1ª e Última)
                                        </h4>
                                        <p class="text-sm text-gray-600 leading-relaxed mb-2">
                                            Mostra as datas exatas em que o lote começou e terminou de ser vendido.
                                        </p>
                                        <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside ml-1">
                                            <li><strong>1ª:</strong> Data da primeira movimentação de saída.</li>
                                            <li><strong>Última:</strong> Data da última venda registrada (seja para
                                                esgotar ou a mais recente).</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            <!-- Desempenho / Tempo p/ Esgotar -->
                            <div
                                class="bg-white p-4 md:p-5 rounded-xl border border-gray-200 shadow-sm relative overflow-hidden group hover:border-red-300 transition">
                                <div
                                    class="absolute top-0 right-0 w-16 h-16 bg-red-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110">
                                </div>
                                <div class="flex items-start gap-4">
                                    <div class="bg-red-100 p-3 rounded-lg text-red-600 mt-1">
                                        <TrendingUp class="w-6 h-6" />
                                    </div>
                                    <div class="flex-1">
                                        <h4 class="text-lg font-bold text-gray-800 mb-1">Desempenho (Tempo p/ Esgotar)
                                        </h4>
                                        <p class="text-sm text-gray-600 leading-relaxed mb-2">
                                            Mede a eficiência de vendas de um lote que já está <strong
                                                class="text-green-600">Esgotado</strong>.
                                        </p>
                                        <p class="text-sm text-gray-600">
                                            Calcula quantos dias se passaram entre a <strong>primeira venda e a última
                                                venda</strong> que zerou o estoque. Quanto menor esse tempo, maior a
                                            liquidez do produto no período! Se o lote ainda tiver estoque, mostrará a
                                            quantidade restante.
                                        </p>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="bg-white border-t border-gray-200 p-4 md:px-6 flex justify-end shrink-0">
                        <button @click="$emit('close')"
                            class="bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold py-2.5 px-6 rounded-lg transition text-sm">
                            Entendi!
                        </button>
                    </div>

                </div>
            </transition>
        </div>
    </transition>
</template>

<script setup>
import { X, Info, Clock, CalendarDays, TrendingUp } from 'lucide-vue-next'

defineProps({
    isOpen: {
        type: Boolean,
        required: true
    }
})

defineEmits(['close'])
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
    transition: all 0.3s ease cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
}

.custom-scrollbar::-webkit-scrollbar-track {
    background-color: transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #cbd5e1;
    border-radius: 9999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: #94a3b8;
}
</style>
