<template>
  <AdminNav>
    <div class="container mt-4">

      <div class="card shadow-sm">

        <div class="card-header d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Assign Staff to Trek</h4>

          <router-link to="/admin/staff" class="btn btn-secondary btn-sm">
            Back
          </router-link>
        </div>

        <div class="card-body">

          <form @submit.prevent="assignStaff">

            <!-- Trek Select -->
            <div class="mb-3">
              <label class="form-label">Select Trek</label>

              <select class="form-select" v-model="form.trek_id" required>
                <option value="">Select Trek</option>
                <option
                  v-for="trek in treks"
                  :key="trek.id"
                  :value="trek.id"
                >
                  {{ trek.trek_name }} - {{ trek.location }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label">Selected Staff</label>
              <input
                type="text"
                class="form-control"
                :value="staffName"
                readonly
              />
            </div>
    

            <button type="submit" class="btn btn-success">
              Assign Staff
            </button>

          </form>

        </div>
      </div>

    </div>
  </AdminNav>
</template>

<script>
import axios from "axios";
import AdminNav from "../components/AdminNav.vue";

export default {
  name: "AdminAssignTrek",

  components: {
    AdminNav
  },

  data() {
    return {
      staffNames:"",
      treks: [],
      form: {
        trek_id: "",
        staff_id: ""
      }
    };
  },

  methods: {

    async getTreks() {
      const token = localStorage.getItem("token");

      const res = await axios.get("http://127.0.0.1:5000/admin/get_treks", {
        headers: { Authorization: `Bearer ${token}` }
      });

      this.treks = res.data.treks;
    },

    async getStaff() {
      const token = localStorage.getItem("token");

      const res = await axios.get("http://127.0.0.1:5000/admin/staff", {
        headers: { Authorization: `Bearer ${token}` }
      });

      this.staff = res.data.staff;
    },

    async assignStaff() {
      try {
        const token = localStorage.getItem("token");

        const res = await axios.post(
          "http://127.0.0.1:5000/admin/assign_staff",
          this.form,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert(res.data.message);

        this.form.trek_id = "";
        this.form.staff_id = "";

      } catch (error) {
        console.log(error);
        alert(error.response?.data?.message || "Assignment failed");
      }
    }

  },

  mounted() {
    this.form.staff_id = this.$route.query.staff_id;
    this.staffName = this.$route.query.name;
    this.getTreks();
  }
};
</script>