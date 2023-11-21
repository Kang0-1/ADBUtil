# -*- coding: utf-8 -*-
import sys

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QModelIndex, QPoint, QEvent
from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import QWidget, QListView, QMenu

from FileManage.app.core.main import Adb
from FileManage.app.core.managers import Global
from FileManage.app.data.models import MessageData
from FileManage.app.data.repositories import FileRepository
from FileManage.app.gui.explorer.files import FileListModel, FileHeaderWidget, FileItemDelegate
from FileManage.app.gui.explorer.toolbar import UploadTools, ParentButton, PathBar
from FileManage.app.helpers.tools import AsyncRepositoryWorker


class Ui_centralwidget(QWidget):
    FILES_WORKER_ID = 300
    DOWNLOAD_WORKER_ID = 399

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

        # self.TreeWidget = TreeWidget(centralwidget)
        # self.TreeWidget.setGeometry(QtCore.QRect(20, 70, 761, 441))
        # self.TreeWidget.setObjectName("TreeWidget")
        # self.TreeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignmentFlag.AlignCenter)
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # self.TreeWidget.headerItem().setFont(0, font)
        # self.TreeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignmentFlag.AlignCenter)
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # self.TreeWidget.headerItem().setFont(1, font)
        # self.TreeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignmentFlag.AlignCenter)
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # self.TreeWidget.headerItem().setFont(2, font)
        # self.TreeWidget.headerItem().setTextAlignment(3, QtCore.Qt.AlignmentFlag.AlignCenter)
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # self.TreeWidget.headerItem().setFont(3, font)
        # self.TreeWidget.setItemWidget()
        self.header = FileHeaderWidget(centralwidget)
        self.header.setGeometry(QtCore.QRect(20, 70, 761, 60))

        self.list = QListView(centralwidget)
        self.model = FileListModel(self.list)

        self.list.setSpacing(1)
        self.list.setModel(self.model)
        self.list.installEventFilter(centralwidget)
        self.list.doubleClicked.connect(self.open)
        self.list.setItemDelegate(FileItemDelegate(self.list))
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.context_menu)
        self.list.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        self.list.setGeometry(QtCore.QRect(22, 130, 750, 400))

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

    def _async_response(self, files: list, error: str):
        print("callback")
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
            print("no files")
        else:
            print("show files")
            self.list.setHidden(False)
            self.model.populate(files)
            self.list.setFocus()

    def update(self):

        print("fist update")
        super(Ui_centralwidget, self).update()
        worker = AsyncRepositoryWorker(
            name="Files",
            worker_id=self.FILES_WORKER_ID,
            repository_method=FileRepository.files,
            response_callback=self._async_response,
            arguments=()
        )
        print("second update")
        # Global.communicate.on_response.connect(self._async_response)
        # worker.run()

        if Adb.worker().work(worker):
            # First Setup loading view
            self.model.clear()
            self.list.setHidden(False)

            worker.start()
            # Then start async worker

            Global().communicate.path_toolbar__refresh.emit()

    def close(self) -> bool:
        Global().communicate.files__refresh.disconnect()
        return super(Ui_centralwidget, self).close()

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
        menu = QMenu()
        menu.addSection("Actions")

        action_copy = QAction('Copy to...', self)
        action_copy.setDisabled(True)
        menu.addAction(action_copy)

        action_move = QAction('Move to...', self)
        action_move.setDisabled(True)
        menu.addAction(action_move)

        action_rename = QAction('Rename', self)
        action_rename.triggered.connect(self.rename)
        menu.addAction(action_rename)

        action_open_file = QAction('Open', self)
        action_open_file.triggered.connect(self.open_file)
        menu.addAction(action_open_file)

        action_delete = QAction('Delete', self)
        action_delete.triggered.connect(self.delete)
        menu.addAction(action_delete)

        action_download = QAction('Download', self)
        action_download.triggered.connect(self.download_files)
        menu.addAction(action_download)

        action_download_to = QAction('Download to...', self)
        action_download_to.triggered.connect(self.download_to)
        menu.addAction(action_download_to)

        menu.addSeparator()

        action_properties = QAction('Properties', self)
        action_properties.triggered.connect(self.file_properties)
        menu.addAction(action_properties)

        menu.exec(self.mapToGlobal(pos))

    def retranslateUi(self, centralwidget):
        _translate = QtCore.QCoreApplication.translate
        centralwidget.setWindowTitle(_translate("centralwidget", "Form"))
        self.upload_tools.setText(_translate("centralwidget", "Upload"))
        self.parent_directory.setText(_translate("centralwidget", "Parent Directory"))
        # self.TreeWidget.headerItem().setText(0, _translate("centralwidget", "File"))
        # self.TreeWidget.headerItem().setText(1, _translate("centralwidget", "Permission"))
        # self.TreeWidget.headerItem().setText(2, _translate("centralwidget", "Size"))
        # self.TreeWidget.headerItem().setText(3, _translate("centralwidget", "Date"))


from qfluentwidgets import CardWidget
