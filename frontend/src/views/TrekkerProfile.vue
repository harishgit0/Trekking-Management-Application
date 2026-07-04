<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>My Profile</h2>
        <p class="text-muted mb-0">
          View your personal information
        </p>
      </div>

      <router-link
        to="/trekker"
        class="btn btn-secondary"
      >
        Back to Dashboard
      </router-link>
    </div>

    <div class="row justify-content-center">

      <div class="col-lg-8">

        <div class="card shadow-sm">

          <div class="card-header">
            <h5 class="mb-0">Profile Information</h5>
          </div>

          <div class="card-body">

            <div class="row">

              <div class="col-md-6 mb-3">
                <label class="form-label fw-bold">Username</label>
                <input
                  type="text"
                  class="form-control"
                  :value="user.username"
                  readonly
                >
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label fw-bold">Email</label>
                <input
                  type="email"
                  class="form-control"
                  :value="user.email"
                  readonly
                >
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label fw-bold">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  :value="user.full_name"
                  readonly
                >
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label fw-bold">Phone</label>
                <input
                  type="text"
                  class="form-control"
                  :value="user.phone"
                  readonly
                >
              </div>

              <div class="col-md-4 mb-3">
                <label class="form-label fw-bold">Age</label>
                <input
                  type="text"
                  class="form-control"
                  :value="user.age"
                  readonly
                >
              </div>

              <div class="col-md-4 mb-3">
                <label class="form-label fw-bold">Gender</label>
                <input
                  type="text"
                  class="form-control"
                  :value="user.gender"
                  readonly
                >
              </div>

              <div class="col-md-4 mb-3">
                <label class="form-label fw-bold">Role</label>
                <input
                  type="text"
                  class="form-control"
                  :value="user.role"
                  readonly
                >
              </div>

              <div class="col-12 mb-3">
                <label class="form-label fw-bold">Address</label>
                <textarea
                  class="form-control"
                  rows="3"
                  readonly
                >{{ user.address }}</textarea>
              </div>

            </div>

          </div>

          <div class="card-footer text-end">

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TrekkerProfile",

  data() {
    return {
      user: {}
    };
  },

  methods: {

    async getProfile() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/trekker/profile",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        // console.log(response.data);
        this.user = response.data.trekker;

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

.card{
    border-radius:12px;
}

.card-header{
    font-weight:600;
}

.form-control,
textarea{
    background:#f8f9fa;
}

</style>