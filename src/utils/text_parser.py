"""
该文件存放多行转列表的函数
"""
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QPlainTextEdit
def text_to_list(editor : QPlainTextEdit) -> list[str]:
    """

    :param editor:
    :return:
    """
    urls : str = editor.toPlainText()
    return urls.splitlines()
