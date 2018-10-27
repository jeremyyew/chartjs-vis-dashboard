<template>
  <!--Dynamic binding of value enables auto switch tab on upload. This is actually necessary, otherwise we get the responsive canvas problem-->
  <el-tabs
    id="main-tabs"
    type="border-card"
    :value="activeTab"
    @tab-click="handleTabClick"
  >
    <el-tab-pane label="Authors" name="author" lazy>
      <div v-if="author.chartData && author.inputFileName">
        <AuthorViz :chartData="author.chartData" :inputFileName="author.inputFileName"/>
      </div>
      <div v-else>
        No author data
      </div>
    </el-tab-pane>
    <el-tab-pane label="Submissions" name="submission" lazy>
      <div v-if="submission.chartData && submission.inputFileName">
        <AuthorViz :chartData="submission.chartData" :inputFileName="submission.inputFileName"/>
      </div>
      <div v-else>
        No submission data
      </div>
    </el-tab-pane>
    <el-tab-pane label="Reviews" name="review" lazy>
      <div v-if="review.chartData && review.inputFileName">
        <ReviewViz :chartData="review.chartData" :inputFileName="review.inputFileName"/>
      </div>
      <div v-else>
        No review data
      </div>
    </el-tab-pane>
    <el-tab-pane label="Reviews x Submissions" name="reviewXSubmission"  lazy>Reviews x Submissions</el-tab-pane>
  </el-tabs>
</template>

<script>
  import AuthorViz from '@/components/AuthorViz';
  import ReviewViz from '@/components/ReviewViz';

  export default {
    name: "ResultTabs",
    components: {ReviewViz, AuthorViz},
    props: {
      result: {
        type: Object,
        required: true
      },
      lastUpdatedViz: {
        value: {
          type: String,
          required: true,
          default: "author"
        }
      }
        // {
        //   type: String,
        //   default: "author",
        //   required: true
        // },
    },
    data() {
      return {
        activeTab: this.lastUpdatedViz.value
      }
      // return this.result
    },
    methods: {
      handleTabClick(tab) {
        this.activeTab = tab.name;
        console.log(this.activeTab)
      }
    },
    computed: {
      author() {
        return this.result.author
      },
      review() {
        return this.result.review
      },
      submission() {
        return this.result.submission
      }
    },
    watch: {
      lastUpdatedViz(next) {
        if (next.value !== this.activeTab) {
          this.activeTab = next.value
        }
      }
    }
  }
</script>

<style scoped lang="sass">
  #main-tabs .el-tab-pane
    height: 600px
    overflow: scroll

</style>
