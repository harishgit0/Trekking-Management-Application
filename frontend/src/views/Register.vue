<template>
  <div>

    <Navbar />

    <div class="container mt-5">

      <div class="row justify-content-center">

        <div class="col-md-8">

          <div class="card shadow p-4">

            <h2 class="text-center mb-4">
              Register
            </h2>

            <form @submit.prevent="register">

              <div class="mb-3">
                <label class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter username"
                  v-model="username"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  placeholder="Enter email"
                  v-model="email"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter full name"
                  v-model="full_name"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Phone</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter phone number"
                  v-model="phone"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Age</label>
                <input
                  type="number"
                  class="form-control"
                  placeholder="Enter age"
                  v-model="age"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Gender</label>

                <select class="form-select" v-model="gender">
                  <option>Male</option>
                  <option>Female</option>
                  <option>Other</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Address</label>

                <textarea
                  class="form-control"
                  rows="3"
                  placeholder="Enter address"
                  v-model="address"
                ></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>

                <input
                  type="password"
                  class="form-control"
                  placeholder="Enter password"
                  v-model="password"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Confirm Password</label>

                <input
                  type="password"
                  class="form-control"
                  placeholder="Confirm password"
                  v-model="confirm_password"
                >
              </div>

              <button
                type="submit"
                class="btn btn-success w-100"
              >
                Register
              </button>

            </form>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default {
  name: "RegisterView",

  components: {
    Navbar
  },
  data() {
    return {
        "username": "",
        "email": "",
        "full_name": "",
        "phone": "",
        "age": "",
        "gender": "",
        "address": "",
        "password": "",
        "confirm_password": ""
    };
  },
  methods:{
    async register() {
      try {
        console.log({
          username: this.username,
          email: this.email,
          full_name: this.full_name,
          phone: this.phone,
          age: this.age,
          gender: this.gender,
          address: this.address,
          password: this.password,
          confirm_password: this.confirm_password
        });
        const response = await fetch(
          "http://127.0.0.1:5000/register",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              username: this.username,
              email: this.email,
              full_name: this.full_name,
              phone: this.phone,
              age: this.age,
              gender: this.gender,
              address: this.address,
              password: this.password,
              confirm_password: this.confirm_password
            })
          }
        );

        const data = await response.json();

        console.log(data);

        if (response.ok) {
          alert(data.message);
          this.$router.push("/login");
        } else {
          alert(data.message);
        }

      } catch (error) {
        console.error(error);
        alert("Registration failed");
      }
    }
  }
}
</script>