import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import { createVuetify } from 'vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import store from './store'
// import './axios.js'

const vuetify = createVuetify()
loadFonts()

const app = createApp(App)

app.use(vuetify)
app.use(router)
app.use(store)

app.mount('#app')