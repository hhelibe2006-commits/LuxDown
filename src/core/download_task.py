from __future__ import annotations

import threading
from typing import Callable, Optional

from src.core.downloader import download
from src.core.exceptions import DownloadCancelled
from src.information import SettingsManager
from src.signal import Logger


class DownloadTask:
    """
    下载任务类，将原来ui里的下载逻辑抽象了出来，
    同时还提供供给yt-dlp的回调函数以及对应的取消操作
    """
    def __init__(
        self,
        url: str,
        index: int | str,
        settings: SettingsManager,
        logger: Logger,
        resolution: str,
        progress_callback: Optional[Callable[[dict], None]] = None,
        finished_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        self.url = url
        self.index = index
        self.settings = settings
        self.logger = logger
        self.resolution = resolution
        self._cancel_event = threading.Event()
        self._progress_cb = progress_callback
        self._finished_cb = finished_callback

    def cancel(self) -> None:
        self._cancel_event.set()

    def _progress_wrapper(self, d: dict) -> None:
        if self._cancel_event.is_set():
            raise DownloadCancelled("task cancelled")

        if self._progress_cb:
            self._progress_cb(d)

    def run(self) -> bool:
        try:
            success = download(
                self.url,
                self._progress_wrapper,
                self.index,
                self.settings,
                self.logger,
                self.resolution,
            )
        except Exception as e:
            try:
                self.logger.error(f"Unexpected error in DownloadTask.run: {e}")
            except Exception:
                pass
            success = False

        if self._finished_cb:
            try:
                self._finished_cb()
            except Exception as e:
                try:
                    self.logger.error(f"Exception in finished_callback: {e}")
                except Exception:
                    pass
        return success

