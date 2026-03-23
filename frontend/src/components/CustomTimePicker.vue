<template>
  <div class="relative w-full" ref="timePickerContainer">
    <!-- Input Display -->
    <div class="relative items-center">
      <input type="text" ref="inputRef" :placeholder="placeholder" :value="inputValue" @input="handleInput"
        @keydown="handleKeydown" @focus="openPicker"
        class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 leading-tight transition duration-200 outline-none"
        :class="{
          'border-red-500 bg-white': isOpen,
          'hover:border-gray-400': !isOpen
        }" />
      <Clock class="w-5 h-5 text-gray-600 absolute right-3 top-1/2 -translate-y-1/2 cursor-pointer"
        @click="togglePicker" />
    </div>

    <!-- Time Picker Dropdown -->
    <Teleport to="body">
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
        <div v-if="isOpen" ref="dropdownRef"
          class="fixed z-[60] bg-white border-2 border-gray-300 rounded-lg shadow-lg overflow-hidden flex"
          :style="dropdownStyle">
        
        <!-- Hours Column -->
        <div class="w-20 border-r border-gray-200 h-64 overflow-y-auto custom-scrollbar" ref="hoursContainer">
          <button type="button" v-for="h in 24" :key="'h-' + (h - 1)"
            @click="selectHour(h - 1)"
            class="w-full text-center py-2 text-sm font-semibold transition duration-200 hover:bg-red-50 hover:text-red-600"
            :class="{
              'bg-red-600 text-white hover:bg-red-700 hover:text-white': isHourSelected(h - 1),
              'text-gray-700': !isHourSelected(h - 1)
            }">
            {{ formatNumber(h - 1) }}
          </button>
        </div>

        <!-- Minutes Column -->
        <div class="w-20 h-64 overflow-y-auto custom-scrollbar" ref="minutesContainer">
          <button type="button" v-for="m in 60" :key="'m-' + (m - 1)"
            @click="selectMinute(m - 1)"
            class="w-full text-center py-2 text-sm font-semibold transition duration-200 hover:bg-red-50 hover:text-red-600"
            :class="{
              'bg-red-600 text-white hover:bg-red-700 hover:text-white': isMinuteSelected(m - 1),
              'text-gray-700': !isMinuteSelected(m - 1)
            }">
            {{ formatNumber(m - 1) }}
          </button>
        </div>

      </div>
    </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { Clock } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String, // Format: HH:mm
    default: ''
  },
  placeholder: {
    type: String,
    default: '00:00'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const timePickerContainer = ref(null)
const dropdownRef = ref(null)
const dropdownStyle = ref({})

const hoursContainer = ref(null)
const minutesContainer = ref(null)

const inputValue = ref('')

const selectedHour = ref(null)
const selectedMinute = ref(null)

// Initialize values
watch(() => props.modelValue, (newVal) => {
  inputValue.value = newVal || ''
  if (newVal && newVal.length === 5) {
    const [h, m] = newVal.split(':').map(Number)
    if (!isNaN(h) && !isNaN(m)) {
      selectedHour.value = h
      selectedMinute.value = m
    }
  } else {
    selectedHour.value = null
    selectedMinute.value = null
  }
}, { immediate: true })

const formatNumber = (num) => String(num).padStart(2, '0')

const isHourSelected = (h) => selectedHour.value === h
const isMinuteSelected = (m) => selectedMinute.value === m

const selectHour = (h) => {
  selectedHour.value = h
  if (selectedMinute.value === null) selectedMinute.value = 0
  updateValue()
}

const selectMinute = (m) => {
  selectedMinute.value = m
  if (selectedHour.value === null) selectedHour.value = 0
  updateValue()
  // Optional: close on minute selection
  // isOpen.value = false
}

const updateValue = () => {
  if (selectedHour.value !== null && selectedMinute.value !== null) {
    const val = `${formatNumber(selectedHour.value)}:${formatNumber(selectedMinute.value)}`
    inputValue.value = val
    emit('update:modelValue', val)
  }
}

const handleKeydown = (e) => {
  if (['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(e.key)) return

  if (e.target.value.length >= 5) {
    const hasSelection = e.target.selectionStart !== e.target.selectionEnd
    if (!hasSelection) {
      e.preventDefault()
      return
    }
  }

  if (/^[0-9]$/.test(e.key)) return
  e.preventDefault()
}

const handleInput = (e) => {
  let value = e.target.value.replace(/\D/g, '')

  if (value.length >= 2) {
    let hh = parseInt(value.slice(0, 2))
    if (value.slice(0, 2).length === 2) {
      if (hh > 23) hh = 23
      value = String(hh).padStart(2, '0') + value.slice(2)
    }
  }

  if (value.length >= 4) {
    let mm = parseInt(value.slice(2, 4))
    if (value.slice(2, 4).length === 2) {
      if (mm > 59) mm = 59
      value = value.slice(0, 2) + String(mm).padStart(2, '0')
    }
  }

  if (value.length > 4) value = value.slice(0, 4)

  let formattedValue = ''
  if (value.length > 0) formattedValue = value.slice(0, 2)
  if (value.length > 2) formattedValue += ':' + value.slice(2, 4)

  inputValue.value = formattedValue

  if (formattedValue.length === 5) {
    emit('update:modelValue', formattedValue)
    const [h, m] = formattedValue.split(':').map(Number)
    selectedHour.value = h
    selectedMinute.value = m
  } else if (value.length === 0) {
    emit('update:modelValue', '')
    selectedHour.value = null
    selectedMinute.value = null
  }
}

const openPicker = async () => {
  isOpen.value = true
  await nextTick()
  updatePosition()
  scrollToSelected()
}

const togglePicker = async () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    await nextTick()
    updatePosition()
    scrollToSelected()
  }
}

const scrollToSelected = () => {
  if (selectedHour.value !== null && hoursContainer.value) {
    const btn = hoursContainer.value.children[selectedHour.value]
    if (btn) btn.scrollIntoView({ block: 'center' })
  }
  if (selectedMinute.value !== null && minutesContainer.value) {
    const btn = minutesContainer.value.children[selectedMinute.value]
    if (btn) btn.scrollIntoView({ block: 'center' })
  }
}

const updatePosition = () => {
  if (!timePickerContainer.value || !dropdownRef.value) return

  const containerRect = timePickerContainer.value.getBoundingClientRect()
  const dropdownRect = dropdownRef.value.getBoundingClientRect()
  const viewportHeight = window.innerHeight
  const viewportWidth = window.innerWidth

  if (viewportWidth < 768) {
    dropdownStyle.value = {
      top: `${containerRect.bottom + 4}px`,
      left: `${containerRect.left}px`
    }
    return
  }

  let style = {}
  const spaceRight = viewportWidth - containerRect.right
  const spaceLeft = containerRect.left

  if (spaceRight >= dropdownRect.width + 10) {
    style.left = `${containerRect.left}px`
    style.top = `${containerRect.bottom + 4}px`
  } else if (spaceLeft >= dropdownRect.width + 10) {
    style.right = `${viewportWidth - containerRect.right}px`
    style.top = `${containerRect.bottom + 4}px`
  } else {
    style.left = `${containerRect.left}px`
    style.top = `${containerRect.bottom + 4}px`
  }

  const potentialBottom = containerRect.bottom + 4 + dropdownRect.height
  if (potentialBottom > viewportHeight && containerRect.top > dropdownRect.height) {
    style.top = `${containerRect.top - dropdownRect.height - 4}px`
  }

  dropdownStyle.value = style
}

const handleClickOutside = (event) => {
  const isOutsideContainer = timePickerContainer.value && !timePickerContainer.value.contains(event.target)
  const isOutsideDropdown = dropdownRef.value ? !dropdownRef.value.contains(event.target) : true
  if (isOutsideContainer && isOutsideDropdown) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', () => {
    if (isOpen.value) updatePosition()
  })
  window.addEventListener('scroll', () => {
    if (isOpen.value) updatePosition()
  }, true)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 4px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #9ca3af;
}
</style>
