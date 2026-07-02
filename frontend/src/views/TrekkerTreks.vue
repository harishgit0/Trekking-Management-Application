<template>
  <div class="container mt-4">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Browse Treks</h2>
        <p class="text-muted mb-0">
          Search and book your next trekking adventure
        </p>
      </div>

      <router-link
        to="/trekker"
        class="btn btn-secondary"
      >
        Back to Dashboard
      </router-link>
    </div>

    <!-- Search & Filters -->
    <div class="card shadow-sm mb-4">
      <div class="card-body">

        <div class="row g-3">

          <div class="col-md-5">
            <input
              type="text"
              class="form-control"
              placeholder="Search trek or location..."
              v-model="search"
            >
          </div>

          <div class="col-md-3">
            <select
              class="form-select"
              v-model="difficulty"
            >
              <option value="">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div class="col-md-2">
            <button
              class="btn btn-primary w-100"
              @click="searchTreks"
            >
              Search
            </button>
          </div>

          <div class="col-md-2">
            <button
              class="btn btn-outline-secondary w-100"
              @click="resetFilters"
            >
              Reset
            </button>
          </div>

        </div>

      </div>
    </div>

    <!-- Available Treks -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h4 class="mb-0">Available Treks</h4>

      <span class="badge bg-primary fs-6">
        {{ treks.length }} Treks
      </span>
    </div>

    <div class="row">

      <div
        class="col-lg-4 col-md-6 mb-4"
        v-for="trek in treks"
        :key="trek.id"
      >

        <div class="card h-100 shadow-sm">

          <div class="card-header d-flex justify-content-between">

            <h5 class="mb-0">
              {{ trek.trek_name }}
            </h5>

            <span
              class="badge"
              :class="{
                'bg-success': trek.difficulty=='Easy',
                'bg-warning text-dark': trek.difficulty=='Moderate',
                'bg-danger': trek.difficulty=='Hard'
              }"
            >
              {{ trek.difficulty }}
            </span>

          </div>

          <div class="card-body">

            <p>
              <strong>📍 Location:</strong><br>
              {{ trek.location }}
            </p>

            <p>
              <strong>📅 Trek Dates:</strong><br>
              {{ trek.start_date }} to {{ trek.end_date }}
            </p>

            <p>
              <strong>⏳ Duration:</strong>
              {{ trek.duration_days }} Days
            </p>

            <p>
              <strong>👥 Slots:</strong>
              {{ trek.available_slots }}/{{ trek.total_slots }}
            </p>

            <p>
              <strong>Status:</strong>

              <span
                class="badge"
                :class="{
                  'bg-success': trek.status=='Approved',
                  'bg-warning text-dark': trek.status=='Pending',
                  'bg-danger': trek.status=='Cancelled'
                }"
              >
                {{ trek.status }}
              </span>
            </p>

            <hr>

            <p class="small text-muted">
              {{ trek.description }}
            </p>

          </div>

          <div class="card-footer bg-white">

            <button
              class="btn btn-success w-100"
              @click="bookTrek(trek.id)"
              :disabled="trek.available_slots===0"
            >
              Book Trek
            </button>

          </div>

        </div>

      </div>

    </div>

    <!-- Empty State -->
    <div
      v-if="treks.length===0"
      class="alert alert-info text-center mt-4"
    >
      No treks found.
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TrekkerTreks",

  data() {
    return {
      treks: [],
      allTreks: [],
      search: "",
      difficulty: ""
    };
  },

  methods: {

    async getTreks() {
      try {
        const token = localStorage.getItem("token");

        const response = await axios.get("http://127.0.0.1:5000/trekker/treks",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.allTreks = response.data.treks;
        this.treks = this.allTreks.slice(0, 7);
      } catch (error) {
        console.log(error);
      }
    },

    searchTreks() {
      const keyword = this.search.toLowerCase().trim();

      this.treks = this.allTreks.filter(trek => {
        const matchesSearch =
          trek.trek_name.toLowerCase().includes(keyword) ||
          trek.location.toLowerCase().includes(keyword);

        const matchesDifficulty =
          this.difficulty === "" ||
          trek.difficulty === this.difficulty;

        return matchesSearch && matchesDifficulty;
      });
    },

    resetFilters() {
      this.search = "";
      this.difficulty = "";
      this.treks = this.allTreks.slice(0, 7);
    },

    async bookTrek(id) {

        const confirmBooking = confirm(
            "Are you sure you want to book this trek?"
        );

        if (!confirmBooking) {
            return;
        }

        try {

            const token = localStorage.getItem("token");

            const response = await axios.post(
            `http://127.0.0.1:5000/trekker/book/${id}`,
            {},
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
            );

            alert(response.data.message);

            // Refresh trek list
            this.getTreks();

        } catch (error) {

            if (error.response) {
            alert(error.response.data.message);
            }

        }
        }

  },

  mounted() {
    this.getTreks();
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

.card-footer{
    background:white;
}

.badge{
    font-size:0.8rem;
}

</style>