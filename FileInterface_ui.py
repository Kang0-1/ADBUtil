# -*- coding: utf-8 -*-
import Resources
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QToolButton

from toolbar import UploadTools, ParentButton, PathBar



class Ui_centralwidget(QWidget):
    def setupUi(self, centralwidget):
        centralwidget.setObjectName("FileManager")
        centralwidget.resize(800, 600)
        self.CardWidget = CardWidget(centralwidget)
        self.CardWidget.setGeometry(QtCore.QRect(0, 0, 800, 60))
        self.CardWidget.setObjectName("CardWidget")

        self.upload_tools = UploadTools(centralwidget)
        self.upload_tools.setGeometry(QtCore.QRect(30, 10, 100, 31))
        self.upload_tools.setObjectName("Upload")

        self.parent_directory = ParentButton(centralwidget)
        self.parent_directory.setGeometry(QtCore.QRect(160, 10, 91, 31))
        self.parent_directory.setObjectName("Parent_Directory")

        self.FilePath = PathBar(centralwidget)
        self.FilePath.setGeometry(QtCore.QRect(270, 10, 371, 31))
        self.FilePath.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.FilePath.setObjectName("FilePath")



        self.line = QtWidgets.QFrame(centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 50, 800, 16))
        self.line.setLineWidth(3)
        self.line.setObjectName("line")

        self.TreeWidget = TreeWidget(centralwidget)
        self.TreeWidget.setGeometry(QtCore.QRect(20, 70, 761, 441))
        self.TreeWidget.setObjectName("TreeWidget")
        self.TreeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.TreeWidget.headerItem().setFont(0, font)
        self.TreeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.TreeWidget.headerItem().setFont(1, font)
        self.TreeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.TreeWidget.headerItem().setFont(2, font)
        self.TreeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.TreeWidget.headerItem().setFont(3, font)

        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)

    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", "Form"))
        self.upload_tools.setText(_translate("centralwidget", "Upload"))
        self.parent_directory.setText(_translate("centralwidget", "Parent Directory"))
        self.TreeWidget.headerItem().setText(0, _translate("centralwidget", "File"))
        self.TreeWidget.headerItem().setText(1, _translate("centralwidget", "Permission"))
        self.TreeWidget.headerItem().setText(2, _translate("centralwidget", "Size"))
        self.TreeWidget.headerItem().setText(3, _translate("centralwidget", "Date"))


from qfluentwidgets import CardWidget, LineEdit, PrimaryDropDownPushButton, PrimaryPushButton, TreeWidget
