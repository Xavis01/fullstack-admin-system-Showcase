<template>
  <div class="min-h-screen w-full flex flex-col md:flex-row bg-[#0D0D0D] relative overflow-x-hidden font-montserrat">
    
    <!-- Esquerda: Flutuantes (Oculto no mobile e em alto zoom) -->
    <div class="hidden lg:flex flex-1 relative items-center justify-center p-8 overflow-hidden z-0 bg-[#0F0F0F]">
      
      <!-- Background glows avermelhados (sistema) -->
      <div class="absolute top-[10%] left-[20%] w-[400px] h-[400px] bg-red-900/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div class="absolute bottom-[10%] right-[20%] w-[500px] h-[500px] bg-red-800/10 rounded-full blur-[150px] pointer-events-none"></div>
      
      <!-- Partículas flutuantes aleatórias para o UX interativo -->
      <div class="absolute top-[28%] left-[38%] w-2 h-2 bg-red-500/50 rounded-full shadow-[0_0_10px_rgba(239,68,68,0.8)] animate-sparkle"></div>
      <div class="absolute bottom-[35%] right-[30%] w-2.5 h-2.5 bg-red-500/40 rounded-full shadow-[0_0_12px_rgba(239,68,68,0.8)] animate-sparkle" style="animation-delay: 1.3s;"></div>
      <div class="absolute top-[58%] left-[45%] w-1.5 h-1.5 bg-red-400/50 rounded-full shadow-[0_0_10px_rgba(248,113,113,0.8)] animate-sparkle" style="animation-delay: 0.7s;"></div>
      <div class="absolute top-[40%] right-[40%] w-1.5 h-1.5 bg-orange-500/50 rounded-full shadow-[0_0_10px_rgba(249,115,22,0.8)] animate-sparkle" style="animation-delay: 2.1s;"></div>
      <div class="absolute bottom-[45%] left-[42%] w-2 h-2 bg-red-600/50 rounded-full shadow-[0_0_10px_rgba(220,38,38,0.8)] animate-sparkle" style="animation-delay: 1.8s;"></div>
      <div class="absolute top-[35%] right-[45%] w-1.5 h-1.5 bg-red-400/60 rounded-full shadow-[0_0_8px_rgba(248,113,113,0.8)] animate-sparkle" style="animation-delay: 0.4s;"></div>
      <div class="absolute bottom-[30%] left-[48%] w-1 h-1 bg-white/40 rounded-full shadow-[0_0_6px_rgba(255,255,255,0.8)] animate-sparkle" style="animation-delay: 2.5s;"></div>

      <!-- Content Center -->
      <div class="z-30 flex flex-col items-center text-center relative group">
        <!-- Partículas de luz saindo do logo quando passa o mouse -->
        <div class="absolute inset-0 z-[-1] transition-opacity duration-500 opacity-50 group-hover:opacity-100">
           <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-red-600/20 rounded-full blur-[40px]"></div>
           <div class="absolute top-[20%] right-[30%] w-2 h-2 bg-white/60 rounded-full shadow-[0_0_10px_rgba(255,255,255,0.8)] animate-sparkle" style="animation-delay: 0.2s;"></div>
           <div class="absolute bottom-[20%] left-[30%] w-1.5 h-1.5 bg-red-300/60 rounded-full shadow-[0_0_8px_rgba(252,165,165,0.8)] animate-sparkle" style="animation-delay: 1.5s;"></div>
           <div class="absolute top-[40%] left-[10%] w-2 h-2 bg-orange-400/50 rounded-full shadow-[0_0_12px_rgba(251,146,60,0.8)] animate-sparkle" style="animation-delay: 2.8s;"></div>
           <div class="absolute bottom-[10%] right-[10%] w-1 h-1 bg-white/40 rounded-full shadow-[0_0_5px_rgba(255,255,255,0.9)] animate-sparkle" style="animation-delay: 0.9s;"></div>
        </div>

        <!-- Logo only, sem fundo mas com glow -->
        <div class="w-32 h-32 mb-8 flex items-center justify-center animate-float-slow transition-transform duration-700 group-hover:scale-[1.05]">
          <img src="/IconeEscorpiaoQuadrado.png" alt="Logo Soda Escorpião" class="w-full h-full object-contain drop-shadow-[0_0_20px_rgba(255,255,255,0.4)]" />
        </div>
        
        <div class="flex items-center gap-4 mb-6">
          <div class="h-[1px] w-16 bg-gradient-to-r from-transparent to-red-600/60"></div>
          <span class="text-red-500 font-bold tracking-[0.25em] text-[10px] uppercase">Admin Panel</span>
          <div class="h-[1px] w-16 bg-gradient-to-l from-transparent to-red-600/60"></div>
        </div>
        
        <p class="text-gray-400 text-sm max-w-[280px] leading-relaxed">
          Painel de gestão inteligente da empresa Soda Cáustica Escorpião
        </p>
      </div>

      <!-- Floating Cards -->
      <!-- 1. Revenue -->
      <div class="absolute top-[12%] left-[8%] bg-[#121212]/90 backdrop-blur-xl border border-white/5 rounded-2xl p-5 w-52 shadow-[0_8px_32px_rgba(0,0,0,0.5)] animate-float hover:scale-105 hover:border-red-500/30 transition-all duration-300 cursor-default flex flex-col z-20" style="animation-delay: 0.3s; animation-duration: 6.5s;">
        <div class="flex items-center gap-2 mb-3">
          <div class="p-1.5 bg-red-500/20 rounded-lg"><BarChart3 class="w-4 h-4 text-red-500" /></div>
          <span class="text-gray-400 text-xs font-medium">Faturamento</span>
        </div>
        <div class="text-white font-bold text-2xl mb-1 flex items-end tracking-widest gap-2">
          R$ &bull;&bull;&bull;&bull;
        </div>
        <div class="text-emerald-400 text-xs font-medium flex items-center gap-1 mb-2 tracking-widest">
          <TrendingUp class="w-3.5 h-3.5" /> +&bull;&bull;&bull;%
        </div>
        <!-- Mini bars chart -->
        <div class="flex justify-between items-end h-8 mt-4 gap-1.5">
          <div class="w-full bg-red-600/80 rounded-t-sm h-[40%]"></div>
          <div class="w-full bg-red-600/80 rounded-t-sm h-[60%]"></div>
          <div class="w-full bg-red-600/80 rounded-t-sm h-[45%]"></div>
          <div class="w-full bg-red-600/80 rounded-t-sm h-[80%]"></div>
          <div class="w-full bg-red-600/80 rounded-t-sm h-[65%]"></div>
          <div class="w-full bg-red-500 rounded-t-sm h-[100%] shadow-[0_0_10px_rgba(249,115,22,0.6)]"></div>
          <div class="w-full bg-red-600/80 rounded-t-sm h-[90%]"></div>
        </div>
      </div>

      <!-- 2. Security Shield -->
      <div class="absolute top-[15%] right-[10%] bg-[#121212]/90 backdrop-blur-xl border border-white/5 rounded-2xl p-4 w-40 shadow-[0_8px_32px_rgba(0,0,0,0.5)] animate-float-right hover:scale-110 hover:border-gray-500/50 transition-all duration-300 cursor-default z-20" style="animation-delay: 1.2s; animation-duration: 5.8s;">
        <div class="p-2 bg-white/5 border border-white/10 w-fit rounded-xl mb-4">
          <ShieldCheck class="w-5 h-5 text-gray-400" />
        </div>
        <div class="space-y-2.5">
          <div class="h-1.5 bg-gray-700/50 rounded-full w-full"></div>
          <div class="h-1.5 bg-gray-700/50 rounded-full w-2/3"></div>
        </div>
      </div>

      <!-- 3. Real-time Pill -->
      <div class="absolute right-[20%] top-[45%] bg-[#121212]/90 backdrop-blur-md border border-red-500/20 rounded-full px-4 py-2 flex items-center gap-2 animate-float-fast hover:shadow-[0_0_30px_rgba(239,68,68,0.25)] hover:border-red-500/50 transition-all duration-300 cursor-default shadow-[0_0_20px_rgba(239,68,68,0.1)] z-20" style="animation-duration: 4.2s;">
        <Zap class="w-4 h-4 text-red-500 fill-red-500/30" />
        <span class="text-gray-300 text-[11px] font-semibold tracking-widest uppercase">Real-time</span>
      </div>

      <!-- 4. Estoque -->
      <div class="absolute bottom-[20%] left-[10%] bg-[#121212]/90 backdrop-blur-xl border border-white/5 rounded-2xl p-5 w-48 shadow-[0_8px_32px_rgba(0,0,0,0.5)] animate-float-left hover:-translate-y-2 hover:border-yellow-500/30 transition-all duration-300 cursor-default z-20" style="animation-delay: 2.5s; animation-duration: 7.2s;">
        <div class="flex items-center gap-2 mb-3">
          <Package class="w-4 h-4 text-red-500" />
          <span class="text-gray-400 text-xs font-medium">Estoque</span>
        </div>
        <div class="text-white font-bold text-xl mb-4 tracking-widest">&bull;&bull;&bull;&bull; <span class="text-xs font-normal text-gray-500 tracking-normal">itens</span></div>
        <div class="h-1.5 w-full bg-gray-800 rounded-full overflow-hidden">
          <div class="h-full bg-red-500 w-[65%] rounded-full shadow-[0_0_10px_rgba(234,179,8,0.8)]"></div>
        </div>
      </div>

      <!-- 5. Sync ERP -->
      <div class="absolute bottom-[10%] right-[15%] bg-[#121212]/90 backdrop-blur-xl border border-white/5 rounded-2xl p-4 w-44 shadow-[0_8px_32px_rgba(0,0,0,0.5)] animate-float hover:scale-105 hover:border-emerald-500/30 transition-all duration-300 cursor-default z-20" style="animation-delay: 1.7s; animation-duration: 6.1s;">
        <div class="flex items-center gap-2 mb-2">
          <Database class="w-4 h-4 text-gray-400" />
          <span class="text-gray-400 text-xs font-medium">Sync DB</span>
        </div>
        <div class="flex items-center gap-2 mt-2">
          <div class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)] relative">
             <div class="absolute inset-0 rounded-full bg-emerald-400 animate-ping opacity-75"></div>
          </div>
          <span class="text-emerald-400 text-[11px] font-bold tracking-wide">Conectado</span>
        </div>
      </div>
    </div>

    <!-- Direita: Formulário de Login (Ocupa 100% no mobile) -->
    <div class="flex-1 lg:flex-none lg:w-[45%] xl:w-[40%] flex flex-col items-center p-6 bg-white relative overflow-y-auto min-h-screen md:min-h-0">
       <!-- Gradient overlay suave -->
       <div class="absolute inset-0 bg-gradient-to-br from-white to-gray-100 pointer-events-none min-h-full"></div>

       <!-- Container do Form -->
       <div class="z-10 w-full max-w-[400px] my-auto py-8 relative min-h-[600px] flex flex-col justify-center">
          
          <!-- Formulário original adaptado às constraints -->
          <transition name="flip" mode="out-in" @before-enter="beforeEnter" @enter="enter" @leave="leave">
            <div :key="isSignupMode ? 'signup' : 'login'" class="w-full mt-4 md:mt-0">
              <!-- Ícone e Título adicionais integrados na animação -->
              <div class="flex justify-center mb-0 md:mb-2">
                 <div class="w-24 h-24 flex items-center justify-center overflow-hidden">
                    <img src="/IconeEscorpiaoQuadrado.png" alt="Logo" class="w-full h-full object-contain" />
                 </div>
              </div>
              <div class="text-center mb-8">
                 <h2 class="text-2xl font-bold text-gray-800 tracking-tight">{{ isSignupMode ? 'Criar Conta' : 'Painel de Gestão' }}</h2>
                 <p class="text-xs text-gray-400 mt-1">Acesso restrito para administradores</p>
              </div>

              <form class="form !max-w-full shadow-[0_20px_40px_-15px_rgba(0,0,0,0.3)] bg-[#1a1a1a]"
                @submit.prevent="isSignupMode ? handleSignup() : handleLogin()">
                <p class="title">{{ isSignupMode ? 'Cadastro' : 'Login' }}</p>
                <!-- <p class="message">Sistema Administrativo Soda Escorpião</p> -->

                <!-- Campo Nome (apenas no modo cadastro) -->
                <label v-if="isSignupMode">
                  <input class="input" type="text" placeholder="" v-model.trim="nome" required minlength="3">
                  <span>Nome Completo</span>
                </label>

                <!-- Campo Email -->
                <label>
                  <input class="input" type="email" placeholder="" v-model.trim="email" required>
                  <span>Email</span>
                </label>

                <!-- Campo Data de Nascimento (apenas no modo cadastro) -->
                <label v-if="isSignupMode">
                  <CustomCalendarDark v-model="dtNascimento" placeholder="" label="Data de Nascimento (opcional)" />
                </label>

                <!-- Campo Senha -->
                <label class="relative block">
                  <input class="input pr-10" :type="showPassword ? 'text' : 'password'" placeholder="" v-model.trim="password" required
                    :minlength="isSignupMode ? 6 : undefined"
                    :autocomplete="isSignupMode ? 'new-password' : 'current-password'">
                  <span>Senha{{ isSignupMode ? ' (mínimo 6 caracteres)' : '' }}</span>
                  <button type="button" @click="showPassword = !showPassword" tabindex="-1"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-red-500 transition-colors focus:outline-none z-10 p-1">
                    <EyeOff v-if="!showPassword" class="w-5 h-5" />
                    <Eye v-else class="w-5 h-5" />
                  </button>
                </label>

                <!-- Botão Submit com Shine Hover e Fade Constant Animation -->
                <button class="submit flex w-full gap-1.5 justify-center mt-2 items-center text-center relative overflow-hidden group btn-shine btn-fade" :disabled="loading">
                  <span v-if="!loading" class="font-semibold relative z-10">{{ isSignupMode ? 'Cadastrar' : 'Acessar Painel Admin' }}</span>
                  <LoaderCircle v-else class="animate-spin w-5 h-5 relative z-10" />
                </button>

                <!-- Link para alternar modo -->
                <p class="signin mt-1">
                  {{ isSignupMode ? 'Já possui conta?' : 'Não possui cadastro?' }}
                  <a @click.prevent="toggleMode"
                    class="group relative inline-block transition hover:text-red-500 cursor-pointer font-medium">
                    Clique Aqui
                    <span
                      class="absolute left-0 bottom-0 h-0.5 transition-all duration-300 w-0 group-hover:w-full bg-red-500"></span>
                  </a>
                </p>
                
                <div class="flex items-center justify-center gap-2 text-gray-500/70 mt-2 mb-1 border-t border-white/5 pt-4">
                  <ShieldCheck class="w-4 h-4" />
                  <span class="text-[11px] font-medium tracking-wide">Conexão segura e criptografada</span>
                </div>

                <!-- Mensagem de erro -->
                <p v-if="errorMsg" class="error-msg pt-2">{{ errorMsg }}</p>
              </form>
            </div>
          </transition>
       </div>
       
       <!-- Footer na direita -->
       <div class="mt-auto pt-8 w-full flex flex-col items-center text-[10px] md:text-[11px] text-gray-500 z-10 px-4 relative">
         <div class="flex flex-col md:flex-row items-center gap-1 md:gap-3">
           <span>© 2026 Soda Escorpião — Todos os direitos reservados.</span>
           <!-- <span class="hidden md:inline text-gray-400">•</span> -->
           <a href="#" class="hover:text-red-500 transition-colors">Termos de Uso & Política de Privacidade</a>
         </div>
         <p class="mt-4 opacity-70 text-[9px] md:text-[10px]">Desenvolvido por Lucas Xavier</p>
       </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LoaderCircle, Flame, BarChart3, TrendingUp, ShieldCheck, Zap, Package, Database, Eye, EyeOff } from 'lucide-vue-next'
import { useUserStore } from '../stores/user'
import { useToastStore } from '../stores/toast'
import CustomCalendarDark from '../components/CustomCalendarDark.vue'

// Refs para ambos os modos
const isSignupMode = ref(false)
const nome = ref('')
const email = ref('')
const dtNascimento = ref('')
const password = ref('')
const showPassword = ref(false)
const errorMsg = ref('')
const loading = ref(false)

const router = useRouter()
const userStore = useUserStore()
const toastStore = useToastStore()

// Alterna entre login e cadastro
function toggleMode() {
  isSignupMode.value = !isSignupMode.value
  // Limpa os campos
  nome.value = ''
  email.value = ''
  dtNascimento.value = ''
  password.value = ''
  showPassword.value = false
  errorMsg.value = ''
}

// Animation hooks para 3D flip
function beforeEnter(el) {
  el.style.opacity = '0'
}

function enter(el, done) {
  setTimeout(() => {
    el.style.opacity = '1'
    done()
  }, 50)
}

function leave(el, done) {
  el.style.opacity = '0'
  setTimeout(done, 300)
}

// Função de Cadastro
async function handleSignup() {
  errorMsg.value = ''
  loading.value = true

  try {
    const body = {
      nome: nome.value,
      email: email.value,
      password: password.value
    }

    // Adiciona data de nascimento se preenchida
    if (dtNascimento.value) {
      body.dt_nascimento = dtNascimento.value
    }

    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })

    const data = await res.json()

    if (!res.ok) {
      const message = data.error || 'Erro ao cadastrar.'
      errorMsg.value = message

      toastStore.add({
        title: 'Erro no Cadastro',
        message: message,
        type: 'error',
        duration: 5000
      })

      loading.value = false
      return
    }

    // Sucesso no cadastro
    toastStore.add({
      title: 'Cadastro Realizado!',
      message: 'Aguarde a aprovação de um administrador para acessar o sistema.',
      type: 'success',
      duration: 6000
    })

    // Volta para o modo login e limpa campos
    isSignupMode.value = false
    nome.value = ''
    email.value = ''
    dtNascimento.value = ''
    password.value = ''
    showPassword.value = false

  } catch (err) {
    errorMsg.value = 'Erro de conexão.'
    toastStore.add({
      title: 'Erro de Conexão',
      message: 'Não foi possível conectar ao servidor. Verifique sua internet.',
      type: 'error',
      duration: 5000
    })
  }

  loading.value = false
}

// Função de Login (mantida)
async function handleLogin() {
  errorMsg.value = ''
  loading.value = true

  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    })

    let data
    try {
      data = await res.json()
    } catch {
      errorMsg.value = 'Erro no servidor. Tente novamente mais tarde.'
      toastStore.add({
        title: 'Erro no Servidor',
        message: 'O servidor retornou uma resposta inválida.',
        type: 'error',
        duration: 5000
      })
      loading.value = false
      return
    }

    if (!res.ok) {
      const message = data.error || data.message || 'Erro ao entrar.'
      errorMsg.value = message

      toastStore.add({
        title: 'Falha no Login',
        message: message,
        type: 'error'
      })

      loading.value = false
      return
    }

    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))

    // Verifica se o usuário é admin
    if (data.user.is_admin !== true) {
      // Remove as credenciais que acabamos de salvar
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')

      errorMsg.value = 'Acesso negado. Apenas administradores podem acessar este sistema.'

      toastStore.add({
        title: 'Acesso Negado',
        message: 'Apenas administradores podem acessar este sistema.',
        type: 'error',
        duration: 5000
      })

      loading.value = false
      return
    }

    userStore.setUser(data.user, data.access_token)

    const firstName = data.user.primeiro_nome || (data.user.nome ? data.user.nome.split(' ')[0] : 'Usuário')

    toastStore.add({
      title: `Bem vindo, ${firstName}!`,
      message: 'Login realizado com sucesso.',
      type: 'success',
      duration: 3000
    })

    // Redireciona para a tela principal
    router.push('/')
  } catch (err) {
    errorMsg.value = 'Erro de conexão.'
    toastStore.add({
      title: 'Erro de Conexão',
      message: 'Não foi possível conectar ao servidor. Verifique sua internet.',
      type: 'error',
      duration: 5000
    })
  }

  loading.value = false
}
</script>

<style scoped>
@keyframes float {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-12px) rotate(3deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}
@keyframes float-right {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(4deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}
@keyframes float-left {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(-3deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}
@keyframes float-fast {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-8px) rotate(-2deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}
@keyframes float-slow {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-6px) rotate(1deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}
@keyframes sparkle {
  0% { transform: scale(0) translateY(0); opacity: 0; }
  25% { transform: scale(1.2) translateY(-5px); opacity: 1; }
  50% { transform: scale(0.8) translateY(-10px); opacity: 0.8; }
  100% { transform: scale(0) translateY(-20px); opacity: 0; }
}
@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}
.animate-float-right {
  animation: float-right 6s ease-in-out infinite;
}
.animate-float-left {
  animation: float-left 6s ease-in-out infinite;
}
.animate-float-fast {
  animation: float-fast 4s ease-in-out infinite;
}
.animate-float-slow {
  animation: float-slow 8s ease-in-out infinite;
}
.animate-sparkle {
  animation: sparkle 4s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
}
/* Perspective container for 3D effect */
.flip-container {
  perspective: 1200px;
  position: relative;
}

/* 3D Flip Animation */
.flip-enter-active,
.flip-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  backface-visibility: hidden;
}

.flip-enter-from {
  transform: rotateY(-90deg);
}

.flip-leave-to {
  transform: rotateY(90deg);
}

.flip-leave-active {
  position: absolute;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 350px;
  padding: 20px;
  border-radius: 20px;
  position: relative;
  background-color: #1a1a1a;
  color: #fff;
  border: 1px solid #333;
}

.title {
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -1px;
  position: relative;
  display: flex;
  align-items: center;
  padding-left: 30px;
  color: #df4141;
}

.title::before {
  width: 18px;
  height: 18px;
}

.title::after {
  width: 18px;
  height: 18px;
  animation: pulse 1s linear infinite;
}

.title::before,
.title::after {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  border-radius: 50%;
  left: 0px;
  background-color: #df4141;
}

.message,
.signin {
  font-size: 14.5px;
  color: rgba(255, 255, 255, 0.7);
}

.signin {
  text-align: center;
}

.signin a {
  color: #df4141;
}

.form label {
  position: relative;
}

.form label .input {
  background-color: #333;
  color: #fff;
  width: 100%;
  padding: 20px 05px 05px 10px;
  outline: 0;
  border: 1px solid rgba(105, 105, 105, 0.397);
  border-radius: 10px;
}

.form label .input+span {
  color: rgba(255, 255, 255, 0.5);
  position: absolute;
  left: 10px;
  top: 0px;
  font-size: 0.9em;
  cursor: text;
  transition: 0.3s ease;
}

.form label .input:placeholder-shown+span {
  top: 12.5px;
  font-size: 0.9em;
}

.form label .input:focus+span,
.form label .input:valid+span {
  color: #df4141;
  top: 0px;
  font-size: 0.7em;
  font-weight: 600;
}

.input {
  font-size: medium;
}

.submit {
  border: none;
  outline: none;
  padding: 10px;
  border-radius: 10px;
  color: #fff;
  font-size: 16px;
  transform: .3s ease;
  background-color: #df4141;
}

.btn-shine::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.3), transparent);
  transform: skewX(-20deg);
}

.btn-shine:hover::after {
  animation: shine 1.2s infinite;
}

.btn-fade::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 150%;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 100, 100, 0.6), transparent);
  transform: skewX(-30deg);
  animation: fade-pulse 3s linear infinite;
  z-index: 1;
  pointer-events: none;
}

@keyframes fade-pulse {
  0% { left: -150%; opacity: 0; }
  20% { opacity: 1; }
  60% { opacity: 1; }
  100% { left: 150%; opacity: 0; }
}

@keyframes shine {
  100% {
    left: 200%;
  }
}

.error-msg {
  color: #df4141;
  text-align: center;
  font-size: 14px;
  margin-top: 5px;
}

.submit:hover {
  background-color: #df414196;
}

@keyframes pulse {
  from {
    transform: scale(0.9);
    opacity: 1;
  }

  to {
    transform: scale(1.8);
    opacity: 0;
  }
}
</style>
