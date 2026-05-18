"""
该文件存放主界面的类
"""
from concurrent.futures import ThreadPoolExecutor, Future

from PySide6.QtCore import QUrl
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMainWindow, QPlainTextEdit, \
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit, QMessageBox, QMenu

from src.core import extract_info
from src.information import settings_manager
from src.signal import Logger
from src.ui.download_task_widget import SignalEmitter
from src.ui.list_widget import ListWidget
from src.ui.menu_bar import MenuBar
from src.ui.parser_interface import DownloadDialog
from src.utils import centered_ui, set_window_size, text_to_list, \
    is_url, check_update
from src.widgets import MessageBox


class MainInterface(QMainWindow):
    """
    该类为主界面类
    """
    def __init__(self) -> None:
        super().__init__()
        self.text_edit: QTextEdit = QTextEdit()
        self.plain_text_edit: QPlainTextEdit = QPlainTextEdit()
        self.parse_button: QPushButton = QPushButton(self.tr("解析"))
        self.logger: Logger = Logger()
        self.main_widget: QWidget = QWidget()
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.menu_bar: MenuBar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.check_update_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.emitter: SignalEmitter = SignalEmitter()
        self.list_widget: ListWidget = ListWidget(self.emitter, self.logger)
        self._check_update_futures: set[Future] = set()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.list_widget.closeEvent(event)
        self.executor.shutdown(wait=False)
        self.check_update_executor.shutdown(wait=False)
        super().closeEvent(event)

    def initialize(self) -> None:
        self._signal_binding()
        self._initialize_parsing_box()
        self._initialize_help_menu_bar()
        self._initialize_windows()

    def _signal_binding(self) -> None:
        self.emitter.parse_finished.connect(self.on_parse_finished)
        self.emitter.download_start.connect(self.list_widget.start_download)
        self.emitter.download_finished.connect(self.list_widget.remove_task_item)
        self.emitter.check_update.connect(self.ui_tra)
        self.logger.log_signal.connect(self.append_log_text)

    def _initialize_parsing_box(self) -> None:
        self.plain_text_edit.setPlaceholderText(self.tr("请输入链接"))
        self.text_edit.setReadOnly(True)
        self.parse_button.clicked.connect(self.on_parse_button_clicked)
        self._setup_input_layout()

    def _initialize_help_menu_bar(self) -> None:
        help_menu: QMenu = self.menu_bar.addMenu(self.tr("帮助"))
        up_date: QAction = help_menu.addAction(self.tr("检查更新"))
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

    @Slot(str, str, bool, str)
    def ui_tra(self, title: str, text: str, c: bool, html_url: str) -> None:
        if c:
            y = MessageBox(self, title, text,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No).exec()
            if y == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(QUrl(html_url))
        else:
            MessageBox(self, title, text).exec()

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
