import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./pages/Home.vue'),
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('./pages/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/courses',
    name: 'Courses',
    component: () => import('./pages/Courses.vue'),
  },
  {
    path: '/courses/:id',
    name: 'CourseDetail',
    component: () => import('./pages/CourseDetail.vue'),
  },
  {
    path: '/payment',
    name: 'Payment',
    component: () => import('./pages/Payment.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory('/student/'),
  routes,
})

export default router
