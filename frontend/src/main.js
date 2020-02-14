import Vue from 'vue'
import App from './App.vue'
import router from './router'
import utils from './utils'

Vue.config.productionTip = false
Vue.mixin(utils)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
