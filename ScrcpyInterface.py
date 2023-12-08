import os
import re
import resources_rc
from PySide6.QtGui import QIcon, QMouseEvent, QKeyEvent, QImage, QPixmap
import threading
import time
from pathlib import Path
from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QApplication
from argparse import ArgumentParser
from adbutils import adb, AdbTimeout
from qfluentwidgets import MessageBox, InfoBar, InfoBarPosition, SearchLineEdit, LineEditButton, LineEdit

import scrcpy

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
    snapShot_finished_signal = Signal(str, str)
    # 用信号和槽来改变device
    device_serial = Signal(str)

    @Slot()
    def onDeviceRoot(self, message, type):
        self.show_info_bar(message, type)

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
        self.snapShot_finished_signal.connect(self.show_info_bar)
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

        # 设置 QLabel 的尺寸策略
        # self.ui.label.setScaledContents(True)  # 确保内容缩放以适应 QLabel 的大小

        self.is_swiping = False

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        self.ui.button_connect.clicked.connect(self.click_connect)
        self.ui.button_connect.setToolTip("注意在同一网络下连接!")

        validator = QIntValidator(0, 999, self)
        self.ui.input_keycode.setValidator(validator)
        self.ui.input_keycode.returnPressed.connect(self.on_input_keycode)
        self.ui.input_keycode.searchSignal.connect(self.on_input_keycode)

        self.ui.button_refresh.clicked.connect(self.click_refresh)

        self.ui.button_start.clicked.connect(self.click_start)

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

    def emit_device_serial(self, value):
        self.device_serial.emit(value)

    def wheelEvent(self, event):
        # TODO 不能滑动设置页，YouTube滑动会触发点击
        self.is_swiping = True
        # 获取滚轮事件的垂直滚动值
        delta = event.angleDelta().y()

        # 获取设备屏幕的分辨率
        image_size = self.client.resolution
        image_ratio = image_size[0] / image_size[1]  # 设备屏幕的宽高比

        # 获取窗口中用于显示设备屏幕的标签(Label)的宽高比
        window_ratio = self.ui.label.width() / self.ui.label.height()

        # 计算显示比例：根据设备屏幕和显示窗口的宽高比，确定按宽度或高度缩放
        if image_ratio > window_ratio:
            # 如果设备的宽高比大于窗口的宽高比，则按宽度缩放
            ratio = self.ui.label.width() / image_size[0]
        else:
            # 否则，按高度缩放
            ratio = self.ui.label.height() / image_size[1]

        # 动态计算滑动距离：根据滚轮滚动的幅度(delta)和显示比例(ratio)来计算
        swipe_distance = int(abs(delta) / ratio / 4)

        # 计算滑动的起点：屏幕中心
        x = image_size[0] // 2
        y = image_size[1] // 2
        start_x = int(x)
        start_y = int(y)

        # 计算滑动的终点：根据滚轮方向向上或向下滑动
        end_x = start_x
        end_y = start_y - swipe_distance if delta < 0 else start_y + swipe_distance

        # 在滑动之前短暂延迟，以区分点击和滑动
        QtCore.QThread.msleep(100)

        # 打印滑动的起始和结束坐标（调试用）
        print(start_x, start_y, end_x, end_y)

        # 发送滑动命令到设备
        self.device.swipe(start_x, start_y, end_x, end_y, 0.1)

        self.is_swiping = False

    def click_connect(self):
        ip = self.ui.ipInput.text()
        print(ip)
        if not ip:
            # w = Dialog("Connect Info", "请输入ip:port", self)
            w = MessageBox("🤣🤣🤣", "请输入 ip:port", self)
            w.yesButton.setText("Yes")
            w.cancelButton.setText("No")
            w.show()
            return
        if not re.match(r"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?):([0-9]|[1-9]\d{1,"
                        r"3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$", ip):
            w = MessageBox("🫵🫵🫵", "输入格式有误", self)
            w.yesButton.setText("Yes")
            w.cancelButton.setText("No")
            w.show()
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
                self.click_refresh()
                # self.devices = self.list_devices()
                self.ui.ipInput.clear()
            else:
                InfoBar.error("Error", "连接失败!", self, True, 2000, InfoBarPosition.BOTTOM, self).show()
                print("连接失败")
        except AdbTimeout as e:
            InfoBar.error("Error", "连接失败!" + str(e), self, True, 2000, InfoBarPosition.BOTTOM, self).show()
            print(e)

    def click_refresh(self):
        self.devices = self.list_devices()
        if self.devices:
            if self.ui.combo_device.currentText():
                self.device = adb.device(serial=self.ui.combo_device.currentText())
                self.device_serial.emit(self.device.serial)
        else:
            self.device = None
            self.device_serial.emit(None)

    def click_start(self):
        # print("click_start" + self.device.serial)
        if self.device:
            self.ui.progressRing.setVisible(False)
            self.device_serial.emit(self.device.serial)
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
        else:
            self.device_serial.emit(None)
            InfoBar.error("Error", "未找到设备!", self, True, 2000, InfoBarPosition.BOTTOM, self).show()

    def choose_device(self, device):
        if device not in self.devices:
            QMessageBox.information(self, "Device Not Found", f"Device serial [{device}] not found!")
            return
        # 更新当前选择的设备
        self.device = adb.device(serial=device)
        self.ui.combo_device.setCurrentText(device)
        self.device_serial.emit(self.device.serial)

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
        self.ui.button_home.setIcon(QIcon(':/resources/主页.png'))
        self.ui.button_home.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_home.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_HOME))
        # 四种方式
        # adb.device(serial=self.device.serial).shell("input keyevent 3")
        # adb.device(serial=self.device.serial).shell(['input', 'keyevent', str(scrcpy.KEYCODE_HOME)])
        # self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        # self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)

        self.ui.button_back.setIcon(QIcon(':/resources/系统返回.png'))
        self.ui.button_back.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_back.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_BACK))
        # self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        # self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)

        self.ui.button_logcat.clicked.connect(self.on_click_logcat_start)
        self.ui.button_logcat_stop.setVisible(False)
        self.ui.button_logcat_stop.clicked.connect(self.on_click_logcat_stop)

        self.ui.button_snapshot.setIcon(QIcon(':/resources/截图.png'))
        self.ui.button_snapshot.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_snapshot.clicked.connect(self.on_click_snapShot)

        self.ui.button_recording.setIcon(QIcon(':/resources/录像.png'))
        self.ui.button_recording.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_recording.clicked.connect(self.on_click_recording_start)

        self.ui.button_recording_stop.setVisible(False)
        self.ui.button_recording_stop.setIcon(QIcon(':/resources/暂停录像.png'))
        self.ui.button_recording_stop.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_recording_stop.clicked.connect(self.on_click_recording_stop)

        self.ui.button_power.setIcon(QIcon(':/resources/关机.png'))
        self.ui.button_power.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_power.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_POWER))

        self.ui.button_mute.setIcon(QIcon(':/resources/静音.png'))
        self.ui.button_mute.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_mute.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_VOLUME_MUTE))

        self.ui.button_enter.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_DPAD_CENTER))

        self.ui.button_up.setIcon(QIcon(':/resources/向上箭头.png'))
        self.ui.button_up.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_up.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_DPAD_UP))

        self.ui.button_down.setIcon(QIcon(':/resources/向下箭头.png'))
        self.ui.button_down.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_down.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_DPAD_DOWN))

        self.ui.button_left.setIcon(QIcon(':/resources/向左箭头.png'))
        self.ui.button_left.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_left.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_DPAD_LEFT))

        self.ui.button_right.setIcon(QIcon(':/resources/向右箭头.png'))
        self.ui.button_right.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_right.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_DPAD_RIGHT))

        self.ui.button_volUp.setIcon(QIcon(':/resources/音量加.png'))
        self.ui.button_volUp.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_volUp.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_VOLUME_UP))

        self.ui.button_volDown.setIcon(QIcon(':/resources/音量减.png'))
        self.ui.button_volDown.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_volDown.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_VOLUME_DOWN))

        self.ui.button_menu.setIcon(QIcon(':/resources/菜单.png'))
        self.ui.button_menu.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_menu.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_MENU))

        self.ui.button_delete.setIcon(QIcon(':/resources/删除.png'))
        self.ui.button_delete.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_delete.clicked.connect(
            lambda: self.general_button_handler(scrcpy.KEYCODE_DEL))

        self.ui.button_num_0.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_0))
        self.ui.button_num_1.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_1))
        self.ui.button_num_2.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_2))
        self.ui.button_num_3.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_3))
        self.ui.button_num_4.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_4))
        self.ui.button_num_5.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_5))
        self.ui.button_num_6.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_6))
        self.ui.button_num_7.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_7))
        self.ui.button_num_8.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_8))
        self.ui.button_num_9.clicked.connect(lambda: self.general_button_handler(scrcpy.KEYCODE_9))

    def general_button_handler(self, keycode):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error")
            return
        threading.Thread(target=self.device.keyevent, args=(keycode,), daemon=True).start()
        # self.device.keyevent(keycode)

    def on_input_keycode(self):
        keycode = self.ui.input_keycode.text()
        if keycode:
            self.general_button_handler(keycode)

    def on_click_logcat_start(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error")
            return
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
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error")
            return
        threading.Thread(target=self.perform_snapShot).start()

    def perform_snapShot(self):
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
            self.snapShot_finished_signal.emit("屏幕截取成功，截图保存在: " + str(screenshot_file), "success")
            # self.show_info_bar("屏幕截取成功，截图保存在: " + str(screenshot_file), "success")
        except Exception as e:
            print("截图失败: " + str(e))
            self.snapShot_finished_signal.emit("屏幕截取失败! " + str(e), "error")
            # self.show_info_bar("屏幕截取失败! " + str(e), "error")

    def on_click_recording_start(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error")
            return
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
            if self.is_swiping:
                return
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            if evt.button() == Qt.LeftButton:
                if self.client:
                    image_size = self.client.resolution  # 实际图像的分辨率
                    # print("image width = ", image_size[0], "image height = ", image_size[1])
                    image_ratio = image_size[0] / image_size[1]
                    # print("width = ", self.ui.label.width(), "height = ", self.ui.label.height())
                    window_ratio = self.ui.label.width() / self.ui.label.height()
                    if image_size[0] > self.ui.label.width() or image_size[1] > self.ui.label.height():
                        if image_ratio > window_ratio:
                            self.ratio = self.ui.label.width() / image_size[0]
                        else:
                            self.ratio = self.ui.label.height() / image_size[1]
                    else:
                        self.ratio = 1

                    # 调整点击坐标
                    # print(evt.position().x(), evt.position().y())
                    x = (evt.position().x() - (
                                self.ui.label.width() - self.ui.label.image_label.width()) / 2) / self.ratio
                    y = (evt.position().y() - (
                            self.ui.label.height() - self.ui.label.image_label.height()) / 2) / self.ratio
                    # print(x, y)

                    # 处理点击事件
                    self.client.control.touch(x, y, action)
                else:
                    self.show_info_bar("点击start开始投屏", "info")
            elif evt.button() == Qt.RightButton:
                # 处理鼠标右键点击（返回操作）
                if action == scrcpy.ACTION_DOWN:
                    # 发送返回命令
                    self.client.control.keycode(scrcpy.KEYCODE_BACK, scrcpy.ACTION_DOWN)
                    self.client.control.keycode(scrcpy.KEYCODE_BACK, scrcpy.ACTION_UP)

        return handler

    def on_key_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QKeyEvent):
            if QApplication.focusWidget() == self.ui.input_keycode:
                return
            code = self.map_code(evt.key())
            if code != -1:
                if self.client:
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
            pix = QPixmap(image)
            self.ui.label.set_image(pix)

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
