<script>
// Importing Line class from the vue-chartjs wrapper
import { Bar } from 'vue-chartjs';
import utils from '@/utils';
// Exporting this so it can be used in other components

export default {
  extends: Bar,
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
            scaleLabel: utils.labelUtil(this.yLabel),
          }],
          xAxes: [{
            gridLines: {
              display: false,
            },
            ticks: {
              autoSkip: false,
            },
            scaleLabel: utils.labelUtil(this.xLabel),
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
