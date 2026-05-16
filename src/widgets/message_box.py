from PySide6.QtWidgets import QMessageBox

class MessageBox(QMessageBox):
    def __init__(self, parent = None, title = '', text = '', buttons = QMessageBox.StandardButton.Ok, icon = QMessageBox.Icon.Information):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(icon)
        self.setButtonText(QMessageBox.StandardButton.Ok, '确认')
        self.setButtonText(QMessageBox.StandardButton.Yes, '下载')
        self.setButtonText(QMessageBox.StandardButton.No, '取消')
        self.setStandardButtons(buttons)
