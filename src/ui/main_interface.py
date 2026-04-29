"""
该文件存放主界面的类
"""
from concurrent.futures import ThreadPoolExecutor
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QMainWindow, QPlainTextEdit, \
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QProgressBar,\
    QListWidget, QLabel, QListWidgetItem
# pylint: disable=no-name-in-module
from PySide6.QtCore import Slot, Signal, QObject
from src.utils import centered_ui, set_window_size, text_to_dict, is_url
from ui.settings_interface import SettingsInterface
from src.core import parse
from ui.parser_interface import ParsyParser
from core import download

class cc(QObject):
    signal1 = Signal(tuple)
    closed = Signal(object, object)
    download_signal = Signal(object)
    delete = Signal(object)

class ListWidget(QWidget):
    def __init__(self, signal, title):
        super().__init__()
        self.l = None
        self.e = False
        self.signal = signal
        self.my_signal = cc()
        self.hbox = QHBoxLayout()
        self.label = QLabel(title)
        self.hbox.addWidget(self.label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.hbox.addWidget(self.progress_bar)
        self.button = QPushButton("取消")
        self.hbox.addWidget(self.button)
        self.setLayout(self.hbox)
        self.button.clicked.connect(self.on_button)
        self.my_signal.download_signal.connect(self.up)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def on_button(self):
        self.e = True
        self.signal.delete.emit(self.l)

    def up(self, value):
        self.progress_bar.setValue(value)

    def hook(self, d):
        if self.e:
            raise
        if d['status'] == 'downloading':
            self.executor.submit(self.my_signal.download_signal.emit, d.get('_percent'))
        elif d['status'] == 'finished':
            self.signal.delete.emit(self.l)

class MainInterface(QMainWindow):
    """
    该类为主界面类
    """
    def __init__(self):
        super().__init__()
        self.plain_text_edit = QPlainTextEdit()
        self.parse_button = QPushButton("解析")
        self.main_widget = QWidget()
        self.vbox = QVBoxLayout()
        self.menu_bar = self.menuBar()
        self.settings = SettingsInterface(self)
        self.list_widget = QListWidget()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.download_executor = ThreadPoolExecutor()
        self.signal = cc()
        self.signal.signal1.connect(self.windows)
        self.signal.closed.connect(self.download_url)
        self.signal.delete.connect(self.delete)

    def initialize(self):
        self.__initialize_parsing_box()
        self.__initialize_menu_bar()
        self.__initialize_help_menu_bar()
        self.vbox.addWidget(self.list_widget)
        self.__initialize_windows()

    def __initialize_help_menu_bar(self):
        help_menu = self.menu_bar.addMenu("帮助")
        help_menu.addAction("检查更新")
        help_menu.addAction("关于")
        help_menu.addAction("帮助")

    def __initialize_parsing_box(self):
        self.plain_text_edit.setPlaceholderText("请输入链接")
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self.setup_input_layout()

    def __initialize_menu_bar(self):
        setting_menu = self.menu_bar.addAction("设置")
        setting_menu.triggered.connect(self.on_settings)

    def __initialize_windows(self):
        self.setWindowTitle("LuxDown")
        set_window_size(self, percentage = 0.8)
        centered_ui.center_ui(self)
        self.main_widget.setLayout(self.vbox)
        self.show()

    @Slot()
    def on_settings(self):
        self.settings.exec()
        self.settings.synchronous()

    @Slot()
    def on_parse_button_clicked(self):
        urls = text_to_dict(self.plain_text_edit)
        for url in urls:
            if is_url(url):
                self.executor.submit(self.__cc, url)
            else:
                pass

    def __cc(self, url):
        parsed = parse(url)
        print(parsed)
        self.signal.signal1.emit(parsed)

    def windows(self, parsed):
        parsy_parser = ParsyParser(parsed, self.signal)
        parsy_parser.initialize()
        parsy_parser.exec()

    def setup_input_layout(self):
        self.setCentralWidget(self.main_widget)
        hbox = QHBoxLayout()
        self.vbox.addLayout(hbox)
        hbox.addWidget(self.plain_text_edit)
        hbox.addWidget(self.parse_button)

    def download_url(self, titles, urls):
        for i in urls.keys() & titles.keys():
            a = QListWidgetItem(self.list_widget)
            l = ListWidget(self.signal, titles[i])
            l.l=a
            a.setSizeHint(l.sizeHint())
            self.list_widget.setItemWidget(a,l)
            self.download_executor.submit(download, urls[i], l.hook, i, self.settings.settings_information)

    def delete(self,widget):
        row = self.list_widget.row(widget)
        delete = self.list_widget.takeItem(row)
        del delete
