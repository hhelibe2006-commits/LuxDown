"""
该文件存放界面位置设置的函数
"""
# pylint: disable=no-name-in-module
from PySide6 import QtGui

def center_ui(window):
    #获取屏幕中心点
    screen = QtGui.QGuiApplication.primaryScreen().availableGeometry()
    #获取窗口大小
    size = window.geometry()
    #设置窗口位置
    window.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)
