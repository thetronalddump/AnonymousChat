import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import Chat from './components/Chat.vue'

const routes = [
    { path: '/login', component: Login, name: 'Login' },
    { path: '/chat', component: Chat, name: 'Chat' },
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})