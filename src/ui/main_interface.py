import sys
from PySide6.QtWidgets import QMainWindow, QApplication, \
    QPlainTextEdit, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QTableWidget, QHeaderView
from .settings_interface import SettingsInterface
from utils import centered_ui,set_window_size,text_to_dict

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = QTableWidget(0,4)
        self.plain_text_edit = QPlainTextEdit()
        self.parse_button = QPushButton("解析")
        self.download_button = QPushButton("下载")
        self.main_widget = QWidget()
        self.vbox = QVBoxLayout()
        self.menu_bar = self.menuBar()

    def initialize(self):
        self.initialize_parsing_box()
        self.initialize_menu_bar()
        self.initialize_table_widget()
        self.initialize_windows()

    def initialize_parsing_box(self):
        self.plain_text_edit.setPlaceholderText("请输入链接")
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self.plain_text_edit.setMinimumHeight(20)
        self.plain_text_edit.setMaximumHeight(200)
        self.setup_input_layout()

    def initialize_menu_bar(self):
        setting_menu = self.menu_bar.addAction("设置")
        setting_menu.triggered.connect(self.show_settings)

    def initialize_table_widget(self):
        self.table_widget.setHorizontalHeaderLabels(["标题","时长","大小","链接"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.vbox.addWidget(self.table_widget)

    def initialize_windows(self):
        self.setWindowTitle("LuxDown")
        set_window_size(self, percentage = 0.8)
        centered_ui.center_ui(self)
        self.vbox.addStretch()
        self.main_widget.setLayout(self.vbox)
        self.show()

    def on_parse_button_clicked(self):
        urls = text_to_dict(self.plain_text_edit)

    def show_settings(self):
        settings = SettingsInterface(self)
        settings.exec_()

    def setup_input_layout(self):
        self.setCentralWidget(self.main_widget)
        hbox = QHBoxLayout()
        self.vbox.addLayout(hbox)
        hbox.addWidget(self.plain_text_edit)
        hbox.addWidget(self.parse_button)
        hbox.addWidget(self.download_button)
