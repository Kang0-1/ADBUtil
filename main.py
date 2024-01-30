import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QGuiApplication, QDesktopServices
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtWidgets import QFrame, QHBoxLayout
from qfluentwidgets import FluentIcon as FIF, TeachingTipView, PushButton
from qfluentwidgets import MSFluentWindow
from qfluentwidgets import SubtitleLabel, setFont, NavigationAvatarWidget, NavigationItemPosition, InfoBarIcon, \
    TeachingTip, \
    TeachingTipTailPosition

import config
from AppManageInterface import AppManageInterface
from FileInterface import FileInterface
from ScrcpyInterface import ScrcpyInterface
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

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('about', ':/resources/关于.png'),
            onClick=self.onSupport,
            position=NavigationItemPosition.BOTTOM
        )

    def onSupport(self):
        # TeachingTip.create(
        #     target=self.navigationInterface.widget('avatar'),
        #     icon=InfoBarIcon.INFORMATION,
        #     title='关于',
        #     content=self.tr("With respect, let's advance towards a new stage of the spin."),
        #     isClosable=True,
        #     tailPosition=TeachingTipTailPosition.BOTTOM_LEFT,
        #     duration=-1,
        #     parent=self
        # )

        # w = MessageBox(
        #     'About',
        #     'ADB Box V1.1',
        #     self
        # )
        # w.yesButton.setText('Git')
        # w.cancelButton.setText('使用指南')
        # # 为 yesButton 设置点击事件
        # w.yesButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/Kang0-1/ADBUtil")))
        # # 为 cancelButton 设置点击事件
        # w.cancelButton.clicked.connect(self.openLocalFile)
        # w.exec()

        pos = TeachingTipTailPosition.BOTTOM_LEFT
        view = TeachingTipView(
            icon=None,
            title='关于本应用',
            content=self.tr("\n\nADB Box V1.2\n\n 联系方式: \n"),
            isClosable=True,
            tailPosition=pos,
        )
        v_layout = QVBoxLayout()
        # 创建并添加第一个邮箱链接
        email_label_1 = QLabel('<a href="mailto:weijia.kang@changhong.com">weijia.kang@changhong.com</a>')
        email_label_1.setTextFormat(Qt.RichText)
        email_label_1.setOpenExternalLinks(True)
        v_layout.addWidget(email_label_1)
        # 创建并添加第二个邮箱链接
        email_label_2 = QLabel('<a href="mailto:lin5.yang@changhong.com">lin5.yang@changhong.com</a>')
        email_label_2.setTextFormat(Qt.RichText)
        email_label_2.setOpenExternalLinks(True)
        v_layout.addWidget(email_label_2)
        container_widget_email = QWidget()
        container_widget_email.setLayout(v_layout)
        view.addWidget(container_widget_email, stretch=0, align=Qt.AlignLeft)
        h_layout = QHBoxLayout()
        button_github = PushButton('GitHub')
        button_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/Kang0-1/ADBUtil")))
        button_github.setFixedWidth(120)
        h_layout.addWidget(button_github)
        button_guidance = PushButton('使用指南')
        button_guidance.setFixedWidth(120)
        button_guidance.clicked.connect(self.openLocalFile)
        h_layout.addWidget(button_guidance)
        container_widget = QWidget()
        container_widget.setLayout(h_layout)
        view.addWidget(container_widget, stretch=0, align=Qt.AlignLeft)

        t = TeachingTip.make(view, self.navigationInterface.widget('avatar'), 3000, pos, self)
        view.closed.connect(t.close)

    def openLocalFile(self):
        word_document_path = config.get_word_document_path()

        if os.path.exists(word_document_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(word_document_path))
        else:
            print("文件不存在")

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
