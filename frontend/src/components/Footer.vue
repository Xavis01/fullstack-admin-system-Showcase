<template>
    <footer class="bg-white py-12 shadow-[0_-5px_10px_rgba(0,0,0,0.05)]">
        <div class="max-w-7xl mx-auto px-6">
            <!-- Troque o grid por flex para 3 colunas -->
            <div class="flex flex-col md:flex-row justify-between gap-8">
                <!-- Sobre a empresa -->
                <div class="md:w-1/4">
                    <h3 class="text-lg font-bold text-gray-900 mb-4 font-montserrat">SODA CÁUSTICA ESCORPIÃO</h3>
                    <p class="text-gray-700 text-sm font-montserrat">
                        Sistema Administrativo da Soda Cáustica Escorpião
                    </p>
                </div>

                <!-- Contato -->
                <div class="md:w-1/4">
                    <h3 class="text-lg font-bold text-gray-900 mb-4 font-montserrat">CONTATO SUPORTE
                    </h3>
                    <ul class="space-y-2 text-sm text-gray-700 font-montserrat tracking-wide">
                        <div class="flex gap-2">
                            <Mail size="18" />
                            <li>lucas.xavierbres@gmail.com</li>
                        </div>
                        <a href="https://wa.me/5527996517804" target="_blank" rel="noopener noreferrer"
                            class="flex gap-2 items-center hover:text-green-600 transition-colors cursor-pointer">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
                                fill="currentColor">
                                <path
                                    d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                            </svg>
                            <li>(27) 99651-7804</li>
                        </a>
                    </ul>
                </div>

                <!-- Redes sociais -->
                <div class="md:w-1/4">
                    <h3 class="text-lg font-bold text-gray-900 mb-4 font-montserrat">REDES SOCIAIS</h3>
                    <div class="flex gap-4 items-center">
                        <a title="Instagram" href="https://www.instagram.com/sodaescorpiao/" target="_blank"
                            rel="noopener noreferrer" aria-label="Instagram"
                            class="text-red-700 hover:text-red-500 transition">
                            <Instagram class="w-6 h-6" />
                        </a>
                        <a title="Facebook" href="https://www.facebook.com/61559856353973/" target="_blank"
                            rel="noopener noreferrer" aria-label="Facebook"
                            class="text-red-700 hover:text-red-500 transition">
                            <Facebook class="w-6 h-6" />
                        </a>

                        <a title="TikTok" href="https://www.tiktok.com/@sodaescorpiao" target="_blank"
                            rel="noopener noreferrer" aria-label="TikTok"
                            class="text-red-700 hover:text-red-500 transition rounded-lg p-1 border-2 border-red-700 hover:border-red-500">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                                fill="currentColor">
                                <path
                                    d="M448.5 209.9c-44 .1-87-13.6-122.8-39.2l0 178.7c0 33.1-10.1 65.4-29 92.6s-45.6 48-76.6 59.6-64.8 13.5-96.9 5.3-60.9-25.9-82.7-50.8-35.3-56-39-88.9 2.9-66.1 18.6-95.2 40-52.7 69.6-67.7 62.9-20.5 95.7-16l0 89.9c-15-4.7-31.1-4.6-46 .4s-27.9 14.6-37 27.3-14 28.1-13.9 43.9 5.2 31 14.5 43.7 22.4 22.1 37.4 26.9 31.1 4.8 46-.1 28-14.4 37.2-27.1 14.2-28.1 14.2-43.8l0-349.4 88 0c-.1 7.4 .6 14.9 1.9 22.2 3.1 16.3 9.4 31.9 18.7 45.7s21.3 25.6 35.2 34.6c19.9 13.1 43.2 20.1 67 20.1l0 87.4z" />
                            </svg>
                        </a>

                    </div>
                </div>
            </div>

            <!-- Direitos autorais -->
            <div
                class="mt-12 pt-6 border-t border-gray-200 text-center text-sm text-gray-500 font-montserrat tracking-wide flex flex-col items-center gap-1">
                <p>© 2026 Soda Cáustica Escorpião. Todos os direitos reservados.</p>
                <p class="text-[10px] opacity-70">Desenvolvido por Lucas Xavier</p>
            </div>
        </div>
    </footer>


</template>


<script setup>
import { Instagram, Facebook, MapPinned, Mail } from 'lucide-vue-next';
</script>