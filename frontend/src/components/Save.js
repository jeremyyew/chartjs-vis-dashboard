import Const from './const';

function saveAuthorNew() {
  let fileName = 'Author Submission Visual Analysis';
  var leftMargin = Const.leftMargin;
  var rightMargin = Const.rightMargin;
  var contentWidth = Const.contentWidth;
  var initialTopMargin = Const.topMargin;
  var doc = new jsPDF('p', 'pt');
  var title = "Author Submission Visual Analysis";
  doc.setFont("Times");
  doc.setFontSize(Const.pdfTitleFontSize);
  var titleLength = doc.getStringUnitWidth(title) * Const.pdfTitleFontSize;
  doc.text((contentWidth - titleLength) / 2.0 + leftMargin, initialTopMargin, title);
  var startingTopMargin = initialTopMargin + Const.pdfTitleFontSize;
  doc.setFontSize(Const.pdfTextFontSize);

  var numOfAddedSections = 0;

  html2canvas(document.getElementById('topauthorchart')).then(authorCanvas => {
    var topMarginAfterAuthor = startingTopMargin;
    if (this.authorChartIncluded) {
      numOfAddedSections += 1;
      var authorImageData = authorCanvas.toDataURL("image/png");
      var authorImageWidth = Const.imageWidth;
      var authorImageHeight = authorCanvas.height * authorImageWidth / authorCanvas.width;
      doc.addImage(authorImageData, 'PNG', leftMargin, startingTopMargin, authorImageWidth, authorImageHeight);

      var authorTextLines = doc.splitTextToSize(this.authorText.val, contentWidth);
      doc.text(leftMargin, startingTopMargin + authorImageHeight + 20, authorTextLines);

      // Note: here pdfLineHeight is the line height considering the white space between lines
      var authorTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * authorTextLines.length;
      topMarginAfterAuthor = startingTopMargin + authorImageHeight + authorTextLinesHeight + 30;
    }

    html2canvas(document.getElementById('topcountrychart')).then(countryCanvas => {
      var topMarginAfterCountry = topMarginAfterAuthor;
      if (this.countryChartIncluded) {
        numOfAddedSections += 1;
        var countryImageData = countryCanvas.toDataURL("image/png");
        var countryImageWidth = Const.imageWidth;
        var countryImageHeight = countryCanvas.height * countryImageWidth / countryCanvas.width;
        doc.addImage(countryImageData, 'PNG', leftMargin, topMarginAfterAuthor, countryImageWidth, countryImageHeight);

        var countryTextLines = doc.splitTextToSize(this.countryText.val, contentWidth);
        doc.text(leftMargin, topMarginAfterAuthor + countryImageHeight + 20, countryTextLines);

        if (numOfAddedSections % 2 == 1) {
          var countryTextLinesHeight = Const.pdfLineHeight * Const.pdfTextFontSize * countryTextLines.length;
          topMarginAfterCountry = topMarginAfterAuthor + countryImageHeight + countryTextLinesHeight + 20;

        }
      }

      html2canvas(document.getElementById('topaffiliationchart')).then(affiliationCanvas => {
        if (this.affiliationChartIncluded) {
          if (numOfAddedSections % 2 == 0 && numOfAddedSections > 0) {
            doc.addPage();
            topMarginAfterCountry = Const.topMargin;
          }
          var affiliationImageData = affiliationCanvas.toDataURL("image/png");
          var affiliationImageWidth = Const.imageWidth;
          var affiliationImageHeight = affiliationCanvas.height * affiliationImageWidth / affiliationCanvas.width;
          doc.addImage(affiliationImageData, 'PNG', leftMargin, topMarginAfterCountry, affiliationImageWidth, affiliationImageHeight);

          var affiliationTextLines = doc.splitTextToSize(this.affiliationText.val, contentWidth);
          doc.text(leftMargin, topMarginAfterCountry + affiliationImageHeight + 20, affiliationTextLines);
        }

        doc.save(fileName + '.pdf');
      });

    });

  });

}

export default {
  saveAuthorNew
}
