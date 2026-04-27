from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QTableWidget, QCheckBox, \
    QHeaderView, QPushButton
from PySide6.QtCore import QUrl, Slot, QObject, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from utils import set_window_size, center_ui


class ParsyParser(QDialog):
    def __init__(self, parent:tuple, signal):
        super().__init__()
        self.title = parent[-2]
        self.signal = signal
        self.verticalLayout_2 = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()

        self.webEngineView = QWebEngineView()
        self.webEngineView.setUrl(QUrl(parent[-1]))
        self.horizontalLayout.addWidget(self.webEngineView)

        self.verticalLayout = QVBoxLayout()
        self.lineEdit = QLabel(parent[-2])
        self.verticalLayout.addWidget(self.lineEdit)

        self.textEdit = QTextBrowser()
        self.textEdit.setPlainText(parent[-3])
        self.verticalLayout.addWidget(self.textEdit)

        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(len(parent[0]), 4)
        self.tableWidget.setHorizontalHeaderLabels(['','标题','时长','链接'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(len(parent[0])):
            self.tableWidget.setCellWidget(i, 0, QCheckBox())
            self.tableWidget.setCellWidget(i, 1, QLabel(parent[0][i].get('title')))
            self.tableWidget.setCellWidget(i, 2, QLabel(parent[0][i].get('duration_string')))
            self.tableWidget.setCellWidget(i, 3, QLabel(parent[0][i].get('webpage_url')))

        self.verticalLayout_2.addWidget(self.tableWidget)

        hbox = QHBoxLayout()
        hbox.addStretch()
        self.apply_button = QPushButton("下载")
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.close)
        self.apply_button.clicked.connect(self.download)
        hbox.addWidget(self.apply_button)
        hbox.addWidget(self.cancel_button)

        self.verticalLayout_2.addLayout(hbox)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)

    def initialize(self):
        self.__initialize_windows()

    def __initialize_windows(self):
        self.setWindowTitle("下载")
        set_window_size(self, 0.8)
        center_ui(self)

    @Slot()
    def download(self):
        urls = {i:self.tableWidget.cellWidget(i,3).text() for i in range(self.tableWidget.rowCount()) if self.tableWidget.cellWidget(i, 0).isChecked()}
        self.signal.closed.emit(urls)
        self.close()

