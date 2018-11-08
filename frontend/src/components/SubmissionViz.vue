<template>
  <div>
    <el-switch
      v-model="storeState.charts[CHART_IDS.SUBMISSION_TIME_SERIES_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <time-line-chart
      :id="CHART_IDS.SUBMISSION_TIME_SERIES_ID"
      ref="timeserieschart"
      :data-input="timeSeriesData"
      :title-text="'Submission Time Series'"
      :annotation="JCDLAnnotation"
      class="chart"
    />
    <editable-text
      :text.sync="timeseriesText"
      style="margin-bottom: 20px;"
    />

    <el-switch
      v-model="storeState.charts[CHART_IDS.HISTORICAL_ACCEPTANCE_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <line-chart
      :id="CHART_IDS.HISTORICAL_ACCEPTANCE_ID"
      ref="historicalchart"
      :data-input="historicalAcceptanceRate"
      :title-text="'Past Years Acceptance Rates'"
      class="chart"
    />
    <editable-text :text.sync="historicalAcceptanceText" />

    <el-select
      v-model="acceptanceRateChartType"
      placeholder="Select Chart"
      style="margin-top: 20px; margin-right: 30px"
    >
      <el-option
        v-for="item in chartOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-switch
      v-model="storeState.charts[CHART_IDS.ACCEPTANCE_BY_TRACK_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      :id="CHART_IDS.ACCEPTANCE_BY_TRACK_ID"
      ref="acceptancechart"
    >
      <bar-chart-deci
        v-if="acceptanceRateChartType=='bar'"
        :data-input="acceptanceRateByTrackData"
        :title-text="'Acceptance Rate By Track'"
        class="chart"
      />
      <radar-chart
        v-else-if="acceptanceRateChartType=='radar'"
        :data-input="acceptanceRateByTrackData"
        :title-text="'Acceptance Rate By Track'"
        class="chart"
      />
    </div>
    <editable-text :text.sync="acceptanceRateByTrackText" />


    <el-select
      v-model="topAcceptedAuthorsDataLength"
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
      v-model="storeState.charts[CHART_IDS.TOP_ACCEPTED_AUTHORS_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <hori-bar-chart
      :id="CHART_IDS.TOP_ACCEPTED_AUTHORS_ID"
      ref="topacceptedauthorchart"
      :data-input="topAcceptedAuthorsData"
      :title-text="'Top Accepted Authors/Contributors'"
      class="chart"
    />
    <editable-text
      :text.sync="topAcceptedAuthorsText"
      style="margin-bottom: 20px;"
    />


    <el-select
      v-model="topAcceptedAuthorsByTrackLength"
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
    <el-select
      v-model="topAcceptedAuthorsSelectedTrack"
      placeholder="Select Length"
      style="margin-top: 10px;margin-right: 30px"
    >
      <el-option
        v-for="item in trackOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-switch
      v-model="storeState.charts[CHART_IDS.TOP_ACCEPTED_AUTHORS_BY_TRACK_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <hori-bar-chart
      :id="CHART_IDS.TOP_ACCEPTED_AUTHORS_BY_TRACK_ID"
      ref="topacceptedauthorbytrackchart"
      :data-input="topAcceptedAuthorsByTrackData"
      :title-text="'Top Accepted Authors'"
      class="chart"
    />
    <editable-text
      :text.sync="topAcceptedAuthorsByTrackText"
      style="margin-bottom: 20px;"
    />

    <!--Note: due to the constraint of the component, the style width and height must be specified-->
    <el-switch
      v-model="storeState.charts[CHART_IDS.SUBMISSIONS_WORD_CLOUD_ALL_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      :id="CHART_IDS.SUBMISSIONS_WORD_CLOUD_ALL_ID"
      ref="wordcloudall"
    >
      <h4>Word Cloud for All Submissions</h4>
      <vue-word-cloud
        :words="wordCloudTotal"
        :animation-duration="50"
        :color="([, weight]) => weight > 10 ? 'Red' : weight > 5 ? 'Blue' : 'Black'"
        font-family="Roboto"
        style="width: 70%;height: 200px"
      />
    </div>

    <el-switch
      v-model="storeState.charts[CHART_IDS.SUBMISSIONS_WORD_CLOUD_ACCEPTED_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      :id="CHART_IDS.SUBMISSIONS_WORD_CLOUD_ACCEPTED_ID"
      ref="wordcloudaccept"
    >
      <h4>Word Cloud for Accepted Papers</h4>
      <vue-word-cloud
        :words="acceptedWordCloud"
        :animation-duration="50"
        :color="([, weight]) => weight > 10 ? 'Red' : weight > 5 ? 'Blue' : 'Black'"
        font-family="Roboto"
        style="width: 70%;height: 200px"
      />
    </div>

    <el-switch
      v-model="storeState.charts[CHART_IDS.SUBMISSIONS_WORD_CLOUD_BY_TRACK_ID].included"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included"
    />
    <div
      :id="CHART_IDS.SUBMISSIONS_WORD_CLOUD_BY_TRACK_ID"
      ref="wordcloudtrack"
    >
      <h4>Word Cloud for Submissions by Track</h4>
      <el-select
        v-model="wordCloudSelectedTrack"
        placeholder="Select Length"
        style="margin-top: 10px;margin-right: 10px"
      >
        <el-option
          v-for="item in trackOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>


      <!--visualization 1.2-->
      <el-select
        v-model="wordCloudSelectedFilter"
        placeholder="Select a Filter"
        style="margin-top: 10px;margin-right: 10px"
      >
        <el-option
          v-for="item in filterOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <vue-word-cloud
        :words="wordCloudByTrack[wordCloudSelectedTrack]"
        :animation-duration="100"
        :color="([, weight]) => weight > 10 ? 'Red' : weight > 5 ? 'Blue' : 'Black'"
        font-family="Roboto"
        style="width: 70%;height: 200px"
      />
    </div>
    <el-button
      type="success"
      plain
      style="margin-top: 20px"
      @click="saveSubmission"
    >Save
    </el-button>
  </div>
</template>
<script>
import LineChart from '@/components/LineChart';
import TimeLineChart from '@/components/TimeLineChart';
import RadarChart from '@/components/RadarChart';
import BarChart from '@/components/BarChart';
import BarChartDeci from '@/components/BarChartDeci';
import HoriBarChart from '@/components/HoriBarChart';
import PieChart from '@/components/PieChart';

import EditableText from '@/components/EditableText';
import Utils from '@/utils';
import Const from './Const';
import Store from '@/store';
import VueWordCloud from 'vuewordcloud';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const { CHART_IDS } = Const;

export default {
  name: 'SubmissionViz',
  components: {
    LineChart,
    TimeLineChart,
    RadarChart,
    BarChart,
    BarChartDeci,
    HoriBarChart,
    PieChart,
    EditableText,
    [VueWordCloud.name]: VueWordCloud,
  },
  props: ['chartData', 'inputFileName'],
  data() {
    const tracks = this.computeAcceptanceRateByTrack().labels;
    const acceptanceRate = this.computeAcceptanceRateByTrack().datasets[0].data;

    const topIndex = this.indexOfMax(acceptanceRate);
    const topTrack = tracks[topIndex];
    const topValue = acceptanceRate[topIndex] * 100;

    return {
      storeState: Store.state,
      CHART_IDS,
      msg: 'Submission Info Analysis',
      acceptanceRate: this.chartData.acceptanceRate.toFixed(2),
      acceptanceRateSelectedTrack: 'Full Papers',
      topAcceptedAuthorsSelectedTrack: 'Full Papers',
      wordCloudSelectedTrack: 'Full Papers',
      trackOptions: this.getTrackInSubmission().map(track => ({ value: track, label: track })),
      chartOptions: [
        {
          value: 'bar',
          label: 'Bar Chart',
        }, {
          value: 'radar',
          label: 'Radar Chart',
        },
      ],
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
      acceptanceRateChartType: 'bar',
      wordCloudTotal: this.chartData.overallKeywordList,
      acceptedWordCloud: this.chartData.acceptedKeywordList,
      acceptanceRateByTrackData: this.computeAcceptanceRateByTrack(),
      topAcceptedAuthorsData: this.computeTopAcceptedAuthors(3),
      topAcceptedAuthorsDataLength: 3,
      topAcceptedAuthorsByTrackData: this.computeTopAcceptedAuthorsByTrack(3, 'Full Papers'),
      topAcceptedAuthorsByTrackLength: 3,
      topAcceptedAuthorsByTrackChartIncluded: true,
      historicalAcceptanceRate: this.computeHistoricalAcceptanceRate(),
      timeSeriesData: this.computeTimeSeriesData(),
      JCDLAnnotation: this.computeJCDLDeadlineData(),
      timeSeriesChartIncluded: true,
      timeseriesText: {
        val: "It can be identified clearly from the chart that most researchers won't submit their work until the last moment :-). Additionally, although some people made changes to their work after the first submission, the vast majority of people create the entry and make it the final version, since the red curve and blue curve overlaps in most of the time.",
        // val: "This is a sample text.",
        edit: false,
      },
      historicalAcceptanceText: {
        val: "The historical data on the acceptance rate of JCDL can be found here, appending this year's data in the end. You might notice that for full papers, the rate has seen a major increase from earlier works, while there have been some fluctuations for short papers.",
        edit: false,
      },
      acceptanceRateByTrackText: {
        val: `Then for this year's work, we can divide them into different tracks to examine the details: the track ${String(topTrack)} has the largest acceptance rate, at around ${String(topValue.toFixed(2))}%. Noticeably, Doctoral Consortium and Tutorials didn't take in any entries this year.`,
        edit: false,
      },
      topAcceptedAuthorsText: {
        val: `As for the authors, congratulations to Prof. ${String(this.chartData.topAcceptedAuthors.names[0])} for getting ${String(this.chartData.topAcceptedAuthors.counts[0])} papers/projects accepted to JCDL 2018.`,
        edit: false,
      },
      topAcceptedAuthorsByTrackText: {
        val: 'You may want to dig into different tracks of submissions, and here you can check out the researchers who contribute the most to the selected track.',
        edit: false,
      },
      historicalAcceptanceChartIncluded: true,
      acceptanceRateByTrackChartIncluded: true,
      topAcceptedAuthorsChartIncluded: true,
      wordCloudAllIncluded: true,
      wordCloudAcceptedIncluded: true,
      wordCloudByTrackIncluded: true,

      // visualization 1.2
      wordCloudSelectedFilter: 'Select a Filter',
      filterOptions: [
        {
          value: 'All',
          label: 'All Submissions',
        },
        {
          value: 'Accepted',
          label: 'Accepted Submissions',
        },
        {
          value: 'Rejected',
          label: 'Rejected Submissions',
        },
      ],
      wordCloudByTrack: this.computeFilteredWordCloudByTrack(),
    };
  },
  watch: {
    topAcceptedAuthorsDataLength(newValue, oldValue) {
      const len = newValue;
      this.topAcceptedAuthorsData = this.computeTopAcceptedAuthors(len);
    },
    topAcceptedAuthorsSelectedTrack(newValue, oldValue) {
      this.topAcceptedAuthorsByTrackData = this.computeTopAcceptedAuthorsByTrack(this.topAcceptedAuthorsByTrackLength, newValue);
    },
    topAcceptedAuthorsByTrackLength(newValue, oldValue) {
      const len = newValue;
      this.topAcceptedAuthorsByTrackData = this.computeTopAcceptedAuthorsByTrack(len, this.topAcceptedAuthorsSelectedTrack);
    },
    // visualization 1.2
    wordCloudSelectedFilter(newValue, oldValue) {
      this.wordCloudByTrack = this.computeFilteredWordCloudByTrack(newValue);
    },
  },
  created() {
    Store.registerPrintableChart(CHART_IDS.SUBMISSION_TIME_SERIES_ID);
    Store.registerPrintableChart(CHART_IDS.HISTORICAL_ACCEPTANCE_ID);
    Store.registerPrintableChart(CHART_IDS.ACCEPTANCE_BY_TRACK_ID);
    Store.registerPrintableChart(CHART_IDS.TOP_ACCEPTED_AUTHORS_ID);
    Store.registerPrintableChart(CHART_IDS.TOP_ACCEPTED_AUTHORS_BY_TRACK_ID);
    Store.registerPrintableChart(CHART_IDS.SUBMISSIONS_WORD_CLOUD_ALL_ID);
    Store.registerPrintableChart(CHART_IDS.SUBMISSIONS_WORD_CLOUD_ACCEPTED_ID);
    Store.registerPrintableChart(CHART_IDS.SUBMISSIONS_WORD_CLOUD_BY_TRACK_ID);
  },
  methods: {
    computeFilteredWordCloudByTrack(filter) {
      const { acceptedKeywordList } = this.chartData;
      const acceptedList = acceptedKeywordList.map(keyword => keyword[0]);

      const { rejectedKeywordMap } = this.chartData;
      const rejectedList = Object.keys(rejectedKeywordMap);

      const { keywordsByTrack } = this.chartData;

      let filteredTrack = {};

      if (filter === 'Accepted') {
        Object.keys(keywordsByTrack).forEach((key) => {
          // console.log(`**************key: ${key}`);
          filteredTrack[key] = keywordsByTrack[key].filter((value, index, array) => {
            console.log(value);
            return acceptedList.indexOf(value[0]) > -1;
          });
          // console.log(JSON.stringify(filteredTrack[key], undefined, 4));
        });
      } else if (filter === 'Rejected') {
        Object.keys(keywordsByTrack).forEach((key) => {
          // console.log(`**************key: ${key}`);
          filteredTrack[key] = keywordsByTrack[key].filter((value, index, array) => {
            console.log(value);
            return rejectedList.indexOf(value[0]) > -1;
          });
          // console.log(JSON.stringify(filteredTrack[key], undefined, 4));
        });
      } else {
        filteredTrack = keywordsByTrack;
      }

      // return this.chartData.keywordsByTrack;

      return filteredTrack;
    },
    chooseColorScheme(len) {
      return Utils.chooseColorScheme(len);
    },
    getTrackInSubmission() {
      return Object.keys(this.chartData.acceptanceRateByTrack);
    },
    computeTimeSeriesData() {
      const time = this.chartData.timeSeries.time;
      return {
        datasets: [
          {
            label: 'Submit Time',
            data: this.chartData.timeSeries,
            backgroundColor: 'white',
            fill: false,
            // pointBorderColor: '#249EBF',
            radius: 0,
            borderColor: 'blue',
          },
          {
            label: 'Last Edit Time',
            data: this.chartData.lastEditSeries,
            backgroundColor: 'white',
            fill: false,
            // pointBorderColor: '#249EBF',
            radius: 0,
            borderColor: 'red',
          },
        ],
      };
    },
    computeTopAcceptedAuthorsByTrack(len, track) {
      const authors = this.chartData.topAuthorsByTrack[track].names.slice(0, len);
      const values = this.chartData.topAuthorsByTrack[track].counts.slice(0, len);
      console.log(authors);
      console.log(values);
      const scheme = this.chooseColorScheme(len);
      return {
        labels: authors,
        datasets: [
          {
            label: 'Paper Counts',
            backgroundColor: scheme,
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            data: values,
          },
        ],
      };
    },
    computeHistoricalAcceptanceRate() {
      const years = this.chartData.comparableAcceptanceRate.year;
      console.log('got to the acceptance rate function');
      return {
        labels: years,
        datasets: [
          {
            label: 'Full Papers',
            // backgroundColor: this.chooseColorScheme(10),
            borderColor: 'blue',
            fill: false,
            pointBackgroundColor: 'white',
            borderWidth: 2,
            pointBorderColor: 'blue',
            pointHoverRadius: 5,
            data: this.chartData.comparableAcceptanceRate['Full Papers'],
          },
          {
            label: 'Short Papers',
            // backgroundColor: this.chooseColorScheme(10),
            borderColor: 'red',
            fill: false,
            pointBackgroundColor: 'white',
            borderWidth: 2,
            pointBorderColor: 'red',
            pointHoverRadius: 5,
            data: this.chartData.comparableAcceptanceRate['Short Papers'],
          },
        ],
      };
    },
    computeTopAcceptedAuthors(len) {
      const authors = this.chartData.topAcceptedAuthors.names.slice(0, len);
      // var authors = Object.keys(this.chartData.topAcceptedAuthors);
      const values = this.chartData.topAcceptedAuthors.counts.slice(0, len);
      const scheme = this.chooseColorScheme(len);
      // var values = authors.map(function(author) {return this.chartData.topAcceptedAuthors[author];});
      return {
        labels: authors,
        datasets: [
          {
            label: 'Accepted Papers',
            backgroundColor: scheme,
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            data: values,
          },
        ],
      };
    },
    computeAcceptanceRateByTrack() {
      const tracks = this.getTrackInSubmission();
      const values = [];
      for (const track in tracks) {
        values.push(this.chartData.acceptanceRateByTrack[tracks[track]].toFixed(2));
      }
      return {
        labels: tracks,
        datasets: [
          {
            label: 'Acceptance Rate',
            backgroundColor: this.chooseColorScheme(10),
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            data: values,
          },
        ],
      };
    },
    indexOfMax(arr) {
      return Utils.indexOfMax(arr);
    },
    computeJCDLDeadlineData() {
      return {
        annotations: [
          {
            type: 'line',
            mode: 'vertical',
            scaleID: 'x-axis-0',
            value: '2018-01-18',
            borderDash: [4, 4],
            borderColor: 'red',
            label: {
              content: 'Papers, Tutorial, and Wordshop Deadline',
              enabled: true,
              position: 'top',
              xAdjust: 55,
              yAdjust: 8,
            },
          },
          {
            type: 'line',
            mode: 'vertical',
            scaleID: 'x-axis-0',
            value: '2018-02-02',
            borderDash: [4, 4],
            borderColor: 'red',
            label: {
              content: 'Panel, Poster, and Demo Deadline',
              enabled: true,
              position: 'top',
              xAdjust: -35,
              yAdjust: 45,
            },
          },
        ],
      };
    },
    saveSubmission() {
      const fileName = 'Submission Visual Analysis';
      const leftMargin = Const.leftMargin;
      const rightMargin = Const.rightMargin;
      const initialTopMargin = Const.topMargin;
      const contentWidth = Const.contentWidth;
      const doc = new jsPDF('p', 'pt');
      const title = 'Submission Visual Analysis';
      doc.setFont('Times');
      doc.setFontSize(Const.pdfTitleFontSize);
      const titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize;
      doc.text((contentWidth - titleLength) / 2.0 + leftMargin, initialTopMargin, title);
      const startingTopMargin = initialTopMargin + Const.pdfTitleFontSize;
      doc.setFontSize(Const.pdfTextFontSize);

      let numOfAddedSections = 0;

      html2canvas(document.getElementById('timeserieschart')).then((timeCanvas) => {
        let topMarginAfterTime = startingTopMargin;
        if (this.timeSeriesChartIncluded) {
          numOfAddedSections += 1;

          const timeImageData = timeCanvas.toDataURL('image/png');
          const timeImageWidth = Const.imageWidth;
          const timeImageHeight = timeCanvas.height * timeImageWidth / timeCanvas.width;
          doc.addImage(timeImageData, 'PNG', leftMargin, startingTopMargin, timeImageWidth, timeImageHeight);

          const timeTextLines = doc.splitTextToSize(this.timeseriesText.val, contentWidth);
          doc.text(leftMargin, startingTopMargin + timeImageHeight + 20, timeTextLines);

          // Note: here pdfLineHeight is the line height considering the white space between lines
          const timeTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * timeTextLines.length;
          topMarginAfterTime = startingTopMargin + timeImageHeight + timeTextLinesHeight + 20;
        }


        html2canvas(document.getElementById('historicalchart')).then((historicalCanvas) => {
          let topMarginAfterHistorical = topMarginAfterTime;
          if (this.historicalAcceptanceChartIncluded) {
            numOfAddedSections += 1;

            const historicalImageData = historicalCanvas.toDataURL('image/png');
            const historicalImageWidth = Const.imageWidth;
            const historicalImageHeight = historicalCanvas.height * historicalImageWidth / historicalCanvas.width;
            doc.addImage(historicalImageData, 'PNG', leftMargin, topMarginAfterTime, historicalImageWidth, historicalImageHeight);

            const historicalTextLines = doc.splitTextToSize(this.historicalAcceptanceText.val, contentWidth);
            doc.text(leftMargin, topMarginAfterTime + historicalImageHeight + 20, historicalTextLines);

            if (numOfAddedSections % 2 == 1) {
              const historicalTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * historicalTextLines.length;
              topMarginAfterHistorical = topMarginAfterTime + historicalImageHeight + historicalTextLinesHeight + 20;
            }
          }

          html2canvas(document.getElementById('acceptancechart')).then((acceptanceCanvas) => {
            let topMarginAfterAccept = topMarginAfterHistorical;
            if (this.acceptanceRateByTrackChartIncluded) {
              if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                doc.addPage();
                topMarginAfterHistorical = Const.topMargin;
              }

              numOfAddedSections += 1;
              const acceptImageData = acceptanceCanvas.toDataURL('image/png');
              const acceptImageWidth = Const.imageWidth;
              const acceptImageHeight = acceptanceCanvas.height * acceptImageWidth / acceptanceCanvas.width;
              doc.addImage(acceptImageData, 'PNG', leftMargin, topMarginAfterHistorical, acceptImageWidth, acceptImageHeight);

              const acceptTextLines = doc.splitTextToSize(this.acceptanceRateByTrackText.val, contentWidth);
              doc.text(leftMargin, topMarginAfterHistorical + acceptImageHeight + 20, acceptTextLines);

              if (numOfAddedSections % 2 == 1) {
                const acceptanceLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * acceptTextLines.length;
                topMarginAfterAccept = topMarginAfterHistorical + acceptImageHeight + acceptanceLinesHeight + 20;
              }
            }

            html2canvas(document.getElementById('topacceptedauthorchart')).then((accAuthorCanvas) => {
              let topMarginAfterTopAccAuthors = topMarginAfterAccept;
              if (this.topAcceptedAuthorsChartIncluded) {
                if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                  doc.addPage();
                  topMarginAfterAccept = Const.topMargin;
                }

                numOfAddedSections += 1;
                const accAuthorImageData = accAuthorCanvas.toDataURL('image/png');
                const accAuthorImageWidth = Const.imageWidth;
                const accAuthorImageHeight = accAuthorCanvas.height * accAuthorImageWidth / accAuthorCanvas.width;
                doc.addImage(accAuthorImageData, 'PNG', leftMargin, topMarginAfterAccept, accAuthorImageWidth, accAuthorImageHeight);

                const topAccAuthorsTextLines = doc.splitTextToSize(this.topAcceptedAuthorsText.val, contentWidth);
                doc.text(leftMargin, topMarginAfterAccept + accAuthorImageHeight + 20, topAccAuthorsTextLines);

                if (numOfAddedSections % 2 == 1) {
                  const topAccAuthorsTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * topAccAuthorsTextLines.length;
                  topMarginAfterTopAccAuthors = topMarginAfterAccept + accAuthorImageHeight + topAccAuthorsTextLinesHeight + 20;
                }
              }

              html2canvas(document.getElementById('topacceptedauthorbytrackchart')).then((accAuthorTrackCanvas) => {
                let topMarginAfterTopAccAuthorsTrack = topMarginAfterTopAccAuthors;
                if (this.topAcceptedAuthorsByTrackChartIncluded) {
                  if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                    doc.addPage();
                    topMarginAfterTopAccAuthors = Const.topMargin;
                  }

                  numOfAddedSections += 1;

                  const accAuthorTrackImageData = accAuthorTrackCanvas.toDataURL('image/png');
                  const accAuthorTrackImageWidth = Const.imageWidth;
                  const accAuthorTrackImageHeight = accAuthorTrackCanvas.height * accAuthorTrackImageWidth / accAuthorTrackCanvas.width;
                  doc.addImage(accAuthorTrackImageData, 'PNG', leftMargin, topMarginAfterTopAccAuthors, accAuthorTrackImageWidth, accAuthorTrackImageHeight);

                  const topAccAuthorsTrackTextLines = doc.splitTextToSize(this.topAcceptedAuthorsByTrackText.val, contentWidth);
                  doc.text(leftMargin, topMarginAfterTopAccAuthors + accAuthorTrackImageHeight + 20, topAccAuthorsTrackTextLines);

                  if (numOfAddedSections % 2 == 1) {
                    const topAccAuthorsTrackLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * topAccAuthorsTrackTextLines.length;
                    topMarginAfterTopAccAuthorsTrack = topMarginAfterTopAccAuthors + accAuthorTrackImageHeight + topAccAuthorsTrackLinesHeight + 20;
                  }
                }

                html2canvas(document.getElementById('wordcloudall')).then((wordAllCanvas) => {
                  if (this.wordCloudAllIncluded) {
                    if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                      doc.addPage();
                      topMarginAfterTopAccAuthorsTrack = Const.topMargin;
                    }

                    const wordAllImageData = wordAllCanvas.toDataURL('image/png');
                    const wordAllImageWidth = Const.imageWidth;
                    const wordAllImageHeight = wordAllCanvas.height * wordAllImageWidth / wordAllCanvas.width;
                    doc.addImage(wordAllImageData, 'PNG', leftMargin, topMarginAfterTopAccAuthorsTrack, wordAllImageWidth, wordAllImageHeight);
                  }

                  doc.save(`${fileName}.pdf`);
                });
              });
            });
          });
        });
      });
    },
  },
};
</script>

<style scoped>

</style>
