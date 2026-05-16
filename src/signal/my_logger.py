import logging
from logging import Logger

from PySide6.QtCore import QObject, Signal


class Logger(QObject):
    log_signal: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._logger : Logger = logging.getLogger('LuxDown')

    def debug(self, msg) -> None:
        try:
            self._logger.debug(msg)
        finally:
            self.log_signal.emit(str(msg))

    def warning(self, msg) -> None:
        try:
            self._logger.warning(msg)
        finally:
            self.log_signal.emit(str(msg))

    def error(self, msg) -> None:
        try:
            self._logger.error(msg)
        finally:
            self.log_signal.emit(f'<span style="color: red;">{msg}</span>')

    def info(self, msg) -> None:
        try:
            self._logger.info(msg)
        finally:
            self.log_signal.emit(str(msg))
