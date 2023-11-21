from PySide6.QtGui import QIcon
from qfluentwidgets import FluentIcon as FIF
from FileInterface import FileInterface
from ScrcpyInterface import ScrcpyInterface
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from qfluentwidgets import MSFluentWindow


# class Widget(QFrame):
#
#     def __init__(self, text: str, parent=None):
#         super().__init__(parent=parent)
#         self.label = SubtitleLabel(text, self)
#         self.hBoxLayout = QHBoxLayout(self)
#
#         setFont(self.label, 24)
#         self.label.setAlignment(Qt.AlignCenter)
#         self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
#
#         # 必须给子界面设置全局唯一的对象名
#         self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = ScrcpyInterface(self)
        self.FileInterface = FileInterface(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')
        self.addSubInterface(self.FileInterface, FIF.FOLDER, '文件管理')

    def initWindow(self):
        self.resize(1100, 630)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('ADBUtils')


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    w = Window()
    w.show()
    app.exec()
