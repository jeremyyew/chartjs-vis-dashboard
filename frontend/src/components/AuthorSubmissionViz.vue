<template>
  <div>
    <!--&lt;!&ndash;Visualization 4.1&ndash;&gt;-->
    <el-select
      v-model="topAcceptedAffiliationChartType"
      placeholder="Select Chart"
      style="margin-top: 20px; margin-right: 10px"
    >
      <el-option
        v-for="item in chartOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-select
      v-model="topAcceptedAffiliationDataLength"
      placeholder="Select Length"
      style="margin-top: 20px;margin-right: 10px"
    >
      <el-option
        v-for="item in dataLengthOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-switch
      v-model="topAcceptedAffiliationChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      id="topAcceptedAffiliationChart"
      ref="topAcceptedAffiliationChart"
    >
      <hori-bar-chart
        v-if="topAcceptedAffiliationChartType=='bar'"
        :data-input="topAcceptedAffiliationData"
        :title-text="'Top Accepted Affiliations'"
        class="chart"
      />
      <pie-chart
        v-else-if="topAcceptedAffiliationChartType=='pie'"
        :data-input="topAcceptedAffiliationData"
        :title-text="'Top Affiliations'"
        class="chart"
      />
    </div>
    <!--End of Visualization 4.1-->
  </div>
</template>

<script>
  import HoriBarChart from '@/components/HoriBarChart';
  import PieChart from '@/components/PieChart';
  import Const from './Const';

  import {
    dummyTopAcceptedAffiliationData,
  } from '../mocks/TopAcceptedAffiliationMock';

  export default {
    name: 'AuthorSubmissionViz',
    components: {
      HoriBarChart,
      PieChart,
    },
    props: ['chartData', 'inputFileName'],
    data() {
      return {
        topAcceptedAffiliationChartType: 'bar',
        chartOptions: [
          {
            value: 'pie',
            label: 'Pie Chart',
          }, {
            value: 'bar',
            label: 'Bar Chart',
          },
        ],
        topAcceptedAffiliationDataLength: 3,
        dataLengthOptions: [
          {
            value: 2,
            label: '2',
          },
          {
            value: 3,
            label: '3',
          },
          {
            value: 4,
            label: '4',
          },
          {
            value: 5,
            label: '5',
          },
          {
            value: 6,
            label: '6',
          },
          {
            value: 7,
            label: '7',
          },
          {
            value: 8,
            label: '8',
          },
          {
            value: 9,
            label: '9',
          },
          {
            value: 10,
            label: '10',
          },
        ],
        topAcceptedAffiliationChartIncluded: true,
        topAcceptedAffiliationData: this.computeTopAcceptedAffiliationData(3),
      };
    },
    watch: {
      topAcceptedAffiliationDataLength(newValue, oldValue) {
        this.topAcceptedAffiliationData = this.computeTopAcceptedAffiliationData(newValue);
      },
    },
    methods: {
      chooseColorScheme(len) {
        switch (len) {
          case 2:
            return Const.colorScheme2;
          case 3:
            return Const.colorScheme3;
          case 4:
            return Const.colorScheme3;
          case 5:
            return Const.colorScheme5;
          case 6:
            return Const.colorScheme6;
          case 7:
            return Const.colorScheme7;
          case 8:
            return Const.colorScheme8;
          case 9:
            return Const.colorScheme9;
          default:
            return Const.colorScheme10;
        }
      },
      computeTopAcceptedAffiliationData(len) {
        const scheme = this.chooseColorScheme(len);

        return {
          labels: this.chartData.topAcceptedAffiliations.labels.slice(0, len),
          datasets: [
            {
              label: 'No. of Accepted Papers',
              backgroundColor: scheme,
              pointBackgroundColor: 'white',
              borderWidth: 1,
              pointBorderColor: '#249EBF',
              data: this.chartData.topAcceptedAffiliations.data.slice(0, len),
            },
          ],
        };
      },
    }

  };
</script>

<style scoped>

</style>
