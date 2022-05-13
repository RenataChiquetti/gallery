<template>
  <div>
    <div>
      <NavBar/>
      <b-container>
        <b-row>
          <b-card class="mt-4 w-100 p-3" title="New post" >
            <b-alert v-model="validate.error" variant="danger" dismissible>
              {{ validate.message }}
            </b-alert>
            <b-alert v-model="validate.success" variant="success" dismissible>
              Post created with success!
            </b-alert>
            <b-form @submit="uploadPost">
              <b-form-group  label-for="form-image">
                <b-input-group>
                  <b-input-group-prepend is-text>
                    <b-icon icon="image-fill"></b-icon>
                  </b-input-group-prepend>
                  <b-form-file v-model="file" id="form-image" placeholder="Select an image" accept="image/jpeg, image/png, image/jpg"></b-form-file>
                </b-input-group>
              </b-form-group>

              <div style="text-align: right;">
                <b-button variant="success" ref="submit" type="submit">Submit</b-button>
              </div>
            </b-form>
          </b-card>
        </b-row>
      </b-container>
    </div>
  </div>
</template>


<script>

import api from "../api";
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'Galeria',
  components: {
    NavBar
  },
  data() {
    return {
      file: null,
      validate: {
        error: false,
        success: false,
        message: ""
      }
    }
  },
  methods: {
    async uploadPost(e) {
      e.preventDefault();
      this.validate.error = false;

      if (this.file == null) {
        this.validate.error = true;
        this.validate.message = "You must select an image.";
        return;
      }

      try {
        const formData = new FormData();
        formData.append("file", this.file);

        const response = await api.post("/post", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });

        this.validate.success = true;
      } catch(e) {
        this.validate.error = true;
        this.validate.message = e.response.data;
      }
    }
  }
}

</script>
