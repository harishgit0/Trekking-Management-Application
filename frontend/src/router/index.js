import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import AdminDashboard from "../views/AdminDashboard.vue"
import AdminTrek from "../views/AdminTrek.vue"
import AdminAddTrek from "../views/AdminAddTrek.vue"
import AdminEditTrek from "../views/AdminEditTrek.vue"
import AdminTrekkers from "../views/AdminTrekkers.vue"
import AdminEditTrekker from "../views/AdminEditTrekker.vue"
import AdminStaff from "../views/AdminStaff.vue"
import AdminAddStaff from "../views/AdminAddStaff.vue"
import AdminEditStaff from "../views/AdminEditStaff.vue"
import AdminAssignTrek from "../views/AdminAssignTrek.vue"
import AdminBooking from "../views/AdminBooking.vue"
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
    },
    {
        path :"/admin/trekkers",component:AdminTrekkers
    },
    {
        path :"/admin/trekker/edit/:id",component: AdminEditTrekker
    },
    {
        path :"/admin/staff",component:AdminStaff
    },
    {
        path :"/admin/staff/add",component:AdminAddStaff
    },
    {
        path :"/admin/staff/edit/:id",component:AdminEditStaff
    },
    {
        path :"/admin/assign-trek",component:AdminAssignTrek
    },
    {
        path :"/admin/booking",component:AdminBooking
    }
]


const router = createRouter({
  history: createWebHistory(),
  routes
})  



export default router