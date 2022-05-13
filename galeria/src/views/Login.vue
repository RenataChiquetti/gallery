
<template>
  <b-container>
    <b-row>
      <div class="col-lg-4 col-md-6 col-sm-8 mx-auto">
        <b-card style="margin-top: 30vh" title="Login">
          <b-alert v-model="validation.error" variant="danger" dismissible>
            {{ validation.message }}
          </b-alert>
          <b-form @submit="onSubmit">
            <b-form-group
              id="input-group-1"
              label="Nickname:"
              label-for="input-1"
            >
              <b-form-input
                      id="input-1"
                      v-model="form.name"
                      type="text"
                      placeholder="Enter your Nickname"
                      required
              >
              </b-form-input>
            </b-form-group>

            <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
              <b-form-input
                id="input-2"
                v-model="form.password"
                placeholder="Enter your password"
                required
                type = "password"
              >
              </b-form-input>
            </b-form-group>

            <b-button type="submit" variant="primary" class="color:gray;">Submit</b-button>
            <br/>
          </b-form>
        </b-card>
      </div>
    </b-row>
  </b-container>
</template>


<script>
  import api from "../api";
  import Cookies from 'universal-cookie';

  export default {
    data() {
      return {
        form: {
          name: '',
          password: '',
          errors: false
        },
        validation: {
          error: false,
          message: ""
        }
      }
    },

    methods: {
      async onSubmit(event) {
        event.preventDefault();

        const cookies = new Cookies();

        try {
          const response = await api.post("/login", {
            name: this.form.name,
            password: this.form.password
          });

          this.validation.error = false;

          api.setAuthToken(response.data.token);

          const user = await api.get("/login");

          cookies.set("user_token", JSON.stringify({
            token: response.data.token,
            exp: response.data.exp,
            idAdm: user.data.is_adm,
            id: user.data.id
          }), {
            path: "/",
            expires: new Date(response.data.exp),
            maxAge: 21600
          });

          document.location.href = "/";

        } catch (e) {
          this.validation.message = e.response.data;
          this.validation.error = true;
        }
      }
    }
  }
</script>
