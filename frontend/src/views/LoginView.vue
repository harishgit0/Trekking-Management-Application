<template>
  <div class="login-page">
    
    <div class="card shadow login-card">
      <div class="card-body p-4">

        <h2 class="text-center mb-4">
          Login
        </h2>

        <form @submit.prevent="login">

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
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Enter password"
            >
          </div>

          <button
            type="submit"
            class="btn btn-success w-100"
          >
            Login
          </button>
          <p>Don't have an account? <router-link to="/register">Register</router-link></p>

        </form>

        <div
          v-if="message"
          class="alert alert-danger mt-3"
        >
          {{ message }}
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import api from "../services/api"

export default {
  data() {
    return {
      username: "",
      password: "",
      message: ""
    }
  },

  methods: {
    async login() {
        try {

            const response = await api.post("/login", {
            username: this.username,
            password: this.password
            })

            localStorage.setItem(
            "token",
            response.data.token
            )

            localStorage.setItem(
            "user",
            JSON.stringify(response.data.user)
            )

            const role = response.data.user.role

            if(role === "admin"){
            this.$router.push("/admin")
            }
            else{
            this.$router.push("/user")
            }

        } catch(error) {

            console.log(error)
            console.log(error.response)

            this.message =
            error.response?.data?.message ||
            "Login Failed"

        }
        }
  }
}
</script>

<style scoped>
.login-page {
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
}

.login-card {
    width: 420px;
    border-radius: 15px;
}

h2 {
    font-weight: 700;
    color: #2c5364;
}
</style>