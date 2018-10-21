<template>
  <div>
    <el-switch
      v-model="scoreDistributionChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included">
    </el-switch>
    <bar-chart :data-input="scoreDistributionData" :title-text="'Score Distribution'" class="chart" id="scorechart"
               ref="scorechart"></bar-chart>
    <editable-text v-bind:text.sync="scoreDistributionText" style="margin-bottom: 20px;"></editable-text>

    <el-switch
      v-model="recommendDistributionChartIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included">
    </el-switch>
    <bar-chart :data-input="recommendDistributionData" :title-text="'Recommendation Distribution'" class="chart"
               id="recommendchart" ref="recommendchart"></bar-chart>
    <editable-text v-bind:text.sync="recommendDistributionText" style="margin-bottom: 20px;"></editable-text>

    <el-switch
      v-model="reviewTableIncluded"
      active-color="#13ce66"
      active-text="Included in Report"
      inactive-text="Not Included">
    </el-switch>
    <p>
      The mean scores and mean confidence values can be found as follows:
    <div id="reviewtable" ref="reviewtable">
      <el-table
        :data="reviewTableData"
        stripe
        style="width: 70%;margin-top:10px;margin-bottom: 10px">
        <el-table-column
          prop="field"
          label="Field"
          width="180">
        </el-table-column>
        <el-table-column
          prop="value"
          label="Value"
          width="180">
        </el-table-column>
      </el-table>
    </div>
    <editable-text v-bind:text.sync="reviewTableText"></editable-text>
    <el-button @click="saveReview" type="success" plain style="margin-top: 10px">Save</el-button>
  </div>
</template>

<script>
  import BarChart from '@/components/BarChart'
  import EditableText from '@/components/EditableText'

  import Const from './const'

  export default {
    name: "ReviewViz",
    props: ['chartData', 'inputFileName'],
    components: {
      BarChart,
      EditableText,
    },
    data() {
      var scoreRanges = this.computeScoreDistributionData("score").labels;
      var scoreCounts = this.computeScoreDistributionData("score").datasets[0].data;

      var topIndex = this.indexOfMax(scoreCounts);
      var topRange = scoreRanges[topIndex];

      var recommendCounts = this.computeScoreDistributionData("recommend").datasets[0].data;
      var firstEntryPercentage = recommendCounts[0] / recommendCounts.reduce(function (a, b) {
        return a + b;
      }) * 100;

      return {
        msg: 'Review Info Analysis',
        scoreDistributionData: this.computeScoreDistributionData("score"),
        recommendDistributionData: this.computeScoreDistributionData("recommend"),
        reviewTableData: [
          {
            field: 'Mean Score',
            value: this.chartData.meanScore.toFixed(2)
          }, {
            field: 'Mean Recommendation',
            value: this.chartData.meanRecommend.toFixed(2)
          }, {
            field: 'Mean Confidence',
            value: this.chartData.meanConfidence.toFixed(2)
          }
        ],
        scoreDistributionChartIncluded: true,
        recommendDistributionChartIncluded: true,
        reviewTableIncluded: true,
        scoreDistributionText: {
          val: "Note that when considering the review scores, we are combining multiple entries at the same time: here for the overall score of each paper, we take all reviews for a particular paper, retrieve its overall score and the reviewer's confidence, then calculate the weighted average of the scores w.r.t. the confidence value, and then here it is. It's rather clear that the score range with the largest count is " + String(topRange) + " (a relatively low score though, :-)).",
          edit: false
        },
        recommendDistributionText: {
          val: "The same logic applies to the recommendation scores. Note that we use 0 to represent 'not recommended for best paper', and 1 as 'recommended for best paper', and then do a weighted average using the confidence value. It's hence also clear that the 0's takes up " + String(firstEntryPercentage.toFixed(2)) + "%.",
          edit: false
        },
        reviewTableText: {
          val: "The mean score and recommendation values can be found here, and you are free to add in any additional comments and remarks here.",
          edit: false
        }
      }
    },
    methods : {
      computeScoreDistributionData: function (type) {
        // Type: "score" or "recommend"
        var label = type == "score" ? 'Score Counts' : 'Recommendation Counts';
        var rawData = type == "score" ? this.chartData.scoreDistribution : this.chartData.recommendDistribution;
        return {
          labels: rawData.labels,
          datasets: [{
            label: label,
            data: rawData.counts,
            backgroundColor: 'rgba(52, 152, 219, 0.4)',
            pointBackgroundColor: 'white',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
          }]
        }
      },
      indexOfMax: function (arr) {
        if (arr.length === 0) {
          return -1;
        }

        var max = arr[0];
        var maxIndex = 0;

        for (var i = 1; i < arr.length; i++) {
          if (arr[i] > max) {
            maxIndex = i;
            max = arr[i];
          }
        }

        return maxIndex;
      },
      saveReview: function () {
        let fileName = 'Review Visual Analysis';
        var leftMargin = Const.leftMargin;
        var rightMargin = Const.rightMargin;
        var contentWidth = Const.contentWidth;
        var initialTopMargin = Const.topMargin;
        var doc = new jsPDF("p", "pt");
        var title = "Review Visual Analysis";
        doc.setFont("Times");
        doc.setFontSize(Const.pdfTitleFontSize);
        var titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize;
        doc.text((contentWidth - titleLength) / 2.0 + leftMargin, initialTopMargin, title);
        var startingTopMargin = initialTopMargin + Const.pdfTitleFontSize;
        doc.setFontSize(Const.pdfTextFontSize);

        var numOfAddedSections = 0;

        html2canvas(document.getElementById('scorechart')).then(scoreCanvas => {
          var topMarginAfterScore = startingTopMargin;
          if (this.scoreDistributionChartIncluded) {
            numOfAddedSections += 1;

            var scoreImageData = scoreCanvas.toDataURL("image/png");
            var scoreImageWidth = Const.imageWidth;
            var scoreImageHeight = scoreCanvas.height * scoreImageWidth / scoreCanvas.width;
            doc.addImage(scoreImageData, 'PNG', leftMargin, startingTopMargin, scoreImageWidth, scoreImageHeight);

            var scoreTextLines = doc.splitTextToSize(this.scoreDistributionText.val, contentWidth);
            doc.text(leftMargin, startingTopMargin + scoreImageHeight + 20, scoreTextLines);

            var scoreTextHeight = Const.pdfLineHeight * Const.pdfTextFontSize * scoreTextLines.length;
            var topMarginAfterScore = startingTopMargin + scoreImageHeight + scoreTextHeight + 20;

          }

          html2canvas(document.getElementById('recommendchart')).then(recommendCanvas => {
            var topMarginAfterRecommend = topMarginAfterScore;
            if (this.recommendDistributionChartIncluded) {
              numOfAddedSections += 1;
              var recommendImageData = recommendCanvas.toDataURL("image/png");
              var recommendImageWidth = Const.imageWidth;
              var recommendImageHeight = recommendCanvas.height * recommendImageWidth / recommendCanvas.width;
              doc.addImage(recommendImageData, 'PNG', leftMargin, topMarginAfterScore, recommendImageWidth, recommendImageHeight);

              var recommendTextLines = doc.splitTextToSize(this.recommendDistributionText.val, contentWidth);
              doc.text(leftMargin, topMarginAfterScore + recommendImageHeight + 20, recommendTextLines);

              if (numOfAddedSections % 2 == 1) {
                var recommendTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * recommendTextLines.length;
                topMarginAfterRecommend = topMarginAfterScore + recommendImageHeight + recommendTextLinesHeight + 20;
              }
            }

            html2canvas(document.getElementById('reviewtable')).then(tableCanvas => {
              if (this.reviewTableIncluded) {
                if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
                  doc.addPage();
                  topMarginAfterRecommend = Const.topMargin;
                }
                var tableImageData = tableCanvas.toDataURL("image/png");
                var tableImageWidth = Const.imageWidth;
                var tableImageHeight = tableCanvas.height * tableImageWidth / tableCanvas.width;
                doc.addImage(tableImageData, 'PNG', leftMargin, topMarginAfterRecommend, tableImageWidth, tableImageHeight);

                var tableTextLines = doc.splitTextToSize(this.reviewTableText.val, contentWidth);
                doc.text(leftMargin, topMarginAfterRecommend + tableImageHeight + 20, tableTextLines);
              }

              doc.save(fileName + '.pdf');
            });
          });
        });

      },
    }
  }
</script>

<style scoped>

</style>
