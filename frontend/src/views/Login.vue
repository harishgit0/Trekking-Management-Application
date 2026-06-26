<template>
  <div>

    <Navbar />

    <div class="container mt-5">

      <div class="row justify-content-center">

        <div class="col-md-6">

          <div class="card shadow p-4">

            <h2 class="text-center mb-4">
              Login
            </h2>

            <form @submit.prevent="login">

              <!-- Username -->
              <div class="mb-3">
                <label class="form-label">
                  Username
                </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="username"
                  placeholder="Enter username"
                >
              </div>

              <!-- Password -->
              <div class="mb-3">
                <label class="form-label">
                  Password
                </label>

                <input
                  type="password"
                  class="form-control"
                  v-model="password"
                  placeholder="Enter password"
                >
              </div>

              <!-- Button -->
              <button
                type="submit"
                class="btn btn-primary w-100"
              >
                Login
              </button>

            </form>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import api from "../services/api"
import Navbar from "../components/Navbar.vue"

export default {
  name: "LoginView",

  components: {
    Navbar
  },
  data() {
    return {username:"",password:""}
  },
  methods:{
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

    if(response.data.user.role === "admin"){
      this.$router.push("/admin")
    }

  }
  catch(error) {

    console.log(error.response.data)

  }

}
  }
  
}
</script>