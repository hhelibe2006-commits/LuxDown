from PySide6.QtWidgets import QWidget
from utils import set_window_size,center_ui

class ParsyParser(QWidget):
    def __init__(self, parent=None):
        super().__init__()

    def initialize(self):
        self.initialize_windows()

    def initialize_windows(self):
        self.setWindowTitle("解析")
        set_window_size(self, 0.8)
        center_ui(self)

