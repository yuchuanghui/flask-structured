<template>
  <v-app id="app'">
    <!-- <h1>Test</h1> -->
    <router-view/>
  </v-app>
</template>

<script>
import Blogs from './views/Blogs.vue'
export default {
  name: 'App',
  components: {
    Blogs
  },
  data: () => ({
    //
  }),

}
</script>
