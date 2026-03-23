<template>
    <div id="background" class="min-h-screen bg-gray-200 font-montserrat">
        <section id="home">
            <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">
                <!-- Header with Date -->
                <div
                    class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 md:mb-10 gap-3 md:gap-4">
                    <div class="flex items-center gap-2 md:gap-4">
                        <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
                            <House class="text-white w-6 h-6 md:w-8 md:h-8" />
                        </div>
                        <div>
                            <h2 class="text-2xl md:text-4xl font-extrabold text-neutral-800 uppercase tracking-tight">
                                Bem-Vindo, {{
                                    userFirstName
                                }}</h2>
                            <p class="text-neutral-500 mt-1 text-sm md:text-lg">Selecione um módulo para começar</p>
                        </div>
                    </div>
                    <div class="items-center gap-4 text-right hidden md:flex">
                        <!-- Admin Button (ID=1 only) -->
                        <button v-if="userStore.user && userStore.user.id === 1" @click="router.push('/admin')"
                            class="bg-red-600 hover:bg-red-700 text-white p-3 rounded-xl shadow-lg transition-transform hover:scale-105"
                            title="Gerenciar Administradores">
                            <ShieldUser class="w-6 h-6" />
                        </button>

                        <!-- Stock History Button (Always visible) -->
                        <button @click="router.push('/stock-history')"
                            class="bg-white hover:bg-gray-50 text-red-600 p-3 rounded-xl shadow-lg transition-transform hover:scale-105"
                            title="Movimentações de Estoque">
                            <ScrollText class="w-6 h-6" />
                        </button>

                        <!-- Procedimentos Button (Always visible) -->
                        <button @click="router.push('/procedures')"
                            class="bg-white hover:bg-gray-50 text-red-600 p-3 rounded-xl shadow-lg transition-transform hover:scale-105"
                            title="Procedimentos">
                            <FolderOpen class="w-6 h-6" />
                        </button>

                        <!-- Mail Button (Always visible) -->
                        <a href="https://mail.sodaescorpiao.com.br:2096" target="_blank"
                            class="bg-white hover:bg-gray-50 text-red-600 p-3 rounded-xl shadow-lg transition-transform hover:scale-105"
                            title="Webmail">
                            <Mail class="w-6 h-6" />
                        </a>

                        <!-- Updates Button (Always visible) -->
                        <button @click="router.push('/updates')"
                            class="bg-white hover:bg-gray-50 text-red-600 p-3 rounded-xl shadow-lg transition-transform hover:scale-105"
                            title="Atualizações do Sistema">
                            <Sparkles class="w-6 h-6" />
                        </button>

                        <div>
                            <p class="text-3xl font-bold text-red-600">{{ currentDate }}</p>
                            <p class="text-neutral-500 uppercase font-semibold tracking-wider">{{ currentDay }}</p>
                        </div>
                    </div>
                </div>

                <!-- Mobile Actions -->
                <div class="flex md:hidden items-center justify-between mb-6 gap-3">
                    <div class="flex items-center gap-2">
                        <button v-if="userStore.user && userStore.user.id === 1" @click="router.push('/admin')"
                            class="bg-red-600 hover:bg-red-700 text-white p-2.5 rounded-xl shadow-lg transition-transform active:scale-95"
                            title="Gerenciar Administradores">
                            <ShieldUser class="w-5 h-5" />
                        </button>

                        <a href="http://mail.sodaescorpiao.com.br:2096" target="_blank"
                            class="bg-white hover:bg-gray-50 text-red-600 p-2.5 rounded-xl shadow-lg transition-transform active:scale-95"
                            title="Webmail">
                            <Mail class="w-5 h-5" />
                        </a>

                        <!-- Stock History Button Mobile -->
                        <button @click="router.push('/stock-history')"
                            class="bg-white hover:bg-gray-50 text-red-600 p-2.5 rounded-xl shadow-lg transition-transform active:scale-95"
                            title="Movimentações de Estoque">
                            <ScrollText class="w-5 h-5" />
                        </button>

                        <!-- Procedimentos Button Mobile -->
                        <button @click="router.push('/procedures')"
                            class="bg-white hover:bg-gray-50 text-red-600 p-2.5 rounded-xl shadow-lg transition-transform active:scale-95"
                            title="Procedimentos">
                            <FolderOpen class="w-5 h-5" />
                        </button>

                        <button @click="router.push('/updates')"
                            class="bg-white hover:bg-gray-50 text-red-600 p-2.5 rounded-xl shadow-lg transition-transform active:scale-95"
                            title="Atualizações do Sistema">
                            <Sparkles class="w-5 h-5" />
                        </button>
                    </div>
                    <div class="text-right">
                        <p class="text-lg font-bold text-red-600">{{ currentDate }}</p>
                        <p class="text-xs text-neutral-500 uppercase font-semibold tracking-wider">{{ currentDay }}</p>
                    </div>
                </div>

                <!-- Bento Grid -->
                <!-- Bento Grid -->
                <div
                    class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 md:gap-6 auto-rows-[180px] sm:auto-rows-[200px] md:auto-rows-[200px]">

                    <!-- 1. Produção (Desktop: top-left 2x2 | Mobile Order: 1) -->
                    <div @click="router.push('/production')"
                        class="order-1 md:order-none animate-fade-in group relative bg-[#1a1a1a] rounded-3xl p-4 md:p-6 cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-red-900/20 sm:col-span-2 md:col-span-2 md:row-span-2 border border-neutral-800 hover:border-red-600">
                        <div
                            class="absolute top-0 right-0 p-4 md:p-6 opacity-20 group-hover:opacity-10 transition-opacity duration-300">
                            <Boxes :size="windowWidth < 768 ? 100 : 180" class="text-neutral-500" />
                        </div>
                        <div class="flex flex-col h-full justify-between relative z-10">
                            <div class="bg-red-600/20 w-fit p-2 md:p-3 rounded-2xl">
                                <Boxes class="text-red-500 w-6 h-6 md:w-8 md:h-8" />
                            </div>
                            <div>
                                <div class="flex justify-between items-center mb-2">
                                    <h3 class="text-xl md:text-3xl font-bold text-white">Produção</h3>
                                    <div
                                        class="opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-4 group-hover:translate-x-0">
                                        <ArrowRight class="text-red-500 w-6 h-6 md:w-8 md:h-8" />
                                    </div>
                                </div>
                                <p class="text-sm md:text-base text-gray-400">Gerencie a entrada de estoque, controle de
                                    lotes e processos
                                    produtivos.</p>
                            </div>
                        </div>
                    </div>

                    <!-- 2. Clientes (Desktop: top-right | Mobile Order: 4) -->
                    <div @click="router.push('/client')"
                        class="order-4 md:order-none animate-fade-in animation-delay-300 md:animation-delay-100 group relative bg-[#1a1a1a] rounded-3xl p-4 md:p-6 cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-red-900/20 border border-neutral-800 hover:border-red-600">
                        <div class="absolute -bottom-4 -right-4 opacity-20 group-hover:opacity-10 transition-opacity">
                            <Users :size="windowWidth < 768 ? 80 : 120" class="text-neutral-500" />
                        </div>
                        <div class="flex flex-col h-full justify-between relative z-10">
                            <div class="bg-red-600/20 w-fit p-2 md:p-3 rounded-2xl">
                                <Users class="text-red-500 w-6 h-6" />
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-white">Clientes</h3>
                                <p class="text-sm text-gray-400 mt-1">Base de clientes</p>
                            </div>
                        </div>
                    </div>

                    <!-- 3. Produtos (Desktop: top-right | Mobile Order: 5) -->
                    <div @click="router.push('/product')"
                        class="order-5 md:order-none animate-fade-in animation-delay-400 md:animation-delay-150 group relative bg-[#1a1a1a] rounded-3xl p-4 md:p-6 cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-red-900/20 border border-neutral-800 hover:border-red-600">
                        <div class="absolute -bottom-4 -right-4 opacity-20 group-hover:opacity-10 transition-opacity">
                            <Package :size="windowWidth < 768 ? 80 : 120" class="text-neutral-500" />
                        </div>
                        <div class="flex flex-col h-full justify-between relative z-10">
                            <div class="bg-red-600/20 w-fit p-2 md:p-3 rounded-2xl">
                                <Package class="text-red-500 w-6 h-6" />
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-white">Produtos</h3>
                                <p class="text-sm text-gray-400 mt-1">Catálogo e Estoque</p>
                            </div>
                        </div>
                    </div>

                    <!-- 4. Vendas (Desktop: right 2x2 | Mobile Order: 2) -->
                    <div @click="router.push('/sale')"
                        class="order-2 md:order-none animate-fade-in animation-delay-100 md:animation-delay-200 group relative bg-[#1a1a1a] rounded-3xl p-4 md:p-6 cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-red-900/20 sm:col-span-2 md:col-span-2 md:row-span-2 border border-neutral-800 hover:border-red-600">
                        <div
                            class="absolute top-0 right-0 p-4 md:p-6 opacity-20 group-hover:opacity-10 transition-opacity duration-300">
                            <ShoppingCart :size="windowWidth < 768 ? 100 : 180" class="text-neutral-500" />
                        </div>
                        <div class="flex flex-col h-full justify-between relative z-10">
                            <div class="bg-red-600/20 w-fit p-2 md:p-3 rounded-2xl">
                                <ShoppingCart class="text-red-500 w-6 h-6 md:w-8 md:h-8" />
                            </div>
                            <div>
                                <div class="flex justify-between items-center mb-2">
                                    <h3 class="text-xl md:text-3xl font-bold text-white">Vendas</h3>
                                    <div
                                        class="opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-4 group-hover:translate-x-0">
                                        <ArrowRight class="text-red-500 w-6 h-6 md:w-8 md:h-8" />
                                    </div>
                                </div>
                                <p class="text-sm md:text-base text-gray-400">Registre saídas, controle o faturamento e
                                    visualize histórico
                                    de vendas.</p>
                            </div>
                        </div>
                    </div>

                    <!-- 5. Dashboard (Desktop: bottom-left | Mobile Order: 3) -->
                    <div @click="router.push('/dashboard')"
                        class="order-3 md:order-none animate-fade-in animation-delay-200 md:animation-delay-300 group relative bg-[#1a1a1a] rounded-3xl p-4 md:p-6 cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-red-900/20 border border-neutral-800 hover:border-red-600">
                        <div class="absolute -bottom-4 -right-4 opacity-20 group-hover:opacity-10 transition-opacity">
                            <ChartColumn :size="windowWidth < 768 ? 80 : 120" class="text-neutral-500" />
                        </div>
                        <div class="flex flex-col h-full justify-between relative z-10">
                            <div class="bg-red-600/20 w-fit p-2 md:p-3 rounded-2xl">
                                <ChartColumn class="text-red-500 w-6 h-6" />
                            </div>
                            <div>
                                <h3 class="text-xl font-bold text-white">Dashboard</h3>
                                <p class="text-sm text-gray-400 mt-1">Visão Geral</p>
                            </div>
                        </div>
                    </div>

                    <!-- 6. Site Institucional (Desktop: bottom-left | Mobile Order: 6) -->
                    <a href="https://sodaescorpiao.com.br" target="_blank"
                        class="order-6 md:order-none animate-fade-in animation-delay-500 md:animation-delay-300 group relative bg-gradient-to-br from-red-600 to-red-800 rounded-3xl p-4 md:p-6 cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-red-900/40 md:col-span-1 border border-red-500">
                        <div
                            class="absolute top-0 right-0 p-3 md:p-4 opacity-30 group-hover:opacity-100 transition-all duration-300 transform group-hover:scale-110">
                            <ExternalLink class="text-white w-8 h-8 md:w-12 md:h-12" />
                        </div>
                        <div class="flex flex-col h-full justify-between relative z-10 text-white">
                            <Globe class="w-6 h-6 md:w-8 md:h-8" />
                            <div>
                                <h3 class="text-lg font-bold">Site Institucional</h3>
                                <p class="text-xs text-red-100 mt-1">sodaescorpiao.com.br</p>
                            </div>
                        </div>
                    </a>

                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { Users, Package, ShoppingCart, Boxes, ChartColumn, ExternalLink, Globe, ArrowRight, House, ShieldUser, Sparkles, Mail, FolderOpen, ScrollText } from 'lucide-vue-next'

const userStore = useUserStore()
const router = useRouter()

// Ensure valid session
userStore.ensureValidSession(router)

const userFirstName = computed(() => {
    if (userStore.user && userStore.user.primeiro_nome) return userStore.user.primeiro_nome
    if (userStore.user && userStore.user.nome) return userStore.user.nome.split(' ')[0]
    return 'Usuário'
})

const currentDate = ref('')
const currentDay = ref('')
const windowWidth = ref(window.innerWidth)

const updateDate = () => {
    const now = new Date()
    // Manual formatting for Portuguese
    const days = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

    currentDate.value = now.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' }) // 13/12/2025
    currentDay.value = days[now.getDay()]
}

const updateWindowWidth = () => {
    windowWidth.value = window.innerWidth
}

onMounted(() => {
    updateDate()
    window.addEventListener('resize', updateWindowWidth)
})

onUnmounted(() => {
    window.removeEventListener('resize', updateWindowWidth)
})
</script>

<style scoped>
/* Gradient Text for Header if needed, currently using neutral-800 */
</style>
