<template>
    <div class="not-found-container font-montserrat bg-gray-200">
        <div class="content text-center">
            <h1 class="error-code text-red-600">404</h1>
            <h2 class="error-message text-gray-800">Página não encontrada</h2>
            <p class="description text-gray-600">
                Ops! A página que você está procurando não existe ou foi removida.
            </p>
            <router-link to="/"
                class="back-button bg-red-600 hover:bg-red-700 text-white shadow-md transition-transform transform hover:scale-105">
                Voltar para o Início
            </router-link>
        </div>
    </div>
</template>

<script setup>
// Component logic if needed
</script>

<style scoped>
.not-found-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: #1f2937;
}

.content {
    padding: 3rem;
    background: white;
    border-radius: 1rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    max-width: 500px;
    width: 90%;
}

.error-code {
    font-size: 6rem;
    font-weight: 800;
    margin: 0;
    line-height: 1;
}

.error-message {
    font-size: 1.8rem;
    margin: 1rem 0;
    font-weight: 700;
}

.description {
    font-size: 1.1rem;
    margin-bottom: 2.5rem;
}

.back-button {
    display: inline-block;
    padding: 0.8rem 2rem;
    text-decoration: none;
    border-radius: 0.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
</style>
