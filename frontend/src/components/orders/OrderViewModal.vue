<template>
    <div>
        <!-- Blur Layer with synchronized transition -->
        <transition name="modal-backdrop">
            <div v-if="isOpen" class="fixed inset-0 z-[70]"
                style="backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); will-change: opacity; transform: translateZ(0);">
            </div>
        </transition>

        <transition name="modal-backdrop">
            <div v-if="isOpen"
                class="fixed inset-0 flex items-center justify-center z-[80] font-montserrat px-3 md:px-4 pt-20 md:pt-36 pb-6">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-2xl z-10 w-full max-w-lg flex flex-col overflow-hidden max-h-full">

                        <!-- Header -->
                        <div class="bg-neutral-700 text-white px-6 py-4 flex items-center justify-between shrink-0">
                            <div class="flex items-center gap-3">
                                <div class="bg-white/15 p-2 rounded-lg">
                                    <Eye class="w-5 h-5" />
                                </div>
                                <h3 class="text-lg font-bold">PEDIDO #{{ order?.id }}</h3>
                            </div>
                            <div class="flex items-center gap-2">
                                <button @click="printOrder" title="Imprimir Pedido"
                                    class="bg-white/10 hover:bg-white/20 active:scale-95 text-white p-2 rounded-lg transition flex items-center gap-1.5 text-xs font-bold">
                                    <Printer class="w-4 h-4" />
                                    <span class="hidden sm:inline">IMPRIMIR</span>
                                </button>
                                <button @click="copyOrderDetails" title="Copiar Detalhes"
                                    class="bg-white/10 hover:bg-white/20 active:scale-95 text-white p-2 rounded-lg transition flex items-center gap-1.5 text-xs font-bold">
                                    <Copy class="w-4 h-4" />
                                    <span class="hidden sm:inline">COPIAR</span>
                                </button>
                                <button @click="$emit('close')"
                                    class="text-white/60 hover:text-white transition-colors p-1 rounded-full hover:bg-white/10 ml-2">
                                    <X class="w-5 h-5" />
                                </button>
                            </div>
                        </div>

                        <!-- Body -->
                        <div class="flex-1 overflow-y-auto p-6 space-y-5" v-if="order">

                            <!-- Status badge -->
                            <div class="flex justify-center">
                                <span class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-bold"
                                    :class="order.achieved ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'">
                                    <CheckCircle2 v-if="order.achieved" class="w-4 h-4" />
                                    <Clock v-else class="w-4 h-4" />
                                    {{ order.achieved ? 'CONCLUÍDO' : 'PENDENTE' }}
                                </span>
                            </div>

                            <!-- Info rows -->
                            <div class="space-y-4">
                                <!-- Client -->
                                <div class="flex items-start gap-3">
                                    <div
                                        class="w-9 h-9 rounded-lg bg-blue-50 flex items-center justify-center text-blue-600 flex-shrink-0 mt-0.5">
                                        <UserIcon class="w-4 h-4" />
                                    </div>
                                    <div>
                                        <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wide">Cliente
                                        </p>
                                        <p class="text-sm font-semibold text-neutral-800">{{ order.client_name }}</p>
                                    </div>
                                </div>

                                <!-- Quantity -->
                                <div class="flex items-start gap-3">
                                    <div
                                        class="w-9 h-9 rounded-lg bg-purple-50 flex items-center justify-center text-purple-600 flex-shrink-0 mt-0.5">
                                        <BoxIcon class="w-4 h-4" />
                                    </div>
                                    <div>
                                        <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wide">
                                            Quantidade Solicitada
                                        </p>
                                        <p class="text-sm font-semibold text-neutral-800">{{
                                            order.quant_caixa_solicitada }} {{
                                                order.lotes?.[0]?.product_name?.toLowerCase().includes('25kg') ? 'Sacos' :
                                                    'Caixas' }}
                                        </p>
                                    </div>
                                </div>

                                <!-- Created by -->
                                <div class="flex items-start gap-3">
                                    <div
                                        class="w-9 h-9 rounded-lg bg-gray-100 flex items-center justify-center text-gray-500 flex-shrink-0 mt-0.5">
                                        <CalendarDays class="w-4 h-4" />
                                    </div>
                                    <div>
                                        <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wide">Criado
                                            por</p>
                                        <p class="text-sm font-semibold text-neutral-800">{{ order.created_by_name }}
                                        </p>
                                        <p class="text-xs text-gray-400">{{ formatDate(order.created_at) }}</p>
                                    </div>
                                </div>
                            </div>

                            <!-- Observação -->
                            <div v-if="order.observacao" class="space-y-4">
                                <div class="flex items-start gap-3">
                                    <div
                                        class="w-9 h-9 rounded-lg bg-yellow-50 flex items-center justify-center text-yellow-600 flex-shrink-0 mt-0.5">
                                        <MessageSquareText class="w-4 h-4" />
                                    </div>
                                    <div>
                                        <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wide">Observação
                                        </p>
                                        <p class="text-sm text-neutral-700 whitespace-pre-line">{{ order.observacao }}</p>
                                    </div>
                                </div>
                            </div>

                            <!-- Lotes section -->
                            <div>
                                <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wide mb-2 ml-1">Lotes
                                    Vinculados
                                    ({{ order.lotes?.length || 0 }})</p>
                                <div v-if="order.lotes && order.lotes.length > 0" class="space-y-2">
                                    <div v-for="lote in order.lotes" :key="lote.num_lote"
                                        class="flex items-center gap-2.5 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2.5">
                                        <img v-if="lote.product_image" :src="lote.product_image"
                                            class="w-8 h-8 rounded-full object-cover border border-gray-200 flex-shrink-0" />
                                        <div v-else
                                            class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 flex-shrink-0">
                                            <Package class="w-4 h-4" />
                                        </div>
                                        <div class="flex-1 min-w-0">
                                            <p class="text-sm font-semibold text-neutral-800 truncate">{{
                                                lote.product_name }}</p>
                                            <p class="text-xs text-gray-500">
                                                Lote #{{ lote.num_lote }}
                                                · Qtd: <span class="font-bold text-neutral-800">{{ lote.quantidade }}
                                                    {{ lote.product_name?.toLowerCase().includes('25kg') ? 'sc' : 'cx'
                                                    }}</span>
                                                · Estoque: <span class="font-bold"
                                                    :class="lote.estoque_lote > 0 ? 'text-green-600' : 'text-red-500'">{{
                                                        lote.estoque_lote }} {{
                                                        lote.product_name?.toLowerCase().includes('25kg') ? 'sc' : 'cx'
                                                    }}</span>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div v-else class="text-sm text-gray-400 italic px-1">Nenhum lote vinculado</div>
                            </div>

                        </div>

                        <!-- Footer -->
                        <div class="px-6 py-4 border-t border-gray-100 flex justify-end shrink-0">
                            <button @click="$emit('close')"
                                class="px-6 py-2.5 text-sm font-bold text-white bg-neutral-700 hover:bg-neutral-800 rounded-lg transition active:scale-95">
                                FECHAR
                            </button>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { X, Eye, CheckCircle2, Clock, Package, CalendarDays, Printer, Copy, MessageSquareText } from 'lucide-vue-next'
import { UserRound as UserIcon, Box as BoxIcon } from 'lucide-vue-next'
import { useToastStore } from '../../stores/toast'

const props = defineProps({
    isOpen: Boolean,
    order: Object
})

const emit = defineEmits(['close'])

const toastStore = useToastStore()

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const copyOrderDetails = () => {
    if (!props.order) return
    const o = props.order
    const lines = []

    if (o.lotes && o.lotes.length > 0) {
        lines.push('───────────────────────────────────────')
        for (const lote of o.lotes) {
            const unit = lote.product_name?.toLowerCase().includes('25kg') ? 'sc' : 'cx'
            lines.push(`Produto: ${lote.product_name}`)
            lines.push(`Lote #${lote.num_lote} | Qtd: ${lote.quantidade} ${unit}`)
            lines.push('───────────────────────────────────────')
        }
    } else {
        lines.push('Nenhum lote vinculado')
    }

    const text = lines.join('\n')

    const fallbackCopy = () => {
        const ta = document.createElement('textarea')
        ta.value = text
        ta.style.position = 'fixed'
        ta.style.opacity = '0'
        document.body.appendChild(ta)
        ta.select()
        try {
            document.execCommand('copy')
            toastStore.add({ title: 'Copiado!', message: 'Detalhes do pedido copiados.', type: 'success' })
        } catch {
            toastStore.add({ title: 'Erro', message: 'Não foi possível copiar.', type: 'error' })
        }
        document.body.removeChild(ta)
    }

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text)
            .then(() => toastStore.add({ title: 'Copiado!', message: 'Detalhes do pedido copiados.', type: 'success' }))
            .catch(() => fallbackCopy())
    } else {
        fallbackCopy()
    }
}

const printOrder = () => {
    if (!props.order) return
    const o = props.order

    const makeLotesTable = () => {
        if (!o.lotes || o.lotes.length === 0) return '<p>Nenhum lote vinculado.</p>'

        let html = '<table style="width:100%;border-collapse:collapse;margin-top:20px;font-size:14px;">'
        html += '<thead><tr>'
        html += '<th style="text-align:left;padding:10px;border-bottom:2px solid #333;font-weight:700;">Produto</th>'
        html += '<th style="text-align:center;padding:10px;border-bottom:2px solid #333;font-weight:700;">Lote</th>'
        html += '<th style="text-align:center;padding:10px;border-bottom:2px solid #333;font-weight:700;">Quantidade</th>'
        html += '</tr></thead><tbody>'

        for (const lote of o.lotes) {
            const unit = lote.product_name?.toLowerCase().includes('25kg') ? 'sc' : 'cx'
            html += '<tr>'
            html += `<td style="padding:10px;border-bottom:1px solid #ddd;">${lote.product_name}</td>`
            html += `<td style="text-align:center;padding:10px;border-bottom:1px solid #ddd;">#${lote.num_lote}</td>`
            html += `<td style="text-align:center;padding:10px;border-bottom:1px solid #ddd;font-weight:bold;">${lote.quantidade} ${unit}</td>`
            html += '</tr>'
        }
        html += '</tbody></table>'
        return html
    }

    let html = `
        <html><head><title>Pedido #${o.id}</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; color: #222; max-width: 800px; margin: 0 auto; }
            .header { border-bottom: 2px solid #dc2626; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: flex-end; }
            h1 { font-size: 28px; margin: 0; color: #111; }
            .status { font-weight: bold; padding: 6px 12px; border-radius: 4px; font-size: 14px; }
            .status.concluido { background-color: #dcfce7; color: #166534; }
            .status.pendente { background-color: #fef08a; color: #854d0e; }
            
            .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 40px; }
            .info-box { background: #f9f9f9; padding: 15px; border-radius: 8px; border: 1px solid #eee; }
            .info-label { font-size: 11px; color: #666; text-transform: uppercase; font-weight: bold; margin-bottom: 4px; }
            .info-value { font-size: 16px; font-weight: 600; color: #222; }
            
            h2 { font-size: 18px; color: #333; margin-top: 40px; margin-bottom: 10px; }
            
            @media print {
                body { padding: 0; }
                @page { margin: 2cm; }
            }
        </style></head><body>
        
        <div class="header">
            <div>
                <h1>PEDIDO #${o.id}</h1>
                <div style="margin-top: 8px; color: #666; font-size: 14px;">Emissão: ${formatDate(o.created_at)} por ${o.created_by_name}</div>
            </div>
            <div class="status ${o.achieved ? 'concluido' : 'pendente'}">
                ${o.achieved ? 'CONCLUÍDO' : 'PENDENTE'}
            </div>
        </div>

        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">Cliente</div>
                <div class="info-value">${o.client_name}</div>
            </div>
            <div class="info-box">
                <div class="info-label">Quantidade Solicitada Total</div>
                <div class="info-value">${o.quant_caixa_solicitada} ${o.lotes?.[0]?.product_name?.toLowerCase().includes('25kg') ? 'Sacos' : 'Caixas'}</div>
            </div>
        </div>

        <h2>Lotes Vinculados</h2>
        ${makeLotesTable()}

        </body></html>
    `

    const w = window.open('', '_blank', 'width=800,height=600')
    w.document.write(html)
    w.document.close()
    w.focus()
    setTimeout(() => { w.print(); w.close() }, 500)
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
