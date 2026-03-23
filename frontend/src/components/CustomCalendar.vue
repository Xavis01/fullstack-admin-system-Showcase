<template>
  <div class="relative w-full" ref="calendarContainer">
    <!-- Input Display -->
    <div class="relative items-center">
      <input type="text" ref="inputRef" :placeholder="placeholder" :value="inputValue" @input="handleInput"
        @keydown="handleKeydown" @focus="openCalendar"
        class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 leading-tight transition duration-200 outline-none"
        :class="{
          'border-red-500 bg-white': isOpen,
          'hover:border-gray-400': !isOpen
        }" />
      <Calendar class="w-5 h-5 text-gray-600 absolute right-3 top-1/2 -translate-y-1/2 cursor-pointer"
        @click="toggleCalendar" />
    </div>

    <!-- Calendar Dropdown -->
    <Teleport to="body">
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
        <div v-if="isOpen" ref="dropdownRef"
          class="fixed z-[60] bg-white border-2 border-gray-300 rounded-lg shadow-lg p-4 w-64" :style="dropdownStyle">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
          <button type="button" @click="prevMonth" class="p-1 hover:bg-gray-100 rounded-full transition">
            <ChevronLeft class="w-5 h-5 text-gray-600" />
          </button>
          <span class="font-bold text-gray-700 capitalize">
            {{ currentMonthName }} {{ currentYear }}
          </span>
          <button type="button" @click="nextMonth" class="p-1 hover:bg-gray-100 rounded-full transition">
            <ChevronRight class="w-5 h-5 text-gray-600" />
          </button>
        </div>

        <!-- Days Header -->
        <div class="grid grid-cols-7 gap-1 mb-2 text-center">
          <span v-for="day in weekDays" :key="day" class="text-xs font-bold text-gray-500">
            {{ day }}
          </span>
        </div>

        <!-- Days Grid -->
        <div class="grid grid-cols-7 gap-1">
          <!-- Empty slots for previous month -->
          <div v-for="n in startDayOfWeek" :key="'empty-' + n" class="h-8"></div>

          <!-- Days -->
          <button type="button" v-for="day in daysInMonth" :key="day" @click="selectDate(day)"
            class="h-8 w-8 rounded-full flex items-center justify-center text-sm transition duration-200 hover:bg-red-50 hover:text-red-600"
            :class="{
              'bg-red-600 text-white hover:bg-red-700 hover:text-white': isSelected(day),
              'text-gray-700': !isSelected(day),
              'font-bold': isToday(day)
            }">
            {{ day }}
          </button>
        </div>
      </div>
    </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { Calendar, ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String, // Format: YYYY-MM-DD
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Selecione uma data'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const calendarContainer = ref(null)
const dropdownRef = ref(null)
const dropdownStyle = ref({})

// Date Logic
const currentDate = ref(new Date())
const displayDate = ref(new Date()) // For navigating months without changing selection

const weekDays = ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']

const currentMonthName = computed(() => {
  return displayDate.value.toLocaleString('pt-BR', { month: 'long' })
})

const currentYear = computed(() => {
  return displayDate.value.getFullYear()
})

const daysInMonth = computed(() => {
  const year = displayDate.value.getFullYear()
  const month = displayDate.value.getMonth()
  return new Date(year, month + 1, 0).getDate()
})

const startDayOfWeek = computed(() => {
  const year = displayDate.value.getFullYear()
  const month = displayDate.value.getMonth()
  return new Date(year, month, 1).getDay()
})

const inputValue = ref('')

// Initialize input value from modelValue
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    const [year, month, day] = newVal.split('-')
    inputValue.value = `${day}/${month}/${year}`
  } else {
    inputValue.value = ''
  }
}, { immediate: true })

const handleKeydown = (e) => {
  // Allow navigation keys
  if (['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(e.key)) return

  // Block input if max length reached (10 chars: DD/MM/YYYY) and no selection
  if (e.target.value.length >= 10) {
    const hasSelection = e.target.selectionStart !== e.target.selectionEnd
    if (!hasSelection) {
      e.preventDefault()
      return
    }
  }

  // Allow numbers
  if (/^[0-9]$/.test(e.key)) return

  // Block everything else
  e.preventDefault()
}

const handleInput = (e) => {
  let value = e.target.value.replace(/\D/g, '') // Ensure only digits

  // Limits
  const currentYear = new Date().getFullYear()

  // 1. Day Masking
  if (value.length >= 2) {
    let day = parseInt(value.slice(0, 2))
    // Prevent 00 or > 31
    if (value.slice(0, 2).length === 2) {
      if (day > 31) day = 31
      if (day === 0) day = 1
      value = String(day).padStart(2, '0') + value.slice(2)
    }
  }

  // 2. Month Masking
  if (value.length >= 4) {
    let month = parseInt(value.slice(2, 4))
    if (value.slice(2, 4).length === 2) {
      if (month > 12) month = 12
      if (month === 0) month = 1
      value = value.slice(0, 2) + String(month).padStart(2, '0') + value.slice(4)
    }
  }

  // 3. Year Masking
  if (value.length >= 8) {
    let yearStr = value.slice(4, 8)
    let year = parseInt(yearStr)

    // Only clamp year if 4 digits are present
    if (yearStr.length === 4) {
      if (year > currentYear) year = currentYear
      value = value.slice(0, 4) + String(year)
    }
  }

  // Limit length
  if (value.length > 8) value = value.slice(0, 8)

  // Construct Formatted Value
  let formattedValue = ''
  if (value.length > 0) {
    formattedValue = value.slice(0, 2)
  }
  if (value.length > 2) {
    formattedValue += '/' + value.slice(2, 4)
  }
  if (value.length > 4) {
    formattedValue += '/' + value.slice(4, 8)
  }

  inputValue.value = formattedValue

  // Emit if valid date
  if (formattedValue.length === 10) {
    const [day, month, year] = formattedValue.split('/').map(Number)
    // Check Validity
    if (day > 0 && day <= 31 && month > 0 && month <= 12 && year >= 1900 && year <= currentYear) {
      const date = new Date(year, month - 1, day)
      // Check calendar validity (e.g. 31/02 -> invalid)
      if (date.getDate() === day && date.getMonth() === month - 1) {
        const y = String(year)
        const m = String(month).padStart(2, '0')
        const d = String(day).padStart(2, '0')
        emit('update:modelValue', `${y}-${m}-${d}`)
        displayDate.value = new Date(year, month - 1, day)
      }
    }
  } else if (value.length === 0) {
    emit('update:modelValue', '')
  }
}

const openCalendar = async () => {
  isOpen.value = true
  await nextTick()
  updatePosition()
}


const isSelected = (day) => {
  if (!props.modelValue) return false
  const [year, month, d] = props.modelValue.split('-').map(Number)
  return (
    day === d &&
    displayDate.value.getMonth() === month - 1 &&
    displayDate.value.getFullYear() === year
  )
}

const isToday = (day) => {
  const today = new Date()
  return (
    day === today.getDate() &&
    displayDate.value.getMonth() === today.getMonth() &&
    displayDate.value.getFullYear() === today.getFullYear()
  )
}

// Actions
const toggleCalendar = async () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    if (props.modelValue) {
      const [year, month, day] = props.modelValue.split('-').map(Number)
      displayDate.value = new Date(year, month - 1, day)
    } else {
      displayDate.value = new Date()
    }
    await nextTick()
    updatePosition()
  }
}

const updatePosition = () => {
  if (!calendarContainer.value || !dropdownRef.value) return

  const containerRect = calendarContainer.value.getBoundingClientRect()
  const dropdownRect = dropdownRef.value.getBoundingClientRect()
  const viewportHeight = window.innerHeight
  const viewportWidth = window.innerWidth

  // Mobile detection (< 768px) - use bottom-center positioning
  if (viewportWidth < 768) {
    const spaceBelow = viewportHeight - containerRect.bottom
    const spaceAbove = containerRect.top

    // Vertical positioning
    if (spaceBelow >= dropdownRect.height + 8) {
      // Enough space below - show below
      dropdownStyle.value = {
        top: `${containerRect.bottom + 4}px`,
        left: `${containerRect.left}px`
      }
    } else if (spaceAbove >= dropdownRect.height + 8) {
      // Not enough space below but enough above - show above
      dropdownStyle.value = {
        bottom: `${viewportHeight - containerRect.top + 4}px`,
        left: `${containerRect.left}px`
      }
    } else {
      // Not enough space either way - show below with scroll
      dropdownStyle.value = {
        top: `${containerRect.bottom + 4}px`,
        left: `${containerRect.left}px`
      }
    }
    return
  }

  // Desktop - use side positioning
  let style = {}

  // Try right side first
  const spaceRight = viewportWidth - containerRect.right
  const spaceLeft = containerRect.left

  if (spaceRight >= dropdownRect.width + 10) {
    // Show on right
    style.left = `${containerRect.right + 10}px`
    style.top = `${containerRect.top}px`
  } else if (spaceLeft >= dropdownRect.width + 10) {
    // Show on left
    style.right = `${viewportWidth - containerRect.left + 10}px`
    style.top = `${containerRect.top}px`
  } else {
    // Not enough space on sides, show below
    style.left = `${containerRect.left}px`
    style.top = `${containerRect.bottom + 4}px`
  }

  // Adjust if goes off screen vertically
  const potentialBottom = containerRect.top + dropdownRect.height
  if (potentialBottom > viewportHeight && style.top) {
    style.top = `${Math.max(8, viewportHeight - dropdownRect.height - 8)}px`
  }

  dropdownStyle.value = style
}

const prevMonth = () => {
  displayDate.value = new Date(displayDate.value.getFullYear(), displayDate.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  displayDate.value = new Date(displayDate.value.getFullYear(), displayDate.value.getMonth() + 1, 1)
}

const selectDate = (day) => {
  const year = displayDate.value.getFullYear()
  const month = String(displayDate.value.getMonth() + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  const dateString = `${year}-${month}-${d}`

  emit('update:modelValue', dateString)
  isOpen.value = false
}

const handleClickOutside = (event) => {
  const isOutsideContainer = calendarContainer.value && !calendarContainer.value.contains(event.target)
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
