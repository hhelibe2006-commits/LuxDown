import sys
from src.utils import is_url, text_to_dict
from PySide6.QtWidgets import QPlainTextEdit, QApplication


def test_is_url():
    #测试谷歌链接
    assert is_url('https://www.google.com') == True
    #测试随机字符串
    assert is_url('sdfjvb') == False
    #测试ip地址
    assert is_url('https://1.1.1.1') == True
    #测试不带协议的链接
    assert is_url('www.google.com') == False
    #测试协议大写的链接
    assert is_url('HTTPS://www.google.com') == True
    #测试空字符串
    assert is_url('') == False
    #测试带端口的链接
    assert is_url('http://127.0.0.1:3000') == True


def test_text_to_dict():
    app = QApplication(sys.argv)
    assert text_to_dict(QPlainTextEdit()) == []
    assert text_to_dict(QPlainTextEdit("sdf\nsdvfj\nsdf")) == ["sdf", "sdvfj", "sdf"]

