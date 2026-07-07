<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Welcome, {{ username }}</h2>
        <p class="text-muted">Trekker Dashboard</p>
      </div>

      <button class="btn btn-danger" @click="logout">
        Logout
      </button>
    </div>

    <div class="row">

      <!-- Left Sidebar -->
      <div class="col-lg-3 mb-4">

        <div class="card shadow-sm">

          <div class="card-header">
            <h5 class="mb-0">Quick Actions</h5>
          </div>

          <div class="card-body d-grid gap-2">

            <router-link
              to="/trekker/treks"
              class="btn btn-primary"
            >
              Browse Treks
            </router-link>

            <router-link
              to="/trekker/bookings"
              class="btn btn-success"
            >
              My Bookings
            </router-link>

            <router-link
              to="/trekker/history"
              class="btn btn-warning"
            >
              Trek History
            </router-link>

            <router-link
              to="/trekker/profile"
              class="btn btn-info"
            >
              My Profile
            </router-link>

          </div>

        </div>

      </div>

      <!-- Main Content -->
      <div class="col-lg-9">

        <!-- Stats -->
        <div class="row">

          <div class="col-md-3 mb-3">
            <div class="card shadow-sm text-center">
              <div class="card-body">
                <h6>Available Treks</h6>
                <h2>{{ availableTreks }}</h2>
              </div>
            </div>
          </div>

          <div class="col-md-3 mb-3">
            <div class="card shadow-sm text-center">
              <div class="card-body">
                <h6>Booked Treks</h6>
                <h2>{{ bookedTreks }}</h2>
              </div>
            </div>
          </div>

          <div class="col-md-3 mb-3">
            <div class="card shadow-sm text-center">
              <div class="card-body">
                <h6>Upcoming Treks</h6>
                <h2>{{ upcomingTreks }}</h2>
              </div>
            </div>
          </div>

          <div class="col-md-3 mb-3">
            <div class="card shadow-sm text-center">
              <div class="card-body">
                <h6>Completed Treks</h6>
                <h2>{{ completedTreks }}</h2>
              </div>
            </div>
          </div>

        </div>

        <!-- Available Treks -->
        <div class="card shadow-sm mt-4">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Available Treks</h5>
                <span class="badge bg-primary">{{ treks.length }} Treks</span>
            </div>

            <div class="card-body p-0">

                <div class="table-responsive">

                <table class="table table-hover align-middle mb-0">

                    <thead class="table-light">
                    <tr>
                        <th>Trek Name</th>
                        <th>Location</th>
                        <th>Difficulty</th>
                        <th>Duration</th>
                        <th>Slots</th>
                        <th>Status</th>
                        <th></th>
                    </tr>
                    </thead>

                    <tbody>

                    <tr v-for="trek in treks" :key="trek.id">

                        <td>
                        <strong>{{ trek.trek_name }}</strong>
                        </td>

                        <td>{{ trek.location }}</td>

                        <td>
                        <span
                            class="badge"
                            :class="{
                            'bg-success': trek.difficulty === 'Easy',
                            'bg-warning text-dark': trek.difficulty === 'Moderate',
                            'bg-danger': trek.difficulty === 'Hard'
                            }"
                        >
                            {{ trek.difficulty }}
                        </span>
                        </td>

                        <td>{{ trek.duration_days }} Days</td>

                        <td>
                        {{ trek.available_slots }}/{{ trek.total_slots }}
                        </td>

                        <td>
                        <span
                            class="badge"
                            :class="{
                            'bg-success': trek.status === 'Approved',
                            'bg-warning text-dark': trek.status === 'Pending',
                            'bg-danger': trek.status === 'Cancelled'
                            }"
                        >
                            {{ trek.status }}
                        </span>
                        </td>

                        <td>
                        <button
                            class="btn btn-sm btn-primary"
                            @click="bookTrek(trek.id)"
                        >
                            Book
                        </button>
                        </td>

                    </tr>

                    <tr v-if="treks.length === 0">
                        <td colspan="7" class="text-center py-4 text-muted">
                        No treks available.
                        </td>
                    </tr>

                    </tbody>

                </table>

                </div>

            </div>
            </div>

        <!-- My Bookings -->
        <div class="card shadow-sm mt-4">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">My Bookings</h5>
                <span class="badge bg-success">{{ my_bookings.length }} Bookings</span>
            </div>

            <div class="card-body p-0">

                <div class="table-responsive">

                <table class="table table-hover align-middle mb-0">

                    <thead class="table-light">
                    <tr>
                        <th>Trek Name</th>
                        <th>Location</th>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Booking Status</th>
                    </tr>
                    </thead>

                    <tbody>

                    <tr
                        v-for="booking in my_bookings"
                        :key="booking.id"
                    >
                        <td>
                        <strong>{{ booking.trek_name }}</strong>
                        </td>

                        <td>{{ booking.location }}</td>

                        <td>{{ booking.start_date }}</td>

                        <td>{{ booking.end_date }}</td>

                        <td>
                        <span
                            class="badge"
                            :class="{
                            'bg-success': booking.booking_status === 'Booked',
                            'bg-primary': booking.booking_status === 'Completed',
                            'bg-danger': booking.booking_status === 'Cancelled'
                            }"
                        >
                            {{ booking.booking_status }}
                        </span>
                        </td>
                    </tr>

                    <tr v-if="my_bookings.length === 0">
                        <td colspan="5" class="text-center py-4 text-muted">
                        You haven't booked any treks yet.
                        </td>
                    </tr>

                    </tbody>

                </table>

                </div>

            </div>
            </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "TrekkerDashboard",
  data() {
    return {
      username: "",
      availableTreks: 0,
      bookedTreks: 0,
      upcomingTreks: 0,
      completedTreks: 0,
      search: '',
      treks:{},
      my_bookings:{}
    }
  },
  methods:{
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      localStorage.removeItem("role");
      this.$router.push("/login");
    },
    async get_stats(){
      try{
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/trekker/stats",{
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.availableTreks = response.data.available_treks;
        this.bookedTreks = response.data.booked_treks;
        this.upcomingTreks = response.data.upcoming_treks;
        this.completedTreks = response.data.completed_treks;
      }catch(error){
        console.log(error);
      }
    },
    async get_treks(){
      try{
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/trekker/treks",{
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.treks = response.data.treks;
      }catch(error){
        console.log(error);
      }
    },
    bookTrek(id){
      this.$router.push("/trekker/treks/")
    },
    async my_booking(){
      try{
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/trekker/my_bookings",{
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        console.log(response.data.bookings);
        this.my_bookings = response.data.bookings;
      }catch(error){
        console.log(error);
      }
    }
  },
  mounted() {
    const user = JSON.parse(localStorage.getItem("user"));

    if (user) {
      this.username = user.username;
    }
    this.get_stats();
    this.get_treks();
    this.my_booking();
  }
}
</script>