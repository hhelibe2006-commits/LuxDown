"""
该文件存放主界面的类
"""
from concurrent.futures import ThreadPoolExecutor

# pylint: disable=no-name-in-module
from PySide6.QtCore import Slot, Signal, QObject
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QMainWindow, QPlainTextEdit, \
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QProgressBar, \
    QListWidget, QLabel, QListWidgetItem, QTextEdit, QMessageBox, QFileDialog

from src.core import extract_info, download
from src.utils import centered_ui, set_window_size, text_to_list, \
    is_url, check_update
from ui.parser_interface import DownloadDialog
from ui.settings_interface import SettingsInterface


class MyLogger(QObject):
    log_signal = Signal(str)

    def debug(self, msg):
        self.log_signal.emit(msg)

    def warning(self, msg):
        self.log_signal.emit(msg)

    def error(self, msg):
        self.log_signal.emit(f'<span style="color: red;">{msg}</span>')

    def info(self, msg):
        self.log_signal.emit(msg)
class SignalEmitter(QObject):
    parse_finished = Signal(tuple)
    download_start = Signal(object, object)
    progress_update = Signal(object)
    download_finished = Signal(object)

class DownloadTaskWidget(QWidget):
    def __init__(self, signal, title):
        super().__init__()
        self.list_item = None
        self.is_cancelled = False
        self.is_dual_download = False
        self.external_emitter = signal
        self.emitter = SignalEmitter()
        self.hbox = QHBoxLayout()
        self.label = QLabel(title)
        self.hbox.addWidget(self.label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.hbox.addWidget(self.progress_bar)
        self.button = QPushButton(self.tr("取消"))
        self.hbox.addWidget(self.button)
        self.setLayout(self.hbox)
        self.button.clicked.connect(self.on_cancel_clicked)
        self.emitter.progress_update.connect(self.update_progress)


    @Slot()
    def on_cancel_clicked(self):
        self.is_cancelled = True
        self.external_emitter.download_finished.emit(self.list_item)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def progress_hook(self, d):
        if self.is_cancelled:
            raise
        if d['status'] == 'downloading':
            self.emitter.progress_update.emit(d['_percent'])
        elif d['status'] == 'finished':
            if not self.is_dual_download:
                self.external_emitter.download_finished.emit(self.list_item)
            self.is_dual_download = False

class MainInterface(QMainWindow):
    """
    该类为主界面类
    """
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        self.plain_text_edit = QPlainTextEdit()
        self.parse_button = QPushButton(self.tr("解析"))
        self.logger = MyLogger()
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.menu_bar = self.menuBar()
        self.settings_dialog = SettingsInterface(self)
        self.list_widget = QListWidget()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.download_executor = ThreadPoolExecutor()
        self.emitter = SignalEmitter()
        self.emitter.parse_finished.connect(self.on_parse_finished)
        self.emitter.download_start.connect(self.start_download)
        self.emitter.download_finished.connect(self.remove_task_item)
        self.logger.log_signal.connect(self.append_log_text)

    def closeEvent(self, event):
        self.executor.shutdown(wait=False)
        self.download_executor.shutdown(wait=False)
        super().closeEvent(event)

    def initialize(self):
        self._initialize_parsing_box()
        self._initialize_menu_bar()
        self._initialize_cookies_menu_bar()
        self._initialize_help_menu_bar()
        self.main_layout.addWidget(self.list_widget)
        self._initialize_windows()
        #reply = QMessageBox.question(self, '确认', '是否保存？',
        #                             QMessageBox.Yes, QMessageBox.No)

    def _initialize_cookies_menu_bar(self):
        cookies_menu = self.menu_bar.addMenu(self.tr("cookies"))
        w = cookies_menu.addAction(self.tr("导入cookies"))
        d = cookies_menu.addAction(self.tr("清除cookies"))
        w.triggered.connect(self.import_cookies)
        d.triggered.connect(self.clear_cookies)

    def clear_cookies(self):
        reply = QMessageBox.question(self, '确认', '是否删除', QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        with open('cookies.txt', 'w', encoding='utf-8') as f:
            f.write('')

    def import_cookies(self):
        file, _ = QFileDialog.getOpenFileName(self)
        if file:
            with open(file, 'r', encoding='utf-8') as date:
                with open('cookies.txt', 'w', encoding='utf-8') as f:
                    f.write(date.read())

    def _initialize_help_menu_bar(self):
        help_menu = self.menu_bar.addMenu(self.tr("帮助"))
        up_date=help_menu.addAction(self.tr("检查更新"))
        help_menu.addAction(self.tr("关于"))
        help_menu.addAction(self.tr("帮助"))
        up_date.triggered.connect(check_update)

    def _initialize_parsing_box(self):
        self.plain_text_edit.setPlaceholderText(self.tr("请输入链接"))
        self.text_edit.setReadOnly(True)
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self._setup_input_layout()

    def _initialize_menu_bar(self):
        setting_menu = self.menu_bar.addAction(self.tr("设置"))
        setting_menu.triggered.connect(self.on_settings)

    def _initialize_windows(self):
        self.setWindowTitle(self.tr("LuxDown"))
        set_window_size(self, ratio= 0.8)
        centered_ui.center_ui(self)
        self.main_widget.setLayout(self.main_layout)
        self.show()

    def append_log_text(self, text):
        self.text_edit.append(text)

    @Slot()
    def on_settings(self):
        self.settings_dialog.exec()
        self.settings_dialog.synchronous()

    @Slot()
    def on_parse_button_clicked(self):
        self.text_edit.clear()
        urls = text_to_list(self.plain_text_edit)
        for url in urls:
            if is_url(url):
                self.executor.submit(self._parse_url_in_thread, url)
            else:
                pass

    def _parse_url_in_thread(self, url):
        parsed = extract_info(url, self.logger)
        self.emitter.parse_finished.emit(parsed)

    def on_parse_finished(self, parsed):
        download_dialog = DownloadDialog(parsed, self.emitter)
        download_dialog.exec()

    def _setup_input_layout(self):
        self.setCentralWidget(self.main_widget)
        hbox = QHBoxLayout()
        self.main_layout.addLayout(hbox)
        hbox.addWidget(self.plain_text_edit)
        hbox.addWidget(self.text_edit)
        hbox.addWidget(self.parse_button)

    def start_download(self, titles, urls):
        for index in urls.keys() & titles.keys():
            list_item = QListWidgetItem(self.list_widget)
            task_widget = DownloadTaskWidget(self.emitter, titles[index])
            task_widget.is_dual_download= self.settings_dialog.settings_information.download_audio and self.settings_dialog.settings_information.download_video
            task_widget.list_item=list_item
            list_item.setSizeHint(task_widget.sizeHint())
            self.list_widget.setItemWidget(list_item,task_widget)
            self.download_executor.submit(download, urls[index], task_widget.progress_hook, index, self.settings_dialog.settings_information, self.logger)

    def remove_task_item(self, item):
        row = self.list_widget.row(item)
        if row != -1:
            widget = self.list_widget.itemWidget(item)
            if widget is not None:
                widget.deleteLater()
            self.list_widget.takeItem(row)
