from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QListWidgetItem


class SignalEmitter(QObject):
    parse_finished : Signal = Signal(tuple)
    download_start : Signal = Signal(object, object, object)
    progress_update : Signal = Signal(int)
    download_finished : Signal = Signal(QListWidgetItem)
    check_update : Signal = Signal(str, str, bool, str)