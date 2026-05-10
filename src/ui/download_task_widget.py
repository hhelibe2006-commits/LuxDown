import threading

from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar, QPushButton


class SignalEmitter(QObject):
    parse_finished = Signal(tuple)
    download_start = Signal(object, object)
    progress_update = Signal(object)
    download_finished = Signal(object)
    check_update = Signal(object, object)

class DownloadTaskWidget(QWidget):
    def __init__(self, signal, title):
        super().__init__()
        self.list_item = None
        self.is_cancelled = threading.Event()
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
        self.is_cancelled.set()
        self.external_emitter.download_finished.emit(self.list_item)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def progress_hook(self, d):
        if self.is_cancelled.is_set():
            raise
        if d['status'] == 'downloading':
            self.emitter.progress_update.emit(d['_percent'])
        elif d['status'] == 'finished':
            if not self.is_dual_download:
                self.external_emitter.download_finished.emit(self.list_item)
            self.is_dual_download = False