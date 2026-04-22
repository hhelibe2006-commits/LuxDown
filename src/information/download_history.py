"""
该文件存放调用sqlite3存储下载记录的函数与类
"""
import sqlite3
class DownloadHistory:
    def __init__(self):
        self.history_list = ('title', 'time', 'url', )
        sqlite3.connect('./data/history.db')
