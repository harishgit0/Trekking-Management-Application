<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>My Bookings</h2>
        <p class="text-muted mb-0">
          View all your booked treks
        </p>
      </div>

      <router-link
        to="/trekker"
        class="btn btn-secondary"
      >
        Back to Dashboard
      </router-link>
    </div>

    <!-- Booking Table -->
    <div class="card shadow-sm">

      <div class="card-header">
        <h5 class="mb-0">Booked Treks</h5>
      </div>

      <div class="card-body p-0">

        <table class="table table-hover mb-0">

          <thead class="table-light">

            <tr>
              <th>#</th>
              <th>Trek</th>
              <th>Location</th>
              <th>Dates</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>

          </thead>

          <tbody>

            <tr
              v-for="(booking,index) in bookings"
              :key="booking.id"
            >

              <td>{{ index+1 }}</td>

              <td>
                {{ booking.trek_name }}
              </td>

              <td>
                {{ booking.location }}
              </td>

              <td>
                {{ booking.start_date }}
                <br>
                <small class="text-muted">
                  to {{ booking.end_date }}
                </small>
              </td>

              <td>
                {{ booking.booking_date }}
              </td>

              <td>

                <span
                  class="badge"
                  :class="{
                    'bg-primary': booking.booking_status==='Booked',
                    'bg-success': booking.booking_status==='Completed',
                    'bg-danger': booking.booking_status==='Cancelled'
                  }"
                >
                  {{ booking.booking_status }}
                </span>

              </td>

            </tr>

            <tr v-if="bookings.length===0">

              <td
                colspan="6"
                class="text-center py-4"
              >
                No bookings found.
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default{

name:"TrekkerMyBooking",

data(){

return{

bookings:[]

}

},

methods:{

async getBookings(){

try{

const token=localStorage.getItem("token");

const response=await axios.get(
"http://127.0.0.1:5000/trekker/my_bookings",
{
headers:{
Authorization:`Bearer ${token}`
}
}
);
this.bookings=response.data.bookings;

}catch(error){

console.log(error);

}

}

},

mounted(){

this.getBookings();

}

}
</script>

<style scoped>

.card{
border-radius:12px;
}

.card-header{
font-weight:600;
}

.badge{
font-size:0.85rem;
}

.table td{
vertical-align:middle;
}

</style>