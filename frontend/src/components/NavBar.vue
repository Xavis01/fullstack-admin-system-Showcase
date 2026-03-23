<template>
  <header class="bg-white/80 backdrop-blur-md border-b border-gray-100 fixed top-0 left-0 w-full z-[1000] h-16 md:h-20 transition-all duration-300">
    <div class="max-w-7xl mx-auto flex justify-between items-center px-4 sm:px-6 lg:px-8 h-full">
      <!-- Logo -->
      <router-link to="/" class="flex-shrink-0 flex items-center">
        <img :src="Logo" alt="Logo Soda Escorpião"
          class="h-8 sm:h-10 md:h-12 w-auto object-contain transition-transform duration-300 hover:scale-105" />
      </router-link>

      <!-- Navegação Desktop -->
      <nav class="hidden md:flex space-x-1 lg:space-x-2 flex-grow justify-center font-montserrat">
        <router-link v-for="link in navLinks" :key="link.id" :to="link.to"
          class="px-4 py-2 rounded-full text-sm lg:text-base font-medium transition-all duration-300 flex items-center"
          :class="activeSection === link.id ? 'bg-red-50 text-red-700' : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'">
          {{ link.label }}
        </router-link>
      </nav>

      <!-- User Component Desktop -->
      <div class="hidden md:flex items-center justify-end w-32 lg:w-48 relative group">
        <!-- User Pill -->
        <div class="flex items-center gap-2 px-3 py-2 rounded-full border border-gray-200 bg-white shadow-sm cursor-pointer transition-all duration-300 hover:shadow-md hover:border-gray-300 group-hover:bg-gray-50">
          <CircleUserRound class="text-gray-500 w-5 h-5 group-hover:text-red-600 transition-colors duration-300" />
          <span class="text-gray-700 font-medium text-sm truncate max-w-[100px]">{{ userStore.user?.primeiro_nome || 'Usuário' }}</span>
        </div>
        
        <!-- User Dropdown (Hover) -->
        <div class="absolute right-0 top-full pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
          <div class="w-48 bg-white rounded-xl shadow-lg border border-gray-100 transform origin-top-right scale-95 group-hover:scale-100 transition-transform duration-300">
            <div class="p-2">
              <button @click="logout" class="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-red-600 font-medium rounded-lg hover:bg-red-50 transition-colors">
                <LogOut class="w-4 h-4" />
                Sair do Sistema
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Hamburger Button (Mobile Only) -->
      <div class="md:hidden flex items-center">
        <button @click="menuOpen = !menuOpen"
          class="p-2 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-red-500">
          <Menu class="w-6 h-6" />
        </button>
      </div>

    </div>
  </header>

  <!-- Mobile Drawer Overlay -->
  <Transition name="overlay">
    <div v-if="menuOpen" @click="menuOpen = false"
      class="md:hidden fixed inset-0 bg-gray-900/40 backdrop-blur-sm z-[1001]">
    </div>
  </Transition>

  <!-- Mobile Drawer -->
  <Transition name="drawer">
    <div v-if="menuOpen" ref="mobileMenu"
      class="md:hidden fixed top-0 right-0 h-[100dvh] w-[80%] max-w-sm bg-white shadow-2xl z-[1002] flex flex-col">

      <!-- Drawer Header -->
      <div class="flex items-center justify-between p-5 border-b border-gray-100">
        <img :src="Logo" alt="Logo" class="h-8 w-auto object-contain" />
        <button @click="menuOpen = false" class="p-2 rounded-full text-gray-500 hover:bg-gray-100 transition-colors">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 flex flex-col py-4 px-3 overflow-y-auto space-y-1 font-montserrat">
        <router-link v-for="link in navLinks" :key="link.id" :to="link.to" @click="menuOpen = false"
          class="flex items-center w-full py-3 px-4 rounded-xl text-left font-medium transition-colors"
          :class="activeSection === link.id ? 'text-red-700 bg-red-50' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'">
          {{ link.label }}
        </router-link>
      </nav>

      <!-- User Section (Mobile) -->
      <div class="p-5 space-y-4 bg-gray-50/50 mt-auto">
        <div class="flex items-center gap-3 px-2">
          <div class="bg-white p-2 rounded-full shadow-sm border border-gray-100">
            <CircleUserRound class="text-red-600 w-6 h-6" />
          </div>
          <span class="text-gray-800 font-medium font-montserrat">{{ userStore.user?.primeiro_nome || 'Usuário' }}</span>
        </div>
        <button @click="logout"
          class="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-white border border-red-200 text-red-600 font-medium font-montserrat hover:bg-red-50 transition-colors shadow-sm">
          <LogOut class="w-5 h-5" />
          Sair do Sistema
        </button>
      </div>

    </div>
  </Transition>

</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useUserStore } from '../stores/user.js'
import Logo from '../assets/LogoEscorpiao.png'
import { useRoute, useRouter } from 'vue-router'
import { CircleUserRound, LogOut, Menu, X } from 'lucide-vue-next'
import { useToastStore } from '../stores/toast'

const userStore = useUserStore()
const toastStore = useToastStore()
const route = useRoute()
const router = useRouter()
const activeSection = ref('')
const mobileMenu = ref(null)
const menuOpen = ref(false)

const navLinks = [
  { id: 'home', label: 'INÍCIO', to: '/' },
  { id: 'production', label: 'PRODUÇÃO', to: '/production' },
  { id: 'sale', label: 'VENDAS', to: '/sale' },
  { id: 'product', label: 'PRODUTOS', to: '/product' },
  { id: 'client', label: 'CLIENTES', to: '/client' },
  { id: 'dashboard', label: 'DASHBOARD', to: '/dashboard' }
]

function logout() {
  userStore.logout()
  toastStore.add({
    title: 'Logout',
    message: 'Você saiu do sistema. Até logo!',
    type: 'info',
    duration: 3000
  })
  router.push('/login')
  menuOpen.value = false
}

// Lógica de scroll para a homepage se necessário
const sections = [
  { id: 'empresa', label: 'EMPRESA' },
  { id: 'produtos', label: 'PRODUTOS' },
  { id: 'receitas', label: 'RECEITAS' },
  { id: 'ondecomprar', label: 'ONDE COMPRAR' }
]

function handleScroll() {
  if (route.path !== '/') return
  let current = ''
  for (const section of sections) {
    const el = document.getElementById(section.id)
    if (el) {
      const rect = el.getBoundingClientRect()
      if (rect.top <= 150 && rect.bottom > 150) {
        current = section.id
        break
      }
    }
  }
  activeSection.value = current || 'home'
}

function updateActiveSection(newPath) {
  if (newPath === '/') {
    handleScroll()
  } else {
    if (newPath.startsWith('/info')) {
      activeSection.value = 'info'
    } else if (newPath.startsWith('/contato')) {
      activeSection.value = 'contato'
    } else {
      activeSection.value = newPath.replace('/', '')
    }
  }
}

onMounted(() => {
  if (route.path === '/') {
    window.addEventListener('scroll', handleScroll)
  }
  updateActiveSection(route.path)
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('mousedown', handleClickOutside)
})

watch(() => route.path, (newPath) => {
  if (newPath === '/') {
    window.addEventListener('scroll', handleScroll)
  } else {
    window.removeEventListener('scroll', handleScroll)
  }
  updateActiveSection(newPath)
})

function handleClickOutside(event) {
  if (menuOpen.value && mobileMenu.value && !mobileMenu.value.contains(event.target)) {
    menuOpen.value = false
  }
}
</script>

<style scoped>
/* Mobile Drawer Transitions */
.drawer-enter-active,
.drawer-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drawer-enter-from,
.drawer-leave-to {
  transform: translateX(100%);
}

.drawer-enter-to,
.drawer-leave-from {
  transform: translateX(0);
}

/* Overlay Transitions */
.overlay-enter-active,
.overlay-leave-active {
  transition: opacity 0.3s ease;
}

.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

.overlay-enter-to,
.overlay-leave-from {
  opacity: 1;
}
</style>
