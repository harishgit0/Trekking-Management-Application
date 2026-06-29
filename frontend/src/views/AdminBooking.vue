<template>
  <AdminNav>

    <div class="container-fluid">

      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Manage Bookings</h2>
      </div>

      <!-- Card -->
      <div class="card shadow-sm">

        <div class="card-body">

          <table class="table table-striped table-hover">

            <thead>
              <tr>
                <th>ID</th>
                <th>User</th>
                <th>Trek</th>
                <th>Booking Date</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>

              <tr v-for="booking in bookings" :key="booking.id">

                <td>{{ booking.id }}</td>

                <td>
                  {{ booking.user_name || booking.user_id }}
                </td>

                <td>
                  {{ booking.trek_name || booking.trek_id }}
                </td>

                <td>
                  {{ booking.booking_date || "N/A" }}
                </td>

                <td>
                  <span
                    class="badge"
                    :class="statusClass(booking.status)"
                  >
                    {{ booking.status }}
                  </span>
                </td>

                <td>

                  <button
                    class="btn btn-success btn-sm me-2"
                    v-if="booking.status === 'Pending'"
                    @click="updateStatus(booking.id, 'Approved')"
                  >
                    Approve
                  </button>

                  <button
                    class="btn btn-danger btn-sm me-2"
                    v-if="booking.status === 'Pending'"
                    @click="updateStatus(booking.id, 'Rejected')"
                  >
                    Reject
                  </button>

                </td>

              </tr>

              <tr v-if="bookings && bookings.length === 0">
                <td colspan="6" class="text-center">
                  No Bookings Found
                </td>
              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

  </AdminNav>
</template>
<script>
    import axios from "axios";
    import AdminNav from "../components/AdminNav.vue";
    export default {
        name: "AdminBooking",
        components: {
            AdminNav
        },
        data() {
            return {
                bookings: []
            };
        },
        methods: {
            statusClass(status) {
                if (status === "Booked") {
                    return "bg-success";
                } else if (status === "Rejected") {
                    return "bg-danger";
                } else {
                    return "bg-warning";
                }
            },
            async fetchBookings() {
                try {
                    const token = localStorage.getItem("token");
                    const response = await axios.get("http://127.0.0.1:5000/admin/get_bookings",
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    )
                    this.bookings = response.data.bookings || [];
                } catch (error) {
                    console.error(error);
                    this.bookings = [];
                }
            },
            async updateStatus(bookingId, status) {
                try {
                    await axios.put(`/api/bookings/${bookingId}`, { status });
                    this.fetchBookings();
                } catch (error) {
                    console.error(error);
                }
            }
        },
        mounted() {
            this.fetchBookings();
        }
    }
</script>