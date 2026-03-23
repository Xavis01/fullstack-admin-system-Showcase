import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import './assets/main.css'
import router from './router'
import { createPinia } from 'pinia'

const app = createApp(App)

app.use(router)
app.use(createPinia())

app.mount('#app')

// Interceptador global do fetch para tratar erros 401 (Token Expirado)
const originalFetch = window.fetch;
window.fetch = async (...args) => {
    const requestUrl = typeof args[0] === 'string' ? args[0] : (args[0]?.url || args[0]?.toString() || '');
    const response = await originalFetch(...args);

    // Evita o erro "Sessão Expirada" disparar junto ao errar a senha no Login
    if (response.status === 401 && !requestUrl.includes('/api/login')) {
        // Importar stores dinamicamente para garantir que o Pinia já esteja inicializado
        const { useUserStore } = await import('./stores/user');
        const { useToastStore } = await import('./stores/toast');

        const userStore = useUserStore();
        const toastStore = useToastStore();

        // Evitar loop infinito ou chamadas duplicadas se já estiver deslogado
        // Mas 401 significa que o back rejeitou, então forçamos logout
        userStore.logout();

        toastStore.add({
            title: 'Sessão Expirada',
            message: 'Sua sessão expirou. Por favor, faça login novamente.',
            type: 'error',
            duration: 5000
        });

        router.push('/login');
    }

    return response;
};
