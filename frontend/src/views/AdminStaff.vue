<template>
  <AdminNav>

    <div class="container-fluid">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Manage Trekking Staff</h2>

        <router-link
          to="/admin/staff/add"
          class="btn btn-primary"
        >
          Add Staff
        </router-link>
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
                <th>Assigned Treks</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="staff in staffMembers"
                :key="staff.id"
              >
                <td>{{ staff.id }}</td>
                <td>{{ staff.full_name }}</td>
                <td>{{ staff.email }}</td>
                <td>{{ staff.phone }}</td>

                <td>
                  <span
                    class="badge"
                    :class="staff.active_status ? 'bg-success' : 'bg-danger'"
                  >
                    {{ staff.active_status ? "Active" : "Inactive" }}
                  </span>
                </td>

                <td>
                  {{ staff.assigned_treks || 0 }}
                </td>

                <td>

                  <router-link
                    :to="`/admin/staff/edit/${staff.id}`"
                    class="btn btn-warning btn-sm me-2"
                  >
                    Edit
                  </router-link>

                  <router-link
                    :to="{
                      path: '/admin/assign-trek',
                      query: {
                        staff_id: staff.id,
                        name: staff.username
                      }
                    }"
                    class="btn btn-primary btn-sm"
                  >
                    Assign Trek
                  </router-link>

                </td>

              </tr>

              <tr v-if="staffMembers.length === 0">
                <td colspan="7" class="text-center">
                  No Staff Members Found
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
import router from "../router/index.js";

export default {
  name: "AdminStaff",

  components: {
    AdminNav
  },

  data() {
    return {
      staffMembers: []
    };
  },

  methods: {

    async getStaff() {

      try {

        const token = localStorage.getItem("token");

        const response = await axios.get(
          "http://127.0.0.1:5000/admin/staff",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        this.staffMembers = response.data.staff;

      } catch (error) {

        console.log(error);

      }

    }

  },

  mounted() {

    this.getStaff();

  }

};
</script>