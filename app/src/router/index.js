import { createRouter, createWebHistory } from 'vue-router';

import MapPickView from '../views/MapPickView.vue';

const routes = [
    {
        path: '/mappick',
        name: 'map_pick',
        component: MapPickView
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router;