from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMainWindow, QApplication

def set_window_size(window, percentage):
    screen = QGuiApplication.primaryScreen().geometry()

    screen_width = screen.width()
    screen_height = screen.height()

    window.resize(screen_width * percentage, screen_height * percentage)