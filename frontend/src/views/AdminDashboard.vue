<template>
  <AdminNav>
    <div class="container py-3">

      <h1 class="mb-4">Dashboard</h1>

      <div class="row">

        <div class="col-md-4 mb-3">
          <div class="card p-3 shadow-sm text-center">
            <h4>Total Treks</h4>
            <h2>0</h2>
          </div>
        </div>

        <div class="col-md-4 mb-3">
          <div class="card p-3 shadow-sm text-center">
            <h4>Total Trekking Staff</h4>
            <h2>0</h2>
          </div>
        </div>

        <div class="col-md-4 mb-3">
          <div class="card p-3 shadow-sm text-center">
            <h4>Total Users (Trekkers)</h4>
            <h2>0</h2>
          </div>
        </div>

        <div class="col-md-4 mb-3">
          <div class="card p-3 shadow-sm text-center">
            <h4>Total Bookings</h4>
            <h2>0</h2>
          </div>
        </div>

      </div>

      <!-- Recent Bookings Section -->
      <div class="mt-4">
        <h3 class="mb-3">Recent Bookings</h3>

        <div class="card p-3 shadow-sm">
          <ul class="mb-0">
            <li v-for="booking in bookings" :key="booking.id">
              {{ booking.id }} - {{ booking.trek_id }} - {{ booking.status }}
            </li>
          </ul>
        </div>

      </div>

    </div>
  </AdminNav>
</template>

<script>
import AdminNav from "../components/AdminNav.vue";

export default {
  components: {
    AdminNav,
  },
  data() {
    return {
      bookings: []
    };
  }
};
</script>