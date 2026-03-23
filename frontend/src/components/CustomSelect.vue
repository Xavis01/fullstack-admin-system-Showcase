<template>
  <div class="relative w-full" ref="selectContainer">
    <!-- Selected Value Display -->
    <div @click="toggleDropdown"
      class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 leading-tight cursor-pointer transition duration-200 flex items-center justify-between"
      :class="{
        'border-red-500 bg-white': isOpen,
        'hover:border-gray-400': !isOpen && !disabled && !loading,
        'opacity-50 cursor-not-allowed': disabled,
        'opacity-50 cursor-wait': loading
      }">
      <div class="flex items-center gap-2">
        <img v-if="selectedOption?.image" :src="selectedOption.image"
          class="w-6 h-6 object-cover rounded-full border border-gray-200" alt="" />
        <component v-if="selectedOption?.icon" :is="selectedOption.icon" class="w-5 h-5 text-gray-500" />
        <span :class="{ 'text-gray-400': !selectedOption }">
          {{ selectedOption?.label || placeholder }}
        </span>
      </div>
      <svg v-if="!loading" class="fill-current h-5 w-5 text-gray-600 transition-transform duration-200"
        :class="{ 'rotate-180': isOpen }" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
        <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
      </svg>
      <div v-else class="flex items-center justify-center w-5 h-5">
        <LoaderCircle class="animate-spin text-gray-600 w-5 h-5" />
      </div>
    </div>

    <!-- Dropdown Options -->
    <Teleport to="body">
      <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
        <div v-if="isOpen" :style="dropdownStyle"
          class="fixed z-[9999] bg-white border-2 border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
          <div v-for="option in options" :key="option.value" @click="selectOption(option)"
            class="px-3 py-2 cursor-pointer transition duration-150 hover:bg-red-50 hover:text-red-600 first:rounded-t-lg last:rounded-b-lg flex items-center gap-2"
            :class="[
              option.class,
              modelValue === option.value ? 'bg-red-100 text-red-600 font-semibold' : 'text-gray-700'
            ]">
            <img v-if="option.image" :src="option.image"
              class="w-6 h-6 object-cover rounded-full border border-gray-200" alt="" />
            <component v-if="option.icon" :is="option.icon" class="w-5 h-5 text-gray-500" />
            <span>{{ option.label }}</span>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { LoaderCircle } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: [String, Number, null],
    default: null
  },
  options: {
    type: Array,
    required: true
  },
  placeholder: {
    type: String,
    default: 'Selecione...'
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const selectContainer = ref(null)

const selectedOption = computed(() => {
  return props.options.find(option => option.value === props.modelValue)
})

const dropdownStyle = computed(() => {
  if (!selectContainer.value) return {}

  const rect = selectContainer.value.getBoundingClientRect()
  return {
    top: `${rect.bottom + 4}px`,
    left: `${rect.left}px`,
    width: `${rect.width}px`
  }
})

const toggleDropdown = () => {
  if (props.loading || props.disabled) return
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  isOpen.value = false
}

const handleClickOutside = (event) => {
  if (selectContainer.value && !selectContainer.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
