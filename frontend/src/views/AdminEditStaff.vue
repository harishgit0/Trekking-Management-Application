<template>
  <AdminNav>

    <div class="container mt-4">

      <router-link
        to="/admin/staff"
        class="btn btn-secondary mb-3"
      >
        ← Back to staff
      </router-link>

      <div class="row justify-content-center">

        <div class="col-lg-8">

          <div class="card shadow">

            <div class="card-header bg-primary text-white">
              <h4 class="mb-0">Edit staff</h4>
            </div>

            <div class="card-body p-4">

              <form @submit.prevent="updatestaff">

                <div class="row">

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Full Name</label>
                    <input
                      type="text"
                      class="form-control"
                      v-model="staff.full_name"
                      required
                    >
                  </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Email</label>
                    <input
                      type="email"
                      class="form-control"
                      v-model="staff.email"
                      required
                    >
                  </div>

                </div>

                <div class="row">

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Phone</label>
                    <input
                      type="text"
                      class="form-control"
                      v-model="staff.phone"
                      required
                    >
                  </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Age</label>
                    <input
                      type="number"
                      class="form-control"
                      v-model="staff.age"
                      min="1"
                      required
                    >
                  </div>

                </div>

                <div class="row">

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Gender</label>

                    <select
                      class="form-select"
                      v-model="staff.gender"
                      required
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>

                  </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label">Status</label>

                    <select
                      class="form-select"
                      v-model="staff.active_status"
                    >
                      <option :value="true">Active</option>
                      <option :value="false">Blacklisted</option>
                    </select>

                  </div>

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

                <div class="d-flex gap-2">

                  <button
                    type="submit"
                    class="btn btn-warning"
                  >
                    Update staff
                  </button>

                  <router-link
                    to="/admin/staff"
                    class="btn btn-secondary"
                  >
                    Cancel
                  </router-link>

                </div>

              </form>

            </div>

          </div>

        </div>

      </div>

    </div>

  </AdminNav>
</template>

<script>
import axios from "axios";
import AdminNav from "../components/AdminNav.vue";

export default {
  name: "AdminEditStaff",

  components: {
    AdminNav
  },

  data() {
    return {
      staff: {}
    };
  },

  methods: {

    async getStaff() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
          `http://127.0.0.1:5000/admin/get_staff/${this.$route.params.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.staff = response.data;

      } catch (error) {

        console.log(error);

        alert("Failed to load staff");

      }

    },

    async updatestaff() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.put(
          `http://127.0.0.1:5000/admin/update_staff/${this.$route.params.id}`,
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
          "Failed to update Staff"
        );

      }

    }

  },

  mounted() {

    this.getStaff();

  }

};
</script>