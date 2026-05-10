from PySide6.QtCore import QObject, Signal

class MyLogger(QObject):
    log_signal : Signal = Signal(str)

    def debug(self, msg) -> None:
        self.log_signal.emit(msg)

    def warning(self, msg) -> None:
        self.log_signal.emit(msg)

    def error(self, msg) -> None:
        self.log_signal.emit(f'<span style="color: red;">{msg}</span>')

    def info(self, msg) -> None:
        self.log_signal.emit(msg)