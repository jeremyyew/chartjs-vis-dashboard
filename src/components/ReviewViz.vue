<template>
  <div>
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
    </p>
    <div
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
    <editable-text :text.sync="reviewTableText"/>
    <el-button
      type="success"
      plain
      style="margin-top: 10px"
      @click="saveReview"
    >Save
    </el-button>
  </div>
</template>

<script>
import BarChart from '@/components/BarChart';
import EditableText from '@/components/EditableText';

import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// visualization 2.1
import {
  dummyLabels,
  dummyData,
} from '../mocks/ScoreRecommendationMock';

import Const from './Const';

export default {
  name: 'ReviewViz',
  components: {
    BarChart,
    EditableText,
  },
  props: ['chartData', 'inputFileName'],
  data() {
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
  },
  methods: {
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
  },
};
</script>

<style scoped>

</style>
