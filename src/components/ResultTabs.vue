<template>
  <el-tabs
    id="main-tabs"
    type="border-card"
  >
    <el-tab-pane label="Authors" name="author">
      <div>
        <div v-if="author.chartData && author.inputFileName">
          <AuthorViz :chartData="author.chartData" :inputFileName="author.inputFileName"/>
        </div>
        <div v-else>
          No author data
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="Submissions" name="submission">
      <div v-if="submission.chartData && submission.inputFileName">
        <AuthorViz :chartData="submission.chartData" :inputFileName="submission.inputFileName"/>
      </div>
      <div v-else>
        No submission data
      </div>
    </el-tab-pane>
    <el-tab-pane label="Reviews" name="review">
      <div v-if="review.chartData && review.inputFileName">
        <ReviewViz :chartData="review.chartData" :inputFileName="review.inputFileName"/>
      </div>
      <div v-else>
        No review data
      </div>
    </el-tab-pane>
    <el-tab-pane label="Reviews x Submissions">Reviews x Submissions</el-tab-pane>
  </el-tabs>
</template>

<script>
  import AuthorViz from '@/components/AuthorViz';
  import ReviewViz from '@/components/ReviewViz';

  export default {
    name: "ResultTabs",
    components: {ReviewViz, AuthorViz},
    props: [
      'result'
    ],
    data() {
      // const {author, review, submission } = this.result;
      // return {
      //   author,
      //   review,
      //   submission,
      //   // activeTab: lastUpdatedViz
      // }
      return this.result
    }
  }
</script>

<style scoped lang="sass">
  #main-tabs .el-tab-pane
    height: 600px
    overflow: scroll

</style>
