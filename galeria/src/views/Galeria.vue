<template>
  <div>
    <div>
      <NavBar/>
    </div>
    <b-container fluid >
      <b-alert v-model="error" variant="danger" dismissible>
        {{ message }}
      </b-alert>
      <div style="display: flex; flex-wrap: wrap; gap:10px; justify-content:center" class="mt-3">
        <div v-for="post in posts">
          <div style="width: 300px">
            <Post
              :post = "post"
            />
          </div>
        </div>
      </div>
    </b-container>
  </div>
</template>


<script>
import api from "../api"

import Post from '@/components/Post.vue'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'Galeria',
  components: {
    Post,
    NavBar
  },
  data() {
    return {
      error: false,
      message: "",
      posts:[]
    }
  },
  created() {
    this.getPosts();
  },
  methods: {
    async getPosts() {
      try {
        this.error = false;
        const posts = await api.get("/post?allowed=1");

        this.posts = posts.data;
      } catch(e) {
        this.error = true;
        this.message = e.response.data;
      }
    }
  }
}
</script>
