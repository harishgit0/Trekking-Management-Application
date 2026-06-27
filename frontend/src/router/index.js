import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import AdminDashboard from "../views/AdminDashboard.vue"
import AdminTrek from "../views/AdminTrek.vue"
import AdminAddTrek from "../views/AdminAddTrek.vue"
import AdminEditTrek from "../views/AdminEditTrek.vue"


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
    },
    {
        path :"/admin/treks",component:AdminTrek
    },
    {
        path :"/admin/treks/add",component: AdminAddTrek
    },
    {
        path :"/admin/treks/edit/:id",component: AdminEditTrek
    }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})  



export default router