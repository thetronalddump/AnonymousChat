import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import Chat from './components/Chat.vue'
import Main from "@/components/Main.vue";

const routes = [
    { path: '/login', component: Login, name: 'Login' },
    { path: '/chat', component: Chat, name: 'Chat' },
    { path: '/', component: Main, name: 'Main' },
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})