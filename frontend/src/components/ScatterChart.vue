<script>
import { Scatter } from 'vue-chartjs';
import utils from '@/utils';

export default {
  extends: Scatter,
  props: ['dataInput', 'titleText', 'xLabel', 'yLabel'],
  data() {
    return {
      // Chart.js options that controls the appearance of the chart
      options: {
        title: {
          display: true,
          text: this.titleText,
          fontSize: 14,
        },
        scales: {
          yAxes: [{
            scaleLabel: utils.labelUtil(this.yLabel),
            ticks: {
              beginAtZero: true,
              callback(value, index, values) {
                if (Math.floor(value) === value) {
                  return value;
                }
              },
              // stepSize: 1
            },
            gridLines: {
              display: true,
            },
          }],
          xAxes: [{
            scaleLabel: utils.labelUtil(this.xLabel),
            gridLines: {
              display: false,
            },
            ticks: {
              autoSkip: false,
            },
          }],
        },
        legend: {
          display: true,
        },
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  computed: {
    chartData() {
      return this.dataInput;
    },
  },
  watch: {
    dataInput() {
      console.log('Got it in the bar chart!');
      // this.renderChart(this.dataInput, this.options);
      this.$data._chart.destroy();
      this.render();
      // this._chart.update();
    },
  },
  mounted() {
    // this.renderChart(this.dataInput, this.options)
    this.render();
  },
  methods: {
    render() {
      this.renderChart(this.chartData, this.options);
    },
  },
};
</script>

<style scoped>

</style>
