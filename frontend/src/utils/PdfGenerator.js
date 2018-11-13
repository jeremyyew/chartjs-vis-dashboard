import Const from '@/components/Const';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import Store from '@/store';
import utils from '@/utils';

const PDF_FILE_NAME = 'Conference Visualization Report';

export default class PdfGenerator {
  generate(chartIds) {
    this.doc = new jsPDF('p', 'pt');
    this.setPdfParams();
    this.setPdfMainTitle();
    return this.generateDiagramsThenSave(chartIds);
  }

  async generateDiagramsThenSave(ids) {
    this.doc.setFontSize(Const.pdfTextFontSize);
    // For each chart id, get the chart, caption, and check if it is included in global store
    // Assumes that caption div is directly below chart div
    for (const id of ids) {
      if (!Store.state.charts[id]) {
        continue;
      }
      console.log('PRINTING', id);
      await this.elementToCanvas(id,
        Store.state.charts[id].included);
    }
    return this.doc.save(`${this.fileName}.pdf`);
  }

  getParentTab(element){
    const parentTabPane = element.closest(".el-tab-pane");
    return parentTabPane.id.replace(/^pane-+/,"");
  }

  async elementToCanvas(id, included) {
    if (!included) {
      return Promise.resolve('ok');
    }
    var element = document.getElementById(id);
    if (!element) {
      return Promise.resolve('ok');
    }
    await Store.switchActiveTab(this.getParentTab(element));
    let canv = await html2canvas(element);
    let tries = 1;
    while ((tries < 5) && (canv.width === 0 || canv.height === 0)) {
      canv = await html2canvas(element);
      tries += 1;
    }
    console.log(canv);
    if (this.numOfAddedSections % 2 === 0 && this.numOfAddedSections >= 2) {
      this.doc.addPage();
      this.currentMargin = Const.topMargin;
    }
    this.numOfAddedSections += 1;
    const imageData = canv.toDataURL('image/png');
    const imageHeight = canv.height * Const.imageWidth / canv.width;
    this.doc.addImage(imageData, 'PNG', this.leftMargin, this.currentMargin, Const.imageWidth, imageHeight);
    this.currentMargin += imageHeight;

    const caption = document.getElementById(id).nextElementSibling.innerText;
    if (caption) {
      const captionLines = this.doc.splitTextToSize(caption, this.contentWidth);
      this.currentMargin += this.imageCaptionSpacing;
      this.doc.text(
        this.leftMargin,
        this.currentMargin,
        captionLines,
      );
      // Note: here pdfLineHeight is the line height considering the white space between lines
      const captionLinesHeight = Const.pdfLineHeight
        * Const.pdfTextFontSize * captionLines.length;
      this.currentMargin += captionLinesHeight;
    }
    this.currentMargin += 30;
    return Promise.resolve('ok');
  }


  setPdfParams() {
    this.fileName = PDF_FILE_NAME;
    this.leftMargin = Const.leftMargin;
    this.rightMargin = Const.rightMargin;
    this.contentWidth = Const.contentWidth;
    this.initialTopMargin = Const.topMargin;
    this.doc.setFont('Times');
    this.doc.setFontSize(Const.pdfTitleFontSize);
    this.numOfAddedSections = 0;
    this.imageCaptionSpacing = 20;
  }

  setPdfMainTitle() {
    this.title = PDF_FILE_NAME;
    this.titleLength = this.doc.getStringUnitWidth(this.title) * Const.pdfTitleFontSize;
    this.doc.text((this.contentWidth - this.titleLength) / 2.0
      + this.leftMargin, this.initialTopMargin, this.title);
    this.startingTopMargin = this.initialTopMargin + Const.pdfTitleFontSize;
    this.currentMargin = this.startingTopMargin;
  }
}
