'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  VUE_APP_API_BASE_URL: '"http://localhost:8000/"',
  VUE_APP_REDIRECT_URI: '"http://localhost:8080/"',
  VUE_APP_GITHUB_CLIENT_ID: '"39d4bbed1466f7617544"'
})
