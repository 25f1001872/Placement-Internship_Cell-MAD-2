import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import RegisterStudent from '../views/RegisterStudent.vue'
import RegisterCompany from '../views/RegisterCompany.vue'
import HomePage from '../views/HomePage.vue'

const routes = [
    { path: '/', component: HomePage },
    { path: '/login', component: LoginPage },
    { path: '/register/student', component: RegisterStudent },
    { path: '/register/company', component: RegisterCompany },
    { path: '/admin/dashboard', component: () => import('../views/admin/AdminDashboard.vue'), meta: { requiresAuth: true, role: 'admin' } },
    { path: '/company/dashboard', component: () => import('../views/company/CompanyDashboard.vue'), meta: { requiresAuth: true, role: 'company' } },
    { path: '/student/dashboard', component: () => import('../views/student/StudentDashboard.vue'), meta: { requiresAuth: true, role: 'student' } },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('role')
    if (to.meta.requiresAuth && !token) return next('/login')
    if (to.meta.role && to.meta.role !== role) return next('/login')
    next()
})

export default router