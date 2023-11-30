# ADB File Explorer
# Copyright (C) 2022  Azat Aldeshov
from typing import Any

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QModelIndex, QAbstractListModel, QRect, QSize
from PySide6.QtGui import QPixmap, QColor, QPalette, QFont
from PySide6.QtWidgets import QStyle, QWidget, QStyledItemDelegate, \
    QStyleOptionViewItem, QApplication, QSizePolicy, QHBoxLayout, QTextEdit, \
    QMainWindow
from qfluentwidgets import CaptionLabel

from FileManage.app.core.configurations import Resources
from FileManage.app.core.managers import Global
from FileManage.app.data.models import FileType, MessageData
from FileManage.app.data.repositories import FileRepository


class FileHeaderWidget(QWidget):
    def __init__(self, parent=None):
        super(FileHeaderWidget, self).__init__(parent)
        self.setLayout(QHBoxLayout(self))
        policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        font = QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        font.setBold(True)

        self.file = CaptionLabel('File', self)
        self.file.setAlignment(Qt.AlignCenter)
        # self.file.setContentsMargins(0, 0, 0, 0)
        self.file.setFont(font)
        policy.setHorizontalStretch(39)
        self.file.setSizePolicy(policy)
        self.layout().addWidget(self.file)

        self.permissions = CaptionLabel('Permissions', self)
        self.permissions.setAlignment(Qt.AlignCenter)
        self.permissions.setFont(font)
        policy.setHorizontalStretch(18)
        self.permissions.setSizePolicy(policy)
        self.layout().addWidget(self.permissions)

        self.size = CaptionLabel('Size', self)
        self.size.setAlignment(Qt.AlignCenter)
        self.size.setFont(font)
        policy.setHorizontalStretch(21)
        self.size.setSizePolicy(policy)
        self.layout().addWidget(self.size)

        self.date = CaptionLabel('Date', self)
        self.date.setAlignment(Qt.AlignCenter)
        self.date.setFont(font)
        policy.setHorizontalStretch(22)
        self.date.setSizePolicy(policy)
        self.layout().addWidget(self.date)

        self.setStyleSheet("QWidget { background-color: #E5E5E5; }")


class FileItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtCore.QSize:
        result = super(FileItemDelegate, self).sizeHint(option, index)
        result.setHeight(40)
        return result

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex):
        (editor.setText(index.model().data(index, Qt.EditRole)))

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex):
        editor.setGeometry(
            option.rect.left() + 48, option.rect.top(), int(option.rect.width() / 2.5) - 55, option.rect.height()
        )

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex):
        model.setData(index, editor.text(), Qt.EditRole)

    @staticmethod
    def paint_line(painter: QtGui.QPainter, color: QColor, x, y, w, h):
        painter.setPen(color)
        painter.drawLine(x, y, w, h)

    @staticmethod
    def paint_text(painter: QtGui.QPainter, text: str, color: QColor, options, x, y, w, h):
        painter.setPen(color)
        font = QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        painter.setFont(font)
        painter.drawText(QRect(x, y, w, h), options, text)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex):
        if not index.data():
            return super(FileItemDelegate, self).paint(painter, option, index)

        self.initStyleOption(option, index)
        style = option.widget.style() if option.widget else QApplication.style()
        # style.drawControl(QStyle.ControlElement.CE_ItemViewItem, option, painter, option.widget)
        style.drawPrimitive(QStyle.PrimitiveElement.PE_PanelItemViewItem, option, painter, option.widget)

        icon = option.icon
        if not icon.isNull():
            icon_rect = option.rect.adjusted(0, 0, -option.rect.width() + 80, 0)
            icon.paint(painter, icon_rect)

        text_color = option.palette.color(QPalette.Normal, QPalette.Text)

        top = option.rect.top() + 6
        bottom = option.rect.height()

        first_start = option.rect.left() + 70
        second_start = option.rect.left() + int(option.rect.width() / 2.5)
        third_start = option.rect.left() + int(option.rect.width() / 1.75)
        fourth_start = option.rect.left() + int(option.rect.width() / 1.25)
        end = option.rect.width() + option.rect.left()

        self.paint_text(
            painter, index.data().name, text_color, Qt.AlignmentFlag.AlignVCenter,
            first_start, top, second_start - first_start - 4, bottom - 10
        )

        self.paint_text(
            painter, index.data().permissions, text_color, Qt.AlignCenter | option.displayAlignment,
            second_start, top, third_start - second_start - 4, bottom - 10
        )

        self.paint_text(
            painter, index.data().size, text_color, Qt.AlignCenter | option.displayAlignment,
            third_start, top, fourth_start - third_start - 4, bottom - 10
        )

        self.paint_text(
            painter, index.data().date, text_color, Qt.AlignCenter | option.displayAlignment,
            fourth_start, top, end - fourth_start, bottom - 10
        )


class FileListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []

    def clear(self):
        self.beginResetModel()
        self.items.clear()
        self.endResetModel()

    def populate(self, files: list):
        self.beginResetModel()
        self.items.clear()
        self.items = files
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)

    def icon_path(self, index: QModelIndex = ...):
        file_type = self.items[index.row()].type
        if file_type == FileType.DIRECTORY:
            return Resources.icon_folder
        elif file_type == FileType.FILE:
            return Resources.icon_file
        elif file_type == FileType.LINK:
            link_type = self.items[index.row()].link_type
            if link_type == FileType.DIRECTORY:
                return Resources.icon_link_folder
            elif link_type == FileType.FILE:
                return Resources.icon_link_file
            return Resources.icon_link_file_unknown
        return Resources.icon_file_unknown

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        if role == Qt.EditRole and value:
            data, error = FileRepository.rename(self.items[index.row()], value)
            if error:
                Global().communicate.notification.emit(
                    MessageData(
                        timeout=10000,
                        title="Rename",
                        body="<span style='color: red; font-weight: 600'> %s </span>" % error,
                    )
                )
            Global().communicate.files__refresh.emit()
        return super(FileListModel, self).setData(index, value, role)

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.items[index.row()]
        elif role == Qt.EditRole:
            return self.items[index.row()].name
        elif role == Qt.DecorationRole:
            return QPixmap(self.icon_path(index)).scaled(32, 32, Qt.KeepAspectRatio)
        return None


class TextView(QMainWindow):
    def __init__(self, filename, data):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(500, 300))
        self.setWindowTitle(filename)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.text_edit.insertPlainText(data)
        self.text_edit.move(10, 10)
