<template>
    <div class="relative w-full" ref="containerRef">
        <!-- Input Display -->
        <div class="relative">
            <input type="text" readonly :placeholder="placeholder" :value="displayValue" @click="toggleDropdown"
                class="w-full bg-gray-100 text-gray-700 border-2 border-gray-300 rounded-lg h-[44px] px-3 leading-tight transition duration-200 outline-none cursor-pointer"
                :class="{
                    'border-red-500 bg-white': isOpen,
                    'hover:border-gray-400': !isOpen
                }" />
            <svg class="fill-current h-5 w-5 text-gray-600 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none transition-transform duration-200"
                :class="{ 'rotate-180': isOpen }" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
            </svg>
        </div>

        <!-- Dropdown -->
        <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-1"
            enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
            <div v-if="isOpen"
                class="absolute z-50 w-full mt-1 bg-white border-2 border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
                <!-- Select All Option -->
                <div @click="toggleSelectAll"
                    class="px-3 py-2 cursor-pointer transition duration-150 hover:bg-red-50 first:rounded-t-lg flex items-center gap-2 border-b border-gray-200">
                    <div class="w-5 h-5 border-2 border-gray-300 rounded flex items-center justify-center transition-colors duration-200"
                        :class="{ 'bg-red-600 border-red-600': allSelected, 'bg-white': !allSelected }">
                        <Check v-if="allSelected" class="w-3.5 h-3.5 text-white" stroke-width="3" />
                    </div>
                    <span class="font-bold text-gray-700">{{ allOptionLabel }}</span>
                </div>

                <!-- Individual Options -->
                <div v-for="option in options" :key="option.value" @click="toggleOption(option.value)"
                    class="px-3 py-2 cursor-pointer transition duration-150 hover:bg-red-50 last:rounded-b-lg flex items-center gap-2">
                    <div class="w-5 h-5 border-2 border-gray-300 rounded flex items-center justify-center transition-colors duration-200"
                        :class="{ 'bg-red-600 border-red-600': isSelected(option.value), 'bg-white': !isSelected(option.value) }">
                        <Check v-if="isSelected(option.value)" class="w-3.5 h-3.5 text-white" stroke-width="3" />
                    </div>
                    <span class="text-gray-700">{{ option.label }}</span>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { Check } from 'lucide-vue-next'

const props = defineProps({
    modelValue: {
        type: Array,
        default: () => []
    },
    options: {
        type: Array,
        required: true
    },
    placeholder: {
        type: String,
        default: 'Selecione'
    },
    allOptionLabel: {
        type: String,
        default: 'Todos'
    }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const containerRef = ref(null)

const displayValue = computed(() => {
    if (props.modelValue.length === 0) return ''
    if (props.modelValue.length === props.options.length) return props.allOptionLabel
    if (props.modelValue.length === 1) {
        const option = props.options.find(o => o.value === props.modelValue[0])
        return option ? option.label : ''
    }
    return `${props.modelValue.length} selecionados`
})

const allSelected = computed(() => {
    return props.modelValue.length === props.options.length && props.options.length > 0
})

const isSelected = (value) => {
    return props.modelValue.includes(value)
}

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const toggleOption = (value) => {
    const newValue = [...props.modelValue]
    const index = newValue.indexOf(value)

    if (index > -1) {
        newValue.splice(index, 1)
    } else {
        newValue.push(value)
    }

    emit('update:modelValue', newValue)
}

const toggleSelectAll = () => {
    if (allSelected.value) {
        emit('update:modelValue', [])
    } else {
        emit('update:modelValue', props.options.map(o => o.value))
    }
}

const handleClickOutside = (event) => {
    if (containerRef.value && !containerRef.value.contains(event.target)) {
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
