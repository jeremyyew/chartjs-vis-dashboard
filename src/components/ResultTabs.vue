<template>
  <el-tabs
    id="main-tabs"
    type="border-card"
  >
    <el-tab-pane label="Authors">
      <div>
        <div v-if="author">
          <AuthorViz :chartData="author.chartData" :inputFileName="author.inputFileName"/>
        </div>
        <div v-else>
          No author data
          <div/>
        </div>
        </div>
    </el-tab-pane>
    <el-tab-pane label="Submissions">Submissions</el-tab-pane>
    <el-tab-pane label="Reviews">Reviews</el-tab-pane>
    <el-tab-pane label="Reviews x Submissions">Reviews x Submissions</el-tab-pane>
  </el-tabs>
</template>

<script>
  import AuthorViz from '@/components/AuthorViz'

  export default {
    name: "ResultTabs",
    components: {AuthorViz},
    props: [
      'result'
    ],
    data: function () {
      let { author, review, submission } = this.result;
      return {
        author,
        review,
        submission
      }
    },
    watch: {
      result (newVal) {
        this.author = newVal.author
      },
      authorDataLength: function (newValue, oldValue) {
        var len = newValue;
        var authorInitialText = "So it's rather clear that the one with the largest number of submissions this year is: " + this.topAuthors.labels[0] + ", and all the top " + String(len) + ", putting together, contribute " + String(this.topAuthors.data.slice(0, len).reduce(function (a, b) {
          return a + b;
        })) + " submissions in total.";
        this.authorText = {
          val: authorInitialText,
          edit: false
        }
        this.topAuthorData = this.computeAuthorData(len);
      },
    }
  }
</script>

<style scoped lang="sass">
  #main-tabs .el-tab-pane
    height: 500px
    overflow: scroll

</style>
