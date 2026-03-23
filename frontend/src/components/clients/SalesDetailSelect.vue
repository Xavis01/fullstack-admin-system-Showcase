<template>
  <div class="relative w-full" ref="selectContainer">
    <!-- Trigger Button (Displays Total) -->
    <div @click="toggleDropdown"
      class="w-full bg-transparent text-neutral-800 font-bold cursor-pointer transition duration-200 flex items-center justify-center gap-1.5 group"
      :class="{
        'text-red-600': isOpen,
        'hover:text-red-600': !isOpen && sales.length > 0,
        'cursor-default opacity-80': sales.length === 0
      }">
      <span class="truncate">{{ total }}</span>

      <!-- Arrow Icon -->
      <svg v-if="sales.length > 0" class="fill-current h-4 w-4 transition-transform duration-200 ml-2"
        :class="{ 'rotate-180': isOpen }" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
        <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
      </svg>
    </div>

    <!-- Dropdown Content -->
    <Teleport to="body">
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">

        <div v-if="isOpen && sales.length > 0" ref="dropdownRef"
          :style="{ top: dropdownPosition.top, left: dropdownPosition.left }"
          class="fixed z-[9999] w-64 mt-0 bg-white border border-gray-200 rounded-xl shadow-xl overflow-hidden">

          <!-- Header of Dropdown -->
          <div
            class="px-3 py-2 bg-neutral-100 border-b border-gray-200 text-xs font-bold text-gray-500 uppercase tracking-wider grid grid-cols-[1fr_50px_70px] gap-2">
            <div>LOTE</div>
            <div class="text-center">QTD</div>
            <div class="text-right">DATA</div>
          </div>

          <!-- List -->
          <div class="max-h-60 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent">
            <div v-for="(sale, index) in sales" :key="index"
              class="px-3 py-2 text-sm border-b border-gray-100 last:border-0 hover:bg-neutral-50 transition grid grid-cols-[1fr_50px_70px] gap-2 items-center">

              <div class="font-semibold text-neutral-800 truncate" :title="sale.num_lote">
                {{ sale.num_lote }}
              </div>

              <div class="text-center text-neutral-600 font-medium">
                {{ sale.quant_caixa_vendida }}
              </div>

              <div class="text-right text-xs text-gray-500">
                {{ formatDate(sale.data_venda) }}
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps({
  total: {
    type: [Number, String],
    required: true
  },
  sales: {
    type: Array,
    default: () => []
  }
})

const isOpen = ref(false)
const selectContainer = ref(null)
const dropdownRef = ref(null)
const dropdownPosition = ref({ top: '0px', left: '0px', width: 'auto' })

const calculatePosition = () => {
  if (!selectContainer.value) return
  const rect = selectContainer.value.getBoundingClientRect()
  dropdownPosition.value = {
    top: `${rect.bottom + 8}px`, // 8px margin
    left: `${rect.left}px`,
    width: `${rect.width}px` // match trigger width or min-width
  }
}

const toggleDropdown = async () => {
  if (props.sales.length === 0) return

  if (!isOpen.value) {
    calculatePosition()
    isOpen.value = true
  } else {
    isOpen.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  // Assumes YYYY-MM-DD
  const [year, month, day] = dateString.split('-')
  return `${day}/${month}/${year.slice(2)}` // DD/MM/YY
}

const handleClickOutside = (event) => {
  const isClickInsideTrigger = selectContainer.value && selectContainer.value.contains(event.target)
  const isClickInsideDropdown = dropdownRef.value && dropdownRef.value.contains(event.target)

  if (!isClickInsideTrigger && !isClickInsideDropdown) {
    isOpen.value = false
  }
}

const handleScroll = (event) => {
  if (isOpen.value) {
    // If scrolling happens inside the dropdown, ignore it
    if (dropdownRef.value && (event.target === dropdownRef.value || dropdownRef.value.contains(event.target))) {
      return
    }
    // If scrolling happens outside (e.g. main page scroll), close it
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', handleScroll, true) // capture phase for all scrolls
  window.addEventListener('resize', handleScroll)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', handleScroll, true)
  window.removeEventListener('resize', handleScroll)
})
</script>

<style scoped>
/* Custom Scrollbar for this component specifically if needed, 
   though Tailwind scrollbar plugin might be handling it globally */
</style>
