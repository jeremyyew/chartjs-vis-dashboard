// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import ECharts from 'vue-echarts/components/ECharts';

// import ECharts modules manually to reduce bundle size
// for each plot category (line, bar, etc), it must be imported here manually otherwise cannot be
// used
import 'echarts/lib/chart/bar';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/polar';
import 'echarts/lib/chart/line';

import VueAxios from 'vue-axios';
import axios from 'axios';
import VueAuthenticate from 'vue-authenticate';
import App from './App';
import router from './router';

Vue.config.productionTip = false;
Vue.use(ElementUI);

Vue.component('chart', ECharts);
// Vue.use(ECharts)

Vue.use(VueAxios, axios);
Vue.use(VueAuthenticate, {
  baseUrl: process.env.VUE_APP_API_BASE_URL,
  registerUrl: process.env.VUE_APP_DEFAULT_REGISTRATION_URL,
  loginUrl: process.env.VUE_APP_DEFAULT_LOGIN_URL,
  tokenType: 'JWT',
  providers: {
    facebook: {
      clientId: process.env.VUE_APP_FACEBOOK_CLIENT_ID,
      redirectUri: process.env.VUE_APP_REDIRECT_URI,
      url: process.env.VUE_APP_SOCIAL_LOGIN_URL,
    },
    google: {
      clientId: process.env.VUE_APP_GOOGLE_CLIENT_ID,
      redirectUri: process.env.VUE_APP_REDIRECT_URI,
      url: process.env.VUE_APP_SOCIAL_LOGIN_URL,
    },
    github: {
      clientId: process.env.VUE_APP_GITHUB_CLIENT_ID,
      redirectUri: process.env.VUE_APP_REDIRECT_URI,
      url: process.env.VUE_APP_SOCIAL_LOGIN_URL,
    },
  },
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
