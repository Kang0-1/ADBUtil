import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QModelIndex, QPoint, QEvent
from PySide6.QtGui import QKeySequence, QAction, QIcon, QPixmap, QCursor
from PySide6.QtWidgets import QWidget, QInputDialog, QMessageBox, QFileDialog
from qfluentwidgets import InfoBar, InfoBarPosition, RoundMenu, Dialog, StateToolTip

from FileInterface_ui import Ui_centralwidget
from FileManage.app.core.main import Adb
from FileManage.app.core.managers import Global
from FileManage.app.data.models import MessageData, FileType, MessageType
from FileManage.app.data.repositories import FileRepository
from FileManage.app.gui.explorer.files import FileListModel, FileItemDelegate, TextView
from FileManage.app.helpers.tools import AsyncRepositoryWorker, ProgressCallbackHelper


class FileInterface(QWidget):
    FILES_WORKER_ID = 300
    DOWNLOAD_WORKER_ID = 399
    UPLOAD_WORKER_ID = 398
    DELETE_WORKER_ID = 301

    def __init__(self, parent=None):
        super(FileInterface, self).__init__(parent)
        self.ui = Ui_centralwidget()
        self.ui.setupUi(self)
        self.ui.upload_tools.upload_files.triggered.connect(self.__action_upload_files__)
        self.ui.upload_tools.upload_directory.triggered.connect(self.__action_upload_directory__)
        self.ui.create_folder_bt.clicked.connect(self.__action_create_folder__)
        self.ui.parent_dir_bt.clicked.connect(
            lambda: Global().communicate.files__refresh.emit() if Adb.worker().check(300) and Adb.manager().up() else ''
        )
        self.model = FileListModel(self.ui.list)
        self.ui.list.setModel(self.model)
        self.ui.list.doubleClicked.connect(self.open)
        self.ui.list.setItemDelegate(FileItemDelegate(self.ui.list))
        self.ui.list.customContextMenuRequested.connect(self.context_menu)
        self.setAcceptDrops(True)

        Global().communicate.files__refresh.connect(self.update)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.isfile(file_path):
                self.setup([file_path])
                self.upload()
            elif os.path.isdir(file_path):
                self.setup([file_path])
                self.upload()

    def __action_upload_directory__(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Select directory', '~')
        print(dir_name)
        if dir_name:
            self.setup([dir_name])
            self.upload()

    def __action_upload_files__(self):
        file_names = QFileDialog.getOpenFileNames(self, 'Select files', '~')[0]
        print(file_names)

        if file_names:
            self.setup(file_names)
            self.upload()

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

        action_rename = QAction(QIcon(':/resources/icons/rename.png'), 'Rename', self)
        action_rename.triggered.connect(self.rename)
        menu.addAction(action_rename)

        action_open_file = QAction(QIcon(':/resources/icons/open.png'), 'Open', self)
        action_open_file.triggered.connect(self.open_file)
        menu.addAction(action_open_file)

        action_delete = QAction(QIcon(':/resources/icons/delete.png'), 'Delete', self)
        action_delete.triggered.connect(self.delete)
        menu.addAction(action_delete)

        action_download = QAction(QIcon(':/resources/icons/download.png'), 'Download', self)
        action_download.triggered.connect(self.download_files)
        menu.addAction(action_download)

        action_download_to = QAction(QIcon(':/resources/icons/download.png'), 'Download to...', self)
        action_download_to.triggered.connect(self.download_to)
        menu.addAction(action_download_to)

        menu.addSeparator()

        action_properties = QAction(QIcon(':/resources/icons/properties.png'), 'Properties', self)
        action_properties.triggered.connect(self.file_properties)
        menu.addAction(action_properties)
        self.setFocus()
        pos = QCursor.pos()
        menu.popup(pos)

    def __action_create_folder__(self):
        text, ok = QInputDialog.getText(self, 'New folder', 'Enter new folder name:')

        if ok and text:
            data, error = FileRepository.new_folder(text)
            if error:
                self.show_info_bar("创建文件夹失败", "error")
            if data:
                self.show_info_bar("创建文件夹成功","success")
            Global().communicate.files__refresh.emit()

    @property
    def file(self):
        if self.ui.list and self.ui.list.currentIndex():
            return self.model.items[self.ui.list.currentIndex().row()]

    @property
    def files(self):
        if self.ui.list and len(self.ui.list.selectedIndexes()) > 0:
            return map(lambda index: self.model.items[index.row()], self.ui.list.selectedIndexes())

    def update(self):
        super(FileInterface, self).update()
        worker = AsyncRepositoryWorker(
            name="Files",
            worker_id=self.FILES_WORKER_ID,
            repository_method=FileRepository.files,
            response_callback=self._async_response,
            arguments=()
        )
        if Adb.worker().work(worker):
            self.model.clear()
            self.ui.list.setHidden(True)
            self.ui.loading.setHidden(False)
            self.ui.empty_label.setHidden(True)
            self.ui.loading_movie.start()

            worker.start()
            Global().communicate.path_toolbar__refresh.emit()

    def close(self) -> bool:
        Global().communicate.files__refresh.disconnect()
        return super(FileInterface, self).close()

    def _async_response(self, files: list, error: str):
        self.ui.loading_movie.stop()
        self.ui.loading.setHidden(True)

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
            self.ui.empty_label.setHidden(False)
        else:
            self.ui.list.setHidden(False)
            self.model.populate(files)
            self.ui.list.setFocus()

    def eventFilter(self, obj: 'QObject', event: 'QEvent') -> bool:
        if obj == self.ui.list and \
                event.type() == QEvent.KeyPress and \
                event.matches(QKeySequence.InsertParagraphSeparator) and \
                not self.ui.list.isPersistentEditorOpen(self.ui.list.currentIndex()):
            self.open(self.ui.list.currentIndex())
        return super(FileInterface, self).eventFilter(obj, event)

    def default_response(self, data, error):
        self.close_state_info()
        if error:
            self.show_info_bar("文件下载失败", "error")
        else:
            self.show_info_bar("文件下载成功，下载路径为" + str(data), "success")

    def delete_response(self, data, error):
        Global.communicate.files__refresh.emit()
        if error:
            self.show_info_bar("文件删除失败", "error")
        else:
            self.show_info_bar("文件删除成功", "success")

    def rename(self):
        self.ui.list.edit(self.ui.list.currentIndex())

    def open_file(self):
        # QDesktopServices.openUrl(QUrl.fromLocalFile("downloaded_path")) open via external app
        if self.file.isdir:
            if Adb.manager().open(self.file):
                Global().communicate.files__refresh.emit()
        if not self.file.isdir:
            data, error = FileRepository.open_file(self.file)
            if error:
                self.show_info_bar("文件打开错误", "error")
            else:
                self.text_view_window = TextView(self.file.name, data)
                self.text_view_window.show()

    def delete(self):
        file_names = ', '.join(map(lambda f: f.name, self.files))
        print(file_names)
        w = Dialog('Delete', "确认删除吗？( %s)" % file_names)
        if w.exec():
            for file in self.files:
                print(file)
                helper = ProgressCallbackHelper()
                worker = AsyncRepositoryWorker(
                    worker_id=self.DOWNLOAD_WORKER_ID,
                    name="Delete",
                    repository_method=FileRepository.delete,
                    response_callback=self.delete_response,
                    arguments=(helper.progress_callback.emit, file)
                )
                if Adb.worker().work(worker):
                    helper.setup(worker, worker.update_loading_widget)
                    worker.start()


    def download_to(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Download to', '~')
        if dir_name:
            self.download_files(dir_name)

    def download_files(self, destination: str = None):
        print(destination)
        if not destination:
            folder_name = f"AdbUtilFiles/Download/"
            desktop_path = Path(
                os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) / folder_name
            desktop_path.mkdir(parents=True, exist_ok=True)
            destination = desktop_path
            print(destination)
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
                self.show_state_info("正在下载文件···")
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
            QPixmap(self.model.icon_path(self.ui.list.currentIndex())).scaled(120, 120, Qt.KeepAspectRatio)
        )
        properties.setWindowTitle('Properties')
        properties.setInformativeText(info)
        properties.exec_()

    def upload_response(self, data, error):
        Global().communicate.files__refresh.emit()
        self.close_state_info()
        if error:
            self.show_info_bar("文件上传失败", "error")
        else:
            self.show_info_bar("文件上传成功", "success")

    def show_info_bar(self, message, type):
        if type == "info":
            InfoBar.info("Info", message, self, True, 3000, InfoBarPosition.BOTTOM, self).show()
        elif type == "success":
            InfoBar.success("Success", message, self, True, 3000, InfoBarPosition.BOTTOM, self).show()
        elif type == "warning":
            InfoBar.warning("Warning", message, self, True, 3000, InfoBarPosition.BOTTOM, self).show()
        elif type == "error":
            InfoBar.error("Error", message, self, True, 3000, InfoBarPosition.BOTTOM, self).show()
        else:
            print("未知的信息类型")

    def show_state_info(self, message):
        self.ui.stateTooltip = StateToolTip(message, "请等待~", self)
        self.ui.stateTooltip.move(880, 10)
        self.ui.stateTooltip.show()

    def close_state_info(self):
        if self.ui.stateTooltip:
            self.ui.stateTooltip.setState(True)
            self.ui.stateTooltip = None

    def setup(self, files: list):
        self.upload_files = []
        self.upload_files = files

    def upload(self):
        if self.upload_files:
            helper = ProgressCallbackHelper()
            worker = AsyncRepositoryWorker(
                worker_id=self.UPLOAD_WORKER_ID,
                name="Upload",
                repository_method=FileRepository.upload,
                response_callback=self.upload_response,
                arguments=(helper.progress_callback.emit, self.upload_files.pop())
            )
            if Adb.worker().work(worker):
                self.show_state_info("正在上传文件···")
                worker.start()
            Global().communicate.files__refresh.emit()
