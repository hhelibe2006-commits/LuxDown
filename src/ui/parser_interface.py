from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QTableWidget
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from utils import set_window_size, center_ui

class ParsyParser(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("下载")
        self.verticalLayout_2 = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        self.webEngineView = QWebEngineView()
        self.webEngineView.setUrl(QUrl(parent[2]))
        self.horizontalLayout.addWidget(self.webEngineView)
        self.verticalLayout = QVBoxLayout()
        self.lineEdit = QLabel(parent[1])
        self.verticalLayout.addWidget(self.lineEdit)
        self.textEdit = QTextBrowser()
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tableWidget = QTableWidget()
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)

    def initialize(self):
        self.initialize_windows()

    def initialize_windows(self):
        self.setWindowTitle("解析")
        set_window_size(self, 0.8)
        center_ui(self)

