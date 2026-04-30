"""
该文件存放界面大小设置的函数
"""
# pylint: disable=no-name-in-module
from PySide6.QtGui import QGuiApplication

def set_window_size(window, ratio):
    #获取屏幕大小
    screen = QGuiApplication.primaryScreen().geometry()
    #分别获取屏幕的长度和宽度
    screen_width = screen.width()
    screen_height = screen.height()
    #设置窗口大小
    window.resize(screen_width * ratio, screen_height * ratio)
