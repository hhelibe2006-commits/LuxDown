from __future__ import annotations


class DownloadCancelled(Exception):
    """
    明确的下载取消异常，供下载线程捕获以进行善后处理
    """
    pass

