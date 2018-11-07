<template>
  <center>
    <div
      id="app"
      style="width:85%;"
    >
      <el-container id="main">
        <el-header
          id="main-header"
          height="90px"
        >
          <el-row
            type="flex"
            class="row-bg"
            justify="space-between"
            align="middle"
            style="height: inherit; line-height: 15px;"
          >
            <el-col :span="6" />
            <el-col
              :span="12"
            >
              <span
                id="app-title"
                :style="{marginTop: 30 }"
              >Conference Visualizer</span>
            </el-col>
            <el-col
              id="sign-in-col"
              :span="6"
            >
              <el-button
                v-if="!isAuthenticated"
                id="sign-in"
                type="primary"
                @click="authDialogOpen = true"
              >
                Log In
              </el-button>
              <el-button
                v-if="isAuthenticated"
                id="sign-out"
                type="primary"
                @click="logout"
              >
                Log Out ({{ username }})
              </el-button>
              <el-dialog
                title="Log in or Sign Up"
                :visible.sync="authDialogOpen"
                width="50%"
              >
                <el-tabs
                  v-model="loginFormActiveTabName"
                  :stretch="true"
                >
                  <el-tab-pane
                    label="Log In"
                    name="loginTab"
                  >
                    <el-form
                      ref="loginForm"
                      v-loading="isLoginLoading"
                      :rules="loginRules"
                      :model="loginForm"
                      label-width="120px"
                    >
                      <el-form-item
                        label="Username"
                        prop="username"
                      >
                        <el-input v-model="loginForm.username" />
                      </el-form-item>
                      <el-form-item
                        label="Password"
                        prop="password"
                      >
                        <el-input
                          v-model="loginForm.password"
                          type="password"
                        />
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-block"
                          @click="login"
                        >
                          Login
                        </el-button>
                      </el-form-item>
                      <el-form-item>
                        <div class="side-line">or</div>
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-facebook btn-block"
                          icon="fab fa-facebook"
                          @click="authenticate('facebook')"
                        >
                          Login with Facebook
                        </el-button>
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-google btn-block"
                          icon="fab fa-google"
                          @click="authenticate('google')"
                        >
                          Login with Google
                        </el-button>
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-github btn-block"
                          icon="fab fa-github"
                          @click="authenticate('github')"
                        >
                          Login with Github
                        </el-button>
                      </el-form-item>
                    </el-form>
                  </el-tab-pane>
                  <el-tab-pane
                    label="Sign Up"
                    name="signupTab"
                  >
                    <el-form
                      ref="registerForm"
                      v-loading="isRegistrationLoading"
                      :rules="registerRules"
                      :model="registerForm"
                      label-width="120px"
                    >
                      <el-form-item
                        label="Email"
                        prop="email"
                      >
                        <el-input
                          v-model="registerForm.email"
                          type="email"
                        />
                      </el-form-item>
                      <el-form-item
                        label="Username"
                        prop="username"
                      >
                        <el-input
                          v-model="registerForm.username"
                        />
                      </el-form-item>
                      <el-form-item
                        label="Password"
                        prop="password"
                      >
                        <el-input
                          v-model="registerForm.password"
                          type="password"
                        />
                      </el-form-item>
                      <el-form-item
                        label="Confirm"
                        prop="checkPassword"
                      >
                        <el-input
                          v-model="registerForm.checkPassword"
                          type="password"
                        />
                      </el-form-item>
                      <el-form-item>
                        <el-button
                          type="primary"
                          class="btn-block"
                          @click="register"
                        >
                          Sign Up
                        </el-button>
                      </el-form-item>
                    </el-form>
                  </el-tab-pane>
                </el-tabs>

                <span
                  slot="footer"
                  class="dialog-footer"
                />
              </el-dialog>
            </el-col>
          </el-row>
        </el-header>
        <el-container>
          <el-aside style="width:20%;">
            <!--<router-link to="/">-->
            <!--<el-button @click="startHacking" type="primary">Start</el-button>-->
            <!--</router-link>-->
            <!--<router-link to="/chart" :chartData="testChartsDataInput">-->
            <!--<el-button type="selection">Chart</el-button>-->
            <!--</router-link>-->
            <!--router-link to="/ec">
              <el-button type="success">EC</el-button>
            </router-link-->
            <!--<router-link to="/te">-->
            <!--<el-button type="success">WY</el-button>-->
            <!--</router-link>-->
            <el-dialog
              title="Map author.csv headers"
              :visible.sync="mappingAuthorData.dialogOpen"
              width="85%"
              @close="resetFile('mappingAuthorData')"
            >
              <el-table
                :data="mappingAuthorData.previewData"
                border
              >
                <el-table-column
                  v-for="idx in (0, mappingAuthorData.numCols)"
                  :key="idx"
                  :render-header="selectHeaders"
                  :label="null"
                  :prop="String(idx-1)"
                  :width="150"
                />
              </el-table>
              <el-button
                type="primary"
                @click="getDataInsight('mappingAuthorData')"
              >
                Submit
              </el-button>
            </el-dialog>
            <el-dialog
              title="Map submission.csv headers"
              :visible.sync="mappingSubmissionData.dialogOpen"
              width="85%"
              @close="resetFile('mappingSubmissionData')"
            >
              <el-table
                :data="mappingSubmissionData.previewData"
                border
              >
                <el-table-column
                  v-for="idx in (0, mappingSubmissionData.numCols)"
                  :key="idx"
                  :render-header="selectHeaders"
                  :label="null"
                  :prop="String(idx-1)"
                  :width="150"
                />
              </el-table>
              <el-button
                type="primary"
                @click="getDataInsight('mappingSubmissionData')"
              >
                Submit
              </el-button>
            </el-dialog>
            <el-dialog
              title="Map review.csv headers"
              :visible.sync="mappingReviewData.dialogOpen"
              width="85%"
              @close="resetFile('mappingReviewData')"
            >
              <el-table
                :data="mappingReviewData.previewData"
                border
              >
                <el-table-column
                  v-for="idx in (0, mappingReviewData.numCols)"
                  :key="idx"
                  :render-header="selectHeaders"
                  :label="null"
                  :prop="String(idx-1)"
                  :width="150"
                />
              </el-table>
              <el-button
                type="primary"
                @click="getDataInsight('mappingReviewData')"
              >
                Submit
              </el-button>
            </el-dialog>
            <center id="upload">
              <form
                v-if="isInitial || isSaving || isSuccess"
                enctype="multipart/form-data"
                novalidate
              >
                <!--The type multipart/form-data is important, otherwise Django will not accept-->
                <h2>Upload Files</h2>
                <h4>Drag files into their respective boxes, or click to browse</h4>
                <div class="dropbox">
                  <input
                    type="file"
                    :name="uploadFieldName"
                    :disable="isSaving"
                    accept=".csv"
                    class="input-author-file"
                    @change="uploadCSV($event.target.name, $event.target.files,
                                       'mappingAuthorData')"
                  >
                  <p style="margin-bottom:0px;padding-top:32px;font-size:18px">
                    <strong>author.csv</strong>
                  </p>
                </div>
                <div class="dropbox">
                  <input
                    type="file"
                    :name="uploadFieldName"
                    :disable="isSaving"
                    accept=".csv"
                    class="input-submission-file"
                    @change="uploadCSV($event.target.name, $event.target.files,
                                       'mappingSubmissionData')"
                  >
                  <p style="margin-bottom:0px;padding-top:32px;font-size:18px">
                    <strong>submission.csv</strong>
                  </p>
                </div>
                <div class="dropbox">
                  <input
                    type="file"
                    :name="uploadFieldName"
                    :disable="isSaving"
                    accept=".csv"
                    class="input-review-file"
                    @change="uploadCSV($event.target.name, $event.target.files,
                                       'mappingReviewData')"
                  >
                  <p style="margin-bottom:0px;padding-top:32px;font-size:18px">
                    <strong>review.csv</strong>
                  </p>
                </div>
              </form>
            </center>
          </el-aside>
          <el-main>
            <ResultTabs
              :result="result"
              :last-updated-viz="lastUpdatedViz"
            />
            <center>
              <router-view :key="$route.fullPath" />
            </center>
          </el-main>
        </el-container>
        <el-footer id="main-footer">
          <el-row
            type="flex"
            class="row-bg"
            justify="space-between"
            style="height: inherit"
          >
            <el-col :span="4" />
            <el-col :span="12" />
            <el-col :span="4">
              <img
                src="./assets/logo.png"
                style="vertical-align: middle;width: 20px; "
              >
            </el-col>
          </el-row>
        </el-footer>
      </el-container>
    </div>
  </center>

</template>

<script>
import ResultTabs from '@/components/ResultTabs';
import Auth from '@/components/Auth';
import Store from '@/store';
import utils from '@/utils';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import { upload } from './components/Upload';

const STATUS_INITIAL = 0;
const STATUS_SAVING = 1;
const STATUS_SUCCESS = 2;
const
  STATUS_FAILED = 3;

const { stringify } = utils;

const REFRESH_TOKEN_MS = 15 * 60 * 1000;
let refreshTokenTimer;

export default {
  name: 'App',
  components: { ResultTabs },
  data() {
    const validatePassword = (rule, value, callback) => {
      if (this.registerForm.checkPassword !== '') {
        this.$refs.registerForm.validateField('checkPassword');
      }
      callback();
    };
    const validateCheckPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('Please confirm your password again because it is not matching.'));
      } else {
        callback();
      }
    };
    return {
      storeState: Store.state,
      authDialogOpen: false,
      isRegistrationLoading: false,
      isLoginLoading: false,
      isAuthenticated: this.$auth.isAuthenticated(),
      username: this.$auth.isAuthenticated() ? jwt_decode(this.$auth.getToken()).username : null,
      loginFormActiveTabName: 'loginTab',
      loginForm: {
        username: '',
        password: '',
      },
      loginRules: {
        username: [
          {
            required: true,
            message: 'Please input a username',
            trigger: 'blur',
          },
        ],
        password: [
          {
            required: true,
            message: 'Please input a password',
            trigger: 'blur',
          },
        ],
      },
      registerForm: {
        email: '',
        username: '',
        password: '',
        checkPassword: '',
      },
      registerRules: {
        email: [
          {
            required: true,
            message: 'Please input an email address',
            trigger: 'blur',
          },
          {
            type: 'email',
            message: 'Please input a valid email',
            trigger: 'blur',
          },
        ],
        username: [
          {
            required: true,
            message: 'Please input a username',
            trigger: 'blur',
          },
        ],
        password: [
          {
            required: true,
            message: 'Please input a password',
            trigger: 'blur',
          },
          {
            validator: validatePassword,
            trigger: 'blur',
          },
        ],
        checkPassword: [
          {
            required: true,
            message: 'Please confirm your password',
            trigger: 'blur',
          },
          {
            validator: validateCheckPassword,
            trigger: 'blur',
          },
        ],
      },
      uploadedFiles: [],
      uploadError: null,
      currentStatus: null,
      uploadFieldName: 'file',
      testChartsDataInput: null,
      result: {
        author: {},
        review: {},
        submission: {},
      },
      mappingAuthorData: {
        placeHolder: [],
        previewData: [],
        numCols: 0,
        dialogOpen: false,
        methodName: 'getAuthorInfo',
        fileID: '.input-author-file',
        initialUploadForm: {
          data: null,
          firstNameIndex: -1,
          lastNameIndex: -1,
          countryIndex: -1,
          affiliationIndex: -1,
        },
        uploadForm: {
          data: null,
          firstNameIndex: -1,
          lastNameIndex: -1,
          countryIndex: -1,
          affiliationIndex: -1,
        },
        options: [
          {
            value: 'firstNameIndex',
            label: 'First Name',
          },
          {
            value: 'lastNameIndex',
            label: 'Last Name',
          },
          {
            value: 'countryIndex',
            label: 'Country',
          },
          {
            value: 'affiliationIndex',
            label: 'Affiliation',
          },
        ],
      },
      mappingSubmissionData: {
        placeHolder: [],
        previewData: [],
        numCols: 0,
        dialogOpen: false,
        methodName: 'getSubmissionInfo',
        fileID: '.input-submission-file',
        initialUploadForm: {
          data: null,
          trackNameIndex: -1,
          authorIndex: -1,
          submissionTimeIndex: -1,
          lastEditTimeIndex: -1,
          keywordIndex: -1,
          decisionIndex: -1,
        },
        uploadForm: {
          data: null,
          trackNameIndex: -1,
          authorIndex: -1,
          submissionTimeIndex: -1,
          lastEditTimeIndex: -1,
          keywordIndex: -1,
          decisionIndex: -1,
        },
        options: [
          {
            value: 'trackNameIndex',
            label: 'Track Name',
          },
          {
            value: 'authorIndex',
            label: 'Author',
          },
          {
            value: 'submissionTimeIndex',
            label: 'Submission Time',
          },
          {
            value: 'lastEditTimeIndex',
            label: 'Last Edit Time',
          },
          {
            value: 'keywordIndex',
            label: 'Keyword',
          },
          {
            value: 'decisionIndex',
            label: 'Decision',
          },
        ],
      },
      mappingReviewData: {
        placeHolder: [],
        previewData: [],
        numCols: 0,
        dialogOpen: false,
        methodName: 'getReviewInfo',
        fileID: '.input-review-file',
        initialUploadForm: {
          data: null,
          submissionIDIndex: -1,
          evaluationIndex: -1,
        },
        uploadForm: {
          data: null,
          submissionIDIndex: -1,
          evaluationIndex: -1,
        },
        options: [
          {
            value: 'submissionIDIndex',
            label: 'Submission ID',
          },
          {
            value: 'evaluationIndex',
            label: 'Evaluation',
          },
        ],
      },
      lastUpdatedViz: { value: 'author' },
      options: [
        {
          value: 'author',
          label: 'Author File',
        }, {
          value: 'submission',
          label: 'Submission File',
        }, {
          value: 'review',
          label: 'Review File',
        },
      ],
    };
  },
  computed: {
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isSaving() {
      return this.currentStatus === STATUS_SAVING;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
    },
    isFailed() {
      return this.currentStatus === STATUS_FAILED;
    },
  },
  watch: {
  },
  created() {
    console.log(`Store.state: ${stringify(Store.state)}`);
    console.log(`storeState: ${stringify(this.storeState)}`);
    this.$persist(['storeState']);


    if (this.$auth.getToken() !== null) {
      this.refreshToken();
    }
  },
  mounted() {
    this.reset();
  },
  methods: {
    // startHacking() {
    //   this.$notify({
    //     title: 'It works!',
    //     type: 'success',
    //     message: 'We\'ve laid the ground work for you.',
    //     duration: 2500,
    //   });
    // },
    setUserAuthenticated() {
      this.isAuthenticated = true;
      this.username = jwt_decode(this.$auth.getToken()).username;
      refreshTokenTimer = setTimeout(this.refreshToken, REFRESH_TOKEN_MS);
    },
    login() {
      this.$refs.loginForm.validate((valid) => {
        if (!valid) {
          return false;
        }
        this.isLoginLoading = true;
        this.$auth.login(this.loginForm).then(() => {
          this.setUserAuthenticated();
          this.authDialogOpen = false;
        }).catch((error) => {
          const errorMessage = error.response.data.non_field_errors[0];

          this.$message({
            message: errorMessage !== undefined ? errorMessage : 'Unexpected login failure. Please try again later.',
            type: 'error',
          });
        }).finally(() => {
          this.isLoginLoading = false;
        });

        return true;
      });
    },
    register() {
      this.$refs.registerForm.validate((valid) => {
        if (!valid) {
          return false;
        }

        this.isRegistrationLoading = true;
        this.$auth.register({
          username: this.registerForm.username,
          email: this.registerForm.email,
          password: this.registerForm.password,
        }).then((response) => {
          this.$message({
            message: 'Sign up successful!',
            type: 'success',
          });
          // TODO: trigger login automatically?
        }).catch((error) => {
          this.$message({
            message: error.response.data.detail,
            type: 'error',
          });
        }).finally(() => {
          this.isRegistrationLoading = false;
        });
        return true;
      });
    },
    refreshToken() {
      axios.post(process.env.VUE_APP_API_BASE_URL + process.env.VUE_APP_TOKEN_REFRESH_URL,
        { token: this.$auth.getToken() })
        .then(() => {
          this.setUserAuthenticated();
        })
        .catch(() => {
          this.logout();
        });
    },
    authenticate(provider) {
      // Auth.authenticate(provider);
      // Store.login('jeremy.yew@u.yale-nus.edu.sg');
      this.isLoginLoading = true;
      this.$auth.authenticate(provider, { provider: provider === 'google' ? 'google-oauth2' : provider })
        .then(() => {
          this.setUserAuthenticated();
          this.authDialogOpen = false;
          this.isLoginLoading = false;

          axios.post(`${process.env.VUE_APP_API_BASE_URL}api/checkauth/`)
            .then((responseInner) => {
              console.log(responseInner.data);
            })
            .catch((error) => {
            });
        })
        .catch((error) => {
          // We want to use finally to set the login loading to false.
          // However, the promise here is a custom implementation and has no finally.
          this.isLoginLoading = false;
          console.log(error);
        });
    },
    logout() {
      // Store.logout();
      this.$auth.logout()
        .then(() => {
          clearTimeout(refreshTokenTimer);
          this.isAuthenticated = false;
          // Because we want to allow calling logout at any point of time, e.g. during create,
          // this (and child) components might not have been mounted yet
          this.$nextTick(() => {
            this.$message({
              message: 'You have been signed out!',
              type: 'warning',
            });
          });
        })
        .catch((error) => {
          console.log(`Failed to log out: ${error}`);
        });
    },
    reset() {
      // reset form to initial state
      this.currentStatus = STATUS_INITIAL;
      this.uploadedFiles = [];
      this.uploadError = null;
    },
    resetFile(dataField) {
      document.querySelector(this[dataField].fileID).value = '';
    },
    selectHeaders(createElement, { column, $index }) {
      let dataField = 'mappingAuthorData';
      if (this.mappingSubmissionData.dialogOpen) dataField = 'mappingSubmissionData';
      if (this.mappingReviewData.dialogOpen) dataField = 'mappingReviewData';

      return createElement(
        'el-select', {
          props: {
            placeholder: 'Select',
            value: this[dataField].placeHolder[$index],
            clearable: true,
          },
          on: {
            change: (value) => {
              for (const field in this[dataField].uploadForm) {
                if (this[dataField].uploadForm[field] === $index) {
                  this[dataField].uploadForm[field] = -1;
                }
              }
              this[dataField].placeHolder[$index] = value;
              this[dataField].uploadForm[value] = $index;
            },
          },
        },
        [
          this[dataField].options.map(option => createElement('el-option', {
            props: {
              key: option.value,
              value: option.value,
              label: option.label,
              disabled: this[dataField].uploadForm[option.value] !== -1,
            },
          }))],
      );
    },
    uploadCSV(fieldName, fileList, dataField) {
      if (!fileList.length) return;

      this.currentStatus = STATUS_SAVING;

      const formData = new FormData();
      Array
        .from(Array(fileList.length)
          .keys())
        .map((x) => {
          formData.append(fieldName, fileList[x], fileList[x].name);
        });

      upload(formData, 'parse')
        .then((x) => {
          this[dataField].uploadForm.data = x.data;
          this[dataField].previewData = x.previewData;
          this[dataField].numCols = Object.keys(x.previewData[0]).length;
          this[dataField].dialogOpen = true;
        })
        .catch((err) => {
          this.uploadError = err.response;
          this.currentStatus = STATUS_FAILED;
          this.resetFile(dataField);
        });
    },
    getDataInsight(dataField) {
      for (const field in this[dataField].uploadForm) {
        if (field !== 'data' && this[dataField].uploadForm[field] === -1) {
          this.$message({
            message: 'All headers fields must be filled up!',
            type: 'error',
          });
          return;
        }
      }

      this[dataField].dialogOpen = false;
      const nameArray = document.querySelector(this[dataField].fileID).value.split('\\');
      const inputFileName = nameArray[nameArray.length - 1];

      upload(this[dataField].uploadForm, this[dataField].methodName)
        .then((x) => {
          this.currentStatus = STATUS_SUCCESS;

          this.lastUpdatedViz = { value: x.infoType };
          this.result[x.infoType] = {
            inputFileName,
            chartData: x.infoData,
          };
        })
        .catch((err) => {
          this.uploadError = err.response;
          this.currentStatus = STATUS_FAILED;
        }).finally(() => {
          this[dataField].uploadForm = this[dataField].initialUploadForm;
          this[dataField].placeHolder = [];
        });
    },
  },
};

</script>

<style lang="scss">
  @import "@fortawesome/fontawesome-free/css/all.css";
  @import "@fortawesome/fontawesome-free/css/fontawesome.css";
  $content-padding: 20px;
  #upload {
  }

  .dropbox {
    outline: 2px dashed grey; /* the dash box */
    outline-offset: -10px;
    background: lightcyan;
    color: dimgray;
    /*padding: 10px 10px;*/
    height: 100px; /* minimum height */
    width: 90%;
    position: relative;
    cursor: pointer;
  }

  .input-author-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    height: 100%;
    position: absolute;
    cursor: pointer;
    left: 0; /*put this otherwise the input box will shift by half of the parent width */
  }

  .input-submission-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    height: 100%;
    position: absolute;
    cursor: pointer;
    left: 0; /*put this otherwise the input box will shift by half of the parent width */
  }

  .input-review-file {
    opacity: 0; /* invisible but it's there! */
    width: 100%;
    height: 100%;
    position: absolute;
    cursor: pointer;
    left: 0; /*put this otherwise the input box will shift by half of the parent width */
  }

  .dropbox:hover {
    background: lightblue; /* when mouse over to the drop zone, change color */
  }

  .dropbox p {
    font-size: 1.2em;
    text-align: center;
    padding: 50px 0;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    width: 100% !important;
    /*margin-top: 30px;*/
  }

  #main {
    /*margin-bottom: 20px;*/
  }

  .el-header,
  .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
    /*margin-bottom: 5px;*/
  }

  .el-aside {
    padding: $content-padding;
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 30px;
    /*margin-right: 5px;*/
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    height: 800px;
    /*text-align: center;*/
    /*line-height: 450px;*/
  }

  body {
    margin: 0;
  }

  body > .el-container {
    /*margin-bottom: 40px;*/
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  #sign-in {
  }

  #sign-in-col {
  }

  #app-title-col {

  }

  #app-title {
    font-weight: bolder;
    font-size: 30px;
    margin-top: 50px;
  }

  #main-header {
  }

  .side-line {
    display: flex;
    flex-direction: row;
  }

  .side-line:before, .side-line:after {
    content: "";
    flex: 1 1;
    border-bottom: 1px solid rgba(0,0,0,.2);
    margin:auto .5em;
  }

  .btn-block {
    width: 100%;
  }

  .btn-facebook {
    border: 0;
    background-color: #4267b2;
  }
  .btn-facebook:hover, .btn-facebook:focus {
    background-color: #3b5291;
  }
  .btn-google {
    border: 0;
    background-color: #4285f4;
  }
  .btn-google:hover, .btn-google:focus {
    background-color: #426fde;
  }
  .btn-github {
    border: 0;
    background-color: #333333;
  }
  .btn-github:hover, .btn-github:focus {
    background-color: #555555;
  }
</style>
