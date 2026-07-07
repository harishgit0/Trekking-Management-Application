<template>
  <div class="container mt-4">

    <!-- Dashboard Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Staff Dashboard</h2>
        <p class="text-muted mb-0">
          Manage your assigned treks and responsibilities
        </p>
      </div>

      <button class="btn btn-danger" @click="logout">
        Logout
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">

      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <h5>Total Assigned Treks</h5>
            <h2>{{ totalTreks }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <h5>Upcoming Treks</h5>
            <h2>{{ upcomingTreks }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <h5>Completed Treks</h5>
            <h2>{{ completedTreks }}</h2>
          </div>
        </div>
      </div>

    </div>

    <!-- Assigned Treks -->
    <div class="card shadow-sm mb-4">
      <div class="card-header">
        <h5 class="mb-0">Assigned Treks</h5>
      </div>

      <div class="card-body">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Trek Name</th>
              <th>Location</th>
              <th>Start Date</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="trek in assignedTreks" :key="trek.id">
              <td>{{ trek.trek_name }}</td>
              <td>{{ trek.location }}</td>
              <td>{{ trek.start_date }}</td>
              <td>
                <span class="badge bg-success">
                  {{ trek.status }}
                </span>
              </td>
            </tr>

            <tr v-if="assignedTreks.length === 0">
              <td colspan="4" class="text-center">
                No treks assigned yet.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="card shadow-sm">
      <div class="card-header">
        <h5 class="mb-0">Quick Actions</h5>
      </div>

      <div class="card-body">
        <router-link to="/staff/assign-trek" class="btn btn-primary me-2">
          Assigned Trek
        </router-link>

        <router-link to="/staff/profile" class="btn btn-secondary">Profile</router-link>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import router from "../router";

export default {
  name: "StaffDashboard",

  data() {
    return {
      totalTreks: 0,
      upcomingTreks: 0,
      completedTreks: 0,
      assignedTreks: {}
    };
  },

  methods: {
    logout() {
      localStorage.clear();
      this.$router.replace("/login");
    },

    async getStats() {
      try {
        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/staff/dashboard_counts",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.totalTreks = response.data.total_assigned_treks;
        this.upcomingTreks = response.data.upcoming_treks;
        this.completedTreks = response.data.completed_treks;

      } catch (error) {
        console.error("Stats Error:", error);

        if (error.response) {
          console.log(error.response.data);
        }
      }
    },

    async get_trek() {
      try {
        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/staff/get_treks",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.assignedTreks = response.data.treks;

      } catch (error) {
        console.error("Treks Error:", error);

        if (error.response) {
          console.log(error.response.data);
        }
      }
    }
  },

  mounted() {
    this.getStats();
    this.get_trek();
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

h2 {
  font-weight: 600;
}

.table td,
.table th {
  vertical-align: middle;
}
</style>