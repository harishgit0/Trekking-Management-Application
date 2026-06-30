<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Participants</h2>
        <p class="text-muted">
          View trekkers registered for this trek
        </p>
      </div>

      <router-link
        to="/staff/assign-trek"
        class="btn btn-secondary"
      >
        Back
      </router-link>
    </div>

    <!-- Trek Info -->
    <div class="card shadow-sm mb-4">
      <div class="card-header">
        <h5>{{ trek.trek_name }}</h5>
      </div>

      <div class="card-body">
        <div class="row">

          <div class="col-md-4">
            <p>
              <strong>Location:</strong>
              {{ trek.location }}
            </p>
          </div>

          <div class="col-md-4">
            <p>
              <strong>Start Date:</strong>
              {{ trek.start_date }}
            </p>
          </div>

          <div class="col-md-4">
            <p>
              <strong>Status:</strong>
              {{ trek.status }}
            </p>
          </div>

        </div>
      </div>
    </div>

    <!-- Participant Count -->
    <div class="card shadow-sm mb-4">
      <div class="card-body text-center">
        <h5>Total Participants</h5>
        <h2>{{ participants.length }}</h2>
      </div>
    </div>

    <!-- Participants Table -->
    <div class="card shadow-sm">
      <div class="card-header">
        <h5>Participant List</h5>
      </div>

      <div class="card-body">

        <table class="table table-striped table-hover">

          <thead>
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Email</th>
              <th>Booking Date</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="(participant, index) in participants"
              :key="participant.id"
            >
              <td>{{ index + 1 }}</td>

              <td>{{ participant.username }}</td>

              <td>{{ participant.email }}</td>

              <td>{{ participant.booking_date }}</td>

              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-success':
                      participant.booking_status === 'Booked',

                    'bg-danger':
                      participant.booking_status === 'Cancelled'
                  }"
                >
                  {{ participant.booking_status }}
                </span>
              </td>
            </tr>

            <tr v-if="participants.length === 0">
              <td colspan="5" class="text-center">
                No participants found.
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

export default {
  name: "StaffPart",

  data() {
    return {
      trek: {},
      participants: []
    };
  },

  methods: {
    async getParticipants() {
      try {
        const token = localStorage.getItem("token");
        const trekId = this.$route.params.id;

        const response = await axios.get(
          `http://127.0.0.1:5000/staff/participants/${trekId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.trek = response.data.trek;
        this.participants = response.data.participants;

      } catch (error) {
        console.log(error);
      }
    }
  },

  mounted() {
    this.getParticipants();
  }
};
</script>

<style scoped>
.card {
  border-radius: 12px;
}

.card-header {
  font-weight: 600;
}

table {
  vertical-align: middle;
}
</style>