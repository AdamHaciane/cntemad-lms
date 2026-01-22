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
  {
    path: '/catalog',
    name: 'Catalog',
    component: () => import('./pages/Catalog.vue'),
  },
  {
    path: '/ec/:id',
    name: 'ECDetail',
    component: () => import('./pages/ECDetail.vue'),
  },
  {
    path: '/ec/:id/learn',
    name: 'Learn',
    component: () => import('./pages/Learn.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/ec/:id/quiz',
    name: 'Quiz',
    component: () => import('./pages/Quiz.vue'),
    meta: { requiresAuth: true },
  },
  // Admin Centre routes
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('./pages/admin/CenterDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/students',
    name: 'AdminStudents',
    component: () => import('./pages/admin/CenterStudents.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/payments',
    name: 'AdminPayments',
    component: () => import('./pages/admin/CenterPayments.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  // Teacher routes
  {
    path: '/teacher/courses',
    name: 'TeacherCourses',
    component: () => import('./pages/teacher/MesCours.vue'),
    meta: { requiresAuth: true, requiresTeacher: true },
  },
  {
    path: '/teacher/ec/:id/stats',
    name: 'ECStats',
    component: () => import('./pages/teacher/ECStats.vue'),
    meta: { requiresAuth: true, requiresTeacher: true },
  },
  // National Admin routes
  {
    path: '/national/dashboard',
    name: 'NationalDashboard',
    component: () => import('./pages/national/NationalDashboard.vue'),
    meta: { requiresAuth: true, requiresNationalAdmin: true },
  },
  {
    path: '/national/map',
    name: 'CentersMap',
    component: () => import('./pages/national/CentersMap.vue'),
    meta: { requiresAuth: true, requiresNationalAdmin: true },
  },
  {
    path: '/national/centers',
    name: 'CentersList',
    component: () => import('./pages/national/CentersMap.vue'),
    meta: { requiresAuth: true, requiresNationalAdmin: true },
  },
  {
    path: '/national/compare',
    name: 'CentersCompare',
    component: () => import('./pages/national/CentersCompare.vue'),
    meta: { requiresAuth: true, requiresNationalAdmin: true },
  },
  // Evaluator routes
  {
    path: '/evaluator/corrections',
    name: 'CorrectionsQueue',
    component: () => import('./pages/evaluator/CorrectionsQueue.vue'),
    meta: { requiresAuth: true, requiresEvaluator: true },
  },
  {
    path: '/evaluator/correction/:id',
    name: 'CorrectionDetail',
    component: () => import('./pages/evaluator/CorrectionDetail.vue'),
    meta: { requiresAuth: true, requiresEvaluator: true },
  },
  {
    path: '/evaluator/certificates',
    name: 'CertificatesValidation',
    component: () => import('./pages/evaluator/CertificatesValidation.vue'),
    meta: { requiresAuth: true, requiresEvaluator: true },
  },
  // Mentor routes
  {
    path: '/mentor/mentees',
    name: 'MesMentores',
    component: () => import('./pages/mentor/MesMentores.vue'),
    meta: { requiresAuth: true, requiresMentor: true },
  },
  {
    path: '/mentor/mentee/:id',
    name: 'MenteeDetail',
    component: () => import('./pages/mentor/MenteeDetail.vue'),
    meta: { requiresAuth: true, requiresMentor: true },
  },
  {
    path: '/mentor/messages',
    name: 'MentorMessages',
    component: () => import('./pages/mentor/Messages.vue'),
    meta: { requiresAuth: true, requiresMentor: true },
  },
  {
    path: '/mentor/messages/:id',
    name: 'MentorChat',
    component: () => import('./pages/mentor/Messages.vue'),
    meta: { requiresAuth: true, requiresMentor: true },
  },
  {
    path: '/mentor/alerts',
    name: 'MentorAlerts',
    component: () => import('./pages/mentor/Alerts.vue'),
    meta: { requiresAuth: true, requiresMentor: true },
  },
  // Parent/Guardian routes
  {
    path: '/parent/dashboard',
    name: 'ParentDashboard',
    component: () => import('./pages/guardian/ParentDashboard.vue'),
    meta: { requiresAuth: true, requiresGuardian: true },
  },
  {
    path: '/parent/child/:id',
    name: 'ChildProgress',
    component: () => import('./pages/guardian/ChildProgress.vue'),
    meta: { requiresAuth: true, requiresGuardian: true },
  },
  {
    path: '/parent/pay',
    name: 'ParentPayment',
    component: () => import('./pages/guardian/ParentPayment.vue'),
    meta: { requiresAuth: true, requiresGuardian: true },
  },
  {
    path: '/parent/pay/:id',
    name: 'ParentPaymentChild',
    component: () => import('./pages/guardian/ParentPayment.vue'),
    meta: { requiresAuth: true, requiresGuardian: true },
  },
]

const router = createRouter({
  history: createWebHistory('/student/'),
  routes,
})

export default router
