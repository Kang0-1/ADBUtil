# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QMovie, QAction
from PySide6.QtWidgets import QWidget, QListView, QLabel

from FileManage.app.core.configurations import Resources
from FileManage.app.gui.explorer.files import FileHeaderWidget
from FileManage.app.gui.explorer.toolbar import PathBar


class Ui_centralwidget(QWidget):

    def setupUi(self, centralwidget):
        centralwidget.setObjectName("FileManager")
        centralwidget.resize(1018, 580)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(centralwidget.sizePolicy().hasHeightForWidth())
        centralwidget.setSizePolicy(sizePolicy)

        self.CardWidget = CardWidget(centralwidget)
        self.CardWidget.setGeometry(QtCore.QRect(0, 0, 1000, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CardWidget.sizePolicy().hasHeightForWidth())
        self.CardWidget.setSizePolicy(sizePolicy)
        self.CardWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.CardWidget.setObjectName("CardWidget_toolbar")

        self.upload_tools = PrimaryDropDownPushButton(self.CardWidget)
        self.upload_tools.setGeometry(QtCore.QRect(30, 10, 70, 40))
        self.upload_tools._menu = RoundMenu(self.upload_tools)
        self.upload_tools.setIcon(QIcon('./resources/icons/upload.png'))
        self.upload_tools.setIconSize(QtCore.QSize(32, 32))
        self.upload_tools.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
                           "    color: black;\n"
                           "    background: rgba(255, 255, 255, 0.7);\n"
                           "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                           "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                           "    border-radius: 10px;\n"
                           "    padding: 5px 12px 6px 12px;\n"
                           "    font-size: 1px;\n"
                           "    outline: none;\n"
                           "}\n"
                           "PushButton[hasIcon=false] {\n"
                           "    padding: 5px 12px 6px 12px;\n"
                           "}\n"
                           "PushButton[hasIcon=true] {\n"
                           "    padding: 2px 12px 6px 50px;\n"
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
                           "ToggleButton:checked:pressed,\n"
                           "ToggleToolButton:checked:pressed {\n"
                           "    color: rgba(255, 255, 255, 0.63);\n"
                           "    background-color: #3eabb3;\n"
                           "    border: 1px solid #3eabb3;\n"
                           "}")
        self.setObjectName("upload_button")
        self.upload_tools.clicked.connect(self.upload_tools._showMenu)
        self.upload_tools._menu.addSection("Upload files")
        self.upload_tools.upload_files = QAction(QIcon('./resources/icons/file.png'), 'Upload files', self)
        self.upload_tools._menu.addAction(self.upload_tools.upload_files)
        self.upload_tools.upload_directory = QAction(QIcon('./resources/icons/folder.png'), 'Upload directory', self)
        self.upload_tools._menu.addAction(self.upload_tools.upload_directory)
        self.upload_tools.setMenu(self.upload_tools._menu)

        self.create_folder_bt = PrimaryPushButton(self.CardWidget)
        self.create_folder_bt.setGeometry(QtCore.QRect(150, 10, 57, 40))
        self.create_folder_bt.setMinimumSize(QtCore.QSize(57, 40))
        self.create_folder_bt.setIcon(QIcon('./resources/icons/create_folder.png'))
        self.create_folder_bt.setIconSize(QtCore.QSize(32, 32))
        self.create_folder_bt.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
                                            "    color: black;\n"
                                            "    background: rgba(255, 255, 255, 0.7);\n"
                                            "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                            "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                            "    border-radius: 10px;\n"
                                            "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                            "    padding: 5px 12px 6px 12px;\n"
                                            "    font-size: 1px;\n"
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
                                            "ToggleButton:checked:pressed,\n"
                                            "ToggleToolButton:checked:pressed {\n"
                                            "    color: rgba(255, 255, 255, 0.63);\n"
                                            "    background-color: #3eabb3;\n"
                                            "    border: 1px solid #3eabb3;\n"
                                            "}")
        self.create_folder_bt.setObjectName("create_folder_button")

        self.parent_dir_bt = PrimaryPushButton(self.CardWidget)
        self.parent_dir_bt.setGeometry(QtCore.QRect(250, 10, 57, 40))
        self.parent_dir_bt.setIcon(QIcon('./resources/icons/back.png'))
        self.parent_dir_bt.setIconSize(QtCore.QSize(30, 30))
        self.parent_dir_bt.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
                                         "    color: black;\n"
                                         "    background: rgba(255, 255, 255, 0.7);\n"
                                         "    border: 1px solid rgba(0, 0, 0, 0.073);\n"
                                         "    border-bottom: 1px solid rgba(0, 0, 0, 0.183);\n"
                                         "    border-radius: 10px;\n"
                                         "    /* font: 14px \'Segoe UI\', \'Microsoft YaHei\'; */\n"
                                         "    padding: 5px 12px 6px 12px;\n"
                                         "    font-size: 1px;\n"
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
                                         "ToggleButton:checked:pressed,\n"
                                         "ToggleToolButton:checked:pressed {\n"
                                         "    color: rgba(255, 255, 255, 0.63);\n"
                                         "    background-color: #3eabb3;\n"
                                         "    border: 1px solid #3eabb3;\n"
                                         "}")
        self.parent_dir_bt.setObjectName("parent_dir_button")

        self.FilePath = PathBar(self.CardWidget)
        self.FilePath.setGeometry(QtCore.QRect(350, 10, 630, 50))
        self.FilePath.setObjectName("FilePath")

        self.header = FileHeaderWidget(centralwidget)
        self.header.setGeometry(QtCore.QRect(20, 70, 1000, 60))

        self.list = QListView(centralwidget)
        self.list.setSpacing(1)
        self.list.installEventFilter(centralwidget)
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self.list.setGeometry(QtCore.QRect(22, 130, 1000, 450))

        self.loading = QLabel(self)
        self.loading.setAlignment(Qt.AlignCenter)
        self.loading_movie = QMovie(Resources.anim_loading, parent=self.loading)
        self.loading_movie.setScaledSize(QSize(48, 48))
        self.loading.setMovie(self.loading_movie)

        self.empty_label = QLabel("Folder is empty", self)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #969696; border: 1px solid #969696")

        self.stateTooltip = None


        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)


    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", "Form"))




from qfluentwidgets import CardWidget, PrimaryPushButton, PrimaryDropDownPushButton, RoundMenu
