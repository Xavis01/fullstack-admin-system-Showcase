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
                class="fixed inset-0 flex items-center justify-center z-[60] font-montserrat px-3 md:px-4 pt-36 pb-6">
                <div class="absolute inset-0 bg-black/50" @click="$emit('close')"></div>
                <transition name="modal">
                    <div v-if="isOpen"
                        class="bg-white rounded-xl shadow-2xl z-10 w-full max-w-5xl flex flex-col overflow-hidden max-h-full">

                        <!-- Header -->
                        <div
                            class="bg-neutral-800 text-white px-4 md:px-6 py-3 md:py-4 flex items-center justify-between shrink-0 rounded-t-xl">
                            <div class="flex items-center gap-3">
                                <div class="bg-red-600 p-2 rounded-lg">
                                    <FileText class="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 class="text-base md:text-lg font-bold">RELATÓRIO ESCORPIÃO</h3>
                                    <p class="text-white/60 text-xs font-medium">{{ periodLabel }}</p>
                                </div>
                            </div>
                            <div class="flex items-center gap-1.5 md:gap-2">
                                <!-- Export Buttons -->
                                <button @click="exportPDF" title="Baixar PDF"
                                    class="bg-red-600 hover:bg-red-700 active:scale-95 text-white p-2 md:px-3 md:py-2 rounded-lg transition flex items-center gap-1.5 text-xs font-bold">
                                    <Download class="w-4 h-4" />
                                    <span class="hidden md:inline">PDF</span>
                                </button>
                                <button @click="printReport" title="Imprimir"
                                    class="bg-white/10 hover:bg-white/20 active:scale-95 text-white p-2 md:px-3 md:py-2 rounded-lg transition flex items-center gap-1.5 text-xs font-bold">
                                    <Printer class="w-4 h-4" />
                                    <span class="hidden md:inline">IMPRIMIR</span>
                                </button>
                                <button @click="copyText" title="Copiar texto"
                                    class="bg-white/10 hover:bg-white/20 active:scale-95 text-white p-2 md:px-3 md:py-2 rounded-lg transition flex items-center gap-1.5 text-xs font-bold">
                                    <Copy class="w-4 h-4" />
                                    <span class="hidden md:inline">COPIAR</span>
                                </button>
                                <button @click="$emit('close')"
                                    class="text-white/50 hover:text-white transition p-1 rounded-full hover:bg-white/10 ml-1">
                                    <X class="w-5 h-5" />
                                </button>
                            </div>
                        </div>

                        <!-- Report Body -->
                        <div ref="reportBody" class="flex-1 overflow-y-auto p-4 md:p-6 space-y-5 custom-scrollbar">
                            <template v-if="reportData">
                                <!-- KPI Row -->
                                <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                                    <div
                                        class="bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-xl p-4 text-center">
                                        <p class="text-[10px] font-bold text-blue-500 uppercase tracking-wider mb-1">
                                            Total Vendas</p>
                                        <p class="text-xl md:text-2xl font-extrabold text-blue-700">{{
                                            reportData.total_sales.toLocaleString('pt-BR') }}</p>
                                    </div>
                                    <div
                                        class="bg-gradient-to-br from-green-50 to-green-100 border border-green-200 rounded-xl p-4 text-center">
                                        <p class="text-[10px] font-bold text-green-500 uppercase tracking-wider mb-1">
                                            Total Produção</p>
                                        <p class="text-xl md:text-2xl font-extrabold text-green-700">{{
                                            reportData.total_production.toLocaleString('pt-BR') }}</p>
                                    </div>
                                    <div
                                        class="bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-xl p-4 text-center">
                                        <p class="text-[10px] font-bold text-purple-500 uppercase tracking-wider mb-1">
                                            Produtos</p>
                                        <p class="text-xl md:text-2xl font-extrabold text-purple-700">{{
                                            reportData.stock_by_product.length }}</p>
                                        <p class="text-[10px] text-purple-400 font-semibold">itens</p>
                                    </div>
                                    <div
                                        class="bg-gradient-to-br from-amber-50 to-amber-100 border border-amber-200 rounded-xl p-4 text-center">
                                        <p class="text-[10px] font-bold text-amber-500 uppercase tracking-wider mb-1">
                                            Clientes</p>
                                        <p class="text-xl md:text-2xl font-extrabold text-amber-700">{{
                                            reportData.purchases_by_client.length }}</p>
                                        <p class="text-[10px] text-amber-400 font-semibold">ativos</p>
                                    </div>
                                </div>

                                <!-- Estoque Atual -->
                                <div class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                                    <div class="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center gap-2">
                                        <Package class="w-4 h-4 text-gray-500" />
                                        <h4 class="text-xs font-bold text-gray-700 uppercase tracking-wide">Estoque
                                            Atual por Produto</h4>
                                    </div>
                                    <div class="divide-y divide-gray-100">
                                        <div v-for="item in reportData.stock_by_product" :key="'stock-' + item.product"
                                            class="flex items-center justify-between px-4 py-2.5 hover:bg-gray-50 transition">
                                            <span class="text-sm font-semibold text-neutral-800">{{ item.product
                                                }}</span>
                                            <span
                                                class="text-sm font-bold text-neutral-700 bg-gray-100 px-3 py-1 rounded-full">{{
                                                    item.stock.toLocaleString('pt-BR') }} {{ getUnit(item.product) }}</span>
                                        </div>
                                        <div v-if="reportData.stock_by_product.length === 0"
                                            class="px-4 py-4 text-sm text-gray-400 text-center italic">Nenhum dado</div>
                                    </div>
                                </div>

                                <!-- Vendas e Produção side by side -->
                                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                    <!-- Vendas por Produto -->
                                    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                                        <div
                                            class="bg-blue-50 px-4 py-3 border-b border-blue-100 flex items-center gap-2">
                                            <ShoppingBag class="w-4 h-4 text-blue-500" />
                                            <h4 class="text-xs font-bold text-blue-700 uppercase tracking-wide">Vendas
                                                por Produto</h4>
                                        </div>
                                        <div class="divide-y divide-gray-100">
                                            <div v-for="item in reportData.sales_by_product"
                                                :key="'sales-' + item.product"
                                                class="flex items-center justify-between px-4 py-2.5">
                                                <span class="text-sm font-semibold text-neutral-800">{{ item.product
                                                    }}</span>
                                                <span class="text-sm font-bold text-blue-600">{{
                                                    item.total.toLocaleString('pt-BR') }} {{ getUnit(item.product)
                                                    }}</span>
                                            </div>
                                            <div v-if="reportData.sales_by_product.length === 0"
                                                class="px-4 py-4 text-sm text-gray-400 text-center italic">Nenhum dado
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Produção por Produto -->
                                    <div class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                                        <div
                                            class="bg-green-50 px-4 py-3 border-b border-green-100 flex items-center gap-2">
                                            <Factory class="w-4 h-4 text-green-500" />
                                            <h4 class="text-xs font-bold text-green-700 uppercase tracking-wide">
                                                Produção por Produto</h4>
                                        </div>
                                        <div class="divide-y divide-gray-100">
                                            <div v-for="item in reportData.production_by_product"
                                                :key="'prod-' + item.product"
                                                class="flex items-center justify-between px-4 py-2.5">
                                                <span class="text-sm font-semibold text-neutral-800">{{ item.product
                                                    }}</span>
                                                <span class="text-sm font-bold text-green-600">{{
                                                    item.total.toLocaleString('pt-BR') }} {{ getUnit(item.product)
                                                    }}</span>
                                            </div>
                                            <div v-if="reportData.production_by_product.length === 0"
                                                class="px-4 py-4 text-sm text-gray-400 text-center italic">Nenhum dado
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Compras por Cliente -->
                                <div class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                                    <div
                                        class="bg-amber-50 px-4 py-3 border-b border-amber-100 flex items-center gap-2">
                                        <Users class="w-4 h-4 text-amber-500" />
                                        <h4 class="text-xs font-bold text-amber-700 uppercase tracking-wide">Compras por
                                            Cliente</h4>
                                    </div>
                                    <div class="divide-y divide-gray-100">
                                        <div v-for="item in reportData.purchases_by_client"
                                            :key="'client-' + item.client"
                                            class="flex items-center justify-between px-4 py-2.5 hover:bg-gray-50 transition">
                                            <span class="text-sm font-semibold text-neutral-800">{{ item.client
                                                }}</span>
                                            <span class="text-sm font-bold text-amber-600">{{
                                                item.total.toLocaleString('pt-BR') }} {{ getUnit(item.client, true)
                                                }}</span>
                                        </div>
                                        <div v-if="reportData.purchases_by_client.length === 0"
                                            class="px-4 py-4 text-sm text-gray-400 text-center italic">Nenhum dado</div>
                                    </div>
                                </div>

                            </template>
                        </div>
                    </div>
                </transition>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import {
    FileText, Download, Printer, Copy, X,
    Package, ShoppingBag, Factory, Users
} from 'lucide-vue-next'
import { useToastStore } from '../../stores/toast'

const props = defineProps({
    isOpen: Boolean,
    reportData: Object,
    periodLabel: String
})
defineEmits(['close'])

const toastStore = useToastStore()
const reportBody = ref(null)

const getUnit = (name, isClient = false) => {
    if (isClient) return ''
    return name?.toLowerCase().includes('25kg') ? 'sc' : 'cx'
}

// ============= COPY TEXT =============
const copyText = () => {
    if (!props.reportData) return
    const d = props.reportData
    const lines = []

    lines.push('═══════════════════════════════════════')
    lines.push('         RELATÓRIO ESCORPIÃO')
    lines.push(`         Período: ${props.periodLabel}`)
    lines.push('═══════════════════════════════════════')
    lines.push('')

    // Totals
    lines.push('📊 RESUMO GERAL')
    lines.push('───────────────────────────────────────')
    lines.push(`  Total de Vendas:    ${d.total_sales.toLocaleString('pt-BR')}`)
    lines.push(`  Total de Produção:  ${d.total_production.toLocaleString('pt-BR')}`)
    lines.push('')

    // Stock
    lines.push('📦 ESTOQUE ATUAL POR PRODUTO')
    lines.push('───────────────────────────────────────')
    if (d.stock_by_product.length > 0) {
        for (const item of d.stock_by_product) {
            lines.push(`  ${item.product.padEnd(30)} ${String(item.stock.toLocaleString('pt-BR')).padStart(8)} ${getUnit(item.product)}`)
        }
    } else {
        lines.push('  Sem dados')
    }
    lines.push('')

    // Sales by product
    lines.push('🛒 VENDAS POR PRODUTO')
    lines.push('───────────────────────────────────────')
    if (d.sales_by_product.length > 0) {
        for (const item of d.sales_by_product) {
            lines.push(`  ${item.product.padEnd(30)} ${String(item.total.toLocaleString('pt-BR')).padStart(8)} ${getUnit(item.product)}`)
        }
    } else {
        lines.push('  Sem dados')
    }
    lines.push('')

    // Production by product
    lines.push('🏭 PRODUÇÃO POR PRODUTO')
    lines.push('───────────────────────────────────────')
    if (d.production_by_product.length > 0) {
        for (const item of d.production_by_product) {
            lines.push(`  ${item.product.padEnd(30)} ${String(item.total.toLocaleString('pt-BR')).padStart(8)} ${getUnit(item.product)}`)
        }
    } else {
        lines.push('  Sem dados')
    }
    lines.push('')

    // Purchases by client
    lines.push('👥 COMPRAS POR CLIENTE')
    lines.push('───────────────────────────────────────')
    if (d.purchases_by_client.length > 0) {
        for (const item of d.purchases_by_client) {
            lines.push(`  ${item.client.padEnd(30)} ${String(item.total.toLocaleString('pt-BR')).padStart(8)}`)
        }
    } else {
        lines.push('  Sem dados')
    }
    lines.push('')
    lines.push('═══════════════════════════════════════')

    const text = lines.join('\n')
    const fallbackCopy = () => {
        const ta = document.createElement('textarea')
        ta.value = text
        ta.style.position = 'fixed'
        ta.style.top = '0'
        ta.style.left = '0'
        ta.style.opacity = '0'
        document.body.appendChild(ta)
        ta.focus()
        ta.select()
        try {
            document.execCommand('copy')
            toastStore.add({ title: 'Copiado!', message: 'Relatório copiado para a área de transferência.', type: 'success' })
        } catch {
            toastStore.add({ title: 'Erro', message: 'Não foi possível copiar o relatório.', type: 'error' })
        }
        document.body.removeChild(ta)
    }

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text)
            .then(() => toastStore.add({ title: 'Copiado!', message: 'Relatório copiado para a área de transferência.', type: 'success' }))
            .catch(() => fallbackCopy())
    } else {
        fallbackCopy()
    }
}

// ============= PRINT =============
const printReport = () => {
    if (!props.reportData) return
    const d = props.reportData

    const makeTable = (headers, rows) => {
        let html = '<table style="width:100%;border-collapse:collapse;margin-bottom:16px;font-size:13px;">'
        html += '<thead><tr>'
        for (const h of headers) {
            html += `<th style="text-align:left;padding:8px 12px;border-bottom:2px solid #333;font-weight:700;">${h}</th>`
        }
        html += '</tr></thead><tbody>'
        for (const row of rows) {
            html += '<tr>'
            for (const cell of row) {
                html += `<td style="padding:6px 12px;border-bottom:1px solid #ddd;">${cell}</td>`
            }
            html += '</tr>'
        }
        html += '</tbody></table>'
        return html
    }

    let html = `
        <html><head><title>Relatório Escorpião</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; padding: 30px; color: #222; }
            h1 { font-size: 22px; margin-bottom: 4px; }
            h2 { font-size: 15px; margin-top: 24px; margin-bottom: 8px; padding-bottom: 4px; border-bottom: 2px solid #dc2626; color: #333; }
            .subtitle { color: #888; font-size: 13px; margin-bottom: 20px; }
            .kpi-row { display: flex; gap: 16px; margin-bottom: 20px; }
            .kpi { flex: 1; text-align: center; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }
            .kpi-value { font-size: 22px; font-weight: 800; }
            .kpi-label { font-size: 11px; color: #888; text-transform: uppercase; }
        </style></head><body>
        <h1>RELATÓRIO ESCORPIÃO</h1>
        <p class="subtitle">Período: ${props.periodLabel}</p>

        <div class="kpi-row">
            <div class="kpi"><div class="kpi-value">${d.total_sales.toLocaleString('pt-BR')}</div><div class="kpi-label">Total Vendas</div></div>
            <div class="kpi"><div class="kpi-value">${d.total_production.toLocaleString('pt-BR')}</div><div class="kpi-label">Total Produção</div></div>
        </div>

        <h2>Estoque Atual por Produto</h2>
        ${makeTable(['Produto', 'Estoque'], d.stock_by_product.map(i => [i.product, `${i.stock.toLocaleString('pt-BR')} ${getUnit(i.product)}`]))}

        <h2>Vendas por Produto</h2>
        ${makeTable(['Produto', 'Vendas'], d.sales_by_product.map(i => [i.product, `${i.total.toLocaleString('pt-BR')} ${getUnit(i.product)}`]))}

        <h2>Produção por Produto</h2>
        ${makeTable(['Produto', 'Produção'], d.production_by_product.map(i => [i.product, `${i.total.toLocaleString('pt-BR')} ${getUnit(i.product)}`]))}

        <h2>Compras por Cliente</h2>
        ${makeTable(['Cliente', 'Total'], d.purchases_by_client.map(i => [i.client, `${i.total.toLocaleString('pt-BR')}`]))}

        </body></html>
    `

    const w = window.open('', '_blank', 'width=800,height=600')
    w.document.write(html)
    w.document.close()
    w.focus()
    setTimeout(() => { w.print(); w.close() }, 500)
}

// ============= PDF =============
const exportPDF = async () => {
    if (!props.reportData) return
    const d = props.reportData

    try {
        // Dynamic import jspdf
        const jspdfModule = await import('jspdf')
        const jsPDF = jspdfModule.jsPDF || jspdfModule.default
        const autoTableModule = await import('jspdf-autotable')
        const autoTable = autoTableModule.default || autoTableModule

        const doc = new jsPDF('p', 'mm', 'a4')
        const pageWidth = doc.internal.pageSize.getWidth()
        let y = 15

        // Title
        doc.setFontSize(20)
        doc.setFont('helvetica', 'bold')
        doc.text('RELATORIO ESCORPIAO', pageWidth / 2, y, { align: 'center' })
        y += 8

        doc.setFontSize(11)
        doc.setFont('helvetica', 'normal')
        doc.setTextColor(120)
        doc.text(`Periodo: ${props.periodLabel}`, pageWidth / 2, y, { align: 'center' })
        doc.setTextColor(0)
        y += 10

        // Line
        doc.setDrawColor(220, 38, 38)
        doc.setLineWidth(0.8)
        doc.line(15, y, pageWidth - 15, y)
        y += 8

        // KPIs
        doc.setFontSize(11)
        doc.setFont('helvetica', 'bold')
        doc.text(`Total Vendas: ${d.total_sales.toLocaleString('pt-BR')}`, 15, y)
        doc.text(`Total Producao: ${d.total_production.toLocaleString('pt-BR')}`, pageWidth / 2, y)
        y += 10

        // Helper function for tables
        const addTable = (title, head, body) => {
            if (y > 260) { doc.addPage(); y = 15 }
            doc.setFontSize(12)
            doc.setFont('helvetica', 'bold')
            doc.setTextColor(51)
            doc.text(title, 15, y)
            doc.setTextColor(0)
            y += 2

            autoTable(doc, {
                startY: y,
                head: [head],
                body: body,
                theme: 'striped',
                margin: { left: 15, right: 15 },
                headStyles: { fillColor: [51, 51, 51], fontSize: 9, fontStyle: 'bold' },
                bodyStyles: { fontSize: 9 },
                styles: { cellPadding: 3 }
            })
            y = doc.lastAutoTable.finalY + 8
        }

        addTable('Estoque Atual por Produto', ['Produto', 'Estoque'],
            d.stock_by_product.map(i => [i.product, `${i.stock.toLocaleString('pt-BR')} ${getUnit(i.product)}`]))

        addTable('Vendas por Produto', ['Produto', 'Vendas'],
            d.sales_by_product.map(i => [i.product, `${i.total.toLocaleString('pt-BR')} ${getUnit(i.product)}`]))

        addTable('Producao por Produto', ['Produto', 'Producao'],
            d.production_by_product.map(i => [i.product, `${i.total.toLocaleString('pt-BR')} ${getUnit(i.product)}`]))

        addTable('Compras por Cliente', ['Cliente', 'Total'],
            d.purchases_by_client.map(i => [i.client, `${i.total.toLocaleString('pt-BR')}`]))

        doc.save(`relatorio_escorpiao_${new Date().toISOString().slice(0, 10)}.pdf`)
        toastStore.add({ title: 'PDF Gerado!', message: 'Relatório baixado com sucesso.', type: 'success' })
    } catch (e) {
        console.error('Erro ao gerar PDF:', e)
        toastStore.add({ title: 'Erro', message: 'Falha ao gerar PDF: ' + e.message, type: 'error' })
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
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #d1d5db;
    border-radius: 9999px;
}
</style>
