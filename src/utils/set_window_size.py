"""
该文件存放界面大小设置的函数
"""
from PySide6.QtCore import QRect
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMainWindow, QDialog


def set_window_size(window : QMainWindow | QDialog, ratio : float) -> None:
    #获取屏幕大小
    screen : QRect = QGuiApplication.primaryScreen().geometry()
    #分别获取屏幕的长度和宽度
    screen_width : int= screen.width()
    screen_height : int= screen.height()
    #设置窗口大小
    window.resize(int(screen_width * ratio), int(screen_height * ratio))
