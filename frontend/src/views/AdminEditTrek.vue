<template>
  <AdminNav>

    <div class="card shadow-sm mt-4">

      <div class="card-header">
        <h4>Edit Trek</h4>
      </div>

      <div class="card-body">

        <form @submit.prevent="updateTrek">

          <div class="mb-3">
            <label class="form-label">Trek Name</label>
            <input
              type="text"
              class="form-control"
              v-model="trek.trek_name"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Location</label>
            <input
              type="text"
              class="form-control"
              v-model="trek.location"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Description</label>
            <textarea
              class="form-control"
              rows="4"
              v-model="trek.description"
              required
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label">Difficulty</label>

            <select
              class="form-select"
              v-model="trek.difficulty"
              required
            >
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Duration (Days)</label>
            <input
              type="number"
              class="form-control"
              v-model="trek.duration_days"
              min="1"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Total Slots</label>
            <input
              type="number"
              class="form-control"
              v-model="trek.total_slots"
              min="1"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Available Slots</label>
            <input
              type="number"
              class="form-control"
              v-model="trek.available_slots"
              min="0"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Start Date</label>
            <input
              type="date"
              class="form-control"
              v-model="trek.start_date"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">End Date</label>
            <input
              type="date"
              class="form-control"
              v-model="trek.end_date"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Status</label>

            <select
              class="form-select"
              v-model="trek.status"
            >
              <option value="Pending">Pending</option>
              <option value="Approved">Approved</option>
              <option value="Closed">Closed</option>
            </select>
          </div>

          <button
            type="submit"
            class="btn btn-warning"
            @click="updateTrek"
          >
            Update Trek
          </button>

        </form>

      </div>

    </div>

  </AdminNav>
</template>

<script>
import axios from "axios";
import AdminNav from "../components/AdminNav.vue";

export default {
  name: "AdminEditTrek",

  components: {
    AdminNav
  },

  data() {
    return {
      trek: {}
    };
  },

  methods: {

    async getTrek() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
          `http://127.0.0.1:5000/admin/get_trek/${this.$route.params.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.trek = response.data;

      } catch (error) {

        console.log(error);

        alert("Failed to load trek");

      }

    },

async updateTrek() {

  try {

    const token = localStorage.getItem("token");

    const response = await axios.put(
      `http://127.0.0.1:5000/admin/update_trek/${this.$route.params.id}`,
      this.trek,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert(response.data.message);

    this.$router.push("/admin/treks");

  } catch (error) {

    console.log(error);

    alert(
      error.response?.data?.message ||
      "Failed to update trek"
    );

  }

}

  },

  mounted() {

    this.getTrek();

  }

};
</script>