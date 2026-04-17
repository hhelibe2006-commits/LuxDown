from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QScreen

def center_ui(window):
    screen = QtGui.QGuiApplication.primaryScreen().availableGeometry()
    size = window.geometry()
    window.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)