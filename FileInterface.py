from PySide6.QtWidgets import QWidget, QMessageBox, QApplication
from FileInterface_ui import Ui_centralwidget


class FileInterface(QWidget):
    def __init__(self, parent=None):
        super(FileInterface, self).__init__(parent)
        self.ui = Ui_centralwidget()
        self.ui.setupUi(self)
