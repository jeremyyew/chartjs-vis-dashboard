<template>
  <el-dialog
    title="Map author.csv headers"
    :visible.sync="mappingData.dialogOpen"
    width="85%"
    @close="resetFile"
  >
    <el-table
      :data="mappingData.previewData"
      border
    >
      <el-table-column
        v-for="idx in (0, mappingData.numCols)"
        :key="idx"
        :render-header="selectHeaders"
        :label="null"
        :prop="String(idx-1)"
        :width="150"
      />
    </el-table>
    <el-button
      type="primary"
      :disabled="mappingData.numCols < mappingData.defaultMinCol"
      @click="getDataInsightDefaultHeaders(dataTypeName)"
    >
      Default
    </el-button>
    <el-button
      type="primary"
      @click="getDataInsight(dataTypeName)"
    >
      Submit
    </el-button>
  </el-dialog>
</template>

<script>

import { upload } from '@/components/Upload';

export default {
  name: 'MappingHeaderDialog',
  props: {
    mappingData: {
      type: Object,
      required: true,
    },
    dataTypeName: {
      type: String,
      required: true,
    },
  },
  methods: {
    resetFile() {
      document.querySelector(this.mappingData.fileID).value='';
    },
    selectHeaders(createElement, { column, $index }) {
      return createElement(
        'el-select', {
          props: {
            placeholder: 'Select',
            value: this.mappingData.placeHolder[$index],
            clearable: true,
          },
          on: {
            change: (value) => {
              for (const field in this.mappingData.uploadForm) {
                if (this.mappingData.uploadForm[field] === $index) {
                  this.mappingData.uploadForm[field] = -1;
                }
              }
              this.mappingData.placeHolder[$index] = value;
              this.mappingData.uploadForm[value] = $index;
            },
          },
        },
        [
          this.mappingData.options.map(option => createElement('el-option', {
            props: {
              key: option.value,
              value: option.value,
              label: option.label,
              disabled: this.mappingData.uploadForm[option.value] !== -1,
            },
          }))],
      );
    },
    getDataInsightDefaultHeaders() {
      this.mappingData.uploadForm = this.mappingData.defaultUploadForm;
      this.getDataInsight();
    },
    getDataInsight() {
      for (const field in this.mappingData.uploadForm) {
        if (this.mappingData.uploadForm[field] === -1) {
          this.$message({
            message: 'All headers fields must be filled up!',
            type: 'error',
          });
          return;
        }
      }

      this.mappingData.dialogOpen = false;
      const nameArray = document.querySelector(this.mappingData.fileID).value.split('\\');
      const inputFileName = nameArray[nameArray.length - 1];

      upload(this.mappingData.uploadForm, this.mappingData.methodName)
        .then((x) => {
          const result = {
            inputFileName,
            chartData: x.infoData,
          };
          this.$emit('dataProcessSuccess', x.infoType, result);
        })
        .catch((err) => {
          this.$emit('dataProcessFailed', err);
        }).finally(() => {
          this.mappingData.uploadForm = this.mappingData.initialUploadForm;
          this.mappingData.placeHolder = [];
        });
    },
  },
};
</script>

<style scoped lang="sass">
.el-tab-pane
  height: 600px
  overflow: scroll

</style>
