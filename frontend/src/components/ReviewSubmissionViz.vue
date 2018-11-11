<template>
  <div>
    <el-select
      v-model="topReviewedAuthorDataLength"
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
    <bar-chart
      id="topreviewedauthorchart"
      ref="topreviewedauthorchart"
      :data-input="topReviewedAuthorData"
      :title-text="'Top Authors'"
      class="chart"
    />
    <!--using text.sync for two-way data binding to editable text child component-->
    <editable-text :text.sync="topReviewdAuthorText" />
  </div>
</template>

<script>
  import BarChart from '@/components/BarChart';
  import EditableText from '@/components/EditableText';

  import Const from './Const';
  import {
    dummyLabels,
    dummyData
  } from '../mocks/TopReviewedAuthorMock'

  export default {
    name: 'AuthorReviewViz',
    components: {
      BarChart,
      EditableText,
    },
    props: ['chartData', 'inputFileName'],
    data() {
      const topReviewedAuthorInitialText = 'Authors with the most number of reviews';

      return {
        msg: 'Author Info Analysis',
        topReviewdAuthorText: {
          val: topReviewedAuthorInitialText,
          edit: false,
        },
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
        topReviewedAuthorData: this.computeTopReviewedAuthorData(3),
        topReviewedAuthorDataLength: 3,
      };
    },
    watch: {
      topReviewedAuthorDataLength(newValue, oldValue) {
        this.topReviewedAuthorData = this.computeTopReviewedAuthorData(newValue);
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
      computeTopReviewedAuthorData(len) {
        const scheme = this.chooseColorScheme(len);
        const topReviewedAuthorData = {
          labels: dummyLabels.slice(0, len),
          datasets: [
            {
              label: 'Submission Counts',
              backgroundColor: scheme,
              pointBackgroundColor: 'white',
              borderWidth: 1,
              pointBorderColor: '#249EBF',
              data: dummyData.slice(0, len),
            },
          ],
        };
        return topReviewedAuthorData;
      },
    },
  };
</script>

<style scoped>

</style>

