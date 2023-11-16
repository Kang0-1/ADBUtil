import re
from typing import Optional

import cv2
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from argparse import ArgumentParser
from adbutils import adb, AdbTimeout
from qfluentwidgets import MessageBox, MessageDialog, Dialog, InfoBar, InfoBarPosition

import scrcpy

from untitled import Ui_centralwidget

if not QApplication.instance():
    app = QApplication()
else:
    app = QApplication.instance()


class ScrcpyInterface(QWidget):
    def __init__(self, parent=None):
        super(ScrcpyInterface, self).__init__(parent)
        self.client = None
        self.ui = Ui_centralwidget()
        self.ui.setupUi(self)
        self.max_width = 800
        self.ratio = 1

        # Setup devices
        self.devices = self.list_devices()
        if self.devices:
            self.device = adb.device(serial=self.devices[0])
        self.alive = True

        # Bind controllers
        self.ui.button_home.clicked.connect(self.on_click_home)
        self.ui.button_back.clicked.connect(self.on_click_back)

        # Bind config
        self.ui.combo_device.currentTextChanged.connect(self.choose_device)
        self.ui.flip.stateChanged.connect(self.on_flip)

        # 使用布局管理器
        layout = QVBoxLayout()
        layout.addWidget(self.ui.label)  # 假设这是显示投屏画面的 QLabel

        # 设置 QLabel 的尺寸策略
        self.ui.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.label.setScaledContents(False)  # 确保内容缩放以适应 QLabel 的大小

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        self.ui.button_connect.clicked.connect(lambda: self.click_connect())

        self.ui.button_refresh.clicked.connect(lambda: self.click_refresh())

        self.ui.button_start.clicked.connect(lambda: self.click_start())

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

    def click_connect(self):
        ip = self.ui.ipInput.text()
        print(ip)
        if not ip:
            # w = Dialog("Connect Info", "请输入ip:port", self)
            w = MessageBox("🤣🤣🤣", "请输入 ip:port", self)
            w.yesButton.setText("下次一定")
            w.cancelButton.setText("你在教我做事啊?")
            w.show()
            return
        if not re.match(r"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):([0-9]|[1-9]\d{1,"
                        r"3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$", ip):
            w = MessageBox("🫵🫵🫵", "ip输错了，检查下", self)
            w.yesButton.setText("再检查下")
            w.cancelButton.setText("我没错啊")
            w.show()
            print("ip输入有误")
            return
        if ip in self.devices:
            w = MessageBox("👉🤡👈", "已经连接该设备", self)
            w.yesButton.setText("我忘记了")
            w.cancelButton.setText("我没忘记")
            w.show()
            print("已经连接该设备!")
            return
        try:
            output = adb.connect(ip)
            if "connected to" in output:
                print(output)
                InfoBar.success("Success", "连接成功!", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
                self.devices = self.list_devices()
                self.ui.ipInput.clear()
            else:
                InfoBar.error("Error", "连接失败!", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
                print("连接失败")
        except AdbTimeout as e:
            print(e)

    def click_refresh(self):
        self.devices = self.list_devices()
        if self.devices:
            if self.device:
                self.ui.combo_device.setCurrentText(self.device)
            else:
                self.device = adb.device(serial=self.devices[0])
                self.ui.combo_device.setCurrentText(self.device)

    def click_start(self):
        if self.device:
            self.ui.progressRing.setVisible(False)
            # Setup client
            self.client = scrcpy.Client(
                device=self.device,
                flip=self.ui.flip.isChecked(),
                bitrate=1000000000
            )
            self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
            self.client.start(True, True)
        else:
            QMessageBox.information(self, "Info", "No Device!")

    def choose_device(self, device):
        if device not in self.devices:
            QMessageBox.information(self, "Device Not Found", f"Device serial [{device}] not found!")
            return
        # 更新当前选择的设备
        self.device = adb.device(serial=device)
        self.ui.combo_device.setCurrentText(device)

        # 停止当前 scrcpy 客户端，如果它正在运行
        if self.client:
            self.client.stop()
            self.client = None

        # 启动新设备的 scrcpy 客户端
        self.start_scrcpy_client()

    def start_scrcpy_client(self):
        if self.device:
            self.ui.progressRing.setVisible(False)
            # 初始化并启动 scrcpy 客户端
            self.client = scrcpy.Client(
                device=self.device,
                flip=self.ui.flip.isChecked(),
                bitrate=1000000000
            )
            self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
            self.client.start(True, True)

    def list_devices(self):
        self.ui.combo_device.clear()
        items = [i.serial for i in adb.device_list()]
        self.ui.combo_device.addItems(items)
        return items

    def on_flip(self, _):
        self.client.flip = self.ui.flip.isChecked()

    def on_click_home(self):
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)

    def on_click_back(self):
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            image_size = self.client.resolution  # 实际图像的分辨率

            # 调整点击坐标
            x = (evt.position().x() - (self.ui.label.width() - image_size[0] * self.ratio) / 2 )/ self.ratio
            y = (evt.position().y() - (self.ui.label.height() - image_size[1] * self.ratio) / 2 )/ self.ratio

            # 处理点击事件
            self.client.control.touch(x, y, action)

        return handler

    def on_key_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QKeyEvent):
            code = self.map_code(evt.key())
            if code != -1:
                self.client.control.keycode(code, action)

        return handler

    def map_code(self, code):
        """
        Map qt keycode ti android keycode

        Args:
            code: qt keycode
            android keycode, -1 if not founded
        """

        if code == -1:
            return -1
        if 48 <= code <= 57:
            return code - 48 + 7
        if 65 <= code <= 90:
            return code - 65 + 29
        if 97 <= code <= 122:
            return code - 97 + 29

        hard_code = {
            32: scrcpy.KEYCODE_SPACE,
            16777219: scrcpy.KEYCODE_DEL,
            16777248: scrcpy.KEYCODE_SHIFT_LEFT,
            16777220: scrcpy.KEYCODE_ENTER,
            16777217: scrcpy.KEYCODE_TAB,
            16777249: scrcpy.KEYCODE_CTRL_LEFT,
        }
        if code in hard_code:
            return hard_code[code]

        print(f"Unknown keycode: {code}")
        return -1

    def on_frame(self, frame):
        app.processEvents()
        if frame is not None:
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.shape[1] * 3,
                QImage.Format.Format_BGR888,
            )
            image_ratio = frame.shape[1] / frame.shape[0]
            window_ratio = self.ui.label.width() / self.ui.label.height()
            if frame.shape[1] > self.ui.label.width() or frame.shape[0] > self.ui.label.height():
                if image_ratio > window_ratio:
                    self.ratio = self.ui.label.width() / frame.shape[1]
                else:
                    self.ratio = self.ui.label.height() / frame.shape[0]
            else:
                self.ratio = 1

            pix = QPixmap(image)
            pix.setDevicePixelRatio(1 / self.ratio)
            self.ui.label.setPixmap(pix)

    def closeEvent(self, _):
        self.client.stop()
        self.alive = False


def run():
    parser = ArgumentParser(description="A simple scrcpy client")
    parser.add_argument(
        "-m",
        "--max_width",
        type=int,
        default=800,
        help="Set max width of the window, default 800",
    )
    parser.add_argument(
        "-d",
        "--device",
        type=str,
        help="Select device manually (device serial required)",
    )
    parser.add_argument("--encoder_name", type=str, help="Encoder name to use")
    args = parser.parse_args()

    scrcpyInterface = ScrcpyInterface(args.max_width, args.device, args.encoder_name)
    # scrcpyInterface.show()

    scrcpyInterface.client.start()
    while scrcpyInterface.alive:
        scrcpyInterface.client.start()
