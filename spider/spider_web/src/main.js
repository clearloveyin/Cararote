import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from '@/router/router'
import store from '@/store/store'
import '@/plugins/element.js'
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false
new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
Vue.use(VueCookies)
