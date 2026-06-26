<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">

    <div class="container">

      <router-link
        class="navbar-brand"
        to="/"
      >
        Trekking Management System
      </router-link>

      <div class="navbar-nav ms-auto">

        <router-link
          class="nav-link"
          to="/"
        >
          Home
        </router-link>

        <router-link
          class="nav-link"
          to="/login"
        >
          Login
        </router-link>

        <router-link
          class="nav-link"
          to="/register"
        >
          Register
        </router-link>

      </div>

    </div>

  </nav>
</template>

<script>
export default {
  name: "Navbar"
}
</script>