"""
该文件存放多行转列表的函数
"""
# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QPlainTextEdit
def text_to_dict(text : QPlainTextEdit):
    """

    :param text:
    :return:
    """
    urls = text.toPlainText()
    return urls.splitlines()
