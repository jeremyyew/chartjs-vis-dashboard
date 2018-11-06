import Vue from 'vue';
import Utils from '../utils';

const Store = {
  state: {
    charts: {},
  },
  logIndex: 0,
  log(prev, key) {
    console.log(`************************************\n${this.logIndex}: <${key}>: STORE STATE CHANGE: ${prev} -> ${Utils.stringify(this.state[key])}\n************************************`);
    this.logIndex += 1;
  },
  registerPrintableChart(id, included = true) {
    const prev = Utils.stringify(this.state.charts);
    // this.state.charts[id] = { included };
    this.state.charts = Object.assign({}, this.state.charts,
      {
        [id]: {
          included,
        },
      });
    this.log(prev, 'charts');
  },
  toggleIncluded(id, included) {
    // if (this.state.charts[id] === undefined) {
    //   console.log(`STORE: chart id ${id} Not registered!`);
    //   return;
    // }
    if (this.state.charts[id].included !== included) {
      const prev = Utils.stringify(this.state.charts);
      this.state.charts[id].included = included;
      this.log(prev, 'charts');
    }
  },
};


export default Store;
