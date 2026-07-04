<template>
  <AdminNav>

    <div class="container">

      <div class="card shadow-sm mt-4">

        <div class="card-header d-flex justify-content-between align-items-center">
          <h4 class="mb-0">Add Trekking Staff</h4>

          <router-link
            to="/admin/staff"
            class="btn btn-secondary"
          >
            Back
          </router-link>
        </div>

        <div class="card-body">

          <form @submit.prevent="addStaff">

            <div class="mb-3">
              <label class="form-label">Username</label>
              <input
                type="text"
                class="form-control"
                v-model="staff.username"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Full Name</label>
              <input
                type="text"
                class="form-control"
                v-model="staff.full_name"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Email</label>
              <input
                type="email"
                class="form-control"
                v-model="staff.email"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                v-model="staff.password"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Phone</label>
              <input
                type="text"
                class="form-control"
                v-model="staff.phone"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Age</label>
              <input
                type="number"
                class="form-control"
                v-model="staff.age"
                min="18"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Gender</label>

              <select
                class="form-select"
                v-model="staff.gender"
                required
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>

            </div>

            <div class="mb-3">
              <label class="form-label">Address</label>

              <textarea
                class="form-control"
                rows="3"
                v-model="staff.address"
                required
              ></textarea>

            </div>

            <div class="mb-3">
              <label class="form-label">Status</label>

              <select
                class="form-select"
                v-model="staff.active_status"
              >
                <option :value="true">Active</option>
                <option :value="false">Inactive</option>
              </select>

            </div>

            <button
              type="submit"
              class="btn btn-success"
            >
              Add Staff
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
  name: "AdminAddStaff",

  components: {
    AdminNav
  },

  data() {
    return {
      staff: {
        username: "",
        full_name: "",
        email: "",
        password: "",
        phone: "",
        age: "",
        gender: "",
        address: "",
        active_status: true
      }
    };
  },

  methods: {

    async addStaff() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.post(
          "http://127.0.0.1:5000/admin/add_staff",
          this.staff,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        alert(response.data.message);

        this.$router.push("/admin/staff");

      } catch (error) {

        console.log(error);

        alert(
          error.response?.data?.message ||
          "Failed to add staff"
        );

      }

    }

  }

};
</script>