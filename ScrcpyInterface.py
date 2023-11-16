from typing import Optional

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from argparse import ArgumentParser
from adbutils import adb
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
        self.ui.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label.setScaledContents(True)  # 确保内容缩放以适应 QLabel 的大小

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        # self.ui.ipInput
        #
        # self.ui.button_connect

        self.ui.button_refresh.clicked.connect(lambda: self.click_refresh())

        self.ui.button_start.clicked.connect(lambda: self.click_start())

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

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
            label_size = self.ui.label.size()  # QLabel 的当前大小
            image_size = self.client.resolution  # 实际图像的分辨率

            if image_size is None:
                return

            # 计算缩放比例
            x_scale = image_size[0] / label_size.width()
            y_scale = image_size[1] / label_size.height()

            # 调整点击坐标
            x = evt.x() * x_scale
            y = evt.y() * y_scale

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
        if frame is not None:
            # 将 frame 转换为 QImage
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
            pix = QPixmap.fromImage(image)

            # 设置 QLabel 的 QPixmap
            self.ui.label.setPixmap(pix)
            # 可能需要调整窗口大小以适应新图像大小
            self.adjustSize()

    def on_frame_1(self, frame):
        app.processEvents()
        if frame is not None:
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_BGR888,)
            pix = QPixmap.fromImage(image)
            scaled_pix = pix.scaled(
                self.ui.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.label.setPixmap(scaled_pix)

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
