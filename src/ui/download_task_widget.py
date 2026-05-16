import threading

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar, QPushButton

from src.core.exceptions import DownloadCancelled
from src.signal import SignalEmitter


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
        # 如果绑定了 DownloadTask，则调用其 cancel 方法；否则回退到发送下载完成信号以移除 UI 项
        task = getattr(self, 'task', None)
        if task is not None:
            try:
                task.cancel()
            except Exception:
                # 在极少数情况下回退到立即移除项，并记录异常
                try:
                    import logging

                    logging.exception("Failed to cancel associated DownloadTask")
                except Exception:
                    pass
                self.external_emitter.download_finished.emit(self.list_item)
        else:
            self.external_emitter.download_finished.emit(self.list_item)

    @Slot(int)
    def update_progress(self, value : int) -> None:
        self.progress_bar.setValue(value)

    def progress_hook(self, d : dict) -> None:
        # 当用户请求取消时抛出明确的异常，供下载线程捕获并做善后处理
        if self.is_cancelled.is_set():
            raise DownloadCancelled("user cancelled")

        status = d.get('status')
        if status == 'downloading':
            # yt-dlp 可能把百分比放在 '_percent' 或 'percent'，并且可能是字符串
            percent = d.get('_percent') or d.get('percent')
            if isinstance(percent, (int, float, str)):
                try:
                    # 转为整数显示（先转为字符串以满足静态类型检查）
                    self.emitter.progress_update.emit(int(float(str(percent))))
                except (TypeError, ValueError):
                    # 忽略无法解析的百分比
                    pass
        elif status == 'finished':
            if not self.is_dual_download:
                self.external_emitter.download_finished.emit(self.list_item)
            # 重置双轨下载标记
            self.is_dual_download = False