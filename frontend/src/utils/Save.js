import Const from '@/components/Const';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const PDF_FILE_NAME = 'Conference Visualization Report';

class PDFGenerator {
  constructor(sections) {
    this.doc = new jsPDF('p', 'pt');
    this.setPdfParams();
    this.setPdfMainTitle();

    // collect ids, callbacks and section titles of all diagrams
  }

  elementToCanvas(id, text) {

  }

  saveAll() {
    const lines = doc.splitTextToSize(this.authorText.val, (pdfInMM - leftMargin - rightMargin));
    doc.text(leftMargin, 20, lines);
    html2canvas(document.getElementById('testpdf'))
      .then((canvas) => {
        const imageData = canvas.toDataURL('image/png');
        doc.addImage(imageData, 'PNG', 15, 50, canvas.width / 8, canvas.height / 8);
        doc.save(`${fileName}.pdf`);
      });
  }

  setPdfParams() {
    this.fileName = PDF_FILE_NAME;
    this.leftMargin = Const.leftMargin;
    this.rightMargin = Const.rightMargin;
    this.contentWidth = Const.contentWidth;
    this.initialTopMargin = Const.topMargin;
    this.pdfInMM = 210;
    this.doc.setFont('Times');
    this.doc.setFontSize(Const.pdfTitleFontSize);
    this.startingTopMargin = this.initialTopMargin + Const.pdfTitleFontSize;
    this.numOfAddedSections = 0;
  }

  setPdfMainTitle() {
    this.title = PDF_FILE_NAME;
    this.titleLength = this.doc.getStringUnitWidth(this.title) * Const.pdfTitleFontSize;
    this.doc.text((this.contentWidth - this.titleLength) / 2.0
      + this.leftMargin, this.initialTopMargin, this.title);
  }
}


export default {
  PDFGenerator,
};
