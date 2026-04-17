import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from utils import centered_ui,set_window_size

class MainInterface:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()

    def initialize_ui(self):
        self.window.setWindowTitle("LuxDown")

        set_window_size(self.window, 0.8)
        centered_ui.center_ui(self.window)

        self.window.show()
        sys.exit(self.app.exec_())

