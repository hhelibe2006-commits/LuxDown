from PySide6.QtCore import QObject, Signal


class SignalEmitter(QObject):
    parse_finished : Signal = Signal(tuple)
    download_start : Signal = Signal(object, object)
    progress_update : Signal = Signal(object)
    download_finished : Signal = Signal(object)
    check_update : Signal = Signal(object, object)