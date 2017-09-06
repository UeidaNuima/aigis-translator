import Vue from 'vue';
import Router from 'vue-router';
import Main from '@/components/Main';
import File from '@/components/File';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: Main,
    },
    {
      path: '/file/:id',
      name: 'file',
      component: File,
    },
  ],
});
