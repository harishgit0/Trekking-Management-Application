<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Trekking History</h2>
        <p class="text-muted mb-0">
          View all your completed trekking adventures
        </p>
      </div>

      <router-link
        to="/trekker"
        class="btn btn-secondary"
      >
        Back to Dashboard
      </router-link>
    </div>

    <!-- History Table -->
    <div class="card shadow-sm">

      <div class="card-header">
        <h5 class="mb-0">Completed Treks</h5>
      </div>

      <div class="card-body p-0">

        <table class="table table-hover mb-0">

          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Trek</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Duration</th>
              <th>Trek Dates</th>
              <th>Completed On</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="(history,index) in history"
              :key="history.id"
            >

              <td>{{ index + 1 }}</td>

              <td>{{ history.trek_name }}</td>

              <td>{{ history.location }}</td>

              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-success': history.difficulty==='Easy',
                    'bg-warning text-dark': history.difficulty==='Moderate',
                    'bg-danger': history.difficulty==='Hard'
                  }"
                >
                  {{ history.difficulty }}
                </span>
              </td>

              <td>
                {{ history.duration_days }} Days
              </td>

              <td>
                {{ history.start_date }}
                <br>
                <small class="text-muted">
                  to {{ history.end_date }}
                </small>
              </td>

              <td>
                {{ history.completed_date }}
              </td>

            </tr>

            <tr v-if="history.length===0">
              <td colspan="7" class="text-center py-4">
                No completed treks yet.
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

  name: "TrekkerHistory",

  data() {
    return {
      history: []
    };
  },

  methods: {

    async getHistory() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/trekker/history",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.history = response.data.history;

      } catch (error) {
        console.log(error);
      }

    }

  },

  mounted() {
    this.getHistory();
  }

};
</script>

<style scoped>

.card{
    border-radius:12px;
}

.card-header{
    font-weight:600;
}

.table td{
    vertical-align:middle;
}

.badge{
    font-size:0.8rem;
}

</style>