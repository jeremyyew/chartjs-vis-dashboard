<template>
  <!--Dynamic binding of value enables auto switch tab on upload. This is actually necessary, otherwise we get the responsive canvas problem-->
  <el-tabs
    id="main-tabs"
    type="border-card"
    :value="activeTab"
    @tab-click="handleTabClick"
  >
    <el-tab-pane
      label="Authors"
      name="author"
      lazy
    >
      <div v-if="author.chartData && author.inputFileName">
        <AuthorViz
          :chart-data="author.chartData"
          :input-file-name="author.inputFileName"
        />
      </div>
      <div v-else>
        No author data
      </div>
    </el-tab-pane>




    <el-tab-pane
      label="Submissions"
      name="submission"
      lazy
    >
      <div v-if="submission.chartData && submission.inputFileName">
        <SubmissionViz
          :chart-data="submission.chartData"
          :input-file-name="submission.inputFileName"
        />
      </div>
      <div v-else>
        No submission data
      </div>
    </el-tab-pane>




    <el-tab-pane
      label="Reviews"
      name="review"
      lazy
    >
      <div v-if="review.chartData && review.inputFileName">
        <ReviewViz
          :chart-data="review.chartData"
          :input-file-name="review.inputFileName"
        />
      </div>
      <div v-else>
        No review data
      </div>
    </el-tab-pane>


    <!--Authors x Submissions -->
    <el-tab-pane
      label="Authors x Reviews"
      name="AuthorsxReviews"
      lazy
    >
      <div v-if="author.chartData && review.chartData && review.inputFileName && author.inputFileName">
        <AuthorReviewViz
          :chart-data="submission.chartData"
          :input-file-name="submission.inputFileName"
        />
      </div>
      <div v-else>
        No author or review data
      </div>
    </el-tab-pane>
    <!--Authors x Reviews ends-->


    <!--Author x Submissions-->
    <el-tab-pane
      label="Authors x Submissions"
      name="AuthorsxSubmissions"
      lazy
    >
      <div v-if="author.chartData && submission.chartData && submission.inputFileName && author.inputFileName">
        <AuthorSubmissionViz
          :chart-data="submission.chartData"
          :input-file-name="submission.inputFileName"
        />
      </div>
      <div v-else>
        No author or submission data
      </div>
    </el-tab-pane>
    <!--Authors x Submissions ends-->


  </el-tabs>
</template>

<script>
import AuthorViz from '@/components/AuthorViz';
import ReviewViz from '@/components/ReviewViz';
import SubmissionViz from './SubmissionViz'
import AuthorReviewViz from './AuthorReviewViz';
import AuthorSubmissionViz from './AuthorSubmissionViz';

export default {
  name: 'ResultTabs',
  components: { SubmissionViz, ReviewViz, AuthorViz, AuthorReviewViz, AuthorSubmissionViz },
  props: {
    result: {
      type: Object,
      required: true,
    },
    lastUpdatedViz: {
      value: {
        type: String,
        required: true,
        default: 'author',
      },
    },
    // {
    //   type: String,
    //   default: "author",
    //   required: true
    // },
  },
  data() {
    return {
      activeTab: this.lastUpdatedViz.value,
    };
    // return this.result
  },
  computed: {
    author() {
      console.log('################');
      console.log(JSON.stringify(this.result.author, undefined, 2));
      return this.result.author;
    },
    review() {
      return this.result.review;
    },
    submission() {
      return this.result.submission;
    },
    reviewsubmission() {

    },
  },
  watch: {
    lastUpdatedViz(next) {
      if (next.value !== this.activeTab) {
        this.activeTab = next.value;
      }
    },
  },
  methods: {
    handleTabClick(tab) {
      this.activeTab = tab.name;
    },
  },
};
</script>

<style scoped lang="sass">
  #main-tabs .el-tab-pane
    height: 600px
    overflow: scroll

</style>
