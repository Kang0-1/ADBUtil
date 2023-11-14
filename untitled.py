# -*- coding: utf-8 -*-
from PySide6 import QtCore, QtWidgets
# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_centralwidget(object):
    def setupUi(self, centralwidget):
        centralwidget.setObjectName("centralwidget")
        centralwidget.resize(607, 539)
        self.CardWidget = CardWidget(centralwidget)
        self.CardWidget.setGeometry(QtCore.QRect(0, 80, 611, 411))
        self.CardWidget.setObjectName("CardWidget")
        self.label = QtWidgets.QLabel(self.CardWidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 601, 411))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.CardWidget_2 = CardWidget(centralwidget)
        self.CardWidget_2.setGeometry(QtCore.QRect(0, 0, 611, 81))
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.combo_device = ComboBox(self.CardWidget_2)
        self.combo_device.setGeometry(QtCore.QRect(250, 10, 161, 31))
        self.combo_device.setObjectName("combo_device")
        self.BodyLabel = BodyLabel(self.CardWidget_2)
        self.BodyLabel.setGeometry(QtCore.QRect(180, 10, 61, 21))
        self.BodyLabel.setProperty("pixelFontSize", 18)
        self.BodyLabel.setObjectName("BodyLabel")
        self.button_start = PrimaryPushButton(self.CardWidget_2)
        self.button_start.setGeometry(QtCore.QRect(480, 20, 101, 31))
        self.button_start.setObjectName("button_start")
        self.flip = CheckBox(self.CardWidget_2)
        self.flip.setGeometry(QtCore.QRect(280, 50, 77, 22))
        self.flip.setObjectName("flip")
        self.button_refresh = PrimaryPushButton(self.CardWidget_2)
        self.button_refresh.setGeometry(QtCore.QRect(20, 20, 91, 31))
        self.button_refresh.setObjectName("button_refresh")
        self.CardWidget_3 = CardWidget(centralwidget)
        self.CardWidget_3.setGeometry(QtCore.QRect(0, 490, 611, 51))
        self.CardWidget_3.setObjectName("CardWidget_3")
        self.button_home = PushButton(self.CardWidget_3)
        self.button_home.setGeometry(QtCore.QRect(160, 10, 102, 32))
        self.button_home.setObjectName("button_home")
        self.button_back = PushButton(self.CardWidget_3)
        self.button_back.setGeometry(QtCore.QRect(310, 10, 102, 32))
        self.button_back.setObjectName("button_back")

        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)

    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", "Form"))
        self.label.setText(_translate("centralwidget", "LOADING"))
        self.BodyLabel.setText(_translate("centralwidget", "Device"))
        self.button_start.setText(_translate("centralwidget", "Start"))
        self.flip.setText(_translate("centralwidget", "Reverse"))
        self.button_refresh.setText(_translate("centralwidget", "Refresh"))
        self.button_home.setText(_translate("centralwidget", "HOME"))
        self.button_back.setText(_translate("centralwidget", "BACK"))
from qfluentwidgets import BodyLabel, CardWidget, CheckBox, ComboBox, PrimaryPushButton, PushButton
