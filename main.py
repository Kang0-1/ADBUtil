import sys
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout

from qfluentwidgets import FluentWindow, SubtitleLabel, setFont, SplitFluentWindow, MSFluentWindow, setTheme, Theme
from qfluentwidgets import FluentIcon as FIF
from AppManageInterface import AppManageInterface
from FileInterface import FileInterface
from ScrcpyInterface import ScrcpyInterface
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from qfluentwidgets import MSFluentWindow
from ToolsInterface import ToolsInterface


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.homeInterface = ScrcpyInterface(self)
        self.appManageInterface = AppManageInterface(self)
        self.FileInterface = FileInterface(self)
        self.toolsInterface = ToolsInterface(self)
        self.homeInterface.device_serial.connect(self.FileInterface.ui.FilePath._refresh)
        self.homeInterface.device_serial.connect(self.toolsInterface.getDeviceFromSignal)  # 连接信号和槽
        self.homeInterface.device_serial.connect(self.appManageInterface.getDeviceFromSignal)  # 连接信号和槽
        self.toolsInterface.deviceRoot.connect(self.homeInterface.onDeviceRoot)  # 连接信号和槽
        if self.homeInterface.device:
            self.homeInterface.emit_device_serial(self.homeInterface.device.serial)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')
        self.addSubInterface(self.toolsInterface, FIF.DEVELOPER_TOOLS, '设备信息')
        self.addSubInterface(self.appManageInterface, FIF.DOCUMENT, '应用管理')
        self.addSubInterface(self.FileInterface, FIF.FOLDER, '文件管理')

    def initWindow(self):
        self.resize(1100, 630)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('ADBUtils')

    def center(self):
        # PyQt6获取屏幕参数
        screen = QGuiApplication.primaryScreen().size()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    w = Window()
    w.center()
    w.show()
    app.exec()
