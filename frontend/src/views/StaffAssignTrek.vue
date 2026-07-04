<template>
  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Assigned Treks</h2>
        <p class="text-muted mb-0">
          View and manage your assigned treks
        </p>
      </div>

      <router-link to="/staff" class="btn btn-primary">Back to Dashboard</router-link>
    </div>

    <div class="row">

      <div
        class="col-md-6 col-lg-4 mb-4"
        v-for="trek in treks"
        :key="trek.id"
      >
        <div class="card h-100 shadow-sm">

          <div class="card-header">
            <h5 class="mb-0">{{ trek.trek_name }}</h5>
          </div>

          <div class="card-body">

            <p>
              <strong>Location:</strong>
              {{ trek.location }}
            </p>

            <p>
              <strong>Difficulty:</strong>
              {{ trek.difficulty }}
            </p>

            <p>
              <strong>Duration:</strong>
              {{ trek.duration_days }} Days
            </p>

            <p>
              <strong>Start Date:</strong>
              {{ trek.start_date }}
            </p>

            <p>
              <strong>End Date:</strong>
              {{ trek.end_date }}
            </p>

            <p>
              <strong>Available Slots:</strong>
              {{ trek.available_slots }}/{{ trek.total_slots }}
            </p>

            <p>
              <strong>Status:</strong>
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
            </p>

            <p class="small text-muted">
              {{ trek.description }}
            </p>

          </div>

          <div class="card-footer">

            <div class="mb-3">
                <label class="form-label">Available Slots</label>
                <input
                type="number"
                class="form-control"
                v-model="trek.available_slots"
                >
            </div>

            <div class="mb-3">
                <label class="form-label">Status</label>
                <select
                class="form-select"
                v-model="trek.status"
                >
                <option value="Pending">Closed</option>
                <option value="Started">Started</option>
                </select>
            </div>

            <div class="d-grid gap-2">

                <button
                class="btn btn-danger"
                @click="completeTrek(trek)"
                :disabled="trek.status === 'Completed'"
                >
                Mark as Completed
                </button>

                <button
                class="btn btn-primary"
                @click="updateTrek(trek)"
                >
                Update Trek
                </button>

                <button
                class="btn btn-info"
                @click="viewParticipants(trek.id)"
                >
                View Participants
                </button>

            </div>

            </div>

        </div>
      </div>

    </div>

    <div
      v-if="treks.length === 0"
      class="alert alert-info text-center"
    >
      No treks assigned yet.
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StaffAssignTrek",

  data() {
    return {
      treks: []
    };
  },

  methods: {
    async getTreks() {
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

        this.treks = response.data.treks;

      } catch (error) {
        console.log(error);
      }
    },
    async updateTrek(trek) {
        try {
        const token = localStorage.getItem("token");

        await axios.put(
            `http://127.0.0.1:5000/staff/update_trek/${trek.id}`,
            {
            available_slots: trek.available_slots,
            status: trek.status
            },
            {
            headers: {
                Authorization: `Bearer ${token}`
            }
            }
        );

        alert("Trek updated successfully");
        this.$router.push("/staff");
        

        } catch (error) {
        console.log(error);
        }
    },

    async completeTrek(trek) {
        trek.status = "Completed";
        await this.updateTrek(trek);
    },

    viewParticipants(trekId) {
        this.$router.push(`/staff/participants/${trekId}`);
    }
  },

  mounted() {
    this.getTreks();
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
</style>