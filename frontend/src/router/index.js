import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import ClientView from '../views/ClientView.vue'
import ProductView from '../views/ProductView.vue'
import SaleView from '../views/SaleView.vue'
import ProductionView from '../views/ProductionView.vue'
import { useUserStore } from '../stores/user'




const routes = [
    { path: '/login', name: 'Login', component: LoginView, meta: { hideNavbar: true } },
    { path: '/', name: 'Home', component: HomeView, meta: { requiresAuth: true } },
    { path: '/admin', name: 'Admin', component: () => import('../views/AdminView.vue'), meta: { requiresAuth: true } },
    { path: '/production', name: 'Production', component: ProductionView, meta: { requiresAuth: true } },
    { path: '/sale', name: 'Sale', component: SaleView, meta: { requiresAuth: true } },
    { path: '/product', name: 'Product', component: ProductView, meta: { requiresAuth: true } },
    { path: '/client', name: 'Client', component: ClientView, meta: { requiresAuth: true } },
    { path: '/dashboard', name: 'Dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
    { path: '/updates', name: 'Updates', component: () => import('../views/UpdatesView.vue'), meta: { requiresAuth: true } },
    { path: '/procedures', name: 'Procedures', component: () => import('../views/ProceduresView.vue'), meta: { requiresAuth: true } },
    { path: '/stock-history', name: 'StockHistory', component: () => import('../views/StockHistoryView.vue'), meta: { requiresAuth: true } },
    { path: '/:catchAll(.*)', name: 'NotFound', component: () => import('../views/NotFoundView.vue'), meta: { hideNavbar: true } }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        // Se tem hash (ex: #produtos), scrolla depois do DOM montar
        if (to.hash) {
            return new Promise((resolve) => {
                // aguarda o próximo ciclo do DOM/render
                setTimeout(() => {
                    resolve({
                        el: to.hash,
                        behavior: 'smooth',
                    })
                }, 100) // 300ms é seguro, pode ajustar
            })
        }

        // Se volta para cima, ou muda de página sem hash
        return { top: 0 }
    }
    ,
})

router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    const isLoggedIn = !!localStorage.getItem('access_token')

    // Se a rota requer autenticação
    if (to.meta.requiresAuth) {
        if (!isLoggedIn) {
            // Não está logado, redireciona para login
            next({ name: 'Login' })
        } else if (!userStore.is_admin) {
            // Está logado mas não é admin, faz logout e redireciona
            userStore.logout()
            next({ name: 'Login' })
        } else {
            // Está logado e é admin, permite acesso
            next()
        }
    } else if (to.name === 'Login' && isLoggedIn && userStore.is_admin) {
        // Se está logado como admin e tenta acessar login, redireciona para home
        next({ name: 'Home' })
    } else {
        next()
    }
})

export default router
