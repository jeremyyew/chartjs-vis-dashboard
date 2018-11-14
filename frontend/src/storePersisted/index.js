import VuePersist from 'vue-persist';
import Vue from 'vue';
import Const from '@/components/Const';
const { DEFAULT_STORE_NAME } = Const;

Vue.use(VuePersist, { read: () => {}, name: DEFAULT_STORE_NAME });
const cache = ((JSON.parse(localStorage.getItem(DEFAULT_STORE_NAME)) || {}).data || {}).storePersistedState;
const Store = {
  state: cache || {
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
//
// const StoreComponent = new Vue({
//   data: {
//     state: {
//       loggedIn: false,
//       username: null,
//       vizData: null,
//     },
//   },
//   persist: ['state'],
// });
//
// export function (Vue, {
//   name: defaultStoreName = 'persist:store',
//   expiration: defaultExpiration,
//   read = k => localStorage.getItem(k),
//   write = (k, v) => localStorage.setItem(k, v),
//   clear = k => localStorage.removeItem(k)
// } = {}) {
//   const cache = {}
//
//   Vue.prototype.$persist = function (names, storeName = defaultStoreName, storeExpiration = defaultExpiration) {
//     let store = cache[storeName] = JSON.parse(read(storeName) || '{}')
//     store.data = store.data || {}
//
//     if (isExpired(store.expiration)) {
//       clear(storeName)
//       store = {
//         data: {},
//         expiration: getExpiration(storeExpiration)
//       }
//     }
//
//     if (!store.expiration) {
//       store.expiration = getExpiration(storeExpiration)
//     }
//
//     this._persistWatchers = this._persistWatchers || []
//
//     for (const name of names) {
//       if (typeof store.data[name] !== 'undefined') {
//         this[name] = store.data[name]
//       }
//
//       if (this._persistWatchers.indexOf(name) === -1) {
//         this._persistWatchers.push(name)
//
//         this.$watch(name, val => {
//           store.data[name] = val
//           write(storeName, JSON.stringify(store))
//         })
//       }
//     }
//   }
// }
//
// function getExpiration(exp) {
//   return exp ? Date.now() + exp : 0
// }
//
// function isExpired(exp) {
//   return exp && (Date.now() > exp)
// }

export default Store;
