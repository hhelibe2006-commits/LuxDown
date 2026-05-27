"""
简化导入
"""

from src.core.download_task import DownloadTask
from src.core.ydl_options import build_ydl_opts
from src.utils.text_parser import text_to_list

# 导出的公共接口
__all__ = [
    "DownloadTask",
    "text_to_list",
    "build_ydl_opts",
]
