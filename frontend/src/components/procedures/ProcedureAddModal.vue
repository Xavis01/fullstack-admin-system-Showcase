<template>
  <div>
    <!-- Blur Backdrop -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 z-40"
        style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
      </div>
    </transition>

    <!-- Overlay & Modal -->
    <transition name="modal-backdrop">
      <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center z-50 font-montserrat p-4">
        <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
        <transition name="modal">
          <div v-if="isOpen" class="bg-white rounded-3xl shadow-2xl w-full max-w-md p-6 md:p-8 z-10">

            <!-- Header -->
            <div class="flex items-center gap-3 mb-6">
              <div class="bg-red-100 p-2 rounded-xl">
                <FolderOpen class="w-5 h-5 text-red-600" />
              </div>
              <h3 class="text-xl font-bold text-neutral-800">Adicionar Procedimento</h3>
            </div>

            <div class="space-y-4">
              <!-- Name -->
              <div>
                <label class="block text-sm font-semibold text-neutral-600 mb-1.5">Nome do procedimento *</label>
                <input v-model="nome" type="text" placeholder="Ex: Procedimento de Segurança"
                  class="w-full border border-neutral-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-red-500 transition" />
              </div>

              <!-- File drop zone -->
              <div>
                <label class="block text-sm font-semibold text-neutral-600 mb-1.5">Arquivo *</label>
                <div class="border-2 border-dashed border-neutral-300 rounded-xl p-4 text-center cursor-pointer hover:border-red-400 transition"
                  @click="$refs.fileInput.click()"
                  @dragover.prevent
                  @drop.prevent="onDrop">
                  <template v-if="!file">
                    <Upload class="w-7 h-7 mx-auto text-neutral-400 mb-2" />
                    <p class="text-sm text-neutral-500">Clique ou arraste o arquivo aqui</p>
                    <p class="text-xs text-neutral-400 mt-1">PDF, DOCX, XLSX, PNG, etc.</p>
                  </template>
                  <template v-else>
                    <FileCheck class="w-7 h-7 mx-auto text-green-500 mb-1" />
                    <p class="text-sm font-semibold text-neutral-700 truncate">{{ file.name }}</p>
                    <p class="text-xs text-neutral-400">{{ formatFileSize(file.size) }}</p>
                  </template>
                </div>
                <input ref="fileInput" type="file" class="hidden" @change="onFileChange" />
              </div>
            </div>

            <p v-if="error" class="mt-3 text-sm text-red-600 font-medium">{{ error }}</p>

            <!-- Actions -->
            <div class="flex gap-3 mt-6">
              <button @click="$emit('close')"
                class="flex-1 py-2.5 rounded-xl border border-neutral-300 text-neutral-600 font-semibold hover:bg-neutral-50 transition text-sm">
                Cancelar
              </button>
              <button @click="submit" :disabled="loading"
                class="flex-1 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-semibold transition text-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
                <span v-if="loading" class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></span>
                <span>{{ loading ? 'Salvando...' : 'Salvar' }}</span>
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { FolderOpen, Upload, FileCheck } from 'lucide-vue-next'

const props = defineProps({
  isOpen: Boolean,
  loading: Boolean,
  error: String
})

const emit = defineEmits(['close', 'submit'])

const nome = ref('')
const file = ref(null)
const fileInput = ref(null)

watch(() => props.isOpen, (val) => {
  if (val) {
    nome.value = ''
    file.value = null
  }
})

function onFileChange(e) { file.value = e.target.files[0] || null }
function onDrop(e) { file.value = e.dataTransfer.files[0] || null }
function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

function submit() {
  emit('submit', { nome: nome.value, file: file.value })
}
</script>

<style scoped>
.modal-backdrop-enter-active,
.modal-backdrop-leave-active { transition: opacity 0.3s ease; }
.modal-backdrop-enter-from,
.modal-backdrop-leave-to { opacity: 0; }

.modal-enter-active,
.modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from,
.modal-leave-to { opacity: 0; transform: scale(0.9) translateY(-20px); }
</style>
