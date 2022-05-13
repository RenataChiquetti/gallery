import Vue from 'vue'
import VueRouter from 'vue-router'
import Permissao from '../views/Permissao.vue'
import Galeria from '../views/Galeria.vue'
import Login from '../views/Login.vue'
import Cadastro from '../views/Cadastro.vue'
import ConfigUser from '../views/ConfigUser.vue'
import Cookies from "universal-cookie"
import api from "../api"

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Galeria',
    component: Galeria
  },
  {
    path: '/permissao',
    name: 'Permissao',
    component: Permissao
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/cadastro',
    name: 'Cadastro',
    component: Cadastro
  },
  {
    path: '/configuser',
    name: 'ConfigUser',
    component: ConfigUser
  }

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

const cookies = new Cookies();

router.beforeEach((to, from, next) => {

  const user_token = cookies.get("user_token");

  if ((to.path != '/login') && (!user_token)) {
    next('/login');
    return;
  } else if (from.path == '/login' && (user_token)) {
    api.setAuthToken(user_token.token);
    next("/");
    return;
  } else if ((to.path == '/login') && (user_token)) {
    api.setAuthToken(user_token.token);
    next("/");
    return;
  } else {
    if (user_token) api.setAuthToken(user_token.token);
    next();
    return;
  }
});

export default router;
