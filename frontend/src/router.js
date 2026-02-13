import { createRouter, createWebHistory } from 'vue-router'
import PersonList from './views/PersonList.vue'
import PersonCreate from './views/PersonCreate.vue'
import AdminFields from './views/AdminFields.vue'
import FormBuilder from './views/FormBuilder.vue'

const routes = [
    { path: '/', component: PersonList },
    { path: '/create', component: PersonCreate },
    { path: '/admin', component: AdminFields },
    { path: '/builder', component: FormBuilder },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
