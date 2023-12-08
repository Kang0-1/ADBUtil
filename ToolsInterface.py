import os
import re
import subprocess
import threading
import time
import resources_rc
from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QSize
from PySide6.QtGui import QIcon, QFontMetrics
from PySide6.QtWidgets import *
from adbutils import adb
from qfluentwidgets import InfoBar, InfoBarPosition
import config
from tools import Ui_Form


class ToolsInterface(QWidget):
    deviceReady = Signal()
    updateActivityInfo_signal = Signal(object, object)

    @Slot(str)
    def getDeviceFromSignal(self, device_serial):
        if device_serial:
            threading.Thread(target=self.initDevice, args=(device_serial,)).start()
        else:
            self.device = None
            self.setInfoToDefault()

    def __init__(self, parent=None):
        super(ToolsInterface, self).__init__(parent)
        self.device = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.deviceReady.connect(self.onDeviceReady)
        self.setSearchPropUI()
        self.setInputTextUI()
        self.ui.button_refresh.setIcon(QIcon(':/resources/刷新.png'))
        self.ui.button_refresh.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_refresh.clicked.connect(lambda: (self.getActivityInfo(), self.getBaseInfo()))
        self.updateActivityInfo_signal.connect(self.update_text_edit)

    @Slot()
    def onDeviceReady(self):
        # 这里执行所有依赖于设备的UI更新操作
        self.getBaseInfo()
        self.getActivityInfo()

    def initDevice(self, device_serial):
        print("工具页：" + device_serial)
        self.device = adb.device(serial=device_serial)
        fingerprint = self.device.prop.get("ro.build.fingerprint")
        build_version = identify_version(fingerprint)
        if build_version == "userdebug":
            try:
                ro = self.device.root()
                print(ro)
                time.sleep(2)
                print("设备已root")
            except Exception as e:
                print(f"root失败: {e}")
        self.deviceReady.emit()

    def setInfoToDefault(self):
        self.ui.model.setText("UnKnown")
        self.ui.brand.setText("UnKnown")
        self.ui.android_version.setText("UnKnown")
        self.ui.sn.setText("UnKnown")
        self.ui.mac.setText("UnKnown")
        self.ui.fingerprint.setText("UnKnown")
        self.ui.ipv4.setText("UnKnown")
        self.ui.sw.setText("UnKnown")
        self.ui.hw.setText("UnKnown")

    def getBaseInfo(self):
        try:
            if not self.device:
                self.show_info_bar("当前无设备连接，请检查", "error", 2)
            device = self.device
            self.ui.model.setText(device.prop.model)
            self.ui.brand.setText(device.prop.get("ro.product.brand"))
            self.ui.android_version.setText(device.prop.get("ro.build.version.release"))
            self.ui.sn.setText(device.prop.get("ro.serialno"))
            self.ui.mac.setText(device.prop.get("ro.boot.mac"))
            fingerprint = device.prop.get("ro.build.fingerprint")
            self.ui.fingerprint.setText(fingerprint)
            self.ui.ipv4.setText(getIP(device))
            build_version = identify_version(fingerprint)
            print(build_version)
            if build_version == "user":
                self.ui.sw.setText("设备不能root")
                self.ui.hw.setText("设备不能root")
            else:
                self.ui.sw.setText(device.prop.get("ro.odm.changhong.sw.ver"))
                self.ui.hw.setText(device.prop.get("ro.odm.changhong.hw.ver"))
        except AttributeError as e:
            print(e)

    def getActivityInfo(self):
        threading.Thread(target=self._getActivityInfoThread).start()

    def _getActivityInfoThread(self):
        try:
            device = self.device
            package_name = get_package_name(device)
            process_name = get_process_name(device)
            launch_activity = get_launch_activity(device)
            resumed_activity = get_resumed_activity(device)
            last_history_activity = get_last_history_activity(device)
            stack_activities = get_stack_activities(device, package_name)
            self.updateActivityInfo_signal.emit(package_name, self.ui.show_1)
            self.updateActivityInfo_signal.emit(process_name, self.ui.show_2)
            self.updateActivityInfo_signal.emit(launch_activity, self.ui.show_3)
            self.updateActivityInfo_signal.emit(resumed_activity, self.ui.show_4)
            self.updateActivityInfo_signal.emit(last_history_activity, self.ui.show_5)
            self.updateActivityInfo_signal.emit(stack_activities, self.ui.show_6)
        except Exception as e:
            print(e)

    def update_text_edit(self, text_input, text_edit):
        max_width = 540
        font_metrics = QFontMetrics(text_edit.font())

        if isinstance(text_input, list):
            # 处理字符串列表
            text_input.reverse()
            text = '\n'.join(text_input)
            line_count = len(text_input) + 2
        else:
            # 处理单个字符串
            text = text_input
            line_count = text.count('\n') + 3  # 包含换行符的情况

        text_edit.setText(text)

        # 根据最长字符串计算宽度
        max_string = max(text_input, key=len, default="") if isinstance(text_input, list) else text_input
        text_width = font_metrics.horizontalAdvance(max_string) + 30

        # 限制文本框宽度不超过最大宽度
        if text_width > max_width:
            text_width = max_width
            line_count = max(line_count, text_edit.document().lineCount())

        new_height = font_metrics.height() * line_count

        # 确保高度只增加不减少
        # new_height = max(new_height, text_edit.height())

        # 设置QTextEdit的新尺寸
        text_edit.setFixedSize(QSize(text_width, new_height))

    def setSearchPropUI(self):
        self.ui.search_prop.returnPressed.connect(self.on_getProp)
        self.ui.search_prop.searchSignal.connect(self.on_getProp)
        self.ui.search_prop.clearSignal.connect(self.on_getProp)

    def on_getProp(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error", 2)
            return
        search_text = self.ui.search_prop.text().strip()
        if not search_text:
            self.show_info_bar("请输入文本内容", "info", 2)
            return
        prop_value = self.device.prop.get(search_text)
        if search_text and not prop_value:
            self.show_info_bar("获取结果为空", "success", 2)
        print("prop_value:" + prop_value)
        self.ui.output_prop.setText(prop_value)

    def setInputTextUI(self):
        self.ui.button_input.clicked.connect(self.on_input_button_clicked)

    def on_input_button_clicked(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error", 2)
            return
        input_text = self.ui.input_text.text().strip()
        if not input_text:
            self.show_info_bar("请输入文本内容", "info", 2)
            return
        try:
            self.device.shell(f"input text '{input_text}'")
            self.show_info_bar("文本已发送", "success", 2)
            self.ui.input_text.clear()
        except Exception as e:
            self.show_info_bar("未连接设备，请检查:" + str(e), "error", 2)

    def show_info_bar(self, message, type, second):
        if type == "info":
            InfoBar.info("Info", message, self, True, 1000 * second, InfoBarPosition.BOTTOM, self).show()
        elif type == "success":
            InfoBar.success("Success", message, self, True, 1000 * second, InfoBarPosition.BOTTOM, self).show()
        elif type == "warning":
            InfoBar.warning("Warning", message, self, True, 1000 * second, InfoBarPosition.BOTTOM, self).show()
        elif type == "error":
            InfoBar.error("Error", message, self, True, 1000 * second, InfoBarPosition.BOTTOM, self).show()
        else:
            print("未知的信息类型")


def getIP(device):
    try:
        # 获取有线接口的IP地址
        # ip_wlan1 = adb.device(serial="UG0623TEST0017").shell(
        #     "ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'")
        # ip_eth0 = subprocess.check_output(
        #     "adb shell \"ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'\"",
        #     shell=True, stderr=subprocess.DEVNULL).decode().strip()
        cmd_getEth = [
            config.adb_path,
            '-s', device.serial,
            "shell",
            "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
        ]
        # 创建一个 STARTUPINFO 对象
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE  # 设置窗口隐藏
        # 执行命令
        process_1 = subprocess.run(cmd_getEth, startupinfo=startupinfo, text=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # 获取输出
        ip_eth0 = process_1.stdout
        # 如果有线接口有IP，返回这个IP
        if ip_eth0:
            return f"ETH : {ip_eth0}"
        # 获取无线接口的IP地址
        cmd_getWlan = [
            config.adb_path,
            '-s', device.serial,
            "shell",
            "ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
        ]
        # 执行命令
        process_2 = subprocess.run(cmd_getWlan, startupinfo=startupinfo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取输出
        ip_wlan0 = process_2.stdout
        # ip_wlan0 = subprocess.check_output(
        #     "adb shell \"ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'\"",
        #     shell=True, stderr=subprocess.DEVNULL).decode().strip()
        # 如果无线接口有IP，返回这个IP
        if ip_wlan0:
            return f"WIFI : {ip_wlan0}"
    except subprocess.CalledProcessError:
        pass
    # 如果两个接口都没有IP，返回“未连接”
    return "未连接"


def identify_version(s):
    # 正则表达式匹配 'userdebug' 或 'user'
    # 注意 'userdebug' 需要在 'user' 之前匹配，因为 'userdebug' 包含 'user'
    match = re.search(r'userdebug|user', s)
    if match:
        return match.group()
    return "unknown"


def middle(string, start, end):
    if not string or start not in string or end not in string:
        return ""

    start_index = string.index(start) + len(start)
    end_index = string.index(end, start_index) if end else len(string)

    return string[start_index:end_index]


def get_package_name(device):
    if not device:
        return "未连接设备，请检查"
    result = device.shell("dumpsys activity activities | grep packageName")

    if not result.strip():
        return "没有获取到包名, 请检查ADB设备是否已断开"

    first_line = result.split("\n")[0].strip()
    package_name = middle(first_line, "packageName=", " processName=")
    return package_name if package_name else "没有获取到包名"


def get_process_name(device):
    if not device:
        return "未连接设备，请检查"
    result = device.shell("dumpsys activity activities | grep processName")

    if not result.strip():
        return "没有获取到进程, 请检查ADB设备是否已断开"

    first_line = result.split("\n")[0].strip()
    process_name = middle(first_line, "processName=", "")
    return process_name if process_name else "没有获取到进程"


def get_launch_activity(device):
    if not device:
        return "未连接设备，请检查"
    result = device.shell("dumpsys activity activities | grep mActivityComponent")

    if not result.strip():
        return "没有获取到启动活动, 请检查ADB设备是否已断开"

    first_line = result.split("\n")[0].strip()
    activity_component = middle(first_line, "mActivityComponent=", "")
    launch_activity = activity_component
    return launch_activity if launch_activity else "没有获取到启动活动"


def get_resumed_activity(device):
    if not device:
        return "未连接设备，请检查"
    result = device.shell("dumpsys activity activities | grep mResumedActivity")

    if not result.strip():
        return "没有获取到前台活动, 请检查ADB设备是否锁屏或已断开"

    first_line = result.split("\n")[0].strip()
    activity_component = middle(first_line, "u0 ", " t")
    resumed_activity = activity_component
    return resumed_activity if resumed_activity else "没有获取到前台活动"


def get_last_history_activity(device):
    if not device:
        return "未连接设备，请检查"
    result = device.shell("dumpsys activity activities | grep mLastPausedActivity")

    if not result.strip():
        return "没有获取到上次活动, 请检查ADB设备是否已断开"

    first_line = result.split("\n")[0].strip()
    activity_component = middle(first_line, "u0 ", " t")
    last_paused_activity = activity_component
    return last_paused_activity if last_paused_activity else "没有获取到上次活动"


def get_stack_activities(device, package_name):
    if not device:
        return "未连接设备，请检查"
    command = f"dumpsys activity activities | grep {package_name} | grep Activities"
    result = device.shell(command)

    stack_activities = []
    if not result.strip():
        stack_activities.append("没有获取到堆栈列表, 请检查ADB设备是否已断开")
        return stack_activities

    activities_part = middle(result, "[", "]")
    activities = activities_part.split(",")

    for activity in activities:
        activity_component = middle(activity.strip(), "u0 ", " t")
        if activity_component:
            stack_activities.append(activity_component)

    return stack_activities
