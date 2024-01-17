# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from PySide6 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1018, 582)
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setGeometry(QtCore.QRect(0, 0, 371, 581))
        self.CardWidget.setObjectName("CardWidget")
        self.StrongBodyLabel = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel.setGeometry(QtCore.QRect(10, 15, 113, 19))
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.StrongBodyLabel_2 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_2.setGeometry(QtCore.QRect(10, 65, 113, 19))
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.StrongBodyLabel_3 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_3.setGeometry(QtCore.QRect(10, 115, 121, 19))
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.StrongBodyLabel_6 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_6.setGeometry(QtCore.QRect(10, 265, 131, 19))
        self.StrongBodyLabel_6.setObjectName("StrongBodyLabel_6")
        self.StrongBodyLabel_7 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_7.setGeometry(QtCore.QRect(10, 315, 131, 19))
        self.StrongBodyLabel_7.setObjectName("StrongBodyLabel_7")
        self.StrongBodyLabel_16 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_16.setObjectName("Label_Wlan0Mac")
        self.model = LineEdit(self.CardWidget)
        self.model.setGeometry(QtCore.QRect(200, 10, 161, 33))
        self.model.setReadOnly(True)
        self.model.setObjectName("model")
        self.brand = LineEdit(self.CardWidget)
        self.brand.setGeometry(QtCore.QRect(200, 60, 161, 33))
        self.brand.setReadOnly(True)
        self.brand.setObjectName("brand")
        self.android_version = LineEdit(self.CardWidget)
        self.android_version.setGeometry(QtCore.QRect(200, 110, 161, 33))
        self.android_version.setReadOnly(True)
        self.android_version.setObjectName("android_version")
        self.fingerprint = LineEdit(self.CardWidget)
        self.fingerprint.setGeometry(QtCore.QRect(200, 260, 161, 33))
        self.fingerprint.setReadOnly(True)
        self.fingerprint.setObjectName("fingerprint")
        self.ipv4 = LineEdit(self.CardWidget)
        self.ipv4.setGeometry(QtCore.QRect(200, 310, 161, 33))
        self.ipv4.setReadOnly(True)
        self.ipv4.setObjectName("ipv4")
        self.output_prop = LineEdit(self.CardWidget)
        self.output_prop.setGeometry(QtCore.QRect(200, 460, 161, 33))
        self.output_prop.setText("")
        self.output_prop.setReadOnly(True)
        self.output_prop.setObjectName("output_prop")
        self.search_prop = SearchLineEdit(self.CardWidget)
        self.search_prop.setGeometry(QtCore.QRect(10, 460, 171, 33))
        self.search_prop.setObjectName("search_prop")
        self.StrongBodyLabel_8 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_8.setGeometry(QtCore.QRect(10, 165, 131, 19))
        self.StrongBodyLabel_8.setObjectName("StrongBodyLabel_8")
        self.sn = LineEdit(self.CardWidget)
        self.sn.setGeometry(QtCore.QRect(200, 160, 161, 33))
        self.sn.setReadOnly(True)
        self.sn.setObjectName("sn")
        self.mac = LineEdit(self.CardWidget)
        self.mac.setGeometry(QtCore.QRect(200, 210, 161, 33))
        self.mac.setReadOnly(True)
        self.mac.setObjectName("mac")
        self.wlanMac = LineEdit(self.CardWidget)
        self.wlanMac.setReadOnly(True)
        self.wlanMac.setObjectName("wlanMac")
        self.StrongBodyLabel_9 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_9.setGeometry(QtCore.QRect(10, 215, 131, 19))
        self.StrongBodyLabel_9.setObjectName("StrongBodyLabel_9")
        self.StrongBodyLabel_4 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_4.setGeometry(QtCore.QRect(10, 365, 131, 19))
        self.StrongBodyLabel_4.setObjectName("StrongBodyLabel_4")
        self.hw = LineEdit(self.CardWidget)
        self.hw.setGeometry(QtCore.QRect(200, 410, 161, 33))
        self.hw.setReadOnly(True)
        self.hw.setObjectName("hw")
        self.StrongBodyLabel_5 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_5.setGeometry(QtCore.QRect(10, 415, 131, 19))
        self.StrongBodyLabel_5.setObjectName("StrongBodyLabel_5")
        self.sw = LineEdit(self.CardWidget)
        self.sw.setGeometry(QtCore.QRect(200, 360, 161, 33))
        self.sw.setReadOnly(True)
        self.sw.setObjectName("sw")
        self.StrongBodyLabel_17 = StrongBodyLabel(self.CardWidget)
        self.StrongBodyLabel_17.setObjectName("StrongBodyLabel_17")
        self.product = LineEdit(self.CardWidget)
        self.product.setReadOnly(True)
        self.product.setObjectName("product")

        self.button_cmd = PrimaryPushButton(self.CardWidget)
        self.button_cmd.setGeometry(QtCore.QRect(100, 550, 91, 31))
        self.button_cmd.setFixedSize(81, 31)
        self.button_cmd.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
                                      "    color: black;\n"
                                      "    background: rgba(255, 255, 255, 0.7);\n"
                                      "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                      "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                      "    border-radius: 15px;\n"
                                      "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                      "    padding: 5px 12px 6px 12px;\n"
                                      "    font-size: 13px;\n"
                                      "    font-weight:bold;\n"
                                      "    outline: none;\n"
                                      "}\n"
                                      "PushButton[hasIcon=false] {\n"
                                      "    padding: 5px 12px 6px 12px;\n"
                                      "}\n"
                                      "PushButton[hasIcon=true] {\n"
                                      "    padding: 5px 12px 6px 36px;\n"
                                      "}\n"
                                      "PushButton:hover, ToolButton:hover, ToggleButton:hover, ToggleToolButton:hover {\n"
                                      "    background: rgba(249, 249, 249, 0.5);\n"
                                      "}\n"
                                      "PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {\n"
                                      "    color: rgba(0, 0, 0, 0.63);\n"
                                      "    background: rgba(249, 249, 249, 0.3);\n"
                                      "    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
                                      "}\n"
                                      "PushButton:disabled, ToolButton:disabled, ToggleButton:disabled, ToggleToolButton:disabled {\n"
                                      "    color: rgba(0, 0, 0, 0.36);\n"
                                      "    background: rgba(249, 249, 249, 0.3);\n"
                                      "    border: 1px solid rgba(0, 0, 0, 0.06);\n"
                                      "    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
                                      "}\n"
                                      "PrimaryPushButton,\n"
                                      "PrimaryToolButton,\n"
                                      "ToggleButton:checked,\n"
                                      "ToggleToolButton:checked {\n"
                                      "    color: white;\n"
                                      "    background-color: #009faa;\n"
                                      "    border: 1px solid #00a7b3;\n"
                                      "    border-bottom: 1px solid #007780;\n"
                                      "}\n"
                                      "PrimaryPushButton:hover,\n"
                                      "PrimaryToolButton:hover,\n"
                                      "ToggleButton:checked:hover,\n"
                                      "ToggleToolButton:checked:hover {\n"
                                      "    background-color: #00a7b3;\n"
                                      "    border: 1px solid #2daab3;\n"
                                      "    border-bottom: 1px solid #007780;\n"
                                      "}\n"
                                      "PrimaryPushButton:pressed,\n"
                                      "PrimaryToolButton:pressed,\n"
                                      "ToggleButton:checked:pressed,\n"
                                      "ToggleToolButton:checked:pressed {\n"
                                      "    color: rgba(255, 255, 255, 0.63);\n"
                                      "    background-color: #3eabb3;\n"
                                      "    border: 1px solid #3eabb3;\n"
                                      "}\n"
                                      "PrimaryPushButton:disabled,\n"
                                      "PrimaryToolButton:disabled,\n"
                                      "ToggleButton:checked:disabled,\n"
                                      "ToggleToolButton:checked:disabled {\n"
                                      "    color: rgba(255, 255, 255, 0.9);\n"
                                      "    background-color: rgb(205, 205, 205);\n"
                                      "    border: 1px solid rgb(205, 205, 205);\n"
                                      "}")
        self.button_cmd.setObjectName("button_cmd")
        self.button_sign = PrimaryPushButton(self.CardWidget)
        self.button_sign.setGeometry(QtCore.QRect(100, 550, 91, 31))
        self.button_sign.setFixedSize(101, 31)
        self.button_sign.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
                                      "    color: black;\n"
                                      "    background: rgba(255, 255, 255, 0.7);\n"
                                      "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                      "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                      "    border-radius: 15px;\n"
                                      "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                      "    padding: 5px 12px 6px 12px;\n"
                                      "    font-size: 13px;\n"
                                      "    font-weight:bold;\n"
                                      "    outline: none;\n"
                                      "}\n"
                                      "PushButton[hasIcon=false] {\n"
                                      "    padding: 5px 12px 6px 12px;\n"
                                      "}\n"
                                      "PushButton[hasIcon=true] {\n"
                                      "    padding: 5px 12px 6px 36px;\n"
                                      "}\n"
                                      "PushButton:hover, ToolButton:hover, ToggleButton:hover, ToggleToolButton:hover {\n"
                                      "    background: rgba(249, 249, 249, 0.5);\n"
                                      "}\n"
                                      "PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {\n"
                                      "    color: rgba(0, 0, 0, 0.63);\n"
                                      "    background: rgba(249, 249, 249, 0.3);\n"
                                      "    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
                                      "}\n"
                                      "PushButton:disabled, ToolButton:disabled, ToggleButton:disabled, ToggleToolButton:disabled {\n"
                                      "    color: rgba(0, 0, 0, 0.36);\n"
                                      "    background: rgba(249, 249, 249, 0.3);\n"
                                      "    border: 1px solid rgba(0, 0, 0, 0.06);\n"
                                      "    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
                                      "}\n"
                                      "PrimaryPushButton,\n"
                                      "PrimaryToolButton,\n"
                                      "ToggleButton:checked,\n"
                                      "ToggleToolButton:checked {\n"
                                      "    color: white;\n"
                                      "    background-color: #009faa;\n"
                                      "    border: 1px solid #00a7b3;\n"
                                      "    border-bottom: 1px solid #007780;\n"
                                      "}\n"
                                      "PrimaryPushButton:hover,\n"
                                      "PrimaryToolButton:hover,\n"
                                      "ToggleButton:checked:hover,\n"
                                      "ToggleToolButton:checked:hover {\n"
                                      "    background-color: #00a7b3;\n"
                                      "    border: 1px solid #2daab3;\n"
                                      "    border-bottom: 1px solid #007780;\n"
                                      "}\n"
                                      "PrimaryPushButton:pressed,\n"
                                      "PrimaryToolButton:pressed,\n"
                                      "ToggleButton:checked:pressed,\n"
                                      "ToggleToolButton:checked:pressed {\n"
                                      "    color: rgba(255, 255, 255, 0.63);\n"
                                      "    background-color: #3eabb3;\n"
                                      "    border: 1px solid #3eabb3;\n"
                                      "}\n"
                                      "PrimaryPushButton:disabled,\n"
                                      "PrimaryToolButton:disabled,\n"
                                      "ToggleButton:checked:disabled,\n"
                                      "ToggleToolButton:checked:disabled {\n"
                                      "    color: rgba(255, 255, 255, 0.9);\n"
                                      "    background-color: rgb(205, 205, 205);\n"
                                      "    border: 1px solid rgb(205, 205, 205);\n"
                                      "}")
        self.button_sign.setObjectName("button_sign")
        # self.button_remount = PrimaryPushButton(self.CardWidget)
        # self.button_remount.setGeometry(QtCore.QRect(220, 550, 91, 31))
        # self.button_remount.setFixedSize(91, 31)
        # self.button_remount.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
        #                                   "    color: black;\n"
        #                                   "    background: rgba(255, 255, 255, 0.7);\n"
        #                                   "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
        #                                   "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
        #                                   "    border-radius: 15px;\n"
        #                                   "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
        #                                   "    padding: 5px 12px 6px 12px;\n"
        #                                   "    font-size: 13px;\n"
        #                                   "    font-weight:bold;\n"
        #                                   "    outline: none;\n"
        #                                   "}\n"
        #                                   "PushButton[hasIcon=false] {\n"
        #                                   "    padding: 5px 12px 6px 12px;\n"
        #                                   "}\n"
        #                                   "PushButton[hasIcon=true] {\n"
        #                                   "    padding: 5px 12px 6px 36px;\n"
        #                                   "}\n"
        #                                   "PushButton:hover, ToolButton:hover, ToggleButton:hover, ToggleToolButton:hover {\n"
        #                                   "    background: rgba(249, 249, 249, 0.5);\n"
        #                                   "}\n"
        #                                   "PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {\n"
        #                                   "    color: rgba(0, 0, 0, 0.63);\n"
        #                                   "    background: rgba(249, 249, 249, 0.3);\n"
        #                                   "    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
        #                                   "}\n"
        #                                   "PushButton:disabled, ToolButton:disabled, ToggleButton:disabled, ToggleToolButton:disabled {\n"
        #                                   "    color: rgba(0, 0, 0, 0.36);\n"
        #                                   "    background: rgba(249, 249, 249, 0.3);\n"
        #                                   "    border: 1px solid rgba(0, 0, 0, 0.06);\n"
        #                                   "    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
        #                                   "}\n"
        #                                   "PrimaryPushButton,\n"
        #                                   "PrimaryToolButton,\n"
        #                                   "ToggleButton:checked,\n"
        #                                   "ToggleToolButton:checked {\n"
        #                                   "    color: white;\n"
        #                                   "    background-color: #009faa;\n"
        #                                   "    border: 1px solid #00a7b3;\n"
        #                                   "    border-bottom: 1px solid #007780;\n"
        #                                   "}\n"
        #                                   "PrimaryPushButton:hover,\n"
        #                                   "PrimaryToolButton:hover,\n"
        #                                   "ToggleButton:checked:hover,\n"
        #                                   "ToggleToolButton:checked:hover {\n"
        #                                   "    background-color: #00a7b3;\n"
        #                                   "    border: 1px solid #2daab3;\n"
        #                                   "    border-bottom: 1px solid #007780;\n"
        #                                   "}\n"
        #                                   "PrimaryPushButton:pressed,\n"
        #                                   "PrimaryToolButton:pressed,\n"
        #                                   "ToggleButton:checked:pressed,\n"
        #                                   "ToggleToolButton:checked:pressed {\n"
        #                                   "    color: rgba(255, 255, 255, 0.63);\n"
        #                                   "    background-color: #3eabb3;\n"
        #                                   "    border: 1px solid #3eabb3;\n"
        #                                   "}\n"
        #                                   "PrimaryPushButton:disabled,\n"
        #                                   "PrimaryToolButton:disabled,\n"
        #                                   "ToggleButton:checked:disabled,\n"
        #                                   "ToggleToolButton:checked:disabled {\n"
        #                                   "    color: rgba(255, 255, 255, 0.9);\n"
        #                                   "    background-color: rgb(205, 205, 205);\n"
        #                                   "    border: 1px solid rgb(205, 205, 205);\n"
        #                                   "}")
        # self.button_remount.setObjectName("button_remount")
        self.CardWidget_2 = CardWidget(Form)
        self.CardWidget_2.setGeometry(QtCore.QRect(370, 0, 651, 581))
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.StrongBodyLabel_15 = StrongBodyLabel(self.CardWidget_2)
        self.StrongBodyLabel_15.setGeometry(QtCore.QRect(20, 390, 71, 19))
        self.StrongBodyLabel_15.setStyleSheet("font-weight:bold;\n"
                                              "")
        self.StrongBodyLabel_15.setObjectName("StrongBodyLabel_15")
        self.StrongBodyLabel_14 = StrongBodyLabel(self.CardWidget_2)
        self.StrongBodyLabel_14.setGeometry(QtCore.QRect(20, 320, 71, 19))
        self.StrongBodyLabel_14.setStyleSheet("font-weight:bold;\n"
                                              "")
        self.StrongBodyLabel_14.setObjectName("StrongBodyLabel_14")
        self.StrongBodyLabel_13 = StrongBodyLabel(self.CardWidget_2)
        self.StrongBodyLabel_13.setGeometry(QtCore.QRect(20, 250, 71, 19))
        self.StrongBodyLabel_13.setStyleSheet("font-weight:bold;\n"
                                              "")
        self.StrongBodyLabel_13.setObjectName("StrongBodyLabel_13")
        self.StrongBodyLabel_12 = StrongBodyLabel(self.CardWidget_2)
        self.StrongBodyLabel_12.setGeometry(QtCore.QRect(20, 180, 71, 19))
        self.StrongBodyLabel_12.setStyleSheet("font-weight:bold;\n"
                                              "")
        self.StrongBodyLabel_12.setObjectName("StrongBodyLabel_12")
        self.StrongBodyLabel_11 = StrongBodyLabel(self.CardWidget_2)
        self.StrongBodyLabel_11.setGeometry(QtCore.QRect(20, 110, 71, 19))
        self.StrongBodyLabel_11.setStyleSheet("font-weight:bold;\n"
                                              "")
        self.StrongBodyLabel_11.setObjectName("StrongBodyLabel_11")
        self.StrongBodyLabel_10 = StrongBodyLabel(self.CardWidget_2)
        self.StrongBodyLabel_10.setGeometry(QtCore.QRect(20, 40, 71, 19))
        self.StrongBodyLabel_10.setStyleSheet("font-weight:bold;\n"
                                              "")
        self.StrongBodyLabel_10.setObjectName("StrongBodyLabel_10")
        self.show_6 = TextEdit(self.CardWidget_2)
        self.show_6.setGeometry(QtCore.QRect(100, 380, 391, 41))
        self.show_6.setReadOnly(True)
        self.show_6.setObjectName("show_6")
        self.button_refresh = PrimaryPushButton(self.CardWidget_2)
        self.button_refresh.setGeometry(QtCore.QRect(20, 510, 50, 50))
        self.button_refresh.setFixedSize(QtCore.QSize(50, 50))
        self.button_refresh.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
                                          "    color: black;\n"
                                          "    background: rgba(255, 255, 255, 0.7);\n"
                                          "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                          "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                          "    border-radius: 25px;\n"
                                          "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                          "    padding: 5px 12px 6px 12px;\n"
                                          "    font-size:1px;\n"
                                          "    outline: none;\n"
                                          "}\n"
                                          "PushButton[hasIcon=false] {\n"
                                          "    padding: 5px 12px 6px 12px;\n"
                                          "}\n"
                                          "PushButton[hasIcon=true] {\n"
                                          "    padding: 5px 12px 6px 36px;\n"
                                          "}\n"
                                          "PushButton:hover, ToolButton:hover, ToggleButton:hover, ToggleToolButton:hover {\n"
                                          "    background: rgba(249, 249, 249, 0.5);\n"
                                          "}\n"
                                          "PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {\n"
                                          "    color: rgba(0, 0, 0, 0.63);\n"
                                          "    background: rgba(249, 249, 249, 0.3);\n"
                                          "    border-bottom: 1px solid rgba(0, 0, 0, 0.073);\n"
                                          "}\n"
                                          "PushButton:disabled, ToolButton:disabled, ToggleButton:disabled, ToggleToolButton:disabled {\n"
                                          "    color: rgba(0, 0, 0, 0.36);\n"
                                          "    background: rgba(249, 249, 249, 0.3);\n"
                                          "    border: 1px solid rgba(0, 0, 0, 0.06);\n"
                                          "    border-bottom: 1px solid rgba(0, 0, 0, 0.06);\n"
                                          "}\n"
                                          "PrimaryPushButton,\n"
                                          "PrimaryToolButton,\n"
                                          "ToggleButton:checked,\n"
                                          "ToggleToolButton:checked {\n"
                                          "    color: white;\n"
                                          "    background-color: #009faa;\n"
                                          "    border: 1px solid #00a7b3;\n"
                                          "    border-bottom: 1px solid #007780;\n"
                                          "}\n"
                                          "PrimaryPushButton:hover,\n"
                                          "PrimaryToolButton:hover,\n"
                                          "ToggleButton:checked:hover,\n"
                                          "ToggleToolButton:checked:hover {\n"
                                          "    background-color: #00a7b3;\n"
                                          "    border: 1px solid #2daab3;\n"
                                          "    border-bottom: 1px solid #007780;\n"
                                          "}\n"
                                          "PrimaryPushButton:pressed,\n"
                                          "PrimaryToolButton:pressed,\n"
                                          "ToggleButton:checked:pressed,\n"
                                          "ToggleToolButton:checked:pressed {\n"
                                          "    color: rgba(255, 255, 255, 0.63);\n"
                                          "    background-color: #3eabb3;\n"
                                          "    border: 1px solid #3eabb3;\n"
                                          "}\n"
                                          "PrimaryPushButton:disabled,\n"
                                          "PrimaryToolButton:disabled,\n"
                                          "ToggleButton:checked:disabled,\n"
                                          "ToggleToolButton:checked:disabled {\n"
                                          "    color: rgba(255, 255, 255, 0.9);\n"
                                          "    background-color: rgb(205, 205, 205);\n"
                                          "    border: 1px solid rgb(205, 205, 205);\n"
                                          "}")
        self.button_refresh.setText("")
        self.button_refresh.setObjectName("button_refresh")
        self.show_5 = TextEdit(self.CardWidget_2)
        self.show_5.setGeometry(QtCore.QRect(100, 310, 391, 41))
        self.show_5.setReadOnly(True)
        self.show_5.setObjectName("show_5")
        self.show_4 = TextEdit(self.CardWidget_2)
        self.show_4.setGeometry(QtCore.QRect(100, 240, 391, 41))
        self.show_4.setReadOnly(True)
        self.show_4.setObjectName("show_4")
        self.show_1 = TextEdit(self.CardWidget_2)
        self.show_1.setGeometry(QtCore.QRect(100, 30, 391, 41))
        self.show_1.setReadOnly(True)
        self.show_1.setObjectName("show_1")
        self.show_2 = TextEdit(self.CardWidget_2)
        self.show_2.setGeometry(QtCore.QRect(100, 100, 391, 41))
        self.show_2.setReadOnly(True)
        self.show_2.setObjectName("show_2")
        self.show_3 = TextEdit(self.CardWidget_2)
        self.show_3.setGeometry(QtCore.QRect(100, 170, 391, 41))
        self.show_3.setReadOnly(True)
        self.show_3.setObjectName("show_3")

        layout = QHBoxLayout(Form)
        self.CardWidget.setFixedWidth(500)
        subLayout_1 = QVBoxLayout(self.CardWidget)
        vsubLayout = QFormLayout()
        vsubLayout.setContentsMargins(5, 10, 10,5)
        vsubLayout.addRow(self.StrongBodyLabel, self.model)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_17, self.product)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_2, self.brand)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_3, self.android_version)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_8, self.sn)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_9, self.mac)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_16, self.wlanMac)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_6, self.fingerprint)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_7, self.ipv4)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_4, self.sw)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.StrongBodyLabel_5, self.hw)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        vsubLayout.addRow(self.search_prop, self.output_prop)
        vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # vsubLayout.addRow(self.input_text, self.button_input)
        # vsubLayout.setAlignment(self.button_input, Qt.AlignmentFlag.AlignCenter)
        # vsubLayout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        hsubLayout2 = QHBoxLayout()
        hsubLayout2.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        hsubLayout2.addWidget(self.button_cmd)
        hsubLayout2.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        hsubLayout2.addWidget(self.button_sign)
        hsubLayout2.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        hsubLayout2.addWidget(self.button_refresh)
        hsubLayout2.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        # hsubLayout2.addWidget(self.button_remount)
        # hsubLayout2.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        subLayout_1.addLayout(vsubLayout)
        subLayout_1.addLayout(hsubLayout2)
        layout.addWidget(self.CardWidget, 1)

        subLayout_2 = QFormLayout(self.CardWidget_2)
        subLayout_2.addRow(self.StrongBodyLabel_10, self.show_1)
        subLayout_2.addRow(self.StrongBodyLabel_11, self.show_2)
        subLayout_2.addRow(self.StrongBodyLabel_12, self.show_3)
        subLayout_2.addRow(self.StrongBodyLabel_13, self.show_4)
        subLayout_2.addRow(self.StrongBodyLabel_14, self.show_5)
        subLayout_2.addRow(self.StrongBodyLabel_15, self.show_6)
        # subLayout_2.addRow(self.button_refresh)

        layout.addWidget(self.CardWidget_2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.StrongBodyLabel.setText(_translate("Form", "Model"))
        self.StrongBodyLabel_2.setText(_translate("Form", "Brand"))
        self.StrongBodyLabel_3.setText(_translate("Form", "Android Version"))
        self.StrongBodyLabel_6.setText(_translate("Form", "FingerPrint"))
        self.StrongBodyLabel_7.setText(_translate("Form", "Ipv4Address"))
        self.model.setText(_translate("Form", "UnKnown"))
        self.brand.setText(_translate("Form", "UnKnown"))
        self.android_version.setText(_translate("Form", "UnKnown"))
        self.fingerprint.setText(_translate("Form", "UnKnown"))
        self.ipv4.setText(_translate("Form", "UnKnown"))
        self.search_prop.setPlaceholderText(_translate("Form", "Prop"))
        self.StrongBodyLabel_8.setText(_translate("Form", "Serial Number"))
        self.sn.setText(_translate("Form", "UnKnown"))
        self.mac.setText(_translate("Form", "UnKnown"))
        self.StrongBodyLabel_9.setText(_translate("Form", "Eth MAC"))
        self.StrongBodyLabel_4.setText(_translate("Form", "Software Version"))
        self.hw.setText(_translate("Form", "UnKnown"))
        self.StrongBodyLabel_5.setText(_translate("Form", "Hardware Version"))
        self.sw.setText(_translate("Form", "UnKnown"))
        self.button_cmd.setText(_translate("Form", "Shell"))
        self.button_sign.setText(_translate("Form", "Google Sign"))
        self.StrongBodyLabel_16.setText(_translate("Form", "Wlan MAC"))
        self.wlanMac.setText(_translate("Form", "UnKnown"))
        self.StrongBodyLabel_17.setText(_translate("Form", "Product"))
        self.product.setText(_translate("Form", "unKnown"))
        # self.button_remount.setText(_translate("Form", "remount"))
        self.StrongBodyLabel_15.setText(_translate("Form", "活动堆栈："))
        self.StrongBodyLabel_14.setText(_translate("Form", "上次活动："))
        self.StrongBodyLabel_13.setText(_translate("Form", "前台活动："))
        self.StrongBodyLabel_12.setText(_translate("Form", "启动活动："))
        self.StrongBodyLabel_11.setText(_translate("Form", "当前进程："))
        self.StrongBodyLabel_10.setText(_translate("Form", "当前包名："))


from qfluentwidgets import CardWidget, LineEdit, PrimaryPushButton, SearchLineEdit, StrongBodyLabel, TextEdit
