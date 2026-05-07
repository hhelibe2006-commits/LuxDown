from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QTableWidget, QCheckBox, \
    QHeaderView, QPushButton
from PySide6.QtCore import QUrl, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from utils import set_window_size, center_ui


class DownloadDialog(QDialog):
    def __init__(self, parse_result:tuple, notifier):
        super().__init__()
        self.video_title = parse_result[-2]
        self.notifier = notifier
        self.main_layout = QVBoxLayout(self)
        self.top_area_layout = QHBoxLayout()
        self.webEngineView = QWebEngineView()
        self.right_panel_layout = QVBoxLayout()
        self.description_browser = QTextBrowser()
        self.video_table = QTableWidget(len(parse_result[0]), 4)
        self.initialize(parse_result)

    def initialize(self,parse_result):
        self._initialize_window()
        self._initialize_parse_result(parse_result)
        self._initialize_video_table(parse_result)
        self._initialize_main_layout()

    def _initialize_parse_result(self, parse_result):
        self.webEngineView.setUrl(QUrl(parse_result[-1]))
        self.top_area_layout.addWidget(self.webEngineView)
        self.title_label = QLabel(parse_result[-2])
        self.right_panel_layout.addWidget(self.title_label)
        self.description_browser.setPlainText(parse_result[-3])
        self.right_panel_layout.addWidget(self.description_browser)
        self.top_area_layout.addLayout(self.right_panel_layout)
        self.top_area_layout.setStretch(0, 1)
        self.top_area_layout.setStretch(1, 2)
        self.main_layout.addLayout(self.top_area_layout)

    def _initialize_video_table(self, parse_result):
        self.video_table.setHorizontalHeaderLabels(['', self.tr('标题'), self.tr('时长'), self.tr('链接')])
        self.video_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for row in range(len(parse_result[0])):
            self.video_table.setCellWidget(row, 0, QCheckBox())
            self.video_table.setCellWidget(row, 1, QLabel(parse_result[0][row].get('title')))
            self.video_table.setCellWidget(row, 2, QLabel(parse_result[0][row].get('duration_string')))
            self.video_table.setCellWidget(row, 3, QLabel(parse_result[0][row].get('webpage_url')))
        self.main_layout.addWidget(self.video_table)

    def _initialize_main_layout(self):
        hbox = QHBoxLayout()
        hbox.addStretch()
        self.apply_button = QPushButton(self.tr("下载"))
        self.cancel_button = QPushButton(self.tr("取消"))
        self.cancel_button.clicked.connect(self.close)
        self.apply_button.clicked.connect(self.download)
        hbox.addWidget(self.apply_button)
        hbox.addWidget(self.cancel_button)
        self.main_layout.addLayout(hbox)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 2)

    def _initialize_window(self):
        self.setWindowTitle(self.tr("下载"))
        set_window_size(self, 0.8)
        center_ui(self)

    @Slot()
    def download(self):
        urls = {i:self.video_table.cellWidget(i, 3).text() for i in range(self.video_table.rowCount()) if self.video_table.cellWidget(i, 0).isChecked()}
        title = {i:self.video_table.cellWidget(i, 1).text() for i in range(self.video_table.rowCount()) if self.video_table.cellWidget(i, 0).isChecked()}
        self.notifier.download_start.emit(title, urls)
        self.close()

