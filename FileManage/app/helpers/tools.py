# ADB File Explorer
# Copyright (C) 2022  Azat Aldeshov
import json
import logging
import os
import shutil
import subprocess

from PySide6 import QtCore
from PySide6.QtCore import QObject, QFile, QIODevice, QTextStream, QThread
from PySide6.QtWidgets import QWidget
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

from FileManage.app.data.models import MessageData


class CommonProcess:
    """
    CommonProcess - executes subprocess then saves output data and exit code.
    If 'stdout_callback' is defined then every output data line will call this function

    Keyword arguments:
    arguments -- array list of arguments
    stdout -- define stdout (default subprocess.PIPE)
    stdout_callback -- callable function, params: (data: str) -> None (default None)
    """

    def __init__(self, arguments: list, stdout=subprocess.PIPE, stdout_callback: callable = None):
        self.ErrorData = None
        self.OutputData = None
        self.IsSuccessful = False
        if arguments:
            try:
                process = subprocess.Popen(arguments, stdout=stdout, stderr=subprocess.PIPE)
                if stdout == subprocess.PIPE and stdout_callback:
                    for line in iter(process.stdout.readline, b''):
                        stdout_callback(line.decode(encoding='utf-8'))
                        # stdout_callback(self.try_decode(line))
                data, error = process.communicate()
                self.ExitCode = process.poll()
                self.IsSuccessful = self.ExitCode == 0
                self.ErrorData = error.decode(encoding='utf-8') if error else None
                self.OutputData = data.decode(encoding='utf-8') if data else None
                # self.ErrorData = self.try_decode(error) if error else None
                # self.OutputData = self.try_decode(data) if data else None
            except FileNotFoundError:
                self.ErrorData = "Command '%s' failed! File (command) '%s' not found!" % \
                                 (' '.join(arguments), arguments[0])
            except BaseException as error:
                logging.exception("Unexpected error=%s, type(error)=%s" % (error, type(error)))
                self.ErrorData = str(error)

    # def try_decode(self, data):
    #     if not data:
    #         return None
    #     for encoding in ['utf-8', 'b64', 'gb18030', 'big5', 'cp1252', 'cp936', 'gbk']:
    #         try:
    #             print(encoding + data.decode(encoding))
    #             return data.decode(encoding)
    #         except UnicodeDecodeError:
    #             continue
    #         # 如果所有预定义的编码都失败了，使用 chardet 检测编码
    #     detected_encoding = chardet.detect(data)['encoding']
    #     if detected_encoding:
    #         try:
    #             return data.decode(detected_encoding)
    #         except UnicodeDecodeError:
    #             pass
    #     return data  # 解码失败，返回原始数据

class AsyncRepositoryWorker(QThread):
    on_response = QtCore.Signal(object, object)  # Response : data, error

    def __init__(
            self, worker_id: int, name: str,
            repository_method: callable,
            arguments: tuple, response_callback: callable
    ):
        super(AsyncRepositoryWorker, self).__init__()
        self.on_response.connect(response_callback)
        self.finished.connect(self.close)

        self.__repository_method = repository_method
        self.__arguments = arguments
        self.loading_widget = None
        self.closed = False
        self.id = worker_id
        self.name = name

    def run(self):
        data, error = self.__repository_method(*self.__arguments)
        self.on_response.emit(data, error)

    def close(self):
        if self.loading_widget:
            self.loading_widget.close()
        self.deleteLater()
        self.closed = True

    def set_loading_widget(self, widget: QWidget):
        self.loading_widget = widget

    def update_loading_widget(self, path, progress):
        if self.loading_widget and not self.closed:
            self.loading_widget.update_progress('SOURCE: %s' % path, progress)


class ProgressCallbackHelper(QObject):
    progress_callback = QtCore.Signal(str, int)

    def setup(self, parent: QObject, callback: callable):
        self.setParent(parent)
        self.progress_callback.connect(callback)


class Communicate(QObject):
    files = QtCore.Signal()
    devices = QtCore.Signal()
    # on_response = QtCore.pyqtSignal(object, object)  # Response : data, error

    up = QtCore.Signal()
    files__refresh = QtCore.Signal()
    path_toolbar__refresh = QtCore.Signal()

    status_bar = QtCore.Signal(str, int)  # Message, Duration
    notification = QtCore.Signal(MessageData)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_python_rsa_keys_signer(rerun=True) -> PythonRSASigner:
    privkey = os.path.expanduser('~/.android/adbkey')
    if os.path.isfile(privkey):
        with open(privkey) as f:
            private = f.read()
        pubkey = privkey + '.pub'
        if not os.path.isfile(pubkey):
            if shutil.which('ssh-keygen'):
                os.system(f'ssh-keygen -y -f {privkey} > {pubkey}')
            else:
                raise OSError('Could not call ssh-keygen!')
        with open(pubkey) as f:
            public = f.read()
        return PythonRSASigner(public, private)
    elif rerun:
        path = os.path.expanduser('~/.android')
        if not os.path.isfile(path):
            if not os.path.isdir(path):
                os.mkdir(path)
            keygen(key)
            return get_python_rsa_keys_signer(False)


def read_string_from_file(path: str):
    file = QFile(path)
    if file.open(QIODevice.ReadOnly | QIODevice.Text):
        text = QTextStream(file).readAll()
        file.close()
        return text
    return str()


def quote_file_name(path: str):
    return '\'' + path + '\''


def json_to_dict(path: str):
    try:
        return dict(json.loads(read_string_from_file(path)))
    except BaseException as exception:
        logging.error('File %s. %s' % (path, exception))
        return dict()
