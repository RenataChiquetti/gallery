<template>
  
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">Wedding</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/">Gallery</b-nav-item>
        <b-nav-item to="/cadastro">Upload</b-nav-item>
        <b-nav-item to="/permissao" v-if="isAdm">Permissions</b-nav-item>
        
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item to="/configuser" right v-if="isAdm">Cfg User</b-nav-item>
        <b-nav-item @click="logout" right >Logout</b-nav-item>
      </b-navbar-nav>
      
  </b-collapse>
  </b-navbar>
</template>


<script>
import Cookies from "universal-cookie";

const cookies = new Cookies();

export default {
  name: 'NavBar',
  data() {
    return {
      isAdm: false
    }
  },
  created() {
    const user_token = cookies.get("user_token");

    if (!user_token)
      this.isAdm = false;
    else
      this.isAdm = user_token.idAdm;
    
  },
  methods: {
    logout()  {
      cookies.remove("user_token");
      document.location.href = "/login";
    }
  }
}

</script>
