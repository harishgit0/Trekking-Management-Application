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

            <form>

              <div class="mb-3">
                <label class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter username"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  placeholder="Enter email"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter full name"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Phone</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter phone number"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Age</label>
                <input
                  type="number"
                  class="form-control"
                  placeholder="Enter age"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Gender</label>

                <select class="form-select">
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
                ></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>

                <input
                  type="password"
                  class="form-control"
                  placeholder="Enter password"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Confirm Password</label>

                <input
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
  }
}
</script>