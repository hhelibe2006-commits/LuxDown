from PySide6.QtWidgets import QPlainTextEdit
def text_to_dict(text : QPlainTextEdit):
    urls = text.toPlainText()
    return urls.splitlines()