<template>
  <div>
    <div>
      <NavBar/>
      <b-container>
        <b-row>
          <b-card class="mt-4 w-100 p-3" title="Create User" >
            <b-alert v-model="form.error" variant="danger" dismissible>
              {{ form.message }}
            </b-alert>
            <b-alert v-model="form.success" variant="success" dismissible>
              User created with success.
            </b-alert>
            <b-form @submit="createUser">
                <div class="d-flex justify-content-center">
                    <b-form-input class="mr-4" v-model="form.name" placeholder="User name"></b-form-input>
                    <b-form-input v-model="form.password" placeholder="Password"></b-form-input>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b-form-checkbox v-model="form.is_adm" class="mt-3" value="true">Is adm</b-form-checkbox>
                    <div style="text-align: right;">
                        <b-button type="submit" variant="success" class="color:gray; mt-3">Create</b-button>
                    </div> 
                </div>
            </b-form>
          </b-card>
        </b-row>

        <b-row>
          <b-card class="mt-4 w-100 p-3" title="Users" >
            <b-alert v-model="deleteUsers.error" variant="danger" dismissible>
                {{ deleteUsers.message }}
            </b-alert>
            <b-alert v-model="deleteUsers.success" variant="success" dismissible>
                User deleted with success.
            </b-alert>
            <hr>
            <div v-for="user in users">
                <div style="display: flex; justify-content: space-between; align-items: center;" class="mt-4">
                    <div>
                        <h5>{{user.name}}</h5>
                    </div>
                    <div style="text-align: right;">
                        <b-button @click="deleteUser(user.id)" variant="danger">Delete</b-button>
                    </div> 
                </div>
            </div>
          </b-card>
        </b-row>

      </b-container>
    </div>
  </div>
</template>


<script>

import api from "../api"
import NavBar from '@/components/NavBar.vue'

export default {
    name: 'ConfigUser',
    components: {
        NavBar
    },
    data() {
      return {
        form: {
            name: '',
            password: '',
            is_adm: false,
            error: false,
            success: false,
            message: ""
        },
        deleteUsers: {
            error: false,
            success: false,
            message: ""
        },
        users: []
      }
    },
    created() {
        this.fetchUsers();
    },
    methods: {
        async createUser(e) {
            e.preventDefault();

            try {
                this.form.error = false;

                const response = await api.post("/user", {
                    name: this.form.name,
                    password: this.form.password,
                    is_adm: this.form.is_adm
                });

                this.form.name = "";
                this.form.password = "";
                this.form.is_adm = false;

                await this.fetchUsers();

                this.form.success = true;
            } catch (e) {
                this.form.error = true;
                this.form.message = e.response.data;
            }
        },

        async fetchUsers() {
           try {
                const response = await api.get("/user");

                this.users = response.data;
            } catch (e) {
                this.deleteUsers.error = true;
                this.deleteUsers.message = e.response.data;
            } 
        },

        async deleteUser(id) {
           try {
                this.deleteUsers.error = false;

                await api.delete(`/user/${id}`);

                await this.fetchUsers();

                this.deleteUsers.success = true;
            } catch (e) {
                this.deleteUsers.error = true;
                this.deleteUsers.message = e.response.data;
            } 
        },
    }
}

</script>