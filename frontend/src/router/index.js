import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminView from '../views/AdminView.vue'
import UserView from '../views/UserView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  { path: '/', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/admin', component: AdminView },
  { path: '/user', component: UserView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router