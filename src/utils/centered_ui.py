from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QScreen

def center_ui(window):
    #获取屏幕中心点
    screen = QtGui.QGuiApplication.primaryScreen().availableGeometry()
    #获取窗口大小
    size = window.geometry()
    #设置窗口位置
    window.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)