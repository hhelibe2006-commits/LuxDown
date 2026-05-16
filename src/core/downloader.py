"""
该文件存放调用yt-dlp进行下载的函数与类
"""
from pathlib import Path
from typing import Callable

import yt_dlp

from src.core.exceptions import DownloadCancelled
from src.core.ydl_options import build_ydl_opts
from src.information import SettingsManager
from src.signal import Logger


def download(url: str,
             progress_hook: Callable[[dict], None],
             index: int | str,
             settings: SettingsManager,
             logger: Logger,
             resolution: str) -> bool:
    """
    下载函数，供给DownloadTask使用，
    负责下载和返回下载进度给DownloadTask，
    在出现错误时会返回
    """
    # 确保下载目录存在
    Path(settings.default_download_dir).mkdir(parents=True, exist_ok=True)

    # 使用配置构建器集中管理 yt-dlp 配置
    ydl_opts = build_ydl_opts(settings, logger, index, resolution, progress_hook)

    # 如果没有启用任何格式，直接返回 False
    if 'format' not in ydl_opts and not (settings.download_audio or settings.download_video):
        try:
            logger.error('no download format enabled in settings')
        except Exception:
            pass
        return False

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
        try:
            ydl.download([url])
        except DownloadCancelled:
            # 用户取消下载
            try:
                logger.info("download cancelled by user")
            except Exception:
                pass
            return False
        except Exception as exc:  # 捕获并记录其他异常，返回 False
            try:
                logger.error(f"download failed: {exc}")
            except Exception:
                pass
            return False
    return True
