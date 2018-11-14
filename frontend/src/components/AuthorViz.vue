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
      v-model="storeState.charts[CHART_IDS.TOP_ACCEPTED_AFFILIATION_BAR_PIE_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      :id="CHART_IDS.TOP_ACCEPTED_AFFILIATION_BAR_PIE_ID"
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
        :title-text="'Top Accepted Affiliations'"
        class="chart"
      />
    </div>
    <!--End of Visualization 4.1-->


    <el-select
      v-model="authorDataLength"
      placeholder="Select Length"
      style="margin-top: 10px;margin-right: 40px"
    >
      <el-option
        v-for="item in dataLengthOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-switch
      v-model="storeState.charts[CHART_IDS.TOP_AUTHOR_BAR_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <bar-chart
      :id="CHART_IDS.TOP_AUTHOR_BAR_ID"
      ref="topAuthorChart"
      :data-input="topAuthorData"
      :title-text="'Top Authors'"
      :x-label="'Authors'"
      :y-label="'Submission Counts'"
      class="chart"
    />
    <!--using text.sync for two-way data binding to editable text child component-->
    <editable-text :text.sync="authorText" />


    <el-select
      v-model="countryChartType"
      placeholder="Select Chart"
      style="margin-top: 20px;margin-right: 10px"
    >
      <el-option
        v-for="item in chartOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-select
      v-model="countryDataLength"
      placeholder="Select Length"
      style="margin-top: 20px;margin-right: 30px"
    >
      <el-option
        v-for="item in dataLengthOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-switch
      v-model="storeState.charts[CHART_IDS.TOP_COUNTRY_BAR_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      :id="CHART_IDS.TOP_COUNTRY_BAR_ID"
      ref="topCountryChart"
    >
      <hori-bar-chart
        v-if="countryChartType=='bar'"
        :data-input="topCountryData"
        :title-text="'Top Countries'"
        class="chart"
      />
      <pie-chart
        v-else-if="countryChartType=='pie'"
        :data-input="topCountryData"
        :title-text="'Top Countries'"
        class="chart"
      />
    </div>
    <editable-text :text.sync="countryText" />


    <el-select
      v-model="affiliationChartType"
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
      v-model="affiliationDataLength"
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
      v-model="storeState.charts[CHART_IDS.TOP_SUBMITTED_AFFILIATION_BAR_PIE_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      :id="CHART_IDS.TOP_SUBMITTED_AFFILIATION_BAR_PIE_ID"
      ref="topAffiliationChart"
    >
      <hori-bar-chart
        v-if="affiliationChartType=='bar'"
        :data-input="topAffiliationData"
        :title-text="'Top Affiliations'"
        class="chart"
      />
      <pie-chart
        v-else-if="affiliationChartType=='pie'"
        :data-input="topAffiliationData"
        :title-text="'Top Affiliations'"
        class="chart"
      />
    </div>
    <editable-text :text.sync="affiliationText" />

    <el-button
      type="success"
      plain
      style="margin-top: 10px"
      @click=""
    >Save
    </el-button>
  </div>
</template>

<script>
import BarChart from '@/components/BarChart';
import HoriBarChart from '@/components/HoriBarChart';
import PieChart from '@/components/PieChart';
import Utils from '@/utils';
import EditableText from '@/components/EditableText';
import Const from './Const';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import Store from '@/store';
// visualization 4.1
import {
  dummyTopAcceptedAffiliationData,
} from '../mocks/TopAcceptedAffiliationMock';

const { CHART_IDS } = Const;

export default {
  name: 'AuthorViz',
  components: {
    BarChart,
    HoriBarChart,
    PieChart,
    EditableText,
  },
  props: ['chartData', 'inputFileName'],
  data() {
    const authorInitialText = `So it's rather clear that the one with the largest number of submissions this year is: ${this.chartData.topAuthors.labels[0]}, and all the top ${String(3)}, putting together, contribute ${String(this.chartData.topAuthors.data.slice(0, 3).reduce((a, b) => a + b))} submissions in total.`;

    const countryInitialText = `And from the country information (generated from the author data), we can see that the top 1 country, in this case ${this.chartData.topCountries.labels[0]}, has made ${String(((this.chartData.topCountries.data[0] - this.chartData.topCountries.data[1]) / this.chartData.topCountries.data[1] * 100).toFixed(2))}% more submission than the second-placed ${this.chartData.topCountries.labels[1]}.`;

    return {
      CHART_IDS,
      storeState: Store.state,
      msg: 'Author Info Analysis',
      authorText: {
        val: authorInitialText,
        edit: false,
      },
      countryText: {
        val: countryInitialText,
        edit: false,
      },
      affiliationText: {
        val: 'You may add in any additional remarks here.',
        edit: false,
      },
      topAuthors: this.chartData.topAuthors,
      topCountries: this.chartData.topCountries,
      topAffiliations: this.chartData.topAffiliations,
      chartOptions: [
        {
          value: 'pie',
          label: 'Pie Chart',
        }, {
          value: 'bar',
          label: 'Bar Chart',
        },
      ],
      countryChartType: 'pie',
      affiliationChartType: 'bar',
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
      authorDataLength: 3,
      countryDataLength: 3,
      affiliationDataLength: 3,
      countryChartIncluded: true,
      affiliationChartIncluded: true,
      topAuthorData: this.computeAuthorData(3),
      topCountryData: this.computeCountryData(3),
      topAffiliationData: this.computeAffiliationData(3),
      //  visualization 4.1
      topAcceptedAffiliationChartType: 'bar',
      topAcceptedAffiliationChartIncluded: true,
      topAcceptedAffiliationDataLength: 3,
      topAcceptedAffiliationData: this.computeTopAcceptedAffiliationData(3),
    };
  },
  watch: {
    authorDataLength(newValue, oldValue) {
      const len = newValue;
      const authorInitialText = `So it's rather clear that the one with the largest number of submissions this year is: ${this.topAuthors.labels[0]}, and all the top ${String(len)}, putting together, contribute ${String(this.topAuthors.data.slice(0, len).reduce((a, b) => a + b))} submissions in total.`;
      this.authorText = {
        val: authorInitialText,
        edit: false,
      };
      this.topAuthorData = this.computeAuthorData(len);
    },
    countryDataLength(newValue, oldValue) {
      const len = newValue;
      const countryInitialText = `And from the country information (generated from the author data), we can see that the top 1 country, in this case ${this.topCountries.labels[0]}, has made ${String(((this.topCountries.data[0] - this.topCountries.data[1]) / this.topCountries.data[1] * 100).toFixed(2))}% more submission than the second-placed ${this.topCountries.labels[1]}.`;
      this.countryText = {
        val: countryInitialText,
        edit: false,
      };
      console.log('Inside the data length trigger!');
      this.topCountryData = this.computeCountryData(len);
    },
    affiliationDataLength(newValue, oldValue) {
      const len = newValue;
      const affiliationInitialText = 'You may add in any additional remarks here.';
      this.affiliationText = {
        val: affiliationInitialText,
        edit: false,
      };
      this.topAffiliationData = this.computeAffiliationData(len);
    },
    // visualization 4.1
    topAcceptedAffiliationDataLength(newValue, oldValue) {
      this.topAcceptedAffiliationData = this.computeTopAcceptedAffiliationData(newValue);
    },
  },
  created() {
    Store.registerPrintableChart(CHART_IDS.TOP_ACCEPTED_AFFILIATION_BAR_PIE_ID);
    Store.registerPrintableChart(CHART_IDS.TOP_AUTHOR_BAR_ID);
    Store.registerPrintableChart(CHART_IDS.TOP_COUNTRY_BAR_ID);
    Store.registerPrintableChart(CHART_IDS.TOP_SUBMITTED_AFFILIATION_BAR_PIE_ID);
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
    computeAuthorData(len) {
      // var len = this.authorDataLength;
      const scheme = this.chooseColorScheme(len);
      const topAuthorData = {
        labels: this.chartData.topAuthors.labels.slice(0, len),
        datasets: [
          {
            label: 'Submission Counts',
            backgroundColor: scheme,
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            data: this.chartData.topAuthors.data.slice(0, len),
          },
        ],
      };
      return topAuthorData;
    },
    computeCountryData(len) {
      // var len = this.countryDataLength;
      const scheme = this.chooseColorScheme(len);
      const topCountryData = {
        labels: this.chartData.topCountries.labels.slice(0, len),
        datasets: [
          {
            label: 'Submission Counts',
            backgroundColor: scheme,
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            data: this.chartData.topCountries.data.slice(0, len),
          },
        ],
      };
      return topCountryData;
    },
    computeAffiliationData(len) {
      // var len = this.affiliationDataLength;
      const scheme = this.chooseColorScheme(len);
      const topAffiliationData = {
        labels: this.chartData.topAffiliations.labels.slice(0, len),
        datasets: [
          {
            label: 'Submission Counts',
            backgroundColor: scheme,
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            data: this.chartData.topAffiliations.data.slice(0, len),
          },
        ],
      };
      return topAffiliationData;
    },
    // visualization 4.1
    computeTopAcceptedAffiliationData(len) {
      const scheme = this.chooseColorScheme(len);

      return {
        labels: dummyTopAcceptedAffiliationData.labels.slice(0, len),
        datasets: [
          {
            label: 'No. of Accepted Papers',
            backgroundColor: scheme,
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            data: dummyTopAcceptedAffiliationData.data.slice(0, len),
          },
        ],
      };
    },
  },
};
</script>

<style scoped>

</style>
