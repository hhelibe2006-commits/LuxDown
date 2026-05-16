import pytest

from src import text_to_list


def test_text_to_list_with_string():
    s = "a\n b \n\n  c  \n"
    res = text_to_list(s)
    assert res == ["a", "b", "c"]


def test_text_to_list_with_empty_string():
    assert text_to_list("") == []


def test_text_to_list_with_qplaintextedit_if_available():
    try:
        from PySide6.QtWidgets import QPlainTextEdit
    except Exception:  # pragma: no cover - optional dependency
        pytest.skip("PySide6 not available")

    editor = QPlainTextEdit()
    editor.setPlainText("one\n\n two ")
    assert text_to_list(editor) == ["one", "two"]

