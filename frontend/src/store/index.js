import Vue from 'vue';
import utils from '../utils';
import Const from '@/components/Const';

const Store = {
  state: {
    charts: {},
    activeTab: {
      value: Const.VIZ_TYPES.AUTHOR,
    },
  },
  switchActiveTab(tabname) {
    if (this.state.activeTab.value !== tabname) {
      console.log("SWITCHING!!!!!!!");
      // const prev = Object.assign({}, this.state);
      this.state.activeTab.value = tabname;
      // this.log('activeTab', prev);
    }
  },
  logIndex: 0,
  log(key, prevState) {
    // console.log(`************************************\n${this.logIndex}: <${key}>: STORE STATE CHANGE: ${utils.stringify(prevState)} -> ${utils.stringify(this.state)}\n************************************`);
    this.logIndex += 1;
  },
  registerPrintableChart(id, included = true) {
    const prev = this.state;
    this.state.charts = Object.assign({}, this.state.charts,
      {
        [id]: {
          included,
        },
      });
    this.log('charts', prev);
  },
  toggleIncluded(id, included) {
    if (this.state.charts[id].included !== included) {
      const prev = this.state;
      this.state.charts[id].included = included;
      this.log('charts', prev);
    }
  },
};


export default Store;
