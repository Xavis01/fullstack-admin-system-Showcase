<script setup>
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue';
import ToastContainer from './components/Toast/ToastContainer.vue';


const route = useRoute()
</script>

<template>
  <NavBar v-if="route.name && !route.meta.hideNavbar" />
  <ToastContainer />
  <router-view />
  <Footer v-if="route.name && !route.meta.hideNavbar" />
</template>


<style>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
