<template>
  <div>
    <b-card :title="post.name">
    <hr>
      <b-alert v-model="validate.error" variant="danger" dismissible>
        {{ validate.message }}
      </b-alert>
      <div style="display:flex; width:100%; justify-content:center; align-items:center;">
        <b-img style="max-width:250px;max-height:250px;width:auto;height:auto;" :src="post.path" fluid alt="Responsive image"></b-img>
      </div>
      <div style="display: flex; justify-content: left; align-items: center;" class="mt-2">
        <div style="display: flex; align-items: center;" class="mr-4">
          <a href="#" @click="makeLike" style="color: #000;" v-if="!like.isLiked"><b-icon icon="hand-thumbs-up-fill" class="mr-2"></b-icon></a>
          <a href="#" @click="makeLike" style="color: #e74c3c;" v-if="like.isLiked"><b-icon icon="hand-thumbs-up-fill" class="mr-2"></b-icon></a>
          <h6 class="bold center mt-2" ><strong>{{like.counter}}</strong></h6>
        </div>
        <div style="display: flex; align-items: center;">
          <a href="#" @click="comments.commentsOpen = !comments.commentsOpen" style="color: #000;"><b-icon icon="chat-dots-fill" class="mr-2"></b-icon></a>
          <h6 class="bold center mt-2"><strong>{{comments.commentsNumber}}</strong></h6>
        </div>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center;" class="mt-2">
          <b-form-textarea
            id="textarea-no-resize"
            placeholder="Comment something."
            v-model="comments.newValue"
            no-resize
          ></b-form-textarea>
          <a href="#" @click="makeComment" style="color: #000;" class="h4 ml-2"><b-icon icon="cursor-fill"></b-icon></a>
      </div>
    </b-card>
    <b-modal v-model="comments.commentsOpen" scrollable hide-footer title="Comments">
      <div v-for="item in comments.comments">
        <p class="fs-15 grey-label" style="margin-bottom:0px;"><strong> {{item.name}}</strong></p>
        <p>{{item.content}}</p>
      </div>
    </b-modal>
  </div>
</template>


<script>

import api from '@/api';
import Cookies from 'universal-cookie';

export default {
  props: {
    post: {}
  },
  name: 'Post',
  data() {
    return {
      validate: {
        error: false,
        message: "",
      },
      comments: {
        comments: [],
        commentsNumber: 0,
        commentsOpen: false,
        newValue: ""
      },
      like: {
        counter: 0,
        isLiked: false
      },
      userId: 0
    }
  },
  created() {
    this.getComments();
    this.getLikes();
    this.checkLike();

    const cookies = new Cookies();

    const user = cookies.get("user_token");
    this.userId = user.id;
  },
  methods: {
    async getComments() {
      try {
        this.validate.error = false;

        const comments = await api.get(`/comment?post_id=${this.post.id}`);

        this.comments.comments = comments.data;
        this.comments.commentsNumber = comments.data.length;
      } catch(e) {
        this.validate.error = true;
        this.validate.message = e.response.data;
      }
    },
    async getLikes() {
      try {
        this.validate.error = false;

        const like = await api.get(`/like/${this.post.id}`);

        this.like.counter = like.data;
      } catch(e) {
        this.validate.error = true;
        this.validate.message = e.response.data;
      }
    },
    async checkLike() {
      try {
        this.validate.error = false;

        const like = await api.get(`/like/user/${this.post.id}`);

        this.like.isLiked = like.data;
      } catch(e) {
        this.validate.error = true;
        this.validate.message = e.response.data;
      }
    },
    async makeLike() {
      try {
        this.validate.error = false;

        const like = await api.post(`/like`, {
          post_id: this.post.id
        });

        this.checkLike();
        this.getLikes();
      } catch(e) {
        this.validate.error = true;
        this.validate.message = e.response.data;
      }
    },
    async makeComment() {
      try {
        this.validate.error = false;

        if (this.comments.newValue == "") {
          this.validate.error = true;
          this.validate.message = "Cannot make empty comment.";
          return;
        }

        const comment = await api.post(`/comment`, {
          content: this.comments.newValue,
          user_id: this.userId,
          post_id: this.post.id
        });

        this.comments.newValue = "";

        this.getComments();
      } catch(e) {
        this.validate.error = true;
        this.validate.message = e.response.data;
      }
    }
  }
}

</script>
