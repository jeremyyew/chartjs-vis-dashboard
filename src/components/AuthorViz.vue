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
        :title-text="'Top Affiliations'"
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
      v-model="authorChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <bar-chart
      id="topauthorchart"
      ref="topauthorchart"
      :data-input="topAuthorData"
      :title-text="'Top Authors'"
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
      v-model="countryChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      id="topcountrychart"
      ref="topcountrychart"
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
      v-model="affiliationChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      id="topaffiliationchart"
      ref="topaffiliationchart"
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
      @click="saveAuthorNew"
    >Save
    </el-button>
  </div>
</template>

<script>
import BarChart from '@/components/BarChart';
import HoriBarChart from '@/components/HoriBarChart';
import PieChart from '@/components/PieChart';

import EditableText from '@/components/EditableText';

import Const from './Const';

import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// visualization 4.1
import {
  dummyTopAcceptedAffiliationData,
} from '../mocks/TopAcceptedAffiliationMock';

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
      authorChartIncluded: true,
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
    saveAuthorNew() {
      const fileName = 'Author Submission Visual Analysis';
      const leftMargin = Const.leftMargin;
      const rightMargin = Const.rightMargin;
      const contentWidth = Const.contentWidth;
      const initialTopMargin = Const.topMargin;
      const doc = new jsPDF('p', 'pt');
      const title = 'Author Submission Visual Analysis';
      doc.setFont('Times');
      doc.setFontSize(Const.pdfTitleFontSize);
      const titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize;
      doc.text((contentWidth - titleLength) / 2.0 + leftMargin, initialTopMargin, title);
      const startingTopMargin = initialTopMargin + Const.pdfTitleFontSize;
      doc.setFontSize(Const.pdfTextFontSize);

      let numOfAddedSections = 0;

      html2canvas(document.getElementById('topauthorchart')).then((authorCanvas) => {
        let topMarginAfterAuthor = startingTopMargin;
        if (this.authorChartIncluded) {
          numOfAddedSections += 1;
          const authorImageData = authorCanvas.toDataURL('image/png');
          const authorImageWidth = Const.imageWidth;
          const authorImageHeight = authorCanvas.height * authorImageWidth / authorCanvas.width;
          doc.addImage(authorImageData, 'PNG', leftMargin, startingTopMargin, authorImageWidth, authorImageHeight);

          const authorTextLines = doc.splitTextToSize(this.authorText.val, contentWidth);
          doc.text(leftMargin, startingTopMargin + authorImageHeight + 20, authorTextLines);

          // Note: here pdfLineHeight is the line height considering the white space between lines
          const authorTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * authorTextLines.length;
          topMarginAfterAuthor = startingTopMargin + authorImageHeight + authorTextLinesHeight + 30;
        }

        html2canvas(document.getElementById('topcountrychart')).then((countryCanvas) => {
          let topMarginAfterCountry = topMarginAfterAuthor;
          if (this.countryChartIncluded) {
            numOfAddedSections += 1;
            const countryImageData = countryCanvas.toDataURL('image/png');
            const countryImageWidth = Const.imageWidth;
            const countryImageHeight = countryCanvas.height * countryImageWidth / countryCanvas.width;
            doc.addImage(countryImageData, 'PNG', leftMargin, topMarginAfterAuthor, countryImageWidth, countryImageHeight);

            const countryTextLines = doc.splitTextToSize(this.countryText.val, contentWidth);
            doc.text(leftMargin, topMarginAfterAuthor + countryImageHeight + 20, countryTextLines);

            if (numOfAddedSections % 2 === 1) {
              const countryTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * countryTextLines.length;
              topMarginAfterCountry = topMarginAfterAuthor + countryImageHeight + countryTextLinesHeight + 20;
            }
          }

          html2canvas(document.getElementById('topaffiliationchart')).then((affiliationCanvas) => {
            if (this.affiliationChartIncluded) {
              if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                doc.addPage();
                topMarginAfterCountry = Const.topMargin;
              }
              const affiliationImageData = affiliationCanvas.toDataURL('image/png');
              const affiliationImageWidth = Const.imageWidth;
              const affiliationImageHeight = affiliationCanvas.height * affiliationImageWidth / affiliationCanvas.width;
              doc.addImage(affiliationImageData, 'PNG', leftMargin, topMarginAfterCountry, affiliationImageWidth, affiliationImageHeight);

              const affiliationTextLines = doc.splitTextToSize(this.affiliationText.val, contentWidth);
              doc.text(leftMargin, topMarginAfterCountry + affiliationImageHeight + 20, affiliationTextLines);
            }

            doc.save(`${fileName}.pdf`);
          });
        });
      });
    },
  },
};
</script>

<style scoped>

</style>
