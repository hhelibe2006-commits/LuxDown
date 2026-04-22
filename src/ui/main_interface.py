from PySide6.QtWidgets import QMainWindow, QPlainTextEdit, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Slot
from utils import centered_ui, set_window_size, text_to_dict, is_url
from .settings_interface import SettingsInterface
from core import parse

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plain_text_edit = QPlainTextEdit()
        self.parse_button = QPushButton("解析")
        self.main_widget = QWidget()
        self.vbox = QVBoxLayout()
        self.menu_bar = self.menuBar()
        self.settings = SettingsInterface(self)

    def initialize(self):
        self.__initialize_parsing_box()
        self.__initialize_menu_bar()
        self.__initialize_windows()

    def __initialize_parsing_box(self):
        self.plain_text_edit.setPlaceholderText("请输入链接")
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self.setup_input_layout()

    def __initialize_menu_bar(self):
        setting_menu = self.menu_bar.addAction("设置")
        setting_menu.triggered.connect(self.settings.exec)

    def __initialize_windows(self):
        self.setWindowTitle("LuxDown")
        set_window_size(self, percentage = 0.8)
        centered_ui.center_ui(self)
        self.main_widget.setLayout(self.vbox)
        self.show()

    @Slot()
    def on_parse_button_clicked(self):
        urls = text_to_dict(self.plain_text_edit)
        for url in urls:
            if is_url(url):
                parsed = parse(url)
            else:
                pass

    def setup_input_layout(self):
        self.setCentralWidget(self.main_widget)
        hbox = QHBoxLayout()
        self.vbox.addLayout(hbox)
        hbox.addWidget(self.plain_text_edit)
        hbox.addWidget(self.parse_button)
