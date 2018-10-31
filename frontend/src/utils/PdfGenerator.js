import Const from '@/components/Const';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const PDF_FILE_NAME = 'Conference Visualization Report';

export default class PdfGenerator {
  constructor(sections) {
    this.doc = new jsPDF('p', 'pt');
    this.setPdfParams();
    this.setPdfMainTitle();
    // collect ids, callbacks and section titles of all diagrams
    this.generateDiagramsThenSave(sections);
  }

  async generateDiagramsThenSave(sections) {
    this.doc.setFontSize(Const.pdfTextFontSize);
    for (const section of sections) {
      await this.elementToCanvas(section.id, section.caption);
    }
    this.doc.save(`${this.fileName}.pdf`);
  }

  async elementToCanvas(id, caption) {
    const canv = await html2canvas(document.getElementById(id));
    if (this.numOfAddedSections % 2 === 0 && this.numOfAddedSections >= 2) {
      this.doc.addPage();
      this.currentMargin = Const.topMargin;
    }
    this.numOfAddedSections += 1;
    const imageData = canv.toDataURL('image/png');
    const imageHeight = canv.height * Const.imageWidth / canv.width;
    this.doc.addImage(imageData, 'PNG', this.leftMargin, this.currentMargin, Const.imageWidth, imageHeight);
    const captionLines = this.doc.splitTextToSize(caption, this.contentWidth);
    this.doc.text(
      this.leftMargin,
      this.currentMargin + imageHeight + this.imageCaptionSpacing,
      captionLines,
    );
    // Note: here pdfLineHeight is the line height considering the white space between lines
    const captionLinesHeight = Const.pdfLineHeight
      * Const.pdfTextFontSize * captionLines.length;
    this.currentMargin += imageHeight + captionLinesHeight + 30;
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
