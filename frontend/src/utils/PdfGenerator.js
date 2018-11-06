import Const from '@/components/Const';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import Store from '@/store';
import Utils from '@/utils';

const PDF_FILE_NAME = 'Conference Visualization Report';

export default class PdfGenerator {
  generate(chartIds) {
    this.doc = new jsPDF('p', 'pt');
    this.setPdfParams();
    this.setPdfMainTitle();
    this.generateDiagramsThenSave(chartIds);
  }

  async generateDiagramsThenSave(ids) {
    this.doc.setFontSize(Const.pdfTextFontSize);
    // For each chart id, get the chart, caption, and check if it is included in global store
    // Assumes that caption div is directly below chart div
    for (const id of ids) {
      await this.elementToCanvas(id,
        Store.state.charts[id].included);
    }
    this.doc.save(`${this.fileName}.pdf`);
  }

  async elementToCanvas(id, included) {
    if (!included) {
      return Promise.resolve('ok');
    }
    const canv = await html2canvas(document.getElementById(id));
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
    this.doc.setFont('Calibri');
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
