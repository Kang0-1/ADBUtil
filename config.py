# config.py
import os
import sys


def get_adb_path():
    # 打包后的路径
    packaged_path = os.path.join(getattr(sys, '_MEIPASS', ''), '_internal', 'tool', 'adb.exe')

    # 开发时的路径
    dev_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tool', 'adb.exe')

    # 检查哪个路径存在，并返回
    if os.path.exists(packaged_path):
        return packaged_path
    elif os.path.exists(dev_path):
        return dev_path
    else:
        raise FileNotFoundError("adb.exe not found")


# 设置adb路径
adb_path = get_adb_path()
