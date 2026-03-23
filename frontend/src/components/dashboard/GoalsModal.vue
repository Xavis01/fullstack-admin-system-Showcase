<template>
    <div>
        <!-- Blur Layer with synchronized transition -->
        <transition name="modal-backdrop">
            <!-- Blur Backdrop (Pure Blur) -->
            <div v-if="isOpen" class="fixed inset-0 z-40 pointer-events-none"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen"
                class="fixed inset-0 z-50 flex justify-center items-start p-3 sm:p-4 pt-20 sm:pt-24 md:pt-44 pb-6 sm:pb-8 md:pb-12 font-montserrat">

                <!-- Dark Overlay -->
                <div class="absolute inset-0 bg-black/50 transition-opacity" @click="$emit('close')"></div>

                <!-- Modal Content -->
                <transition name="modal">
                    <div v-if="isOpen" ref="modalContentRef"
                        class="pointer-events-auto w-full max-w-4xl flex flex-col max-h-full bg-white rounded-xl shadow-2xl relative z-10 transition-all duration-500 ease-in-out overflow-hidden">

                        <!-- Header -->
                        <div
                            class="bg-red-600 text-white p-3 md:p-4 text-center flex items-center justify-center gap-2 md:gap-3 rounded-t-xl shrink-0 relative shadow-md z-10">
                            <Goal class="w-5 h-5 md:w-6 md:h-6" />
                            <h3 class="text-base md:text-lg lg:text-xl font-bold tracking-wide">METAS DE PRODUÇÃO</h3>


                            <!-- Filter Button -->
                            <div class="absolute right-11 md:right-14 top-1/2 -translate-y-1/2 z-20">
                                <!-- z-20 for dropdown -->
                                <button @click="toggleFilter"
                                    class="text-white hover:bg-white/20 rounded-full p-1 md:p-1.5 transition-colors flex items-center justify-center relative"
                                    :class="{ 'bg-white/20': showFilter }">
                                    <Filter class="w-4 h-4 md:w-5 md:h-5" />
                                    <!-- Active Filter Indicator -->
                                    <span v-if="filterOption !== 'all'"
                                        class="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-yellow-400 rounded-full border-2 border-red-600"></span>
                                </button>

                                <!-- Dropdown Menu -->
                                <transition name="fade">
                                    <div v-if="showFilter"
                                        class="absolute right-0 top-full mt-2 w-48 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden py-1 text-left z-30">
                                        <div
                                            class="px-3 py-2 border-b border-gray-50 text-[10px] font-bold text-gray-400 uppercase tracking-wider">
                                            Filtrar Metas
                                        </div>

                                        <button @click="setFilter('all')"
                                            class="w-full px-4 py-2.5 text-sm font-semibold flex items-center justify-between hover:bg-gray-50 transition-colors"
                                            :class="filterOption === 'all' ? 'text-red-600 bg-red-50/50' : 'text-gray-600'">
                                            <span>Todas</span>
                                            <Check v-if="filterOption === 'all'" class="w-4 h-4" />
                                        </button>

                                        <button @click="setFilter('concluded')"
                                            class="w-full px-4 py-2.5 text-sm font-semibold flex items-center justify-between hover:bg-gray-50 transition-colors"
                                            :class="filterOption === 'concluded' ? 'text-green-600 bg-green-50/50' : 'text-gray-600'">
                                            <span>Concluídas</span>
                                            <Check v-if="filterOption === 'concluded'" class="w-4 h-4" />
                                        </button>

                                        <button @click="setFilter('reached')"
                                            class="w-full px-4 py-2.5 text-sm font-semibold flex items-center justify-between hover:bg-gray-50 transition-colors"
                                            :class="filterOption === 'reached' ? 'text-yellow-600 bg-yellow-50/50' : 'text-gray-600'">
                                            <span>Atingidas</span>
                                            <Check v-if="filterOption === 'reached'" class="w-4 h-4" />
                                        </button>

                                        <button @click="setFilter('pending')"
                                            class="w-full px-4 py-2.5 text-sm font-semibold flex items-center justify-between hover:bg-gray-50 transition-colors"
                                            :class="filterOption === 'pending' ? 'text-blue-600 bg-blue-50/50' : 'text-gray-600'">
                                            <span>Em Andamento</span>
                                            <Check v-if="filterOption === 'pending'" class="w-4 h-4" />
                                        </button>
                                    </div>
                                </transition>

                                <!-- Invisible Click Outside Layer (Local) -->
                                <div v-if="showFilter" class="fixed inset-0 z-20 cursor-default"
                                    @click="showFilter = false"></div>
                            </div>

                            <!-- Close Button (Restored to Header with explicit handler) -->
                            <button @click.stop="handleClose"
                                class="absolute right-3 md:right-4 text-white hover:bg-white/20 rounded-full p-2 transition-colors z-30 cursor-pointer pointer-events-auto">
                                <X class="w-5 h-5 md:w-6 md:h-6" />
                            </button>
                        </div>

                        <!-- Body -->
                        <div
                            class="p-3 sm:p-4 md:p-6 overflow-y-auto flex-1 custom-scrollbar bg-gray-50/50 relative rounded-b-xl">

                            <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden mb-6"
                                :class="{ 'ring-2 ring-red-50 border-red-100': isEditing }">

                                <!-- Toggle Header -->
                                <div class="flex items-center justify-between p-3 md:p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                                    @click="toggleForm">
                                    <div class="flex items-center gap-2 md:gap-3">
                                        <div class="p-1.5 md:p-2 rounded-lg transition-colors bg-red-50 text-red-600">
                                            <component :is="isEditing ? Pencil : Plus" class="w-4 h-4 md:w-5 md:h-5"
                                                :class="isEditing ? 'text-gray-500' : 'text-red-600'" />
                                        </div>
                                        <div>
                                            <h3 class="text-sm md:text-base font-bold text-gray-800">
                                                {{ isEditing ? 'EDITAR META' : 'NOVA META' }}
                                            </h3>
                                            <p v-if="isEditing" class="text-xs text-gray-500 font-medium">
                                                Editando meta #{{ isEditing }}
                                            </p>
                                        </div>
                                    </div>
                                    <ChevronDown class="w-5 h-5 text-gray-400 transition-transform duration-300"
                                        :class="{ 'rotate-180': showForm }" />
                                </div>

                                <!-- Collapsible Form Content -->
                                <transition name="expand">
                                    <div v-show="showForm" class="border-t border-gray-100">
                                        <div class="p-3 md:p-4 space-y-3 md:space-y-4 bg-gray-50/30">
                                            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-4">
                                                <div>
                                                    <label
                                                        class="block text-gray-600 text-xs font-bold mb-1.5 ml-1">DATA
                                                        INÍCIO</label>
                                                    <CustomCalendar v-model="form.data_inicio" placeholder="Início" />
                                                </div>
                                                <div>
                                                    <label
                                                        class="block text-gray-600 text-xs font-bold mb-1.5 ml-1">DATA
                                                        FIM</label>
                                                    <CustomCalendar v-model="form.data_fim" placeholder="Fim" />
                                                </div>
                                                <div>
                                                    <label
                                                        class="block text-gray-600 text-xs font-bold mb-1.5 ml-1">META
                                                        (QTD)</label>
                                                    <input v-model="form.meta_final" type="number"
                                                        placeholder="Ex: 2500"
                                                        class="w-full bg-white text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 focus:outline-none focus:border-red-500 transition-colors placeholder:text-gray-400 text-sm font-medium">
                                                </div>
                                            </div>

                                            <div
                                                class="flex flex-col-reverse sm:flex-row justify-end gap-2 md:gap-3 pt-2">
                                                <button v-if="isEditing" @click="cancelEdit"
                                                    class="px-4 py-2 text-gray-500 hover:text-gray-700 font-bold text-xs md:text-sm transition-colors">
                                                    CANCELAR
                                                </button>
                                                <button @click="saveGoal" :disabled="loading"
                                                    class="text-white font-bold py-2 px-6 md:px-8 rounded-lg shadow-md transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg active:scale-95 text-xs md:text-sm bg-neutral-800 hover:bg-neutral-900 w-full sm:w-auto">
                                                    <LoaderCircle v-if="loading" class="animate-spin w-4 h-4" />
                                                    {{ isEditing ? 'ATUALIZAR' : 'CRIAR' }}
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </transition>
                            </div>

                            <!-- Goals List with smooth transition -->
                            <div class="space-y-4">
                                <transition name="fade" mode="out-in" @before-leave="onBeforeLeave" @enter="onEnter"
                                    @after-enter="onAfterEnter">
                                    <div v-if="isLoadingGoals" key="loading" class="flex justify-center py-12">
                                        <LoaderCircle class="animate-spin text-red-600 w-8 h-8" />
                                    </div>

                                    <div v-else-if="filteredGoals.length === 0" key="empty"
                                        class="text-center py-12 opacity-60">
                                        <div
                                            class="bg-gray-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                                            <Goal class="w-10 h-10 text-gray-400" />
                                        </div>
                                        <p class="text-gray-600 text-lg font-bold">
                                            {{ filterMessage }}
                                        </p>
                                        <p class="text-sm text-gray-400 mt-1">
                                            {{ filterSubMessage }}
                                        </p>
                                    </div>

                                    <div v-else key="list">
                                        <div v-for="goal in filteredGoals" :key="goal.id"
                                            class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden relative group hover:shadow-md transition-all duration-300 hover:-translate-y-0.5 mb-4"
                                            :class="{ 'ring-2 ring-blue-100': isEditing === goal.id }">

                                            <!-- Status Stripe -->
                                            <div class="absolute left-0 top-0 bottom-0 w-2" :class="{
                                                'bg-green-500': goal.achieved,
                                                'bg-blue-500': !goal.achieved && (goal.meta_atual / goal.meta_final) < 1,
                                                'bg-yellow-500': !goal.achieved && (goal.meta_atual / goal.meta_final) >= 1
                                            }"></div>

                                            <div class="p-5 pl-8">
                                                <div
                                                    class="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 gap-4">
                                                    <div>
                                                        <div class="flex items-center gap-3">
                                                            <h4 class="text-base md:text-lg font-bold text-gray-800">
                                                                META DE PRODUÇÃO #{{ goal.id }}
                                                            </h4>
                                                            <span v-if="goal.achieved"
                                                                class="px-2 py-0.5 text-xs font-bold text-green-700 bg-green-100 rounded-full border border-green-200 uppercase tracking-widest flex items-center gap-1">
                                                                <CheckCircle2 class="w-3 h-3" /> CONCLUÍDA
                                                            </span>
                                                            <span v-else-if="goal.meta_atual >= goal.meta_final"
                                                                class="px-2 py-0.5 text-xs font-bold text-yellow-700 bg-yellow-100 rounded-full border border-yellow-200 uppercase tracking-widest">
                                                                ATINGIDA
                                                            </span>
                                                        </div>
                                                        <p
                                                            class="text-sm text-gray-500 mt-1 flex items-center gap-2 font-semibold bg-gray-50 w-fit px-2 py-1 rounded-md">
                                                            <Calendar class="w-4 h-4 text-gray-400" />
                                                            {{ formatDate(goal.data_inicio) }} <span
                                                                class="text-gray-300">|</span>
                                                            {{ formatDate(goal.data_fim) }}
                                                        </p>
                                                    </div>

                                                    <div
                                                        class="flex items-center gap-2 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity duration-200">

                                                        <button
                                                            v-if="!goal.achieved && goal.meta_atual >= goal.meta_final"
                                                            @click="confirmAction('conclude', goal)"
                                                            :disabled="goal.is_locked" title="Concluir Meta"
                                                            class="p-2 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition-colors border border-green-100 disabled:opacity-50 disabled:cursor-not-allowed">
                                                            <CheckCircle2 class="w-5 h-5" />
                                                        </button>

                                                        <button @click="toggleLock(goal)"
                                                            class="p-2 bg-gray-50 text-gray-500 rounded-lg hover:bg-gray-100 transition-colors border border-gray-100"
                                                            :title="goal.is_locked ? 'Desbloquear' : 'Bloquear'">
                                                            <component :is="goal.is_locked ? Lock : Unlock"
                                                                class="w-5 h-5"
                                                                :class="goal.is_locked ? 'text-red-500' : 'text-green-500'" />
                                                        </button>

                                                        <button @click="startEdit(goal)" :disabled="goal.is_locked"
                                                            class="p-2 bg-gray-50 text-gray-500 rounded-lg hover:bg-gray-100 transition-colors border border-gray-100 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed">
                                                            <Pencil class="w-5 h-5" />
                                                        </button>

                                                        <button @click="confirmAction('delete', goal)"
                                                            :disabled="goal.is_locked"
                                                            class="p-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors border border-red-100 disabled:opacity-50 disabled:cursor-not-allowed">
                                                            <Trash2 class="w-5 h-5" />
                                                        </button>
                                                    </div>
                                                </div>

                                                <!-- Progress Bar Section -->
                                                <div class="mb-2">
                                                    <div class="flex justify-between items-end mb-2">
                                                        <div class="flex flex-col">
                                                            <span
                                                                class="text-3xl font-extrabold text-gray-800 leading-none">
                                                                {{ goal.meta_atual.toLocaleString() }}
                                                            </span>
                                                            <span
                                                                class="text-[10px] text-gray-500 font-bold uppercase tracking-wider mt-1">
                                                                PRODUZIDOS
                                                            </span>
                                                        </div>
                                                        <div class="text-right">
                                                            <span class="text-sm font-bold text-gray-600">
                                                                {{ goal.meta_final.toLocaleString() }}
                                                            </span>
                                                            <span
                                                                class="text-[10px] text-gray-400 block font-bold uppercase tracking-wider">ALVO</span>
                                                        </div>
                                                    </div>

                                                    <!-- The Bar -->
                                                    <div
                                                        class="h-3 w-full bg-gray-100 rounded-full overflow-hidden shadow-inner relative border border-gray-100">
                                                        <div class="h-full rounded-full transition-all duration-1000 ease-out relative overflow-hidden"
                                                            :class="{
                                                                'bg-green-500': goal.achieved,
                                                                'bg-yellow-500': !goal.achieved && goal.meta_atual >= goal.meta_final,
                                                                'bg-blue-500': !goal.achieved && goal.meta_atual < goal.meta_final
                                                            }" :style="{ width: calculatePercentage(goal) + '%' }">
                                                            <!-- Shine effect -->
                                                            <div
                                                                class="absolute inset-0 bg-white/20 skew-x-12 -translate-x-full animate-[shimmer_2s_infinite]">
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <div class="flex justify-between mt-2 font-bold items-center">
                                                        <span class="text-xs px-2 py-0.5 rounded-md" :class="{
                                                            'bg-green-100 text-green-700': goal.meta_atual >= goal.meta_final,
                                                            'bg-blue-50 text-blue-700': goal.meta_atual < goal.meta_final
                                                        }">
                                                            {{ Math.min(Math.round((goal.meta_atual / goal.meta_final) *
                                                                100), 999) }}%
                                                        </span>

                                                        <span v-if="goal.meta_atual >= goal.meta_final"
                                                            class="text-xs text-green-600 flex items-center gap-1">
                                                            +{{ (goal.meta_atual - goal.meta_final).toLocaleString() }}
                                                            {{ getGoalUnit(goal) }}
                                                            <span
                                                                class="text-[10px] px-1 bg-green-100 rounded text-green-700">EXTRA</span>
                                                        </span>
                                                        <span v-else
                                                            class="text-xs text-red-500 flex items-center gap-1">
                                                            -{{ (goal.meta_final - goal.meta_atual).toLocaleString() }}
                                                            {{ getGoalUnit(goal) }}
                                                            <span
                                                                class="text-[10px] px-1 bg-red-50 rounded text-red-600">FALTAM</span>
                                                        </span>
                                                    </div>
                                                </div>

                                                <!-- Interactive Details Toggle -->
                                                <div class="mt-4 border-t border-gray-50 pt-2">
                                                    <button @click="toggleDetails(goal.id)"
                                                        class="w-full flex items-center justify-center gap-2 text-xs font-bold text-gray-400 hover:text-red-600 transition-colors py-1 group/btn">
                                                        <span v-if="expandedGoalId === goal.id">OCULTAR DETALHES</span>
                                                        <span v-else>VER LOTES CONTRIBUINTES</span>
                                                        <ChevronDown class="w-4 h-4 transition-transform duration-300"
                                                            :class="{ 'rotate-180': expandedGoalId === goal.id }" />
                                                    </button>

                                                    <!-- Expanded Details -->
                                                    <transition name="expand">
                                                        <div v-if="expandedGoalId === goal.id" class="overflow-hidden">
                                                            <div class="pt-2 pb-1">
                                                                <div v-if="!goal.linked_productions || goal.linked_productions.length === 0"
                                                                    class="text-center py-2 text-xs text-gray-400 italic">
                                                                    Nenhum lote contabilizado ainda.
                                                                </div>
                                                                <div v-else
                                                                    class="grid grid-cols-3 gap-2 text-xs font-semibold text-gray-500 bg-gray-50 p-2 rounded-lg">
                                                                    <div class="text-left pl-1">LOTE</div>
                                                                    <div class="text-center">DATA</div>
                                                                    <div class="text-right pr-1">QTD</div>

                                                                    <template
                                                                        v-for="(prod, index) in goal.linked_productions"
                                                                        :key="index">
                                                                        <div
                                                                            class="text-gray-700 font-bold border-t border-gray-100 py-1 pl-1">
                                                                            #{{ prod.num_lote }}
                                                                        </div>
                                                                        <div
                                                                            class="text-center border-t border-gray-100 py-1">
                                                                            {{ formatDate(prod.data_producao) }}
                                                                        </div>
                                                                        <div
                                                                            class="text-right border-t border-gray-100 py-1 pr-1 text-gray-800">
                                                                            {{ prod.quantidade.toLocaleString() }}
                                                                        </div>
                                                                    </template>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </transition>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </transition>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>

        <!-- Use Generic Confirmation Modal -->
        <ConfirmationModal :isOpen="confirmation.isOpen" :title="confirmation.title" :message="confirmation.message"
            :type="confirmation.type" :loading="loadingAction" :confirmText="confirmation.confirmText"
            @close="closeConfirmation" @confirm="handleConfirmation" />
    </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch, computed } from 'vue';
import { useToastStore } from '../../stores/toast';
import { useUserStore } from '../../stores/user';
import CustomCalendar from '../CustomCalendar.vue';
import ConfirmationModal from '../common/ConfirmationModal.vue';
import {
    Goal, X, Plus, ChevronDown, LoaderCircle,
    Calendar, CheckCircle2, Pencil, Trash2, Lock, Unlock, Filter, Check
} from 'lucide-vue-next';
import { nextTick } from 'vue';

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['close']);
const toastStore = useToastStore();
const userStore = useUserStore();

const goals = ref([]);
const isLoadingGoals = ref(true);
const showForm = ref(false);
const loading = ref(false);
const loadingAction = ref(false); // For modal actions
const isEditing = ref(null); // ID if editing
const expandedGoalId = ref(null); // Track which goal has details open
const modalContentRef = ref(null);

// Smooth resize via Transition Hooks
const onBeforeLeave = () => {
    if (!modalContentRef.value) return;
    modalContentRef.value.style.height = `${modalContentRef.value.offsetHeight}px`;
    modalContentRef.value.style.overflow = 'hidden';
};

const onEnter = () => {
    if (!modalContentRef.value) return;
    const el = modalContentRef.value;

    // Measure target height
    const prevHeight = el.style.height;
    el.style.height = 'auto';
    const targetHeight = el.offsetHeight;
    el.style.height = prevHeight;

    // Force reflow
    el.offsetHeight;

    // Animate
    requestAnimationFrame(() => {
        el.style.height = `${targetHeight}px`;
    });
};

const onAfterEnter = () => {
    if (!modalContentRef.value) return;
    modalContentRef.value.style.height = null;
    modalContentRef.value.style.overflow = null;
};

// Fetch when opened and close filter when closed
watch(() => props.isOpen, (newVal) => {
    if (newVal) {
        fetchGoals();
    } else {
        // Close filter dropdown when modal is closed
        showFilter.value = false;
    }
});

const toggleDetails = (goalId) => {
    if (expandedGoalId.value === goalId) {
        expandedGoalId.value = null;
    } else {
        expandedGoalId.value = goalId;
    }
};

const form = ref({
    data_inicio: '',
    data_fim: '',
    meta_final: ''
});

// Confirmation Modal State
const confirmation = reactive({
    isOpen: false,
    title: '',
    message: '',
    type: 'danger',
    action: null, // 'delete' or 'conclude'
    targetId: null,
    targetData: null,
    confirmText: 'SIM'
});



const showFilter = ref(false);
const filterOption = ref('all'); // all, concluded, reached, pending

const toggleFilter = () => {
    showFilter.value = !showFilter.value;
};

const setFilter = (option) => {
    filterOption.value = option;
    showFilter.value = false;
};

const handleClose = () => {
    showFilter.value = false;
    emit('close');
};

const filteredGoals = computed(() => {
    if (!goals.value) return [];

    return goals.value.filter(goal => {
        if (filterOption.value === 'all') return true;

        if (filterOption.value === 'concluded') return goal.achieved;

        if (filterOption.value === 'reached') {
            // "Atingida" means met target but NOT marked concluded (yellow status)
            return !goal.achieved && goal.meta_atual >= goal.meta_final;
        }

        if (filterOption.value === 'pending') {
            // "Em Andamento" means target not yet met
            return !goal.achieved && goal.meta_atual < goal.meta_final;
        }

        return true;
    });
});

const filterMessage = computed(() => {
    switch (filterOption.value) {
        case 'concluded': return 'Metas concluídas.';
        case 'reached': return 'Metas atingidas.';
        case 'pending': return 'Metas em andamento.';
        default: return 'Nenhuma meta ativa.';
    }
});

const filterSubMessage = computed(() => {
    return filterOption.value === 'all'
        ? 'Defina seus objetivos de produção acima.'
        : 'Tente alterar o filtro.';
});

const getGoalUnit = (goal) => {
    const productName = goal.linked_productions?.[0]?.product_name;
    return productName?.toLowerCase().includes('25kg') ? 'sc' : 'cx';
};

const fetchGoals = async () => {
    isLoadingGoals.value = true;
    try {
        const response = await fetch(`/api/goals`, {
            headers: {
                'Authorization': `Bearer ${userStore.token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Falha ao buscar metas');
        goals.value = await response.json();
    } catch (error) {
        console.error("Erro ao buscar metas", error);
        toastStore.add({
            title: 'Erro',
            message: "Erro ao carregar metas.",
            type: 'error'
        });
    } finally {
        isLoadingGoals.value = false;
    }
};

const toggleLock = async (goal) => {
    // Optimistic Update: Change state immediately
    const startState = goal.is_locked;
    goal.is_locked = !goal.is_locked;

    try {
        const response = await fetch(`/api/goals/${goal.id}/lock`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${userStore.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_locked: goal.is_locked })
        });

        if (!response.ok) throw new Error('Erro ao alterar bloqueio');

        // const msg = goal.is_locked ? "Meta bloqueada." : "Meta desbloqueada.";
        // toastStore.add({ title: 'Sucesso', message: msg, type: 'success' });

    } catch (error) {
        // Revert on error
        goal.is_locked = startState;
        toastStore.add({ title: 'Erro', message: "Erro ao alterar bloqueio.", type: 'error' });
    }
};

const toggleForm = () => {
    // If editing, clicking header cancels edit mode but keeps form open if validation fails? 
    // Usually standard behavior: toggle open/close. If editing, we close and reset.
    if (showForm.value) {
        showForm.value = false;
        setTimeout(() => resetForm(), 300); // Reset after transition
    } else {
        showForm.value = true;
    }
};

const resetForm = () => {
    form.value = {
        data_inicio: '',
        data_fim: '',
        meta_final: ''
    };
    isEditing.value = null;
};

const cancelEdit = () => {
    showForm.value = false;
    setTimeout(() => resetForm(), 300);
};

const saveGoal = async () => {
    if (!form.value.data_inicio || !form.value.data_fim || !form.value.meta_final) {
        toastStore.add({ title: 'Atenção', message: "Preencha todos os campos.", type: 'warning' });
        return;
    }

    loading.value = true;
    try {
        const url = isEditing.value ? `/api/goals/${isEditing.value}` : `/api/goals`;
        const method = isEditing.value ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Authorization': `Bearer ${userStore.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(form.value)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || 'Erro ao salvar meta');
        }

        toastStore.add({
            title: 'Sucesso',
            message: isEditing.value ? "Meta atualizada!" : "Meta criada com sucesso!",
            type: 'success'
        });

        cancelEdit(); // Closes form and resets
        fetchGoals();
    } catch (error) {
        console.error("Erro ao salvar meta", error);
        toastStore.add({ title: 'Erro', message: error.message || "Erro ao salvar meta.", type: 'error' });
    } finally {
        loading.value = false;
    }
};

const startEdit = (goal) => {
    form.value = {
        data_inicio: goal.data_inicio, // Assuming YYYY-MM-DD from API matches input
        data_fim: goal.data_fim,
        meta_final: goal.meta_final
    };
    isEditing.value = goal.id;
    showForm.value = true;
    // Scroll to top of modal to see form
    const modalBody = document.querySelector('.custom-scrollbar');
    if (modalBody) modalBody.scrollTo({ top: 0, behavior: 'smooth' });
};

// --- Confirmation Actions ---

const confirmAction = (action, goal) => {
    confirmation.action = action;
    confirmation.targetId = goal.id;
    confirmation.targetData = goal;
    confirmation.isOpen = true;

    if (action === 'delete') {
        confirmation.title = 'Excluir Meta';
        confirmation.message = 'Tem certeza que deseja excluir esta meta permanentemente?';
        confirmation.type = 'danger';
        confirmation.confirmText = 'EXCLUIR';
    } else if (action === 'conclude') {
        confirmation.title = 'Concluir Meta';
        confirmation.message = 'Deseja marcar esta meta como CONCLUÍDA? Isso irá arquivá-la como sucesso.';
        confirmation.type = 'success';
        confirmation.confirmText = 'CONCLUIR';
    }
};

const closeConfirmation = () => {
    confirmation.isOpen = false;
    confirmation.action = null;
    confirmation.targetId = null;
};

const handleConfirmation = async () => {
    loadingAction.value = true;
    try {
        if (confirmation.action === 'delete') {
            await performDelete(confirmation.targetId);
        } else if (confirmation.action === 'conclude') {
            await performConclude(confirmation.targetData);
        }
        closeConfirmation();
        fetchGoals();
    } catch (error) {
        // Error handled in perform functions
    } finally {
        loadingAction.value = false;
    }
};

const performDelete = async (id) => {
    try {
        const response = await fetch(`/api/goals/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${userStore.token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Erro ao excluir');
        toastStore.add({ title: 'Sucesso', message: "Meta excluída.", type: 'success' });
    } catch (error) {
        toastStore.add({ title: 'Erro', message: "Erro ao excluir meta.", type: 'error' });
        throw error;
    }
};

const performConclude = async (goal) => {
    try {
        const response = await fetch(`/api/goals/${goal.id}/achieved`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${userStore.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ achieved: true })
        });

        if (!response.ok) throw new Error('Erro ao concluir');
        toastStore.add({ title: 'Sucesso', message: "Meta concluída com sucesso!", type: 'success' });
    } catch (error) {
        toastStore.add({ title: 'Erro', message: "Erro ao concluir meta.", type: 'error' });
        throw error;
    }
};

// --- Helpers ---

const calculatePercentage = (goal) => {
    if (!goal.meta_final || goal.meta_final === 0) return 0;
    const pct = (goal.meta_atual / goal.meta_final) * 100;
    return Math.min(pct, 100);
};

const formatDate = (dateStr) => {
    if (!dateStr) return '';
    if (dateStr.includes('/')) return dateStr;
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
};

onMounted(() => {
    if (props.isOpen) {
        fetchGoals();
    }
});
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

/* Expand Transition for Form */
.expand-enter-active,
.expand-leave-active {
    transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    max-height: 500px;
    opacity: 1;
    overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
    max-height: 0;
    opacity: 0;
}

/* Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

@keyframes shimmer {
    100% {
        transform: translateX(100%) skewX(12deg);
    }
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
