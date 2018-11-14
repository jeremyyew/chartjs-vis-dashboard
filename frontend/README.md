# VIZ Project from Publication Data

> A Vue.js project

## Saving visualizations in a PDF document
### TODO:
- [ ] Proper keys for tabs
- [ ] Refactor review, author_review, author_submission
- [ ] Remove old print methods
- [ ] Fix word clouds?
- [ ] Loading + printing overlay
- [ ] Docs: change in component architecture

### Previous approach: component-level methods and data
Previously the saving of visualizations into PDF was done via standalone component-level methods such as `saveAuthor` or `saveSubmission`. These were lengthy and highly repetitive. 

The main motivation of the new mechanism detailed below is to be able to print all charts in one document, which was not possible via the previous approach as each method had to access component-level data. The new mechanism also abstracts the process of generating the PDF, and reduces code duplication. 

### New approach: global store and `PdfGenerator` class 
The class `PdfGenerator` in `utils` uses `html2canvas` to  transform the html elements created with `chartjs` to `canvas` elements, and then saves them in a pdf document. It takes care of formatting, margins, styling, etc. 

We use a global store object to keep track of all the charts and whether each is included or not - this helps us avoid having to:
 - declare chart-printing-related information at the `App` level and pass them as props to individual components through `ResultTabs` to each tab, and
  - use events to trigger changes in chart info from the child to the parent, 
  thus decoupling each set of charts from the main `App`. 
  
### Usage at viz component level: 
1. Register the chart `id`'s in the global store at the `created()` hook: 
     ```ecmascript 6
     created() {
       // use constants, and use snake case for the actual id string 
        Store.registerPrintableChart(CHART_ID_TOP_AUTHOR_BAR);
        Store.registerPrintableChart(CHART_ID_TOP_COUNTRY_BAR);
     }
     ```
     As you can see, `registerPrintableChart` simply assigns `id` as a key with `included` true by default.We use `Object.assign` because of Vue's change detection caveats for added properties (we want to register charts dynamically at component level).
     ```ecmascript 6
     registerPrintableChart(id, included = true) {
       this.state.charts = Object.assign({}, this.state.charts,
         { [id]: { included } } 
       );
     }
     ```
2. Bind the `included` switch, or any other data, to global state: 
```vue
 <el-switch
      v-model="storeState.charts[CHART_ID_TOP_AUTHOR_BAR].included"
      ...
  />
```
Toggling the switch will automatically modify that info in the global state under chart `id`, allowing `PdfGenerator` to parse that info when needed. 

### Usage at print button level: 
```ecmascript 6
generatePdf() {
  const pdfGenerator = new Utils.PdfGenerator();
  pdfGenerator.generate([CHART_ID_TOP_AUTHOR_BAR, CHART_ID_TOP_COUNTRY_BAR]);
}
```
`PdfGenerator` may be invoked in any component that you need to insert a print button, and can print any set of charts. 

Currently `PdfGenerator` is only used at the `App` level, and is given all `id`'s explicitly. This allows explicit ordering of charts. If it is not given any `id`'s it will automatically iterate through all charts registered in the global state (in no guaranteed order). 

### Notes

- When we bind the global state with `v-model` we are directly mutating state, which is not good practice - however, the code is way simpler this way: we do not have to define a unique computed property with a getter and setter for every single chart's `included` attribute. I tried to do something generic with either `computed` or `methods` but wasn't able to. We would have to do individual computed properties for other data that involve more complicated mutation (such as addition of properties) in the future.
- On a related note, when directly exposing global data in the Vue instance, it is best to declare `Store.state` as opposed to some property such as `Store.state.charts`. This is because that property may rely on Object re-assignment (see `registerPrintableChart`) in order to set new reactive properties. This means upon a new registration, `Store.state.charts` now holds a reference to another object, and will not detect changes made by the any bindings made on the initial `Store.state.charts` data declared. 
- Currently, we avoid storing the caption data, and simply access the caption text in the DOM via `document.getElementById(CHART_ID).nextElementSibling.innerText`. This is a weak assumption but greatly simplifies the process.
- In order to use constants in template we must pass in as data, e.g.
```ecmascript 6
data() {
    return {
      CHART_IDS,
      ...
    },
}
```
And for setting element `id` using data, we must `v-bind:id` or `:id`.
- We use `id` instead of `ref` as we want to be able to call `generate` from any component, not just the component that contains the visualization (since we would access a `ref` element via `this.$refs`). The downside is that if we reuse the component (with same `id`s) only the first one will be retrieved from the DOM. A possible method to use `ref`'s if necessary, might be to pass a reference to the visualization during registration, in `mounted` instead of `created`.  


## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

More details regarding this visualization project will come up once the main components are up.

# Known Bugs 
1. Word cloud does not print.
