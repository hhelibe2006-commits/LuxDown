"""
该文件存放多行转列表的函数
"""
# pylint: disable=no-name-in-module
from typing import Union

from PySide6.QtWidgets import QPlainTextEdit


def text_to_list(editor_or_text: Union[QPlainTextEdit, str]) -> list[str]:
    if isinstance(editor_or_text, QPlainTextEdit):
        text = editor_or_text.toPlainText()
    else:
        text = editor_or_text or ""

    return [line.strip() for line in text.splitlines() if line.strip()]
