import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import AdminDashboard from "../views/AdminDashboard.vue"

const routes=[
    {
        path :"/",component:HomeView
    },
    {
        path :"/login",component:Login
    },
    {
        path :"/register",component:Register
    },
    {
        path :"/admin",component:AdminDashboard
    }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})  



export default router