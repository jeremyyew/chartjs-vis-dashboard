<template>
  <div>
    <el-select v-model="authorDataLength" placeholder="Select Length" style="margin-top: 10px;margin-right: 40px">
      <p> AuthorViz Component </p>
      <el-option
        v-for="item in dataLengthOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <el-switch
      v-model="authorChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included">
    </el-switch>
    <!-- <P>
      {{authorChartIncluded}}
    </p> -->
    <bar-chart :data-input="topAuthorData" :title-text="'Top Authors'" class="chart" id="topauthorchart"
               ref="topauthorchart"></bar-chart>
    <!--using text.sync for two-way data binding to editable text child component-->
    <editable-text v-bind:text.sync="authorText"></editable-text>

    <el-select v-model="countryChartType" placeholder="Select Chart" style="margin-top: 20px;margin-right: 10px">
      <el-option
        v-for="item in chartOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <el-select v-model="countryDataLength" placeholder="Select Length" style="margin-top: 20px;margin-right: 30px">
      <el-option
        v-for="item in dataLengthOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <el-switch
      v-model="countryChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included">
    </el-switch>
    <div id="topcountrychart" ref="topcountrychart">
      <hori-bar-chart v-bind:data-input="topCountryData" :title-text="'Top Countries'" class="chart"
                      v-if="countryChartType=='bar'"></hori-bar-chart>
      <pie-chart v-bind:data-input="topCountryData" :title-text="'Top Countries'" class="chart"
                 v-else-if="countryChartType=='pie'"></pie-chart>
    </div>
    <editable-text v-bind:text.sync="countryText"></editable-text>

    <el-select v-model="affiliationChartType" placeholder="Select Chart" style="margin-top: 20px; margin-right: 10px">
      <el-option
        v-for="item in chartOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <el-select v-model="affiliationDataLength" placeholder="Select Length"
               style="margin-top: 20px;margin-right: 10px">
      <el-option
        v-for="item in dataLengthOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <el-switch
      v-model="affiliationChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included">
    </el-switch>
    <div id="topaffiliationchart" ref="topaffiliationchart">
      <hori-bar-chart :data-input="topAffiliationData" :title-text="'Top Affiliations'" class="chart"
                      v-if="affiliationChartType=='bar'"></hori-bar-chart>
      <pie-chart :data-input="topAffiliationData" :title-text="'Top Affiliations'" class="chart"
                 v-else-if="affiliationChartType=='pie'"></pie-chart>
    </div>
    <editable-text v-bind:text.sync="affiliationText"></editable-text>

    <el-button @click="saveAuthorNew" type="success" plain style="margin-top: 10px">Save</el-button>
  </div>
</template>

<script>
  import BarChart from '@/components/BarChart'
  import HoriBarChart from '@/components/HoriBarChart'
  import PieChart from '@/components/PieChart'

  import EditableText from '@/components/EditableText'

  import Const from './const'

  export default {
    name: "AuthorViz",
    props: ['chartData', 'inputFileName'],
    components: {
      BarChart,
      HoriBarChart,
      PieChart,
      EditableText,
    },
    data() {
      var authorInitialText = "So it's rather clear that the one with the largest number of submissions this year is: " + this.chartData.topAuthors.labels[0] + ", and all the top " + String(3) + ", putting together, contribute " + String(this.chartData.topAuthors.data.slice(0, 3).reduce(function (a, b) {
        return a + b;
      })) + " submissions in total.";

      var countryInitialText = "And from the country information (generated from the author data), we can see that the top 1 country, in this case " + this.chartData.topCountries.labels[0] + ", has made " + String(((this.chartData.topCountries.data[0] - this.chartData.topCountries.data[1]) / this.chartData.topCountries.data[1] * 100).toFixed(2)) + "% more submission than the second-placed " + this.chartData.topCountries.labels[1] + ".";

      return {
        msg: 'Author Info Analysis',
        authorText: {
          val: authorInitialText,
          edit: false
        },
        countryText: {
          val: countryInitialText,
          edit: false
        },
        affiliationText: {
          val: "You may add in any additional remarks here.",
          edit: false
        },
        topAuthors: this.chartData.topAuthors,
        topCountries: this.chartData.topCountries,
        topAffiliations: this.chartData.topAffiliations,
        chartOptions: [
          {
            value: 'pie',
            label: 'Pie Chart'
          }, {
            value: 'bar',
            label: 'Bar Chart'
          }
        ],
        countryChartType: 'pie',
        affiliationChartType: 'bar',
        dataLengthOptions: [
          {
            value: 3,
            label: '3'
          }, {
            value: 5,
            label: '5'
          }, {
            value: 10,
            label: '10'
          }
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
      }
    },
    methods: {
      computeAuthorData: function (len) {
        // var len = this.authorDataLength;
        var scheme = this.chooseColorScheme(len);
        var topAuthorData = {
          labels: this.chartData.topAuthors.labels.slice(0, len),
          datasets: [
            {
              label: 'Submission Counts',
              backgroundColor: scheme,
              pointBackgroundColor: 'white',
              borderWidth: 1,
              pointBorderColor: '#249EBF',
              data: this.chartData.topAuthors.data.slice(0, len),
            }
          ]
        }
        return topAuthorData;
      },
      computeCountryData: function (len) {
        // var len = this.countryDataLength;
        var scheme = this.chooseColorScheme(len);
        var topCountryData = {
          labels: this.chartData.topCountries.labels.slice(0, len),
          datasets: [
            {
              label: 'Submission Counts',
              backgroundColor: scheme,
              pointBackgroundColor: 'white',
              borderWidth: 1,
              pointBorderColor: '#249EBF',
              data: this.chartData.topCountries.data.slice(0, len),
            }
          ]
        }
        return topCountryData;
      },
      computeAffiliationData: function (len) {
        // var len = this.affiliationDataLength;
        var scheme = this.chooseColorScheme(len);
        var topAffiliationData = {
          labels: this.chartData.topAffiliations.labels.slice(0, len),
          datasets: [
            {
              label: 'Submission Counts',
              backgroundColor: scheme,
              pointBackgroundColor: 'white',
              borderWidth: 1,
              pointBorderColor: '#249EBF',
              data: this.chartData.topAffiliations.data.slice(0, len),
            }
          ]
        };
        return topAffiliationData;
      },
      chooseColorScheme: function (len) {
        switch (len) {
          case 3:
            return Const.colorScheme3;
          case 5:
            return Const.colorScheme5;
          default:
            return Const.colorScheme10;
        }
      },
      saveAuthorNew: function () {
        let fileName = 'Author Submission Visual Analysis';
        var leftMargin = Const.leftMargin;
        var rightMargin = Const.rightMargin;
        var contentWidth = Const.contentWidth;
        var initialTopMargin = Const.topMargin;
        var doc = new jsPDF('p', 'pt');
        var title = "Author Submission Visual Analysis";
        doc.setFont("Times");
        doc.setFontSize(Const.pdfTitleFontSize);
        var titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize;
        doc.text((contentWidth - titleLength) / 2.0 + leftMargin, initialTopMargin, title);
        var startingTopMargin = initialTopMargin + Const.pdfTitleFontSize;
        doc.setFontSize(Const.pdfTextFontSize);

        var numOfAddedSections = 0;

        html2canvas(document.getElementById('topauthorchart')).then(authorCanvas => {
          var topMarginAfterAuthor = startingTopMargin;
          if (this.authorChartIncluded) {
            numOfAddedSections += 1;
            var authorImageData = authorCanvas.toDataURL("image/png");
            var authorImageWidth = Const.imageWidth;
            var authorImageHeight = authorCanvas.height * authorImageWidth / authorCanvas.width;
            doc.addImage(authorImageData, 'PNG', leftMargin, startingTopMargin, authorImageWidth, authorImageHeight);

            var authorTextLines = doc.splitTextToSize(this.authorText.val, contentWidth);
            doc.text(leftMargin, startingTopMargin + authorImageHeight + 20, authorTextLines);

            // Note: here pdfLineHeight is the line height considering the white space between lines
            var authorTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * authorTextLines.length;
            topMarginAfterAuthor = startingTopMargin + authorImageHeight + authorTextLinesHeight + 30;
          }

          html2canvas(document.getElementById('topcountrychart')).then(countryCanvas => {
            var topMarginAfterCountry = topMarginAfterAuthor;
            if (this.countryChartIncluded) {
              numOfAddedSections += 1;
              var countryImageData = countryCanvas.toDataURL("image/png");
              var countryImageWidth = Const.imageWidth;
              var countryImageHeight = countryCanvas.height * countryImageWidth / countryCanvas.width;
              doc.addImage(countryImageData, 'PNG', leftMargin, topMarginAfterAuthor, countryImageWidth, countryImageHeight);

              var countryTextLines = doc.splitTextToSize(this.countryText.val, contentWidth);
              doc.text(leftMargin, topMarginAfterAuthor + countryImageHeight + 20, countryTextLines);

              if (numOfAddedSections % 2 === 1) {
                var countryTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * countryTextLines.length;
                topMarginAfterCountry = topMarginAfterAuthor + countryImageHeight + countryTextLinesHeight + 20;

              }
            }

            html2canvas(document.getElementById('topaffiliationchart')).then(affiliationCanvas => {
              if (this.affiliationChartIncluded) {
                if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                  doc.addPage();
                  topMarginAfterCountry = Const.topMargin;
                }
                var affiliationImageData = affiliationCanvas.toDataURL("image/png");
                var affiliationImageWidth = Const.imageWidth;
                var affiliationImageHeight = affiliationCanvas.height * affiliationImageWidth / affiliationCanvas.width;
                doc.addImage(affiliationImageData, 'PNG', leftMargin, topMarginAfterCountry, affiliationImageWidth, affiliationImageHeight);

                var affiliationTextLines = doc.splitTextToSize(this.affiliationText.val, contentWidth);
                doc.text(leftMargin, topMarginAfterCountry + affiliationImageHeight + 20, affiliationTextLines);
              }

              doc.save(fileName + '.pdf');
            });

          });

        });

      },
    },
    watch: {
      authorDataLength: function (newValue, oldValue) {
        var len = newValue;
        var authorInitialText = "So it's rather clear that the one with the largest number of submissions this year is: " + this.topAuthors.labels[0] + ", and all the top " + String(len) + ", putting together, contribute " + String(this.topAuthors.data.slice(0, len).reduce(function (a, b) {
          return a + b;
        })) + " submissions in total.";
        this.authorText = {
          val: authorInitialText,
          edit: false
        };
        this.topAuthorData = this.computeAuthorData(len);
      },
      countryDataLength: function (newValue, oldValue) {
        var len = newValue;
        var countryInitialText = "And from the country information (generated from the author data), we can see that the top 1 country, in this case " + this.topCountries.labels[0] + ", has made " + String(((this.topCountries.data[0] - this.topCountries.data[1]) / this.topCountries.data[1] * 100).toFixed(2)) + "% more submission than the second-placed " + this.topCountries.labels[1] + ".";
        this.countryText = {
          val: countryInitialText,
          edit: false
        };
        console.log("Inside the data length trigger!");
        this.topCountryData = this.computeCountryData(len);
      },
      affiliationDataLength: function (newValue, oldValue) {
        var len = newValue;
        var affiliationInitialText = "You may add in any additional remarks here.";
        this.affiliationText = {
          val: affiliationInitialText,
          edit: false
        };
        this.topAffiliationData = this.computeAffiliationData(len);
      }
    }
  }
</script>

<style scoped>

</style>
