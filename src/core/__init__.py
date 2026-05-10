"""
声明core为包，并简化导入
"""
__all__ = ["download", "extract_info"]
from .downloader import download
from .parser import extract_info
