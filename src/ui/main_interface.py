"""
该文件存放主界面的类
"""
import http.cookiejar
from concurrent.futures import ThreadPoolExecutor, Future

# pylint: disable=no-name-in-module
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QCloseEvent
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QMainWindow, QPlainTextEdit, \
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, \
    QListWidgetItem, QTextEdit, QMessageBox, QFileDialog, QMenuBar, QMenu

from src.core import extract_info
from src.core.download_task import DownloadTask
from src.information import settings_manager
from src.signal import MyLogger
from src.ui.download_task_widget import DownloadTaskWidget, SignalEmitter
from src.ui.parser_interface import DownloadDialog
from src.ui.settings_interface import SettingsInterface
from src.utils import centered_ui, set_window_size, text_to_list, \
    is_url, check_update
from src.widgets import MessageBox
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl


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
        self.download_executor : ThreadPoolExecutor = ThreadPoolExecutor(max_workers=3)
        self.check_update_executor : ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.emitter : SignalEmitter = SignalEmitter()
        self._check_update_futures: set[Future] = set()

    def closeEvent(self, event : QCloseEvent) -> None:
        self.executor.shutdown(wait=False)
        self.download_executor.shutdown(wait=False)
        self.check_update_executor.shutdown(wait=False)
        super().closeEvent(event)

    def initialize(self) -> None:
        self._signal_binding()
        self._initialize_parsing_box()
        self._initialize_menu_bar()
        self._initialize_cookies_menu_bar()
        self._initialize_help_menu_bar()
        self._initialize_windows()

    def _signal_binding(self) -> None:
        self.emitter.parse_finished.connect(self.on_parse_finished)
        self.emitter.download_start.connect(self.start_download)
        self.emitter.download_finished.connect(self.remove_task_item)
        self.emitter.check_update.connect(self.ui_tra)
        self.logger.log_signal.connect(self.append_log_text)

    def _initialize_parsing_box(self) -> None:
        self.plain_text_edit.setPlaceholderText(self.tr("请输入链接"))
        self.text_edit.setReadOnly(True)
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self._setup_input_layout()

    def _initialize_menu_bar(self) -> None:
        setting_menu : QAction = self.menu_bar.addAction(self.tr("设置"))
        setting_menu.triggered.connect(self.on_settings)

    def _initialize_cookies_menu_bar(self) -> None:
        cookies_menu : QMenu = self.menu_bar.addMenu(self.tr("cookies"))
        w = cookies_menu.addAction(self.tr("导入cookies"))
        d = cookies_menu.addAction(self.tr("清除cookies"))
        w.triggered.connect(self.import_cookies)
        d.triggered.connect(self.clear_cookies)

    def _initialize_help_menu_bar(self) -> None:
        help_menu : QMenu = self.menu_bar.addMenu(self.tr("帮助"))
        up_date : QAction = help_menu.addAction(self.tr("检查更新"))
        help_menu.addAction(self.tr("关于"))
        help_menu.addAction(self.tr("帮助"))
        up_date.triggered.connect(self.check_update)

    def _initialize_windows(self) -> None:
        self.main_layout.addWidget(self.list_widget)
        self.setWindowTitle(self.tr("LuxDown"))
        set_window_size(self, ratio= 0.8)
        centered_ui.center_ui(self)
        self.main_widget.setLayout(self.main_layout)
        self.show()

    @Slot(str, str)
    def ui_tra(self, string : str, url : str) -> None:
        if string == 'err':
            MessageBox(self, title='检测更新', text='无法连接到更新服务器，请检查网络。').exec()
        elif string:
            reply : int = MessageBox(
                self,
                title='有新版本',
                text='是否下载',
                buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
            ).exec()
            if reply == QMessageBox.StandardButton.Ok:
                QDesktopServices.openUrl(QUrl(url))
        else:
            MessageBox(self, title='检测更新', text='已是最新版本').exec()

    @Slot
    def clear_cookies(self) -> None:
        reply = MessageBox(
            self,
            title='确认',
            text='是否删除',
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return
        settings_manager.clear_cookies()

    @Slot()
    def import_cookies(self) -> None:
        file, _ = QFileDialog.getOpenFileName(self)
        if file:
            settings_manager.import_cookies(file)

    @Slot()
    def check_update(self) -> None:
        # 如果已有未完成的检查任务则跳过
        if any(not f.done() for f in self._check_update_futures):
            return

        fut = self.check_update_executor.submit(check_update, self.emitter.check_update)
        self._check_update_futures.add(fut)
        # 在完成时从集合中移除
        fut.add_done_callback(lambda f: self._check_update_futures.discard(f))

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
                MessageBox(self, title=self.tr('该条目不是链接'), text=self.tr(f'{url}不是链接')).exec()

    def _parse_url_in_thread(self, url : str) -> None:
        parsed : tuple = extract_info(
            url,
            self.logger,
            settings_manager.cookies_file
        )
        self.emitter.parse_finished.emit(parsed)

    @Slot(tuple)
    def on_parse_finished(self, parsed : tuple) -> None:
        download_dialog : DownloadDialog = DownloadDialog(parsed, self.emitter)
        download_dialog.exec()

    def _setup_input_layout(self) -> None:
        self.setCentralWidget(self.main_widget)
        hbox : QHBoxLayout = QHBoxLayout()
        self.main_layout.addLayout(hbox)
        hbox.addWidget(self.plain_text_edit)
        hbox.addWidget(self.text_edit)
        hbox.addWidget(self.parse_button)

    @Slot(dict, dict, dict)
    def start_download(self, titles : dict, urls : dict, resolution : dict) -> None:
        for index in urls.keys() & titles.keys() & resolution.keys():
            list_item : QListWidgetItem = QListWidgetItem(self.list_widget)
            task_widget : DownloadTaskWidget = DownloadTaskWidget(self.emitter, titles[index])
            task_widget.is_dual_download = (
                    settings_manager.download_audio and
                    settings_manager.download_video
            )
            task_widget.list_item = list_item
            list_item.setSizeHint(task_widget.sizeHint())
            self.list_widget.setItemWidget(list_item,task_widget)
            def _finished_cb(item=list_item) -> None:
                # 当任务完成时通知 UI 移除对应的项
                self.emitter.download_finished.emit(item)

            download_task = DownloadTask(
                urls[index],
                index,
                settings_manager,
                self.logger,
                resolution[index],
                progress_callback=task_widget.progress_hook,
                finished_callback=_finished_cb,
            )
            task_widget.task = download_task
            self.download_executor.submit(download_task.run)

    @Slot(QListWidgetItem)
    def remove_task_item(self, item : QListWidgetItem) -> None:
        row : int = self.list_widget.row(item)
        if row != -1:
            widget : QWidget = self.list_widget.itemWidget(item)
            if widget is not None:
                widget.deleteLater()
            taken_item = self.list_widget.takeItem(row)
            del taken_item
