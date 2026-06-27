<template>
  <AdminNav>

    <div class="container-fluid">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Manage Treks</h2>

        <router-link to="/admin/treks/add" class="btn btn-primary">Add Trek</router-link>
      </div>

      <div class="card shadow-sm">

        <div class="card-body">

          <table class="table table-striped table-hover">

            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Duration</th>
                <th>Slots</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              <tr v-for="trek in treks" :key="trek.id">

                <td>{{ trek.id }}</td>
                <td>{{ trek.trek_name }}</td>
                <td>{{ trek.location }}</td>
                <td>{{ trek.difficulty }}</td>
                <td>{{ trek.duration_days }} Days</td>
                <td>{{ trek.available_slots }}</td>
                <td>{{ trek.status }}</td>

                <td>

                  <router-link :to="`/admin/treks/edit/${trek.id}`"class="btn btn-primary btn-sm">Edit</router-link>

                  <button
                    class="btn btn-danger btn-sm"
                    @click="deleteTrek(trek.id)"
                  >
                    Delete
                  </button>

                </td>

              </tr>

              <tr v-if="treks.length === 0">
                <td colspan="8" class="text-center">
                  No Treks Available
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
  name: "AdminTrek",

  components: {
    AdminNav
  },

  data() {
    return {
      showAddModal: false,
      treks: []
    };
  },
  methods: {

    async deleteTrek(id) {

  if (!confirm("Are you sure you want to delete this trek?")) {
    return;
  }

  try {

    const token = localStorage.getItem("token");

    const response = await axios.delete(
      `http://127.0.0.1:5000/admin/delete_trek/${id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert(response.data.message);

    this.getTrek();

  } catch (error) {

    console.error(error);

    alert(
      error.response?.data?.message ||
      "Failed to delete trek"
    );
  }
},
    getTrek() {
  const token = localStorage.getItem("token");

  axios.get(
    "http://127.0.0.1:5000/admin/get_treks",
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )
  .then((response) => {
    this.treks = response.data.treks;
  })
  .catch((error) => {
    console.log(error);
  });
}
  },
  mounted() {
    this.getTrek();
  },
};
</script>