import threading

from PySide6.QtCore import Signal, QObject, Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar, QPushButton

from signal import SignalEmitter

class DownloadTaskWidget(QWidget):
    def __init__(self, signal : SignalEmitter, title : str) -> None:
        super().__init__()
        self.list_item = None
        self.is_cancelled : threading.Event = threading.Event()
        self.is_dual_download : bool = False
        self.external_emitter : SignalEmitter = signal
        self.emitter : SignalEmitter = SignalEmitter()
        self.hbox : QHBoxLayout = QHBoxLayout()
        self.label : QLabel = QLabel(title)
        self.hbox.addWidget(self.label)
        self.progress_bar : QProgressBar = QProgressBar()
        self.progress_bar.setValue(0)
        self.hbox.addWidget(self.progress_bar)
        self.button : QPushButton = QPushButton(self.tr("取消"))
        self.hbox.addWidget(self.button)
        self.setLayout(self.hbox)
        self.button.clicked.connect(self.on_cancel_clicked)
        self.emitter.progress_update.connect(self.update_progress)

    @Slot()
    def on_cancel_clicked(self) -> None:
        self.is_cancelled.set()
        self.external_emitter.download_finished.emit(self.list_item)

    @Slot(int)
    def update_progress(self, value : int) -> None:
        self.progress_bar.setValue(value)

    def progress_hook(self, d : dict) -> None:
        if self.is_cancelled.is_set():
            raise
        if d['status'] == 'downloading':
            self.emitter.progress_update.emit(int(d['_percent']))
        elif d['status'] == 'finished':
            if not self.is_dual_download:
                self.external_emitter.download_finished.emit(self.list_item)
            self.is_dual_download = False