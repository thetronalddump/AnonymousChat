
import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/styles.css'
import {router} from "@/router.js";
import { createPinia} from "pinia";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'


const app = createApp(App)

app.use(ElementPlus)
app.use(router)
app.use(createPinia())
app.mount('#app')
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}