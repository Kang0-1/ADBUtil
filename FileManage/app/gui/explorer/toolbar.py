# ADB File Explorer
# Copyright (C) 2022  Azat Aldeshov
from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from FileManage.app.core.main import Adb
from FileManage.app.core.managers import Global
from FileManage.app.data.models import MessageData, MessageType
from FileManage.app.data.repositories import FileRepository
from FileManage.app.helpers.tools import AsyncRepositoryWorker, ProgressCallbackHelper
import globals
from qfluentwidgets import PrimaryDropDownPushButton, PrimaryPushButton, LineEdit, RoundMenu


class UploadTools(PrimaryDropDownPushButton):
    def __init__(self, parent):
        super(UploadTools, self).__init__(parent)
        self._menu = RoundMenu(self)
        self.uploader = self.FilesUploader()

        self.setIcon(QIcon('./resources/icons/upload.png'))
        self.setIconSize(QtCore.QSize(32, 32))
        self.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
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
        self.setObjectName("upload_button")
        self.clicked.connect(self._showMenu)

        self._menu.addSection("Upload files")


        upload_files = QAction(QIcon('./resources/icons/file.png'), 'Upload files', self)
        upload_files.triggered.connect(self.__action_upload_files__)
        self._menu.addAction(upload_files)

        upload_directory = QAction(QIcon('./resources/icons/folder.png'), 'Upload directory', self)
        upload_directory.triggered.connect(self.__action_upload_directory__)
        self._menu.addAction(upload_directory)

        # upload_files = QAction(QIcon(Resources.icon_folder_create), '&Create folder', self)
        # upload_files.triggered.connect(self.__action_create_folder__)
        # self.menu.addAction(upload_files)
        self.setMenu(self._menu)

    def __action_upload_files__(self):
        file_names = QFileDialog.getOpenFileNames(self, 'Select files', '~')[0]

        if file_names:
            self.uploader.setup(file_names)
            self.uploader.upload()

    def __action_upload_directory__(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Select directory', '~')

        if dir_name:
            self.uploader.setup([dir_name])
            self.uploader.upload()

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

    class FilesUploader:
        UPLOAD_WORKER_ID = 398

        def __init__(self):
            self.files = []

        def setup(self, files: list):
            self.files = files

        def upload(self, data=None, error=None):
            if self.files:
                helper = ProgressCallbackHelper()
                worker = AsyncRepositoryWorker(
                    worker_id=self.UPLOAD_WORKER_ID,
                    name="Upload",
                    repository_method=FileRepository.upload,
                    response_callback=self.upload,
                    arguments=(helper.progress_callback.emit, self.files.pop())
                )
                if Adb.worker().work(worker):
                    Global().communicate.notification.emit(
                        MessageData(
                            title="Uploading",
                            message_type=MessageType.LOADING_MESSAGE,
                            message_catcher=worker.set_loading_widget
                        )
                    )
                    helper.setup(worker, worker.update_loading_widget)
                    worker.start()
            else:
                Global().communicate.files__refresh.emit()

            if error:
                Global().communicate.notification.emit(
                    MessageData(
                        timeout=15000,
                        title='Upload error',
                        body="<span style='color: red; font-weight: 600'> %s </span>" % error,
                    )
                )
            if data:
                Global().communicate.notification.emit(
                    MessageData(
                        title='Uploaded',
                        timeout=15000,
                        body=data,
                    )
                )


# class ParentButton(PrimaryPushButton):
#     def __init__(self, parent):
#         super(ParentButton, self).__init__(parent)
#
#         # self.action = QAction(QIcon(Resources.icon_back), 'Parent', self)
#         # self.setIconSize(QtCore.QSize(27, 27))
#         # self.action.setShortcut('Escape')
#         # self.action.triggered.connect(
#         #     lambda: Global().communicate.files__refresh.emit() if Adb.worker().check(300) and Adb.manager().up() else ''
#         # )
#         # self.setDefaultAction(self.action)


class PathBar(QWidget):
    def __init__(self, parent: QWidget):
        super(PathBar, self).__init__(parent)
        # self.setLayout(QHBoxLayout(self))

        self.prefix = globals.CURRENT_DEVICE
        self.value = Adb.manager().path()

        self.text = LineEdit(self)
        self.text.installEventFilter(self)
        self.text.setGeometry(QtCore.QRect(0, 0, 420, 45))
        self.text.setMaximumSize(QtCore.QSize(430, 40))
        self.text.setText(self.prefix + self.value)
        self.text.textEdited.connect(self._update)
        self.text.returnPressed.connect(self._action)
        # self.layout().addWidget(self.text)

        self.go = PrimaryPushButton(self)
        self.go.setIcon(QIcon('./resources/icons/go.png'))
        self.go.setGeometry(QtCore.QRect(450, 0, 57, 40))
        self.go.setMaximumSize(QtCore.QSize(57, 40))
        self.go.setIconSize(QtCore.QSize(30, 30))
        self.go.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
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
        self.go.clicked.connect(self._action)
        # self.layout().addWidget(self.go)

        self.refresh = PrimaryPushButton(self)
        self.refresh.setIcon(QIcon('./resources/icons/refresh.png'))
        self.refresh.setGeometry(QtCore.QRect(550, 0, 57, 40))
        self.refresh.setMinimumSize(QtCore.QSize(52, 40))
        self.refresh.setIconSize(QtCore.QSize(32, 32))
        self.refresh.setStyleSheet("PushButton, ToolButton, ToggleButton, ToggleToolButton {\n"
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
        self.refresh.clicked.connect(self._refresh)
        # self.layout().addWidget(self.refresh)

        # self.layout().setContentsMargins(0, 0, 0, 0)
        Global().communicate.path_toolbar__refresh.connect(self._clear)

    def eventFilter(self, obj: 'QObject', event: 'QEvent') -> bool:
        if obj == self.text and event.type() == QEvent.FocusIn:
            self.text.setText(self.value)
        elif obj == self.text and event.type() == QEvent.FocusOut:
            self.text.setText(self.prefix + self.value)
        return super(PathBar, self).eventFilter(obj, event)

    def _clear(self):
        self.value = Adb.manager().path()
        self.text.setText(self.prefix + self.value)

    def _update(self, text: str):
        self.value = text

    def _refresh(self, device_serial):
        self.prefix = device_serial
        if self.prefix.__len__() > 0:
            if Adb.manager().set_device(Device(id=self.prefix, name=self.prefix, type="device")):
                Global().communicate.files__refresh.emit()
            else:
                Global().communicate.notification.emit(
                    MessageData(
                        title='Device',
                        timeout=10000,
                        body="Could not open the device %s" % Adb.manager().get_device().name
                    )
                )
        self.value = Adb.manager().path()
        self.text.setText(self.prefix + self.value)

    def _action(self):
        self.text.clearFocus()
        file, error = FileRepository.file(self.value)
        if error:
            Global().communicate.path_toolbar__refresh.emit()
            Global().communicate.notification.emit(
                MessageData(
                    timeout=10000,
                    title="Opening folder",
                    body="<span style='color: red; font-weight: 600'> %s </span>" % error,
                )
            )
        elif file and Adb.manager().go(file):
            Global().communicate.files__refresh.emit()
        else:
            Global().communicate.path_toolbar__refresh.emit()
            Global().communicate.notification.emit(
                MessageData(
                    timeout=10000,
                    title="Opening folder",
                    body="<span style='color: red; font-weight: 600'> Cannot open location </span>",
                )
            )

class Device:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.type = kwargs.get("type")