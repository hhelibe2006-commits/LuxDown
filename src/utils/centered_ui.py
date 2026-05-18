"""
该文件存放界面位置设置的函数
"""
from PySide6 import QtGui
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QMainWindow, QDialog


def center_ui(window : QMainWindow | QDialog) -> None:
    #获取屏幕可用区域
    screen : QRect = QtGui.QGuiApplication.primaryScreen().availableGeometry()
    #获取窗口大小
    size : QRect = window.geometry()
    #设置窗口位置
    window.move(int((screen.width() - size.width())/2), int((screen.height() - size.height())/2))
