<template>
    <Teleport to="body">
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[80]"
                style="backdrop-filter: blur(8px); background-color: rgba(0, 0, 0, 0.5);">
            </div>
        </transition>

        <transition name="modal">
            <div v-if="isOpen" class="fixed inset-0 z-[80] flex items-center justify-center p-4 font-montserrat">
                <div class="absolute inset-0" @click="$emit('close')"></div>
                <div
                    class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden relative transform translate-y-14">
                    <!-- Header -->
                    <div class="bg-neutral-900 text-white p-6 relative overflow-hidden">
                        <div
                            class="absolute -right-10 -top-10 bg-neutral-800 w-40 h-40 rounded-full opacity-50 blur-2xl">
                        </div>
                        <div class="relative z-10 flex justify-between items-center">
                            <div>
                                <h2 class="text-2xl font-bold flex items-center gap-2">
                                    <Package class="w-6 h-6 text-red-500" />
                                    FLUXO DE DEVOLUÇÃO
                                </h2>
                                <p class="text-neutral-400 text-sm mt-1">Guia rápido do processo de retorno</p>
                            </div>
                            <button @click="$emit('close')"
                                class="bg-white/10 p-2 rounded-full hover:bg-white/20 transition">
                                <X class="w-5 h-5" />
                            </button>
                        </div>
                    </div>

                    <!-- Content -->
                    <div class="p-8 space-y-8">
                        <!-- Step 1 -->
                        <div class="flex gap-4 relative">
                            <div class="flex flex-col items-center">
                                <div
                                    class="w-10 h-10 rounded-full bg-yellow-100 text-yellow-600 flex items-center justify-center font-bold border-4 border-white shadow-md z-10">
                                    1</div>
                                <div class="w-0.5 h-full bg-gray-100 absolute top-10"></div>
                            </div>
                            <div class="pb-6">
                                <h4 class="font-bold text-gray-800 text-lg flex items-center gap-2">
                                    Registro Inicial <span
                                        class="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full uppercase">Aberto</span>
                                </h4>
                                <p class="text-gray-500 text-sm mt-1 leading-relaxed">
                                    O cliente solicita a devolução. Você registra a quantidade e o motivo.
                                    A mercadoria sai da venda, mas ainda <strong>aguarda chegada física</strong>.
                                </p>
                            </div>
                        </div>

                        <!-- Step 2 -->
                        <div class="flex gap-4 relative">
                            <div class="flex flex-col items-center">
                                <div
                                    class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold border-4 border-white shadow-md z-10">
                                    2</div>
                                <div class="w-0.5 h-full bg-gray-100 absolute top-10"></div>
                            </div>
                            <div class="pb-6">
                                <h4 class="font-bold text-gray-800 text-lg flex items-center gap-2">
                                    Chegada Física <span
                                        class="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full uppercase">Retornada</span>
                                </h4>
                                <p class="text-gray-500 text-sm mt-1 leading-relaxed">
                                    A mercadoria chega na empresa. Você edita a devolução e informa a <strong>Data de
                                        Retorno</strong>.
                                    Isso confirma que o produto está em mãos.
                                </p>
                            </div>
                        </div>

                        <!-- Step 3 -->
                        <div class="flex gap-4">
                            <div class="flex flex-col items-center">
                                <div
                                    class="w-10 h-10 rounded-full bg-green-100 text-green-600 flex items-center justify-center font-bold border-4 border-white shadow-md z-10">
                                    3</div>
                            </div>
                            <div>
                                <h4 class="font-bold text-gray-800 text-lg flex items-center gap-2">
                                    Reintegração (Dar Baixa) <span
                                        class="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full uppercase">Concluída</span>
                                </h4>
                                <p class="text-gray-500 text-sm mt-1 leading-relaxed">
                                    Após conferência, você seleciona um <strong>Novo Lote</strong> de destino (ou cria
                                    um novo).
                                    O estoque é atualizado automaticamente.
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="bg-gray-50 p-4 text-center border-t">
                        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-800 font-bold text-sm">
                            ENTENDI
                        </button>
                    </div>
                </div>
            </div>
        </transition>
    </Teleport>
</template>

<script setup>
import { Package, X } from 'lucide-vue-next'

defineProps({
    isOpen: Boolean
})

defineEmits(['close'])
</script>
