<template>

  <div>

    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-dark px-3">

      <span class="navbar-brand">
        Trekking Management System
      </span>

      <button
        class="btn btn-danger"
        @click="logout"
      >
        Logout
      </button>

    </nav>

    <div id="admin-main">

      <!-- Sidebar -->

      <div id="admin-left">

        <router-link to="/admin">
          Dashboard
        </router-link>

        <router-link to="/admin/treks">
          Treks
        </router-link>

        <router-link to="/admin/trekkers">
          Trekkers
        </router-link>

        <router-link to="/admin/staff">
          Staff
        </router-link>

        <router-link to="/admin/bookings">
          Bookings
        </router-link>

      </div>

      <!-- Content Slot -->

      <div id="admin-right">

        <slot></slot>

      </div>

    </div>

  </div>

</template>

<script>
export default {
  name: "AdminNav"
,
methods: {
  logout() {
    localStorage.removeItem("token")
    localStorage.removeItem("user")

    this.$router.push("/login")
  }
}
}

</script>

<style scoped>

#admin-main{
  display:flex;
  min-height:calc(100vh - 56px);
}

#admin-left{
  width:250px;
  background:#212529;
  padding:20px;
}

#admin-left a{
  display:block;
  color:white;
  text-decoration:none;
  padding:10px;
  margin-bottom:10px;
}

#admin-left a:hover{
  background:#343a40;
}

#admin-right{
  flex:1;
  padding:20px;
}

</style>