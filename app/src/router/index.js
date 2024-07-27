import { createRouter, createWebHistory } from 'vue-router';
import DataDisplay from '../components/DataDisplay.vue';
import ConcertsSummary from '../components/ConcertsSummary.vue';

const routes = [
  { path: '/', component: DataDisplay },
  { path: '/summary', component: ConcertsSummary },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
