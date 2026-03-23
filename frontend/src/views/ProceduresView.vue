<template>
    <div class="min-h-screen bg-gray-200 font-montserrat">
        <section id="procedures">
            <div class="max-w-5xl mx-auto px-3 sm:px-4 md:px-6 pt-20 sm:pt-24 md:pt-26 pb-6 sm:pb-8 md:pb-12">

                <!-- Header -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 md:mb-8">
                    <div class="flex items-center gap-2 md:gap-4">
                        <button @click="router.back()"
                            class="bg-white p-2 rounded-xl shadow hover:bg-gray-50 active:scale-95 transition text-neutral-600">
                            <ArrowLeft class="w-5 h-5 md:w-6 md:h-6" />
                        </button>
                        <div class="bg-red-600 p-2 md:p-3 rounded-xl shadow-lg">
                            <FolderOpen class="text-white w-5 h-5 md:w-7 md:h-7" />
                        </div>
                        <div>
                            <h2 class="text-xl sm:text-2xl md:text-3xl font-extrabold text-neutral-800 uppercase tracking-wide">
                                Procedimentos
                            </h2>
                            <p class="text-neutral-500 text-xs sm:text-sm">Arquivos e documentos da empresa</p>
                        </div>
                    </div>
                    <button @click="showAdd = true"
                        class="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white font-semibold px-4 py-2.5 rounded-xl shadow-lg transition-all active:scale-95">
                        <Plus class="w-4 h-4" />
                        <span class="text-sm">Adicionar Arquivo</span>
                    </button>
                </div>

                <!-- Loading -->
                <div v-if="loading" class="flex justify-center items-center py-16">
                    <div class="animate-spin rounded-full h-10 w-10 border-4 border-red-600 border-t-transparent"></div>
                </div>

                <!-- Empty State -->
                <div v-else-if="procedures.length === 0"
                    class="animate-fade-in flex flex-col items-center justify-center py-20 text-center">
                    <div class="bg-[#1a1a1a] p-6 rounded-3xl mb-4 border border-neutral-800">
                        <FolderOpen class="w-12 h-12 text-neutral-500" />
                    </div>
                    <p class="text-neutral-600 font-semibold text-lg">Nenhum procedimento cadastrado</p>
                    <p class="text-neutral-400 text-sm mt-1">Clique em "Adicionar Arquivo" para começar</p>
                </div>

                <!-- List -->
                <div v-else class="space-y-3">
                    <div v-for="(proc, index) in procedures" :key="proc.id"
                        class="animate-fade-in group relative bg-[#1a1a1a] rounded-2xl p-4 md:p-5 border border-neutral-800 hover:border-red-600 transition-all duration-300 hover:shadow-xl hover:shadow-red-900/10"
                        :style="`animation-delay: ${index * 50}ms`">
                        <div class="flex items-center gap-3 md:gap-4">

                            <!-- File Type Icon -->
                            <div :class="fileIconClass(proc.original_filename)"
                                class="flex-shrink-0 w-11 h-11 md:w-12 md:h-12 rounded-xl flex items-center justify-center font-bold text-xs shadow-md">
                                {{ fileExt(proc.original_filename) }}
                            </div>

                            <!-- Info -->
                            <div class="flex-1 min-w-0">
                                <p class="text-white font-bold text-sm md:text-base truncate">{{ proc.nome }}</p>
                                <p class="text-neutral-400 text-xs mt-0.5 truncate">{{ proc.original_filename }}</p>
                                <div class="flex flex-wrap items-center gap-x-3 gap-y-0.5 mt-1.5">
                                    <span class="flex items-center gap-1 text-neutral-500 text-xs">
                                        <User class="w-3 h-3" /> {{ proc.created_by_name }}
                                    </span>
                                    <span class="flex items-center gap-1 text-neutral-500 text-xs">
                                        <CalendarDays class="w-3 h-3" /> {{ formatDate(proc.created_at) }}
                                    </span>
                                    <span v-if="proc.updated_at !== proc.created_at"
                                        class="flex items-center gap-1 text-neutral-600 text-xs">
                                        <Pencil class="w-3 h-3" /> Editado {{ formatDate(proc.updated_at) }}
                                    </span>
                                </div>
                            </div>

                            <!-- Actions -->
                            <div class="flex items-center gap-1.5 flex-shrink-0">
                                <button @click="openFile(proc)"
                                    class="p-2 rounded-lg bg-neutral-800 hover:bg-green-600 text-neutral-300 hover:text-white transition-all duration-200"
                                    title="Abrir arquivo">
                                    <ExternalLink class="w-4 h-4" />
                                </button>
                                <button @click="openEdit(proc)"
                                    class="p-2 rounded-lg bg-neutral-800 hover:bg-blue-600 text-neutral-300 hover:text-white transition-all duration-200"
                                    title="Editar">
                                    <Pencil class="w-4 h-4" />
                                </button>
                                <button @click="openDelete(proc)"
                                    class="p-2 rounded-lg bg-neutral-800 hover:bg-red-600 text-neutral-300 hover:text-white transition-all duration-200"
                                    title="Excluir">
                                    <Trash2 class="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Modals -->
        <ProcedureAddModal
            :isOpen="showAdd"
            :loading="addLoading"
            :error="addError"
            @close="showAdd = false"
            @submit="submitAdd"
        />

        <ProcedureEditModal
            :isOpen="showEdit"
            :procedure="editTarget"
            :loading="editLoading"
            :error="editError"
            @close="showEdit = false"
            @submit="submitEdit"
        />

        <ProcedureDeleteModal
            :isOpen="showDelete"
            :procedure="deleteTarget"
            :loading="deleteLoading"
            @close="showDelete = false"
            @confirm="submitDelete"
        />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, FolderOpen, Plus, ExternalLink, Pencil, Trash2, User, CalendarDays } from 'lucide-vue-next'
import { useToastStore } from '../stores/toast'
import ProcedureAddModal from '../components/procedures/ProcedureAddModal.vue'
import ProcedureEditModal from '../components/procedures/ProcedureEditModal.vue'
import ProcedureDeleteModal from '../components/procedures/ProcedureDeleteModal.vue'

const router = useRouter()
const toastStore = useToastStore()

// ─── State ────────────────────────────────────────────────────────────────────
const procedures = ref([])
const loading = ref(false)

const showAdd = ref(false)
const addLoading = ref(false)
const addError = ref('')

const showEdit = ref(false)
const editTarget = ref(null)
const editLoading = ref(false)
const editError = ref('')

const showDelete = ref(false)
const deleteTarget = ref(null)
const deleteLoading = ref(false)

// ─── Helpers ──────────────────────────────────────────────────────────────────
function authHeaders() {
    return { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
    })
}

function fileExt(filename) {
    if (!filename) return 'FILE'
    const ext = filename.split('.').pop().toUpperCase()
    return ext.length > 5 ? ext.slice(0, 4) : ext
}

function fileIconClass(filename) {
    const ext = (filename || '').split('.').pop().toLowerCase()
    const map = {
        pdf: 'bg-red-600 text-white',
        doc: 'bg-blue-600 text-white', docx: 'bg-blue-600 text-white',
        xls: 'bg-green-600 text-white', xlsx: 'bg-green-600 text-white',
        ppt: 'bg-orange-500 text-white', pptx: 'bg-orange-500 text-white',
        png: 'bg-purple-500 text-white', jpg: 'bg-purple-500 text-white', jpeg: 'bg-purple-500 text-white',
    }
    return map[ext] || 'bg-neutral-600 text-white'
}

// ─── Fetch ─────────────────────────────────────────────────────────────────────
async function fetchProcedures() {
    loading.value = true
    try {
        const res = await fetch('/api/procedures', { headers: authHeaders() })
        if (!res.ok) throw new Error()
        procedures.value = await res.json()
    } catch {
        toastStore.add({ title: 'Erro', message: 'Não foi possível carregar os procedimentos.', type: 'error' })
    } finally {
        loading.value = false
    }
}

// ─── ADD ───────────────────────────────────────────────────────────────────────
async function submitAdd({ nome, file }) {
    addError.value = ''
    if (!nome?.trim()) { addError.value = 'Informe o nome do procedimento.'; return }
    if (!file) { addError.value = 'Selecione um arquivo.'; return }

    addLoading.value = true
    try {
        const fd = new FormData()
        fd.append('nome', nome.trim())
        fd.append('file', file)
        const res = await fetch('/api/procedures', { method: 'POST', headers: authHeaders(), body: fd })
        const data = await res.json()
        if (!res.ok) { addError.value = data.error || 'Erro ao salvar.'; return }
        procedures.value.unshift(data.procedure)
        showAdd.value = false
        toastStore.add({ title: 'Sucesso', message: 'Procedimento adicionado com sucesso!', type: 'success' })
    } catch {
        addError.value = 'Erro de conexão.'
    } finally {
        addLoading.value = false
    }
}

// ─── EDIT ──────────────────────────────────────────────────────────────────────
function openEdit(proc) {
    editTarget.value = proc
    editError.value = ''
    showEdit.value = true
}

async function submitEdit({ nome, file }) {
    editError.value = ''
    if (!nome?.trim()) { editError.value = 'Informe o nome.'; return }

    editLoading.value = true
    try {
        const fd = new FormData()
        fd.append('nome', nome.trim())
        if (file) fd.append('file', file)
        const res = await fetch(`/api/procedures/${editTarget.value.id}`, { method: 'PUT', headers: authHeaders(), body: fd })
        const data = await res.json()
        if (!res.ok) { editError.value = data.error || 'Erro ao atualizar.'; return }
        const idx = procedures.value.findIndex(p => p.id === editTarget.value.id)
        if (idx !== -1) procedures.value[idx] = data.procedure
        showEdit.value = false
        toastStore.add({ title: 'Sucesso', message: 'Procedimento atualizado!', type: 'success' })
    } catch {
        editError.value = 'Erro de conexão.'
    } finally {
        editLoading.value = false
    }
}

// ─── DELETE ────────────────────────────────────────────────────────────────────
function openDelete(proc) {
    deleteTarget.value = proc
    showDelete.value = true
}

async function submitDelete() {
    deleteLoading.value = true
    try {
        const res = await fetch(`/api/procedures/${deleteTarget.value.id}`, { method: 'DELETE', headers: authHeaders() })
        if (!res.ok) { toastStore.add({ title: 'Erro', message: 'Não foi possível excluir.', type: 'error' }); return }
        procedures.value = procedures.value.filter(p => p.id !== deleteTarget.value.id)
        showDelete.value = false
        toastStore.add({ title: 'Excluído', message: 'Procedimento removido com sucesso.', type: 'success' })
    } catch {
        toastStore.add({ title: 'Erro', message: 'Erro de conexão.', type: 'error' })
    } finally {
        deleteLoading.value = false
    }
}

// ─── OPEN FILE ─────────────────────────────────────────────────────────────────
async function openFile(proc) {
    try {
        const res = await fetch(`/api/procedures/${proc.id}/file`, { headers: authHeaders() })
        if (!res.ok) throw new Error()
        const blob = await res.blob()
        const url = URL.createObjectURL(blob)
        window.open(url, '_blank')
        setTimeout(() => URL.revokeObjectURL(url), 60000)
    } catch {
        toastStore.add({ title: 'Erro', message: 'Não foi possível abrir o arquivo.', type: 'error' })
    }
}

onMounted(fetchProcedures)
</script>

<style scoped></style>
