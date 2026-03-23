<template>
    <div>
        <!-- Blur Layer with synchronized transition -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[60]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen"
                class="fixed inset-0 flex items-start justify-center z-[60] font-montserrat pt-[180px] pb-8 px-3 md:px-4">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <!-- Modal Content -->
                    <div v-if="isOpen"
                        class="bg-white rounded-2xl shadow-2xl z-10 w-full max-w-6xl max-h-[calc(100vh-220px)] overflow-hidden flex flex-col text-left">

                        <!-- Header -->
                        <div
                            class="px-4 md:px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-white shrink-0">
                            <div class="flex items-center gap-3 min-w-0">
                                <div class="bg-red-100 p-2 rounded-xl text-red-600 shrink-0">
                                    <Truck class="w-5 h-5 md:w-6 md:h-6" />
                                </div>
                                <div class="min-w-0">
                                    <h2
                                        class="text-base md:text-xl font-bold text-neutral-800 tracking-tight leading-tight">
                                        PEDIDOS DE VENDA (EXPEDIÇÃO)</h2>
                                    <p class="text-xs md:text-sm text-gray-500 font-medium hidden sm:block">
                                        Gerenciamento de pedidos para separação/expedição</p>
                                </div>
                            </div>
                            <button @click="$emit('close')"
                                class="text-gray-400 hover:text-neutral-800 hover:bg-gray-100 p-2 rounded-full transition-colors active:scale-95 shrink-0">
                                <X class="w-5 h-5" />
                            </button>
                        </div>

                        <!-- Toolbar – mobile: coluna; desktop: linha -->
                        <div
                            class="px-4 md:px-6 py-3 md:py-4 bg-gray-50 flex flex-col md:flex-row md:justify-between md:items-center gap-3 border-b border-gray-100 shrink-0">

                            <!-- Filtros + refresh -->
                            <div class="flex items-center gap-2">
                                <button @click="fetchOrders"
                                    class="text-gray-500 hover:text-neutral-800 p-2 rounded-lg hover:bg-gray-200 transition shrink-0"
                                    title="Atualizar lista">
                                    <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': isFetching }" />
                                </button>
                                <div class="flex items-center bg-gray-200 rounded-lg p-1 flex-1 md:flex-none">
                                    <button @click="statusFilter = 'all'"
                                        :class="['flex-1 md:flex-none px-3 md:px-4 py-1.5 rounded-md text-xs md:text-sm font-semibold transition-all', statusFilter === 'all' ? 'bg-white text-neutral-800 shadow-sm' : 'text-gray-500 hover:text-neutral-700']">
                                        TODOS
                                    </button>
                                    <button @click="statusFilter = 'pending'"
                                        :class="['flex-1 md:flex-none px-3 md:px-4 py-1.5 rounded-md text-xs md:text-sm font-semibold transition-all', statusFilter === 'pending' ? 'bg-white text-yellow-600 shadow-sm' : 'text-gray-500 hover:text-neutral-700']">
                                        PEND.
                                    </button>
                                    <button @click="statusFilter = 'separado'"
                                        :class="['flex-1 md:flex-none px-3 md:px-4 py-1.5 rounded-md text-xs md:text-sm font-semibold transition-all', statusFilter === 'separado' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500 hover:text-neutral-700']">
                                        SEP.
                                    </button>
                                    <button @click="statusFilter = 'achieved'"
                                        :class="['flex-1 md:flex-none px-3 md:px-4 py-1.5 rounded-md text-xs md:text-sm font-semibold transition-all', statusFilter === 'achieved' ? 'bg-white text-green-600 shadow-sm' : 'text-gray-500 hover:text-neutral-700']">
                                        CONC.
                                    </button>
                                </div>
                            </div>

                            <!-- Botão Novo Pedido (full-width no mobile) -->
                            <button @click="openCreateModal"
                                class="w-full md:w-auto bg-red-600 hover:bg-red-700 active:scale-95 text-white font-bold h-10 px-6 rounded-lg shadow transition duration-200 flex items-center justify-center gap-2">
                                <Plus class="w-5 h-5" />
                                NOVO PEDIDO
                            </button>
                        </div>

                        <!-- Body / Table + Cards -->
                        <div
                            class="flex-1 overflow-y-auto bg-gray-50 p-3 md:p-6 custom-scrollbar relative min-h-[300px]">
                            <div v-if="isFetching" class="flex justify-center items-center py-12">
                                <LoaderCircle class="animate-spin text-neutral-400 w-10 h-10" />
                            </div>

                            <div v-else-if="orders.length === 0"
                                class="flex flex-col items-center justify-center py-12 text-gray-400">
                                <Truck class="w-16 h-16 mb-4 opacity-50" />
                                <p class="text-lg font-semibold text-gray-500">Nenhum pedido encontrado</p>
                                <p class="text-sm mt-1">Crie um novo pedido para começar</p>
                            </div>

                            <template v-else>

                                <!-- ===== DESKTOP TABLE (md+) ===== -->
                                <div
                                    class="hidden md:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                                    <div
                                        class="grid grid-cols-[60px_2fr_2fr_1fr_100px_120px_160px] gap-3 px-6 py-3 bg-neutral-100 font-bold text-xs text-neutral-600 uppercase">
                                        <div>ID</div>
                                        <div>CLIENTE</div>
                                        <div>LOTES</div>
                                        <div>OBS</div>
                                        <div class="text-center">QUANTIDADE</div>
                                        <div class="text-center">STATUS</div>
                                        <div class="text-center">AÇÕES</div>
                                    </div>

                                    <div class="divide-y divide-gray-100">
                                        <div v-for="order in filteredOrders" :key="order.id">
                                            <!-- Main row -->
                                            <div
                                                class="grid grid-cols-[60px_2fr_2fr_1fr_100px_120px_160px] gap-3 px-6 py-3 items-center hover:bg-gray-50 transition">
                                                <div class="font-bold text-neutral-800">#{{ order.id }}</div>
                                                <div class="text-sm text-neutral-700 truncate font-medium">{{
                                                    order.client_name }}</div>

                                                <!-- Lotes column with expand -->
                                                <div class="flex items-center gap-2 min-w-0">
                                                    <template v-if="order.lotes && order.lotes.length > 0">
                                                        <img v-if="order.lotes[0].product_image"
                                                            :src="order.lotes[0].product_image"
                                                            class="w-6 h-6 rounded-full object-cover border border-gray-200 flex-shrink-0" />
                                                        <div v-else
                                                            class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                                                            <Package size="12" />
                                                        </div>
                                                        <span class="text-sm text-neutral-700 truncate">#{{
                                                            order.lotes[0].num_lote }} - {{ order.lotes[0].product_name
                                                            }}</span>

                                                        <!-- Expand arrow for multiple lotes -->
                                                        <button v-if="order.lotes.length > 1" type="button"
                                                            @click="toggleExpandLotes(order.id)"
                                                            class="flex-shrink-0 flex items-center gap-0.5 text-gray-400 hover:text-red-500 transition p-1 rounded hover:bg-red-50">
                                                            <span class="text-[10px] font-bold">+{{ order.lotes.length -
                                                                1 }}</span>
                                                            <ChevronDown class="w-3.5 h-3.5 transition-transform"
                                                                :class="{ 'rotate-180': expandedOrders.has(order.id) }" />
                                                        </button>
                                                    </template>
                                                    <span v-else class="text-sm text-gray-400 italic">Sem lotes</span>
                                                </div>

                                                <!-- Observação -->
                                                <div class="text-xs text-gray-500 truncate" :title="order.observacao || ''">
                                                    {{ order.observacao || '—' }}
                                                </div>

                                                <div class="text-sm text-neutral-800 font-bold text-center">{{
                                                    order.quant_caixa_solicitada }} {{
                                                        order.lotes?.[0]?.product_name?.toLowerCase().includes('25kg') ?
                                                            'SC' : 'CX' }}
                                                </div>

                                                <div class="flex justify-center">
                                                    <span
                                                        :class="order.achieved ? 'bg-green-100 text-green-700' : order.separado ? 'bg-blue-100 text-blue-700' : 'bg-yellow-100 text-yellow-700'"
                                                        class="px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 justify-center">
                                                        <CheckCircle2 v-if="order.achieved" class="w-3 h-3" />
                                                        <PackageCheck v-else-if="order.separado" class="w-3 h-3" />
                                                        <Clock v-else class="w-3 h-3" />
                                                        {{ order.achieved ? 'CONCLUÍDO' : order.separado ? 'SEPARADO' : 'PENDENTE' }}
                                                    </span>
                                                </div>

                                                <div class="flex items-center justify-center gap-1">
                                                    <!-- Botão VENDER rápido para pedidos com 1 lote (desktop) -->
                                                    <button v-if="!order.achieved && order.lotes?.length === 1 && !order.lotes[0].sold"
                                                        @click="openSaleFromOrder(order, order.lotes[0])"
                                                        class="p-1.5 text-red-600 hover:bg-red-50 rounded transition"
                                                        title="Vender este lote">
                                                        <ShoppingCart class="w-4 h-4" />
                                                    </button>
                                                    <span v-else-if="order.lotes?.length === 1 && order.lotes[0].sold"
                                                        class="flex items-center gap-1 text-green-600 bg-green-50 text-[10px] font-bold px-2 py-1 rounded-md"
                                                        :title="'Venda #' + order.lotes[0].sale_id">
                                                        <CheckCircle2 class="w-3 h-3" />
                                                        #{{ order.lotes[0].sale_id }}
                                                    </span>
                                                    <!-- Botão Toggle Separado (desktop) -->
                                                    <button v-if="!order.achieved"
                                                        @click="toggleSeparado(order)"
                                                        class="p-1.5 rounded transition"
                                                        :class="order.separado ? 'text-blue-600 hover:bg-blue-50' : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'"
                                                        :title="order.separado ? 'Retornar para Pendente' : 'Marcar como Separado'">
                                                        <PackageCheck class="w-4 h-4" />
                                                    </button>
                                                    <button @click="openViewModal(order)"
                                                        class="p-1.5 text-gray-500 hover:text-neutral-800 hover:bg-gray-100 rounded transition"
                                                        title="Visualizar">
                                                        <Eye class="w-4 h-4" />
                                                    </button>
                                                    <button @click="openEditModal(order)"
                                                        class="p-1.5 text-blue-600 hover:bg-blue-50 rounded transition"
                                                        title="Editar">
                                                        <Pencil class="w-4 h-4" />
                                                    </button>
                                                    <button @click="confirmDelete(order)"
                                                        class="p-1.5 text-red-600 hover:bg-red-50 rounded transition"
                                                        title="Excluir">
                                                        <Trash2 class="w-4 h-4" />
                                                    </button>
                                                </div>
                                            </div>

                                            <!-- Expanded lotes panel -->
                                            <transition enter-active-class="transition-all duration-200 ease-out"
                                                enter-from-class="max-h-0 opacity-0"
                                                enter-to-class="max-h-[500px] opacity-100"
                                                leave-active-class="transition-all duration-150 ease-in"
                                                leave-from-class="max-h-[500px] opacity-100"
                                                leave-to-class="max-h-0 opacity-0">
                                                <div v-if="expandedOrders.has(order.id) && order.lotes && order.lotes.length > 1"
                                                    class="bg-gray-50 border-t border-gray-100 overflow-hidden">
                                                    <div class="px-8 py-3 space-y-2">
                                                        <p
                                                            class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">
                                                            Todos os lotes deste pedido</p>
                                                        <div v-for="lote in order.lotes" :key="lote.num_lote"
                                                            class="flex items-center gap-2.5 bg-white border border-gray-200 rounded-lg px-3 py-2">
                                                            <img v-if="lote.product_image" :src="lote.product_image"
                                                                class="w-6 h-6 rounded-full object-cover border border-gray-200 flex-shrink-0" />
                                                            <div v-else
                                                                class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                                                                <Package class="w-3 h-3" />
                                                            </div>
                                                            <span class="text-sm font-medium text-neutral-700">#{{
                                                                lote.num_lote }} - {{ lote.product_name }}</span>
                                                            <span
                                                                class="text-xs text-gray-500 ml-auto flex items-center gap-2">
                                                                <span>Qtd: <span class="font-bold text-neutral-800">{{
                                                                    lote.quantidade }} {{
                                                                        lote.product_name?.toLowerCase().includes('25kg')
                                                                        ? 'sc' : 'cx'
                                                                        }}</span></span>
                                                                <span class="text-gray-300">|</span>
                                                                <span>Estoque: <span class="font-bold"
                                                                        :class="lote.estoque_lote > 0 ? 'text-green-600' : 'text-red-500'">{{
                                                                            lote.estoque_lote }} {{
                                                                            lote.product_name?.toLowerCase().includes('25kg')
                                                                                ? 'sc' : 'cx'
                                                                        }}</span></span>
                                                                <!-- Botão Vender / Check vendido -->
                                                                <button v-if="!lote.sold && !order.achieved"
                                                                    @click.stop="openSaleFromOrder(order, lote)"
                                                                    class="ml-1 flex items-center gap-1 bg-red-600 hover:bg-red-700 text-white text-[10px] font-bold px-2.5 py-1 rounded-md transition active:scale-95"
                                                                    title="Criar venda para este lote">
                                                                    <ShoppingCart class="w-3 h-3" />
                                                                    VENDER
                                                                </button>
                                                                <span v-else-if="lote.sold"
                                                                    class="ml-1 flex items-center gap-1 bg-green-100 text-green-700 text-[10px] font-bold px-2.5 py-1 rounded-md"
                                                                    :title="'Venda #' + lote.sale_id">
                                                                    <CheckCircle2 class="w-3 h-3" />
                                                                    VENDIDO #{{ lote.sale_id }}
                                                                </span>
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </transition>
                                        </div>
                                    </div>
                                </div>

                                <!-- ===== MOBILE CARDS (< md) ===== -->
                                <div class="block md:hidden space-y-3">
                                    <div v-for="order in filteredOrders" :key="order.id"
                                        class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">

                                        <!-- Card Header: ID + Cliente + Status badge -->
                                        <div
                                            class="flex items-start justify-between px-4 pt-4 pb-3 border-b border-gray-100">
                                            <div class="flex-1 min-w-0">
                                                <div class="flex items-center gap-2 flex-wrap mb-1">
                                                    <span class="font-bold text-neutral-800">#{{ order.id }}</span>
                                                    <span
                                                        :class="order.achieved ? 'bg-green-100 text-green-700' : order.separado ? 'bg-blue-100 text-blue-700' : 'bg-yellow-100 text-yellow-700'"
                                                        class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-bold">
                                                        <CheckCircle2 v-if="order.achieved" class="w-3 h-3" />
                                                        <PackageCheck v-else-if="order.separado" class="w-3 h-3" />
                                                        <Clock v-else class="w-3 h-3" />
                                                        {{ order.achieved ? 'CONCLUÍDO' : order.separado ? 'SEPARADO' : 'PENDENTE' }}
                                                    </span>
                                                </div>
                                                <p class="text-sm font-semibold text-neutral-700 truncate">{{
                                                    order.client_name }}</p>
                                            </div>
                                            <!-- Ações rápidas -->
                                            <div class="flex items-center gap-1 shrink-0 ml-2">
                                                <!-- Botão Toggle Separado (mobile) -->
                                                <button v-if="!order.achieved"
                                                    @click="toggleSeparado(order)"
                                                    class="p-2 rounded-lg transition"
                                                    :class="order.separado ? 'text-blue-600 hover:bg-blue-50' : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'"
                                                    :title="order.separado ? 'Retornar para Pendente' : 'Marcar como Separado'">
                                                    <PackageCheck class="w-4 h-4" />
                                                </button>
                                                <button @click="openViewModal(order)"
                                                    class="p-2 text-gray-500 hover:text-neutral-800 hover:bg-gray-100 rounded-lg transition"
                                                    title="Visualizar">
                                                    <Eye class="w-4 h-4" />
                                                </button>
                                                <button @click="openEditModal(order)"
                                                    class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                                                    title="Editar">
                                                    <Pencil class="w-4 h-4" />
                                                </button>
                                                <button @click="confirmDelete(order)"
                                                    class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                                                    title="Excluir">
                                                    <Trash2 class="w-4 h-4" />
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Card Body: Lotes + Caixas + Status action -->
                                        <div class="px-4 py-3 space-y-2">
                                            <!-- Lotes -->
                                            <div>
                                                <p
                                                    class="text-[10px] font-bold text-gray-400 uppercase tracking-wide mb-1.5">
                                                    Lotes</p>
                                                <div v-if="order.lotes && order.lotes.length > 0" class="space-y-1.5">
                                                    <!-- Primeiro lote sempre visível -->
                                                    <div
                                                        class="flex items-center gap-2 bg-gray-50 rounded-lg px-3 py-2">
                                                        <img v-if="order.lotes[0].product_image"
                                                            :src="order.lotes[0].product_image"
                                                            class="w-6 h-6 rounded-full object-cover border border-gray-200 flex-shrink-0" />
                                                        <div v-else
                                                            class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                                                            <Package size="12" />
                                                        </div>
                                                        <span class="text-sm text-neutral-700 truncate">#{{
                                                            order.lotes[0].num_lote }} - {{
                                                                order.lotes[0].product_name }}</span>
                                                    </div>
                                                    <!-- Lotes adicionais expansíveis -->
                                                    <template v-if="order.lotes.length > 1">
                                                        <transition
                                                            enter-active-class="transition-all duration-200 ease-out"
                                                            enter-from-class="max-h-0 opacity-0"
                                                            enter-to-class="max-h-[400px] opacity-100"
                                                            leave-active-class="transition-all duration-150 ease-in"
                                                            leave-from-class="max-h-[400px] opacity-100"
                                                            leave-to-class="max-h-0 opacity-0">
                                                            <div v-if="expandedOrders.has(order.id)"
                                                                class="space-y-1.5 overflow-hidden">
                                                                <div v-for="lote in order.lotes.slice(1)"
                                                                    :key="lote.num_lote"
                                                                    class="flex items-center gap-2 bg-gray-50 rounded-lg px-3 py-2">
                                                                    <img v-if="lote.product_image"
                                                                        :src="lote.product_image"
                                                                        class="w-6 h-6 rounded-full object-cover border border-gray-200 flex-shrink-0" />
                                                                    <div v-else
                                                                        class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                                                                        <Package size="12" />
                                                                    </div>
                                                                    <span class="text-sm text-neutral-700 truncate">#{{
                                                                        lote.num_lote }} - {{ lote.product_name
                                                                        }}</span>
                                                                    <span
                                                                        class="text-xs text-gray-500 ml-auto flex items-center gap-2 shrink-0">
                                                                        <span>Qtd: <span
                                                                                class="font-bold text-neutral-800">{{
                                                                                    lote.quantidade }} {{
                                                                                    lote.product_name?.toLowerCase().includes('25kg')
                                                                                        ? 'sc' : 'cx' }}</span></span>
                                                                        <span class="text-gray-300">|</span>
                                                                        <span>Estoque: <span class="font-bold"
                                                                                :class="lote.estoque_lote > 0 ? 'text-green-600' : 'text-red-500'">{{
                                                                                    lote.estoque_lote }} {{
                                                                                    lote.product_name?.toLowerCase().includes('25kg')
                                                                                        ? 'sc' : 'cx' }}</span></span>
                                                                    </span>
                                                                    <!-- Botão Vender / Check vendido (mobile) -->
                                                                    <button v-if="!lote.sold && !order.achieved"
                                                                        @click.stop="openSaleFromOrder(order, lote)"
                                                                        class="flex items-center gap-1 bg-red-600 hover:bg-red-700 text-white text-[10px] font-bold px-2 py-1 rounded-md transition active:scale-95 shrink-0"
                                                                        title="Criar venda">
                                                                        <ShoppingCart class="w-3 h-3" />
                                                                        VENDER
                                                                    </button>
                                                                    <span v-else-if="lote.sold"
                                                                        class="flex items-center gap-1 bg-green-100 text-green-700 text-[10px] font-bold px-2 py-1 rounded-md shrink-0">
                                                                        <CheckCircle2 class="w-3 h-3" />
                                                                        VENDIDO #{{ lote.sale_id }}
                                                                    </span>
                                                                </div>
                                                            </div>
                                                        </transition>
                                                        <button @click="toggleExpandLotes(order.id)"
                                                            class="w-full flex items-center justify-center gap-1 text-xs font-semibold text-red-600 hover:text-red-700 py-1 transition">
                                                            <ChevronDown class="w-3.5 h-3.5 transition-transform"
                                                                :class="{ 'rotate-180': expandedOrders.has(order.id) }" />
                                                            {{ expandedOrders.has(order.id) ? 'Ver menos' :
                                                                `+${order.lotes.length - 1} lote(s)` }}
                                                        </button>
                                                    </template>
                                                </div>
                                                <p v-else class="text-sm text-gray-400 italic">Sem lotes</p>
                                            </div>

                                            <!-- Caixas + Status -->
                                            <div
                                                class="flex items-center justify-between pt-2 border-t border-gray-100">
                                                <div class="flex items-center gap-1.5">
                                                    <span
                                                        class="text-xs font-semibold text-gray-500 uppercase">Qtd:</span>
                                                    <span class="text-sm font-bold text-neutral-800">{{
                                                        order.quant_caixa_solicitada }} {{
                                                            order.lotes?.[0]?.product_name?.toLowerCase().includes('25kg') ?
                                                                'SC' : 'CX' }}</span>
                                                </div>
                                                <!-- Botão vender o primeiro lote (quando só tem 1 lote) -->
                                                <button v-if="!order.achieved && order.lotes?.length === 1 && !order.lotes[0].sold"
                                                    @click="openSaleFromOrder(order, order.lotes[0])"
                                                    class="flex items-center gap-1.5 bg-red-600 hover:bg-red-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition active:scale-95">
                                                    <ShoppingCart class="w-3.5 h-3.5" />
                                                    VENDER
                                                </button>
                                                <span v-else-if="order.lotes?.length === 1 && order.lotes[0].sold"
                                                    class="flex items-center gap-1 bg-green-100 text-green-700 text-[10px] font-bold px-2.5 py-1 rounded-md">
                                                    <CheckCircle2 class="w-3 h-3" />
                                                    VENDIDO #{{ order.lotes[0].sale_id }}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </template>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>

        <OrderFormModal :isOpen="isFormModalOpen" :order="selectedOrder" :isEdit="!!selectedOrder" @close="isFormModalOpen = false"
            @saved="fetchOrders" />

        <OrderViewModal :isOpen="isViewModalOpen" :order="viewOrder" @close="isViewModalOpen = false" />

        <OrderDeleteModal :isOpen="!!orderToDelete" :itemName="orderToDelete?.id" :loading="isDeleting"
            @close="orderToDelete = null" @confirm="executeDelete" />

        <!-- Modal de Venda (Método A: aberto a partir de um lote da expedição) -->
        <SalesFormModal :isOpen="isSaleModalOpen" :prefilledData="salePrefilledData"
            @close="isSaleModalOpen = false" @save="onSaleSaved" />

        <!-- Modal de Confirmação Toggle Separado -->
        <OrderSeparadoConfirmModal :isOpen="!!orderToToggleSeparado" :order="orderToToggleSeparado"
            :isToggling="isTogglingSeparado" @close="orderToToggleSeparado = null"
            @confirm="executeSeparadoToggle" />
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { X, Truck, Plus, RefreshCw, LoaderCircle, Package, Pencil, Trash2, CheckCircle2, Clock, ChevronDown, Eye, ShoppingCart, PackageCheck } from 'lucide-vue-next'
import { useUserStore } from '../../stores/user'
import { useToastStore } from '../../stores/toast'
import OrderFormModal from './OrderFormModal.vue'
import OrderViewModal from './OrderViewModal.vue'
import OrderDeleteModal from './OrderDeleteModal.vue'
import OrderSeparadoConfirmModal from './OrderSeparadoConfirmModal.vue'
import SalesFormModal from '../sales/SalesFormModal.vue'

const props = defineProps({
    isOpen: Boolean
})

const emit = defineEmits(['close', 'sale-saved'])

const userStore = useUserStore()
const toastStore = useToastStore()

const isFetching = ref(false)
const orders = ref([])
const isFormModalOpen = ref(false)
const selectedOrder = ref(null)

const isViewModalOpen = ref(false)
const viewOrder = ref(null)

const statusFilter = ref('all')

const orderToDelete = ref(null)
const isDeleting = ref(false)

// Estado para abrir modal de venda (Método A)
const isSaleModalOpen = ref(false)
const salePrefilledData = ref(null)

// Estado para modal de confirmação toggle separado
const orderToToggleSeparado = ref(null)
const isTogglingSeparado = ref(false)

// Track which orders have their lotes expanded
const expandedOrders = reactive(new Set())

const filteredOrders = computed(() => {
    if (statusFilter.value === 'all') return orders.value
    if (statusFilter.value === 'achieved') return orders.value.filter(o => o.achieved)
    if (statusFilter.value === 'separado') return orders.value.filter(o => !o.achieved && o.separado)
    // pending = not achieved AND not separado
    return orders.value.filter(o => !o.achieved && !o.separado)
})

function toggleExpandLotes(orderId) {
    if (expandedOrders.has(orderId)) {
        expandedOrders.delete(orderId)
    } else {
        expandedOrders.add(orderId)
    }
}

const toggleSeparado = (order) => {
    if (!userStore.user?.is_master) {
        toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários master podem alterar o status de separação.', type: 'error' })
        return
    }
    orderToToggleSeparado.value = order
}

const executeSeparadoToggle = async () => {
    if (!orderToToggleSeparado.value) return
    isTogglingSeparado.value = true
    const order = orderToToggleSeparado.value
    try {
        const response = await fetch(`/api/orders/${order.id}/toggle-separado`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${userStore.token}`
            }
        })
        if (response.ok) {
            const data = await response.json()
            order.separado = data.separado
            toastStore.add({ title: 'Sucesso', message: data.message, type: 'success' })
            orderToToggleSeparado.value = null
        } else {
            const err = await response.json()
            toastStore.add({ title: 'Erro', message: err.error || 'Falha ao alterar status.', type: 'error' })
        }
    } catch (e) {
        console.error(e)
        toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
    } finally {
        isTogglingSeparado.value = false
    }
}

const fetchOrders = async () => {
    if (!props.isOpen) return
    isFetching.value = true
    try {
        const response = await fetch('/api/orders', {
            headers: {
                'Authorization': `Bearer ${userStore.token}`
            }
        })
        if (response.ok) {
            let data = await response.json()
            orders.value = data
        } else {
            toastStore.add({ title: 'Erro', message: 'Falha ao buscar pedidos', type: 'error' })
        }
    } catch (e) {
        console.error(e)
        toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
    } finally {
        isFetching.value = false
    }
}

watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        expandedOrders.clear()
        fetchOrders()
    }
})

const openCreateModal = () => {
    if (!userStore.user?.is_master) {
        toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem criar pedidos.', type: 'error' })
        return
    }
    selectedOrder.value = null
    isFormModalOpen.value = true
}

const openEditModal = (order) => {
    if (!userStore.user?.is_master) {
        toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem editar pedidos.', type: 'error' })
        return
    }
    selectedOrder.value = order
    isFormModalOpen.value = true
}

const openViewModal = (order) => {
    viewOrder.value = order
    isViewModalOpen.value = true
}

// Método A: Abrir modal de venda a partir de um lote da expedição
const openSaleFromOrder = (order, lote) => {
    salePrefilledData.value = {
        num_lote: lote.num_lote,
        product_id: null, // será preenchido pelo SalesFormModal via consulta de produções
        client_id: order.client_id,
        quant_caixa_vendida: lote.quantidade,
        order_product_id: lote.id  // ID do OrderProduct para vincular
    }
    isSaleModalOpen.value = true
}

// Callback quando venda vinculada é salva
const onSaleSaved = () => {
    isSaleModalOpen.value = false
    salePrefilledData.value = null
    fetchOrders() // Recarrega para atualizar os checks
    emit('sale-saved') // Propaga para o SaleView atualizar a tabela de vendas
}

const confirmDelete = (order) => {
    if (!userStore.user?.is_master) {
        toastStore.add({ title: 'Acesso Negado', message: 'Somente usuários com permissão podem excluir pedidos.', type: 'error' })
        return
    }
    orderToDelete.value = order
}

const executeDelete = async () => {
    if (!orderToDelete.value) return
    isDeleting.value = true
    const order = orderToDelete.value

    try {
        const response = await fetch(`/api/orders/${order.id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${userStore.token}`
            }
        })

        if (response.ok) {
            toastStore.add({ title: 'Sucesso', message: 'Pedido excluído', type: 'success' })
            fetchOrders()
            orderToDelete.value = null
        } else {
            toastStore.add({ title: 'Erro', message: 'Falha ao excluir.', type: 'error' })
        }
    } catch (e) {
        console.error(e)
    } finally {
        isDeleting.value = false
    }
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

.custom-scrollbar::-webkit-scrollbar-track {
    background-color: transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #d1d5db;
    border-radius: 9999px;
}
</style>
