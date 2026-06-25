<template>
  <div class="register-page">
    <div class="card shadow register-card">
      <div class="card-body p-4">

        <h2 class="text-center mb-4">
          Create Account
        </h2>

        <form @submit.prevent="register">

          <div class="mb-3">
            <label class="form-label">Username</label>
            <input
              v-model="username"
              type="text"
              class="form-control"
              placeholder="Enter username"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="Enter email"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input
              v-model="full_name"
              type="text"
              class="form-control"
              placeholder="Enter full name"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Phone</label>
            <input
              v-model="phone"
              type="text"
              class="form-control"
              placeholder="Enter phone number"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Age</label>
            <input
              v-model="age"
              type="number"
              class="form-control"
              placeholder="Enter age"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Gender</label>
            <select
              v-model="gender"
              class="form-select"
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
              v-model="address"
              class="form-control"
              rows="3"
              placeholder="Enter address"
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Enter password"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Confirm Password</label>
            <input
              v-model="confirmPassword"
              type="password"
              class="form-control"
              placeholder="Confirm password"
            >
          </div>

          <button
            type="submit"
            class="btn btn-success w-100"
          >
            Register
          </button>

        </form>

        <div
          v-if="message"
          class="alert alert-info mt-3"
        >
          {{ message }}
        </div>

        <p class="text-center mt-3">
          Already have an account?
          <router-link to="/">
            Login
          </router-link>
        </p>

      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api"

export default {
  name: "RegisterView",

  data() {
    return {
      username: "",
      email: "",
      full_name: "",
      phone: "",
      age: "",
      gender: "",
      address: "",
      password: "",
      confirmPassword: "",
      message: ""
    }
  },

  methods: {
    async register() {

      if (this.password !== this.confirmPassword) {
        this.message = "Passwords do not match"
        return
      }

      try {

        const response = await api.post("/register", {
          username: this.username,
          email: this.email,
          password: this.password,
          full_name: this.full_name,
          phone: this.phone,
          age: this.age,
          gender: this.gender,
          address: this.address
        })

        alert(response.data.message)

        this.$router.push("/")

      } catch (error) {

        this.message =
          error.response?.data?.message ||
          "Registration Failed"

      }
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(
    135deg,
    #0f2027,
    #203a43,
    #2c5364
  );
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.register-card {
  width: 550px;
  border-radius: 15px;
}

h2 {
  color: #2c5364;
  font-weight: 700;
}
</style>x