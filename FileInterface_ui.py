# -*- coding: utf-8 -*-
import sys

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QModelIndex, QPoint, QEvent, QSize, Slot
from PySide6.QtGui import QKeySequence, QAction, QIcon, QPixmap, QMovie, QCursor
from PySide6.QtWidgets import QWidget, QListView, QMenu, QInputDialog, QMessageBox, QFileDialog, QLabel

from FileManage.app.core.configurations import Resources
from FileManage.app.core.main import Adb
from FileManage.app.core.managers import Global
from FileManage.app.data.models import MessageData, FileType, MessageType
from FileManage.app.data.repositories import FileRepository
from FileManage.app.gui.explorer.files import FileListModel, FileHeaderWidget, FileItemDelegate, TextView
from FileManage.app.gui.explorer.toolbar import UploadTools, PathBar
from FileManage.app.helpers.tools import AsyncRepositoryWorker, ProgressCallbackHelper


class Ui_centralwidget(QWidget):
    FILES_WORKER_ID = 300
    DOWNLOAD_WORKER_ID = 399

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

        self.upload_tools = UploadTools(self.CardWidget)
        self.upload_tools.setGeometry(QtCore.QRect(30, 10, 78, 40))
        self.upload_tools.setObjectName("Upload")

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
        self.create_folder_bt.clicked.connect(self.__action_create_folder__)

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
        self.parent_dir_bt.clicked.connect(
            lambda: Global().communicate.files__refresh.emit() if Adb.worker().check(300) and Adb.manager().up() else ''
        )

        self.FilePath = PathBar(self.CardWidget)
        self.FilePath.setGeometry(QtCore.QRect(350, 10, 630, 50))
        self.FilePath.setObjectName("FilePath")

        self.header = FileHeaderWidget(centralwidget)
        self.header.setGeometry(QtCore.QRect(20, 70, 1000, 60))

        self.list = QListView(centralwidget)
        self.model = FileListModel(self.list)

        # self.list.setSpacing(1)
        self.list.setModel(self.model)
        self.list.installEventFilter(centralwidget)
        self.list.doubleClicked.connect(self.open)
        self.list.setItemDelegate(FileItemDelegate(self.list))
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.context_menu)
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

        Global().communicate.files__refresh.connect(self.update)

        self.retranslateUi(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(centralwidget)

    @property
    def file(self):
        if self.list and self.list.currentIndex():
            return self.model.items[self.list.currentIndex().row()]

    @property
    def files(self):
        if self.list and len(self.list.selectedIndexes()) > 0:
            return map(lambda index: self.model.items[index.row()], self.list.selectedIndexes())

    def update(self):
        super(Ui_centralwidget, self).update()
        worker = AsyncRepositoryWorker(
            name="Files",
            worker_id=self.FILES_WORKER_ID,
            repository_method=FileRepository.files,
            response_callback=self._async_response,
            arguments=()
        )
        if Adb.worker().work(worker):
            # First Setup loading view
            self.model.clear()
            self.list.setHidden(True)
            self.loading.setHidden(False)
            self.empty_label.setHidden(True)
            self.loading_movie.start()

            # Then start async worker
            worker.start()
            Global().communicate.path_toolbar__refresh.emit()

    def close(self) -> bool:
        Global().communicate.files__refresh.disconnect()
        return super(Ui_centralwidget, self).close()

    def _async_response(self, files: list, error: str):
        self.loading_movie.stop()
        self.loading.setHidden(True)

        if error:
            print(error, file=sys.stderr)
            if not files:
                Global().communicate.notification.emit(
                    MessageData(
                        title='Files',
                        timeout=15000,
                        body="<span style='color: red; font-weight: 600'> %s </span>" % error
                    )
                )
        if not files:
            self.empty_label.setHidden(False)
        else:
            self.list.setHidden(False)
            self.model.populate(files)
            self.list.setFocus()

    def eventFilter(self, obj: 'QObject', event: 'QEvent') -> bool:
        if obj == self.list and \
                event.type() == QEvent.KeyPress and \
                event.matches(QKeySequence.InsertParagraphSeparator) and \
                not self.list.isPersistentEditorOpen(self.list.currentIndex()):
            self.open(self.list.currentIndex())
        return super(Ui_centralwidget, self).eventFilter(obj, event)

    def open(self, index: QModelIndex = ...):
        if Adb.manager().open(self.model.items[index.row()]):
            Global().communicate.files__refresh.emit()

    def context_menu(self, pos: QPoint):
        menu = RoundMenu()
        menu.addSection("Actions")

        # action_copy = QAction(QIcon('./resources/icons/copy.png'), 'Copy to...', self)
        # action_copy.setDisabled(True)
        # menu.addAction(action_copy)
        #
        # action_move = QAction(QIcon('./resources/icons/move.png'), 'Move to...', self)
        # action_move.setDisabled(True)
        # menu.addAction(action_move)

        action_rename = QAction(QIcon('./resources/icons/rename.png'), 'Rename', self)
        action_rename.triggered.connect(self.rename)
        menu.addAction(action_rename)

        action_open_file = QAction(QIcon('./resources/icons/open.png'), 'Open', self)
        action_open_file.triggered.connect(self.open_file)
        menu.addAction(action_open_file)

        action_delete = QAction(QIcon('./resources/icons/delete.png'), 'Delete', self)
        action_delete.triggered.connect(self.delete)
        menu.addAction(action_delete)

        action_download = QAction(QIcon('./resources/icons/download.png'), 'Download', self)
        action_download.triggered.connect(self.download_files)
        menu.addAction(action_download)

        action_download_to = QAction(QIcon('./resources/icons/download.png'), 'Download to...', self)
        action_download_to.triggered.connect(self.download_to)
        menu.addAction(action_download_to)

        menu.addSeparator()

        action_properties = QAction(QIcon('./resources/icons/properties.png'), 'Properties', self)
        action_properties.triggered.connect(self.file_properties)
        menu.addAction(action_properties)
        self.setFocus()
        pos = QCursor.pos()
        menu.popup(pos)

    @staticmethod
    def default_response(data, error):
        if error:
            InfoBar.error("Error", "文件下载失败", Qt.Horizontal, True, 2000, InfoBarPosition.BOTTOM).show()
        else:
            InfoBar.success("Success", "文件下载成功", Qt.Horizontal, True, 2000, InfoBarPosition.BOTTOM).show()

    def rename(self):
        self.list.edit(self.list.currentIndex())

    def open_file(self):
        # QDesktopServices.openUrl(QUrl.fromLocalFile("downloaded_path")) open via external app
        if self.file.isdir:
            if Adb.manager().open(self.file):
                Global().communicate.files__refresh.emit()
        if not self.file.isdir:
            data, error = FileRepository.open_file(self.file)
            if error:
                Global().communicate.notification.emit(
                    MessageData(
                        title='File',
                        timeout=15000,
                        body="<span style='color: red; font-weight: 600'> %s </span>" % error
                    )
                )
            else:
                self.text_view_window = TextView(self.file.name, data)
                self.text_view_window.show()

    def delete(self):
        file_names = ', '.join(map(lambda f: f.name, self.files))
        w = Dialog(
            'Delete',
            "确认删除吗？( %s)" % file_names
        )
        if w.exec():
            for file in self.files:
                data, error = FileRepository.delete(file)
                if error:
                    InfoBar.error("Error", "文件删除失败", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
                else:
                    InfoBar.success("Success", "文件删除成功", self, True, 2000, InfoBarPosition.BOTTOM, self).show()

            Global.communicate.files__refresh.emit()

    def download_to(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Download to', '~')
        if dir_name:
            self.download_files(dir_name)

    def download_files(self, destination: str = None):
        for file in self.files:
            helper = ProgressCallbackHelper()
            worker = AsyncRepositoryWorker(
                worker_id=self.DOWNLOAD_WORKER_ID,
                name="Download",
                repository_method=FileRepository.download,
                response_callback=self.default_response,
                arguments=(
                    helper.progress_callback.emit, file.path, destination
                )
            )
            if Adb.worker().work(worker):
                Global().communicate.notification.emit(
                    MessageData(
                        title="Downloading to",
                        message_type=MessageType.LOADING_MESSAGE,
                        message_catcher=worker.set_loading_widget
                    )
                )
                helper.setup(worker, worker.update_loading_widget)
                worker.start()

    def file_properties(self):
        file, error = FileRepository.file(self.file.path)
        file = file if file else self.file

        if error:
            Global().communicate.notification.emit(
                MessageData(
                    timeout=10000,
                    title="Opening folder",
                    body="<span style='color: red; font-weight: 600'> %s </span>" % error,
                )
            )

        info = "<br/><u><b>%s</b></u><br/>" % str(file)
        info += "<pre>Name:        %s</pre>" % file.name or '-'
        info += "<pre>Owner:       %s</pre>" % file.owner or '-'
        info += "<pre>Group:       %s</pre>" % file.group or '-'
        info += "<pre>Size:        %s</pre>" % file.raw_size or '-'
        info += "<pre>Permissions: %s</pre>" % file.permissions or '-'
        info += "<pre>Date:        %s</pre>" % file.raw_date or '-'
        info += "<pre>Type:        %s</pre>" % file.type or '-'

        if file.type == FileType.LINK:
            info += "<pre>Links to:    %s</pre>" % file.link or '-'

        properties = QMessageBox(self)
        properties.setStyleSheet("background-color: #DDDDDD; font-style: 'Microsoft YaHei';")
        properties.setIconPixmap(
            QPixmap(self.model.icon_path(self.list.currentIndex())).scaled(120, 120, Qt.KeepAspectRatio)
        )
        properties.setWindowTitle('Properties')
        properties.setInformativeText(info)
        properties.exec_()

    def __action_create_folder__(self):
        text, ok = QInputDialog.getText(self, 'New folder', 'Enter new folder name:')

        if ok and text:
            data, error = FileRepository.new_folder(text)
            if error:
                Global().communicate.notification.emit(
                    MessageData(
                        timeout=15000,
                        title="Creating folder",
                        body="<span style='color: red; font-weight: 600'> %s </span>" % error,
                    )
                )
            if data:
                Global().communicate.notification.emit(
                    MessageData(
                        title="Creating folder",
                        timeout=15000,
                        body=data,
                    )
                )
            Global().communicate.files__refresh.emit()

    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", "Form"))


from qfluentwidgets import CardWidget, PrimaryPushButton, RoundMenu, Dialog, InfoBar, InfoBarPosition
