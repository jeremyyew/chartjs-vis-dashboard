<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div v-if="infoType === 'author'"> <!--Start of Author Component-->
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
      >Save</el-button>

    </div> <!--End of Author Component-->


    <div v-else-if="infoType === 'submission'"> <!--Start of Submission Component-->
      <el-switch
        v-model="timeSeriesChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <time-line-chart
        id="timeserieschart"
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
        v-model="historicalAcceptanceChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <line-chart
        id="historicalchart"
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
        v-model="acceptanceRateByTrackChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <div
        id="acceptancechart"
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
        v-model="topAcceptedAuthorsChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <hori-bar-chart
        id="topacceptedauthorchart"
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
        v-model="topAcceptedAuthorsByTrackChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <hori-bar-chart
        id="topacceptedauthorbytrackchart"
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
        v-model="wordCloudAllIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <div
        id="wordcloudall"
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
        v-model="wordCloudAcceptedIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <div
        id="wordcloudaccept"
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
        v-model="wordCloudByTrackIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <div
        id="wordcloudtrack"
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
      >Save</el-button>

    </div> <!--End of Submission Component-->


    <div v-else-if="infoType === 'review'"> <!--Start of Review Component-->
      <!-- visualization 2.1-->
      <el-switch
        v-model="scoreRecommendationChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <bar-chart
        id="scorerecommendationchart"
        ref="scorechart"
        :data-input="scoreRecommendationData"
        :title-text="'Score vs Recommendation'"
        class="chart"
      />


      <el-switch
        v-model="scoreDistributionChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <bar-chart
        id="scorechart"
        ref="scorechart"
        :data-input="scoreDistributionData"
        :title-text="'Score Distribution'"
        class="chart"
      />
      <editable-text
        :text.sync="scoreDistributionText"
        style="margin-bottom: 20px;"
      />

      <el-switch
        v-model="recommendDistributionChartIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <bar-chart
        id="recommendchart"
        ref="recommendchart"
        :data-input="recommendDistributionData"
        :title-text="'Recommendation Distribution'"
        class="chart"
      />
      <editable-text
        :text.sync="recommendDistributionText"
        style="margin-bottom: 20px;"
      />

      <el-switch
        v-model="reviewTableIncluded"
        active-color="#13ce66"
        active-text="Included in Report"
        inactive-text="Not Included"
      />
      <p>
        The mean scores and mean confidence values can be found as follows:
      </p><div
        id="reviewtable"
        ref="reviewtable"
      >
        <el-table
          :data="reviewTableData"
          stripe
          style="width: 70%;margin-top:10px;margin-bottom: 10px"
        >
          <el-table-column
            prop="field"
            label="Field"
            width="180"
          />
          <el-table-column
            prop="value"
            label="Value"
            width="180"
          />
        </el-table>
      </div>
      <editable-text :text.sync="reviewTableText" />
      <el-button
        type="success"
        plain
        style="margin-top: 10px"
        @click="saveReview"
      >Save</el-button>
    </div> <!--End of Review Component-->


    <div v-else-if="infoType === 'dummy'"> <!--Start of Dummy Component-->
      <line-chart
        v-if="type == 'line'"
        :data-input="data"
      />
      <bar-chart
        v-else-if="type == 'bar'"
        :data-input="data"
      />
    </div> <!--End of Dummy Component-->


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

import Const from './const';

import VueWordCloud from 'vuewordcloud';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// visualization 2.1
import {
  dummyLabels,
  dummyData,
} from '../mocks/ScoreRecommendationMock';

// visualization 4.1
import {
  dummyTopAcceptedAffiliationData,
} from '../mocks/TopAcceptedAffiliationMock';

const { VIZ_TYPES } = Const;

export default {
  name: 'Chart',
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
  props: ['chartData', 'infoType', 'inputFileName'],
  data() {
    if (this.infoType === VIZ_TYPES.AUTHOR) { // author.csv input
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
    }
    if (this.infoType == 'reviewScore') {
      return {
        msg: 'Statistics',
        yesPercentage: this.chartData.yesPercentage.toFixed(2),
        meanScore: this.chartData.meanScore,
        meanConfidence: this.chartData.meanConfidence,
        totalReview: this.chartData.totalReview,
        tableData: [
          {
            field: 'Mean Score',
            value: this.chartData.meanScore.toFixed(2),
          }, {
            field: 'Mean Confidence',
            value: this.chartData.meanConfidence.toFixed(2),
          },
        ],
        options: [
          {
            value: 'line',
            label: 'Line Chart',
          }, {
            value: 'bar',
            label: 'Bar Chart',
          },
        ],
        type: 'bar',
      };
    } if (this.infoType === VIZ_TYPES.SUBMISSION) {
      // console.log("inside submission subsection");
      const tracks = this.computeAcceptanceRateByTrack().labels;
      const acceptanceRate = this.computeAcceptanceRateByTrack().datasets[0].data;

      var topIndex = this.indexOfMax(acceptanceRate);
      const topTrack = tracks[topIndex];
      const topValue = acceptanceRate[topIndex] * 100;

      return {
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
    } if (this.infoType === VIZ_TYPES.REVIEW) {
      const scoreRanges = this.computeScoreDistributionData('score').labels;
      const scoreCounts = this.computeScoreDistributionData('score').datasets[0].data;

      var topIndex = this.indexOfMax(scoreCounts);
      const topRange = scoreRanges[topIndex];

      const recommendCounts = this.computeScoreDistributionData('recommend').datasets[0].data;
      const firstEntryPercentage = recommendCounts[0] / recommendCounts.reduce((a, b) => a + b) * 100;

      return {
        msg: 'Review Info Analysis',
        scoreRecommendationData: this.computeScoreRecommendationData(),
        scoreDistributionData: this.computeScoreDistributionData('score'),
        recommendDistributionData: this.computeScoreDistributionData('recommend'),
        reviewTableData: [
          {
            field: 'Mean Score',
            value: this.chartData.meanScore.toFixed(2),
          }, {
            field: 'Mean Recommendation',
            value: this.chartData.meanRecommend.toFixed(2),
          }, {
            field: 'Mean Confidence',
            value: this.chartData.meanConfidence.toFixed(2),
          },
        ],
        scoreRecommendationChartIncluded: true,
        scoreDistributionChartIncluded: true,
        recommendDistributionChartIncluded: true,
        reviewTableIncluded: true,
        scoreDistributionText: {
          val: `Note that when considering the review scores, we are combining multiple entries at the same time: here for the overall score of each paper, we take all reviews for a particular paper, retrieve its overall score and the reviewer's confidence, then calculate the weighted average of the scores w.r.t. the confidence value, and then here it is. It's rather clear that the score range with the largest count is ${String(topRange)} (a relatively low score though, :-)).`,
          edit: false,
        },
        recommendDistributionText: {
          val: `The same logic applies to the recommendation scores. Note that we use 0 to represent 'not recommended for best paper', and 1 as 'recommended for best paper', and then do a weighted average using the confidence value. It's hence also clear that the 0's takes up ${String(firstEntryPercentage.toFixed(2))}%.`,
          edit: false,
        },
        reviewTableText: {
          val: 'The mean score and recommendation values can be found here, and you are free to add in any additional comments and remarks here.',
          edit: false,
        },
      };
    } // dummy data input
    const yearInfo = this.chartData.year;
    const inCitations = this.chartData.inCitations;
    const outCitations = this.chartData.outCitations;

    const dataInput = {
      labels: yearInfo,
      datasets: [
        {
          label: 'inCitations',
          backgroundColor: 'rgba(47, 152, 208, 0.2)',
          pointBackgroundColor: 'white',
          borderWidth: 1,
          pointBorderColor: '#249EBF',
          data: inCitations,
        },
        {
          label: 'outCitations',
          backgroundColor: 'rgba(133, 23, 20, 0.2)',
          pointBackgroundColor: 'white',
          borderWidth: 1,
          pointBorderColor: '#783FCC',
          data: outCitations,
        },
      ],
    };

    return {
      msg: 'Chart View Component',
      data: dataInput,
      options: [
        {
          value: 'line',
          label: 'Line Chart',
        }, {
          value: 'bar',
          label: 'Bar Chart',
        },
      ],
      type: 'bar',
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

    // visualization 4.1
    topAcceptedAffiliationDataLength(newValue, oldValue) {
      this.topAcceptedAffiliationData = this.computeTopAcceptedAffiliationData(newValue);
    },
    // visualization 1.2
    wordCloudSelectedFilter(newValue, oldValue) {
      this.wordCloudByTrack = this.computeFilteredWordCloudByTrack(newValue);
    },
  },
  methods: {
    saveAuthor() {
      // Still have this function as a reference for what has been done using the mm settings instead of pt
      const fileName = 'Author Submission Visual Analysis';
      const leftMargin = Const.pdfLeftMargin;
      const rightMargin = Const.pdfRightMargin;
      const pdfInMM = Const.pdfInMM;
      const initialTopMargin = Const.pdfTopMargin;
      const doc = new jsPDF('p', 'mm', 'a4');
      const title = 'Author Submission Visual Analysis';
      doc.setFont('Times');
      doc.setFontSize(Const.pdfTitleFontSize);
      const titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize * Const.pdfMMPerPT;
      doc.text((pdfInMM - leftMargin - rightMargin - titleLength) / 2.0 + leftMargin, initialTopMargin, title);
      const startingTopMargin = initialTopMargin + Const.pdfTitleFontSize * Const.pdfMMPerPT;
      doc.setFontSize(Const.pdfTextFontSize);

      // Attn: For the current impl, the logic is as follows:
      // 1. each page of the PDF file will contain 2 images, together with their texts
      // 2. hence, we use this numOfAddedSections to keep track of how many we have added to PDF
      // 3. so if numOfAddedSections % 2 == 1, then no need to addPage(); else if num > 0, then addPage() and reset topMargin
      let numOfAddedSections = 0;

      html2canvas(document.getElementById('topauthorchart')).then((authorCanvas) => {
        let topMarginAfterAuthor = startingTopMargin;
        if (this.authorChartIncluded) {
          numOfAddedSections += 1;
          const authorImageData = authorCanvas.toDataURL('image/png');
          doc.addImage(authorImageData, 'PNG', 15, startingTopMargin, authorCanvas.width / 8, authorCanvas.height / 8);

          const authorTextLines = doc.splitTextToSize(this.authorText.val, (pdfInMM - leftMargin - rightMargin));
          doc.text(leftMargin, startingTopMargin + authorCanvas.height / 8 + 10, authorTextLines);

          // Note: here pdfLineHeight is the line height considering the white space between lines
          const authorTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * authorTextLines.length;
          topMarginAfterAuthor = startingTopMargin + authorCanvas.height / 8 + authorTextLinesHeight - 5;
        }

        html2canvas(document.getElementById('topcountrychart')).then((countryCanvas) => {
          let topMarginAfterCountry = topMarginAfterAuthor;
          if (this.countryChartIncluded) {
            numOfAddedSections += 1;
            const countryImageData = countryCanvas.toDataURL('image/png');
            doc.addImage(countryImageData, 'PNG', 15, topMarginAfterAuthor, countryCanvas.width / 8, countryCanvas.height / 8);

            const countryTextLines = doc.splitTextToSize(this.countryText.val, (pdfInMM - leftMargin - rightMargin));
            doc.text(leftMargin, topMarginAfterAuthor + countryCanvas.height / 8 + 10, countryTextLines);

            if (numOfAddedSections % 2 == 1) {
              const countryTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * countryTextLines.length;
              topMarginAfterCountry = topMarginAfterAuthor + countryCanvas.height / 8 + countryTextLinesHeight - 5;
            }
          }

          html2canvas(document.getElementById('topaffiliationchart')).then((affiliationCanvas) => {
            if (this.affiliationChartIncluded) {
              if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                doc.addPage();
                topMarginAfterCountry = Const.pdfTopMargin;
              }
              const affiliationImageData = affiliationCanvas.toDataURL('image/png');
              doc.addImage(affiliationImageData, 'PNG', 15, topMarginAfterCountry, affiliationCanvas.width / 8, affiliationCanvas.height / 8);

              const affiliationTextLines = doc.splitTextToSize(this.affiliationText.val, (pdfInMM - leftMargin - rightMargin));
              doc.text(leftMargin, topMarginAfterCountry + affiliationCanvas.height / 8 + 10, affiliationTextLines);
            }

            doc.save(`${fileName}.pdf`);
          });
        });
      });
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
    saveReview() {
      const fileName = 'Review Visual Analysis';
      const leftMargin = Const.leftMargin;
      const rightMargin = Const.rightMargin;
      const contentWidth = Const.contentWidth;
      const initialTopMargin = Const.topMargin;
      const doc = new jsPDF('p', 'pt');
      const title = 'Review Visual Analysis';
      doc.setFont('Times');
      doc.setFontSize(Const.pdfTitleFontSize);
      const titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize;
      doc.text((contentWidth - titleLength) / 2.0 + leftMargin, initialTopMargin, title);
      const startingTopMargin = initialTopMargin + Const.pdfTitleFontSize;
      doc.setFontSize(Const.pdfTextFontSize);

      let numOfAddedSections = 0;

      html2canvas(document.getElementById('scorechart')).then((scoreCanvas) => {
        var topMarginAfterScore = startingTopMargin;
        if (this.scoreDistributionChartIncluded) {
          numOfAddedSections += 1;

          const scoreImageData = scoreCanvas.toDataURL('image/png');
          const scoreImageWidth = Const.imageWidth;
          const scoreImageHeight = scoreCanvas.height * scoreImageWidth / scoreCanvas.width;
          doc.addImage(scoreImageData, 'PNG', leftMargin, startingTopMargin, scoreImageWidth, scoreImageHeight);

          const scoreTextLines = doc.splitTextToSize(this.scoreDistributionText.val, contentWidth);
          doc.text(leftMargin, startingTopMargin + scoreImageHeight + 20, scoreTextLines);

          const scoreTextHeight = Const.pdfLineHeight * Const.pdfTextFontSize * scoreTextLines.length;
          var topMarginAfterScore = startingTopMargin + scoreImageHeight + scoreTextHeight + 20;
        }

        html2canvas(document.getElementById('recommendchart')).then((recommendCanvas) => {
          let topMarginAfterRecommend = topMarginAfterScore;
          if (this.recommendDistributionChartIncluded) {
            numOfAddedSections += 1;
            const recommendImageData = recommendCanvas.toDataURL('image/png');
            const recommendImageWidth = Const.imageWidth;
            const recommendImageHeight = recommendCanvas.height * recommendImageWidth / recommendCanvas.width;
            doc.addImage(recommendImageData, 'PNG', leftMargin, topMarginAfterScore, recommendImageWidth, recommendImageHeight);

            const recommendTextLines = doc.splitTextToSize(this.recommendDistributionText.val, contentWidth);
            doc.text(leftMargin, topMarginAfterScore + recommendImageHeight + 20, recommendTextLines);

            if (numOfAddedSections % 2 == 1) {
              const recommendTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * recommendTextLines.length;
              topMarginAfterRecommend = topMarginAfterScore + recommendImageHeight + recommendTextLinesHeight + 20;
            }
          }

          html2canvas(document.getElementById('reviewtable')).then((tableCanvas) => {
            if (this.reviewTableIncluded) {
              if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                doc.addPage();
                topMarginAfterRecommend = Const.topMargin;
              }
              const tableImageData = tableCanvas.toDataURL('image/png');
              const tableImageWidth = Const.imageWidth;
              const tableImageHeight = tableCanvas.height * tableImageWidth / tableCanvas.width;
              doc.addImage(tableImageData, 'PNG', leftMargin, topMarginAfterRecommend, tableImageWidth, tableImageHeight);

              const tableTextLines = doc.splitTextToSize(this.reviewTableText.val, contentWidth);
              doc.text(leftMargin, topMarginAfterRecommend + tableImageHeight + 20, tableTextLines);
            }

            doc.save(`${fileName}.pdf`);
          });
        });
      });
    },
    saveToPdf() {
      const fileName = 'Visual Analysis';
      const leftMargin = 15;
      const rightMargin = 15;
      const pdfInMM = 210;
      const doc = new jsPDF('p', 'mm', 'a4');
      // doc.text("Hello World", 10, 10);
      const lines = doc.splitTextToSize(this.authorText.val, (pdfInMM - leftMargin - rightMargin));
      doc.text(leftMargin, 20, lines);
      html2canvas(document.getElementById('testpdf')).then((canvas) => {
        const imageData = canvas.toDataURL('image/png');
        doc.addImage(imageData, 'PNG', 15, 50, canvas.width / 8, canvas.height / 8);

        doc.save(`${fileName}.pdf`);
      });
    },
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
    getTrackInSubmission() {
      return Object.keys(this.chartData.acceptanceRateByTrack);
    },
    computeTopWordClouds(wordCountMap) {
      const wordsSorted = Object.keys(wordCountMap).sort((a, b) => wordCountMap[b] - wordCountMap[a]).slice(0, 20);
      const topWordCloud = {};
      wordsSorted.forEach((word) => {
        topWordCloud[word] = wordCountMap[word];
      });
      return topWordCloud;
    },
    indexOfMax(arr) {
      if (arr.length === 0) {
        return -1;
      }

      let max = arr[0];
      let maxIndex = 0;

      for (let i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
          maxIndex = i;
          max = arr[i];
        }
      }

      return maxIndex;
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
    computeScoreDistributionData(type) {
      // Type: "score" or "recommend"
      const label = type == 'score' ? 'Score Counts' : 'Recommendation Counts';
      const rawData = type == 'score' ? this.chartData.scoreDistribution : this.chartData.recommendDistribution;

      const return_obj = {
        labels: rawData.labels,
        datasets: [{
          label,
          data: rawData.counts,
          backgroundColor: 'rgba(52, 152, 219, 0.4)',
          pointBackgroundColor: 'white',
          borderWidth: 1,
          pointBorderColor: '#249EBF',
        }],
      };
      console.log(`************\n${JSON.stringify(return_obj, undefined, 4)}`);
      return return_obj;
    },
    computeScoreRecommendationData() {
      const return_obj = {
        labels: dummyLabels,
        datasets: [{
          label: 'No. of Recommendations',
          data: [50, 45, 40, 35, 30, 25, 20, 15, 10, 5],
          backgroundColor: 'rgba(52, 152, 219, 0.4)',
          pointBackgroundColor: 'white',
          borderWidth: 1,
          pointBorderColor: '#249EBF',
        }],
      };
      console.log(`************\n${JSON.stringify(return_obj, undefined, 4)}`);
      return return_obj;
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
    // visualization 1.2
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
  },
  beforeRouteUpdate(to, from, next) {
    // console.log("inside haha");
    next();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .chart {
    margin-bottom: 10px;
    margin-top: 10px;
  }

  .line {
    float: left;
  }

  .center-line {
    /*float: center;*/
  }

  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    /*margin: 0 10px;*/
  }

  a {
    color: #42b983;
  }
</style>
