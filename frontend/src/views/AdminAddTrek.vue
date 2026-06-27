<template>
  <AdminNav>

    <div class="container">

      <div class="mb-3">
        <router-link
          to="/admin/treks"
          class="btn btn-secondary"
        >
          Back to Treks
        </router-link>
      </div>

      <div class="card shadow-sm">

        <div class="card-header">
          <h4>Add New Trek</h4>
        </div>

        <div class="card-body">

          <form @submit.prevent="addTrek">

            <div class="mb-3">
              <label class="form-label">Trek Name</label>
              <input
                type="text"
                class="form-control"
                v-model="newTrek.trek_name"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Location</label>
              <input
                type="text"
                class="form-control"
                v-model="newTrek.location"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Description</label>
              <textarea
                class="form-control"
                rows="4"
                v-model="newTrek.description"
                required
              ></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label">Difficulty</label>

              <select
                class="form-select"
                v-model="newTrek.difficulty"
                required
              >
                <option value="">Select Difficulty</option>
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
                v-model.number="newTrek.duration_days"
                min="1"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Total Slots</label>

              <input
                type="number"
                class="form-control"
                v-model.number="newTrek.total_slots"
                min="1"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Start Date</label>

              <input
                type="date"
                class="form-control"
                v-model="newTrek.start_date"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">End Date</label>

              <input
                type="date"
                class="form-control"
                v-model="newTrek.end_date"
                required
              >
            </div>

            <button
              type="submit"
              class="btn btn-success"
            >
              Add Trek
            </button>

          </form>

        </div>

      </div>

    </div>

  </AdminNav>
</template>

<script>
import axios from "axios"
import AdminNav from "../components/AdminNav.vue"

export default {
  name: "AdminAddTrek",

  components: {
    AdminNav
  },

  data() {
    return {
      newTrek: {
        trek_name: "",
        location: "",
        description: "",
        difficulty: "",
        duration_days: 1,
        total_slots: 1,
        start_date: "",
        end_date: ""
      }
    }
  },

  methods: {

    formatDate(dateString) {
      const date = new Date(dateString)

      const day = String(date.getDate()).padStart(2, "0")
      const month = String(date.getMonth() + 1).padStart(2, "0")
      const year = date.getFullYear()

      return `${day}-${month}-${year}`
    },

    async addTrek() {

      try {

        const token = localStorage.getItem("token")

        const payload = {
          trek_name: this.newTrek.trek_name,
          location: this.newTrek.location,
          description: this.newTrek.description,
          difficulty: this.newTrek.difficulty,
          duration_days: this.newTrek.duration_days,
          total_slots: this.newTrek.total_slots,
          start_date: this.formatDate(this.newTrek.start_date),
          end_date: this.formatDate(this.newTrek.end_date)
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/admin/create_trek",
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        alert(response.data.message)

        this.$router.push("/admin/treks")

      } catch (error) {

        console.error(error)

        alert(
            error.response?.data?.message ||
            "Failed to create trek"
        )
        }
    }
  }
}
</script>