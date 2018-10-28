import VuePersist from 'vue-persist';
import Vue from 'vue';

Vue.use(VuePersist);

const Store = {
  state: {
    loggedIn: false,
    username: null,
    vizData: null,
  },
  logIndex: 0,
  login(username) {
    this.log('username', username);
    this.state.username = username;
    this.log('loggedIn', true);
    this.state.loggedIn = true;
  },
  logout() {
    this.log('username', null);
    this.state.username = null;
    this.log('loggedIn', false);
    this.state.loggedIn = false;
  },
  log(key, newVal) {
    console.log(`************************************\n${this.logIndex}: <${key}> STORE STATE CHANGE: ${this.state[key]} -> ${newVal}\n************************************`);
    this.logIndex += 1;
  },
};

const persister = new Vue({
  data: { state: Store.state },
  persist: ['state'],
});


export default Store;
