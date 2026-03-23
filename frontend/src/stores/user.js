import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { isTokenExpired } from '../utils/jwt'

export const useUserStore = defineStore('user', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('access_token') || null)

  const is_logged = computed(() => !!user.value && !!token.value && !isTokenExpired(token.value))
  const is_admin = computed(() => user.value?.is_admin === true)

  function setUser(newUser, newToken) {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
    if (newToken) {
      token.value = newToken
      localStorage.setItem('access_token', newToken)
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
  }

  // Checar e fazer auto logout se token expirou
  function ensureValidSession(router) {
    if (!is_logged.value) {
      logout()
      if (router) router.push('/login')
    }
  }

  return { user, token, is_logged, is_admin, setUser, logout, ensureValidSession }
})
