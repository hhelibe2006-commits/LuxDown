"""
声明core为包，并简化导入
"""
__all__ = ["download", "extract_info"]
from src.core.downloader import download
from src.core.parser import extract_info
