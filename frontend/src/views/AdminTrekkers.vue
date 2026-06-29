<template>
  <AdminNav>

    <div class="container-fluid">

      <div class="mb-4">
        <h2>Manage Trekkers</h2>
      </div>

      <div class="card shadow-sm">

        <div class="card-body">

          <table class="table table-striped table-hover">

            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="trekker in trekkers"
                :key="trekker.id"
              >
                <td>{{ trekker.id }}</td>
                <td>{{ trekker.full_name }}</td>
                <td>{{ trekker.email }}</td>
                <td>{{ trekker.phone }}</td>
                <td>{{ trekker.active_status ? "Active" : "Blacklisted" }}</td>

                <td>

                  <router-link :to="`/admin/trekker/edit/${trekker.id}`"
                  class="btn btn-primary btn-sm">
                    Edit
                  </router-link>

                  <!-- <button
                    class="btn btn-danger btn-sm"
                  >
                    Blacklist
                  </button> -->

                </td>

              </tr>

              <tr v-if="trekkers.length === 0">
                <td colspan="6" class="text-center">
                  No Trekkers Found
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
  name: "AdminTrekkers",

  components: {
    AdminNav
  },

  data() {
    return {
      trekkers: []
    };
  },
  methods: {
    get_trekkers() {
        const token = localStorage.getItem("token");

        axios.get(
          "http://127.0.0.1:5000/admin/trekkers",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )
        .then((response) => {
          this.trekkers = response.data.trekkers;
        })
        .catch((error) => {
          console.log(error);
        });
    }
  },
  mounted() {
    this.get_trekkers();
  }
};
</script>