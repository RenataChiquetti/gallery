<template>
  <div>
    <div>
      <NavBar/>
    </div>

    <div>
      <div style="width: 100%; display: flex; justify-content: center; margin-top: 1%;">
        <div style="display: flex; flex-wrap: wrap; gap:10px; justify-content:center; max-width: 1500px;">
          <b-alert v-model="error" variant="danger" dismissible>
              {{ message }}
          </b-alert>
          <div v-for="(post) in posts">
            <b-card style="width: 255px; heigth: 255px;">
              <b-img style="max-width:250px;max-height:250px;width:auto;height:auto;" thumbnail fluid :src="post.path" alt=""></b-img>
              <b-form-checkbox v-model="post.allowed" @change="updatePost(post)" class="mt-2">Allow</b-form-checkbox>
            </b-card>
          </div>
          <b-alert v-model="empty" variant="secondary" dismissible>
              There is no Posts :(
          </b-alert>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api"
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'Permissao',
  components: {
    NavBar
  },
  data() {
    return {
      error: false,
      message: "",
      posts: [],
      empty: false
    }
  },
  created() {
    this.fetchPosts();
  },
  methods: {
    async fetchPosts() {
      try {
        this.error = false;

        const response = await api.get("/post");

        this.posts = response.data;

        if (response.data.length == 0) {
          this.empty = true;
        }

      } catch (e) {
        this.error = true;
        this.message = e.response.data;
      }
    },
  
    async updatePost(post) {
      const newPost = post;
      delete newPost.created_on;
      delete newPost.name;

      try {
        this.error = false;
        
        await api.put("/post", newPost);

      } catch(e) {
        this.error = true;
        this.message = e.response.data;
      }
    }
  }
} 

</script>