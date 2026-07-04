<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>My Profile</h2>
        <p class="text-muted">
          View and update your profile information
        </p>
      </div>

      <router-link
        to="/staff"
        class="btn btn-secondary"
      >
        Back to Dashboard
      </router-link>
    </div>

    <div class="card shadow-sm">

      <div class="card-header">
        <h5>Profile Details</h5>
      </div>

      <div class="card-body">

        <div class="row">

          <div class="col-md-6 mb-3">
            <label class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              v-model="profile.username"
              disabled
            >
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              v-model="profile.email"
              disabled
            >
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Full Name</label>
            <input
              type="text"
              class="form-control"
              v-model="profile.full_name"
            >
          </div>

          <div class="col-md-6 mb-3">
            <label class="form-label">Phone</label>
            <input
              type="text"
              class="form-control"
              v-model="profile.phone"
            >
          </div>

          <div class="col-md-4 mb-3">
            <label class="form-label">Age</label>
            <input
              type="number"
              class="form-control"
              v-model="profile.age"
            >
          </div>

          <div class="col-md-4 mb-3">
            <label class="form-label">Gender</label>
            <select
              class="form-select"
              v-model="profile.gender"
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="col-md-4 mb-3">
            <label class="form-label">Role</label>
            <input
              type="text"
              class="form-control"
              v-model="profile.role"
              disabled
            >
          </div>

          <div class="col-12 mb-3">
            <label class="form-label">Address</label>
            <textarea
              class="form-control"
              rows="3"
              v-model="profile.address"
            ></textarea>
          </div>

        </div>

      </div>

      <div class="card-footer">

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StaffProfile",

  data() {
    return {
      profile: {
        username: "",
        email: "",
        full_name: "",
        phone: "",
        age: "",
        gender: "",
        address: "",
        role: ""
      }
    };
  },

  methods: {
    async getProfile() {
      try {
        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/staff/profile",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.profile = response.data.staff;

      } catch (error) {
        console.log(error);
      }
    }
  },

  mounted() {
    this.getProfile();
  }
};
</script>

<style scoped>
.card {
  border-radius: 12px;
}

.card-header {
  font-weight: 600;
}
</style>