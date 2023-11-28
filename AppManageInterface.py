from PySide6.QtWidgets import QWidget
from appmanager_ui import *


class AppManageInterface(QWidget):
    def __init__(self, parent=None):
        super(AppManageInterface, self).__init__(parent)
        self.ui = Ui_appManage()
        self.ui.setupUi(self)