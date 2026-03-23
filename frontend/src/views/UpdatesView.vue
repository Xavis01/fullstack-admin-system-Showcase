<template>
    <div class="min-h-screen bg-gray-200 font-montserrat">
        <section id="updates">
            <div class="max-w-4xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
                <!-- Header -->
                <div class="flex items-center gap-2 md:gap-4 mb-6 md:mb-8">
                    <button @click="router.back()"
                        class="bg-white p-2 rounded-xl shadow hover:bg-gray-50 active:scale-95 transition text-neutral-600">
                        <ArrowLeft class="w-5 h-5 md:w-6 md:h-6" />
                    </button>
                    <h2 class="text-xl sm:text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">
                        Atualizações do Sistema
                    </h2>
                </div>

                <!-- Updates List -->
                <div class="space-y-4 md:space-y-6">

                    <!------------------------------------------------------------------------- EM BREVE ------------------------------------------------------------------>
                    <!--
                    <div
                        class="animate-fade-in bg-red-50 text-neutral-800 rounded-2xl p-4 sm:p-5 md:p-6 shadow-md border border-red-100 relative overflow-hidden">
                        <div class="absolute top-0 right-0 p-4 md:p-6 opacity-5">
                            <Rocket class="text-red-600 w-16 h-16 md:w-24 md:h-24" />
                        </div>
                        <div class="relative z-10">
                            <div class="flex items-center gap-2 md:gap-3 mb-3 md:mb-4">
                                <div class="bg-red-100 p-1.5 md:p-2 rounded-lg">
                                    <Rocket class="text-red-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-lg md:text-xl font-bold text-red-900">Em breve - Versão 1.5.1</h3>
                            </div>
                            <p class="text-red-800 mb-4 font-medium">Novidades que estamos preparando para você:</p>
                            <ul class="space-y-2 md:space-y-3">
                                <li class="flex items-start gap-2 md:gap-3 text-gray-700">
                                    <Hourglass class="w-4 h-4 md:w-5 md:h-5 text-red-400 flex-shrink-0 mt-0.5" />
                                    <span class="text-sm md:text-base">Página com todos os procedimentos da JRS
                                        (Produção, qualidade, administrativo)</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                    -->
                    <!---------------------------------------------------------------------------------------------------------------------------------------------------->




                    <!---------------------------------------------------------------- ATUALIZAÇÃO ATUAL ----------------------------------------------------------------->
                    <div
                        class="animate-fade-in animation-delay-150 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg border-l-4 border-red-600">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-red-100 p-1.5 md:p-2 rounded-lg">
                                    <Sparkles class="text-red-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-lg md:text-xl font-bold text-neutral-800">Versão 1.5.3</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">20/03/2026</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-700">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-green-500 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Novo status de "Separado", clique em <PackageCheck class="inline w-5 h-5 text-blue-600 mx-1 -mt-1"/> na aba de expedições</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-700">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-green-500 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Na mesma aba, agora temos "Observação", onde você pode adicionar informações sobre o pedido, na hora de criar o pedido, ou clicando em <Pencil class="inline w-5 h-5 text-blue-600 mx-1 -mt-1"/></span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-700">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-green-500 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Correção de bugs</span>
                            </li>
                        </ul>
                    </div>

                    <!---------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ----------------------------------------------------------------->
                    <div
                        class="animate-fade-in animation-delay-150 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.5.2</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">16/03/2026</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Fluxo de Expedição e Venda atualizados</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Agora é possível fazer Vendas a partir dos pedidos de Expedição, onde ficam vinculados</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Nova página de Movimentações, clicando em <ScrollText class="inline w-5 h-5 text-red-600 mx-1 -mt-1"/> na página inicial</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Página de Login reestilizada!</span>
                            </li>
                        </ul>
                    </div>
                    <!-------------------------------------------------------------------------------------------------------------------------------------------------->


                    <!----------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ------------------------------------------------------------->
                    <div
                        class="animate-fade-in animation-delay-300 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.5.1</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">10/03/2026</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Nova página de procedimentos da JRS, clicando em <FolderOpen class="inline w-5 h-5 text-red-600 mx-1 -mt-1"/> na página inicial</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Cadastre e gerencie arquivos nessa nova página!</span>
                            </li>
                        </ul>
                    </div>
                    <!-------------------------------------------------------------------------------------------------------------------------------------------------->


                    <!----------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ------------------------------------------------------------->

                    <div
                        class="animate-fade-in animation-delay-300 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.5</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">04/03/2026</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Aba de Expedição na página de “Vendas" pra controle
                                    de Pedidos</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Aba de gerar relatórios na página de
                                    "Dashboard"</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Aba para visualização de datas dos lotes na página de
                                    "Dashboard"</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Algumas telas Mobile atualizadas!</span>
                            </li>
                        </ul>
                    </div>
                    <!-------------------------------------------------------------------------------------------------------------------------------------------------->


                    <!----------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ------------------------------------------------------------->

                    <div
                        class="animate-fade-in animation-delay-300 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.4</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">09/02/2026</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Visualização individual das vendas de cada
                                    cliente</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">
                                    Novo sistema completo de Devoluções na página de Vendas
                                    <button @click="isInstructionsOpen = true"
                                        class="text-red-600 underline hover:text-red-800 font-bold ml-1">
                                        (clique aqui para saber mais)
                                    </button>
                                </span>
                            </li>
                        </ul>
                    </div>


                    <!----------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ------------------------------------------------------------->

                    <div
                        class="animate-fade-in animation-delay-300 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.3</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">26/01/2026</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Todas as páginas agora são responsivas para celulares
                                    e tablets (mobile)</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Gerencie o sistema de qualquer lugar!</span>
                            </li>
                        </ul>
                    </div>
                    <!-------------------------------------------------------------------------------------------------------------------------------------------------->




                    <!----------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ------------------------------------------------------------->

                    <div
                        class="animate-fade-in animation-delay-300 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.2</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">09/01/2026</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Aba de Metas adicionada na página Dashboard!</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Crie e gerencie Metas de produção fácilmente</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Visualize Metas atingidas, concluidas, em
                                    andamento...</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Simples visualização com filtros, e opções de
                                    bloquear, editar e excluir Metas</span>
                            </li>

                        </ul>
                    </div>


                    <!----------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ------------------------------------------------------------->
                    <div
                        class="animate-fade-in animation-delay-300 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.1</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">17/12/2025</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Página de "Atualizações do sistema" criada</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Adicionado filtro por clientes no Dashboard</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Melhoria no layout da barra de navegação</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Teste passar o mouse por cima do seu nome!</span>
                            </li>

                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Animações adicionadas nas páginas</span>
                            </li>

                        </ul>
                    </div>

                    <!----------------------------------------------------------------- ATUALIZAÇÃO ANTIGA ------------------------------------------------------------->

                    <div
                        class="animate-fade-in animation-delay-300 bg-white rounded-2xl p-4 sm:p-5 md:p-6 shadow-lg opacity-80 hover:opacity-100 transition">
                        <div class="flex justify-between items-start mb-3 md:mb-4 gap-2">
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="bg-gray-100 p-1.5 md:p-2 rounded-lg">
                                    <Wrench class="text-gray-600 w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <h3 class="text-base md:text-lg font-bold text-neutral-700">Versão 1.0</h3>
                            </div>
                            <span class="text-xs md:text-sm font-semibold text-gray-500">15/12/2025</span>
                        </div>
                        <ul class="space-y-2 md:space-y-3">
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Lançamento oficial do Sistema Administrativo</span>
                            </li>
                            <li class="flex items-start gap-2 md:gap-3 text-gray-600">
                                <CheckCircle2 class="w-4 h-4 md:w-5 md:h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                                <span class="text-sm md:text-base">Todas as funções funcionando</span>
                            </li>
                        </ul>
                    </div>
                    <!-------------------------------------------------------------------------------------------------------------------------------------------------->

                </div>
            </div>
        </section>

        <!-- Instructions Modal -->
        <ReturnInstructionsModal :isOpen="isInstructionsOpen" @close="isInstructionsOpen = false" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Sparkles, CheckCircle2, Wrench, ScrollText, Rocket, Hourglass, FolderOpen, PackageCheck, Pencil } from 'lucide-vue-next'
import ReturnInstructionsModal from '../components/returns/ReturnInstructionsModal.vue'

const router = useRouter()
const isInstructionsOpen = ref(false)
</script>

<style scoped>
/* Gradient Text for Header if needed, currently using neutral-800 */
</style>
