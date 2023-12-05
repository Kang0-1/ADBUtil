import os
import re
import subprocess
import threading

import config
import resources_rc
from PySide6 import QtCore
from PySide6.QtCore import Slot, Signal, QSize
from PySide6.QtGui import QIcon, QFontMetrics
from PySide6.QtWidgets import *
from adbutils import adb
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBox

from appmanager import Ui_manage


class AppDesc:
    def __init__(self):
        self.packageName = "unknown",
        self.versionName = "unknown",
        self.versionCode = "unknown",
        self.targetSdk = "unknown",
        self.minSdk = "unknown",
        self.isSystemApp = False,
        self.firstInstallTime = "",
        self.lastUpdateTime = "",
        self.apkSigningVersion = "unknown",
        self.installedPath = "unknown",
        self.length = 0,


def convert_string(input_str):
    if '\n' in input_str:
        # 字符串包含换行符，将其分割成字符串数组
        return input_str.split('\n')
    else:
        # 字符串不包含换行符，返回原始字符串
        return input_str


class AppManageInterface(QWidget):
    deviceReady = Signal()
    pull_app_finished_signal = Signal(str, str, int)
    install_app_finished_signal = Signal(str, str, int)

    @Slot(str)
    def getDeviceFromSignal(self, device_serial):
        if device_serial:
            # threading.Thread(target=self.initDevice, args=(device_serial,)).start()
            print("应用管理：" + device_serial)
            self.device = adb.device(serial=device_serial)
            self.deviceReady.emit()
        else:
            self.device = None

    def __init__(self, parent=None):
        super(AppManageInterface, self).__init__(parent)
        self.ui = Ui_manage()
        self.ui.setupUi(self)
        self.device = None
        self.AllPackageNameList = None
        self.SysPackageNameList = None
        self.UserPackageNameList = None
        self.FilterPackageNameList = None
        self.currentApp = None
        self.deviceReady.connect(self.onDeviceReady)
        self.pull_app_finished_signal.connect(self.show_info_bar)
        self.install_app_finished_signal.connect(self.show_info_bar)
        self.ui.allAppInterface.itemClicked.connect(self.onItemClicked)
        self.ui.sysAppInterface.itemClicked.connect(self.onItemClicked)
        self.ui.userAppInterface.itemClicked.connect(self.onItemClicked)

        self.ui.searchLineEdit.returnPressed.connect(self.search_package)
        self.ui.searchLineEdit.searchSignal.connect(self.search_package)
        self.ui.searchLineEdit.clearSignal.connect(self.clear_search)

        self.ui.button_pull.setIcon(QIcon(':/resources/下载.png'))
        self.ui.button_pull.setIconSize(QtCore.QSize(30, 30))
        self.ui.button_pull.clicked.connect(self.pull_app)
        self.ui.button_pull.setToolTip("提取APK")
        self.ui.button_pull.setVisible(False)
        self.ui.button_uninstall.setIcon(QIcon(':/resources/卸载.png'))
        self.ui.button_uninstall.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_uninstall.clicked.connect(self.uninstall_app)
        self.ui.button_uninstall.setToolTip("卸载APP")
        self.ui.button_uninstall.setVisible(False)
        self.ui.button_clear_data.setIcon(QIcon(':/resources/清除数据.png'))
        self.ui.button_clear_data.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_clear_data.clicked.connect(self.clear_data)
        self.ui.button_clear_data.setToolTip("清除缓存")
        self.ui.button_clear_data.setVisible(False)
        self.ui.button_fresh.setIcon(QIcon(':/resources/刷新_黑.png'))
        self.ui.button_fresh.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_fresh.clicked.connect(self.refresh)
        self.ui.button_install.setIcon(QIcon(':/resources/打开文件.png'))
        self.ui.button_install.setIconSize(QtCore.QSize(25, 25))
        self.ui.button_install.clicked.connect(self.openAndInstall)
        self.ui.button_install.setToolTip("打开文件管理器安装APK或拖动到本页面安装")

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            apk_path = urls[0].toLocalFile()
            if os.path.splitext(apk_path)[1].lower() == '.apk':
                self.show_info_bar("开始安装apk", "info", 2)
                threading.Thread(target=self.install_apk, args=(apk_path,)).start()
            else:
                self.show_info_bar("请传入APK文件", "warning", 4)

    def install_apk(self, apk_path):
        # 构建命令
        command = [
            config.adb_path,
            "install",
            "-r",
            apk_path
        ]
        # 执行命令
        process = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # command = f"adb install -r \"{apk_path}\""
        # process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode == 0:
            self.install_app_finished_signal.emit("安装成功!", "success", 2)
        else:
            self.install_app_finished_signal.emit("安装失败!", "error", 2)

    def openAndInstall(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error", 2)
            return
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select an APK file', '~', filter="APK Files (*.apk)")
        if file_name:
            self.show_info_bar("开始安装apk", "info", 2)
            threading.Thread(target=self.install_apk, args=(file_name,)).start()

    def search_package(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error", 2)
            return
        search_text = self.ui.searchLineEdit.text().strip()
        if not search_text:
            self.show_info_bar("请输入文本内容", "info", 2)
            return
        if self.AllPackageNameList:
            if self.FilterPackageNameList:
                self.FilterPackageNameList.clear()
            self.ui.allAppInterface.clear()
            self.ui.SegmentedWidget.widget('All_App').setText('搜索')
            self.FilterPackageNameList = [packageName for packageName in self.AllPackageNameList if
                                          search_text.lower() in packageName.lower()]
            for packageName in self.FilterPackageNameList:
                self.ui.allAppInterface.addItem(QListWidgetItem(packageName))

    def clear_search(self):
        print(1)
        self.ui.allAppInterface.clear()
        self.ui.SegmentedWidget.widget('All_App').setText('全部')
        for packageName in self.AllPackageNameList:
            self.ui.allAppInterface.addItem(QListWidgetItem(packageName))

    def pull_app(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error", 2)
            return
        threading.Thread(target=self.perform_pull_app).start()

    def perform_pull_app(self):
        if not self.currentApp:
            self.show_info_bar("请选择要提取的包名", "warning", 2)
            return
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        export_apk_name = os.path.join(desktop, f"{self.currentApp.packageName}.apk")
        app_install_path = self.currentApp.installedPath.split('\n')[0]
        # 构建命令
        command = [
            config.adb_path,
            "pull",
            app_install_path,
            export_apk_name
        ]
        # 执行命令
        process = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # command = f"adb pull {app_install_path} {export_apk_name}"
        # process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # result = self.device.sync.pull(app_install_path, export_apk_name)
        if process.returncode == 0:
            success = process.stdout
            # 解析速度和时间 (根据实际输出调整正则表达式)
            speed_str = regex_find(success, r"skipped\.\s(.*?)/s")
            time_str = regex_find(success, r"in (.*?)s")
            self.pull_app_finished_signal.emit(f"导出成功! 速度:{speed_str}/s, 耗时:{time_str}s", "success", 2)
        else:
            self.pull_app_finished_signal.emit("导出失败!", "error", 2)

    def uninstall_app(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error", 2)
            return
        if not self.currentApp:
            self.show_info_bar("请选择要提取的包名", "warning", 2)
            return
        w = MessageBox("提示", "确定卸载该应用?", self)
        w.yesButton.setText("Yes")
        w.yesButton.clicked.connect(self.perform_uninstall_app)
        w.cancelButton.setText("No")
        w.show()

    def perform_uninstall_app(self):
        # 构建命令
        command = [
            config.adb_path,
            "uninstall",
            self.currentApp.packageName
        ]
        # 执行命令
        process = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # command = f"adb uninstall {self.currentApp.packageName}"
        # process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        success = process.stdout
        error = process.stderr

        if error:
            self.show_info_bar("卸载失败!", "error", 2)
        elif "Success" in success:
            # 这里移除appDesc从列表中，视您的程序结构而定
            self.currentApp = None
            self.refreshPackageNameList()
            self.show_info_bar("卸载成功!", "success", 2)

    def onItemClicked(self, item):
        if not self.device:
            self.show_info_bar("未连接设备", "error", 2)
            return
        currentIndex = self.ui.SegmentedWidget.currentItem().text()
        print(currentIndex)
        print(f"Clicked Item:{item.text()}")
        app_desc = AppDesc()
        app_desc.packageName = item.text()
        app_desc.isSystemApp = True if app_desc.packageName in self.SysPackageNameList else False
        if app_desc.isSystemApp:
            self.ui.button_uninstall.setVisible(False)
        else:
            self.ui.button_uninstall.setVisible(True)
        self.ui.button_pull.setVisible(True)
        self.ui.button_clear_data.setVisible(True)
        app_desc.installedPath = get_app_install_path(self.device, app_desc.packageName)
        app_desc.app_size = get_app_length(self.device, app_desc.installedPath.split('\n')[0])
        app_desc.length = to_file_length(float(app_desc.app_size))
        get_app_basic_desc(self.device, app_desc.packageName, app_desc)
        self.currentApp = app_desc
        self.updateUI(app_desc)

    def refresh(self):
        if not self.device:
            self.show_info_bar("未连接设备", "error", 2)
            return
        self.refreshPackageNameList()

    def clear_data(self):
        if not self.device:
            self.show_info_bar("未连接设备，请检查", "error", 2)
            return
        if not self.currentApp:
            self.show_info_bar("请选择要提取的包名", "warning", 2)
            return
        w = MessageBox("提示", "确定清除应用数据?", self)
        w.yesButton.setText("Yes")
        w.yesButton.clicked.connect(self.perform_clear_data)
        w.cancelButton.setText("No")
        w.show()

    def perform_clear_data(self):
        result = self.device.shell(f"pm clear {self.currentApp.packageName}")
        if "Success" in result:
            self.show_info_bar("清除数据成功!", "success", 2)
        else:
            self.show_info_bar("清除数据失败!", "error", 2)

    def updateUI(self, app_desc):
        self.update_text_edit(app_desc.packageName, self.ui.LineEdit_1)
        self.update_text_edit(app_desc.versionName, self.ui.LineEdit_2)
        self.update_text_edit(app_desc.versionCode, self.ui.LineEdit_3)
        self.update_text_edit(app_desc.targetSdk, self.ui.LineEdit_4)
        self.update_text_edit(app_desc.minSdk, self.ui.LineEdit_5)
        self.update_text_edit("是" if app_desc.isSystemApp else "否", self.ui.LineEdit_6)
        self.update_text_edit("v" + app_desc.apkSigningVersion, self.ui.LineEdit_7)
        self.update_text_edit(app_desc.length, self.ui.LineEdit_8)
        strs = convert_string(app_desc.installedPath)
        self.update_text_edit(strs, self.ui.TextEdit)

    def update_text_edit(self, text_input, text_edit):
        max_width = 500
        font_metrics = QFontMetrics(text_edit.font())

        if isinstance(text_input, list):
            # 处理字符串列表
            text = '\n'.join(text_input)
            line_count = len(text_input) + 2
        else:
            # 处理单个字符串
            text = text_input
            line_count = text.count('\n') + 2  # 包含换行符的情况

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

    @Slot()
    def onDeviceReady(self):
        self.AllPackageNameList = self.loadPackageNames(0)
        for packageName in self.AllPackageNameList:
            self.ui.allAppInterface.addItem(QListWidgetItem(packageName))

        self.SysPackageNameList = self.loadPackageNames(1)
        for packageName in self.SysPackageNameList:
            self.ui.sysAppInterface.addItem(QListWidgetItem(packageName))

        self.UserPackageNameList = self.loadPackageNames(2)
        for packageName in self.UserPackageNameList:
            self.ui.userAppInterface.addItem(QListWidgetItem(packageName))

    def refreshPackageNameList(self):
        self.ui.allAppInterface.clear()
        self.ui.sysAppInterface.clear()
        self.ui.userAppInterface.clear()
        self.AllPackageNameList = self.loadPackageNames(0)
        for packageName in self.AllPackageNameList:
            self.ui.allAppInterface.addItem(QListWidgetItem(packageName))

        self.SysPackageNameList = self.loadPackageNames(1)
        for packageName in self.SysPackageNameList:
            self.ui.sysAppInterface.addItem(QListWidgetItem(packageName))

        self.UserPackageNameList = self.loadPackageNames(2)
        for packageName in self.UserPackageNameList:
            self.ui.userAppInterface.addItem(QListWidgetItem(packageName))
        self.ui.button_uninstall.setVisible(False)
        self.ui.button_pull.setVisible(False)
        self.ui.button_clear_data.setVisible(False)

    def loadPackageNames(self, type):
        if type == 0:
            command = "pm list packages"
        elif type == 1:
            command = "pm list packages -s"
        else:
            command = "pm list packages -3"
        device = self.device
        packageNameList = []
        result = device.shell(command)
        for line in result.split("\n"):
            line = line.strip()
            if line:
                packageName = line.partition('package:')[2]
                packageNameList.append(packageName)
        return packageNameList

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


def to_file_length(size):
    kb = size / 1024.0
    mb = kb / 1024.0
    gb = mb / 1024.0
    tb = gb / 1024.0

    if size < 0:
        return "-1"
    elif int(kb) == 0:
        return f"{size:.2f}B"
    elif int(mb) == 0:
        return f"{kb:.2f}KB"
    elif int(gb) == 0:
        return f"{mb:.2f}MB"
    elif int(tb) == 0:
        return f"{gb:.2f}GB"
    else:
        return f"{tb:.2f}TB"


def get_app_install_path(device, package_name):
    result = device.shell(f"pm path {package_name}").strip()

    if result:
        # 解析输出以获取应用路径
        app_path = result.partition('package:')[2]
        return app_path
    else:
        return ""


def get_app_length(device, installed_path):
    result = device.shell(f"stat -c '%s' {installed_path}").strip()

    if result:
        app_length = result
        return app_length
    else:
        return ""


def get_app_basic_desc(device, package_name, app_desc):
    result = device.shell(f"dumpsys package {package_name}").strip()

    if result:
        app_desc.firstInstallTime = regex_find(result, r"firstInstallTime=(.*)\s")
        app_desc.lastUpdateTime = regex_find(result, r"lastUpdateTime=(.*)\s")
        app_desc.apkSigningVersion = regex_find(result, r"apkSigningVersion=(.*)\s")
        app_desc.versionName = regex_find(result, r"versionName=(.*)\s")
        app_desc.versionCode = regex_find(result, r"versionCode=(.*?)\s")
        app_desc.minSdk = regex_find(result, r"minSdk=(.*?)\s")
        app_desc.targetSdk = regex_find(result, r"targetSdk=(.*?)\s")

    return app_desc


def regex_find(text, pattern):
    match = re.search(pattern, text)
    return match.group(1) if match else ""
