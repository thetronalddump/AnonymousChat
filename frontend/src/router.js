import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import Chat from './components/Chat.vue'

const routes = [
    { path: '/login', component: Login },
    { path: '/chat', component: Chat }
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})