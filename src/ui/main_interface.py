"""
该文件存放主界面的类
"""
from concurrent.futures import ThreadPoolExecutor

# pylint: disable=no-name-in-module
from PySide6.QtCore import Slot, Signal, QObject
from PySide6.QtGui import QAction
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QMainWindow, QPlainTextEdit, \
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QTextEdit, QMessageBox, QFileDialog, \
    QMenuBar, QMenu

from src.core import extract_info, download
from src.utils import centered_ui, set_window_size, text_to_list, \
    is_url, check_update
from ui.download_task_widget import DownloadTaskWidget, SignalEmitter
from ui.parser_interface import DownloadDialog
from ui.settings_interface import SettingsInterface


class MyLogger(QObject):
    log_signal : Signal = Signal(str)

    def debug(self, msg) -> None:
        self.log_signal.emit(msg)

    def warning(self, msg) -> None:
        self.log_signal.emit(msg)

    def error(self, msg) -> None:
        self.log_signal.emit(f'<span style="color: red;">{msg}</span>')

    def info(self, msg) -> None:
        self.log_signal.emit(msg)

class MainInterface(QMainWindow):
    """
    该类为主界面类
    """
    def __init__(self) -> None:
        super().__init__()
        self.text_edit : QTextEdit = QTextEdit()
        self.plain_text_edit : QPlainTextEdit = QPlainTextEdit()
        self.parse_button : QPushButton = QPushButton(self.tr("解析"))
        self.logger : MyLogger = MyLogger()
        self.main_widget : QWidget = QWidget()
        self.main_layout : QVBoxLayout = QVBoxLayout()
        self.menu_bar : QMenuBar = self.menuBar()
        self.settings_dialog : SettingsInterface = SettingsInterface(self)
        self.list_widget : QListWidget = QListWidget()
        self.executor : ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.download_executor : ThreadPoolExecutor = ThreadPoolExecutor()
        self.check_update_executor : ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.emitter : SignalEmitter = SignalEmitter()

    def closeEvent(self, event) -> None:
        self.executor.shutdown(wait=False)
        self.download_executor.shutdown(wait=False)
        self.check_update_executor.shutdown(wait=False)
        super().closeEvent(event)

    @Slot(str, str)
    def ui_tra(self, string : str, url : str) -> None:
        reply : QMessageBox = QMessageBox(self)
        if string == 'err':
            reply.setWindowTitle('检测更新')
            reply.setText('无法连接到更新服务器，请检查网络。')
            reply.exec()
        elif string:
            reply.setWindowTitle('有新版本')
            reply.setText('是否下载')
            reply.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            an = reply.exec()
            if an == QMessageBox.StandardButton.Ok:
                from PySide6.QtGui import QDesktopServices
                from PySide6.QtCore import QUrl
                QDesktopServices.openUrl(QUrl(url))
        else:
            reply.setWindowTitle('检测更新')
            reply.setText('已是最新版本')
            reply.exec()

    def initialize(self) -> None:
        self.signal_binding()
        self._initialize_parsing_box()
        self._initialize_menu_bar()
        self._initialize_cookies_menu_bar()
        self._initialize_help_menu_bar()
        self._initialize_windows()

    def signal_binding(self) -> None:
        self.emitter.parse_finished.connect(self.on_parse_finished)
        self.emitter.download_start.connect(self.start_download)
        self.emitter.download_finished.connect(self.remove_task_item)
        self.emitter.check_update.connect(self.ui_tra)
        self.logger.log_signal.connect(self.append_log_text)

    def _initialize_cookies_menu_bar(self) -> None:
        cookies_menu : QMenu = self.menu_bar.addMenu(self.tr("cookies"))
        w = cookies_menu.addAction(self.tr("导入cookies"))
        d = cookies_menu.addAction(self.tr("清除cookies"))
        w.triggered.connect(self.import_cookies)
        d.triggered.connect(self.clear_cookies)

    def clear_cookies(self) -> None:
        reply : QMessageBox.StandardButton = QMessageBox.question(self, '确认', '是否删除', QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        with open('cookies.txt', 'w', encoding='utf-8') as f:
            f.write('')

    def import_cookies(self) -> None:
        file, _ = QFileDialog.getOpenFileName(self)
        if file:
            with open(file, 'r', encoding='utf-8') as date:
                with open('cookies.txt', 'w', encoding='utf-8') as f:
                    f.write(date.read())

    @Slot()
    def check_update(self) -> None:
        if len([t for t in self.check_update_executor._threads if t.is_alive()]):
            return
        self.check_update_executor.submit(check_update, self.emitter.check_update)

    def _initialize_help_menu_bar(self) -> None:
        help_menu : QMenu = self.menu_bar.addMenu(self.tr("帮助"))
        up_date : QAction = help_menu.addAction(self.tr("检查更新"))
        help_menu.addAction(self.tr("关于"))
        help_menu.addAction(self.tr("帮助"))
        up_date.triggered.connect(self.check_update)

    def _initialize_parsing_box(self) -> None:
        self.plain_text_edit.setPlaceholderText(self.tr("请输入链接"))
        self.text_edit.setReadOnly(True)
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self._setup_input_layout()

    def _initialize_menu_bar(self) -> None:
        setting_menu : QAction = self.menu_bar.addAction(self.tr("设置"))
        setting_menu.triggered.connect(self.on_settings)

    def _initialize_windows(self) -> None:
        self.main_layout.addWidget(self.list_widget)
        self.setWindowTitle(self.tr("LuxDown"))
        set_window_size(self, ratio= 0.8)
        centered_ui.center_ui(self)
        self.main_widget.setLayout(self.main_layout)
        self.show()

    @Slot(str)
    def append_log_text(self, text : str) -> None:
        self.text_edit.append(text)

    @Slot()
    def on_settings(self) -> None:
        self.settings_dialog.exec()
        self.settings_dialog.synchronous()

    @Slot()
    def on_parse_button_clicked(self) -> None:
        self.text_edit.clear()
        urls : list[str] = text_to_list(self.plain_text_edit)
        for url in urls:
            if is_url(url):
                self.executor.submit(self._parse_url_in_thread, url)
            else:
                pass

    def _parse_url_in_thread(self, url : str) -> None:
        parsed : tuple = extract_info(url, self.logger)
        self.emitter.parse_finished.emit(parsed)

    @Slot(tuple)
    def on_parse_finished(self, parsed : tuple ) -> None:
        download_dialog : DownloadDialog = DownloadDialog(parsed, self.emitter)
        download_dialog.exec()

    def _setup_input_layout(self) -> None:
        self.setCentralWidget(self.main_widget)
        hbox : QHBoxLayout = QHBoxLayout()
        self.main_layout.addLayout(hbox)
        hbox.addWidget(self.plain_text_edit)
        hbox.addWidget(self.text_edit)
        hbox.addWidget(self.parse_button)

    @Slot(dict, dict)
    def start_download(self, titles : dict, urls : dict) -> None:
        for index in urls.keys() & titles.keys():
            list_item : QListWidgetItem = QListWidgetItem(self.list_widget)
            task_widget : DownloadTaskWidget = DownloadTaskWidget(self.emitter, titles[index])
            task_widget.is_dual_download = self.settings_dialog.settings_information.download_audio and self.settings_dialog.settings_information.download_video
            task_widget.list_item = list_item
            list_item.setSizeHint(task_widget.sizeHint())
            self.list_widget.setItemWidget(list_item,task_widget)
            self.download_executor.submit(download, urls[index], task_widget.progress_hook, index, self.settings_dialog.settings_information, self.logger)

    @Slot(QListWidgetItem)
    def remove_task_item(self, item : QListWidgetItem) -> None:
        row : int = self.list_widget.row(item)
        if row != -1:
            widget : QWidget = self.list_widget.itemWidget(item)
            if widget is not None:
                widget.deleteLater()
            self.list_widget.takeItem(row)
