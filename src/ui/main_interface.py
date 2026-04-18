import sys
from PySide6.QtWidgets import QMainWindow, QApplication, \
    QPlainTextEdit, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QMenu, QMenuBar
from PySide6.QtGui import QAction
from .settings_interface import SettingsInterface
from utils import centered_ui,set_window_size,text_to_dict

class MainInterface:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.plain_text_edit = QPlainTextEdit()
        self.parse_button = QPushButton("解析")
        self.download_button = QPushButton("下载")
        self.main_widget = QWidget()
        self.vbox = QVBoxLayout()
        self.menu_bar = self.window.menuBar()
        self.initialize_ui()

    def initialize_ui(self):
        self.window.setWindowTitle("LuxDown")
        self.plain_text_edit.setPlaceholderText("请输入链接")
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self.plain_text_edit.setMinimumHeight(20)
        self.plain_text_edit.setMaximumHeight(200)
        self.initialize_menu_bar()
        #将文本框和按钮组成一个组件,并添加到主窗口
        self.add_input()
        #设置主窗口大小与位置
        set_window_size(self.window, 0.8)
        centered_ui.center_ui(self.window)
        #运行窗口
        self.window.show()
        sys.exit(self.app.exec_())

    def add_input(self):
        self.window.setCentralWidget(self.main_widget)
        hbox = QHBoxLayout()
        self.vbox.addLayout(hbox)
        hbox.addWidget(self.plain_text_edit)
        hbox.addWidget(self.parse_button)
        hbox.addWidget(self.download_button)
        self.vbox.addStretch()
        self.main_widget.setLayout(self.vbox)

    def on_parse_button_clicked(self):
        urls = text_to_dict(self.plain_text_edit)
        print(urls)

    def initialize_menu_bar(self):
        setting_menu = self.menu_bar.addAction("设置")
        setting_menu.triggered.connect(self.show_settings)

    def show_settings(self):
        settings = SettingsInterface(self.window)
        settings.exec_()
