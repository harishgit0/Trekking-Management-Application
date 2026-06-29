<template>
  <AdminNav>
    <div class="container py-4">

      <!-- Header -->
      <div class="mb-4">
        <h2 class="fw-bold">Dashboard</h2>
        <p class="text-muted mb-0">Overview of your trekking system</p>
      </div>

      <!-- STATS CARDS -->
      <div class="row g-4 mb-4">

        <div class="col-md-3">
          <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <p class="text-muted mb-1 small">Total Treks</p>
                <h3 class="fw-bold mb-0 text-primary">{{ count.trek_count }}</h3>
              </div>
              <div class="fs-2">🏔️</div>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <p class="text-muted mb-1 small">Trekking Staff</p>
                <h3 class="fw-bold mb-0 text-success">{{ count.staff_count }}</h3>
              </div>
              <div class="fs-2">👨‍✈️</div>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <p class="text-muted mb-1 small">Trekkers</p>
                <h3 class="fw-bold mb-0 text-warning">{{ count.trekker_count }}</h3>
              </div>
              <div class="fs-2">👥</div>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card border-0 shadow-sm rounded-4 p-3 h-100">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <p class="text-muted mb-1 small">Bookings</p>
                <h3 class="fw-bold mb-0 text-danger">{{ count.booking_count }}</h3>
              </div>
              <div class="fs-2">📌</div>
            </div>
          </div>
        </div>

      </div>

      <!-- RECENT BOOKINGS -->
      <div class="card border-0 shadow-sm rounded-4">

        <div class="card-header bg-white border-0 py-3">
          <h5 class="mb-0 fw-bold">Recent Bookings</h5>
        </div>

        <div class="card-body p-0">

          <div v-if="bookings && bookings.length">
            <div class="table-responsive">
              <table class="table align-middle mb-0">

                <thead class="table-light">
                  <tr>
                    <th>Booking ID</th>
                    <th>Trek ID</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-for="booking in bookings" :key="booking.id">
                    <td class="fw-semibold">#{{ booking.id }}</td>
                    <td>{{ booking.trek_id }}</td>
                    <td>
                      <span class="badge rounded-pill px-3 py-2"
                            :class="statusClass(booking.status)">
                        {{ booking.status }}
                      </span>
                    </td>
                  </tr>
                </tbody>

              </table>
            </div>
          </div>

          <div v-else class="text-center py-5 text-muted">
            <div class="fs-1">📭</div>
            No recent bookings available
          </div>

        </div>
      </div>

    </div>
  </AdminNav>
</template>

<script>
import axios from "axios";
import AdminNav from "../components/AdminNav.vue";

export default {
  components: {
    AdminNav,
  },

  data() {
    return {
      count: {
        trek_count: 0,
        staff_count: 0,
        trekker_count: 0,
        booking_count: 0
      },
      bookings: []
    };
  },

  methods: {

    statusClass(status) {
      switch (status) {
        case "Booked":
          return "bg-success";
        case "Rejected":
          return "bg-danger";
        case "Pending":
          return "bg-warning text-dark";
        default:
          return "bg-secondary";
      }
    },

    async get_count() {
      try {
        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/admin/dashboard_counts",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.count = response.data;

      } catch (error) {
        console.log(error);
      }
    },

    get_booking() {
      const token = localStorage.getItem("token");

      axios.get("http://127.0.0.1:5000/admin/get_bookings", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((response) => {
        this.bookings = response.data.bookings || [];
      })
      .catch((error) => {
        console.log(error);
      });
    }

  },

  mounted() {
    this.get_count();
    this.get_booking();
  }
};
</script>

<style scoped>
.card {
  transition: 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

table td, table th {
  padding: 14px !important;
}
</style>