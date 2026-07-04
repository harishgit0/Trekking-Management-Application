<template>
  <div>

    <Navbar />

    <!-- Hero Section -->
    <div class="container text-center mt-5">

      <h1 class="display-4">
        Trekking Management System
      </h1>

      <p class="lead mt-3">
        Explore, manage and organize trekking adventures efficiently.
      </p>

      <router-link
        to="/login"
        class="btn btn-primary me-2"
      >
        Login
      </router-link>

      <router-link
        to="/register"
        class="btn btn-success"
      >
        Register
      </router-link>

    </div>

    <!-- Features Section -->
    <div class="container mt-5">

      <h2 class="text-center mb-4">
        Features
      </h2>

      <div class="row">

        <div class="col-md-4">
          <div class="card p-3 text-center">
            <h4>Trek Booking</h4>
            <p>Book exciting treks easily.</p>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card p-3 text-center">
            <h4>Management</h4>
            <p>Manage treks and schedules.</p>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card p-3 text-center">
            <h4>Staff Control</h4>
            <p>Assign staff to trekking events.</p>
          </div>
        </div>

      </div>

    </div>

  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default {
  name: "HomeView",

  components: {
    Navbar
  }
}
</script>