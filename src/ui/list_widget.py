from concurrent.futures import ThreadPoolExecutor

from PySide6.QtCore import Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem

from src.core.download_task import DownloadTask
from src.information.settings_information import settings_manager
from src.signal import Logger
from src.ui.download_task_widget import DownloadTaskWidget


class ListWidget(QListWidget):
    def __init__(self, emitter, logger: Logger):
        super().__init__()
        self.emitter = emitter
        self.logger : Logger = logger
        self.download_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=3)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.download_executor.shutdown(wait=False)
        super().closeEvent(event)
    @Slot()
    def start_download(self, titles: dict, urls: dict, resolution: dict):
        for index in urls.keys():
            list_item: QListWidgetItem = QListWidgetItem(self)
            task_widget: DownloadTaskWidget = DownloadTaskWidget(self.emitter, titles[index])
            task_widget.is_dual_download = (
                    settings_manager.download_audio and
                    settings_manager.download_video
            )
            task_widget.list_item = list_item
            list_item.setSizeHint(task_widget.sizeHint())
            self.setItemWidget(list_item, task_widget)
            def _finished_cb(item=list_item) -> None:
                # 当任务完成时通知 UI 移除对应的项
                self.emitter.download_finished.emit(item)

            download_task = DownloadTask(
                urls[index],
                index,
                settings_manager,
                self.logger,
                resolution[index],
                task_widget.progress_hook,
                _finished_cb,
            )
            task_widget.task = download_task
            self.download_executor.submit(download_task.run)


    @Slot(QListWidgetItem)
    def remove_task_item(self, item : QListWidgetItem) -> None:
        row : int = self.row(item)
        if row != -1:
            widget : QWidget = self.itemWidget(item)
            if widget is not None:
                widget.deleteLater()
            taken_item = self.takeItem(row)
            del taken_item
