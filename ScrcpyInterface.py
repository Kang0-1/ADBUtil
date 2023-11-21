import os
import re
from PySide6.QtGui import QIcon, QMouseEvent, QKeyEvent, QImage, QPixmap
import threading
import time
from pathlib import Path
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6 import QtGui, QtCore
from typing import Optional
import cv2
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from argparse import ArgumentParser
from adbutils import adb, AdbTimeout
from qfluentwidgets import MessageBox, InfoBar, InfoBarPosition

import scrcpy
import globals

from untitled import Ui_centralwidget
from main_scrcpy import Ui_centralwidget

if not QApplication.instance():
    app = QApplication()
else:
    app = QApplication.instance()


class ScrcpyInterface(QWidget):
    # 用信号和槽机制来实现线程安全的UI更新
    recording_finished_signal = Signal(str, str)
    recording_hide_stop_button_signal = Signal(object)
    logcat_finished_signal = Signal(str, str)
    logcat_hide_stop_button_signal = Signal(object)

    def __init__(self, parent=None):
        super(ScrcpyInterface, self).__init__(parent)

        self.client = None
        self.device = None
        self.recording_thread = None
        self.logcat_thread = None
        self.record_stop_event = threading.Event()  # 用于控制录屏停止的事件
        self.logcat_stop_event = threading.Event()  # 用于控制log停止的事件
        self.recording_finished_signal.connect(self.show_info_bar)
        self.recording_hide_stop_button_signal.connect(self.hide_stop_button)
        self.logcat_finished_signal.connect(self.show_info_bar)
        self.logcat_hide_stop_button_signal.connect(self.hide_stop_button)
        self.logcat = None  # 存储logcat的数据
        self.logcat_file_path = None  # 存储logcat的log路径

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
        self.bindControllers()

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

        self.ui.button_connect.clicked.connect(self.click_connect)

        self.ui.button_refresh.clicked.connect(self.click_refresh)

        self.ui.button_start.clicked.connect(self.click_start)

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

    def click_connect(self):
        ip = self.ui.ipInput.text()
        print(ip)
        if not ip:
            # w = Dialog("Connect Info", "请输入ip:port", self)
            w = MessageBox("🤣🤣🤣", "请输入 ip:port", self)
            w.yesButton.setText("好的")
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
        # print("1", self.ui.combo_device.currentText())
        # print("1", self.device)
        if self.ui.combo_device.currentText():
            self.device = adb.device(serial=self.ui.combo_device.currentText())
            globals.CURRENT_DEVICE = self.device.serial

    def click_start(self):
        print(self.device)
        if self.device:
            self.ui.progressRing.setVisible(False)
            # 停止当前 scrcpy 客户端，如果它正在运行
            if self.client:
                self.client.stop()
                self.client = None
            # Setup client
            self.client = scrcpy.Client(
                device=self.device,
                flip=self.ui.flip.isChecked(),
                bitrate=1000000000
            )
            self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
            self.client.start(True, True)
            globals.CURRENT_DEVICE = self.device.serial

        else:
            InfoBar.error("Error", "未找到设备!", self, True, 2000, InfoBarPosition.BOTTOM, self).show()

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

    def bindControllers(self):
        self.ui.button_home.setIcon(QIcon('resources/主页.png'))
        self.ui.button_home.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_home.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_HOME))
        # 四种方式
        # adb.device(serial=self.device.serial).shell("input keyevent 3")
        # adb.device(serial=self.device.serial).shell(['input', 'keyevent', str(scrcpy.KEYCODE_HOME)])
        # self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        # self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)

        self.ui.button_back.setIcon(QIcon('resources/系统返回.png'))
        self.ui.button_back.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_back.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_BACK))
        # self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        # self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)

        self.ui.button_logcat.clicked.connect(self.on_click_logcat_start)
        self.ui.button_logcat_stop.setVisible(False)
        self.ui.button_logcat_stop.clicked.connect(self.on_click_logcat_stop)

        self.ui.button_snapshot.setIcon(QIcon('resources/截图.png'))
        self.ui.button_snapshot.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_snapshot.clicked.connect(self.on_click_snapShot)

        self.ui.button_recording.setIcon(QIcon('resources/录像.png'))
        self.ui.button_recording.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_recording.clicked.connect(self.on_click_recording_start)

        self.ui.button_recording_stop.setVisible(False)
        self.ui.button_recording_stop.setIcon(QIcon('resources/暂停录像.png'))
        self.ui.button_recording_stop.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_recording_stop.clicked.connect(self.on_click_recording_stop)

        self.ui.button_power.setIcon(QIcon('resources/关机.png'))
        self.ui.button_power.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_power.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_POWER))

        self.ui.button_mute.setIcon(QIcon('resources/静音.png'))
        self.ui.button_mute.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_mute.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_VOLUME_MUTE))

        self.ui.button_enter.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_DPAD_CENTER))

        self.ui.button_up.setIcon(QIcon('resources/向上箭头.png'))
        self.ui.button_up.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_up.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_DPAD_UP))

        self.ui.button_down.setIcon(QIcon('resources/向下箭头.png'))
        self.ui.button_down.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_down.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_DPAD_DOWN))

        self.ui.button_left.setIcon(QIcon('resources/向左箭头.png'))
        self.ui.button_left.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_left.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_DPAD_LEFT))

        self.ui.button_right.setIcon(QIcon('resources/向右箭头.png'))
        self.ui.button_right.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_right.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_DPAD_RIGHT))

        self.ui.button_volUp.setIcon(QIcon('resources/音量加.png'))
        self.ui.button_volUp.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_volUp.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_VOLUME_UP))

        self.ui.button_volDown.setIcon(QIcon('resources/音量减.png'))
        self.ui.button_volDown.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_volDown.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_VOLUME_DOWN))

        self.ui.button_menu.setIcon(QIcon('resources/菜单.png'))
        self.ui.button_menu.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_menu.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_MENU))

        self.ui.button_delete.setIcon(QIcon('resources/删除.png'))
        self.ui.button_delete.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_delete.clicked.connect(
            lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_DEL))

        self.ui.button_num_0.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_0))
        self.ui.button_num_1.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_1))
        self.ui.button_num_2.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_2))
        self.ui.button_num_3.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_3))
        self.ui.button_num_4.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_4))
        self.ui.button_num_5.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_5))
        self.ui.button_num_6.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_6))
        self.ui.button_num_7.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_7))
        self.ui.button_num_8.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_8))
        self.ui.button_num_9.clicked.connect(lambda: adb.device(serial=self.device.serial).keyevent(scrcpy.KEYCODE_9))

    def on_click_logcat_start(self):
        if self.logcat_thread and self.logcat_thread.is_alive():
            InfoBar.info("Info", "已有Logcat正在进行中", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
            return
        self.ui.button_logcat_stop.setVisible(True)
        InfoBar.info("Info", "开始Logcat", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
        self.logcat_stop_event.clear()  # 重置停止事件
        device = adb.device(serial=self.device.serial)
        self.logcat_thread = threading.Thread(target=self.perform_logcat, args=(device,))
        self.logcat_thread.start()

    def perform_logcat(self, device):
        try:
            print(self.logcat_thread.is_alive())
            folder_name = f"AdbUtilFiles/{self.device.serial}/Logs"
            desktop_path = Path(
                os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) / folder_name
            desktop_path.mkdir(parents=True, exist_ok=True)
            logcat_file = desktop_path / f"{time.strftime('%Y_%m_%d-%H_%M_%S')}.log"
            self.logcat = device.logcat(logcat_file, clear=True, re_filter=None, command="logcat -v time")
            self.logcat_file_path = logcat_file
            self.logcat_stop_event.wait(timeout=None)
            self.logcat.stop(timeout=3)
            print("logcat完成，文件保存在: " + str(logcat_file))
            self.logcat_finished_signal.emit("Log保存成功,目录位于:" + str(logcat_file), "success")
        except Exception as e:
            self.logcat_finished_signal.emit("Logcat失败," + str(e), "error")
        finally:
            self.logcat_thread = None
            self.logcat_hide_stop_button_signal.emit(self.ui.button_logcat_stop)  # 无论如何都隐藏停止按钮

    def on_click_logcat_stop(self):
        self.logcat_stop_event.set()  # 触发停止事件

    def on_click_snapShot(self):
        try:
            device = adb.device(serial=self.device.serial)
            p = device.screenshot()
            folder_name = f"AdbUtilFiles/{self.device.serial}/截图"
            desktop_path = Path(
                os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) / folder_name
            desktop_path.mkdir(parents=True, exist_ok=True)
            screenshot_file = desktop_path / f"{time.time_ns()}.png"
            p.save(screenshot_file)
            print("屏幕截取成功，文件保存在: " + str(screenshot_file))
            InfoBar.success("Success", "屏幕截取成功，截图保存在: " + str(screenshot_file), self, True, 3000,
                            InfoBarPosition.BOTTOM, self).show()
        except Exception as e:
            print("截图失败: " + str(e))
            InfoBar.error("Error", "屏幕截取失败!" + str(e), self, True, 2000, InfoBarPosition.BOTTOM, self).show()

    def on_click_recording_start(self):
        if self.recording_thread and self.recording_thread.is_alive():
            InfoBar.info("Info", "已有录屏正在进行中", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
            return
        self.ui.button_recording_stop.setVisible(True)
        InfoBar.info("Info", "已开始录制", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
        self.record_stop_event.clear()  # 重置停止事件
        device = adb.device(serial=self.device.serial)
        self.recording_thread = threading.Thread(target=self.perform_recording, args=(device,))
        self.recording_thread.start()

    def perform_recording(self, device):
        try:
            folder_name = f"AdbUtilFiles/{self.device.serial}/录屏"
            desktop_path = Path(os.path.join(os.environ['USERPROFILE'], 'Desktop')) / folder_name
            desktop_path.mkdir(parents=True, exist_ok=True)
            recording_file = desktop_path / f"{time.time_ns()}.mp4"
            device.start_recording(recording_file)

            # 等待停止事件或超时（180秒）
            self.record_stop_event.wait(timeout=180)

            device.stop_recording()
            print("录屏成功，文件保存在: " + str(recording_file))
            self.recording_finished_signal.emit("录制完成，视频保存在" + str(recording_file), "success")
        except Exception as e:
            self.recording_finished_signal.emit("录制失败," + str(e), "error")
        finally:
            self.recording_thread = None
            self.recording_hide_stop_button_signal.emit(self.ui.button_recording_stop)  # 无论如何都隐藏停止按钮

    def on_click_recording_stop(self):
        self.record_stop_event.set()  # 触发停止事件

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

    def hide_stop_button(self, button):
        button.setVisible(False)

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            image_size = self.client.resolution  # 实际图像的分辨率

            # 调整点击坐标
            x = (evt.position().x() - (self.ui.label.width() - image_size[0] * self.ratio) / 2) / self.ratio
            y = (evt.position().y() - (self.ui.label.height() - image_size[1] * self.ratio) / 2) / self.ratio

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
