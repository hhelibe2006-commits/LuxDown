import os
import platform
from typing import Callable

from src.information import SettingsManager
from src.signal import MyLogger


def build_ydl_opts(settings: SettingsManager,
                   logger: MyLogger,
                   index: int | str,
                   resolution: str,
                   progress_hook: Callable[[dict], None]) -> dict:
    """
    yt-dlp的下载配置管理函数
    """
    outtmpl = os.path.join(settings.default_download_dir, f"{index}-%(title)s.%(ext)s")
    opts = {
        "logger": logger,
        "outtmpl": outtmpl,
        'progress_hooks': [progress_hook],
        'max_sleep_interval': 5,
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 3,
        'cookiefile': settings.cookies_file,
        'format_sort': [f"res:{resolution.split('x')[-1]}"]
    }

    if settings.download_audio and settings.download_video:
        opts['format'] = 'bestvideo+bestaudio/best'
        opts['merge_output_format'] = settings.current_video_format
    elif settings.download_audio:
        opts['format'] = 'bestaudio/best'
        opts['merge_output_format'] = settings.current_audio_format
    elif settings.download_video:
        opts['format'] = 'bestvideo'
        opts['merge_output_format'] = settings.current_video_format
    else:
        pass

    if platform.system() == 'Windows':
        opts['ffmpeg_location'] = os.path.join('ffmpeg', 'bin', 'ffmpeg.exe')
        opts['deno_path'] = os.path.join('deno', 'deno.exe')

    return opts

