// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './index.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import VueCookies from 'vue-cookies'
import './style/index.css'
import echarts from 'echarts'

Vue.prototype.$echarts = echarts 
Vue.use(VueCookies)
Vue.use(ElementUI);
Vue.config.productionTip = false
const baseURL = window.g.baseURL
Vue.prototype.Ip = baseURL
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
