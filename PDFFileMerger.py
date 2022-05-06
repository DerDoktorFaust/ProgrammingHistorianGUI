from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from PyPDF4 import PdfFileMerger



class Ui_Dialog(QObject):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(667, 514)
        font = QtGui.QFont()
        font.setPointSize(26)
        Dialog.setFont(font)
        self.title_label = QtWidgets.QLabel(Dialog)
        self.title_label.setGeometry(QtCore.QRect(250, 30, 291, 41))
        self.title_label.setObjectName("label")
        self.merge_button = QtWidgets.QPushButton(Dialog)
        self.merge_button.setGeometry(QtCore.QRect(230, 400, 225, 45))
        self.merge_button.setObjectName("merge_button")
        self.file_list_widget = ListDragWidget(Dialog)
        self.file_list_widget.setGeometry(QtCore.QRect(70, 100, 531, 261))
        self.file_list_widget.setObjectName("file_list_widget")

        self.retranslateUi(Dialog)
        self.merge_button.clicked.connect(self.mergeDocSlot)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_label.setText(_translate("Dialog", "PDF File Merger"))
        self.merge_button.setText(_translate("Dialog", "Merge Files"))

    @pyqtSlot()
    def mergeDocSlot(self):
        output_file_name = 'merged.pdf'  # default name for file output

        if self.file_list_widget.count() > 1:  # no merging unless there are enough documents to merge

            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            output_file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "Save File", "merged", "PDF File (*.pdf)", options=options)

            for i in range(self.file_list_widget.count()):
                if output_file_name + ".pdf" == self.file_list_widget.item(i).text():
                    error_message = QtWidgets.QMessageBox.critical(None, "Error!",
                                                                   "Error! Your file name is already in use!")
                    return

            if output_file_name:  # check to make sure there is a name
                # user's file name won't include .pdf unless they type it in
                output_file_name = output_file_name + '.pdf'

                # create PDF merger object
                pdf_merger = PdfFileMerger(open(output_file_name, "wb"))

                for i in range(self.file_list_widget.count()):
                    # get everything from the file list
                    pdf_merger.append(self.file_list_widget.item(i).text())

                pdf_merger.write(output_file_name)
                pdf_merger.close()

                success_message = QtWidgets.QMessageBox.information(
                    None, "Files Merged", f"{output_file_name} has been successfully written!")



class ListDragWidget(QtWidgets.QListWidget):
    """Creates a list widget that allows user to drag and drop PDF
    files into the widget area to add these files."""
    def __init__(self, parent):
        super(ListDragWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(ListDragWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(ListDragWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for file in event.mimeData().urls():
                if file.path().endswith('.pdf'): # make sure it is a PDF file
                    self.addItem(file.path())
        else:
            super(ListDragWidget, self).dropEvent(event)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
